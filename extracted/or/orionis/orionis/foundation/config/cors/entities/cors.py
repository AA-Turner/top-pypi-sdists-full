from dataclasses import dataclass, field
from typing import List, Optional
from orionis.foundation.exceptions import OrionisIntegrityException
from orionis.support.entities.base import BaseEntity

@dataclass(unsafe_hash=True, kw_only=True)
class Cors(BaseEntity):
    """
    CORS configuration compatible with Starlette CORSMiddleware.

    Attributes:
        allow_origins (List[str]): List of allowed origins. Use ["*"] to allow all origins.
        allow_origin_regex (Optional[str]): Regular expression to match allowed origins.
        allow_methods (List[str]): List of allowed HTTP methods. Use ["*"] to allow all methods.
        allow_headers (List[str]): List of allowed HTTP headers. Use ["*"] to allow all headers.
        expose_headers (List[str]): List of headers exposed to the browser.
        allow_credentials (bool): Whether to allow credentials (cookies, authorization headers, etc.).
        max_age (Optional[int]): Maximum time (in seconds) for the preflight request to be cached.

    Methods:
        __post_init__():
            Validates the types of the configuration attributes after initialization.
            Raises:
                OrionisIntegrityException: If any attribute does not match the expected type.
    """

    allow_origins: List[str] = field(
        default_factory = lambda: ["*"],
        metadata = {
            "description": "List of allowed origins. Use [\"*\"] to allow all origins.",
            "deafault": ["*"]
        },
    )

    allow_origin_regex: Optional[str] = field(
        default = None,
        metadata = {
            "description": "Regular expression pattern to match allowed origins.",
            "default": None
        },
    )

    allow_methods: List[str] = field(
        default_factory = lambda: ["*"],
        metadata = {
            "description": "List of allowed HTTP methods. Use [\"*\"] to allow all methods.",
            "default": ["*"]
        },
    )

    allow_headers: List[str] = field(
        default_factory = lambda: ["*"],
        metadata = {
            "description": "List of allowed HTTP headers. Use [\"*\"] to allow all headers.",
            "default": ["*"]
        },
    )

    expose_headers: List[str] = field(
        default_factory = lambda: [],
        metadata = {
            "description": "List of headers exposed to the browser.",
            "default": []
        },
    )

    allow_credentials: bool = field(
        default = False,
        metadata = {
            "description": "Whether to allow credentials (cookies, authorization headers, etc.).",
            "default": False
        },
    )

    max_age: Optional[int] = field(
        default = 600,
        metadata = {
            "description": "Maximum time (in seconds) for preflight request caching.",
            "default": 600
        },
    )

    def __post_init__(self):
        super().__post_init__()
        """
        Validates the types of CORS configuration attributes after initialization.

        Raises:
            OrionisIntegrityException: If any of the following conditions are not met:
                - allow_origins is not a list of strings.
                - allow_origin_regex is not a string or None.
                - allow_methods is not a list of strings.
                - allow_headers is not a list of strings.
                - expose_headers is not a list of strings.
                - allow_credentials is not a boolean.
                - max_age is not an integer or None.
        """

        # Validate `allow_origins` attribute
        if not isinstance(self.allow_origins, list):
            raise OrionisIntegrityException(
                "Invalid type for 'allow_origins': expected a list of strings."
            )

        # Validate `allow_origin_regex` attribute
        if self.allow_origin_regex is not None and not isinstance(self.allow_origin_regex, str):
            raise OrionisIntegrityException(
                "Invalid type for 'allow_origin_regex': expected a string or None."
            )

        # Validate `allow_methods` attribute
        if not isinstance(self.allow_methods, list):
            raise OrionisIntegrityException(
                "Invalid type for 'allow_methods': expected a list of strings."
            )

        # Validate `allow_headers` attribute
        if not isinstance(self.allow_headers, list):
            raise OrionisIntegrityException(
                "Invalid type for 'allow_headers': expected a list of strings."
            )

        # Validate `expose_headers` attribute
        if not isinstance(self.expose_headers, list):
            raise OrionisIntegrityException(
                "Invalid type for 'expose_headers': expected a list of strings."
            )

        # Validate `allow_credentials` attribute
        if not isinstance(self.allow_credentials, bool):
            raise OrionisIntegrityException(
                "Invalid type for 'allow_credentials': expected a boolean."
            )

        # Validate `max_age` attribute
        if self.max_age is not None and not isinstance(self.max_age, int):
            raise OrionisIntegrityException(
                "Invalid type for 'max_age': expected an integer or None."
            )