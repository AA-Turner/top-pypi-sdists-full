from typing import (
    Any,
    Dict,
    Type,
    TypeVar,
    Tuple,
    Optional,
    BinaryIO,
    TextIO,
    TYPE_CHECKING,
)

from typing import List


import attr

from ..types import UNSET, Unset

from typing import Union
from typing import cast
from typing import Dict
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.deploy_app_json_body_secrets import DeployAppJsonBodySecrets


T = TypeVar("T", bound="DeployAppJsonBody")


@attr.s(auto_attribs=True)
class DeployAppJsonBody:
    """
    ### Attributes:
    * `secrets (Union[Unset, DeployAppJsonBodySecrets])`: A key value bag of strings to store sensitive information. Example: {'key': 'value'}
    """

    secrets: Union[Unset, "DeployAppJsonBodySecrets"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.deploy_app_json_body_secrets import DeployAppJsonBodySecrets

        secrets: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.secrets, Unset):
            secrets = self.secrets.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if secrets is not UNSET:
            field_dict["secrets"] = secrets

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.deploy_app_json_body_secrets import DeployAppJsonBodySecrets

        d = src_dict.copy()
        _secrets = d.pop("secrets", UNSET)
        secrets: Union[Unset, DeployAppJsonBodySecrets]
        if isinstance(_secrets, Unset):
            secrets = UNSET
        else:
            secrets = DeployAppJsonBodySecrets.from_dict(_secrets)

        deploy_app_json_body = cls(
            secrets=secrets,
        )

        deploy_app_json_body.additional_properties = d
        return deploy_app_json_body

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
