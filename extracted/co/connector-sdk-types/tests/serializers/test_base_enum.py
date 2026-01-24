from typing import Generic

import pytest
from connector_sdk_types.serializers.enum import BaseEnum
from pydantic import BaseModel, ValidationError
from typing_extensions import TypeVar

T = TypeVar("T", bound=BaseEnum)


class StrEnumWithUnknown(str, BaseEnum):
    KEY_1 = "VALUE_1"
    KEY_2 = "VALUE_2"

    UNKNOWN = "UNKNOWN"


class StrEnumWithoutUnknown(str, BaseEnum):
    KEY_1 = "VALUE_1"
    KEY_2 = "VALUE_2"


class IntEnumWithUnknown(int, BaseEnum):
    KEY_1 = 0
    KEY_2 = 1

    UNKNOWN = -1


class IntEnumWithoutUnknown(int, BaseEnum):
    KEY_1 = 0
    KEY_2 = 1


class MockModel(BaseModel, Generic[T]):
    enum: T


class TestStrBaseEnum:
    def test_missing_value(self):
        assert StrEnumWithUnknown("missing") == StrEnumWithUnknown.UNKNOWN

    def test_missing_unknown(self):
        with pytest.raises(AttributeError):
            StrEnumWithoutUnknown("missing")

    def test_valid_members_with_unknown(self):
        valid_members = list(StrEnumWithUnknown.valid_members())
        expected_members = [member for member in StrEnumWithUnknown if member.name != "UNKNOWN"]
        assert valid_members == expected_members

    def test_valid_members_without_unknown(self):
        valid_members = list(StrEnumWithoutUnknown.valid_members())
        expected_members = [member for member in StrEnumWithoutUnknown if member.name != "UNKNOWN"]
        assert valid_members == expected_members


class TestIntBaseEnum:
    def test_missing_value(self):
        assert IntEnumWithUnknown("missing") == IntEnumWithUnknown.UNKNOWN

    def test_missing_unknown(self):
        with pytest.raises(AttributeError):
            IntEnumWithoutUnknown("missing")

    def test_valid_members_with_unknown(self):
        valid_members = list(IntEnumWithUnknown.valid_members())
        expected_members = [member for member in IntEnumWithUnknown if member.name != "UNKNOWN"]
        assert valid_members == expected_members

    def test_valid_members_without_unknown(self):
        valid_members = list(IntEnumWithoutUnknown.valid_members())
        expected_members = [member for member in IntEnumWithoutUnknown if member.name != "UNKNOWN"]
        assert valid_members == expected_members


class TestStrBaseEnumInPydantic:
    def test_missing_value(self):
        mock_model = MockModel[StrEnumWithUnknown].model_validate({"enum": "missing"})
        assert mock_model.enum == StrEnumWithUnknown.UNKNOWN

    def test_missing_unknown(self):
        with pytest.raises(ValidationError):
            MockModel[IntEnumWithoutUnknown].model_validate({"enum": "missing"})


class TestIntBaseEnumInPydantic:
    def test_missing_value(self):
        mock_model = MockModel[IntEnumWithUnknown].model_validate({"enum": 2})
        assert mock_model.enum == IntEnumWithUnknown.UNKNOWN

    def test_missing_unknown(self):
        with pytest.raises(ValidationError):
            MockModel[IntEnumWithoutUnknown].model_validate({"enum": 2})
