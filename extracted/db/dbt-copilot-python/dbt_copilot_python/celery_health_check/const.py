import tempfile
from pathlib import Path

READINESS_FILE = Path(f"{tempfile.gettempdir()}/celery_ready")
HEARTBEAT_FILE = Path(f"{tempfile.gettempdir()}/celery_worker_heartbeat")
