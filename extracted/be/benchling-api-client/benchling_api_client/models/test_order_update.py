from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.test_order_status import TestOrderStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="TestOrderUpdate")


@attr.s(auto_attribs=True, repr=False)
class TestOrderUpdate:
    """  """

    _container_id: Union[Unset, str] = UNSET
    _status: Union[Unset, TestOrderStatus] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("container_id={}".format(repr(self._container_id)))
        fields.append("status={}".format(repr(self._status)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "TestOrderUpdate({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        container_id = self._container_id
        status: Union[Unset, int] = UNSET
        if not isinstance(self._status, Unset):
            status = self._status.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if container_id is not UNSET:
            field_dict["containerId"] = container_id
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_container_id() -> Union[Unset, str]:
            container_id = d.pop("containerId")
            return container_id

        try:
            container_id = get_container_id()
        except KeyError:
            if strict:
                raise
            container_id = cast(Union[Unset, str], UNSET)

        def get_status() -> Union[Unset, TestOrderStatus]:
            status = UNSET
            _status = d.pop("status")
            if _status is not None and _status is not UNSET:
                try:
                    status = TestOrderStatus(_status)
                except ValueError:
                    status = TestOrderStatus.of_unknown(_status)

            return status

        try:
            status = get_status()
        except KeyError:
            if strict:
                raise
            status = cast(Union[Unset, TestOrderStatus], UNSET)

        test_order_update = cls(
            container_id=container_id,
            status=status,
        )

        test_order_update.additional_properties = d
        return test_order_update

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties

    def get(self, key, default=None) -> Optional[Any]:
        return self.additional_properties.get(key, default)

    @property
    def container_id(self) -> str:
        """ The ID of the container associated with the sample being tested. """
        if isinstance(self._container_id, Unset):
            raise NotPresentError(self, "container_id")
        return self._container_id

    @container_id.setter
    def container_id(self, value: str) -> None:
        self._container_id = value

    @container_id.deleter
    def container_id(self) -> None:
        self._container_id = UNSET

    @property
    def status(self) -> TestOrderStatus:
        """The status of a test order."""
        if isinstance(self._status, Unset):
            raise NotPresentError(self, "status")
        return self._status

    @status.setter
    def status(self, value: TestOrderStatus) -> None:
        self._status = value

    @status.deleter
    def status(self) -> None:
        self._status = UNSET
