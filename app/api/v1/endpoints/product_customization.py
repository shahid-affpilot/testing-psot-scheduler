from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas.product import (
    ProductCustomizationRequest,
    ProductCustomizationDetailResponse,
    ProductCustomizationListResponse,
    ProductCustomizationItem
)
from app.dependencies import get_db
from app.services.product_customization import ProductCustomizationService


router = APIRouter()

@router.post("/product-customization", response_model=ProductCustomizationDetailResponse)
def create_customization(payload: ProductCustomizationRequest, db: Session = Depends(get_db)):
    service = ProductCustomizationService(db)
    result = service.customize(user_id=payload.user_id, product_id=payload.product_id, custom_text=payload.custom_text)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    # Enrich with extra fields from ORM when building response list below
    product = db.query(type(result)).first()  # placeholder not used here
    return ProductCustomizationDetailResponse(
        id=result.id,
        name=result.name,
        custom_text=payload.custom_text,
        image_path=None,
        category=result.category,
        price=result.price,
        last_customized_at=None,
        description=result.description,
    )

@router.get("/customized-product", response_model=ProductCustomizationListResponse)
def list_customizations(user_id: Optional[int] = None, db: Session = Depends(get_db)):
    service = ProductCustomizationService(db)
    items = service.list(user_id)
    resp = [
        ProductCustomizationItem(
            id=p.id,
            name=p.name,
            custom_text=p.custom_text,
            image_path=p.image.path if p.image else None,
            category=p.category,
            price=float(p.price),
            last_customized_at=p.last_customized_at,
        ) for p in items
    ]
    return ProductCustomizationListResponse(items=resp, total=len(resp))

@router.get("/customized-product/{product_id}", response_model=ProductCustomizationDetailResponse)
def get_customization(product_id: int, db: Session = Depends(get_db)):
    service = ProductCustomizationService(db)
    p = service.product_crud.get(product_id)
    if not p:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return ProductCustomizationDetailResponse(
        id=p.id,
        name=p.name,
        custom_text=p.custom_text,
        image_path=p.image.path if p.image else None,
        category=p.category,
        price=float(p.price),
        last_customized_at=p.last_customized_at,
        description=p.description,
    ) 