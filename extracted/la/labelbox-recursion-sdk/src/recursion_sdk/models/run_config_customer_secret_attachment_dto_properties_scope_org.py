from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.run_config_customer_secret_attachment_dto_properties_scope_org_level import RunConfigCustomerSecretAttachmentDtoPropertiesScopeOrgLevel
from uuid import UUID






T = TypeVar("T", bound="RunConfigCustomerSecretAttachmentDtoPropertiesScopeOrg")



@_attrs_define
class RunConfigCustomerSecretAttachmentDtoPropertiesScopeOrg:
    """ 
        Attributes:
            level (RunConfigCustomerSecretAttachmentDtoPropertiesScopeOrgLevel): Org-scoped secret available within one
                organization.
            id (UUID): Organization that owns the secret.
     """

    level: RunConfigCustomerSecretAttachmentDtoPropertiesScopeOrgLevel
    id: UUID





    def to_dict(self) -> dict[str, Any]:
        level = self.level.value

        id = str(self.id)


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "level": level,
            "id": id,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        level = RunConfigCustomerSecretAttachmentDtoPropertiesScopeOrgLevel(d.pop("level"))




        id = UUID(d.pop("id"))




        run_config_customer_secret_attachment_dto_properties_scope_org = cls(
            level=level,
            id=id,
        )

        return run_config_customer_secret_attachment_dto_properties_scope_org

