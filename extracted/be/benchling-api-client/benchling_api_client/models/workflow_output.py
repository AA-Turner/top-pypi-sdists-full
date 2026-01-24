from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.archive_record import ArchiveRecord
from ..models.creation_origin import CreationOrigin
from ..models.fields import Fields
from ..models.workflow_output_summary import WorkflowOutputSummary
from ..models.workflow_task_group_summary import WorkflowTaskGroupSummary
from ..models.workflow_task_summary import WorkflowTaskSummary
from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkflowOutput")


@attr.s(auto_attribs=True, repr=False)
class WorkflowOutput:
    """  """

    _archive_record: Union[Unset, None, ArchiveRecord] = UNSET
    _created_at: Union[Unset, str] = UNSET
    _creation_origin: Union[Unset, CreationOrigin] = UNSET
    _fields: Union[Unset, Fields] = UNSET
    _modified_at: Union[Unset, str] = UNSET
    _next_outputs: Union[Unset, List[WorkflowOutputSummary]] = UNSET
    _next_tasks: Union[Unset, List[WorkflowTaskSummary]] = UNSET
    _source_outputs: Union[Unset, List[WorkflowOutputSummary]] = UNSET
    _source_tasks: Union[Unset, List[WorkflowTaskSummary]] = UNSET
    _web_url: Union[Unset, str] = UNSET
    _workflow_task: Union[Unset, WorkflowTaskSummary] = UNSET
    _workflow_task_group: Union[Unset, WorkflowTaskGroupSummary] = UNSET
    _display_id: Union[Unset, str] = UNSET
    _id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("archive_record={}".format(repr(self._archive_record)))
        fields.append("created_at={}".format(repr(self._created_at)))
        fields.append("creation_origin={}".format(repr(self._creation_origin)))
        fields.append("fields={}".format(repr(self._fields)))
        fields.append("modified_at={}".format(repr(self._modified_at)))
        fields.append("next_outputs={}".format(repr(self._next_outputs)))
        fields.append("next_tasks={}".format(repr(self._next_tasks)))
        fields.append("source_outputs={}".format(repr(self._source_outputs)))
        fields.append("source_tasks={}".format(repr(self._source_tasks)))
        fields.append("web_url={}".format(repr(self._web_url)))
        fields.append("workflow_task={}".format(repr(self._workflow_task)))
        fields.append("workflow_task_group={}".format(repr(self._workflow_task_group)))
        fields.append("display_id={}".format(repr(self._display_id)))
        fields.append("id={}".format(repr(self._id)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "WorkflowOutput({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        archive_record: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self._archive_record, Unset):
            archive_record = self._archive_record.to_dict() if self._archive_record else None

        created_at = self._created_at
        creation_origin: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._creation_origin, Unset):
            creation_origin = self._creation_origin.to_dict()

        fields: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._fields, Unset):
            fields = self._fields.to_dict()

        modified_at = self._modified_at
        next_outputs: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._next_outputs, Unset):
            next_outputs = []
            for next_outputs_item_data in self._next_outputs:
                next_outputs_item = next_outputs_item_data.to_dict()

                next_outputs.append(next_outputs_item)

        next_tasks: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._next_tasks, Unset):
            next_tasks = []
            for next_tasks_item_data in self._next_tasks:
                next_tasks_item = next_tasks_item_data.to_dict()

                next_tasks.append(next_tasks_item)

        source_outputs: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._source_outputs, Unset):
            source_outputs = []
            for source_outputs_item_data in self._source_outputs:
                source_outputs_item = source_outputs_item_data.to_dict()

                source_outputs.append(source_outputs_item)

        source_tasks: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._source_tasks, Unset):
            source_tasks = []
            for source_tasks_item_data in self._source_tasks:
                source_tasks_item = source_tasks_item_data.to_dict()

                source_tasks.append(source_tasks_item)

        web_url = self._web_url
        workflow_task: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._workflow_task, Unset):
            workflow_task = self._workflow_task.to_dict()

        workflow_task_group: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._workflow_task_group, Unset):
            workflow_task_group = self._workflow_task_group.to_dict()

        display_id = self._display_id
        id = self._id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if archive_record is not UNSET:
            field_dict["archiveRecord"] = archive_record
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if creation_origin is not UNSET:
            field_dict["creationOrigin"] = creation_origin
        if fields is not UNSET:
            field_dict["fields"] = fields
        if modified_at is not UNSET:
            field_dict["modifiedAt"] = modified_at
        if next_outputs is not UNSET:
            field_dict["nextOutputs"] = next_outputs
        if next_tasks is not UNSET:
            field_dict["nextTasks"] = next_tasks
        if source_outputs is not UNSET:
            field_dict["sourceOutputs"] = source_outputs
        if source_tasks is not UNSET:
            field_dict["sourceTasks"] = source_tasks
        if web_url is not UNSET:
            field_dict["webURL"] = web_url
        if workflow_task is not UNSET:
            field_dict["workflowTask"] = workflow_task
        if workflow_task_group is not UNSET:
            field_dict["workflowTaskGroup"] = workflow_task_group
        if display_id is not UNSET:
            field_dict["displayId"] = display_id
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_archive_record() -> Union[Unset, None, ArchiveRecord]:
            archive_record = None
            _archive_record = d.pop("archiveRecord")

            if _archive_record is not None and not isinstance(_archive_record, Unset):
                archive_record = ArchiveRecord.from_dict(_archive_record)

            return archive_record

        try:
            archive_record = get_archive_record()
        except KeyError:
            if strict:
                raise
            archive_record = cast(Union[Unset, None, ArchiveRecord], UNSET)

        def get_created_at() -> Union[Unset, str]:
            created_at = d.pop("createdAt")
            return created_at

        try:
            created_at = get_created_at()
        except KeyError:
            if strict:
                raise
            created_at = cast(Union[Unset, str], UNSET)

        def get_creation_origin() -> Union[Unset, CreationOrigin]:
            creation_origin: Union[Unset, Union[Unset, CreationOrigin]] = UNSET
            _creation_origin = d.pop("creationOrigin")

            if not isinstance(_creation_origin, Unset):
                creation_origin = CreationOrigin.from_dict(_creation_origin)

            return creation_origin

        try:
            creation_origin = get_creation_origin()
        except KeyError:
            if strict:
                raise
            creation_origin = cast(Union[Unset, CreationOrigin], UNSET)

        def get_fields() -> Union[Unset, Fields]:
            fields: Union[Unset, Union[Unset, Fields]] = UNSET
            _fields = d.pop("fields")

            if not isinstance(_fields, Unset):
                fields = Fields.from_dict(_fields)

            return fields

        try:
            fields = get_fields()
        except KeyError:
            if strict:
                raise
            fields = cast(Union[Unset, Fields], UNSET)

        def get_modified_at() -> Union[Unset, str]:
            modified_at = d.pop("modifiedAt")
            return modified_at

        try:
            modified_at = get_modified_at()
        except KeyError:
            if strict:
                raise
            modified_at = cast(Union[Unset, str], UNSET)

        def get_next_outputs() -> Union[Unset, List[WorkflowOutputSummary]]:
            next_outputs = []
            _next_outputs = d.pop("nextOutputs")
            for next_outputs_item_data in _next_outputs or []:
                next_outputs_item = WorkflowOutputSummary.from_dict(next_outputs_item_data, strict=False)

                next_outputs.append(next_outputs_item)

            return next_outputs

        try:
            next_outputs = get_next_outputs()
        except KeyError:
            if strict:
                raise
            next_outputs = cast(Union[Unset, List[WorkflowOutputSummary]], UNSET)

        def get_next_tasks() -> Union[Unset, List[WorkflowTaskSummary]]:
            next_tasks = []
            _next_tasks = d.pop("nextTasks")
            for next_tasks_item_data in _next_tasks or []:
                next_tasks_item = WorkflowTaskSummary.from_dict(next_tasks_item_data, strict=False)

                next_tasks.append(next_tasks_item)

            return next_tasks

        try:
            next_tasks = get_next_tasks()
        except KeyError:
            if strict:
                raise
            next_tasks = cast(Union[Unset, List[WorkflowTaskSummary]], UNSET)

        def get_source_outputs() -> Union[Unset, List[WorkflowOutputSummary]]:
            source_outputs = []
            _source_outputs = d.pop("sourceOutputs")
            for source_outputs_item_data in _source_outputs or []:
                source_outputs_item = WorkflowOutputSummary.from_dict(source_outputs_item_data, strict=False)

                source_outputs.append(source_outputs_item)

            return source_outputs

        try:
            source_outputs = get_source_outputs()
        except KeyError:
            if strict:
                raise
            source_outputs = cast(Union[Unset, List[WorkflowOutputSummary]], UNSET)

        def get_source_tasks() -> Union[Unset, List[WorkflowTaskSummary]]:
            source_tasks = []
            _source_tasks = d.pop("sourceTasks")
            for source_tasks_item_data in _source_tasks or []:
                source_tasks_item = WorkflowTaskSummary.from_dict(source_tasks_item_data, strict=False)

                source_tasks.append(source_tasks_item)

            return source_tasks

        try:
            source_tasks = get_source_tasks()
        except KeyError:
            if strict:
                raise
            source_tasks = cast(Union[Unset, List[WorkflowTaskSummary]], UNSET)

        def get_web_url() -> Union[Unset, str]:
            web_url = d.pop("webURL")
            return web_url

        try:
            web_url = get_web_url()
        except KeyError:
            if strict:
                raise
            web_url = cast(Union[Unset, str], UNSET)

        def get_workflow_task() -> Union[Unset, WorkflowTaskSummary]:
            workflow_task: Union[Unset, Union[Unset, WorkflowTaskSummary]] = UNSET
            _workflow_task = d.pop("workflowTask")

            if not isinstance(_workflow_task, Unset):
                workflow_task = WorkflowTaskSummary.from_dict(_workflow_task)

            return workflow_task

        try:
            workflow_task = get_workflow_task()
        except KeyError:
            if strict:
                raise
            workflow_task = cast(Union[Unset, WorkflowTaskSummary], UNSET)

        def get_workflow_task_group() -> Union[Unset, WorkflowTaskGroupSummary]:
            workflow_task_group: Union[Unset, Union[Unset, WorkflowTaskGroupSummary]] = UNSET
            _workflow_task_group = d.pop("workflowTaskGroup")

            if not isinstance(_workflow_task_group, Unset):
                workflow_task_group = WorkflowTaskGroupSummary.from_dict(_workflow_task_group)

            return workflow_task_group

        try:
            workflow_task_group = get_workflow_task_group()
        except KeyError:
            if strict:
                raise
            workflow_task_group = cast(Union[Unset, WorkflowTaskGroupSummary], UNSET)

        def get_display_id() -> Union[Unset, str]:
            display_id = d.pop("displayId")
            return display_id

        try:
            display_id = get_display_id()
        except KeyError:
            if strict:
                raise
            display_id = cast(Union[Unset, str], UNSET)

        def get_id() -> Union[Unset, str]:
            id = d.pop("id")
            return id

        try:
            id = get_id()
        except KeyError:
            if strict:
                raise
            id = cast(Union[Unset, str], UNSET)

        workflow_output = cls(
            archive_record=archive_record,
            created_at=created_at,
            creation_origin=creation_origin,
            fields=fields,
            modified_at=modified_at,
            next_outputs=next_outputs,
            next_tasks=next_tasks,
            source_outputs=source_outputs,
            source_tasks=source_tasks,
            web_url=web_url,
            workflow_task=workflow_task,
            workflow_task_group=workflow_task_group,
            display_id=display_id,
            id=id,
        )

        workflow_output.additional_properties = d
        return workflow_output

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
    def archive_record(self) -> Optional[ArchiveRecord]:
        if isinstance(self._archive_record, Unset):
            raise NotPresentError(self, "archive_record")
        return self._archive_record

    @archive_record.setter
    def archive_record(self, value: Optional[ArchiveRecord]) -> None:
        self._archive_record = value

    @archive_record.deleter
    def archive_record(self) -> None:
        self._archive_record = UNSET

    @property
    def created_at(self) -> str:
        """ The ISO formatted date and time that the task was created """
        if isinstance(self._created_at, Unset):
            raise NotPresentError(self, "created_at")
        return self._created_at

    @created_at.setter
    def created_at(self, value: str) -> None:
        self._created_at = value

    @created_at.deleter
    def created_at(self) -> None:
        self._created_at = UNSET

    @property
    def creation_origin(self) -> CreationOrigin:
        if isinstance(self._creation_origin, Unset):
            raise NotPresentError(self, "creation_origin")
        return self._creation_origin

    @creation_origin.setter
    def creation_origin(self, value: CreationOrigin) -> None:
        self._creation_origin = value

    @creation_origin.deleter
    def creation_origin(self) -> None:
        self._creation_origin = UNSET

    @property
    def fields(self) -> Fields:
        if isinstance(self._fields, Unset):
            raise NotPresentError(self, "fields")
        return self._fields

    @fields.setter
    def fields(self, value: Fields) -> None:
        self._fields = value

    @fields.deleter
    def fields(self) -> None:
        self._fields = UNSET

    @property
    def modified_at(self) -> str:
        """ The ISO formatted date and time that the task was last modified """
        if isinstance(self._modified_at, Unset):
            raise NotPresentError(self, "modified_at")
        return self._modified_at

    @modified_at.setter
    def modified_at(self, value: str) -> None:
        self._modified_at = value

    @modified_at.deleter
    def modified_at(self) -> None:
        self._modified_at = UNSET

    @property
    def next_outputs(self) -> List[WorkflowOutputSummary]:
        """ The outputs in the flowchart which are generated by this output. """
        if isinstance(self._next_outputs, Unset):
            raise NotPresentError(self, "next_outputs")
        return self._next_outputs

    @next_outputs.setter
    def next_outputs(self, value: List[WorkflowOutputSummary]) -> None:
        self._next_outputs = value

    @next_outputs.deleter
    def next_outputs(self) -> None:
        self._next_outputs = UNSET

    @property
    def next_tasks(self) -> List[WorkflowTaskSummary]:
        """ The downstream tasks in the flowchart which are generated by this output. """
        if isinstance(self._next_tasks, Unset):
            raise NotPresentError(self, "next_tasks")
        return self._next_tasks

    @next_tasks.setter
    def next_tasks(self, value: List[WorkflowTaskSummary]) -> None:
        self._next_tasks = value

    @next_tasks.deleter
    def next_tasks(self) -> None:
        self._next_tasks = UNSET

    @property
    def source_outputs(self) -> List[WorkflowOutputSummary]:
        """ The outputs in the flowchart which were used to generate this output. """
        if isinstance(self._source_outputs, Unset):
            raise NotPresentError(self, "source_outputs")
        return self._source_outputs

    @source_outputs.setter
    def source_outputs(self, value: List[WorkflowOutputSummary]) -> None:
        self._source_outputs = value

    @source_outputs.deleter
    def source_outputs(self) -> None:
        self._source_outputs = UNSET

    @property
    def source_tasks(self) -> List[WorkflowTaskSummary]:
        """ The tasks in the flowchart which were used to generate this output. """
        if isinstance(self._source_tasks, Unset):
            raise NotPresentError(self, "source_tasks")
        return self._source_tasks

    @source_tasks.setter
    def source_tasks(self, value: List[WorkflowTaskSummary]) -> None:
        self._source_tasks = value

    @source_tasks.deleter
    def source_tasks(self) -> None:
        self._source_tasks = UNSET

    @property
    def web_url(self) -> str:
        """ URL of the workflow output """
        if isinstance(self._web_url, Unset):
            raise NotPresentError(self, "web_url")
        return self._web_url

    @web_url.setter
    def web_url(self, value: str) -> None:
        self._web_url = value

    @web_url.deleter
    def web_url(self) -> None:
        self._web_url = UNSET

    @property
    def workflow_task(self) -> WorkflowTaskSummary:
        if isinstance(self._workflow_task, Unset):
            raise NotPresentError(self, "workflow_task")
        return self._workflow_task

    @workflow_task.setter
    def workflow_task(self, value: WorkflowTaskSummary) -> None:
        self._workflow_task = value

    @workflow_task.deleter
    def workflow_task(self) -> None:
        self._workflow_task = UNSET

    @property
    def workflow_task_group(self) -> WorkflowTaskGroupSummary:
        if isinstance(self._workflow_task_group, Unset):
            raise NotPresentError(self, "workflow_task_group")
        return self._workflow_task_group

    @workflow_task_group.setter
    def workflow_task_group(self, value: WorkflowTaskGroupSummary) -> None:
        self._workflow_task_group = value

    @workflow_task_group.deleter
    def workflow_task_group(self) -> None:
        self._workflow_task_group = UNSET

    @property
    def display_id(self) -> str:
        """ User-friendly ID of the workflow task group """
        if isinstance(self._display_id, Unset):
            raise NotPresentError(self, "display_id")
        return self._display_id

    @display_id.setter
    def display_id(self, value: str) -> None:
        self._display_id = value

    @display_id.deleter
    def display_id(self) -> None:
        self._display_id = UNSET

    @property
    def id(self) -> str:
        """ The ID of the workflow output """
        if isinstance(self._id, Unset):
            raise NotPresentError(self, "id")
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        self._id = value

    @id.deleter
    def id(self) -> None:
        self._id = UNSET
