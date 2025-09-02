import datetime


def to_grafana_time_format(date: str) -> str | int:
    try:
        date = datetime.datetime.fromisoformat(date)
    except ValueError:
        pass
    else:
        date = int(date.timestamp() * 1000)

    return date
