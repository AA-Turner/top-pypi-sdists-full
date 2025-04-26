from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.custom_fields import CustomFields
from ..types import UNSET, Unset

T = TypeVar("T", bound="DatasetCreate")


@attr.s(auto_attribs=True, repr=False)
class DatasetCreate:
    """  """

    _custom_fields: Union[Unset, CustomFields] = UNSET
    _data_frame_id: Union[Unset, str] = UNSET
    _folder_id: Union[Unset, str] = UNSET
    _name: Union[Unset, str] = UNSET
    _study_ids: Union[Unset, None, List[str]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("custom_fields={}".format(repr(self._custom_fields)))
        fields.append("data_frame_id={}".format(repr(self._data_frame_id)))
        fields.append("folder_id={}".format(repr(self._folder_id)))
        fields.append("name={}".format(repr(self._name)))
        fields.append("study_ids={}".format(repr(self._study_ids)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "DatasetCreate({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        custom_fields: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._custom_fields, Unset):
            custom_fields = self._custom_fields.to_dict()

        data_frame_id = self._data_frame_id
        folder_id = self._folder_id
        name = self._name
        study_ids: Union[Unset, None, List[Any]] = UNSET
        if not isinstance(self._study_ids, Unset):
            if self._study_ids is None:
                study_ids = None
            else:
                study_ids = self._study_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if custom_fields is not UNSET:
            field_dict["customFields"] = custom_fields
        if data_frame_id is not UNSET:
            field_dict["dataFrameId"] = data_frame_id
        if folder_id is not UNSET:
            field_dict["folderId"] = folder_id
        if name is not UNSET:
            field_dict["name"] = name
        if study_ids is not UNSET:
            field_dict["study_ids"] = study_ids

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_custom_fields() -> Union[Unset, CustomFields]:
            custom_fields: Union[Unset, Union[Unset, CustomFields]] = UNSET
            _custom_fields = d.pop("customFields")

            if not isinstance(_custom_fields, Unset):
                custom_fields = CustomFields.from_dict(_custom_fields)

            return custom_fields

        try:
            custom_fields = get_custom_fields()
        except KeyError:
            if strict:
                raise
            custom_fields = cast(Union[Unset, CustomFields], UNSET)

        def get_data_frame_id() -> Union[Unset, str]:
            data_frame_id = d.pop("dataFrameId")
            return data_frame_id

        try:
            data_frame_id = get_data_frame_id()
        except KeyError:
            if strict:
                raise
            data_frame_id = cast(Union[Unset, str], UNSET)

        def get_folder_id() -> Union[Unset, str]:
            folder_id = d.pop("folderId")
            return folder_id

        try:
            folder_id = get_folder_id()
        except KeyError:
            if strict:
                raise
            folder_id = cast(Union[Unset, str], UNSET)

        def get_name() -> Union[Unset, str]:
            name = d.pop("name")
            return name

        try:
            name = get_name()
        except KeyError:
            if strict:
                raise
            name = cast(Union[Unset, str], UNSET)

        def get_study_ids() -> Union[Unset, None, List[str]]:
            study_ids = cast(List[str], d.pop("study_ids"))

            return study_ids

        try:
            study_ids = get_study_ids()
        except KeyError:
            if strict:
                raise
            study_ids = cast(Union[Unset, None, List[str]], UNSET)

        dataset_create = cls(
            custom_fields=custom_fields,
            data_frame_id=data_frame_id,
            folder_id=folder_id,
            name=name,
            study_ids=study_ids,
        )

        dataset_create.additional_properties = d
        return dataset_create

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
    def custom_fields(self) -> CustomFields:
        if isinstance(self._custom_fields, Unset):
            raise NotPresentError(self, "custom_fields")
        return self._custom_fields

    @custom_fields.setter
    def custom_fields(self, value: CustomFields) -> None:
        self._custom_fields = value

    @custom_fields.deleter
    def custom_fields(self) -> None:
        self._custom_fields = UNSET

    @property
    def data_frame_id(self) -> str:
        """ ID of the data frame that """
        if isinstance(self._data_frame_id, Unset):
            raise NotPresentError(self, "data_frame_id")
        return self._data_frame_id

    @data_frame_id.setter
    def data_frame_id(self, value: str) -> None:
        self._data_frame_id = value

    @data_frame_id.deleter
    def data_frame_id(self) -> None:
        self._data_frame_id = UNSET

    @property
    def folder_id(self) -> str:
        """ ID of the folder that contains the file """
        if isinstance(self._folder_id, Unset):
            raise NotPresentError(self, "folder_id")
        return self._folder_id

    @folder_id.setter
    def folder_id(self, value: str) -> None:
        self._folder_id = value

    @folder_id.deleter
    def folder_id(self) -> None:
        self._folder_id = UNSET

    @property
    def name(self) -> str:
        """ Display name for the file """
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
    def study_ids(self) -> Optional[List[str]]:
        """The study IDs that the dataset is associated with. If provided, the dataset will be associated with the provided studies. If not provided, the dataset will not be associated with any studies."""
        if isinstance(self._study_ids, Unset):
            raise NotPresentError(self, "study_ids")
        return self._study_ids

    @study_ids.setter
    def study_ids(self, value: Optional[List[str]]) -> None:
        self._study_ids = value

    @study_ids.deleter
    def study_ids(self) -> None:
        self._study_ids = UNSET
