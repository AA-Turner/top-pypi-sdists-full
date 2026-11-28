"""Settings: the saved values (the settings table of Core's database), the environment and the one .env file,
the defaults in the code."""
from .settings import (
    address,
    api_key_file,
    console_dir,
    current,
    database,
    default,
    home,
    is_client,
    is_service_host,
    local_key_file,
    located,
    resolve,
    save,
    typed,
    url,
)

__all__ = ['address', 'api_key_file', 'console_dir', 'current', 'database', 'default', 'home', 'is_client', 'is_service_host', 'local_key_file', 'located', 'resolve', 'save',
           'typed', 'url']
