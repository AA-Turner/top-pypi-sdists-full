"""Compare user construction with the legacy Python SDK when it is installed."""

import json

from statsig_python_core import StatsigUser
from user_creation_benchmark import summarize, time_action


def main():
    fields = {
        "user_id": "a-user",
        "email": "test@example.com",
        "ip": "1.2.3.4",
        "country": "US",
        "locale": "en-US",
        "app_version": "1.0.0",
        "user_agent": "Mozilla/5.0 (iPhone; iOS 16.6) Safari/604.1",
        "custom": {"key": "value", "key2": 123, "key3": 1.23, "key4": True, "key5": ["1", "2", "3"]},
        "private_attributes": {
            "private_key": "value",
            "private_key2": 123,
            "private_key3": 1.23,
            "private_key4": True,
            "private_key5": ["2", "3", "4"],
        },
    }
    implementations = {"core": StatsigUser}
    try:
        from statsig import StatsigUser as LegacyStatsigUser
    except ImportError:
        pass
    else:
        implementations["legacy"] = LegacyStatsigUser

    for label, constructor in implementations.items():
        samples = [time_action(lambda: constructor(**fields), 10_000) for _ in range(10)]
        print(f"{label} StatsigUser: {json.dumps(summarize(samples))}")


if __name__ == "__main__":
    main()
