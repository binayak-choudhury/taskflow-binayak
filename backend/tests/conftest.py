import pytest
from app import create_app, db
from app.models import User, Project, Task
import uuid

@pytest.fixture
def app():
    """Create application for testing"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Test client"""
    return app.test_client()

@pytest.fixture
def test_user(app):
    """Create a test user"""
    user = User(
        id=str(uuid.uuid4()),
        name='Test User',
        email='test@example.com'
    )
    user.set_password('password123')
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture
def auth_headers(client, test_user):
    """Get authentication headers"""
    response = client.post('/auth/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    token = response.json['token']
    return {'Authorization': f'Bearer {token}'}

@pytest.fixture
def test_project(app, test_user):
    """Create a test project"""
    project = Project(
        id=str(uuid.uuid4()),
        name='Test Project',
        description='Test Description',
        owner_id=test_user.id
    )
    db.session.add(project)
    db.session.commit()
    return project
