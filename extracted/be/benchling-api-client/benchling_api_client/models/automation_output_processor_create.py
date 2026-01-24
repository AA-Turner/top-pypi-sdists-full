from typing import Any, cast, Dict, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..types import UNSET, Unset

T = TypeVar("T", bound="AutomationOutputProcessorCreate")


@attr.s(auto_attribs=True, repr=False)
class AutomationOutputProcessorCreate:
    """  """

    _assay_run_id: str
    _automation_file_config_name: str
    _file_id: str
    _complete_with_errors: Union[Unset, bool] = UNSET
    _folder_id: Union[Unset, str] = UNSET
    _locaton_id: Union[Unset, str] = UNSET
    _timezone: Union[Unset, str] = UNSET

    def __repr__(self):
        fields = []
        fields.append("assay_run_id={}".format(repr(self._assay_run_id)))
        fields.append("automation_file_config_name={}".format(repr(self._automation_file_config_name)))
        fields.append("file_id={}".format(repr(self._file_id)))
        fields.append("complete_with_errors={}".format(repr(self._complete_with_errors)))
        fields.append("folder_id={}".format(repr(self._folder_id)))
        fields.append("locaton_id={}".format(repr(self._locaton_id)))
        fields.append("timezone={}".format(repr(self._timezone)))
        return "AutomationOutputProcessorCreate({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        assay_run_id = self._assay_run_id
        automation_file_config_name = self._automation_file_config_name
        file_id = self._file_id
        complete_with_errors = self._complete_with_errors
        folder_id = self._folder_id
        locaton_id = self._locaton_id
        timezone = self._timezone

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if assay_run_id is not UNSET:
            field_dict["assayRunId"] = assay_run_id
        if automation_file_config_name is not UNSET:
            field_dict["automationFileConfigName"] = automation_file_config_name
        if file_id is not UNSET:
            field_dict["fileId"] = file_id
        if complete_with_errors is not UNSET:
            field_dict["completeWithErrors"] = complete_with_errors
        if folder_id is not UNSET:
            field_dict["folderId"] = folder_id
        if locaton_id is not UNSET:
            field_dict["locatonId"] = locaton_id
        if timezone is not UNSET:
            field_dict["timezone"] = timezone

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_assay_run_id() -> str:
            assay_run_id = d.pop("assayRunId")
            return assay_run_id

        try:
            assay_run_id = get_assay_run_id()
        except KeyError:
            if strict:
                raise
            assay_run_id = cast(str, UNSET)

        def get_automation_file_config_name() -> str:
            automation_file_config_name = d.pop("automationFileConfigName")
            return automation_file_config_name

        try:
            automation_file_config_name = get_automation_file_config_name()
        except KeyError:
            if strict:
                raise
            automation_file_config_name = cast(str, UNSET)

        def get_file_id() -> str:
            file_id = d.pop("fileId")
            return file_id

        try:
            file_id = get_file_id()
        except KeyError:
            if strict:
                raise
            file_id = cast(str, UNSET)

        def get_complete_with_errors() -> Union[Unset, bool]:
            complete_with_errors = d.pop("completeWithErrors")
            return complete_with_errors

        try:
            complete_with_errors = get_complete_with_errors()
        except KeyError:
            if strict:
                raise
            complete_with_errors = cast(Union[Unset, bool], UNSET)

        def get_folder_id() -> Union[Unset, str]:
            folder_id = d.pop("folderId")
            return folder_id

        try:
            folder_id = get_folder_id()
        except KeyError:
            if strict:
                raise
            folder_id = cast(Union[Unset, str], UNSET)

        def get_locaton_id() -> Union[Unset, str]:
            locaton_id = d.pop("locatonId")
            return locaton_id

        try:
            locaton_id = get_locaton_id()
        except KeyError:
            if strict:
                raise
            locaton_id = cast(Union[Unset, str], UNSET)

        def get_timezone() -> Union[Unset, str]:
            timezone = d.pop("timezone")
            return timezone

        try:
            timezone = get_timezone()
        except KeyError:
            if strict:
                raise
            timezone = cast(Union[Unset, str], UNSET)

        automation_output_processor_create = cls(
            assay_run_id=assay_run_id,
            automation_file_config_name=automation_file_config_name,
            file_id=file_id,
            complete_with_errors=complete_with_errors,
            folder_id=folder_id,
            locaton_id=locaton_id,
            timezone=timezone,
        )

        return automation_output_processor_create

    @property
    def assay_run_id(self) -> str:
        if isinstance(self._assay_run_id, Unset):
            raise NotPresentError(self, "assay_run_id")
        return self._assay_run_id

    @assay_run_id.setter
    def assay_run_id(self, value: str) -> None:
        self._assay_run_id = value

    @property
    def automation_file_config_name(self) -> str:
        if isinstance(self._automation_file_config_name, Unset):
            raise NotPresentError(self, "automation_file_config_name")
        return self._automation_file_config_name

    @automation_file_config_name.setter
    def automation_file_config_name(self, value: str) -> None:
        self._automation_file_config_name = value

    @property
    def file_id(self) -> str:
        """ The ID of a blob link or the API ID of a file to process. """
        if isinstance(self._file_id, Unset):
            raise NotPresentError(self, "file_id")
        return self._file_id

    @file_id.setter
    def file_id(self, value: str) -> None:
        self._file_id = value

    @property
    def complete_with_errors(self) -> bool:
        """ Specifies whether file processing should complete with errors. False means any error in output file processing will result in no actions being committed. True means that if row-level errors occur, then failing rows and their errors will be saved to errorFile, and actions from successful rows will be committed. """
        if isinstance(self._complete_with_errors, Unset):
            raise NotPresentError(self, "complete_with_errors")
        return self._complete_with_errors

    @complete_with_errors.setter
    def complete_with_errors(self, value: bool) -> None:
        self._complete_with_errors = value

    @complete_with_errors.deleter
    def complete_with_errors(self) -> None:
        self._complete_with_errors = UNSET

    @property
    def folder_id(self) -> str:
        """ The API ID of the folder to set for the automation output file. Folder items created by the correpsonding output processor will be created in this folder. """
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
    def locaton_id(self) -> str:
        """ The API ID of the location to set for the automation output file. Storable items created by the correpsonding output processor will be created at this location. """
        if isinstance(self._locaton_id, Unset):
            raise NotPresentError(self, "locaton_id")
        return self._locaton_id

    @locaton_id.setter
    def locaton_id(self, value: str) -> None:
        self._locaton_id = value

    @locaton_id.deleter
    def locaton_id(self) -> None:
        self._locaton_id = UNSET

    @property
    def timezone(self) -> str:
        """ The timezone to set for the automation output file. Used as the timezone for the timestamp fields if not set in the timestamp. """
        if isinstance(self._timezone, Unset):
            raise NotPresentError(self, "timezone")
        return self._timezone

    @timezone.setter
    def timezone(self, value: str) -> None:
        self._timezone = value

    @timezone.deleter
    def timezone(self) -> None:
        self._timezone = UNSET
