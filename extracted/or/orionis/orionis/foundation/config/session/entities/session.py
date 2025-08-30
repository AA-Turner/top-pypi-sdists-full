from dataclasses import dataclass, field
from typing import Optional
from orionis.foundation.exceptions import OrionisIntegrityException
from orionis.foundation.config.session.enums import SameSitePolicy
from orionis.foundation.config.session.helpers.secret_key import SecretKey
from orionis.services.environment.env import Env
from orionis.support.entities.base import BaseEntity

@dataclass(unsafe_hash=True, kw_only=True)
class Session(BaseEntity):
    """
    Configuration for Starlette session middleware.

    Attributes:
        secret_key (str): Secret key for signing session cookies (required).
        session_cookie (str): Name of the session cookie. Defaults to 'session'.
        max_age (Optional[int]): Session expiration in seconds. None for browser session.
        same_site (Literal['lax', 'strict', 'none']): SameSite cookie policy.
        path (str): Cookie path. Defaults to '/'.
        https_only (bool): Restrict cookies to HTTPS. Defaults to False.
        domain (Optional[str]): Cookie domain for cross-subdomain usage.
    """

    secret_key: str = field(
        default_factory = lambda: Env.get('APP_KEY', SecretKey.random()),
        metadata = {
            "description": "Secret key for signing session cookies (required).",
            "default": lambda: SecretKey.random()
        }
    )

    session_cookie: str = field(
        default_factory = lambda: Env.get('SESSION_COOKIE_NAME', 'orionis_session'),
        metadata = {
            "description": "Name of the session cookie.",
            "default": 'orionis_session'
        }
    )

    max_age: Optional[int] = field(
        default_factory = lambda: Env.get('SESSION_MAX_AGE', 30 * 60),
        metadata = {
            "description": "Session expiration in seconds. None for browser session.",
            "default": 30 * 60
        }
    )

    same_site: str | SameSitePolicy = field(
        default_factory = lambda: Env.get('SESSION_SAME_SITE', SameSitePolicy.LAX.value),
        metadata = {
            "description": "SameSite cookie policy.",
            "default": SameSitePolicy.LAX.value
        }
    )

    path: str = field(
        default_factory = lambda: Env.get('SESSION_PATH', '/'),
        metadata = {
            "description": "Cookie path.",
            "default": "/"
        }
    )

    https_only: bool = field(
        default_factory = lambda: Env.get('SESSION_HTTPS_ONLY', False),
        metadata = {
            "description": "Restrict cookies to HTTPS.",
            "default": False
        }
    )

    domain: Optional[str] = field(
        default_factory = lambda: Env.get('SESSION_DOMAIN'),
        metadata = {
            "description": "Cookie domain for cross-subdomain usage.",
            "default": None
        }
    )

    def __post_init__(self):
        super().__post_init__()
        """
        Validates the initialization parameters of the session entity.
        Raises:
            OrionisIntegrityException: If any of the following conditions are not met:
                - `secret_key` must be a non-empty string.
                - `secret_key` must be at least 32 characters long.
                - `max_age` must be an integer or None.
                - `same_site` must be one of: 'lax', 'strict', 'none'.
                - If `same_site` is 'none', `https_only` must be True.
                - `domain` must be a string or None.
        """

        # Validate secret_key
        if self.secret_key is None:
            self.secret_key = SecretKey.random()
        if not isinstance(self.secret_key, (bytes, str)) or not self.secret_key.strip():
            raise OrionisIntegrityException("secret_key must be a non-empty string")

        # Validate session_cookie
        if not isinstance(self.session_cookie, str) or not self.session_cookie.strip():
            raise OrionisIntegrityException("session_cookie must be a non-empty string")
        if any(c in self.session_cookie for c in ' ;,'):
            raise OrionisIntegrityException("session_cookie must not contain spaces, semicolons, or commas")

        # Validate max_age
        if self.max_age is not None:
            if not isinstance(self.max_age, int):
                raise OrionisIntegrityException("max_age must be an integer or None")
            if self.max_age <= 0:
                raise OrionisIntegrityException("max_age must be a positive integer if set")

        # Validate same_site
        if not isinstance(self.same_site, (str, SameSitePolicy)):
            raise OrionisIntegrityException("same_site must be a string or SameSitePolicy")
        if isinstance(self.same_site, str):
            options = SameSitePolicy._member_names_
            _value = self.same_site.upper().strip()
            if _value not in options:
                raise OrionisIntegrityException(f"same_site must be one of: {', '.join(options)}")
            else:
                self.same_site = SameSitePolicy[_value].value
        elif isinstance(self.same_site, SameSitePolicy):
            self.same_site = self.same_site.value

        # Validate path
        if not isinstance(self.path, str) or not self.path.startswith('/'):
            raise OrionisIntegrityException("path must be a string starting with '/'")

        # Validate https_only
        if not isinstance(self.https_only, bool):
            raise OrionisIntegrityException("https_only must be a boolean value")

        # Validate domain
        if self.domain is not None:
            if not isinstance(self.domain, str) or not self.domain.strip():
                raise OrionisIntegrityException("domain must be a non-empty string or None")
            if self.domain.startswith('.') or self.domain.endswith('.'):
                raise OrionisIntegrityException("domain must not start or end with a dot")
            if '..' in self.domain:
                raise OrionisIntegrityException("domain must not contain consecutive dots")