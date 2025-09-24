from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict
from datetime import datetime

from .enums import PlatformType, PostTone, PostStatus, ProductCategory

class PlatformItem(BaseModel):
    platform: PlatformType
    platform_id: int

class PostSubmitRequest(BaseModel):
    user_id: int
    content_text: str
    platform_list: Optional[List[PlatformItem]] = None  # List of platform types with their IDs
    product_id: Optional[int] = None
    schedule_time: Optional[datetime] = None
    content_tone: PostTone = PostTone.CASUAL
    hashtags: Optional[List[str]] = None
    target_audience: Optional[str] = None
    image_url: Optional[str] = None
    api_ids: Optional[List[int]] = None

class ImageResponse(BaseModel):
    id: int
    path: str

class PostSubmitResData(BaseModel):
    platforms: List[PlatformType]
    product_id: Optional[int] = None
    schedule_time: Optional[datetime] = None
    status: PostStatus
    hashtags: List[str]
    target_audience: Optional[str] = None

class PostSubmitResponse(BaseModel):
    status_code: int
    status_type: str
    message: str
    data: PostSubmitResData

class AISuggestionsRequest(BaseModel):
    user_id: int
    content_text: str
    product_category: Optional[ProductCategory] = None
    platform_types: List[PlatformType]
    target_audience: Optional[str] = None
    brand_tone: PostTone = PostTone.CASUAL

class ContentReview(BaseModel):
    score: int = Field(..., ge=0, le=100)
    suggestions: List[str]

class AISuggestionsResponse(BaseModel):
    hashtag_suggestions: List[str]
    content_review: ContentReview
    optimized_content: str

class ProductInfo(BaseModel):
    id: int
    name: str
    category: ProductCategory
    price: float

class PostListItem(BaseModel):
    id: int
    content_text: str
    image: Optional[ImageResponse] = None
    platforms: List[PlatformType]
    product_id: Optional[int] = None
    schedule_time: Optional[datetime] = None
    status: PostStatus
    hashtags: List[str]
    created_at: datetime

class PostListResponse(BaseModel):
    posts: List[PostListItem]
    total: int
    limit: int
    offset: int

class PostDetailResponse(BaseModel):
    id: int
    user_id: int
    content_text: str
    image: Optional[ImageResponse] = None
    platforms: List[PlatformType]
    product: Optional[ProductInfo] = None
    schedule_time: Optional[datetime] = None
    published_at: Optional[datetime] = None
    status: PostStatus
    hashtags: List[str]
    target_audience: Optional[str] = None
    call_to_action: Optional[str] = None
    content_tone: PostTone
    created_at: datetime
    modified_at: datetime
