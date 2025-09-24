from typing import List, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.models.product import Product
from app.crud.product import ProductCRUD
from app.schemas.product import ProductResponse

class ProductCustomizationService:
    def __init__(self, db: Session):
        self.db = db
        self.product_crud = ProductCRUD(db)

    def customize(self, user_id: int, product_id: int, custom_text: str) -> ProductResponse:
        product = self.product_crud.get(product_id)
        if not product or product.user_id != user_id:
            return None
        product.custom_text = custom_text
        product.customize_count = (product.customize_count or 0) + 1
        product.last_customized_at = datetime.now(timezone.utc)
        product = self.product_crud.update(product)
        return ProductResponse(
            id=product.id,
            name=product.name,
            category=product.category,
            price=float(product.price),
            image_id=product.image_id,
            description=product.description,
        )

    def list(self, user_id: Optional[int] = None) -> List[Product]:
        return self.product_crud.list_by_user(user_id) 