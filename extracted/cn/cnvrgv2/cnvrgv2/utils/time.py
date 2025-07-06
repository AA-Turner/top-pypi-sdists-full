from datetime import timedelta, datetime

from dateutil.relativedelta import relativedelta


def get_relative_time(days=None, months=None, hours=None):
    """
    Get relative time
    @param days: Number of days
    @param months: Number of months
    @param hours: Number of hours
    @return: Time
    """

    now = datetime.now()
    if days:
        return (now - timedelta(days=days)).strftime("%Y-%m-%d %H:%M:%S %z")
    if months:
        return (now - relativedelta(months=months)).strftime("%Y-%m-%d %H:%M:%S %z")
    if hours:
        return (now - timedelta(hours=hours)).strftime("%Y-%m-%d %H:%M:%S %z")
    return now.strftime("%Y-%m-%d %H:%M:%S %z")
