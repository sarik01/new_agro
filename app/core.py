import secrets
import shutil
from functools import wraps
from flask import *
import hashlib
import jwt, requests

from .config import SECRET_KEY
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from hashlib import sha256
from .models import User
import random
import uuid




def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({
                'message': "Token is missing !!"
            }), 401
        try:
            print(token)
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            print(data)
            current_user = User.query \
                .filter_by(id=data['public_id']) \
                .first()
        except Exception as E:
            return jsonify({
                'message': str(E)
            }), 401
        return f(current_user, *args, **kwargs)

    return decorated
