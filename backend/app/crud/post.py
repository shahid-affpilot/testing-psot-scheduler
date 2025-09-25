from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
from datetime import datetime
from app.models.post import Post
from app.models.enums import PostStatus
from app.crud.base import BaseCRUD

class PostCRUD(BaseCRUD):
    def get(self, post_id: int) -> Optional[Post]:
        return self.db.query(Post).filter(Post.id == post_id).first()

    def list(self, limit: int, offset: int) -> List[Post]:
        return (
            self.db.query(Post)
            .order_by(Post.created_at.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )

    def count(self) -> int:
        return self.db.query(Post).count()

    def create(self, post: Post) -> Post:
        return self.commit_and_refresh(post)

    def update(self, post: Post) -> Post:
        return self.commit_and_refresh(post)

    def list_scheduled_ready_to_publish(self, now: datetime) -> List[Post]:
        """Get all scheduled posts that are ready to be published (schedule_time <= now)"""
        return self.db.query(Post).filter(
            and_(
                Post.status == PostStatus.SCHEDULED,
                Post.schedule_time <= now
            )
        ).options().all()  # Use options() to avoid relationship loading issues 