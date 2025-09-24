from pydantic import BaseModel
from typing import Optional

class DashboardStats(BaseModel):
    posts_published: int
    scheduled: int
    failed: int

class InsightRequest(BaseModel):
    query: Optional[str] = None
    platform: Optional[str] = None

class InsightResponse(BaseModel):
    insight: str

class AnalyticsService:
    def get_stats(self) -> DashboardStats:
        return DashboardStats(posts_published=5, scheduled=3, failed=1)

    def get_insight(self, req: InsightRequest) -> InsightResponse:
        prefix = f"Platform {req.platform}: " if req.platform else ""
        q = req.query or "Posting performance is strong in the morning."
        return InsightResponse(insight=f"{prefix}{q}") 