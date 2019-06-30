from functools import wraps

from flask import make_response, request


def bearer_required(token):
    def decorator(f):
        def failed(description=''):
            value = 'Bearer error="invalid_token", error_description="{}"'.format(description)
            return make_response(description, 401, {'WWW-Authenticate': value})

        @wraps(f)
        def decorated_function(*args, **kwargs):
            header = request.environ.get("HTTP_AUTHORIZATION")
            if header:
                try:
                    auth_type, auth_info = header.split(None, 1)
                    auth_type = auth_type.lower()
                except ValueError:
                    return failed('Authorization is malformed')

                if auth_type == 'bearer':
                    if auth_info == token:
                        return f(*args, **kwargs)
                    else:
                        return failed('The token is incorrect')
            return failed('Bearer token is required')

        return decorated_function

    return decorator
