from typing import Any, cast, Dict, List, Type, TypeVar

import attr

from ..extensions import NotPresentError
from ..models.container_bulk_update_item import ContainerBulkUpdateItem
from ..types import UNSET, Unset

T = TypeVar("T", bound="ContainersBulkUpdateRequest")


@attr.s(auto_attribs=True, repr=False)
class ContainersBulkUpdateRequest:
    """  """

    _containers: List[ContainerBulkUpdateItem]

    def __repr__(self):
        fields = []
        fields.append("containers={}".format(repr(self._containers)))
        return "ContainersBulkUpdateRequest({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        containers = []
        for containers_item_data in self._containers:
            containers_item = containers_item_data.to_dict()

            containers.append(containers_item)

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if containers is not UNSET:
            field_dict["containers"] = containers

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_containers() -> List[ContainerBulkUpdateItem]:
            containers = []
            _containers = d.pop("containers")
            for containers_item_data in _containers:
                containers_item = ContainerBulkUpdateItem.from_dict(containers_item_data, strict=False)

                containers.append(containers_item)

            return containers

        try:
            containers = get_containers()
        except KeyError:
            if strict:
                raise
            containers = cast(List[ContainerBulkUpdateItem], UNSET)

        containers_bulk_update_request = cls(
            containers=containers,
        )

        return containers_bulk_update_request

    @property
    def containers(self) -> List[ContainerBulkUpdateItem]:
        if isinstance(self._containers, Unset):
            raise NotPresentError(self, "containers")
        return self._containers

    @containers.setter
    def containers(self, value: List[ContainerBulkUpdateItem]) -> None:
        self._containers = value
