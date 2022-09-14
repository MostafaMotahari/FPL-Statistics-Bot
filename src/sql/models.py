from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
)

from src.sql.base_class import Base

# User model
class UserModel(Base):
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    telegram_id = Column(Integer, unique=True, index=True)
    phone_number = Column(String, unique=True, index=True)
    card_number = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    status = Column(String, default="user")