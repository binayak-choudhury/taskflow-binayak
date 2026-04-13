def test_register_success(client):
    """Test successful user registration"""
    response = client.post('/auth/register', json={
        'name': 'New User',
        'email': 'new@example.com',
        'password': 'password123'
    })
    
    assert response.status_code == 201
    data = response.json
    assert 'token' in data
    assert data['user']['email'] == 'new@example.com'
    assert data['user']['name'] == 'New User'

def test_register_duplicate_email(client, test_user):
    """Test registration with existing email"""
    response = client.post('/auth/register', json={
        'name': 'Another User',
        'email': 'test@example.com',
        'password': 'password123'
    })
    
    assert response.status_code == 400
    assert 'email' in response.json['fields']

def test_register_validation(client):
    """Test registration validation"""
    response = client.post('/auth/register', json={
        'name': '',
        'email': 'invalid-email',
        'password': '123'
    })
    
    assert response.status_code == 400
    assert 'name' in response.json['fields']
    assert 'password' in response.json['fields']

def test_login_success(client, test_user):
    """Test successful login"""
    response = client.post('/auth/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    
    assert response.status_code == 200
    data = response.json
    assert 'token' in data
    assert data['user']['email'] == 'test@example.com'

def test_login_invalid_credentials(client, test_user):
    """Test login with wrong password"""
    response = client.post('/auth/login', json={
        'email': 'test@example.com',
        'password': 'wrongpassword'
    })
    
    assert response.status_code == 401
    assert response.json['error'] == 'invalid credentials'

def test_login_nonexistent_user(client):
    """Test login with non-existent user"""
    response = client.post('/auth/login', json={
        'email': 'nonexistent@example.com',
        'password': 'password123'
    })
    
    assert response.status_code == 401
