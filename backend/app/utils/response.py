"""Standardized API response utilities"""
from flask import jsonify
from typing import Any, Dict, Optional

def success_response(data: Any = None, status_code: int = 200):
    """Return success response"""
    if data is None:
        return '', status_code
    return jsonify(data), status_code

def error_response(message: str, status_code: int = 400, fields: Optional[Dict[str, str]] = None):
    """Return error response"""
    response = {'error': message}
    if fields:
        response['fields'] = fields
    return jsonify(response), status_code

def paginated_response(items: list, page: int, limit: int, total: int, key: str = 'items'):
    """Return paginated response"""
    return jsonify({
        key: items,
        'pagination': {
            'page': page,
            'limit': limit,
            'total': total,
            'pages': (total + limit - 1) // limit if limit > 0 else 0
        }
    }), 200
