from django.db import connection

import pytest

pytest.importorskip("enum_properties")
from importlib.util import find_spec
from tests.test_requests import TestRequests
from tests.enum_prop.models import EnumTester
from django.urls import reverse
from datetime import datetime


class TestRequestsProps(TestRequests):
    MODEL_CLASS = EnumTester
    NAMESPACE = "tests_enum_prop"

    @property
    def post_params(self):
        return {
            "small_pos_int": self.SmallPosIntEnum.VAL2,
            "small_int": self.SmallIntEnum.VAL0,
            "pos_int": self.PosIntEnum.VAL1,
            "int": self.IntEnum.VALn1,
            "big_pos_int": self.BigPosIntEnum.VAL3,
            "big_int": self.BigIntEnum.VAL2,
            "date_enum": self.DateEnum.BRIAN.value,
            "datetime_enum": self.DateTimeEnum.PINATUBO.value,
            "duration_enum": self.DurationEnum.FORTNIGHT.value,
            "time_enum": self.TimeEnum.LUNCH.value,
            "decimal_enum": self.DecimalEnum.THREE.value,
            "constant": self.Constants.GOLDEN_RATIO,
            "text": self.TextEnum.VALUE2,
            "extern": self.ExternEnum.TWO,
            "dj_int_enum": self.DJIntEnum.TWO,
            "dj_text_enum": self.DJTextEnum.C,
            "non_strict_int": self.SmallPosIntEnum.VAL1,
            "non_strict_text": self.TextEnum.VALUE2,
            "no_coerce": self.SmallPosIntEnum.VAL3,
        }

    @property
    def post_params_symmetric(self):
        return {
            "small_pos_int": self.SmallPosIntEnum.VAL2,
            "small_int": "Value 0",
            "pos_int": self.PosIntEnum.VAL1,
            "int": -2147483648,
            "big_pos_int": self.BigPosIntEnum.VAL2,
            "big_int": self.BigPosIntEnum.VAL2,
            "date_enum": self.DateEnum.BRIAN.value,
            "datetime_enum": datetime(
                year=1964, month=3, day=28, hour=17, minute=36, second=0
            ),
            "duration_enum": self.DurationEnum.FORTNIGHT.value,
            "time_enum": self.TimeEnum.LUNCH.value,
            "decimal_enum": self.DecimalEnum.THREE.value,
            "constant": "φ",
            "text": "v two",
            "extern": "two",
            "dj_int_enum": self.DJIntEnum.TWO,
            "dj_text_enum": self.DJTextEnum.C,
            "non_strict_int": 150,
            "non_strict_text": "arbitrary",
            "no_coerce": "Value 32767",
        }

    @property
    def field_filter_properties(self):
        return {
            "small_pos_int": ["value", "name", "label"],
            "small_int": ["value", "name", "label"],
            "pos_int": ["value", "name", "label"],
            "int": ["value", "name", "label"],
            "big_pos_int": ["value", "name", "label"],
            "big_int": ["value", "name", "label", "pos"],
            "constant": ["value", "name", "label", "symbol"],
            "text": ["value", "name", "label", "aliases"],
            "date_enum": ["value", "name", "label"],
            "datetime_enum": ["value", "name", "label"],
            "duration_enum": ["value", "name", "label"],
            "time_enum": ["value", "name", "label"],
            "decimal_enum": ["value", "name", "label"],
            "extern": ["value", "name", "label"],
            "dj_int_enum": ["value"],
            "dj_text_enum": ["value"],
            "non_strict_int": ["value", "name", "label"],
            "non_strict_text": ["value", "name", "label"],
            "no_coerce": ["value", "name", "label"],
        }

    if find_spec("django_filters"):

        def test_django_filter(self):
            self.do_test_django_filter(
                reverse(f"{self.NAMESPACE}:enum-filter-symmetric"),
                skip_non_strict=False,
            )

        @pytest.mark.skipif(
            connection.vendor == "oracle",
            reason="strict NULL behavior on Oracle >21c breaks exclude filter tests",
        )
        def test_django_filter_exclude(self):
            self.do_test_django_filter(
                reverse(f"{self.NAMESPACE}:enum-filter-symmetric-exclude"),
                skip_non_strict=False,
                exclude=True,
            )

        def test_django_filter_multiple(self):
            self.do_test_django_filter(
                reverse(f"{self.NAMESPACE}:enum-filter-multiple"),
                multi=True,
                skip_non_strict=False,
            )

        @pytest.mark.skipif(
            connection.vendor == "oracle",
            reason="strict NULL behavior on Oracle >21c breaks this test",
        )
        def test_django_filter_multiple_exclude(self):
            self.do_test_django_filter(
                reverse(f"{self.NAMESPACE}:enum-filter-multiple-exclude"),
                multi=True,
                exclude=True,
            )


# don't run these tests again!
TestRequests = None
