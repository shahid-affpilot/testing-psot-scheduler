from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.product import Product
from app.crud.base import BaseCRUD

class ProductCRUD(BaseCRUD):
    def get(self, product_id: int) -> Optional[Product]:
        return self.db.query(Product).filter(Product.id == product_id).first()

    def list_by_user(self, user_id: Optional[int] = None) -> List[Product]:
        q = self.db.query(Product)
        if user_id:
            q = q.filter(Product.user_id == user_id)
        return q.order_by(Product.last_customized_at.desc().nullslast()).all()

    def update(self, product: Product) -> Product:
        return self.commit_and_refresh(product) 