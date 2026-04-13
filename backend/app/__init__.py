from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import logging
import signal
import sys

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    """Application factory"""
    app = Flask(__name__)
    
    # Load config
    app.config.from_object('app.config.Config')
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app, origins=app.config['CORS_ORIGINS'])
    jwt.init_app(app)
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Register error handlers and middleware
    from app.middleware import register_error_handlers, register_request_logging
    register_error_handlers(app)
    if app.config.get('FLASK_ENV') != 'testing':
        register_request_logging(app)
    
    # Register blueprints
    from app.routes import auth_bp, projects_bp, tasks_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(projects_bp)
    app.register_blueprint(tasks_bp)
    
    # Health check endpoint
    @app.route('/health')
    def health():
        return {'status': 'healthy'}, 200
    
    @app.route('/')
    def index():
        return {'message': 'TaskFlow API', 'version': '1.0.0'}, 200
    
    # Graceful shutdown handler
    def shutdown_handler(signum, frame):
        logging.info('Received shutdown signal, exiting gracefully...')
        sys.exit(0)
    
    signal.signal(signal.SIGTERM, shutdown_handler)
    signal.signal(signal.SIGINT, shutdown_handler)
    
    return app
