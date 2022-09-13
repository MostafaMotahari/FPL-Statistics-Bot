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
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)