"""Application middleware"""
from flask import jsonify
from werkzeug.exceptions import HTTPException
import logging

logger = logging.getLogger(__name__)

def register_error_handlers(app):
    """Register global error handlers"""
    
    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({'error': 'bad request'}), 400
    
    @app.errorhandler(401)
    def unauthorized(e):
        return jsonify({'error': 'unauthorized'}), 401
    
    @app.errorhandler(403)
    def forbidden(e):
        return jsonify({'error': 'forbidden'}), 403
    
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({'error': 'not found'}), 404
    
    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({'error': 'method not allowed'}), 405
    
    @app.errorhandler(500)
    def internal_error(e):
        logger.error(f'Internal server error: {str(e)}')
        return jsonify({'error': 'internal server error'}), 500
    
    @app.errorhandler(Exception)
    def handle_exception(e):
        """Handle unexpected exceptions"""
        if isinstance(e, HTTPException):
            return e
        
        logger.error(f'Unhandled exception: {str(e)}', exc_info=True)
        return jsonify({'error': 'internal server error'}), 500

def register_request_logging(app):
    """Log all requests"""
    
    @app.before_request
    def log_request():
        from flask import request
        logger.info(f'{request.method} {request.path}')
    
    @app.after_request
    def log_response(response):
        from flask import request
        logger.info(f'{request.method} {request.path} - {response.status_code}')
        return response
