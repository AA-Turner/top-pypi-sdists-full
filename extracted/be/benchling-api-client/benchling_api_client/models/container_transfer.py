from typing import Any, cast, Dict, List, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.container_quantity import ContainerQuantity
from ..models.container_transfer_destination_contents_item import ContainerTransferDestinationContentsItem
from ..models.deprecated_container_volume_for_input import DeprecatedContainerVolumeForInput
from ..models.sample_restriction_status import SampleRestrictionStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="ContainerTransfer")


@attr.s(auto_attribs=True, repr=False)
class ContainerTransfer:
    """  """

    _destination_contents: List[ContainerTransferDestinationContentsItem]
    _destination_quantity: Union[Unset, ContainerQuantity] = UNSET
    _destination_volume: Union[Unset, DeprecatedContainerVolumeForInput] = UNSET
    _restricted_sample_party_ids: Union[Unset, List[str]] = UNSET
    _restriction_status: Union[Unset, SampleRestrictionStatus] = UNSET
    _sample_owner_ids: Union[Unset, List[str]] = UNSET
    _source_batch_id: Union[Unset, str] = UNSET
    _source_container_id: Union[Unset, str] = UNSET
    _source_entity_id: Union[Unset, str] = UNSET
    _transfer_quantity: Union[Unset, ContainerQuantity] = UNSET
    _transfer_volume: Union[Unset, DeprecatedContainerVolumeForInput] = UNSET

    def __repr__(self):
        fields = []
        fields.append("destination_contents={}".format(repr(self._destination_contents)))
        fields.append("destination_quantity={}".format(repr(self._destination_quantity)))
        fields.append("destination_volume={}".format(repr(self._destination_volume)))
        fields.append("restricted_sample_party_ids={}".format(repr(self._restricted_sample_party_ids)))
        fields.append("restriction_status={}".format(repr(self._restriction_status)))
        fields.append("sample_owner_ids={}".format(repr(self._sample_owner_ids)))
        fields.append("source_batch_id={}".format(repr(self._source_batch_id)))
        fields.append("source_container_id={}".format(repr(self._source_container_id)))
        fields.append("source_entity_id={}".format(repr(self._source_entity_id)))
        fields.append("transfer_quantity={}".format(repr(self._transfer_quantity)))
        fields.append("transfer_volume={}".format(repr(self._transfer_volume)))
        return "ContainerTransfer({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        destination_contents = []
        for destination_contents_item_data in self._destination_contents:
            destination_contents_item = destination_contents_item_data.to_dict()

            destination_contents.append(destination_contents_item)

        destination_quantity: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._destination_quantity, Unset):
            destination_quantity = self._destination_quantity.to_dict()

        destination_volume: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._destination_volume, Unset):
            destination_volume = self._destination_volume.to_dict()

        restricted_sample_party_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._restricted_sample_party_ids, Unset):
            restricted_sample_party_ids = self._restricted_sample_party_ids

        restriction_status: Union[Unset, int] = UNSET
        if not isinstance(self._restriction_status, Unset):
            restriction_status = self._restriction_status.value

        sample_owner_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._sample_owner_ids, Unset):
            sample_owner_ids = self._sample_owner_ids

        source_batch_id = self._source_batch_id
        source_container_id = self._source_container_id
        source_entity_id = self._source_entity_id
        transfer_quantity: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._transfer_quantity, Unset):
            transfer_quantity = self._transfer_quantity.to_dict()

        transfer_volume: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._transfer_volume, Unset):
            transfer_volume = self._transfer_volume.to_dict()

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if destination_contents is not UNSET:
            field_dict["destinationContents"] = destination_contents
        if destination_quantity is not UNSET:
            field_dict["destinationQuantity"] = destination_quantity
        if destination_volume is not UNSET:
            field_dict["destinationVolume"] = destination_volume
        if restricted_sample_party_ids is not UNSET:
            field_dict["restrictedSamplePartyIds"] = restricted_sample_party_ids
        if restriction_status is not UNSET:
            field_dict["restrictionStatus"] = restriction_status
        if sample_owner_ids is not UNSET:
            field_dict["sampleOwnerIds"] = sample_owner_ids
        if source_batch_id is not UNSET:
            field_dict["sourceBatchId"] = source_batch_id
        if source_container_id is not UNSET:
            field_dict["sourceContainerId"] = source_container_id
        if source_entity_id is not UNSET:
            field_dict["sourceEntityId"] = source_entity_id
        if transfer_quantity is not UNSET:
            field_dict["transferQuantity"] = transfer_quantity
        if transfer_volume is not UNSET:
            field_dict["transferVolume"] = transfer_volume

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_destination_contents() -> List[ContainerTransferDestinationContentsItem]:
            destination_contents = []
            _destination_contents = d.pop("destinationContents")
            for destination_contents_item_data in _destination_contents:
                destination_contents_item = ContainerTransferDestinationContentsItem.from_dict(
                    destination_contents_item_data, strict=False
                )

                destination_contents.append(destination_contents_item)

            return destination_contents

        try:
            destination_contents = get_destination_contents()
        except KeyError:
            if strict:
                raise
            destination_contents = cast(List[ContainerTransferDestinationContentsItem], UNSET)

        def get_destination_quantity() -> Union[Unset, ContainerQuantity]:
            destination_quantity: Union[Unset, Union[Unset, ContainerQuantity]] = UNSET
            _destination_quantity = d.pop("destinationQuantity")

            if not isinstance(_destination_quantity, Unset):
                destination_quantity = ContainerQuantity.from_dict(_destination_quantity)

            return destination_quantity

        try:
            destination_quantity = get_destination_quantity()
        except KeyError:
            if strict:
                raise
            destination_quantity = cast(Union[Unset, ContainerQuantity], UNSET)

        def get_destination_volume() -> Union[Unset, DeprecatedContainerVolumeForInput]:
            destination_volume: Union[Unset, Union[Unset, DeprecatedContainerVolumeForInput]] = UNSET
            _destination_volume = d.pop("destinationVolume")

            if not isinstance(_destination_volume, Unset):
                destination_volume = DeprecatedContainerVolumeForInput.from_dict(_destination_volume)

            return destination_volume

        try:
            destination_volume = get_destination_volume()
        except KeyError:
            if strict:
                raise
            destination_volume = cast(Union[Unset, DeprecatedContainerVolumeForInput], UNSET)

        def get_restricted_sample_party_ids() -> Union[Unset, List[str]]:
            restricted_sample_party_ids = cast(List[str], d.pop("restrictedSamplePartyIds"))

            return restricted_sample_party_ids

        try:
            restricted_sample_party_ids = get_restricted_sample_party_ids()
        except KeyError:
            if strict:
                raise
            restricted_sample_party_ids = cast(Union[Unset, List[str]], UNSET)

        def get_restriction_status() -> Union[Unset, SampleRestrictionStatus]:
            restriction_status = UNSET
            _restriction_status = d.pop("restrictionStatus")
            if _restriction_status is not None and _restriction_status is not UNSET:
                try:
                    restriction_status = SampleRestrictionStatus(_restriction_status)
                except ValueError:
                    restriction_status = SampleRestrictionStatus.of_unknown(_restriction_status)

            return restriction_status

        try:
            restriction_status = get_restriction_status()
        except KeyError:
            if strict:
                raise
            restriction_status = cast(Union[Unset, SampleRestrictionStatus], UNSET)

        def get_sample_owner_ids() -> Union[Unset, List[str]]:
            sample_owner_ids = cast(List[str], d.pop("sampleOwnerIds"))

            return sample_owner_ids

        try:
            sample_owner_ids = get_sample_owner_ids()
        except KeyError:
            if strict:
                raise
            sample_owner_ids = cast(Union[Unset, List[str]], UNSET)

        def get_source_batch_id() -> Union[Unset, str]:
            source_batch_id = d.pop("sourceBatchId")
            return source_batch_id

        try:
            source_batch_id = get_source_batch_id()
        except KeyError:
            if strict:
                raise
            source_batch_id = cast(Union[Unset, str], UNSET)

        def get_source_container_id() -> Union[Unset, str]:
            source_container_id = d.pop("sourceContainerId")
            return source_container_id

        try:
            source_container_id = get_source_container_id()
        except KeyError:
            if strict:
                raise
            source_container_id = cast(Union[Unset, str], UNSET)

        def get_source_entity_id() -> Union[Unset, str]:
            source_entity_id = d.pop("sourceEntityId")
            return source_entity_id

        try:
            source_entity_id = get_source_entity_id()
        except KeyError:
            if strict:
                raise
            source_entity_id = cast(Union[Unset, str], UNSET)

        def get_transfer_quantity() -> Union[Unset, ContainerQuantity]:
            transfer_quantity: Union[Unset, Union[Unset, ContainerQuantity]] = UNSET
            _transfer_quantity = d.pop("transferQuantity")

            if not isinstance(_transfer_quantity, Unset):
                transfer_quantity = ContainerQuantity.from_dict(_transfer_quantity)

            return transfer_quantity

        try:
            transfer_quantity = get_transfer_quantity()
        except KeyError:
            if strict:
                raise
            transfer_quantity = cast(Union[Unset, ContainerQuantity], UNSET)

        def get_transfer_volume() -> Union[Unset, DeprecatedContainerVolumeForInput]:
            transfer_volume: Union[Unset, Union[Unset, DeprecatedContainerVolumeForInput]] = UNSET
            _transfer_volume = d.pop("transferVolume")

            if not isinstance(_transfer_volume, Unset):
                transfer_volume = DeprecatedContainerVolumeForInput.from_dict(_transfer_volume)

            return transfer_volume

        try:
            transfer_volume = get_transfer_volume()
        except KeyError:
            if strict:
                raise
            transfer_volume = cast(Union[Unset, DeprecatedContainerVolumeForInput], UNSET)

        container_transfer = cls(
            destination_contents=destination_contents,
            destination_quantity=destination_quantity,
            destination_volume=destination_volume,
            restricted_sample_party_ids=restricted_sample_party_ids,
            restriction_status=restriction_status,
            sample_owner_ids=sample_owner_ids,
            source_batch_id=source_batch_id,
            source_container_id=source_container_id,
            source_entity_id=source_entity_id,
            transfer_quantity=transfer_quantity,
            transfer_volume=transfer_volume,
        )

        return container_transfer

    @property
    def destination_contents(self) -> List[ContainerTransferDestinationContentsItem]:
        """This represents what the contents of the destination container should look like post-transfer."""
        if isinstance(self._destination_contents, Unset):
            raise NotPresentError(self, "destination_contents")
        return self._destination_contents

    @destination_contents.setter
    def destination_contents(self, value: List[ContainerTransferDestinationContentsItem]) -> None:
        self._destination_contents = value

    @property
    def destination_quantity(self) -> ContainerQuantity:
        """ Quantity of a container, well, or transfer. Supports mass, volume, and other quantities. """
        if isinstance(self._destination_quantity, Unset):
            raise NotPresentError(self, "destination_quantity")
        return self._destination_quantity

    @destination_quantity.setter
    def destination_quantity(self, value: ContainerQuantity) -> None:
        self._destination_quantity = value

    @destination_quantity.deleter
    def destination_quantity(self) -> None:
        self._destination_quantity = UNSET

    @property
    def destination_volume(self) -> DeprecatedContainerVolumeForInput:
        """Desired volume for a container, well, or transfer. "volume" type keys are deprecated in API requests; use the more permissive "quantity" type key instead."""
        if isinstance(self._destination_volume, Unset):
            raise NotPresentError(self, "destination_volume")
        return self._destination_volume

    @destination_volume.setter
    def destination_volume(self, value: DeprecatedContainerVolumeForInput) -> None:
        self._destination_volume = value

    @destination_volume.deleter
    def destination_volume(self) -> None:
        self._destination_volume = UNSET

    @property
    def restricted_sample_party_ids(self) -> List[str]:
        """IDs of users or teams to be set as restricted sample parties for the destination container. If not specified, restricted sample parties from the source container, if present, will be added to those of the destination container. This only applies to stand-alone containers."""
        if isinstance(self._restricted_sample_party_ids, Unset):
            raise NotPresentError(self, "restricted_sample_party_ids")
        return self._restricted_sample_party_ids

    @restricted_sample_party_ids.setter
    def restricted_sample_party_ids(self, value: List[str]) -> None:
        self._restricted_sample_party_ids = value

    @restricted_sample_party_ids.deleter
    def restricted_sample_party_ids(self) -> None:
        self._restricted_sample_party_ids = UNSET

    @property
    def restriction_status(self) -> SampleRestrictionStatus:
        if isinstance(self._restriction_status, Unset):
            raise NotPresentError(self, "restriction_status")
        return self._restriction_status

    @restriction_status.setter
    def restriction_status(self, value: SampleRestrictionStatus) -> None:
        self._restriction_status = value

    @restriction_status.deleter
    def restriction_status(self) -> None:
        self._restriction_status = UNSET

    @property
    def sample_owner_ids(self) -> List[str]:
        """IDs of users or teams to be set as sample owners for the destination container. If not specified, restricted sample parties from the source container, if present, will be added to those of the destination container. This only applies to stand-alone containers."""
        if isinstance(self._sample_owner_ids, Unset):
            raise NotPresentError(self, "sample_owner_ids")
        return self._sample_owner_ids

    @sample_owner_ids.setter
    def sample_owner_ids(self, value: List[str]) -> None:
        self._sample_owner_ids = value

    @sample_owner_ids.deleter
    def sample_owner_ids(self) -> None:
        self._sample_owner_ids = UNSET

    @property
    def source_batch_id(self) -> str:
        """ID of the batch that will be transferred in. Must specify one of sourceEntityId, sourceBatchId, or sourceContainerId."""
        if isinstance(self._source_batch_id, Unset):
            raise NotPresentError(self, "source_batch_id")
        return self._source_batch_id

    @source_batch_id.setter
    def source_batch_id(self, value: str) -> None:
        self._source_batch_id = value

    @source_batch_id.deleter
    def source_batch_id(self) -> None:
        self._source_batch_id = UNSET

    @property
    def source_container_id(self) -> str:
        """ID of the container that will be transferred in. Must specify one of sourceEntityId, sourceBatchId, or sourceContainerId."""
        if isinstance(self._source_container_id, Unset):
            raise NotPresentError(self, "source_container_id")
        return self._source_container_id

    @source_container_id.setter
    def source_container_id(self, value: str) -> None:
        self._source_container_id = value

    @source_container_id.deleter
    def source_container_id(self) -> None:
        self._source_container_id = UNSET

    @property
    def source_entity_id(self) -> str:
        """ID of the entity that will be transferred in. Must specify one of sourceEntityId, sourceBatchId, or sourceContainerId."""
        if isinstance(self._source_entity_id, Unset):
            raise NotPresentError(self, "source_entity_id")
        return self._source_entity_id

    @source_entity_id.setter
    def source_entity_id(self, value: str) -> None:
        self._source_entity_id = value

    @source_entity_id.deleter
    def source_entity_id(self) -> None:
        self._source_entity_id = UNSET

    @property
    def transfer_quantity(self) -> ContainerQuantity:
        """ Quantity of a container, well, or transfer. Supports mass, volume, and other quantities. """
        if isinstance(self._transfer_quantity, Unset):
            raise NotPresentError(self, "transfer_quantity")
        return self._transfer_quantity

    @transfer_quantity.setter
    def transfer_quantity(self, value: ContainerQuantity) -> None:
        self._transfer_quantity = value

    @transfer_quantity.deleter
    def transfer_quantity(self) -> None:
        self._transfer_quantity = UNSET

    @property
    def transfer_volume(self) -> DeprecatedContainerVolumeForInput:
        """Desired volume for a container, well, or transfer. "volume" type keys are deprecated in API requests; use the more permissive "quantity" type key instead."""
        if isinstance(self._transfer_volume, Unset):
            raise NotPresentError(self, "transfer_volume")
        return self._transfer_volume

    @transfer_volume.setter
    def transfer_volume(self, value: DeprecatedContainerVolumeForInput) -> None:
        self._transfer_volume = value

    @transfer_volume.deleter
    def transfer_volume(self) -> None:
        self._transfer_volume = UNSET
