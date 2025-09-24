from sqlalchemy.orm import Session
from typing import Optional
from app.models.social_platform import SocialPlatform
from app.models.enums import PlatformType
from app.crud.base import BaseCRUD

class SocialPlatformCRUD(BaseCRUD):
    def get_by_user_and_type(self, user_id: int, platform_type: PlatformType) -> Optional[SocialPlatform]:
        return (
            self.db.query(SocialPlatform)
            .filter(SocialPlatform.user_id == user_id, SocialPlatform.type == platform_type)
            .first()
        )

    def create(self, platform: SocialPlatform) -> SocialPlatform:
        return self.commit_and_refresh(platform) 