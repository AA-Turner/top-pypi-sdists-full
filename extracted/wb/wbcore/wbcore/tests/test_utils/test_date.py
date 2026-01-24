from datetime import date

import pytest
from rest_framework.test import APIRequestFactory

from wbcore.utils.date import get_date_interval_from_request, shortcut
from wbcore.utils.date_builder import Day, Now, WeekStart


class TestGetDateInterval:
    def setup_method(self):
        self.request_factory = APIRequestFactory()

    @pytest.mark.parametrize("start_key", ["start", "start_date", "from", "date_gte"])
    @pytest.mark.parametrize("start", [date(2010, 1, 1)])
    @pytest.mark.parametrize("end_key", ["end", "end_date", "to", "date_lte"])
    @pytest.mark.parametrize("end", [date(2010, 1, 1)])
    def test_get_date_interval_from_request(self, start_key, start, end_key, end):
        request = self.request_factory.get(
            path="",
            data={
                start_key: start.strftime("%Y-%m-%d"),
                end_key: end.strftime("%Y-%m-%d"),
            },
        )
        _start, _end = get_date_interval_from_request(request)

        assert _start == start
        assert _end == end

    def test_get_date_interval_from_request_none(self):
        request = self.request_factory.get(
            path="",
        )
        _start, _end = get_date_interval_from_request(request)

        assert _start is None
        assert _end is None

    def test_get_date_interval_from_request_wrong_date_format(self):
        request = self.request_factory.get(path="", data={"start": "abc", "end": "def"})
        _start, _end = get_date_interval_from_request(request)

        assert _start is None
        assert _end is None


class TestShortcut:
    def test_shortcut(self):
        assert shortcut("ABC", WeekStart - Day, Now) == {"label": "ABC", "value": f"{str(WeekStart-Day)},{str(Now)}"}
