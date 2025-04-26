from typing import Any, cast, Dict, List, Optional, Type, TypeVar

import attr

from ..extensions import NotPresentError
from ..models.benchling_app_manifest_alpha_features_item_type import BenchlingAppManifestAlphaFeaturesItemType
from ..types import UNSET, Unset

T = TypeVar("T", bound="BenchlingAppManifestAlphaFeaturesItem")


@attr.s(auto_attribs=True, repr=False)
class BenchlingAppManifestAlphaFeaturesItem:
    """ A feature allows an App to bidirectionally communicate with users through a Canvas """

    _id: str
    _name: str
    _type: BenchlingAppManifestAlphaFeaturesItemType
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("id={}".format(repr(self._id)))
        fields.append("name={}".format(repr(self._name)))
        fields.append("type={}".format(repr(self._type)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "BenchlingAppManifestAlphaFeaturesItem({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        id = self._id
        name = self._name
        type = self._type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if type is not UNSET:
            field_dict["type"] = type

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

        def get_type() -> BenchlingAppManifestAlphaFeaturesItemType:
            _type = d.pop("type")
            try:
                type = BenchlingAppManifestAlphaFeaturesItemType(_type)
            except ValueError:
                type = BenchlingAppManifestAlphaFeaturesItemType.of_unknown(_type)

            return type

        try:
            type = get_type()
        except KeyError:
            if strict:
                raise
            type = cast(BenchlingAppManifestAlphaFeaturesItemType, UNSET)

        benchling_app_manifest_alpha_features_item = cls(
            id=id,
            name=name,
            type=type,
        )

        benchling_app_manifest_alpha_features_item.additional_properties = d
        return benchling_app_manifest_alpha_features_item

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
    def type(self) -> BenchlingAppManifestAlphaFeaturesItemType:
        """The feature type controls where in the UI a Canvas associated with this feature is rendered."""
        if isinstance(self._type, Unset):
            raise NotPresentError(self, "type")
        return self._type

    @type.setter
    def type(self, value: BenchlingAppManifestAlphaFeaturesItemType) -> None:
        self._type = value
