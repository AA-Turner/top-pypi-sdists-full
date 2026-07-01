from datetime import datetime
from typing import Optional

from croniter import CroniterBadCronError, CroniterBadDateError, croniter

# A fixed reference time keeps validation deterministic. Impossible schedules
# raise regardless of the reference; valid ones simply compute a next fire.
_REFERENCE = datetime(2000, 1, 1)


def cron_schedule_error(schedule: Optional[str]) -> Optional[str]:
    """Return a human-readable reason if `schedule` is an invalid cron, else None.

    A blank/empty schedule means "no schedule" (the job is simply not registered
    with the scheduler) and is intentionally allowed. Detects both malformed
    expressions and ones that parse but can never fire (e.g. "0 0 31 2 *" =
    February 31, which never exists). Fails open on unexpected croniter errors so
    a library quirk can't reject an otherwise-valid schedule.
    """
    if not schedule or not schedule.strip():
        return None
    expr = schedule.strip()
    try:
        croniter(expr, _REFERENCE).get_next(datetime)
    except CroniterBadDateError:
        return "the schedule has no valid date and will never fire"
    except CroniterBadCronError as e:
        return f"{e}"
    except Exception:
        return None
    return None
