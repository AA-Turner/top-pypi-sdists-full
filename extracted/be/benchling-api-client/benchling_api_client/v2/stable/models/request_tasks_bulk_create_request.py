from typing import Any, cast, Dict, List, Type, TypeVar

import attr

from ..extensions import NotPresentError
from ..models.request_tasks_bulk_create import RequestTasksBulkCreate
from ..types import UNSET, Unset

T = TypeVar("T", bound="RequestTasksBulkCreateRequest")


@attr.s(auto_attribs=True, repr=False)
class RequestTasksBulkCreateRequest:
    """  """

    _tasks: List[RequestTasksBulkCreate]

    def __repr__(self):
        fields = []
        fields.append("tasks={}".format(repr(self._tasks)))
        return "RequestTasksBulkCreateRequest({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        tasks = []
        for tasks_item_data in self._tasks:
            tasks_item = tasks_item_data.to_dict()

            tasks.append(tasks_item)

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if tasks is not UNSET:
            field_dict["tasks"] = tasks

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_tasks() -> List[RequestTasksBulkCreate]:
            tasks = []
            _tasks = d.pop("tasks")
            for tasks_item_data in _tasks:
                tasks_item = RequestTasksBulkCreate.from_dict(tasks_item_data, strict=False)

                tasks.append(tasks_item)

            return tasks

        try:
            tasks = get_tasks()
        except KeyError:
            if strict:
                raise
            tasks = cast(List[RequestTasksBulkCreate], UNSET)

        request_tasks_bulk_create_request = cls(
            tasks=tasks,
        )

        return request_tasks_bulk_create_request

    @property
    def tasks(self) -> List[RequestTasksBulkCreate]:
        """ The Legacy Request Tasks to create """
        if isinstance(self._tasks, Unset):
            raise NotPresentError(self, "tasks")
        return self._tasks

    @tasks.setter
    def tasks(self, value: List[RequestTasksBulkCreate]) -> None:
        self._tasks = value
