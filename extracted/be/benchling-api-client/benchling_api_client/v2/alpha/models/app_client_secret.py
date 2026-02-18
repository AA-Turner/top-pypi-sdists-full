from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..types import UNSET, Unset

T = TypeVar("T", bound="AppClientSecret")


@attr.s(auto_attribs=True, repr=False)
class AppClientSecret:
    """  """

    _client_secret: Union[Unset, str] = UNSET
    _id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("client_secret={}".format(repr(self._client_secret)))
        fields.append("id={}".format(repr(self._id)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "AppClientSecret({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        client_secret = self._client_secret
        id = self._id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if client_secret is not UNSET:
            field_dict["clientSecret"] = client_secret
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_client_secret() -> Union[Unset, str]:
            client_secret = d.pop("clientSecret")
            return client_secret

        try:
            client_secret = get_client_secret()
        except KeyError:
            if strict:
                raise
            client_secret = cast(Union[Unset, str], UNSET)

        def get_id() -> Union[Unset, str]:
            id = d.pop("id")
            return id

        try:
            id = get_id()
        except KeyError:
            if strict:
                raise
            id = cast(Union[Unset, str], UNSET)

        app_client_secret = cls(
            client_secret=client_secret,
            id=id,
        )

        app_client_secret.additional_properties = d
        return app_client_secret

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
    def client_secret(self) -> str:
        if isinstance(self._client_secret, Unset):
            raise NotPresentError(self, "client_secret")
        return self._client_secret

    @client_secret.setter
    def client_secret(self, value: str) -> None:
        self._client_secret = value

    @client_secret.deleter
    def client_secret(self) -> None:
        self._client_secret = UNSET

    @property
    def id(self) -> str:
        if isinstance(self._id, Unset):
            raise NotPresentError(self, "id")
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        self._id = value

    @id.deleter
    def id(self) -> None:
        self._id = UNSET
