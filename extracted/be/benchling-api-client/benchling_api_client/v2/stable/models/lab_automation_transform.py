import datetime
from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..extensions import NotPresentError
from ..models.lab_automation_benchling_app_errors import LabAutomationBenchlingAppErrors
from ..models.lab_automation_transform_status import LabAutomationTransformStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="LabAutomationTransform")


@attr.s(auto_attribs=True, repr=False)
class LabAutomationTransform:
    """  """

    _api_url: Union[Unset, str] = UNSET
    _blob_id: Union[Unset, None, str] = UNSET
    _custom_transform_id: Union[Unset, None, str] = UNSET
    _errors: Union[Unset, LabAutomationBenchlingAppErrors] = UNSET
    _id: Union[Unset, str] = UNSET
    _input_generator_id: Union[Unset, None, str] = UNSET
    _modified_at: Union[Unset, datetime.datetime] = UNSET
    _output_processor_id: Union[Unset, None, str] = UNSET
    _status: Union[Unset, LabAutomationTransformStatus] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("api_url={}".format(repr(self._api_url)))
        fields.append("blob_id={}".format(repr(self._blob_id)))
        fields.append("custom_transform_id={}".format(repr(self._custom_transform_id)))
        fields.append("errors={}".format(repr(self._errors)))
        fields.append("id={}".format(repr(self._id)))
        fields.append("input_generator_id={}".format(repr(self._input_generator_id)))
        fields.append("modified_at={}".format(repr(self._modified_at)))
        fields.append("output_processor_id={}".format(repr(self._output_processor_id)))
        fields.append("status={}".format(repr(self._status)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "LabAutomationTransform({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        api_url = self._api_url
        blob_id = self._blob_id
        custom_transform_id = self._custom_transform_id
        errors: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._errors, Unset):
            errors = self._errors.to_dict()

        id = self._id
        input_generator_id = self._input_generator_id
        modified_at: Union[Unset, str] = UNSET
        if not isinstance(self._modified_at, Unset):
            modified_at = self._modified_at.isoformat()

        output_processor_id = self._output_processor_id
        status: Union[Unset, int] = UNSET
        if not isinstance(self._status, Unset):
            status = self._status.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if api_url is not UNSET:
            field_dict["apiURL"] = api_url
        if blob_id is not UNSET:
            field_dict["blobId"] = blob_id
        if custom_transform_id is not UNSET:
            field_dict["customTransformId"] = custom_transform_id
        if errors is not UNSET:
            field_dict["errors"] = errors
        if id is not UNSET:
            field_dict["id"] = id
        if input_generator_id is not UNSET:
            field_dict["inputGeneratorId"] = input_generator_id
        if modified_at is not UNSET:
            field_dict["modifiedAt"] = modified_at
        if output_processor_id is not UNSET:
            field_dict["outputProcessorId"] = output_processor_id
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_api_url() -> Union[Unset, str]:
            api_url = d.pop("apiURL")
            return api_url

        try:
            api_url = get_api_url()
        except KeyError:
            if strict:
                raise
            api_url = cast(Union[Unset, str], UNSET)

        def get_blob_id() -> Union[Unset, None, str]:
            blob_id = d.pop("blobId")
            return blob_id

        try:
            blob_id = get_blob_id()
        except KeyError:
            if strict:
                raise
            blob_id = cast(Union[Unset, None, str], UNSET)

        def get_custom_transform_id() -> Union[Unset, None, str]:
            custom_transform_id = d.pop("customTransformId")
            return custom_transform_id

        try:
            custom_transform_id = get_custom_transform_id()
        except KeyError:
            if strict:
                raise
            custom_transform_id = cast(Union[Unset, None, str], UNSET)

        def get_errors() -> Union[Unset, LabAutomationBenchlingAppErrors]:
            errors: Union[Unset, Union[Unset, LabAutomationBenchlingAppErrors]] = UNSET
            _errors = d.pop("errors")

            if not isinstance(_errors, Unset):
                errors = LabAutomationBenchlingAppErrors.from_dict(_errors)

            return errors

        try:
            errors = get_errors()
        except KeyError:
            if strict:
                raise
            errors = cast(Union[Unset, LabAutomationBenchlingAppErrors], UNSET)

        def get_id() -> Union[Unset, str]:
            id = d.pop("id")
            return id

        try:
            id = get_id()
        except KeyError:
            if strict:
                raise
            id = cast(Union[Unset, str], UNSET)

        def get_input_generator_id() -> Union[Unset, None, str]:
            input_generator_id = d.pop("inputGeneratorId")
            return input_generator_id

        try:
            input_generator_id = get_input_generator_id()
        except KeyError:
            if strict:
                raise
            input_generator_id = cast(Union[Unset, None, str], UNSET)

        def get_modified_at() -> Union[Unset, datetime.datetime]:
            modified_at: Union[Unset, datetime.datetime] = UNSET
            _modified_at = d.pop("modifiedAt")
            if _modified_at is not None and not isinstance(_modified_at, Unset):
                modified_at = isoparse(cast(str, _modified_at))

            return modified_at

        try:
            modified_at = get_modified_at()
        except KeyError:
            if strict:
                raise
            modified_at = cast(Union[Unset, datetime.datetime], UNSET)

        def get_output_processor_id() -> Union[Unset, None, str]:
            output_processor_id = d.pop("outputProcessorId")
            return output_processor_id

        try:
            output_processor_id = get_output_processor_id()
        except KeyError:
            if strict:
                raise
            output_processor_id = cast(Union[Unset, None, str], UNSET)

        def get_status() -> Union[Unset, LabAutomationTransformStatus]:
            status = UNSET
            _status = d.pop("status")
            if _status is not None and _status is not UNSET:
                try:
                    status = LabAutomationTransformStatus(_status)
                except ValueError:
                    status = LabAutomationTransformStatus.of_unknown(_status)

            return status

        try:
            status = get_status()
        except KeyError:
            if strict:
                raise
            status = cast(Union[Unset, LabAutomationTransformStatus], UNSET)

        lab_automation_transform = cls(
            api_url=api_url,
            blob_id=blob_id,
            custom_transform_id=custom_transform_id,
            errors=errors,
            id=id,
            input_generator_id=input_generator_id,
            modified_at=modified_at,
            output_processor_id=output_processor_id,
            status=status,
        )

        lab_automation_transform.additional_properties = d
        return lab_automation_transform

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
    def api_url(self) -> str:
        """ The canonical url of the transform in the API. """
        if isinstance(self._api_url, Unset):
            raise NotPresentError(self, "api_url")
        return self._api_url

    @api_url.setter
    def api_url(self, value: str) -> None:
        self._api_url = value

    @api_url.deleter
    def api_url(self) -> None:
        self._api_url = UNSET

    @property
    def blob_id(self) -> Optional[str]:
        if isinstance(self._blob_id, Unset):
            raise NotPresentError(self, "blob_id")
        return self._blob_id

    @blob_id.setter
    def blob_id(self, value: Optional[str]) -> None:
        self._blob_id = value

    @blob_id.deleter
    def blob_id(self) -> None:
        self._blob_id = UNSET

    @property
    def custom_transform_id(self) -> Optional[str]:
        if isinstance(self._custom_transform_id, Unset):
            raise NotPresentError(self, "custom_transform_id")
        return self._custom_transform_id

    @custom_transform_id.setter
    def custom_transform_id(self, value: Optional[str]) -> None:
        self._custom_transform_id = value

    @custom_transform_id.deleter
    def custom_transform_id(self) -> None:
        self._custom_transform_id = UNSET

    @property
    def errors(self) -> LabAutomationBenchlingAppErrors:
        if isinstance(self._errors, Unset):
            raise NotPresentError(self, "errors")
        return self._errors

    @errors.setter
    def errors(self, value: LabAutomationBenchlingAppErrors) -> None:
        self._errors = value

    @errors.deleter
    def errors(self) -> None:
        self._errors = UNSET

    @property
    def id(self) -> str:
        if isinstance(self._id, Unset):
            raise NotPresentError(self, "id")
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        self._id = value

    @id.deleter
    def id(self) -> None:
        self._id = UNSET

    @property
    def input_generator_id(self) -> Optional[str]:
        if isinstance(self._input_generator_id, Unset):
            raise NotPresentError(self, "input_generator_id")
        return self._input_generator_id

    @input_generator_id.setter
    def input_generator_id(self, value: Optional[str]) -> None:
        self._input_generator_id = value

    @input_generator_id.deleter
    def input_generator_id(self) -> None:
        self._input_generator_id = UNSET

    @property
    def modified_at(self) -> datetime.datetime:
        """ DateTime the transform was last modified. """
        if isinstance(self._modified_at, Unset):
            raise NotPresentError(self, "modified_at")
        return self._modified_at

    @modified_at.setter
    def modified_at(self, value: datetime.datetime) -> None:
        self._modified_at = value

    @modified_at.deleter
    def modified_at(self) -> None:
        self._modified_at = UNSET

    @property
    def output_processor_id(self) -> Optional[str]:
        if isinstance(self._output_processor_id, Unset):
            raise NotPresentError(self, "output_processor_id")
        return self._output_processor_id

    @output_processor_id.setter
    def output_processor_id(self, value: Optional[str]) -> None:
        self._output_processor_id = value

    @output_processor_id.deleter
    def output_processor_id(self) -> None:
        self._output_processor_id = UNSET

    @property
    def status(self) -> LabAutomationTransformStatus:
        if isinstance(self._status, Unset):
            raise NotPresentError(self, "status")
        return self._status

    @status.setter
    def status(self, value: LabAutomationTransformStatus) -> None:
        self._status = value

    @status.deleter
    def status(self) -> None:
        self._status = UNSET
