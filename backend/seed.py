"""Seed database with initial data"""
from app import create_app, db
from app.models import User, Project, Task
from datetime import datetime, timedelta
import uuid

def seed_data():
    app = create_app()
    with app.app_context():
        # Clear existing data
        Task.query.delete()
        Project.query.delete()
        User.query.delete()
        db.session.commit()
        
        # Create test user
        user = User(
            id=str(uuid.uuid4()),
            name='Test User',
            email='test@example.com'
        )
        user.set_password('password123')
        db.session.add(user)
        
        # Create another user for assignment testing
        user2 = User(
            id=str(uuid.uuid4()),
            name='Jane Doe',
            email='jane@example.com'
        )
        user2.set_password('password123')
        db.session.add(user2)
        
        db.session.commit()
        
        # Create project
        project = Project(
            id=str(uuid.uuid4()),
            name='Website Redesign',
            description='Q2 project to redesign the company website',
            owner_id=user.id
        )
        db.session.add(project)
        db.session.commit()
        
        # Create tasks
        tasks = [
            Task(
                id=str(uuid.uuid4()),
                title='Design homepage mockup',
                description='Create initial design mockups for the new homepage',
                status='in_progress',
                priority='high',
                project_id=project.id,
                assignee_id=user.id,
                due_date=(datetime.now() + timedelta(days=7)).date()
            ),
            Task(
                id=str(uuid.uuid4()),
                title='Set up development environment',
                description='Configure local dev environment with new tech stack',
                status='done',
                priority='medium',
                project_id=project.id,
                assignee_id=user2.id,
                due_date=(datetime.now() - timedelta(days=2)).date()
            ),
            Task(
                id=str(uuid.uuid4()),
                title='Write API documentation',
                description='Document all API endpoints for the new backend',
                status='todo',
                priority='low',
                project_id=project.id,
                assignee_id=None,
                due_date=(datetime.now() + timedelta(days=14)).date()
            )
        ]
        
        for task in tasks:
            db.session.add(task)
        
        db.session.commit()
        
        print('Database seeded successfully!')
        print(f'Test user: test@example.com / password123')
        print(f'Test user 2: jane@example.com / password123')
        print(f'Project: {project.name}')
        print(f'Tasks created: {len(tasks)}')

if __name__ == '__main__':
    seed_data()
