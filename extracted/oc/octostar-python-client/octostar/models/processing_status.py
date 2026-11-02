from typing import (
    Any,
    Dict,
    List,
    Type,
    TypeVar,
    Union,
)

import attr

from ..models.child_processing_status import ChildProcessingStatus
from ..models.processing_status_code import ProcessingStatusCode
from ..types import UNSET, Unset

APPEND_TOKEN = "$append"

T = TypeVar("T", bound="ProcessingStatus")


def _serialize_appendable_list(
    value: Union[Unset, None, List[Union[str, ChildProcessingStatus, Dict[str, Any]]]],
) -> Union[Unset, None, List[Any]]:
    if isinstance(value, Unset):
        return UNSET
    if value is None:
        return None
    serialized: List[Any] = []
    for item in value:
        if isinstance(item, str):
            serialized.append(item)
        elif isinstance(item, ChildProcessingStatus):
            serialized.append(item.to_dict())
        else:
            serialized.append(item)
    return serialized


def _deserialize_appendable_list(
    value: Any,
) -> Union[Unset, None, List[Union[str, ChildProcessingStatus, Dict[str, Any]]]]:
    if isinstance(value, Unset):
        return UNSET
    if value is None:
        return None
    out: List[Union[str, ChildProcessingStatus, Dict[str, Any]]] = []
    for item in value:
        if isinstance(item, str):
            out.append(item)
        elif isinstance(item, dict):
            out.append(ChildProcessingStatus.from_dict(item))
        else:
            out.append(item)
    return out


