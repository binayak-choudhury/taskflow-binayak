from typing import List
from app.models import Project, Task
from app.repositories.base_repository import BaseRepository
from app import db

class ProjectRepository(BaseRepository[Project]):
    def __init__(self):
        super().__init__(Project)
    
    def get_user_projects(self, user_id: str, limit: int = None, offset: int = None) -> List[Project]:
        """Get projects owned by user or where user has tasks"""
        owned = db.session.query(Project).filter_by(owner_id=user_id)
        assigned = db.session.query(Project).join(Task).filter(Task.assignee_id == user_id)
        
        query = owned.union(assigned).order_by(Project.created_at.desc())
        
        if offset:
            query = query.offset(offset)
        if limit:
            query = query.limit(limit)
        
        return query.all()
    
    def count_user_projects(self, user_id: str) -> int:
        """Count projects accessible to user"""
        owned = db.session.query(Project.id).filter_by(owner_id=user_id)
        assigned = db.session.query(Project.id).join(Task).filter(Task.assignee_id == user_id)
        return owned.union(assigned).count()
    
    def get_project_stats(self, project_id: str) -> dict:
        """Get task statistics for a project"""
        tasks = Task.query.filter_by(project_id=project_id).all()
        
        stats = {
            'total_tasks': len(tasks),
            'by_status': {'todo': 0, 'in_progress': 0, 'done': 0},
            'by_priority': {'low': 0, 'medium': 0, 'high': 0},
            'by_assignee': {}
        }
        
        for task in tasks:
            stats['by_status'][task.status] += 1
            stats['by_priority'][task.priority] += 1
            
            if task.assignee_id:
                if task.assignee_id not in stats['by_assignee']:
                    stats['by_assignee'][task.assignee_id] = 0
                stats['by_assignee'][task.assignee_id] += 1
        
        return stats
