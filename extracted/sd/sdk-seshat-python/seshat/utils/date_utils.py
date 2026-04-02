from datetime import datetime
from datetime import timezone


def format_datetime_for_api(dt_value):
    """Convert datetime to API-expected format with timezone."""

    if dt_value is None or dt_value == "":
        return None

    # If it's a string, parse it first
    if isinstance(dt_value, str):
        # Handle the YYYY-MM-DDTHH:MM format
        if len(dt_value) == 16:  # Format without seconds
            dt_value = datetime.strptime(dt_value, "%Y-%m-%dT%H:%M")
        else:
            # Try to parse as is
            dt_value = datetime.fromisoformat(dt_value)

    # If it's a datetime object, format it to ISO with timezone
    if isinstance(dt_value, datetime):
        # If datetime is naive (no timezone), assume UTC
        if dt_value.tzinfo is None:
            # Add UTC timezone
            dt_value = dt_value.replace(tzinfo=timezone.utc)
        # Format to ISO string with timezone
        return dt_value.isoformat()

    return dt_value
