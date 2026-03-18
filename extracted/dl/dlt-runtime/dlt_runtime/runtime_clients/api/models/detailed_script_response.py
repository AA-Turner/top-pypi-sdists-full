import datetime
from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
    cast,
)
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.interactive_script_type import InteractiveScriptType
from ..models.script_type import ScriptType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.run_response import RunResponse


T = TypeVar("T", bound="DetailedScriptResponse")


@_attrs_define
class DetailedScriptResponse:
    """
    Attributes:
        created_by (UUID): The ID of the identity who created the script
        date_added (datetime.datetime): The date the entity was added
        date_updated (datetime.datetime): The date the entity was updated
        description (str): The description of the script
        entry_point (str): The entry point of the script. Will usually be the path to a python file in the uploaded
            tarball
        id (UUID): The unique ID of the entity
        name (str): The name of the script
        script_type (ScriptType): The type of the script. Use 'batch' for batch pipelines and 'interactive' for
            notebooks
        version (int): The current version of the script
        workspace_id (UUID): The ID of the workspace the script belongs to
        archived (Union[Unset, bool]): Whether the script is archived and hidden from default listings Default: False.
        interactive_script_type (Union[InteractiveScriptType, None, Unset]): The type of interactive script. Use
            'marimo' for marimo notebook, 'mcp' for MCPs and 'streamlit' for streamlit reports.
        last_run (Union['RunResponse', None, Unset]): The last run of the script, is None if no run has been made
        next_scheduled_run (Union[None, Unset, datetime.datetime]): The next scheduled run of the script, is None if no
            schedule is set
        profile (Union[None, Unset, str]): The name of the profile to use for the script
        public_secret (Union[None, UUID, Unset]): The secret UUID used to generate the public URL for this script
        public_url (Union[None, Unset, str]): The public URL where the script can be accessed without authentication, is
            None if not enabled
        schedule (Union[None, Unset, str]): The schedule of the script. Use 'cron' format for cron jobs
        script_url (Union[None, Unset, str]): The URL where the script can be accessed if interactive
    """

    created_by: UUID
    date_added: datetime.datetime
    date_updated: datetime.datetime
    description: str
    entry_point: str
    id: UUID
    name: str
    script_type: ScriptType
    version: int
    workspace_id: UUID
    archived: Union[Unset, bool] = False
    interactive_script_type: Union[InteractiveScriptType, None, Unset] = UNSET
    last_run: Union["RunResponse", None, Unset] = UNSET
    next_scheduled_run: Union[None, Unset, datetime.datetime] = UNSET
    profile: Union[None, Unset, str] = UNSET
    public_secret: Union[None, UUID, Unset] = UNSET
    public_url: Union[None, Unset, str] = UNSET
    schedule: Union[None, Unset, str] = UNSET
    script_url: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.run_response import RunResponse

        created_by = str(self.created_by)

        date_added = self.date_added.isoformat()

        date_updated = self.date_updated.isoformat()

        description = self.description

        entry_point = self.entry_point

        id = str(self.id)

        name = self.name

        script_type = self.script_type.value

        version = self.version

        workspace_id = str(self.workspace_id)

        archived = self.archived

        interactive_script_type: Union[None, Unset, str]
        if isinstance(self.interactive_script_type, Unset):
            interactive_script_type = UNSET
        elif isinstance(self.interactive_script_type, InteractiveScriptType):
            interactive_script_type = self.interactive_script_type.value
        else:
            interactive_script_type = self.interactive_script_type

        last_run: Union[None, Unset, dict[str, Any]]
        if isinstance(self.last_run, Unset):
            last_run = UNSET
        elif isinstance(self.last_run, RunResponse):
            last_run = self.last_run.to_dict()
        else:
            last_run = self.last_run

        next_scheduled_run: Union[None, Unset, str]
        if isinstance(self.next_scheduled_run, Unset):
            next_scheduled_run = UNSET
        elif isinstance(self.next_scheduled_run, datetime.datetime):
            next_scheduled_run = self.next_scheduled_run.isoformat()
        else:
            next_scheduled_run = self.next_scheduled_run

        profile: Union[None, Unset, str]
        if isinstance(self.profile, Unset):
            profile = UNSET
        else:
            profile = self.profile

        public_secret: Union[None, Unset, str]
        if isinstance(self.public_secret, Unset):
            public_secret = UNSET
        elif isinstance(self.public_secret, UUID):
            public_secret = str(self.public_secret)
        else:
            public_secret = self.public_secret

        public_url: Union[None, Unset, str]
        if isinstance(self.public_url, Unset):
            public_url = UNSET
        else:
            public_url = self.public_url

        schedule: Union[None, Unset, str]
        if isinstance(self.schedule, Unset):
            schedule = UNSET
        else:
            schedule = self.schedule

        script_url: Union[None, Unset, str]
        if isinstance(self.script_url, Unset):
            script_url = UNSET
        else:
            script_url = self.script_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "created_by": created_by,
                "date_added": date_added,
                "date_updated": date_updated,
                "description": description,
                "entry_point": entry_point,
                "id": id,
                "name": name,
                "script_type": script_type,
                "version": version,
                "workspace_id": workspace_id,
            }
        )
        if archived is not UNSET:
            field_dict["archived"] = archived
        if interactive_script_type is not UNSET:
            field_dict["interactive_script_type"] = interactive_script_type
        if last_run is not UNSET:
            field_dict["last_run"] = last_run
        if next_scheduled_run is not UNSET:
            field_dict["next_scheduled_run"] = next_scheduled_run
        if profile is not UNSET:
            field_dict["profile"] = profile
        if public_secret is not UNSET:
            field_dict["public_secret"] = public_secret
        if public_url is not UNSET:
            field_dict["public_url"] = public_url
        if schedule is not UNSET:
            field_dict["schedule"] = schedule
        if script_url is not UNSET:
            field_dict["script_url"] = script_url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.run_response import RunResponse

        d = dict(src_dict)
        created_by = UUID(d.pop("created_by"))

        date_added = isoparse(d.pop("date_added"))

        date_updated = isoparse(d.pop("date_updated"))

        description = d.pop("description")

        entry_point = d.pop("entry_point")

        id = UUID(d.pop("id"))

        name = d.pop("name")

        script_type = ScriptType(d.pop("script_type"))

        version = d.pop("version")

        workspace_id = UUID(d.pop("workspace_id"))

        archived = d.pop("archived", UNSET)

        def _parse_interactive_script_type(
            data: object,
        ) -> Union[InteractiveScriptType, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                interactive_script_type_type_0 = InteractiveScriptType(data)

                return interactive_script_type_type_0
            except:  # noqa: E722
                pass
            return cast(Union[InteractiveScriptType, None, Unset], data)

        interactive_script_type = _parse_interactive_script_type(
            d.pop("interactive_script_type", UNSET)
        )

        def _parse_last_run(data: object) -> Union["RunResponse", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                last_run_type_0 = RunResponse.from_dict(data)

                return last_run_type_0
            except:  # noqa: E722
                pass
            return cast(Union["RunResponse", None, Unset], data)

        last_run = _parse_last_run(d.pop("last_run", UNSET))

        def _parse_next_scheduled_run(
            data: object,
        ) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                next_scheduled_run_type_0 = isoparse(data)

                return next_scheduled_run_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        next_scheduled_run = _parse_next_scheduled_run(
            d.pop("next_scheduled_run", UNSET)
        )

        def _parse_profile(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        profile = _parse_profile(d.pop("profile", UNSET))

        def _parse_public_secret(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                public_secret_type_0 = UUID(data)

                return public_secret_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        public_secret = _parse_public_secret(d.pop("public_secret", UNSET))

        def _parse_public_url(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        public_url = _parse_public_url(d.pop("public_url", UNSET))

        def _parse_schedule(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        schedule = _parse_schedule(d.pop("schedule", UNSET))

        def _parse_script_url(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        script_url = _parse_script_url(d.pop("script_url", UNSET))

        detailed_script_response = cls(
            created_by=created_by,
            date_added=date_added,
            date_updated=date_updated,
            description=description,
            entry_point=entry_point,
            id=id,
            name=name,
            script_type=script_type,
            version=version,
            workspace_id=workspace_id,
            archived=archived,
            interactive_script_type=interactive_script_type,
            last_run=last_run,
            next_scheduled_run=next_scheduled_run,
            profile=profile,
            public_secret=public_secret,
            public_url=public_url,
            schedule=schedule,
            script_url=script_url,
        )

        detailed_script_response.additional_properties = d
        return detailed_script_response

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
