"""Input validation utilities"""
from email_validator import validate_email, EmailNotValidError
from typing import Dict, Any

class ValidationError(Exception):
    """Custom validation error"""
    def __init__(self, fields: Dict[str, str]):
        self.fields = fields
        super().__init__('Validation failed')

def validate_user_input(data: Dict[str, Any], is_registration: bool = False) -> None:
    """Validate user input for registration/login"""
    errors = {}
    
    if is_registration:
        if not data.get('name'):
            errors['name'] = 'is required'
        elif len(data.get('name', '').strip()) < 2:
            errors['name'] = 'must be at least 2 characters'
    
    if not data.get('email'):
        errors['email'] = 'is required'
    elif data.get('email'):
        try:
            validate_email(data['email'])
        except EmailNotValidError:
            errors['email'] = 'invalid email format'
    
    if not data.get('password'):
        errors['password'] = 'is required'
    elif len(data.get('password', '')) < 6:
        errors['password'] = 'must be at least 6 characters'
    elif len(data.get('password', '')) > 128:
        errors['password'] = 'must be less than 128 characters'
    
    if errors:
        raise ValidationError(errors)

def validate_project_input(data: Dict[str, Any]) -> None:
    """Validate project input"""
    errors = {}
    
    if not data.get('name'):
        errors['name'] = 'is required'
    elif len(data.get('name', '').strip()) < 3:
        errors['name'] = 'must be at least 3 characters'
    elif len(data.get('name', '')) > 255:
        errors['name'] = 'must be less than 255 characters'
    
    if data.get('description') and len(data.get('description', '')) > 1000:
        errors['description'] = 'must be less than 1000 characters'
    
    if errors:
        raise ValidationError(errors)

def validate_task_input(data: Dict[str, Any]) -> None:
    """Validate task input"""
    errors = {}
    
    if not data.get('title'):
        errors['title'] = 'is required'
    elif len(data.get('title', '').strip()) < 3:
        errors['title'] = 'must be at least 3 characters'
    elif len(data.get('title', '')) > 255:
        errors['title'] = 'must be less than 255 characters'
    
    if data.get('description') and len(data.get('description', '')) > 2000:
        errors['description'] = 'must be less than 2000 characters'
    
    if data.get('status') and data['status'] not in ['todo', 'in_progress', 'done']:
        errors['status'] = 'must be one of: todo, in_progress, done'
    
    if data.get('priority') and data['priority'] not in ['low', 'medium', 'high']:
        errors['priority'] = 'must be one of: low, medium, high'
    
    if errors:
        raise ValidationError(errors)
