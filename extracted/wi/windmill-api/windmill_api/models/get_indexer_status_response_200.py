from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_indexer_status_response_200_job_indexer import GetIndexerStatusResponse200JobIndexer
    from ..models.get_indexer_status_response_200_log_indexer import GetIndexerStatusResponse200LogIndexer


T = TypeVar("T", bound="GetIndexerStatusResponse200")


@_attrs_define
class GetIndexerStatusResponse200:
    """
    Attributes:
        job_indexer (Union[Unset, GetIndexerStatusResponse200JobIndexer]):
        log_indexer (Union[Unset, GetIndexerStatusResponse200LogIndexer]):
    """

    job_indexer: Union[Unset, "GetIndexerStatusResponse200JobIndexer"] = UNSET
    log_indexer: Union[Unset, "GetIndexerStatusResponse200LogIndexer"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        job_indexer: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.job_indexer, Unset):
            job_indexer = self.job_indexer.to_dict()

        log_indexer: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.log_indexer, Unset):
            log_indexer = self.log_indexer.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if job_indexer is not UNSET:
            field_dict["job_indexer"] = job_indexer
        if log_indexer is not UNSET:
            field_dict["log_indexer"] = log_indexer

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_indexer_status_response_200_job_indexer import GetIndexerStatusResponse200JobIndexer
        from ..models.get_indexer_status_response_200_log_indexer import GetIndexerStatusResponse200LogIndexer

        d = src_dict.copy()
        _job_indexer = d.pop("job_indexer", UNSET)
        job_indexer: Union[Unset, GetIndexerStatusResponse200JobIndexer]
        if isinstance(_job_indexer, Unset):
            job_indexer = UNSET
        else:
            job_indexer = GetIndexerStatusResponse200JobIndexer.from_dict(_job_indexer)

        _log_indexer = d.pop("log_indexer", UNSET)
        log_indexer: Union[Unset, GetIndexerStatusResponse200LogIndexer]
        if isinstance(_log_indexer, Unset):
            log_indexer = UNSET
        else:
            log_indexer = GetIndexerStatusResponse200LogIndexer.from_dict(_log_indexer)

        get_indexer_status_response_200 = cls(
            job_indexer=job_indexer,
            log_indexer=log_indexer,
        )

        get_indexer_status_response_200.additional_properties = d
        return get_indexer_status_response_200

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
