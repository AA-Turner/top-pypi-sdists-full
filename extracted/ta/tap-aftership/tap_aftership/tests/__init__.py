"""Test suite for tap-aftership."""
import datetime

now = datetime.datetime.now(datetime.timezone.utc)
SAMPLE_CONFIG = {
    "start_date": (now - datetime.timedelta(days=1)).strftime("%Y-%m-%d"),
    "end_date": now.strftime("%Y-%m-%d"),
    "api_key": "test-api-key",
}
