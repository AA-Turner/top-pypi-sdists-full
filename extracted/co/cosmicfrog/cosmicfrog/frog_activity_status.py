from enum import Enum
import json

class ActivityStatus(Enum):
    """
    Model activity statuses.
    PENDING -> STARTED -> Terminal(COMPLETED or FAILED)
    """

    PENDING = "pending"
    STARTED = "started"
    COMPLETED = "completed"
    FAILED = "failed"

# print status as json object
# it will be used by FE to adjust activity status
def log_status(
    status: ActivityStatus,
    error: str = '',
):
    data = {"frogstatus": {"status": status, "error": error}}
    print(json.dumps(data))