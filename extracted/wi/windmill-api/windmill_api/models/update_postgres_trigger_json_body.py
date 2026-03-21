from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.update_postgres_trigger_json_body_mode import UpdatePostgresTriggerJsonBodyMode
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.update_postgres_trigger_json_body_error_handler_args import (
        UpdatePostgresTriggerJsonBodyErrorHandlerArgs,
    )
    from ..models.update_postgres_trigger_json_body_publication import UpdatePostgresTriggerJsonBodyPublication
    from ..models.update_postgres_trigger_json_body_retry import UpdatePostgresTriggerJsonBodyRetry


T = TypeVar("T", bound="UpdatePostgresTriggerJsonBody")


@_attrs_define
class UpdatePostgresTriggerJsonBody:
    """
    Attributes:
        replication_slot_name (str): Name of the PostgreSQL logical replication slot to use
        publication_name (str): Name of the PostgreSQL publication to subscribe to for change data capture
        path (str): The unique path identifier for this trigger
        script_path (str): Path to the script or flow to execute when database changes are detected
        is_flow (bool): True if script_path points to a flow, false if it points to a script
        postgres_resource_path (str): Path to the PostgreSQL resource containing connection configuration
        mode (Union[Unset, UpdatePostgresTriggerJsonBodyMode]): job trigger mode
        publication (Union[Unset, UpdatePostgresTriggerJsonBodyPublication]): Configuration for creating/managing the
            publication (tables, operations)
        error_handler_path (Union[Unset, str]): Path to a script or flow to run when the triggered job fails
        error_handler_args (Union[Unset, UpdatePostgresTriggerJsonBodyErrorHandlerArgs]): The arguments to pass to the
            script or flow
        retry (Union[Unset, UpdatePostgresTriggerJsonBodyRetry]): Retry configuration for failed module executions
        permissioned_as (Union[Unset, str]): The user or group this trigger runs as. Used during deployment to preserve
            the original trigger owner.
        preserve_permissioned_as (Union[Unset, bool]): When true and the caller is a member of the 'wm_deployers' group,
            preserves the original permissioned_as value instead of overwriting it.
    """

    replication_slot_name: str
    publication_name: str
    path: str
    script_path: str
    is_flow: bool
    postgres_resource_path: str
    mode: Union[Unset, UpdatePostgresTriggerJsonBodyMode] = UNSET
    publication: Union[Unset, "UpdatePostgresTriggerJsonBodyPublication"] = UNSET
    error_handler_path: Union[Unset, str] = UNSET
    error_handler_args: Union[Unset, "UpdatePostgresTriggerJsonBodyErrorHandlerArgs"] = UNSET
    retry: Union[Unset, "UpdatePostgresTriggerJsonBodyRetry"] = UNSET
    permissioned_as: Union[Unset, str] = UNSET
    preserve_permissioned_as: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        replication_slot_name = self.replication_slot_name
        publication_name = self.publication_name
        path = self.path
        script_path = self.script_path
        is_flow = self.is_flow
        postgres_resource_path = self.postgres_resource_path
        mode: Union[Unset, str] = UNSET
        if not isinstance(self.mode, Unset):
            mode = self.mode.value

        publication: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.publication, Unset):
            publication = self.publication.to_dict()

        error_handler_path = self.error_handler_path
        error_handler_args: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.error_handler_args, Unset):
            error_handler_args = self.error_handler_args.to_dict()

        retry: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.retry, Unset):
            retry = self.retry.to_dict()

        permissioned_as = self.permissioned_as
        preserve_permissioned_as = self.preserve_permissioned_as

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "replication_slot_name": replication_slot_name,
                "publication_name": publication_name,
                "path": path,
                "script_path": script_path,
                "is_flow": is_flow,
                "postgres_resource_path": postgres_resource_path,
            }
        )
        if mode is not UNSET:
            field_dict["mode"] = mode
        if publication is not UNSET:
            field_dict["publication"] = publication
        if error_handler_path is not UNSET:
            field_dict["error_handler_path"] = error_handler_path
        if error_handler_args is not UNSET:
            field_dict["error_handler_args"] = error_handler_args
        if retry is not UNSET:
            field_dict["retry"] = retry
        if permissioned_as is not UNSET:
            field_dict["permissioned_as"] = permissioned_as
        if preserve_permissioned_as is not UNSET:
            field_dict["preserve_permissioned_as"] = preserve_permissioned_as

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.update_postgres_trigger_json_body_error_handler_args import (
            UpdatePostgresTriggerJsonBodyErrorHandlerArgs,
        )
        from ..models.update_postgres_trigger_json_body_publication import UpdatePostgresTriggerJsonBodyPublication
        from ..models.update_postgres_trigger_json_body_retry import UpdatePostgresTriggerJsonBodyRetry

        d = src_dict.copy()
        replication_slot_name = d.pop("replication_slot_name")

        publication_name = d.pop("publication_name")

        path = d.pop("path")

        script_path = d.pop("script_path")

        is_flow = d.pop("is_flow")

        postgres_resource_path = d.pop("postgres_resource_path")

        _mode = d.pop("mode", UNSET)
        mode: Union[Unset, UpdatePostgresTriggerJsonBodyMode]
        if isinstance(_mode, Unset):
            mode = UNSET
        else:
            mode = UpdatePostgresTriggerJsonBodyMode(_mode)

        _publication = d.pop("publication", UNSET)
        publication: Union[Unset, UpdatePostgresTriggerJsonBodyPublication]
        if isinstance(_publication, Unset):
            publication = UNSET
        else:
            publication = UpdatePostgresTriggerJsonBodyPublication.from_dict(_publication)

        error_handler_path = d.pop("error_handler_path", UNSET)

        _error_handler_args = d.pop("error_handler_args", UNSET)
        error_handler_args: Union[Unset, UpdatePostgresTriggerJsonBodyErrorHandlerArgs]
        if isinstance(_error_handler_args, Unset):
            error_handler_args = UNSET
        else:
            error_handler_args = UpdatePostgresTriggerJsonBodyErrorHandlerArgs.from_dict(_error_handler_args)

        _retry = d.pop("retry", UNSET)
        retry: Union[Unset, UpdatePostgresTriggerJsonBodyRetry]
        if isinstance(_retry, Unset):
            retry = UNSET
        else:
            retry = UpdatePostgresTriggerJsonBodyRetry.from_dict(_retry)

        permissioned_as = d.pop("permissioned_as", UNSET)

        preserve_permissioned_as = d.pop("preserve_permissioned_as", UNSET)

        update_postgres_trigger_json_body = cls(
            replication_slot_name=replication_slot_name,
            publication_name=publication_name,
            path=path,
            script_path=script_path,
            is_flow=is_flow,
            postgres_resource_path=postgres_resource_path,
            mode=mode,
            publication=publication,
            error_handler_path=error_handler_path,
            error_handler_args=error_handler_args,
            retry=retry,
            permissioned_as=permissioned_as,
            preserve_permissioned_as=preserve_permissioned_as,
        )

        update_postgres_trigger_json_body.additional_properties = d
        return update_postgres_trigger_json_body

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
