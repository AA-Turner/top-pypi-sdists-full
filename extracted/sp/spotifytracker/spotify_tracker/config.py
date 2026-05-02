import os
import yaml

CONFIG_DIR = '/usr/local/etc/spotify_tracker'
CONFIG_PATH = os.path.join(CONFIG_DIR, 'config.yml')
SCOPE = 'playlist-modify-public'
KEYS = {'username', 'client_id', 'client_secret', 'callback_url', 'token',
        'playlist_id'}


def ensure_config_file_exists():
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)
    if not os.path.exists(CONFIG_PATH):
        open(CONFIG_PATH, 'a')


def _load(filepath):
    with open(filepath, 'r') as f:
        return yaml.safe_load(f.read()) or {}


def _dump(doc):
    return yaml.dump(doc, default_flow_style=False)


def get_config():
    return _load(CONFIG_PATH)


def save_config(config):
    with open(CONFIG_PATH, 'w') as f:
        f.write(_dump(config))


def get_config_value(key):
    return get_config().get(key)


def save_config_value(key, value):
    current_config = get_config()
    current_config[key] = value
    save_config(current_config)
