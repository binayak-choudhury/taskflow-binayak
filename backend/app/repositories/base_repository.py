from typing import TypeVar, Generic, List, Optional
from app import db

T = TypeVar('T')

class BaseRepository(Generic[T]):
    """Base repository with common CRUD operations"""
    
    def __init__(self, model: type[T]):
        self.model = model
    
    def get_by_id(self, id: str) -> Optional[T]:
        return self.model.query.get(id)
    
    def get_all(self, limit: Optional[int] = None, offset: Optional[int] = None) -> List[T]:
        query = self.model.query
        if offset:
            query = query.offset(offset)
        if limit:
            query = query.limit(limit)
        return query.all()
    
    def create(self, **kwargs) -> T:
        instance = self.model(**kwargs)
        db.session.add(instance)
        db.session.commit()
        return instance
    
    def update(self, instance: T) -> T:
        db.session.commit()
        return instance
    
    def delete(self, instance: T) -> None:
        db.session.delete(instance)
        db.session.commit()
    
    def count(self) -> int:
        return self.model.query.count()
