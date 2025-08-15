# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, f-string-without-interpolation, too-many-branches, too-many-statements, unnecessary-pass
from dataclasses import dataclass
from typing import Any, Dict, List
from collections.abc import Iterable
import zaber_bson


@dataclass
class DeviceDbInnerError:
    """
    One of the errors that occurred while trying to access information from the device database.
    """

    code: str
    """
    Code describing type of the error.
    """

    message: str
    """
    Description of the error.
    """

    inner_errors: List['DeviceDbInnerError']
    """
    A list of errors that occurred while trying to access information from the device database.
    """

    @staticmethod
    def zero_values() -> 'DeviceDbInnerError':
        return DeviceDbInnerError(
            code="",
            message="",
            inner_errors=[],
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'DeviceDbInnerError':
        """" Deserialize a binary representation of this class. """
        data = zaber_bson.loads(data_bytes)  # type: Dict[str, Any]
        return DeviceDbInnerError.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        self.validate()
        return zaber_bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'code': str(self.code or ''),
            'message': str(self.message or ''),
            'innerErrors': [item.to_dict() for item in self.inner_errors] if self.inner_errors is not None else [],
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'DeviceDbInnerError':
        return DeviceDbInnerError(
            code=data.get('code'),  # type: ignore
            message=data.get('message'),  # type: ignore
            inner_errors=[DeviceDbInnerError.from_dict(item) for item in data.get('innerErrors')],  # type: ignore
        )

    def validate(self) -> None:
        """" Validates the properties of the instance. """
        if self.code is not None:
            if not isinstance(self.code, str):
                raise ValueError(f'Property "Code" of "DeviceDbInnerError" is not a string.')

        if self.message is not None:
            if not isinstance(self.message, str):
                raise ValueError(f'Property "Message" of "DeviceDbInnerError" is not a string.')

        if self.inner_errors is not None:
            if not isinstance(self.inner_errors, Iterable):
                raise ValueError('Property "InnerErrors" of "DeviceDbInnerError" is not iterable.')

            for i, inner_errors_item in enumerate(self.inner_errors):
                if inner_errors_item is None:
                    raise ValueError(f'Item {i} in property "InnerErrors" of "DeviceDbInnerError" is None.')

                if not isinstance(inner_errors_item, DeviceDbInnerError):
                    raise ValueError(f'Item {i} in property "InnerErrors" of "DeviceDbInnerError" is not an instance of "DeviceDbInnerError".')

                inner_errors_item.validate()
