def test_create_project(client, auth_headers):
    """Test project creation"""
    response = client.post('/projects', 
        headers=auth_headers,
        json={
            'name': 'New Project',
            'description': 'Project Description'
        }
    )
    
    assert response.status_code == 201
    data = response.json
    assert data['name'] == 'New Project'
    assert data['description'] == 'Project Description'

def test_list_projects(client, auth_headers, test_project):
    """Test listing projects"""
    response = client.get('/projects', headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json
    assert 'projects' in data
    assert 'pagination' in data
    assert len(data['projects']) >= 1

def test_get_project(client, auth_headers, test_project):
    """Test getting project details"""
    response = client.get(f'/projects/{test_project.id}', headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json
    assert data['id'] == test_project.id
    assert data['name'] == test_project.name

def test_get_project_stats(client, auth_headers, test_project):
    """Test getting project statistics"""
    response = client.get(f'/projects/{test_project.id}/stats', headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json
    assert 'total_tasks' in data
    assert 'by_status' in data
    assert 'by_priority' in data
    assert 'by_assignee' in data

def test_update_project(client, auth_headers, test_project):
    """Test updating project"""
    response = client.patch(f'/projects/{test_project.id}',
        headers=auth_headers,
        json={'name': 'Updated Project'}
    )
    
    assert response.status_code == 200
    assert response.json['name'] == 'Updated Project'

def test_delete_project(client, auth_headers, test_project):
    """Test deleting project"""
    response = client.delete(f'/projects/{test_project.id}', headers=auth_headers)
    
    assert response.status_code == 204

def test_unauthorized_access(client, test_project):
    """Test accessing project without authentication"""
    response = client.get(f'/projects/{test_project.id}')
    
    assert response.status_code == 401
