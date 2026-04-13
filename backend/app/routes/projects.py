from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Project, Task
from app.repositories import ProjectRepository, TaskRepository

projects_bp = Blueprint('projects', __name__, url_prefix='/projects')
project_repo = ProjectRepository()
task_repo = TaskRepository()

@projects_bp.route('', methods=['GET'])
@jwt_required()
def list_projects():
    """List projects with pagination"""
    user_id = get_jwt_identity()
    
    # Pagination parameters
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 20, type=int)
    limit = min(limit, 100)  # Max 100 items per page
    offset = (page - 1) * limit
    
    projects = project_repo.get_user_projects(user_id, limit=limit, offset=offset)
    total = project_repo.count_user_projects(user_id)
    
    return jsonify({
        'projects': [p.to_dict() for p in projects],
        'pagination': {
            'page': page,
            'limit': limit,
            'total': total,
            'pages': (total + limit - 1) // limit
        }
    }), 200

@projects_bp.route('', methods=['POST'])
@jwt_required()
def create_project():
    """Create a new project"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # Validation
    errors = {}
    if not data.get('name'):
        errors['name'] = 'is required'
    
    if errors:
        return jsonify({'error': 'validation failed', 'fields': errors}), 400
    
    # Create project
    project = Project(
        name=data['name'],
        description=data.get('description'),
        owner_id=user_id
    )
    
    db.session.add(project)
    db.session.commit()
    
    return jsonify(project.to_dict()), 201

@projects_bp.route('/<project_id>', methods=['GET'])
@jwt_required()
def get_project(project_id):
    """Get project details with tasks"""
    user_id = get_jwt_identity()
    
    project = project_repo.get_by_id(project_id)
    if not project:
        return jsonify({'error': 'not found'}), 404
    
    # Check access
    has_access = (
        project.owner_id == user_id or
        Task.query.filter_by(project_id=project_id, assignee_id=user_id).first() is not None
    )
    
    if not has_access:
        return jsonify({'error': 'forbidden'}), 403
    
    return jsonify(project.to_dict(include_tasks=True)), 200

@projects_bp.route('/<project_id>/stats', methods=['GET'])
@jwt_required()
def get_project_stats(project_id):
    """Get project statistics"""
    user_id = get_jwt_identity()
    
    project = project_repo.get_by_id(project_id)
    if not project:
        return jsonify({'error': 'not found'}), 404
    
    # Check access
    has_access = (
        project.owner_id == user_id or
        Task.query.filter_by(project_id=project_id, assignee_id=user_id).first() is not None
    )
    
    if not has_access:
        return jsonify({'error': 'forbidden'}), 403
    
    stats = project_repo.get_project_stats(project_id)
    return jsonify(stats), 200

@projects_bp.route('/<project_id>', methods=['PATCH'])
@jwt_required()
def update_project(project_id):
    """Update project (owner only)"""
    user_id = get_jwt_identity()
    
    project = project_repo.get_by_id(project_id)
    if not project:
        return jsonify({'error': 'not found'}), 404
    
    if project.owner_id != user_id:
        return jsonify({'error': 'forbidden'}), 403
    
    data = request.get_json()
    
    # Update fields
    if 'name' in data:
        if not data['name']:
            return jsonify({'error': 'validation failed', 'fields': {'name': 'is required'}}), 400
        project.name = data['name']
    
    if 'description' in data:
        project.description = data['description']
    
    db.session.commit()
    
    return jsonify(project.to_dict()), 200

@projects_bp.route('/<project_id>', methods=['DELETE'])
@jwt_required()
def delete_project(project_id):
    """Delete project and all its tasks (owner only)"""
    user_id = get_jwt_identity()
    
    project = project_repo.get_by_id(project_id)
    if not project:
        return jsonify({'error': 'not found'}), 404
    
    if project.owner_id != user_id:
        return jsonify({'error': 'forbidden'}), 403
    
    project_repo.delete(project)
    
    return '', 204

@projects_bp.route('/<project_id>/tasks', methods=['GET'])
@jwt_required()
def list_tasks(project_id):
    """List tasks with pagination and filters"""
    user_id = get_jwt_identity()
    
    project = project_repo.get_by_id(project_id)
    if not project:
        return jsonify({'error': 'not found'}), 404
    
    # Check access
    has_access = (
        project.owner_id == user_id or
        Task.query.filter_by(project_id=project_id, assignee_id=user_id).first() is not None
    )
    
    if not has_access:
        return jsonify({'error': 'forbidden'}), 403
    
    # Pagination and filters
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 50, type=int)
    limit = min(limit, 100)
    offset = (page - 1) * limit
    
    status = request.args.get('status')
    assignee = request.args.get('assignee')
    
    tasks = task_repo.get_project_tasks(
        project_id, 
        status=status, 
        assignee_id=assignee,
        limit=limit,
        offset=offset
    )
    total = task_repo.count_project_tasks(project_id, status=status, assignee_id=assignee)
    
    return jsonify({
        'tasks': [task.to_dict() for task in tasks],
        'pagination': {
            'page': page,
            'limit': limit,
            'total': total,
            'pages': (total + limit - 1) // limit
        }
    }), 200

@projects_bp.route('/<project_id>/tasks', methods=['POST'])
@jwt_required()
def create_task(project_id):
    """Create a task in a project"""
    user_id = get_jwt_identity()
    
    project = project_repo.get_by_id(project_id)
    if not project:
        return jsonify({'error': 'not found'}), 404
    
    # Check access
    has_access = (
        project.owner_id == user_id or
        Task.query.filter_by(project_id=project_id, assignee_id=user_id).first() is not None
    )
    
    if not has_access:
        return jsonify({'error': 'forbidden'}), 403
    
    data = request.get_json()
    
    # Validation
    errors = {}
    if not data.get('title'):
        errors['title'] = 'is required'
    
    if data.get('status') and data['status'] not in ['todo', 'in_progress', 'done']:
        errors['status'] = 'must be one of: todo, in_progress, done'
    
    if data.get('priority') and data['priority'] not in ['low', 'medium', 'high']:
        errors['priority'] = 'must be one of: low, medium, high'
    
    if errors:
        return jsonify({'error': 'validation failed', 'fields': errors}), 400
    
    # Create task
    task = Task(
        title=data['title'],
        description=data.get('description'),
        status=data.get('status', 'todo'),
        priority=data.get('priority', 'medium'),
        project_id=project_id,
        assignee_id=data.get('assignee_id')
    )
    
    if data.get('due_date'):
        from datetime import datetime
        try:
            task.due_date = datetime.fromisoformat(data['due_date']).date()
        except ValueError:
            return jsonify({'error': 'validation failed', 'fields': {'due_date': 'invalid date format'}}), 400
    
    db.session.add(task)
    db.session.commit()
    
    return jsonify(task.to_dict()), 201
