from sqlalchemy import Column, String, Integer, BigInteger, Boolean, DateTime, Text, JSON, Numeric, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import func
import enum
from typing import Optional
from datetime import datetime

from .base_model import BaseModel
from .enums import ProductCategory


class Product(BaseModel):
    __tablename__ = "products"

    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    custom_text = Column(String(255), nullable=True)
    customize_count = Column(Integer, default=0, nullable=False)
    last_customized_at = Column(DateTime(timezone=True), nullable=True)
    image_id = Column(BigInteger, ForeignKey("images.id"), nullable=True)
    category = Column(SQLEnum(ProductCategory), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    user_id = Column(BigInteger, nullable=False)  # should be fk of user table
    sell_count = Column(Integer, default=0)
    available = Column(Boolean, default=True)
    ongoing_order = Column(Integer, default=0)
    comment_id = Column(BigInteger, nullable=True)  # should be fk of comment table
    click = Column(Integer, default=0)

    # Relationships
    image = relationship("Image", back_populates="products")
    posts = relationship("Post", back_populates="product")
