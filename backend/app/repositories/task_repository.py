from typing import List, Optional
from app.models import Task
from app.repositories.base_repository import BaseRepository

class TaskRepository(BaseRepository[Task]):
    def __init__(self):
        super().__init__(Task)
    
    def get_project_tasks(
        self, 
        project_id: str, 
        status: Optional[str] = None,
        assignee_id: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> List[Task]:
        """Get tasks for a project with optional filters"""
        query = Task.query.filter_by(project_id=project_id)
        
        if status:
            query = query.filter_by(status=status)
        if assignee_id:
            query = query.filter_by(assignee_id=assignee_id)
        
        query = query.order_by(Task.created_at.desc())
        
        if offset:
            query = query.offset(offset)
        if limit:
            query = query.limit(limit)
        
        return query.all()
    
    def count_project_tasks(
        self,
        project_id: str,
        status: Optional[str] = None,
        assignee_id: Optional[str] = None
    ) -> int:
        """Count tasks with filters"""
        query = Task.query.filter_by(project_id=project_id)
        
        if status:
            query = query.filter_by(status=status)
        if assignee_id:
            query = query.filter_by(assignee_id=assignee_id)
        
        return query.count()
