from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from .enums import ProductCategory

class ProductCreate(BaseModel):
    name: str
    category: ProductCategory
    price: float
    image_id: Optional[int] = None
    description: Optional[str] = None

class ProductResponse(BaseModel):
    id: int
    name: str
    category: ProductCategory
    price: float
    image_id: Optional[int] = None
    description: Optional[str] = None

class ProductCustomizationRequest(BaseModel):
    user_id: int
    product_id: int
    custom_text: str

class ProductCustomizationItem(BaseModel):
    id: int
    name: str
    custom_text: Optional[str] = None
    image_path: Optional[str] = None
    category: ProductCategory
    price: float
    last_customized_at: Optional[datetime] = None

class ProductCustomizationListResponse(BaseModel):
    items: List[ProductCustomizationItem]
    total: int

class ProductCustomizationDetailResponse(ProductCustomizationItem):
    description: Optional[str] = None