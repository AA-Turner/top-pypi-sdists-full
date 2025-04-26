from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.benchling_app_manifest_feature_canvas_locations import (
    BenchlingAppManifestFeatureCanvasLocations,
)
from ..models.benchling_app_manifest_features_item_type import BenchlingAppManifestFeaturesItemType
from ..types import UNSET, Unset

T = TypeVar("T", bound="BenchlingAppManifestFeaturesItem")


@attr.s(auto_attribs=True, repr=False)
class BenchlingAppManifestFeaturesItem:
    """ A feature allows an App to bidirectionally communicate with users through a Canvas """

    _id: str
    _name: str
    _type: BenchlingAppManifestFeaturesItemType
    _locations: Union[Unset, List[BenchlingAppManifestFeatureCanvasLocations]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("id={}".format(repr(self._id)))
        fields.append("name={}".format(repr(self._name)))
        fields.append("type={}".format(repr(self._type)))
        fields.append("locations={}".format(repr(self._locations)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "BenchlingAppManifestFeaturesItem({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        id = self._id
        name = self._name
        type = self._type.value

        locations: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._locations, Unset):
            locations = []
            for locations_item_data in self._locations:
                locations_item = locations_item_data.value

                locations.append(locations_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if type is not UNSET:
            field_dict["type"] = type
        if locations is not UNSET:
            field_dict["locations"] = locations

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_id() -> str:
            id = d.pop("id")
            return id

        try:
            id = get_id()
        except KeyError:
            if strict:
                raise
            id = cast(str, UNSET)

        def get_name() -> str:
            name = d.pop("name")
            return name

        try:
            name = get_name()
        except KeyError:
            if strict:
                raise
            name = cast(str, UNSET)

        def get_type() -> BenchlingAppManifestFeaturesItemType:
            _type = d.pop("type")
            try:
                type = BenchlingAppManifestFeaturesItemType(_type)
            except ValueError:
                type = BenchlingAppManifestFeaturesItemType.of_unknown(_type)

            return type

        try:
            type = get_type()
        except KeyError:
            if strict:
                raise
            type = cast(BenchlingAppManifestFeaturesItemType, UNSET)

        def get_locations() -> Union[Unset, List[BenchlingAppManifestFeatureCanvasLocations]]:
            locations = []
            _locations = d.pop("locations")
            for locations_item_data in _locations or []:
                _locations_item = locations_item_data
                try:
                    locations_item = BenchlingAppManifestFeatureCanvasLocations(_locations_item)
                except ValueError:
                    locations_item = BenchlingAppManifestFeatureCanvasLocations.of_unknown(_locations_item)

                locations.append(locations_item)

            return locations

        try:
            locations = get_locations()
        except KeyError:
            if strict:
                raise
            locations = cast(Union[Unset, List[BenchlingAppManifestFeatureCanvasLocations]], UNSET)

        benchling_app_manifest_features_item = cls(
            id=id,
            name=name,
            type=type,
            locations=locations,
        )

        benchling_app_manifest_features_item.additional_properties = d
        return benchling_app_manifest_features_item

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
    def id(self) -> str:
        """ User-defined identifier of feature. Must be unique within a single app's manifest. """
        if isinstance(self._id, Unset):
            raise NotPresentError(self, "id")
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        self._id = value

    @property
    def name(self) -> str:
        if isinstance(self._name, Unset):
            raise NotPresentError(self, "name")
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def type(self) -> BenchlingAppManifestFeaturesItemType:
        """The feature type controls where in the UI a Canvas associated with this feature is rendered."""
        if isinstance(self._type, Unset):
            raise NotPresentError(self, "type")
        return self._type

    @type.setter
    def type(self, value: BenchlingAppManifestFeaturesItemType) -> None:
        self._type = value

    @property
    def locations(self) -> List[BenchlingAppManifestFeatureCanvasLocations]:
        """ Only supported when feature type is CANVAS. The locations where the canvas feature should be available. """
        if isinstance(self._locations, Unset):
            raise NotPresentError(self, "locations")
        return self._locations

    @locations.setter
    def locations(self, value: List[BenchlingAppManifestFeatureCanvasLocations]) -> None:
        self._locations = value

    @locations.deleter
    def locations(self) -> None:
        self._locations = UNSET
