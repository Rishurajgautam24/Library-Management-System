from werkzeug.exceptions import HTTPException
from flask import make_response

class NotFoundError(HTTPException):
    def __init__(self, status_code=404,error='Not Found'):
        error = {'error': error}
        self.response = make_response(error, status_code)
        
    
class AlreadyExistsError(HTTPException):
    def __init__(self, status_code=400,error='Already Exists'):
        error = {'error': error}
        self.response = make_response(error, status_code)

class ValidationError(HTTPException):
    def __init__(self, status_code=400,error='Validation Error'):
        error = {'error': error}
        self.response = make_response(error, status_code)