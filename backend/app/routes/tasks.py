from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from app import db
from app.models import Task, Project

tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks')

@tasks_bp.route('/<task_id>', methods=['PATCH'])
@jwt_required()
def update_task(task_id):
    """Update a task"""
    user_id = get_jwt_identity()
    
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'not found'}), 404
    
    # Check access (project owner or task assignee)
    project = Project.query.get(task.project_id)
    has_access = (
        project.owner_id == user_id or
        task.assignee_id == user_id
    )
    
    if not has_access:
        return jsonify({'error': 'forbidden'}), 403
    
    data = request.get_json()
    
    # Validation
    errors = {}
    
    if 'title' in data:
        if not data['title']:
            errors['title'] = 'is required'
        else:
            task.title = data['title']
    
    if 'description' in data:
        task.description = data['description']
    
    if 'status' in data:
        if data['status'] not in ['todo', 'in_progress', 'done']:
            errors['status'] = 'must be one of: todo, in_progress, done'
        else:
            task.status = data['status']
    
    if 'priority' in data:
        if data['priority'] not in ['low', 'medium', 'high']:
            errors['priority'] = 'must be one of: low, medium, high'
        else:
            task.priority = data['priority']
    
    if 'assignee_id' in data:
        task.assignee_id = data['assignee_id']
    
    if 'due_date' in data:
        if data['due_date']:
            try:
                task.due_date = datetime.fromisoformat(data['due_date']).date()
            except ValueError:
                errors['due_date'] = 'invalid date format'
        else:
            task.due_date = None
    
    if errors:
        return jsonify({'error': 'validation failed', 'fields': errors}), 400
    
    db.session.commit()
    
    return jsonify(task.to_dict()), 200

@tasks_bp.route('/<task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    """Delete a task (project owner only)"""
    user_id = get_jwt_identity()
    
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'not found'}), 404
    
    # Check if user is project owner
    project = Project.query.get(task.project_id)
    if project.owner_id != user_id:
        return jsonify({'error': 'forbidden'}), 403
    
    db.session.delete(task)
    db.session.commit()
    
    return '', 204
