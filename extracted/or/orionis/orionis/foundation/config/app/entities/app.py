from dataclasses import dataclass, field
from orionis.foundation.config.app.enums import Cipher, Environments
from orionis.foundation.exceptions import OrionisIntegrityException
from orionis.services.environment.env import Env
from orionis.services.environment.key.key_generator import SecureKeyGenerator
from orionis.services.system.workers import Workers
from orionis.support.entities.base import BaseEntity

@dataclass(unsafe_hash=True, kw_only=True)
class App(BaseEntity):
    """
    Application configuration settings.

    Parameters
    ----------
    name : str, optional
        The name of the application. Default is 'Orionis Application'.
    env : str or Environments, optional
        The environment in which the application is running. Default is 'DEVELOPMENT'.
    debug : bool, optional
        Whether debug mode is enabled. Default is True.
    url : str, optional
        The base URL of the application. Default is 'http://127.0.0.1'.
    port : int, optional
        The port on which the application will run. Default is 8000.
    workers : int, optional
        Number of worker processes to handle requests. Default is maximum available workers.
    reload : bool, optional
        Whether the application should reload on code changes. Default is True.
    timezone : str, optional
        The timezone of the application. Default is 'UTC'.
    locale : str, optional
        The locale for the application. Default is 'en'.
    fallback_locale : str, optional
        The fallback locale for the application. Default is 'en'.
    cipher : str or Cipher, optional
        The cipher used for encryption. Default is 'AES_256_CBC'.
    key : str, optional
        The encryption key for the application. Default is None.
    maintenance : str, optional
        The maintenance route for the application. Default is '/maintenance'.

    Methods
    -------
    __post_init__()
        Validates and normalizes the attributes after dataclass initialization.
    """

    name: str = field(
        default_factory = lambda: Env.get('APP_NAME', 'Orionis Application'),
        metadata = {
            "description": "The name of the application. Defaults to 'Orionis Application'.",
            "default": 'Orionis Application'
        }
    )

    env: str | Environments = field(
        default_factory = lambda: Env.get('APP_ENV', Environments.DEVELOPMENT.value),
        metadata = {
            "description": "The environment in which the application is running. Defaults to 'DEVELOPMENT'.",
            "default": Environments.DEVELOPMENT.value
        }
    )

    debug: bool = field(
        default_factory = lambda: Env.get('APP_DEBUG', True),
        metadata = {
            "description": "Flag indicating whether debug mode is enabled. Defaults to False.",
            "default": True
        }
    )

    url: str = field(
        default_factory = lambda: Env.get('APP_URL', 'http://127.0.0.1'),
        metadata = {
            "description": "The base URL of the application. Defaults to 'http://127.0.0.1'.",
            "default": 'http://127.0.0.1'
        }
    )

    port: int = field(
        default_factory = lambda: Env.get('APP_PORT', 8000),
        metadata = {
            "description": "The port on which the application will run. Defaults to 8000.",
            "default": 8000
        }
    )

    workers: int = field(
        default_factory = lambda: Env.get('APP_WORKERS', Workers().calculate()),
        metadata = {
            "description": "The number of worker processes to handle requests. Defaults to the maximum available workers.",
            "default": lambda: Workers().calculate()
        }
    )

    reload: bool = field(
        default_factory = lambda: Env.get('APP_RELOAD', True),
        metadata = {
            "description": "Flag indicating whether the application should reload on code changes. Defaults to True.",
            "default": True
        }
    )

    timezone: str = field(
        default_factory = lambda: Env.get('APP_TIMEZONE', 'UTC'),
        metadata = {
            "description": "The timezone of the application. Defaults to 'UTC'.",
            "default": 'UTC'
        }
    )

    locale: str = field(
        default_factory = lambda: Env.get('APP_LOCALE', 'en'),
        metadata = {
            "description": "The locale for the application. Defaults to 'en'.",
            "default": 'en'
        }
    )

    fallback_locale: str = field(
        default_factory = lambda: Env.get('APP_FALLBACK_LOCALE', 'en'),
        metadata = {
            "description": "The fallback locale for the application. Defaults to 'en'.",
            "default": 'en'
        }
    )

    cipher: str | Cipher = field(
        default_factory = lambda: Env.get('APP_CIPHER', Cipher.AES_256_CBC.value),
        metadata = {
            "description": "The cipher used for encryption. Defaults to 'AES_256_CBC'.",
            "default": Cipher.AES_256_CBC.value
        }
    )

    key: str = field(
        default_factory = lambda: Env.get('APP_KEY'),
        metadata = {
            "description": "The encryption key for the application. Defaults to None.",
            "default": None
        }
    )

    maintenance: str = field(
        default_factory = lambda: Env.get('APP_MAINTENANCE', '/maintenance'),
        metadata = {
            "description": "The maintenance configuration for the application. Defaults to '/maintenance'.",
            "default": '/maintenance'
        }
    )

    def __post_init__(self):
        super().__post_init__()
        """
        Validate and normalize attributes after dataclass initialization.

        This method checks that all configuration fields have the correct types and valid values.
        If any field is invalid, an OrionisIntegrityException is raised to prevent misconfiguration.

        Raises
        ------
        OrionisIntegrityException
            If any attribute does not meet the required type or value constraints.

        Notes
        -----
        This method is automatically called after the dataclass is instantiated to ensure
        application configuration integrity and catch errors early in the lifecycle.
        """

        # Validate `name` attribute
        if not isinstance(self.name, (str, Environments)) or not self.name.strip():
            raise OrionisIntegrityException("The 'name' attribute must be a non-empty string or an Environments instance.")

        # Validate `env` attribute
        options_env = Environments._member_names_
        if isinstance(self.env, str):
            _value = str(self.env).strip().upper()
            if _value in options_env:
                self.env = Environments[_value].value
            else:
                raise OrionisIntegrityException(f"Invalid name value: {self.env}. Must be one of {str(options_env)}.")
        elif isinstance(self.env, Environments):
            self.env = self.env.value

        # Validate `debug` attribute
        if not isinstance(self.debug, bool):
            raise OrionisIntegrityException("The 'debug' attribute must be a boolean.")

        # Validate `url` attribute
        if not isinstance(self.url, str) or not self.url.strip():
            raise OrionisIntegrityException("The 'url' attribute must be a non-empty string.")

        # Validate `port` attribute
        if not isinstance(self.port, int):
            raise OrionisIntegrityException("The 'port' attribute must be an integer.")

        # Validate `workers` attribute
        if not isinstance(self.workers, int):
            raise OrionisIntegrityException("The 'workers' attribute must be an integer.")

        real_workers = Workers().calculate()
        if self.workers < 1 or self.workers > real_workers:
            raise OrionisIntegrityException(f"The 'workers' attribute must be between 1 and {real_workers}.")

        # Validate `reload` attribute
        if not isinstance(self.reload, bool):
            raise OrionisIntegrityException("The 'reload' attribute must be a boolean.")

        # Validate `timezone` attribute
        if not isinstance(self.timezone, str) or not self.timezone.strip():
            raise OrionisIntegrityException("The 'timezone' attribute must be a non-empty string.")

        # Validate `locale` attribute
        if not isinstance(self.locale, str) or not self.locale.strip():
            raise OrionisIntegrityException("The 'locale' attribute must be a non-empty string.")

        # Validate `fallback_locale` attribute
        if not isinstance(self.fallback_locale, str) or not self.fallback_locale.strip():
            raise OrionisIntegrityException("The 'fallback_locale' attribute must be a non-empty string.")

        # Validate `cipher` attribute
        options_cipher = Cipher._member_names_
        if not isinstance(self.cipher, (Cipher, str)):
            raise OrionisIntegrityException("The 'cipher' attribute must be a Cipher or a string.")

        if isinstance(self.cipher, str):
            _value = str(self.cipher).strip().upper().replace("-", "_")
            if _value in options_cipher:
                self.cipher = Cipher[_value].value
            else:
                raise OrionisIntegrityException(f"Invalid cipher value: {self.cipher}. Must be one of {options_cipher}.")
        elif isinstance(self.cipher, Cipher):
            self.cipher = self.cipher.value

        # Validate `key` attribute
        if self.key is None:
            self.key = SecureKeyGenerator.generate()
            Env.set('APP_KEY', self.key)
        if not isinstance(self.key, (bytes, str)) or not self.key.strip():
            raise OrionisIntegrityException("The 'key' attribute must be a non-empty string.")

        # Validate `maintenance` attribute
        if not isinstance(self.maintenance, str) or not self.name.strip() or not self.maintenance.startswith('/'):
            raise OrionisIntegrityException("The 'maintenance' attribute must be a non-empty string representing a valid route (e.g., '/maintenance').")