import json
import logging
import platform
import uuid
from pathlib import Path

logger = logging.getLogger(__name__)


def get_system_user_id(drc_path: Path) -> str:
    user_file = drc_path / "state_user.json"
    try:
        if user_file.exists():
            data = json.loads(user_file.read_text())
            existing = data.get("system_user_id", "")
            try:
                parsed = uuid.UUID(existing)
                if existing == parsed.hex:
                    return existing
                new_id = parsed.hex
            except (ValueError, AttributeError):
                new_id = uuid.uuid4().hex
        else:
            new_id = uuid.uuid4().hex
        user_file.parent.mkdir(parents=True, exist_ok=True)
        user_file.write_text(json.dumps({"system_user_id": new_id}))
        return new_id
    except OSError:
        logger.warning("Failed to persist system_user_id; using in-memory value")
        return uuid.uuid4().hex


def get_os_name() -> str:
    return platform.system()
