from sqlalchemy.orm import Session

from src.sql.models import UserModel
from src.sql.session import get_db

# Get a user
def get_user(db_session: Session, telegram_id: int) -> UserModel:
    return db_session.query(UserModel).filter(UserModel.telegram_id == telegram_id).first()

def get_all_users(db_session: Session, condition=None) -> UserModel:
    return db_session.query(UserModel).all() if not condition else db_session.query(UserModel).filter(condition).all()