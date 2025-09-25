from datetime import datetime, timezone
import asyncio
from app.tasks.celery import celery_app
from app.database.session import SessionLocal
from app.crud.post import PostCRUD
from app.core.mock_platforms import MockPlatformFactory, PlatformError
from app.models.enums import PostStatus
from app.utils.logger import get_logger
from sqlalchemy import and_, text

logger = get_logger(__name__)

@celery_app.task
def publish_post_task(post_id: int):
    """Fetches a scheduled post, and publishes it to the target social media platform."""
    logger.info(f"Executing publish_post_task for post ID: {post_id}")
    db = SessionLocal()

    try:
        # Use raw SQL to get post details without loading relationships
        post_query = text("""
            SELECT p.id, p.content_text, p.status, p.image_id, sp.type as platform_type
            FROM posts p
            JOIN social_platforms sp ON p.platform_id = sp.id
            WHERE p.id = :post_id
        """)

        result = db.execute(post_query, {"post_id": post_id})
        post_row = result.fetchone()

        if not post_row:
            logger.warning(f"Post {post_id} not found.")
            return

        post_db_id, content_text, status, image_id, platform_type = post_row

        if status != PostStatus.SCHEDULED.value:
            logger.warning(f"Post {post_id} is not in a scheduled state (current state: {status}). Aborting.")
            return

        # Get image path if exists
        image_path = None
        if image_id:
            image_query = text("SELECT path FROM images WHERE id = :image_id")
            image_result = db.execute(image_query, {"image_id": image_id})
            image_row = image_result.fetchone()
            if image_row:
                image_path = image_row[0]

        # Get platform instance
        mock_platform = MockPlatformFactory.get_platform(platform_type.lower())

        # Parse content_text JSON
        import json
        content_json = json.loads(content_text) if isinstance(content_text, str) else content_text

        content_payload = {
            "text": content_json.get("text", ""),
        }
        if image_path:
            content_payload["image"] = image_path

        logger.info(f"Publishing post {post_id} to {platform_type}...")

        # Run the async post_content method in the sync celery task
        response = asyncio.run(mock_platform.post_content(content_payload))

        # Update post status using raw SQL
        now = datetime.now(timezone.utc)

        if response.success:
            update_query = text("""
                UPDATE posts
                SET status = 'PUBLISHED', published_at = :now, remarks = :remarks
                WHERE id = :post_id
            """)
            remarks = f"Successfully published. Platform ID: {response.data.get('post_id')}"
            db.execute(update_query, {"now": now, "remarks": remarks, "post_id": post_id})
            logger.info(f"Post {post_id} successfully published to {platform_type}.")
        else:
            update_query = text("""
                UPDATE posts
                SET status = 'FAILED', remarks = :remarks
                WHERE id = :post_id
            """)
            remarks = response.error or "Unknown error from platform."
            db.execute(update_query, {"remarks": remarks, "post_id": post_id})
            logger.error(f"Failed to publish post {post_id} to {platform_type}: {response.error}")

    except PlatformError as e:
        update_query = text("UPDATE posts SET status = 'FAILED', remarks = :remarks WHERE id = :post_id")
        remarks = f"Platform Error: {e.message} (Code: {e.code})"
        db.execute(update_query, {"remarks": remarks, "post_id": post_id})
        logger.error(f"Platform error for post {post_id}: {e.message}")
    except Exception as e:
        update_query = text("UPDATE posts SET status = 'FAILED', remarks = :remarks WHERE id = :post_id")
        remarks = f"An unexpected error occurred: {str(e)}"
        db.execute(update_query, {"remarks": remarks, "post_id": post_id})
        logger.error(f"An unexpected error occurred while publishing post {post_id}: {e}", exc_info=True)

    finally:
        db.commit()
        db.close()


@celery_app.task
def check_scheduled_posts():
    """Periodic task that checks for scheduled posts ready to be published."""
    logger.info("Checking for scheduled posts ready to be published...")
    db = SessionLocal()

    try:
        # Get current time
        now = datetime.now(timezone.utc)
        logger.info(f"Current time (UTC): {now}")

        # Use raw SQL query to avoid SQLAlchemy relationship issues in Celery
        query = text("""
            SELECT id, schedule_time
            FROM posts
            WHERE status = 'SCHEDULED'
            AND schedule_time <= :now
        """)

        result = db.execute(query, {"now": now})
        scheduled_posts = result.fetchall()

        logger.info(f"Found {len(scheduled_posts)} posts ready for publishing")

        # Trigger publish_post_task for each ready post
        for post_row in scheduled_posts:
            post_id = post_row[0]  # First column is id
            schedule_time = post_row[1]  # Second column is schedule_time
            logger.info(f"Triggering publish task for post {post_id} (scheduled for {schedule_time})")
            publish_post_task.delay(post_id)

        return f"Processed {len(scheduled_posts)} scheduled posts"

    except Exception as e:
        logger.error(f"Error in check_scheduled_posts: {e}", exc_info=True)
        return f"Error: {str(e)}"
    finally:
        db.close()
