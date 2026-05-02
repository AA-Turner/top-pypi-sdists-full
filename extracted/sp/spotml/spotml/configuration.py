import os


def get_spotml_config_dir():
    """Spotml configuration directory."""
    path = os.path.join(os.path.expanduser('~'), '.spotml')
    if not os.path.isdir(path):
        os.makedirs(path, mode=0o755, exist_ok=True)

    return path


def get_spotml_keys_dir(provider_name: str):
    """"Spotml keys directory."""
    path = os.path.join(get_spotml_config_dir(), 'keys', provider_name)
    if not os.path.isdir(path):
        os.makedirs(path, mode=0o755, exist_ok=True)

    return path
