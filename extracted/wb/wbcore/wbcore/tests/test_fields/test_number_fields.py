from decimal import Decimal

import pytest
from rest_framework.exceptions import ValidationError

from wbcore.serializers import DecimalField, FloatField, IntegerField
from wbcore.serializers.fields import YearField
from wbcore.serializers.fields.types import WBCoreType


class TestIntegerField:
    def setup_method(self):
        self.field = IntegerField()

    def test_not_none(self):
        assert self.field is not None

    @pytest.mark.parametrize("input, expected", [(1, 1), ("1", 1), (-1, -1), (0, 0)])
    def test_to_internal_value(self, input, expected):
        assert self.field.to_internal_value(input) == expected

    @pytest.mark.parametrize("input", [None, [], "a", "", {}, 1.2])
    def test_to_internal_value_validation_error(self, input):
        with pytest.raises(ValidationError):
            self.field.to_internal_value(input)

    def test_field_type(self):
        assert self.field.field_type == WBCoreType.NUMBER.value

    def test_representation(self):
        assert self.field.get_representation(None, "field_name") == (
            "field_name",
            {
                "key": "field_name",
                "label": None,
                "type": self.field.field_type,
                "required": True,
                "read_only": False,
                "display_mode": "decimal",
                "precision": 0,
                "max_digits": 34,
                "decorators": [],
                "depends_on": [],
                "signed": True,
                "disable_formatting": False,
            },
        )


class TestDecimalField:
    def setup_method(self):
        self.field = DecimalField(decimal_places=2, max_digits=5)

    def test_not_none(self):
        assert self.field is not None

    @pytest.mark.parametrize(
        "input, expected",
        [(1.0, Decimal(1)), ("1.0", Decimal(1)), (-1.0, Decimal(-1)), (0, Decimal(0))],
    )
    def test_to_internal_value(self, input, expected):
        assert self.field.to_internal_value(input) == expected

    @pytest.mark.parametrize("input", [None, [], "a", "", {}])
    def test_to_internal_value_validation_error(self, input):
        with pytest.raises(ValidationError):
            self.field.to_internal_value(input)

    def test_field_type(self):
        assert self.field.field_type == WBCoreType.NUMBER.value

    def test_representation(self):
        assert self.field.get_representation(None, "field_name") == (
            "field_name",
            {
                "key": "field_name",
                "label": None,
                "type": self.field.field_type,
                "required": True,
                "read_only": False,
                "precision": 2,
                "max_digits": 5,
                "decorators": [],
                "depends_on": [],
                "display_mode": "decimal",
                "signed": True,
                "disable_formatting": False,
            },
        )

    def test_percent_representation(self):
        _field = self.field
        _field.percent = True
        assert _field.get_representation(None, "field_name") == (
            "field_name",
            {
                "key": "field_name",
                "label": None,
                "type": WBCoreType.PERCENT.value,
                "required": True,
                "read_only": False,
                "precision": 0,
                "max_digits": 5,
                "decorators": [],
                "depends_on": [],
                "display_mode": "decimal",
                "signed": True,
                "disable_formatting": False,
            },
        )


class TestFloatField:
    def setup_method(self):
        self.field = FloatField()

    def test_not_none(self):
        assert self.field is not None

    @pytest.mark.parametrize("input, expected", [(1.0, 1.0), ("1.0", 1.0), (-1.0, -1.0), (0, 0)])
    def test_to_internal_value(self, input, expected):
        assert self.field.to_internal_value(input) == expected

    @pytest.mark.parametrize("input", [None, [], "a", "", {}])
    def test_to_internal_value_validation_error(self, input):
        with pytest.raises(ValidationError):
            self.field.to_internal_value(input)

    def test_field_type(self):
        assert self.field.field_type == WBCoreType.NUMBER.value

    def test_representation(self):
        assert self.field.get_representation(None, "field_name") == (
            "field_name",
            {
                "key": "field_name",
                "label": None,
                "type": self.field.field_type,
                "required": True,
                "read_only": False,
                "precision": 2,
                "max_digits": 34,
                "decorators": [],
                "depends_on": [],
                "display_mode": "decimal",
                "signed": True,
                "disable_formatting": False,
            },
        )


class TestYearField:
    @pytest.mark.parametrize(
        (
            "key",
            "label",
        ),
        [
            ("Foo", "Bar"),
        ],
    )
    def test_year_field_values(self, key, label):
        field = YearField(label=label, precision=2)
        representation = field.get_representation(None, key)[1]
        assert representation["precision"] == 0
        assert representation["disable_formatting"] == True
