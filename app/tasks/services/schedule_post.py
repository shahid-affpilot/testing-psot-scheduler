from datetime import datetime, timezone
from app.tasks.celery import celery_app
from app.database.session import SessionLocal
from app.models.post import Post
from app.crud.post import PostCRUD

@celery_app.task
def publish_post_task(post_id: int):
    """Mark a scheduled post as published."""
    db = SessionLocal()
    post_crud = PostCRUD(db)
    post = post_crud.get(post_id)
    if post and post.status == "SCHEDULED":
        post.status = "PUBLISHED"
        post.published_at = datetime.now(timezone.utc)
        db.commit()
    db.close()
