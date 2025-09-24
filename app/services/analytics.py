from typing import List, Optional, Dict
from datetime import datetime
from sqlalchemy.orm import Session

from app.crud.analytics import AnalyticsCRUD
from app.crud.api import ApiCRUD # Needed for AIProviderFactory
from app.schemas.analytics import PostSummaryResponse, AiInsightResponse
from app.models.enums import PlatformType, PostStatus
from app.services.ai_providers import AIProviderFactory
from app.utils.logger import get_logger

logger = get_logger(__name__)

class AnalyticsService:
    def __init__(self, db: Session):
        self.db = db
        self.analytics_crud = AnalyticsCRUD(db)
        self.api_crud = ApiCRUD(db) # Initialize ApiCRUD for AIProviderFactory
        self.ai_factory = AIProviderFactory(self.api_crud)

    def get_post_summary(
        self,
        user_id: Optional[int] = None,
        platform_type: Optional[PlatformType] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> PostSummaryResponse:
        counts_by_status = self.analytics_crud.get_post_counts_by_status(
            user_id=user_id,
            platform_type=platform_type,
            start_date=start_date,
            end_date=end_date
        )

        total_posts = sum(counts_by_status.values())

        return PostSummaryResponse(
            total_posts=total_posts,
            published_count=counts_by_status.get(PostStatus.PUBLISHED, 0),
            scheduled_count=counts_by_status.get(PostStatus.SCHEDULED, 0),
            failed_count=counts_by_status.get(PostStatus.FAILED, 0),
            draft_count=counts_by_status.get(PostStatus.DRAFT, 0),
            # Add other statuses here if needed
        )

    async def get_ai_insight(self, user_id: int, query: Optional[str] = None) -> AiInsightResponse:
        provider = self.ai_factory.get_provider(user_id)
        insight_text = await provider.generate_insight(query)
        return AiInsightResponse(insight_text=insight_text)
 