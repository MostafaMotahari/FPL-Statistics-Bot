from src.sql.models import UserModel
from src.sql.session import get_db

# Make migrations
def make_migrations():
    # User models migration
    db_session = get_db().__next__()
    db_session.add(UserModel(telegram_id=0))
    db_session.commit()