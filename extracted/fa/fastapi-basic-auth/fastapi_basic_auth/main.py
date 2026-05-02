import base64
import secrets
from typing import Union, List, Dict
from .schema import BasicAuthUser
from fastapi import Request, Response
from starlette.types import ASGIApp
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

class FastAPIBasicAuthMiddleware:
    """Middleware for FastAPI Basic Authentication.
    
    Provides basic auth protection for specified URL endpoints.
    """
    
    def __init__(self, urls: List[str], users: Union[List[BasicAuthUser], Dict[str, str]]):
        """Initialize the middleware.
        
        Args:
            urls: List of URL paths to protect
            users: List of BasicAuthUser objects or dict of username/password pairs
        """
        if isinstance(users, list):
            self.users = users
        elif isinstance(users, dict):
            self.users = [BasicAuthUser(username=username, password=password) 
                         for username, password in users.items()]
        
        self.urls = urls

    @property
    def build(self):
        """Build and return the middleware class."""
        users = self.users
        urls = self.urls
        
        class BasicAuthMiddleware(BaseHTTPMiddleware):
            async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
                if request.url.path in urls:
                    auth_header = request.headers.get('Authorization')
                    if not auth_header:
                        return self._unauthorized_response()
                    
                    try:
                        scheme, credentials = auth_header.split()
                        if scheme.lower() != 'basic':
                            return self._unauthorized_response()
                            
                        decoded = base64.b64decode(credentials).decode('ascii')
                        username, password = decoded.split(':')
                        
                        # Get the user from the list of users
                        user = next((u for u in users if u.username == username), None)
                        
                        # Check if the user exists and credentials match
                        if user and self._verify_credentials(username, password, user):
                            return await call_next(request)
                            
                    except (ValueError, base64.binascii.Error):
                        return self._unauthorized_response()
                        
                    return self._unauthorized_response()
                return await call_next(request)
            
            @staticmethod
            def _unauthorized_response() -> Response:
                """Generate unauthorized response."""
                response = Response(
                    content='Unauthorized',
                    status_code=401,
                    headers={'WWW-Authenticate': 'Basic'}
                )
                return response
                
            @staticmethod
            def _verify_credentials(username: str, password: str, user: BasicAuthUser) -> bool:
                """Verify user credentials using constant-time comparison."""
                return (secrets.compare_digest(username, user.username) and 
                        secrets.compare_digest(password, user.password))
        
        return BasicAuthMiddleware
    
    def __call__(self, app: ASGIApp, *args, **kwargs):
        return self.build(app, *args, **kwargs)