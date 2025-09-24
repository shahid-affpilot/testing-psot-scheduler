from datetime import datetime, timezone
from app.tasks.celery import celery_app
from app.database.session import SessionLocal
from app.models.post import Post
from app.crud.post import PostCRUD
from app.utils.logger import get_logger

logger = get_logger(__name__)

@celery_app.task
def publish_post_task(post_id: int):
    """Mark a scheduled post as published."""
    logger.info(f"Executing publish_post_task for post ID: {post_id}")
    db = SessionLocal()
    post_crud = PostCRUD(db)
    post = post_crud.get(post_id)
    if post and post.status == "SCHEDULED":
        post.status = "PUBLISHED"
        post.published_at = datetime.now(timezone.utc)
        db.commit()
        logger.info(f"Post {post_id} has been published.")
    else:
        logger.warning(f"Post {post_id} not found or not in scheduled state.")
    db.close()
