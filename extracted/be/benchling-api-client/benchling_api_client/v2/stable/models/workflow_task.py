import datetime
from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..extensions import NotPresentError
from ..models.archive_record import ArchiveRecord
from ..models.creation_origin import CreationOrigin
from ..models.fields import Fields
from ..models.party_summary import PartySummary
from ..models.user_summary import UserSummary
from ..models.workflow_output_summary import WorkflowOutputSummary
from ..models.workflow_task_execution_origin import WorkflowTaskExecutionOrigin
from ..models.workflow_task_execution_type import WorkflowTaskExecutionType
from ..models.workflow_task_group_summary import WorkflowTaskGroupSummary
from ..models.workflow_task_schema_summary import WorkflowTaskSchemaSummary
from ..models.workflow_task_status import WorkflowTaskStatus
from ..models.workflow_task_summary import WorkflowTaskSummary
from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkflowTask")


@attr.s(auto_attribs=True, repr=False)
class WorkflowTask:
    """  """

    _execution_flowchart_id: Union[Unset, str] = UNSET
    _execution_type: Union[Unset, WorkflowTaskExecutionType] = UNSET
    _next_outputs: Union[Unset, List[WorkflowOutputSummary]] = UNSET
    _next_tasks: Union[Unset, List[WorkflowTaskSummary]] = UNSET
    _responsible_parties: Union[Unset, List[PartySummary]] = UNSET
    _root_task: Union[Unset, WorkflowTaskSummary] = UNSET
    _source_outputs: Union[Unset, List[WorkflowOutputSummary]] = UNSET
    _source_tasks: Union[Unset, List[WorkflowTaskSummary]] = UNSET
    _workflow_outputs: Union[Unset, List[WorkflowOutputSummary]] = UNSET
    _archive_record: Union[Unset, None, ArchiveRecord] = UNSET
    _assignee: Union[Unset, None, UserSummary] = UNSET
    _cloned_from: Union[Unset, None, WorkflowTaskSummary] = UNSET
    _created_at: Union[Unset, str] = UNSET
    _creation_origin: Union[Unset, CreationOrigin] = UNSET
    _creator: Union[Unset, UserSummary] = UNSET
    _execution_origin: Union[Unset, None, WorkflowTaskExecutionOrigin] = UNSET
    _fields: Union[Unset, Fields] = UNSET
    _modified_at: Union[Unset, str] = UNSET
    _outputs: Union[Unset, List[WorkflowOutputSummary]] = UNSET
    _scheduled_on: Union[Unset, None, datetime.date] = UNSET
    _schema: Union[Unset, WorkflowTaskSchemaSummary] = UNSET
    _status: Union[Unset, WorkflowTaskStatus] = UNSET
    _web_url: Union[Unset, str] = UNSET
    _workflow_task_group: Union[Unset, WorkflowTaskGroupSummary] = UNSET
    _display_id: Union[Unset, str] = UNSET
    _id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("execution_flowchart_id={}".format(repr(self._execution_flowchart_id)))
        fields.append("execution_type={}".format(repr(self._execution_type)))
        fields.append("next_outputs={}".format(repr(self._next_outputs)))
        fields.append("next_tasks={}".format(repr(self._next_tasks)))
        fields.append("responsible_parties={}".format(repr(self._responsible_parties)))
        fields.append("root_task={}".format(repr(self._root_task)))
        fields.append("source_outputs={}".format(repr(self._source_outputs)))
        fields.append("source_tasks={}".format(repr(self._source_tasks)))
        fields.append("workflow_outputs={}".format(repr(self._workflow_outputs)))
        fields.append("archive_record={}".format(repr(self._archive_record)))
        fields.append("assignee={}".format(repr(self._assignee)))
        fields.append("cloned_from={}".format(repr(self._cloned_from)))
        fields.append("created_at={}".format(repr(self._created_at)))
        fields.append("creation_origin={}".format(repr(self._creation_origin)))
        fields.append("creator={}".format(repr(self._creator)))
        fields.append("execution_origin={}".format(repr(self._execution_origin)))
        fields.append("fields={}".format(repr(self._fields)))
        fields.append("modified_at={}".format(repr(self._modified_at)))
        fields.append("outputs={}".format(repr(self._outputs)))
        fields.append("scheduled_on={}".format(repr(self._scheduled_on)))
        fields.append("schema={}".format(repr(self._schema)))
        fields.append("status={}".format(repr(self._status)))
        fields.append("web_url={}".format(repr(self._web_url)))
        fields.append("workflow_task_group={}".format(repr(self._workflow_task_group)))
        fields.append("display_id={}".format(repr(self._display_id)))
        fields.append("id={}".format(repr(self._id)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "WorkflowTask({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        execution_flowchart_id = self._execution_flowchart_id
        execution_type: Union[Unset, int] = UNSET
        if not isinstance(self._execution_type, Unset):
            execution_type = self._execution_type.value

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

        responsible_parties: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._responsible_parties, Unset):
            responsible_parties = []
            for responsible_parties_item_data in self._responsible_parties:
                responsible_parties_item = responsible_parties_item_data.to_dict()

                responsible_parties.append(responsible_parties_item)

        root_task: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._root_task, Unset):
            root_task = self._root_task.to_dict()

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

        workflow_outputs: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._workflow_outputs, Unset):
            workflow_outputs = []
            for workflow_outputs_item_data in self._workflow_outputs:
                workflow_outputs_item = workflow_outputs_item_data.to_dict()

                workflow_outputs.append(workflow_outputs_item)

        archive_record: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self._archive_record, Unset):
            archive_record = self._archive_record.to_dict() if self._archive_record else None

        assignee: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self._assignee, Unset):
            assignee = self._assignee.to_dict() if self._assignee else None

        cloned_from: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self._cloned_from, Unset):
            cloned_from = self._cloned_from.to_dict() if self._cloned_from else None

        created_at = self._created_at
        creation_origin: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._creation_origin, Unset):
            creation_origin = self._creation_origin.to_dict()

        creator: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._creator, Unset):
            creator = self._creator.to_dict()

        execution_origin: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self._execution_origin, Unset):
            execution_origin = self._execution_origin.to_dict() if self._execution_origin else None

        fields: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._fields, Unset):
            fields = self._fields.to_dict()

        modified_at = self._modified_at
        outputs: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._outputs, Unset):
            outputs = []
            for outputs_item_data in self._outputs:
                outputs_item = outputs_item_data.to_dict()

                outputs.append(outputs_item)

        scheduled_on: Union[Unset, None, str] = UNSET
        if not isinstance(self._scheduled_on, Unset):
            scheduled_on = self._scheduled_on.isoformat() if self._scheduled_on else None

        schema: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._schema, Unset):
            schema = self._schema.to_dict()

        status: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._status, Unset):
            status = self._status.to_dict()

        web_url = self._web_url
        workflow_task_group: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._workflow_task_group, Unset):
            workflow_task_group = self._workflow_task_group.to_dict()

        display_id = self._display_id
        id = self._id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if execution_flowchart_id is not UNSET:
            field_dict["executionFlowchartId"] = execution_flowchart_id
        if execution_type is not UNSET:
            field_dict["executionType"] = execution_type
        if next_outputs is not UNSET:
            field_dict["nextOutputs"] = next_outputs
        if next_tasks is not UNSET:
            field_dict["nextTasks"] = next_tasks
        if responsible_parties is not UNSET:
            field_dict["responsibleParties"] = responsible_parties
        if root_task is not UNSET:
            field_dict["rootTask"] = root_task
        if source_outputs is not UNSET:
            field_dict["sourceOutputs"] = source_outputs
        if source_tasks is not UNSET:
            field_dict["sourceTasks"] = source_tasks
        if workflow_outputs is not UNSET:
            field_dict["workflowOutputs"] = workflow_outputs
        if archive_record is not UNSET:
            field_dict["archiveRecord"] = archive_record
        if assignee is not UNSET:
            field_dict["assignee"] = assignee
        if cloned_from is not UNSET:
            field_dict["clonedFrom"] = cloned_from
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if creation_origin is not UNSET:
            field_dict["creationOrigin"] = creation_origin
        if creator is not UNSET:
            field_dict["creator"] = creator
        if execution_origin is not UNSET:
            field_dict["executionOrigin"] = execution_origin
        if fields is not UNSET:
            field_dict["fields"] = fields
        if modified_at is not UNSET:
            field_dict["modifiedAt"] = modified_at
        if outputs is not UNSET:
            field_dict["outputs"] = outputs
        if scheduled_on is not UNSET:
            field_dict["scheduledOn"] = scheduled_on
        if schema is not UNSET:
            field_dict["schema"] = schema
        if status is not UNSET:
            field_dict["status"] = status
        if web_url is not UNSET:
            field_dict["webURL"] = web_url
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

        def get_execution_flowchart_id() -> Union[Unset, str]:
            execution_flowchart_id = d.pop("executionFlowchartId")
            return execution_flowchart_id

        try:
            execution_flowchart_id = get_execution_flowchart_id()
        except KeyError:
            if strict:
                raise
            execution_flowchart_id = cast(Union[Unset, str], UNSET)

        def get_execution_type() -> Union[Unset, WorkflowTaskExecutionType]:
            execution_type = UNSET
            _execution_type = d.pop("executionType")
            if _execution_type is not None and _execution_type is not UNSET:
                try:
                    execution_type = WorkflowTaskExecutionType(_execution_type)
                except ValueError:
                    execution_type = WorkflowTaskExecutionType.of_unknown(_execution_type)

            return execution_type

        try:
            execution_type = get_execution_type()
        except KeyError:
            if strict:
                raise
            execution_type = cast(Union[Unset, WorkflowTaskExecutionType], UNSET)

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

        def get_responsible_parties() -> Union[Unset, List[PartySummary]]:
            responsible_parties = []
            _responsible_parties = d.pop("responsibleParties")
            for responsible_parties_item_data in _responsible_parties or []:
                responsible_parties_item = PartySummary.from_dict(responsible_parties_item_data, strict=False)

                responsible_parties.append(responsible_parties_item)

            return responsible_parties

        try:
            responsible_parties = get_responsible_parties()
        except KeyError:
            if strict:
                raise
            responsible_parties = cast(Union[Unset, List[PartySummary]], UNSET)

        def get_root_task() -> Union[Unset, WorkflowTaskSummary]:
            root_task: Union[Unset, Union[Unset, WorkflowTaskSummary]] = UNSET
            _root_task = d.pop("rootTask")

            if not isinstance(_root_task, Unset):
                root_task = WorkflowTaskSummary.from_dict(_root_task)

            return root_task

        try:
            root_task = get_root_task()
        except KeyError:
            if strict:
                raise
            root_task = cast(Union[Unset, WorkflowTaskSummary], UNSET)

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

        def get_workflow_outputs() -> Union[Unset, List[WorkflowOutputSummary]]:
            workflow_outputs = []
            _workflow_outputs = d.pop("workflowOutputs")
            for workflow_outputs_item_data in _workflow_outputs or []:
                workflow_outputs_item = WorkflowOutputSummary.from_dict(
                    workflow_outputs_item_data, strict=False
                )

                workflow_outputs.append(workflow_outputs_item)

            return workflow_outputs

        try:
            workflow_outputs = get_workflow_outputs()
        except KeyError:
            if strict:
                raise
            workflow_outputs = cast(Union[Unset, List[WorkflowOutputSummary]], UNSET)

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

        def get_assignee() -> Union[Unset, None, UserSummary]:
            assignee = None
            _assignee = d.pop("assignee")

            if _assignee is not None and not isinstance(_assignee, Unset):
                assignee = UserSummary.from_dict(_assignee)

            return assignee

        try:
            assignee = get_assignee()
        except KeyError:
            if strict:
                raise
            assignee = cast(Union[Unset, None, UserSummary], UNSET)

        def get_cloned_from() -> Union[Unset, None, WorkflowTaskSummary]:
            cloned_from = None
            _cloned_from = d.pop("clonedFrom")

            if _cloned_from is not None and not isinstance(_cloned_from, Unset):
                cloned_from = WorkflowTaskSummary.from_dict(_cloned_from)

            return cloned_from

        try:
            cloned_from = get_cloned_from()
        except KeyError:
            if strict:
                raise
            cloned_from = cast(Union[Unset, None, WorkflowTaskSummary], UNSET)

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

        def get_creator() -> Union[Unset, UserSummary]:
            creator: Union[Unset, Union[Unset, UserSummary]] = UNSET
            _creator = d.pop("creator")

            if not isinstance(_creator, Unset):
                creator = UserSummary.from_dict(_creator)

            return creator

        try:
            creator = get_creator()
        except KeyError:
            if strict:
                raise
            creator = cast(Union[Unset, UserSummary], UNSET)

        def get_execution_origin() -> Union[Unset, None, WorkflowTaskExecutionOrigin]:
            execution_origin = None
            _execution_origin = d.pop("executionOrigin")

            if _execution_origin is not None and not isinstance(_execution_origin, Unset):
                execution_origin = WorkflowTaskExecutionOrigin.from_dict(_execution_origin)

            return execution_origin

        try:
            execution_origin = get_execution_origin()
        except KeyError:
            if strict:
                raise
            execution_origin = cast(Union[Unset, None, WorkflowTaskExecutionOrigin], UNSET)

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

        def get_outputs() -> Union[Unset, List[WorkflowOutputSummary]]:
            outputs = []
            _outputs = d.pop("outputs")
            for outputs_item_data in _outputs or []:
                outputs_item = WorkflowOutputSummary.from_dict(outputs_item_data, strict=False)

                outputs.append(outputs_item)

            return outputs

        try:
            outputs = get_outputs()
        except KeyError:
            if strict:
                raise
            outputs = cast(Union[Unset, List[WorkflowOutputSummary]], UNSET)

        def get_scheduled_on() -> Union[Unset, None, datetime.date]:
            scheduled_on: Union[Unset, None, datetime.date] = UNSET
            _scheduled_on = d.pop("scheduledOn")
            if _scheduled_on is not None and not isinstance(_scheduled_on, Unset):
                scheduled_on = isoparse(cast(str, _scheduled_on)).date()

            return scheduled_on

        try:
            scheduled_on = get_scheduled_on()
        except KeyError:
            if strict:
                raise
            scheduled_on = cast(Union[Unset, None, datetime.date], UNSET)

        def get_schema() -> Union[Unset, WorkflowTaskSchemaSummary]:
            schema: Union[Unset, Union[Unset, WorkflowTaskSchemaSummary]] = UNSET
            _schema = d.pop("schema")

            if not isinstance(_schema, Unset):
                schema = WorkflowTaskSchemaSummary.from_dict(_schema)

            return schema

        try:
            schema = get_schema()
        except KeyError:
            if strict:
                raise
            schema = cast(Union[Unset, WorkflowTaskSchemaSummary], UNSET)

        def get_status() -> Union[Unset, WorkflowTaskStatus]:
            status: Union[Unset, Union[Unset, WorkflowTaskStatus]] = UNSET
            _status = d.pop("status")

            if not isinstance(_status, Unset):
                status = WorkflowTaskStatus.from_dict(_status)

            return status

        try:
            status = get_status()
        except KeyError:
            if strict:
                raise
            status = cast(Union[Unset, WorkflowTaskStatus], UNSET)

        def get_web_url() -> Union[Unset, str]:
            web_url = d.pop("webURL")
            return web_url

        try:
            web_url = get_web_url()
        except KeyError:
            if strict:
                raise
            web_url = cast(Union[Unset, str], UNSET)

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

        workflow_task = cls(
            execution_flowchart_id=execution_flowchart_id,
            execution_type=execution_type,
            next_outputs=next_outputs,
            next_tasks=next_tasks,
            responsible_parties=responsible_parties,
            root_task=root_task,
            source_outputs=source_outputs,
            source_tasks=source_tasks,
            workflow_outputs=workflow_outputs,
            archive_record=archive_record,
            assignee=assignee,
            cloned_from=cloned_from,
            created_at=created_at,
            creation_origin=creation_origin,
            creator=creator,
            execution_origin=execution_origin,
            fields=fields,
            modified_at=modified_at,
            outputs=outputs,
            scheduled_on=scheduled_on,
            schema=schema,
            status=status,
            web_url=web_url,
            workflow_task_group=workflow_task_group,
            display_id=display_id,
            id=id,
        )

        workflow_task.additional_properties = d
        return workflow_task

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
    def execution_flowchart_id(self) -> str:
        """ The ID of the flowchart that this task will execute. This will only be defined if the task has exectutionType FLOWCHART """
        if isinstance(self._execution_flowchart_id, Unset):
            raise NotPresentError(self, "execution_flowchart_id")
        return self._execution_flowchart_id

    @execution_flowchart_id.setter
    def execution_flowchart_id(self, value: str) -> None:
        self._execution_flowchart_id = value

    @execution_flowchart_id.deleter
    def execution_flowchart_id(self) -> None:
        self._execution_flowchart_id = UNSET

    @property
    def execution_type(self) -> WorkflowTaskExecutionType:
        """ The method by which the task of the workflow is executed """
        if isinstance(self._execution_type, Unset):
            raise NotPresentError(self, "execution_type")
        return self._execution_type

    @execution_type.setter
    def execution_type(self, value: WorkflowTaskExecutionType) -> None:
        self._execution_type = value

    @execution_type.deleter
    def execution_type(self) -> None:
        self._execution_type = UNSET

    @property
    def next_outputs(self) -> List[WorkflowOutputSummary]:
        """ The outputs in the flowchart which are generated by this task. """
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
        """ The downstream tasks in the flowchart which are generated by this task. """
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
    def responsible_parties(self) -> List[PartySummary]:
        """ List of users and teams that are responsible for this task """
        if isinstance(self._responsible_parties, Unset):
            raise NotPresentError(self, "responsible_parties")
        return self._responsible_parties

    @responsible_parties.setter
    def responsible_parties(self, value: List[PartySummary]) -> None:
        self._responsible_parties = value

    @responsible_parties.deleter
    def responsible_parties(self) -> None:
        self._responsible_parties = UNSET

    @property
    def root_task(self) -> WorkflowTaskSummary:
        if isinstance(self._root_task, Unset):
            raise NotPresentError(self, "root_task")
        return self._root_task

    @root_task.setter
    def root_task(self, value: WorkflowTaskSummary) -> None:
        self._root_task = value

    @root_task.deleter
    def root_task(self) -> None:
        self._root_task = UNSET

    @property
    def source_outputs(self) -> List[WorkflowOutputSummary]:
        """ The parent outputs in the flowchart which were used to generate this task. """
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
        """ The parent tasks in the flowchart which were used to generate this task. """
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
    def workflow_outputs(self) -> List[WorkflowOutputSummary]:
        """ The outputs of the workflow task group """
        if isinstance(self._workflow_outputs, Unset):
            raise NotPresentError(self, "workflow_outputs")
        return self._workflow_outputs

    @workflow_outputs.setter
    def workflow_outputs(self, value: List[WorkflowOutputSummary]) -> None:
        self._workflow_outputs = value

    @workflow_outputs.deleter
    def workflow_outputs(self) -> None:
        self._workflow_outputs = UNSET

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
    def assignee(self) -> Optional[UserSummary]:
        if isinstance(self._assignee, Unset):
            raise NotPresentError(self, "assignee")
        return self._assignee

    @assignee.setter
    def assignee(self, value: Optional[UserSummary]) -> None:
        self._assignee = value

    @assignee.deleter
    def assignee(self) -> None:
        self._assignee = UNSET

    @property
    def cloned_from(self) -> Optional[WorkflowTaskSummary]:
        if isinstance(self._cloned_from, Unset):
            raise NotPresentError(self, "cloned_from")
        return self._cloned_from

    @cloned_from.setter
    def cloned_from(self, value: Optional[WorkflowTaskSummary]) -> None:
        self._cloned_from = value

    @cloned_from.deleter
    def cloned_from(self) -> None:
        self._cloned_from = UNSET

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
    def creator(self) -> UserSummary:
        if isinstance(self._creator, Unset):
            raise NotPresentError(self, "creator")
        return self._creator

    @creator.setter
    def creator(self, value: UserSummary) -> None:
        self._creator = value

    @creator.deleter
    def creator(self) -> None:
        self._creator = UNSET

    @property
    def execution_origin(self) -> Optional[WorkflowTaskExecutionOrigin]:
        """ The context into which a task was executed """
        if isinstance(self._execution_origin, Unset):
            raise NotPresentError(self, "execution_origin")
        return self._execution_origin

    @execution_origin.setter
    def execution_origin(self, value: Optional[WorkflowTaskExecutionOrigin]) -> None:
        self._execution_origin = value

    @execution_origin.deleter
    def execution_origin(self) -> None:
        self._execution_origin = UNSET

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
    def outputs(self) -> List[WorkflowOutputSummary]:
        if isinstance(self._outputs, Unset):
            raise NotPresentError(self, "outputs")
        return self._outputs

    @outputs.setter
    def outputs(self, value: List[WorkflowOutputSummary]) -> None:
        self._outputs = value

    @outputs.deleter
    def outputs(self) -> None:
        self._outputs = UNSET

    @property
    def scheduled_on(self) -> Optional[datetime.date]:
        """ The date on which the task is scheduled to be executed """
        if isinstance(self._scheduled_on, Unset):
            raise NotPresentError(self, "scheduled_on")
        return self._scheduled_on

    @scheduled_on.setter
    def scheduled_on(self, value: Optional[datetime.date]) -> None:
        self._scheduled_on = value

    @scheduled_on.deleter
    def scheduled_on(self) -> None:
        self._scheduled_on = UNSET

    @property
    def schema(self) -> WorkflowTaskSchemaSummary:
        if isinstance(self._schema, Unset):
            raise NotPresentError(self, "schema")
        return self._schema

    @schema.setter
    def schema(self, value: WorkflowTaskSchemaSummary) -> None:
        self._schema = value

    @schema.deleter
    def schema(self) -> None:
        self._schema = UNSET

    @property
    def status(self) -> WorkflowTaskStatus:
        if isinstance(self._status, Unset):
            raise NotPresentError(self, "status")
        return self._status

    @status.setter
    def status(self, value: WorkflowTaskStatus) -> None:
        self._status = value

    @status.deleter
    def status(self) -> None:
        self._status = UNSET

    @property
    def web_url(self) -> str:
        """ URL of the workflow task """
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
        """ User-friendly ID of the workflow task """
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
        """ The ID of the workflow task """
        if isinstance(self._id, Unset):
            raise NotPresentError(self, "id")
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        self._id = value

    @id.deleter
    def id(self) -> None:
        self._id = UNSET