@attr.s(auto_attribs=True)
class ProcessingStatus:
    """
    Processing status for an entity in the pipeline.

    Note: `timeout` is a caching field - it is NOT stored in the actual status data.
    The ontology is determined from the x-ontology header, not from this model.

    Required identity fields on every write:
    - `entity_id`: the entity UID.
    - `entity_type`: the entity type/concept. Treated as fundamental
      identity (mirroring `entity_id`) -- the per-workspace stats
      aggregation, the fragment-exclusion filter, and the recursive
      rollup all read it without a presence check, so producers MUST
      send it on every status write (including parent updates that
      only append to `fragment_errors` / `fragment_warnings`).

    Trust contract on read: the persisted status snapshot is fully
    trustworthy only when `status_code` is **`COMPLETED`** or
    **`FAILED`** (non-stale terminal states). `STALE` is also terminal
    but signals an unsettled prior run -- the redeploy cleanup
    transitions stuck-partial roots to `STALE` so a fresh run can
    reprocess them, and whatever `detailed_status` is attached
    reflects whatever the previous run managed to write before being
    torn down. Callers that need a definitive answer should gate on
    `status_code in {COMPLETED, FAILED}`.

    fragment_errors / fragment_warnings / warnings each support two modes
    via the `$append` sentinel-token convention:
    - ["$append", err1, err2]  -> append err1, err2 to existing list
    - [err1, err2]             -> replace entire list
    - [] or None               -> clear the list
    - UNSET / omitted          -> no change

    ### Attributes:
    * `entity_id (str)`: Identifier of the entity (required)
    * `entity_type (str)`: Type of the entity (required)
    * `status_code (Union[Unset, ProcessingStatusCode])`: Processing status code (optional)
    * `entity_label (Union[Unset, str])`: Human-readable label for the entity
    * `reason (Union[Unset, str])`: Reason for the status
    * `timeout (Union[Unset, int])`: Redis cache TTL in seconds (not stored in status)
    * `timestamp (Union[Unset, str])`: ISO timestamp when status was last updated
    * `do_not_reindex_before (Union[Unset, str])`: UTC timestamp before which reindexing is rejected
    * `do_not_update_before (Union[Unset, str])`: UTC timestamp; stale updates with older value are silently nooped
    * `n_child_fragments (Union[Unset, int])`: Direct-child fragment count declared by this entity.
    * `source_entity_uid (Union[Unset, str])`: Global-root UID. Required on every fragment write.
    * `os_parent_uid (Union[Unset, str])`: Direct-parent UID. Required on every fragment write.
    * `os_workspace (Union[Unset, str])`: Workspace UID; required for per-workspace stats bucketing.
    * `fragment_errors (Union[Unset, None, List])`: Fragment processor errors, with optional $append token
    * `fragment_warnings (Union[Unset, None, List])`: Fragment processor warnings, with optional $append token
    * `warnings (Union[Unset, None, List])`: Entity-level warnings, with optional $append token
    """

    entity_id: str
    entity_type: str
    status_code: Union[Unset, ProcessingStatusCode] = UNSET
    entity_label: Union[Unset, str] = UNSET
    reason: Union[Unset, str] = UNSET
    timeout: Union[Unset, int] = UNSET
    timestamp: Union[Unset, str] = UNSET
    do_not_reindex_before: Union[Unset, str] = UNSET
    do_not_update_before: Union[Unset, str] = UNSET
    n_child_fragments: Union[Unset, int] = UNSET
    source_entity_uid: Union[Unset, str] = UNSET
    os_parent_uid: Union[Unset, str] = UNSET
    os_workspace: Union[Unset, str] = UNSET
    fragment_errors: Union[
        Unset, None, List[Union[str, ChildProcessingStatus, Dict[str, Any]]]
    ] = UNSET
    fragment_warnings: Union[
        Unset, None, List[Union[str, ChildProcessingStatus, Dict[str, Any]]]
    ] = UNSET
    warnings: Union[
        Unset, None, List[Union[str, ChildProcessingStatus, Dict[str, Any]]]
    ] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        entity_id = self.entity_id
        entity_type = self.entity_type

        status_code: Union[Unset, str] = UNSET
        if not isinstance(self.status_code, Unset):
            status_code = self.status_code.value

        entity_label = self.entity_label
        reason = self.reason
        timeout = self.timeout
        timestamp = self.timestamp
        do_not_reindex_before = self.do_not_reindex_before
        do_not_update_before = self.do_not_update_before
        n_child_fragments = self.n_child_fragments
        source_entity_uid = self.source_entity_uid
        os_parent_uid = self.os_parent_uid
        os_workspace = self.os_workspace

        fragment_errors = _serialize_appendable_list(self.fragment_errors)
        fragment_warnings = _serialize_appendable_list(self.fragment_warnings)
        warnings = _serialize_appendable_list(self.warnings)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "entity_id": entity_id,
                "entity_type": entity_type,
            }
        )
        if status_code is not UNSET:
            field_dict["status_code"] = status_code
        if entity_label is not UNSET:
            field_dict["entity_label"] = entity_label
        if reason is not UNSET:
            field_dict["reason"] = reason
        if timeout is not UNSET:
            field_dict["timeout"] = timeout
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp
        if do_not_reindex_before is not UNSET:
            field_dict["do_not_reindex_before"] = do_not_reindex_before
        if do_not_update_before is not UNSET:
            field_dict["do_not_update_before"] = do_not_update_before
        if n_child_fragments is not UNSET:
            field_dict["n_child_fragments"] = n_child_fragments
        if source_entity_uid is not UNSET:
            field_dict["source_entity_uid"] = source_entity_uid
        if os_parent_uid is not UNSET:
            field_dict["os_parent_uid"] = os_parent_uid
        if os_workspace is not UNSET:
            field_dict["os_workspace"] = os_workspace
        if not isinstance(fragment_errors, Unset):
            field_dict["fragment_errors"] = fragment_errors
        if not isinstance(fragment_warnings, Unset):
            field_dict["fragment_warnings"] = fragment_warnings
        if not isinstance(warnings, Unset):
            field_dict["warnings"] = warnings

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        entity_id = d.pop("entity_id")
        entity_type = d.pop("entity_type")

        _status_code = d.pop("status_code", UNSET)
        status_code: Union[Unset, ProcessingStatusCode]
        if isinstance(_status_code, Unset):
            status_code = UNSET
        else:
            status_code = ProcessingStatusCode(_status_code)

        entity_label = d.pop("entity_label", UNSET)
        reason = d.pop("reason", UNSET)
        timeout = d.pop("timeout", UNSET)
        timestamp = d.pop("timestamp", UNSET)
        do_not_reindex_before = d.pop("do_not_reindex_before", UNSET)
        do_not_update_before = d.pop("do_not_update_before", UNSET)
        n_child_fragments = d.pop("n_child_fragments", UNSET)
        source_entity_uid = d.pop("source_entity_uid", UNSET)
        os_parent_uid = d.pop("os_parent_uid", UNSET)
        os_workspace = d.pop("os_workspace", UNSET)

        fragment_errors = _deserialize_appendable_list(d.pop("fragment_errors", UNSET))
        fragment_warnings = _deserialize_appendable_list(
            d.pop("fragment_warnings", UNSET)
        )
        warnings = _deserialize_appendable_list(d.pop("warnings", UNSET))

        processing_status = cls(
            entity_id=entity_id,
            entity_type=entity_type,
            status_code=status_code,
            entity_label=entity_label,
            reason=reason,
            timeout=timeout,
            timestamp=timestamp,
            do_not_reindex_before=do_not_reindex_before,
            do_not_update_before=do_not_update_before,
            n_child_fragments=n_child_fragments,
            source_entity_uid=source_entity_uid,
            os_parent_uid=os_parent_uid,
            os_workspace=os_workspace,
            fragment_errors=fragment_errors,
            fragment_warnings=fragment_warnings,
            warnings=warnings,
        )

        processing_status.additional_properties = d
        return processing_status

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
