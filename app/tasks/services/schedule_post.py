from datetime import datetime, timezone
import asyncio
from app.tasks.celery import celery_app
from app.database.session import SessionLocal
from app.crud.post import PostCRUD
from app.core.mock_platforms import MockPlatformFactory, PlatformError
from app.models.enums import PostStatus
from app.utils.logger import get_logger

logger = get_logger(__name__)

@celery_app.task
def publish_post_task(post_id: int):
    """Fetches a scheduled post, and publishes it to the target social media platform."""
    logger.info(f"Executing publish_post_task for post ID: {post_id}")
    db = SessionLocal()
    post_crud = PostCRUD(db)
    post = post_crud.get(post_id)

    if not post:
        logger.warning(f"Post {post_id} not found.")
        db.close()
        return

    if post.status != PostStatus.SCHEDULED:
        logger.warning(f"Post {post_id} is not in a scheduled state (current state: {post.status}). Aborting.")
        db.close()
        return

    try:
        platform_type = post.platform.type.value
        mock_platform = MockPlatformFactory.get_platform(platform_type)
        
        content_payload = {
            "text": post.content_text.get("text", ""),
        }
        if post.image:
            content_payload["image"] = post.image.path

        logger.info(f"Publishing post {post_id} to {platform_type}...")
        
        # Run the async post_content method in the sync celery task
        response = asyncio.run(mock_platform.post_content(content_payload))

        if response.success:
            post.status = PostStatus.PUBLISHED
            post.published_at = datetime.now(timezone.utc)
            post.remarks = f"Successfully published. Platform ID: {response.data.get('post_id')}"
            logger.info(f"Post {post_id} successfully published to {platform_type}.")
        else:
            # This case might not be hit if post_content raises exceptions for failures
            post.status = PostStatus.FAILED
            post.remarks = response.error or "Unknown error from platform."
            logger.error(f"Failed to publish post {post_id} to {platform_type}: {response.error}")

    except PlatformError as e:
        post.status = PostStatus.FAILED
        post.remarks = f"Platform Error: {e.message} (Code: {e.code})"
        logger.error(f"Platform error for post {post_id}: {e.message}")
    except Exception as e:
        post.status = PostStatus.FAILED
        post.remarks = f"An unexpected error occurred: {str(e)}"
        logger.error(f"An unexpected error occurred while publishing post {post_id}: {e}", exc_info=True)
    
    finally:
        db.commit()
        db.close()
