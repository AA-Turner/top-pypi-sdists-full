from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_environment_setup_template import ManagedAgentsEnvironmentSetupTemplate





T = TypeVar("T", bound="ManagedAgentsEnvironmentSetupTemplateListResponse")



@_attrs_define
class ManagedAgentsEnvironmentSetupTemplateListResponse:
    """ Starting-point setup scripts the console and agents share. Copy one into setup.script and edit it; none is a preset
    that has to be used as is.

        Example:
            {'items': [{'accelerator': True, 'id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'script': 'example', 'summary':
                'example', 'title': 'example'}]}

        Attributes:
            items (list[ManagedAgentsEnvironmentSetupTemplate]): Starting-point setup scripts. Static per deployment;
                identical for every organization.
            templates (list[ManagedAgentsEnvironmentSetupTemplate] | Unset): Deprecated compatibility alias for items,
                retained for older browser clients during rollout.
     """

    items: list[ManagedAgentsEnvironmentSetupTemplate]
    templates: list[ManagedAgentsEnvironmentSetupTemplate] | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_environment_setup_template import ManagedAgentsEnvironmentSetupTemplate # noqa: PLC0415
        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()
            items.append(items_item)



        templates: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.templates, Unset):
            templates = []
            for templates_item_data in self.templates:
                templates_item = templates_item_data.to_dict()
                templates.append(templates_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "items": items,
        })
        if templates is not UNSET:
            field_dict["templates"] = templates

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_environment_setup_template import ManagedAgentsEnvironmentSetupTemplate # noqa: PLC0415
        d = dict(src_dict)
        items = []
        _items = d.pop("items")
        for items_item_data in (_items):
            items_item = ManagedAgentsEnvironmentSetupTemplate.from_dict(items_item_data)



            items.append(items_item)


        _templates = d.pop("templates", UNSET)
        templates: list[ManagedAgentsEnvironmentSetupTemplate] | Unset = UNSET
        if _templates is not UNSET:
            templates = []
            for templates_item_data in _templates:
                templates_item = ManagedAgentsEnvironmentSetupTemplate.from_dict(templates_item_data)



                templates.append(templates_item)


        managed_agents_environment_setup_template_list_response = cls(
            items=items,
            templates=templates,
        )

        return managed_agents_environment_setup_template_list_response

