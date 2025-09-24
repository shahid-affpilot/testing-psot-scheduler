from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.post import Post
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