from typing import Any, cast, Dict, List, Optional, Type, TypeVar

import attr

from ..extensions import NotPresentError
from ..types import UNSET, Unset

T = TypeVar("T", bound="WebhookEnvelopeV0AppDefinition")


@attr.s(auto_attribs=True, repr=False)
class WebhookEnvelopeV0AppDefinition:
    """  """

    _id: str
    _version_number: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("id={}".format(repr(self._id)))
        fields.append("version_number={}".format(repr(self._version_number)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "WebhookEnvelopeV0AppDefinition({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        id = self._id
        version_number = self._version_number

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if id is not UNSET:
            field_dict["id"] = id
        if version_number is not UNSET:
            field_dict["versionNumber"] = version_number

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_id() -> str:
            id = d.pop("id")
            return id

        try:
            id = get_id()
        except KeyError:
            if strict:
                raise
            id = cast(str, UNSET)

        def get_version_number() -> str:
            version_number = d.pop("versionNumber")
            return version_number

        try:
            version_number = get_version_number()
        except KeyError:
            if strict:
                raise
            version_number = cast(str, UNSET)

        webhook_envelope_v0_app_definition = cls(
            id=id,
            version_number=version_number,
        )

        webhook_envelope_v0_app_definition.additional_properties = d
        return webhook_envelope_v0_app_definition

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
    def id(self) -> str:
        """ App definition id """
        if isinstance(self._id, Unset):
            raise NotPresentError(self, "id")
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        self._id = value

    @property
    def version_number(self) -> str:
        """ App definition version number """
        if isinstance(self._version_number, Unset):
            raise NotPresentError(self, "version_number")
        return self._version_number

    @version_number.setter
    def version_number(self, value: str) -> None:
        self._version_number = value
