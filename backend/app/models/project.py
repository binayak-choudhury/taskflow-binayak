from datetime import datetime
import uuid
from app import db

class Project(db.Model):
    __tablename__ = 'projects'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationships
    owner = db.relationship('User', back_populates='owned_projects')
    tasks = db.relationship('Task', back_populates='project', cascade='all, delete-orphan')
    
    def to_dict(self, include_tasks=False):
        """Convert to dictionary"""
        result = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'owner_id': self.owner_id,
            'created_at': self.created_at.isoformat()
        }
        if include_tasks:
            result['tasks'] = [task.to_dict() for task in self.tasks]
        return result
