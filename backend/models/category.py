from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base  # Assure-toi d'importer la base de données correctement

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text, nullable=True)
    parent_category_id = Column(Integer, ForeignKey('categories.id'), nullable=True)
    slug = Column(String, unique=True, index=True)
    image_url = Column(String, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    is_active = Column(Boolean, default=True)
    meta_title = Column(String, nullable=True)
    meta_description = Column(String, nullable=True)
    parent_category = relationship(
        'Category', remote_side=[id], back_populates="sub_categories"
    )
    sub_categories = relationship(
        'Category', back_populates="parent_category", cascade="all, delete-orphan"
    )