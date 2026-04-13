from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.repositories import UserRepository
from app.utils import validate_user_input, ValidationError, error_response, success_response
from app.models import User
from app import db

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
user_repo = UserRepository()

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    
    # Validation
    try:
        validate_user_input(data, is_registration=True)
    except ValidationError as e:
        return error_response('validation failed', 400, e.fields)
    
    # Check if user exists
    if user_repo.email_exists(data['email']):
        return error_response('validation failed', 400, {'email': 'already exists'})
    
    # Create user
    user = User(name=data['name'].strip(), email=data['email'].lower())
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    
    # Generate token
    access_token = create_access_token(identity=user.id, additional_claims={'email': user.email})
    
    return success_response({
        'token': access_token,
        'user': user.to_dict()
    }, 201)

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    data = request.get_json()
    
    # Validation
    try:
        validate_user_input(data, is_registration=False)
    except ValidationError as e:
        return error_response('validation failed', 400, e.fields)
    
    # Find user
    user = user_repo.get_by_email(data['email'].lower())
    
    if not user or not user.check_password(data['password']):
        return error_response('invalid credentials', 401)
    
    # Generate token
    access_token = create_access_token(identity=user.id, additional_claims={'email': user.email})
    
    return success_response({
        'token': access_token,
        'user': user.to_dict()
    })
