from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.request_response_samples_item_batch import RequestResponseSamplesItemBatch
from ..models.request_response_samples_item_entity import RequestResponseSamplesItemEntity
from ..models.request_response_samples_item_status import RequestResponseSamplesItemStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="RequestResponseSamplesItem")


@attr.s(auto_attribs=True, repr=False)
class RequestResponseSamplesItem:
    """  """

    _batch: Union[Unset, None, RequestResponseSamplesItemBatch] = UNSET
    _entity: Union[Unset, None, RequestResponseSamplesItemEntity] = UNSET
    _status: Union[Unset, RequestResponseSamplesItemStatus] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("batch={}".format(repr(self._batch)))
        fields.append("entity={}".format(repr(self._entity)))
        fields.append("status={}".format(repr(self._status)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "RequestResponseSamplesItem({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        batch: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self._batch, Unset):
            batch = self._batch.to_dict() if self._batch else None

        entity: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self._entity, Unset):
            entity = self._entity.to_dict() if self._entity else None

        status: Union[Unset, int] = UNSET
        if not isinstance(self._status, Unset):
            status = self._status.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if batch is not UNSET:
            field_dict["batch"] = batch
        if entity is not UNSET:
            field_dict["entity"] = entity
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_batch() -> Union[Unset, None, RequestResponseSamplesItemBatch]:
            batch = None
            _batch = d.pop("batch")

            if _batch is not None and not isinstance(_batch, Unset):
                batch = RequestResponseSamplesItemBatch.from_dict(_batch)

            return batch

        try:
            batch = get_batch()
        except KeyError:
            if strict:
                raise
            batch = cast(Union[Unset, None, RequestResponseSamplesItemBatch], UNSET)

        def get_entity() -> Union[Unset, None, RequestResponseSamplesItemEntity]:
            entity = None
            _entity = d.pop("entity")

            if _entity is not None and not isinstance(_entity, Unset):
                entity = RequestResponseSamplesItemEntity.from_dict(_entity)

            return entity

        try:
            entity = get_entity()
        except KeyError:
            if strict:
                raise
            entity = cast(Union[Unset, None, RequestResponseSamplesItemEntity], UNSET)

        def get_status() -> Union[Unset, RequestResponseSamplesItemStatus]:
            status = UNSET
            _status = d.pop("status")
            if _status is not None and _status is not UNSET:
                try:
                    status = RequestResponseSamplesItemStatus(_status)
                except ValueError:
                    status = RequestResponseSamplesItemStatus.of_unknown(_status)

            return status

        try:
            status = get_status()
        except KeyError:
            if strict:
                raise
            status = cast(Union[Unset, RequestResponseSamplesItemStatus], UNSET)

        request_response_samples_item = cls(
            batch=batch,
            entity=entity,
            status=status,
        )

        request_response_samples_item.additional_properties = d
        return request_response_samples_item

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
    def batch(self) -> Optional[RequestResponseSamplesItemBatch]:
        if isinstance(self._batch, Unset):
            raise NotPresentError(self, "batch")
        return self._batch

    @batch.setter
    def batch(self, value: Optional[RequestResponseSamplesItemBatch]) -> None:
        self._batch = value

    @batch.deleter
    def batch(self) -> None:
        self._batch = UNSET

    @property
    def entity(self) -> Optional[RequestResponseSamplesItemEntity]:
        if isinstance(self._entity, Unset):
            raise NotPresentError(self, "entity")
        return self._entity

    @entity.setter
    def entity(self, value: Optional[RequestResponseSamplesItemEntity]) -> None:
        self._entity = value

    @entity.deleter
    def entity(self) -> None:
        self._entity = UNSET

    @property
    def status(self) -> RequestResponseSamplesItemStatus:
        """ The status of the sample, based on the status of the stage run that generated it. """
        if isinstance(self._status, Unset):
            raise NotPresentError(self, "status")
        return self._status

    @status.setter
    def status(self, value: RequestResponseSamplesItemStatus) -> None:
        self._status = value

    @status.deleter
    def status(self) -> None:
        self._status = UNSET
