# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import contextlib
from datetime import datetime, timedelta


class SessionAgeRuleMixin:
    @property
    def name(self):
        return "session-timeout"

    def is_violated(self, value):
        """
        A value of 30 mins or less is considered safe

        Flask represents this value as either a timedelta or as an integer in seconds.
        Falcon represents this value as a datetime (e.g. cookie "expires").
        """
        if self.count_threshold_reached():
            return False
        if isinstance(value, timedelta):
            return value > timedelta(minutes=30)

        if isinstance(value, datetime):
            seconds = (value - datetime.now(value.tzinfo)).total_seconds()
            return seconds > 30 * 60

        if isinstance(value, str):
            with contextlib.suppress(ValueError):
                value = int(value)

        return value is None or value > 30 * 60
