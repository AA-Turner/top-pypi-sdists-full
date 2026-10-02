from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.run_config_customer_secret_attachment_list_dto_items_properties_scope_problem_version_level import RunConfigCustomerSecretAttachmentListDtoItemsPropertiesScopeProblemVersionLevel
from uuid import UUID






T = TypeVar("T", bound="RunConfigCustomerSecretAttachmentListDtoItemsPropertiesScopeProblemVersion")



@_attrs_define
class RunConfigCustomerSecretAttachmentListDtoItemsPropertiesScopeProblemVersion:
    """ 
        Attributes:
            level (RunConfigCustomerSecretAttachmentListDtoItemsPropertiesScopeProblemVersionLevel): Problem-version-scoped
                secret pinned to one specific problem version.
            id (UUID): Problem version that owns the secret.
     """

    level: RunConfigCustomerSecretAttachmentListDtoItemsPropertiesScopeProblemVersionLevel
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
        level = RunConfigCustomerSecretAttachmentListDtoItemsPropertiesScopeProblemVersionLevel(d.pop("level"))




        id = UUID(d.pop("id"))




        run_config_customer_secret_attachment_list_dto_items_properties_scope_problem_version = cls(
            level=level,
            id=id,
        )

        return run_config_customer_secret_attachment_list_dto_items_properties_scope_problem_version

