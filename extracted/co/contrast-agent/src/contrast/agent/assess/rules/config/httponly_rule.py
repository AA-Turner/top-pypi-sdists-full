# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.


class HttpOnlyRuleMixin:
    @property
    def name(self):
        return "httponly"

    def is_violated(self, value):
        """
        The rule is violated if the value is False or if it is not set at all (None)
        """
        if self.count_threshold_reached():
            return False
        return not value
