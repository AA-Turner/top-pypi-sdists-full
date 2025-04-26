import threading
from datetime import datetime, timezone

from tinybird_cdk import config

_LOCK = threading.Lock()

def debug(message):
    log('DEBUG', message)

def info(message):
    log('INFO', message)

def warning(message):
    log('WARNING', message)

def error(message):
    log('ERROR', message)

def log(level, message):
    now = datetime.now(timezone.utc).astimezone().isoformat(timespec='seconds')
    tag = config.get('TB_CDK_TAG')
    with _LOCK:
        print(f'[{now}][{tag}][{level}] {message}')
