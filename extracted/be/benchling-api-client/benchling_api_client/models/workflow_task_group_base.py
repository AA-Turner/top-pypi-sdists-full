from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.archive_record import ArchiveRecord
from ..models.creation_origin import CreationOrigin
from ..models.folder import Folder
from ..models.team_summary import TeamSummary
from ..models.user_summary import UserSummary
from ..models.workflow_output_summary import WorkflowOutputSummary
from ..models.workflow_task_schema_summary import WorkflowTaskSchemaSummary
from ..models.workflow_task_summary import WorkflowTaskSummary
from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkflowTaskGroupBase")


@attr.s(auto_attribs=True, repr=False)
class WorkflowTaskGroupBase:
    """  """

    _archive_record: Union[Unset, None, ArchiveRecord] = UNSET
    _created_at: Union[Unset, str] = UNSET
    _creation_origin: Union[Unset, CreationOrigin] = UNSET
    _creator: Union[Unset, UserSummary] = UNSET
    _folder: Union[Unset, Folder] = UNSET
    _modified_at: Union[Unset, str] = UNSET
    _outputs: Union[Unset, List[WorkflowOutputSummary]] = UNSET
    _responsible_team: Union[Unset, None, TeamSummary] = UNSET
    _watchers: Union[Unset, List[UserSummary]] = UNSET
    _web_url: Union[Unset, str] = UNSET
    _workflow_task_schema: Union[Unset, WorkflowTaskSchemaSummary] = UNSET
    _workflow_tasks: Union[Unset, List[WorkflowTaskSummary]] = UNSET
    _display_id: Union[Unset, str] = UNSET
    _id: Union[Unset, str] = UNSET
    _name: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("archive_record={}".format(repr(self._archive_record)))
        fields.append("created_at={}".format(repr(self._created_at)))
        fields.append("creation_origin={}".format(repr(self._creation_origin)))
        fields.append("creator={}".format(repr(self._creator)))
        fields.append("folder={}".format(repr(self._folder)))
        fields.append("modified_at={}".format(repr(self._modified_at)))
        fields.append("outputs={}".format(repr(self._outputs)))
        fields.append("responsible_team={}".format(repr(self._responsible_team)))
        fields.append("watchers={}".format(repr(self._watchers)))
        fields.append("web_url={}".format(repr(self._web_url)))
        fields.append("workflow_task_schema={}".format(repr(self._workflow_task_schema)))
        fields.append("workflow_tasks={}".format(repr(self._workflow_tasks)))
        fields.append("display_id={}".format(repr(self._display_id)))
        fields.append("id={}".format(repr(self._id)))
        fields.append("name={}".format(repr(self._name)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "WorkflowTaskGroupBase({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        archive_record: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self._archive_record, Unset):
            archive_record = self._archive_record.to_dict() if self._archive_record else None

        created_at = self._created_at
        creation_origin: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._creation_origin, Unset):
            creation_origin = self._creation_origin.to_dict()

        creator: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._creator, Unset):
            creator = self._creator.to_dict()

        folder: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._folder, Unset):
            folder = self._folder.to_dict()

        modified_at = self._modified_at
        outputs: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._outputs, Unset):
            outputs = []
            for outputs_item_data in self._outputs:
                outputs_item = outputs_item_data.to_dict()

                outputs.append(outputs_item)

        responsible_team: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self._responsible_team, Unset):
            responsible_team = self._responsible_team.to_dict() if self._responsible_team else None

        watchers: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._watchers, Unset):
            watchers = []
            for watchers_item_data in self._watchers:
                watchers_item = watchers_item_data.to_dict()

                watchers.append(watchers_item)

        web_url = self._web_url
        workflow_task_schema: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._workflow_task_schema, Unset):
            workflow_task_schema = self._workflow_task_schema.to_dict()

        workflow_tasks: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._workflow_tasks, Unset):
            workflow_tasks = []
            for workflow_tasks_item_data in self._workflow_tasks:
                workflow_tasks_item = workflow_tasks_item_data.to_dict()

                workflow_tasks.append(workflow_tasks_item)

        display_id = self._display_id
        id = self._id
        name = self._name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if archive_record is not UNSET:
            field_dict["archiveRecord"] = archive_record
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if creation_origin is not UNSET:
            field_dict["creationOrigin"] = creation_origin
        if creator is not UNSET:
            field_dict["creator"] = creator
        if folder is not UNSET:
            field_dict["folder"] = folder
        if modified_at is not UNSET:
            field_dict["modifiedAt"] = modified_at
        if outputs is not UNSET:
            field_dict["outputs"] = outputs
        if responsible_team is not UNSET:
            field_dict["responsibleTeam"] = responsible_team
        if watchers is not UNSET:
            field_dict["watchers"] = watchers
        if web_url is not UNSET:
            field_dict["webURL"] = web_url
        if workflow_task_schema is not UNSET:
            field_dict["workflowTaskSchema"] = workflow_task_schema
        if workflow_tasks is not UNSET:
            field_dict["workflowTasks"] = workflow_tasks
        if display_id is not UNSET:
            field_dict["displayId"] = display_id
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name

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

        def get_folder() -> Union[Unset, Folder]:
            folder: Union[Unset, Union[Unset, Folder]] = UNSET
            _folder = d.pop("folder")

            if not isinstance(_folder, Unset):
                folder = Folder.from_dict(_folder)

            return folder

        try:
            folder = get_folder()
        except KeyError:
            if strict:
                raise
            folder = cast(Union[Unset, Folder], UNSET)

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

        def get_responsible_team() -> Union[Unset, None, TeamSummary]:
            responsible_team = None
            _responsible_team = d.pop("responsibleTeam")

            if _responsible_team is not None and not isinstance(_responsible_team, Unset):
                responsible_team = TeamSummary.from_dict(_responsible_team)

            return responsible_team

        try:
            responsible_team = get_responsible_team()
        except KeyError:
            if strict:
                raise
            responsible_team = cast(Union[Unset, None, TeamSummary], UNSET)

        def get_watchers() -> Union[Unset, List[UserSummary]]:
            watchers = []
            _watchers = d.pop("watchers")
            for watchers_item_data in _watchers or []:
                watchers_item = UserSummary.from_dict(watchers_item_data, strict=False)

                watchers.append(watchers_item)

            return watchers

        try:
            watchers = get_watchers()
        except KeyError:
            if strict:
                raise
            watchers = cast(Union[Unset, List[UserSummary]], UNSET)

        def get_web_url() -> Union[Unset, str]:
            web_url = d.pop("webURL")
            return web_url

        try:
            web_url = get_web_url()
        except KeyError:
            if strict:
                raise
            web_url = cast(Union[Unset, str], UNSET)

        def get_workflow_task_schema() -> Union[Unset, WorkflowTaskSchemaSummary]:
            workflow_task_schema: Union[Unset, Union[Unset, WorkflowTaskSchemaSummary]] = UNSET
            _workflow_task_schema = d.pop("workflowTaskSchema")

            if not isinstance(_workflow_task_schema, Unset):
                workflow_task_schema = WorkflowTaskSchemaSummary.from_dict(_workflow_task_schema)

            return workflow_task_schema

        try:
            workflow_task_schema = get_workflow_task_schema()
        except KeyError:
            if strict:
                raise
            workflow_task_schema = cast(Union[Unset, WorkflowTaskSchemaSummary], UNSET)

        def get_workflow_tasks() -> Union[Unset, List[WorkflowTaskSummary]]:
            workflow_tasks = []
            _workflow_tasks = d.pop("workflowTasks")
            for workflow_tasks_item_data in _workflow_tasks or []:
                workflow_tasks_item = WorkflowTaskSummary.from_dict(workflow_tasks_item_data, strict=False)

                workflow_tasks.append(workflow_tasks_item)

            return workflow_tasks

        try:
            workflow_tasks = get_workflow_tasks()
        except KeyError:
            if strict:
                raise
            workflow_tasks = cast(Union[Unset, List[WorkflowTaskSummary]], UNSET)

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

        def get_name() -> Union[Unset, str]:
            name = d.pop("name")
            return name

        try:
            name = get_name()
        except KeyError:
            if strict:
                raise
            name = cast(Union[Unset, str], UNSET)

        workflow_task_group_base = cls(
            archive_record=archive_record,
            created_at=created_at,
            creation_origin=creation_origin,
            creator=creator,
            folder=folder,
            modified_at=modified_at,
            outputs=outputs,
            responsible_team=responsible_team,
            watchers=watchers,
            web_url=web_url,
            workflow_task_schema=workflow_task_schema,
            workflow_tasks=workflow_tasks,
            display_id=display_id,
            id=id,
            name=name,
        )

        workflow_task_group_base.additional_properties = d
        return workflow_task_group_base

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
        """ The ISO formatted date and time that the task group was created """
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
    def folder(self) -> Folder:
        if isinstance(self._folder, Unset):
            raise NotPresentError(self, "folder")
        return self._folder

    @folder.setter
    def folder(self, value: Folder) -> None:
        self._folder = value

    @folder.deleter
    def folder(self) -> None:
        self._folder = UNSET

    @property
    def modified_at(self) -> str:
        """ The ISO formatted date and time that the task group was last modified """
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
        """ The outputs of the workflow task group """
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
    def responsible_team(self) -> Optional[TeamSummary]:
        if isinstance(self._responsible_team, Unset):
            raise NotPresentError(self, "responsible_team")
        return self._responsible_team

    @responsible_team.setter
    def responsible_team(self, value: Optional[TeamSummary]) -> None:
        self._responsible_team = value

    @responsible_team.deleter
    def responsible_team(self) -> None:
        self._responsible_team = UNSET

    @property
    def watchers(self) -> List[UserSummary]:
        """ The users watching the workflow task group """
        if isinstance(self._watchers, Unset):
            raise NotPresentError(self, "watchers")
        return self._watchers

    @watchers.setter
    def watchers(self, value: List[UserSummary]) -> None:
        self._watchers = value

    @watchers.deleter
    def watchers(self) -> None:
        self._watchers = UNSET

    @property
    def web_url(self) -> str:
        """ URL of the workflow task group """
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
    def workflow_task_schema(self) -> WorkflowTaskSchemaSummary:
        if isinstance(self._workflow_task_schema, Unset):
            raise NotPresentError(self, "workflow_task_schema")
        return self._workflow_task_schema

    @workflow_task_schema.setter
    def workflow_task_schema(self, value: WorkflowTaskSchemaSummary) -> None:
        self._workflow_task_schema = value

    @workflow_task_schema.deleter
    def workflow_task_schema(self) -> None:
        self._workflow_task_schema = UNSET

    @property
    def workflow_tasks(self) -> List[WorkflowTaskSummary]:
        """ The input tasks to the workflow task group """
        if isinstance(self._workflow_tasks, Unset):
            raise NotPresentError(self, "workflow_tasks")
        return self._workflow_tasks

    @workflow_tasks.setter
    def workflow_tasks(self, value: List[WorkflowTaskSummary]) -> None:
        self._workflow_tasks = value

    @workflow_tasks.deleter
    def workflow_tasks(self) -> None:
        self._workflow_tasks = UNSET

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
        """ The ID of the workflow task group """
        if isinstance(self._id, Unset):
            raise NotPresentError(self, "id")
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        self._id = value

    @id.deleter
    def id(self) -> None:
        self._id = UNSET

    @property
    def name(self) -> str:
        """ The name of the workflow task group """
        if isinstance(self._name, Unset):
            raise NotPresentError(self, "name")
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @name.deleter
    def name(self) -> None:
        self._name = UNSET
