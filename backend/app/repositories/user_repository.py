from typing import Optional
from app.models import User
from app.repositories.base_repository import BaseRepository

class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)
    
    def get_by_email(self, email: str) -> Optional[User]:
        return User.query.filter_by(email=email).first()
    
    def email_exists(self, email: str) -> bool:
        return User.query.filter_by(email=email).first() is not None
