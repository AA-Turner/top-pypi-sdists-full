# See https://medium.com/ambient-innovation/health-checks-for-celery-in-kubernetes-cf3274a3e106

import sys
from datetime import datetime

from celery import signals
from dateutil.tz import tz

from .const import HEARTBEAT_FILE
from .const import READINESS_FILE
from .heartbeat import HeartBeat


def on_worker_ready(**_):
    READINESS_FILE.touch()


def on_worker_shutdown(**_):
    READINESS_FILE.unlink(missing_ok=True)


def setup(celery_app=None):
    signals.worker_ready.connect(on_worker_ready)

    signals.worker_shutdown.connect(on_worker_shutdown)

    celery_app.steps["worker"].add(HeartBeat)
    return celery_app


def check_health():
    if not READINESS_FILE.is_file():
        print("Healthcheck: Celery readiness file NOT found.")
        sys.exit(1)

    if not HEARTBEAT_FILE.is_file():
        print("Healthcheck: Celery heartbeat file NOT found.")
        sys.exit(1)

    heartbeat_timestamp = float(HEARTBEAT_FILE.read_text())
    current_timestamp = datetime.timestamp(datetime.now(tz=tz.UTC))
    time_diff = current_timestamp - heartbeat_timestamp
    if time_diff > 60:
        print(
            "Healthcheck: Celery Worker heartbeat file timestamp "
            + "DOES NOT match the given constraint."
        )
        sys.exit(1)

    print(
        "Healthcheck: Celery Worker heartbeat file found and timestamp "
        + "matches the given constraint."
    )
    sys.exit(0)


if __name__ == "__main__":
    check_health()
