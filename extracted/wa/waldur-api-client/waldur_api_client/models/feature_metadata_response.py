from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.feature_metadata_response_feature_enums import FeatureMetadataResponseFeatureEnums
    from ..models.feature_metadata_response_features_item import FeatureMetadataResponseFeaturesItem


T = TypeVar("T", bound="FeatureMetadataResponse")


@_attrs_define
class FeatureMetadataResponse:
    """
    Attributes:
        features (list['FeatureMetadataResponseFeaturesItem']): List of feature sections with descriptions
        feature_enums (FeatureMetadataResponseFeatureEnums): Nested feature enum values by section
    """

    features: list["FeatureMetadataResponseFeaturesItem"]
    feature_enums: "FeatureMetadataResponseFeatureEnums"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        features = []
        for features_item_data in self.features:
            features_item = features_item_data.to_dict()
            features.append(features_item)

        feature_enums = self.feature_enums.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "features": features,
                "feature_enums": feature_enums,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.feature_metadata_response_feature_enums import FeatureMetadataResponseFeatureEnums
        from ..models.feature_metadata_response_features_item import FeatureMetadataResponseFeaturesItem

        d = dict(src_dict)
        features = []
        _features = d.pop("features")
        for features_item_data in _features:
            features_item = FeatureMetadataResponseFeaturesItem.from_dict(features_item_data)

            features.append(features_item)

        feature_enums = FeatureMetadataResponseFeatureEnums.from_dict(d.pop("feature_enums"))

        feature_metadata_response = cls(
            features=features,
            feature_enums=feature_enums,
        )

        feature_metadata_response.additional_properties = d
        return feature_metadata_response

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
