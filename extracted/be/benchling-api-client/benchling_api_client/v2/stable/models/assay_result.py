import datetime
from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..extensions import NotPresentError
from ..models.archive_record import ArchiveRecord
from ..models.assay_result_field_validation import AssayResultFieldValidation
from ..models.fields import Fields
from ..models.schema_summary import SchemaSummary
from ..models.user_summary import UserSummary
from ..types import UNSET, Unset

T = TypeVar("T", bound="AssayResult")


@attr.s(auto_attribs=True, repr=False)
class AssayResult:
    """  """

    _archive_record: Union[Unset, None, ArchiveRecord] = UNSET
    _created_at: Union[Unset, datetime.datetime] = UNSET
    _creator: Union[Unset, UserSummary] = UNSET
    _entry_id: Union[Unset, None, str] = UNSET
    _field_validation: Union[Unset, AssayResultFieldValidation] = UNSET
    _fields: Union[Unset, Fields] = UNSET
    _id: Union[Unset, str] = UNSET
    _is_reviewed: Union[Unset, bool] = UNSET
    _modified_at: Union[Unset, datetime.datetime] = UNSET
    _project_id: Union[Unset, None, str] = UNSET
    _schema: Union[Unset, SchemaSummary] = UNSET
    _validation_comment: Union[Unset, str] = UNSET
    _validation_status: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("archive_record={}".format(repr(self._archive_record)))
        fields.append("created_at={}".format(repr(self._created_at)))
        fields.append("creator={}".format(repr(self._creator)))
        fields.append("entry_id={}".format(repr(self._entry_id)))
        fields.append("field_validation={}".format(repr(self._field_validation)))
        fields.append("fields={}".format(repr(self._fields)))
        fields.append("id={}".format(repr(self._id)))
        fields.append("is_reviewed={}".format(repr(self._is_reviewed)))
        fields.append("modified_at={}".format(repr(self._modified_at)))
        fields.append("project_id={}".format(repr(self._project_id)))
        fields.append("schema={}".format(repr(self._schema)))
        fields.append("validation_comment={}".format(repr(self._validation_comment)))
        fields.append("validation_status={}".format(repr(self._validation_status)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "AssayResult({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        archive_record: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self._archive_record, Unset):
            archive_record = self._archive_record.to_dict() if self._archive_record else None

        created_at: Union[Unset, str] = UNSET
        if not isinstance(self._created_at, Unset):
            created_at = self._created_at.isoformat()

        creator: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._creator, Unset):
            creator = self._creator.to_dict()

        entry_id = self._entry_id
        field_validation: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._field_validation, Unset):
            field_validation = self._field_validation.to_dict()

        fields: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._fields, Unset):
            fields = self._fields.to_dict()

        id = self._id
        is_reviewed = self._is_reviewed
        modified_at: Union[Unset, str] = UNSET
        if not isinstance(self._modified_at, Unset):
            modified_at = self._modified_at.isoformat()

        project_id = self._project_id
        schema: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._schema, Unset):
            schema = self._schema.to_dict()

        validation_comment = self._validation_comment
        validation_status = self._validation_status

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if archive_record is not UNSET:
            field_dict["archiveRecord"] = archive_record
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if creator is not UNSET:
            field_dict["creator"] = creator
        if entry_id is not UNSET:
            field_dict["entryId"] = entry_id
        if field_validation is not UNSET:
            field_dict["fieldValidation"] = field_validation
        if fields is not UNSET:
            field_dict["fields"] = fields
        if id is not UNSET:
            field_dict["id"] = id
        if is_reviewed is not UNSET:
            field_dict["isReviewed"] = is_reviewed
        if modified_at is not UNSET:
            field_dict["modifiedAt"] = modified_at
        if project_id is not UNSET:
            field_dict["projectId"] = project_id
        if schema is not UNSET:
            field_dict["schema"] = schema
        if validation_comment is not UNSET:
            field_dict["validationComment"] = validation_comment
        if validation_status is not UNSET:
            field_dict["validationStatus"] = validation_status

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_archive_record() -> Union[Unset, None, ArchiveRecord]:
            archive_record = None
            _archive_record = d.pop("archiveRecord")

            if _archive_record is not None and not isinstance(_archive_record, Unset):
                archive_record = ArchiveRecord.from_dict(_archive_record)

            return archive_record

        try:
            archive_record = get_archive_record()
        except KeyError:
            if strict:
                raise
            archive_record = cast(Union[Unset, None, ArchiveRecord], UNSET)

        def get_created_at() -> Union[Unset, datetime.datetime]:
            created_at: Union[Unset, datetime.datetime] = UNSET
            _created_at = d.pop("createdAt")
            if _created_at is not None and not isinstance(_created_at, Unset):
                created_at = isoparse(cast(str, _created_at))

            return created_at

        try:
            created_at = get_created_at()
        except KeyError:
            if strict:
                raise
            created_at = cast(Union[Unset, datetime.datetime], UNSET)

        def get_creator() -> Union[Unset, UserSummary]:
            creator: Union[Unset, Union[Unset, UserSummary]] = UNSET
            _creator = d.pop("creator")

            if not isinstance(_creator, Unset):
                creator = UserSummary.from_dict(_creator)

            return creator

        try:
            creator = get_creator()
        except KeyError:
            if strict:
                raise
            creator = cast(Union[Unset, UserSummary], UNSET)

        def get_entry_id() -> Union[Unset, None, str]:
            entry_id = d.pop("entryId")
            return entry_id

        try:
            entry_id = get_entry_id()
        except KeyError:
            if strict:
                raise
            entry_id = cast(Union[Unset, None, str], UNSET)

        def get_field_validation() -> Union[Unset, AssayResultFieldValidation]:
            field_validation: Union[Unset, Union[Unset, AssayResultFieldValidation]] = UNSET
            _field_validation = d.pop("fieldValidation")

            if not isinstance(_field_validation, Unset):
                field_validation = AssayResultFieldValidation.from_dict(_field_validation)

            return field_validation

        try:
            field_validation = get_field_validation()
        except KeyError:
            if strict:
                raise
            field_validation = cast(Union[Unset, AssayResultFieldValidation], UNSET)

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

        def get_id() -> Union[Unset, str]:
            id = d.pop("id")
            return id

        try:
            id = get_id()
        except KeyError:
            if strict:
                raise
            id = cast(Union[Unset, str], UNSET)

        def get_is_reviewed() -> Union[Unset, bool]:
            is_reviewed = d.pop("isReviewed")
            return is_reviewed

        try:
            is_reviewed = get_is_reviewed()
        except KeyError:
            if strict:
                raise
            is_reviewed = cast(Union[Unset, bool], UNSET)

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

        def get_project_id() -> Union[Unset, None, str]:
            project_id = d.pop("projectId")
            return project_id

        try:
            project_id = get_project_id()
        except KeyError:
            if strict:
                raise
            project_id = cast(Union[Unset, None, str], UNSET)

        def get_schema() -> Union[Unset, SchemaSummary]:
            schema: Union[Unset, Union[Unset, SchemaSummary]] = UNSET
            _schema = d.pop("schema")

            if not isinstance(_schema, Unset):
                schema = SchemaSummary.from_dict(_schema)

            return schema

        try:
            schema = get_schema()
        except KeyError:
            if strict:
                raise
            schema = cast(Union[Unset, SchemaSummary], UNSET)

        def get_validation_comment() -> Union[Unset, str]:
            validation_comment = d.pop("validationComment")
            return validation_comment

        try:
            validation_comment = get_validation_comment()
        except KeyError:
            if strict:
                raise
            validation_comment = cast(Union[Unset, str], UNSET)

        def get_validation_status() -> Union[Unset, str]:
            validation_status = d.pop("validationStatus")
            return validation_status

        try:
            validation_status = get_validation_status()
        except KeyError:
            if strict:
                raise
            validation_status = cast(Union[Unset, str], UNSET)

        assay_result = cls(
            archive_record=archive_record,
            created_at=created_at,
            creator=creator,
            entry_id=entry_id,
            field_validation=field_validation,
            fields=fields,
            id=id,
            is_reviewed=is_reviewed,
            modified_at=modified_at,
            project_id=project_id,
            schema=schema,
            validation_comment=validation_comment,
            validation_status=validation_status,
        )

        assay_result.additional_properties = d
        return assay_result

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
    def archive_record(self) -> Optional[ArchiveRecord]:
        if isinstance(self._archive_record, Unset):
            raise NotPresentError(self, "archive_record")
        return self._archive_record

    @archive_record.setter
    def archive_record(self, value: Optional[ArchiveRecord]) -> None:
        self._archive_record = value

    @archive_record.deleter
    def archive_record(self) -> None:
        self._archive_record = UNSET

    @property
    def created_at(self) -> datetime.datetime:
        """ DateTime at which the the result was created """
        if isinstance(self._created_at, Unset):
            raise NotPresentError(self, "created_at")
        return self._created_at

    @created_at.setter
    def created_at(self, value: datetime.datetime) -> None:
        self._created_at = value

    @created_at.deleter
    def created_at(self) -> None:
        self._created_at = UNSET

    @property
    def creator(self) -> UserSummary:
        if isinstance(self._creator, Unset):
            raise NotPresentError(self, "creator")
        return self._creator

    @creator.setter
    def creator(self, value: UserSummary) -> None:
        self._creator = value

    @creator.deleter
    def creator(self) -> None:
        self._creator = UNSET

    @property
    def entry_id(self) -> Optional[str]:
        """ ID of the entry that this result is attached to """
        if isinstance(self._entry_id, Unset):
            raise NotPresentError(self, "entry_id")
        return self._entry_id

    @entry_id.setter
    def entry_id(self, value: Optional[str]) -> None:
        self._entry_id = value

    @entry_id.deleter
    def entry_id(self) -> None:
        self._entry_id = UNSET

    @property
    def field_validation(self) -> AssayResultFieldValidation:
        """Object mapping field names to a UserValidation Resource object for that field. To **set** validation for a result, you *must* use this object."""
        if isinstance(self._field_validation, Unset):
            raise NotPresentError(self, "field_validation")
        return self._field_validation

    @field_validation.setter
    def field_validation(self, value: AssayResultFieldValidation) -> None:
        self._field_validation = value

    @field_validation.deleter
    def field_validation(self) -> None:
        self._field_validation = UNSET

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
    def id(self) -> str:
        """ ID of the result """
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
    def is_reviewed(self) -> bool:
        """ Whether or not this result is attached to an accepted entry """
        if isinstance(self._is_reviewed, Unset):
            raise NotPresentError(self, "is_reviewed")
        return self._is_reviewed

    @is_reviewed.setter
    def is_reviewed(self, value: bool) -> None:
        self._is_reviewed = value

    @is_reviewed.deleter
    def is_reviewed(self) -> None:
        self._is_reviewed = UNSET

    @property
    def modified_at(self) -> datetime.datetime:
        """ DateTime at which the the result was last modified """
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
    def project_id(self) -> Optional[str]:
        """ ID of the project to insert the result into """
        if isinstance(self._project_id, Unset):
            raise NotPresentError(self, "project_id")
        return self._project_id

    @project_id.setter
    def project_id(self, value: Optional[str]) -> None:
        self._project_id = value

    @project_id.deleter
    def project_id(self) -> None:
        self._project_id = UNSET

    @property
    def schema(self) -> SchemaSummary:
        if isinstance(self._schema, Unset):
            raise NotPresentError(self, "schema")
        return self._schema

    @schema.setter
    def schema(self, value: SchemaSummary) -> None:
        self._schema = value

    @schema.deleter
    def schema(self) -> None:
        self._schema = UNSET

    @property
    def validation_comment(self) -> str:
        if isinstance(self._validation_comment, Unset):
            raise NotPresentError(self, "validation_comment")
        return self._validation_comment

    @validation_comment.setter
    def validation_comment(self, value: str) -> None:
        self._validation_comment = value

    @validation_comment.deleter
    def validation_comment(self) -> None:
        self._validation_comment = UNSET

    @property
    def validation_status(self) -> str:
        if isinstance(self._validation_status, Unset):
            raise NotPresentError(self, "validation_status")
        return self._validation_status

    @validation_status.setter
    def validation_status(self, value: str) -> None:
        self._validation_status = value

    @validation_status.deleter
    def validation_status(self) -> None:
        self._validation_status = UNSET
