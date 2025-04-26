from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.container_quantity import ContainerQuantity
from ..models.deprecated_container_volume_for_input import DeprecatedContainerVolumeForInput
from ..models.fields import Fields
from ..models.measurement import Measurement
from ..models.sample_restriction_status import SampleRestrictionStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="ContainerBulkUpdateItem")


@attr.s(auto_attribs=True, repr=False)
class ContainerBulkUpdateItem:
    """  """

    _container_id: str
    _barcode: Union[Unset, str] = UNSET
    _concentration: Union[Unset, Measurement] = UNSET
    _quantity: Union[Unset, ContainerQuantity] = UNSET
    _volume: Union[Unset, DeprecatedContainerVolumeForInput] = UNSET
    _fields: Union[Unset, Fields] = UNSET
    _name: Union[Unset, str] = UNSET
    _parent_storage_id: Union[Unset, str] = UNSET
    _restricted_sample_party_ids: Union[Unset, List[str]] = UNSET
    _restriction_status: Union[Unset, SampleRestrictionStatus] = UNSET
    _sample_owner_ids: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("container_id={}".format(repr(self._container_id)))
        fields.append("barcode={}".format(repr(self._barcode)))
        fields.append("concentration={}".format(repr(self._concentration)))
        fields.append("quantity={}".format(repr(self._quantity)))
        fields.append("volume={}".format(repr(self._volume)))
        fields.append("fields={}".format(repr(self._fields)))
        fields.append("name={}".format(repr(self._name)))
        fields.append("parent_storage_id={}".format(repr(self._parent_storage_id)))
        fields.append("restricted_sample_party_ids={}".format(repr(self._restricted_sample_party_ids)))
        fields.append("restriction_status={}".format(repr(self._restriction_status)))
        fields.append("sample_owner_ids={}".format(repr(self._sample_owner_ids)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "ContainerBulkUpdateItem({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        container_id = self._container_id
        barcode = self._barcode
        concentration: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._concentration, Unset):
            concentration = self._concentration.to_dict()

        quantity: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._quantity, Unset):
            quantity = self._quantity.to_dict()

        volume: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._volume, Unset):
            volume = self._volume.to_dict()

        fields: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._fields, Unset):
            fields = self._fields.to_dict()

        name = self._name
        parent_storage_id = self._parent_storage_id
        restricted_sample_party_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._restricted_sample_party_ids, Unset):
            restricted_sample_party_ids = self._restricted_sample_party_ids

        restriction_status: Union[Unset, int] = UNSET
        if not isinstance(self._restriction_status, Unset):
            restriction_status = self._restriction_status.value

        sample_owner_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._sample_owner_ids, Unset):
            sample_owner_ids = self._sample_owner_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if container_id is not UNSET:
            field_dict["containerId"] = container_id
        if barcode is not UNSET:
            field_dict["barcode"] = barcode
        if concentration is not UNSET:
            field_dict["concentration"] = concentration
        if quantity is not UNSET:
            field_dict["quantity"] = quantity
        if volume is not UNSET:
            field_dict["volume"] = volume
        if fields is not UNSET:
            field_dict["fields"] = fields
        if name is not UNSET:
            field_dict["name"] = name
        if parent_storage_id is not UNSET:
            field_dict["parentStorageId"] = parent_storage_id
        if restricted_sample_party_ids is not UNSET:
            field_dict["restrictedSamplePartyIds"] = restricted_sample_party_ids
        if restriction_status is not UNSET:
            field_dict["restrictionStatus"] = restriction_status
        if sample_owner_ids is not UNSET:
            field_dict["sampleOwnerIds"] = sample_owner_ids

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_container_id() -> str:
            container_id = d.pop("containerId")
            return container_id

        try:
            container_id = get_container_id()
        except KeyError:
            if strict:
                raise
            container_id = cast(str, UNSET)

        def get_barcode() -> Union[Unset, str]:
            barcode = d.pop("barcode")
            return barcode

        try:
            barcode = get_barcode()
        except KeyError:
            if strict:
                raise
            barcode = cast(Union[Unset, str], UNSET)

        def get_concentration() -> Union[Unset, Measurement]:
            concentration: Union[Unset, Union[Unset, Measurement]] = UNSET
            _concentration = d.pop("concentration")

            if not isinstance(_concentration, Unset):
                concentration = Measurement.from_dict(_concentration)

            return concentration

        try:
            concentration = get_concentration()
        except KeyError:
            if strict:
                raise
            concentration = cast(Union[Unset, Measurement], UNSET)

        def get_quantity() -> Union[Unset, ContainerQuantity]:
            quantity: Union[Unset, Union[Unset, ContainerQuantity]] = UNSET
            _quantity = d.pop("quantity")

            if not isinstance(_quantity, Unset):
                quantity = ContainerQuantity.from_dict(_quantity)

            return quantity

        try:
            quantity = get_quantity()
        except KeyError:
            if strict:
                raise
            quantity = cast(Union[Unset, ContainerQuantity], UNSET)

        def get_volume() -> Union[Unset, DeprecatedContainerVolumeForInput]:
            volume: Union[Unset, Union[Unset, DeprecatedContainerVolumeForInput]] = UNSET
            _volume = d.pop("volume")

            if not isinstance(_volume, Unset):
                volume = DeprecatedContainerVolumeForInput.from_dict(_volume)

            return volume

        try:
            volume = get_volume()
        except KeyError:
            if strict:
                raise
            volume = cast(Union[Unset, DeprecatedContainerVolumeForInput], UNSET)

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

        def get_name() -> Union[Unset, str]:
            name = d.pop("name")
            return name

        try:
            name = get_name()
        except KeyError:
            if strict:
                raise
            name = cast(Union[Unset, str], UNSET)

        def get_parent_storage_id() -> Union[Unset, str]:
            parent_storage_id = d.pop("parentStorageId")
            return parent_storage_id

        try:
            parent_storage_id = get_parent_storage_id()
        except KeyError:
            if strict:
                raise
            parent_storage_id = cast(Union[Unset, str], UNSET)

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

        container_bulk_update_item = cls(
            container_id=container_id,
            barcode=barcode,
            concentration=concentration,
            quantity=quantity,
            volume=volume,
            fields=fields,
            name=name,
            parent_storage_id=parent_storage_id,
            restricted_sample_party_ids=restricted_sample_party_ids,
            restriction_status=restriction_status,
            sample_owner_ids=sample_owner_ids,
        )

        container_bulk_update_item.additional_properties = d
        return container_bulk_update_item

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
    def container_id(self) -> str:
        if isinstance(self._container_id, Unset):
            raise NotPresentError(self, "container_id")
        return self._container_id

    @container_id.setter
    def container_id(self, value: str) -> None:
        self._container_id = value

    @property
    def barcode(self) -> str:
        """Barcode of the container. The barcode must be unique within the registry and cannot be empty."""
        if isinstance(self._barcode, Unset):
            raise NotPresentError(self, "barcode")
        return self._barcode

    @barcode.setter
    def barcode(self, value: str) -> None:
        self._barcode = value

    @barcode.deleter
    def barcode(self) -> None:
        self._barcode = UNSET

    @property
    def concentration(self) -> Measurement:
        if isinstance(self._concentration, Unset):
            raise NotPresentError(self, "concentration")
        return self._concentration

    @concentration.setter
    def concentration(self, value: Measurement) -> None:
        self._concentration = value

    @concentration.deleter
    def concentration(self) -> None:
        self._concentration = UNSET

    @property
    def quantity(self) -> ContainerQuantity:
        """ Quantity of a container, well, or transfer. Supports mass, volume, and other quantities. """
        if isinstance(self._quantity, Unset):
            raise NotPresentError(self, "quantity")
        return self._quantity

    @quantity.setter
    def quantity(self, value: ContainerQuantity) -> None:
        self._quantity = value

    @quantity.deleter
    def quantity(self) -> None:
        self._quantity = UNSET

    @property
    def volume(self) -> DeprecatedContainerVolumeForInput:
        """Desired volume for a container, well, or transfer. "volume" type keys are deprecated in API requests; use the more permissive "quantity" type key instead."""
        if isinstance(self._volume, Unset):
            raise NotPresentError(self, "volume")
        return self._volume

    @volume.setter
    def volume(self, value: DeprecatedContainerVolumeForInput) -> None:
        self._volume = value

    @volume.deleter
    def volume(self) -> None:
        self._volume = UNSET

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
    def name(self) -> str:
        if isinstance(self._name, Unset):
            raise NotPresentError(self, "name")
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @name.deleter
    def name(self) -> None:
        self._name = UNSET

    @property
    def parent_storage_id(self) -> str:
        """ ID of containing parent inventory, can also specify a coordinate for plates and boxes (e.g. plt_2bAks9dx:a2). """
        if isinstance(self._parent_storage_id, Unset):
            raise NotPresentError(self, "parent_storage_id")
        return self._parent_storage_id

    @parent_storage_id.setter
    def parent_storage_id(self, value: str) -> None:
        self._parent_storage_id = value

    @parent_storage_id.deleter
    def parent_storage_id(self) -> None:
        self._parent_storage_id = UNSET

    @property
    def restricted_sample_party_ids(self) -> List[str]:
        """IDs of users or teams who have access to use a restricted container. Well plate wells and unrestricted containers do not have restricted sample parties."""
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
        """IDs of users or teams who are sample owners for the container. Well plate wells do not have sample owners."""
        if isinstance(self._sample_owner_ids, Unset):
            raise NotPresentError(self, "sample_owner_ids")
        return self._sample_owner_ids

    @sample_owner_ids.setter
    def sample_owner_ids(self, value: List[str]) -> None:
        self._sample_owner_ids = value

    @sample_owner_ids.deleter
    def sample_owner_ids(self) -> None:
        self._sample_owner_ids = UNSET
