from typing import List, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.models.post import Post
from app.models.image import Image
from app.models.social_platform import SocialPlatform
from app.models.enums import PlatformType, PostStatus, PostTone, ImageType, PostType
from app.schemas.post import (
    PostSubmitRequest, PostSubmitResData, PostSubmitResponse, PostListResponse, PostListItem,
    PostDetailResponse, ImageResponse, AISuggestionsRequest, AISuggestionsResponse,
)
from app.crud.post import PostCRUD
from app.crud.image import ImageCRUD
from app.crud.social_platform import SocialPlatformCRUD
from app.crud.api import ApiCRUD
from app.services.ai_providers import AIProviderFactory
from app.tasks.services.schedule_post import publish_post_task


# Orchestrates post business logic: create/list/detail and AI utilities
class PostService:
    def __init__(self, db: Session):
        self.db = db
        self.post_crud = PostCRUD(db)
        self.image_crud = ImageCRUD(db)
        self.platform_crud = SocialPlatformCRUD(db)
        self.api_crud = ApiCRUD(db)
        self.ai_factory = AIProviderFactory(self.api_crud)

    # Ensure a SocialPlatform exists for the user and platform
    def _get_or_create_platform(self, user_id: int, platform_type: PlatformType) -> SocialPlatform:
        platform = self.platform_crud.get_by_user_and_type(user_id, platform_type)
        if platform:
            return platform
        platform = SocialPlatform(name=platform_type.value.capitalize(), type=platform_type, user_id=user_id)
        self.platform_crud.create(platform)
        return platform

    # Create post(s) per selected platforms; attach image from file or URL
    def submit(self, payload: PostSubmitRequest, image_file_path: Optional[str] = None) -> PostSubmitResponse:
        image_obj: Optional[Image] = None
        if image_file_path:
            image_obj = Image(type=ImageType.FILE, path=image_file_path)
            self.image_crud.create(image_obj)
        elif getattr(payload, "image_url", None):
            image_obj = Image(type=ImageType.URL, path=payload.image_url)
            self.image_crud.create(image_obj)

        platform_list = payload.platform_list

        created_posts: List[Post] = []
        for platform in platform_list:
            platform_type, platform_id = list(platform.items())[0]
            platform = self._get_or_create_platform(payload.user_id, platform_type)
            content_json = {
                "text": payload.content_text,
                "hashtags": payload.hashtags or [],
                "target_audience": payload.target_audience,
            }
            status_val = PostStatus.SCHEDULED if payload.schedule_time else PostStatus.PUBLISHED
            published_at = None
            if not payload.schedule_time:
                published_at = datetime.now(timezone.utc)
            post = Post(
                type=PostType.IMAGE if image_obj else PostType.TEXT,
                content_text=content_json,
                content_tone=payload.content_tone,
                platform_id=platform.id,
                product_id=payload.product_id,
                image_id=image_obj.id if image_obj else None,
                user_id=payload.user_id,
                schedule_time=payload.schedule_time,
                status=status_val,
                api_ids=payload.api_ids,
                published_at=published_at,
            )
            self.post_crud.create(post)
            created_posts.append(post)

            # Schedule via Celery if scheduled
            if payload.schedule_time:
                publish_post_task.apply_async(
                    args=[post.id],
                    eta=payload.schedule_time  # datetime object in UTC
                )

        first = created_posts[0]
        image_resp = ImageResponse(id=first.image.id, path=first.image.path) if first.image else None

        return PostSubmitResponse(
            status_code=200,
            status_type="success",
            message="Post submitted successfully",
            data=PostSubmitResData(
                platforms=[p.platform_type for p in created_posts],  # updated attribute name
                product_id=payload.product_id,
                schedule_time=payload.schedule_time,
                status=first.status,
                hashtags=payload.hashtags or [],
                target_audience=payload.target_audience,
            )
        )

    # Paginated list with light mapping to response schema
    def list(self, limit: int, offset: int) -> PostListResponse:
        items = self.post_crud.list(limit=limit, offset=offset)
        total = self.post_crud.count()
        return PostListResponse(
            posts=[self._to_list_item(p) for p in items],
            total=total,
            limit=limit,
            offset=offset,
        )

    # Single post detail view mapping
    def detail(self, post_id: int) -> Optional[PostDetailResponse]:
        post = self.post_crud.get(post_id)
        if not post:
            return None
        return self._to_detail(post)

    # AI hashtag + content analysis via provider selected per user
    async def suggest_hashtags(self, user_id: int, payload: AISuggestionsRequest) -> AISuggestionsResponse:
        provider = self.ai_factory.get_provider(user_id)
        tags = await provider.suggest_hashtags(payload.content_text, [p.value for p in payload.platform_types])
        analysis = await provider.analyze_content(payload.content_text)
        return AISuggestionsResponse(
            hashtag_suggestions=tags,
            content_review=analysis,
            optimized_content=f"{payload.content_text} {' '.join(tags[:3])}",
        )

    # Lightweight insight helper (used by analytics)
    async def generate_insight(self, user_id: int, query: Optional[str]) -> str:
        provider = self.ai_factory.get_provider(user_id)
        return await provider.generate_insight(query)

    def _to_list_item(self, p: Post) -> PostListItem:
        image = ImageResponse(id=p.image.id, path=p.image.path) if p.image else None
        return PostListItem(
            id=p.id,
            content_text=p.content_text.get("text") if isinstance(p.content_text, dict) else str(p.content_text),
            image=image,
            platforms=[p.platform.type],
            product_id=p.product_id,
            schedule_time=p.schedule_time,
            status=p.status,
            hashtags=p.content_text.get("hashtags", []) if isinstance(p.content_text, dict) else [],
            created_at=p.created_at,
        )

    def _to_detail(self, p: Post) -> PostDetailResponse:
        image = ImageResponse(id=p.image.id, path=p.image.path) if p.image else None
        return PostDetailResponse(
            id=p.id,
            user_id=p.user_id,
            content_text=p.content_text.get("text") if isinstance(p.content_text, dict) else str(p.content_text),
            image=image,
            platforms=[p.platform.type],
            product=None,
            schedule_time=p.schedule_time,
            published_at=p.published_at,
            status=p.status,
            hashtags=p.content_text.get("hashtags", []) if isinstance(p.content_text, dict) else [],
            target_audience=p.content_text.get("target_audience") if isinstance(p.content_text, dict) else None,
            call_to_action=p.content_text.get("call_to_action") if isinstance(p.content_text, dict) else None,
            content_tone=p.content_tone,
            created_at=p.created_at,
            modified_at=p.modified_at,
        ) 