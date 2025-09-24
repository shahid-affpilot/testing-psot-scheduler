from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.analytics import AnalyticsService, DashboardStats, InsightRequest, InsightResponse

router = APIRouter()

@router.get("/post-dashboard", response_model=DashboardStats)
def get_dashboard_stats():
    svc = AnalyticsService()
    return svc.get_stats()

@router.post("/ai-insight", response_model=InsightResponse)
def ai_insight(req: InsightRequest):
    svc = AnalyticsService()
    return svc.get_insight(req) 