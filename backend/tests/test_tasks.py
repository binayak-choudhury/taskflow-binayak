from app.models import Task
from app import db

def test_create_task(client, auth_headers, test_project):
    """Test task creation"""
    response = client.post(f'/projects/{test_project.id}/tasks',
        headers=auth_headers,
        json={
            'title': 'New Task',
            'description': 'Task Description',
            'priority': 'high',
            'status': 'todo'
        }
    )
    
    assert response.status_code == 201
    data = response.json
    assert data['title'] == 'New Task'
    assert data['priority'] == 'high'
    assert data['status'] == 'todo'

def test_list_tasks(client, auth_headers, test_project):
    """Test listing tasks"""
    response = client.get(f'/projects/{test_project.id}/tasks', headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json
    assert 'tasks' in data
    assert 'pagination' in data

def test_update_task(client, auth_headers, test_project, app):
    """Test updating task"""
    # Create a task first
    with app.app_context():
        task = Task(
            title='Test Task',
            project_id=test_project.id,
            status='todo',
            priority='medium'
        )
        db.session.add(task)
        db.session.commit()
        task_id = task.id
    
    response = client.patch(f'/tasks/{task_id}',
        headers=auth_headers,
        json={'status': 'done'}
    )
    
    assert response.status_code == 200
    assert response.json['status'] == 'done'

def test_delete_task(client, auth_headers, test_project, app):
    """Test deleting task"""
    # Create a task first
    with app.app_context():
        task = Task(
            title='Test Task',
            project_id=test_project.id,
            status='todo',
            priority='medium'
        )
        db.session.add(task)
        db.session.commit()
        task_id = task.id
    
    response = client.delete(f'/tasks/{task_id}', headers=auth_headers)
    
    assert response.status_code == 204

def test_filter_tasks_by_status(client, auth_headers, test_project):
    """Test filtering tasks by status"""
    response = client.get(
        f'/projects/{test_project.id}/tasks?status=todo',
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json
    assert 'tasks' in data
