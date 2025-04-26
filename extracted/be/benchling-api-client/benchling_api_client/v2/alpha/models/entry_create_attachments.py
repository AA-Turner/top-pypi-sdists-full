from typing import Any, cast, Dict, List, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError, UnknownType
from ..models.custom_fields import CustomFields
from ..models.entry_create_attachments_review_record import EntryCreateAttachmentsReviewRecord
from ..models.fields import Fields
from ..models.initial_table import InitialTable
from ..types import UNSET, Unset

T = TypeVar("T", bound="EntryCreateAttachments")


@attr.s(auto_attribs=True, repr=False)
class EntryCreateAttachments:
    """  """

    _folder_id: str
    _name: str
    _review_record: Union[Unset, EntryCreateAttachmentsReviewRecord] = UNSET
    _initial_tables: Union[Unset, List[InitialTable]] = UNSET
    _attachment_text: Union[Unset, None] = UNSET
    _attachments: Union[Unset, List[str]] = UNSET
    _author_ids: Union[Unset, str, List[str], UnknownType] = UNSET
    _custom_fields: Union[Unset, CustomFields] = UNSET
    _entry_template_id: Union[Unset, str] = UNSET
    _fields: Union[Unset, Fields] = UNSET
    _schema_id: Union[Unset, str] = UNSET

    def __repr__(self):
        fields = []
        fields.append("folder_id={}".format(repr(self._folder_id)))
        fields.append("name={}".format(repr(self._name)))
        fields.append("review_record={}".format(repr(self._review_record)))
        fields.append("initial_tables={}".format(repr(self._initial_tables)))
        fields.append("attachment_text={}".format(repr(self._attachment_text)))
        fields.append("attachments={}".format(repr(self._attachments)))
        fields.append("author_ids={}".format(repr(self._author_ids)))
        fields.append("custom_fields={}".format(repr(self._custom_fields)))
        fields.append("entry_template_id={}".format(repr(self._entry_template_id)))
        fields.append("fields={}".format(repr(self._fields)))
        fields.append("schema_id={}".format(repr(self._schema_id)))
        return "EntryCreateAttachments({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        folder_id = self._folder_id
        name = self._name
        review_record: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._review_record, Unset):
            review_record = self._review_record.to_dict()

        initial_tables: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._initial_tables, Unset):
            initial_tables = []
            for initial_tables_item_data in self._initial_tables:
                initial_tables_item = initial_tables_item_data.to_dict()

                initial_tables.append(initial_tables_item)

        attachment_text = None

        attachments: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._attachments, Unset):
            attachments = self._attachments

        author_ids: Union[Unset, str, List[Any]]
        if isinstance(self._author_ids, Unset):
            author_ids = UNSET
        elif isinstance(self._author_ids, UnknownType):
            author_ids = self._author_ids.value
        elif isinstance(self._author_ids, list):
            author_ids = UNSET
            if not isinstance(self._author_ids, Unset):
                author_ids = self._author_ids

        else:
            author_ids = self._author_ids

        custom_fields: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._custom_fields, Unset):
            custom_fields = self._custom_fields.to_dict()

        entry_template_id = self._entry_template_id
        fields: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._fields, Unset):
            fields = self._fields.to_dict()

        schema_id = self._schema_id

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if folder_id is not UNSET:
            field_dict["folderId"] = folder_id
        if name is not UNSET:
            field_dict["name"] = name
        if review_record is not UNSET:
            field_dict["reviewRecord"] = review_record
        if initial_tables is not UNSET:
            field_dict["initialTables"] = initial_tables
        if attachment_text is not UNSET:
            field_dict["attachmentText"] = attachment_text
        if attachments is not UNSET:
            field_dict["attachments"] = attachments
        if author_ids is not UNSET:
            field_dict["authorIds"] = author_ids
        if custom_fields is not UNSET:
            field_dict["customFields"] = custom_fields
        if entry_template_id is not UNSET:
            field_dict["entryTemplateId"] = entry_template_id
        if fields is not UNSET:
            field_dict["fields"] = fields
        if schema_id is not UNSET:
            field_dict["schemaId"] = schema_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_folder_id() -> str:
            folder_id = d.pop("folderId")
            return folder_id

        try:
            folder_id = get_folder_id()
        except KeyError:
            if strict:
                raise
            folder_id = cast(str, UNSET)

        def get_name() -> str:
            name = d.pop("name")
            return name

        try:
            name = get_name()
        except KeyError:
            if strict:
                raise
            name = cast(str, UNSET)

        def get_review_record() -> Union[Unset, EntryCreateAttachmentsReviewRecord]:
            review_record: Union[Unset, Union[Unset, EntryCreateAttachmentsReviewRecord]] = UNSET
            _review_record = d.pop("reviewRecord")

            if not isinstance(_review_record, Unset):
                review_record = EntryCreateAttachmentsReviewRecord.from_dict(_review_record)

            return review_record

        try:
            review_record = get_review_record()
        except KeyError:
            if strict:
                raise
            review_record = cast(Union[Unset, EntryCreateAttachmentsReviewRecord], UNSET)

        def get_initial_tables() -> Union[Unset, List[InitialTable]]:
            initial_tables = []
            _initial_tables = d.pop("initialTables")
            for initial_tables_item_data in _initial_tables or []:
                initial_tables_item = InitialTable.from_dict(initial_tables_item_data, strict=False)

                initial_tables.append(initial_tables_item)

            return initial_tables

        try:
            initial_tables = get_initial_tables()
        except KeyError:
            if strict:
                raise
            initial_tables = cast(Union[Unset, List[InitialTable]], UNSET)

        def get_attachment_text() -> Union[Unset, None]:
            attachment_text = None

            return attachment_text

        try:
            attachment_text = get_attachment_text()
        except KeyError:
            if strict:
                raise
            attachment_text = cast(Union[Unset, None], UNSET)

        def get_attachments() -> Union[Unset, List[str]]:
            attachments = cast(List[str], d.pop("attachments"))

            return attachments

        try:
            attachments = get_attachments()
        except KeyError:
            if strict:
                raise
            attachments = cast(Union[Unset, List[str]], UNSET)

        def get_author_ids() -> Union[Unset, str, List[str], UnknownType]:
            def _parse_author_ids(
                data: Union[Unset, str, List[Any]]
            ) -> Union[Unset, str, List[str], UnknownType]:
                author_ids: Union[Unset, str, List[str], UnknownType]
                if isinstance(data, Unset):
                    return data
                try:
                    if not isinstance(data, list):
                        raise TypeError()
                    author_ids = cast(List[str], data)

                    return author_ids
                except:  # noqa: E722
                    pass
                if isinstance(data, dict):
                    return UnknownType(data)
                return cast(Union[Unset, str, List[str], UnknownType], data)

            author_ids = _parse_author_ids(d.pop("authorIds"))

            return author_ids

        try:
            author_ids = get_author_ids()
        except KeyError:
            if strict:
                raise
            author_ids = cast(Union[Unset, str, List[str], UnknownType], UNSET)

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

        def get_entry_template_id() -> Union[Unset, str]:
            entry_template_id = d.pop("entryTemplateId")
            return entry_template_id

        try:
            entry_template_id = get_entry_template_id()
        except KeyError:
            if strict:
                raise
            entry_template_id = cast(Union[Unset, str], UNSET)

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

        def get_schema_id() -> Union[Unset, str]:
            schema_id = d.pop("schemaId")
            return schema_id

        try:
            schema_id = get_schema_id()
        except KeyError:
            if strict:
                raise
            schema_id = cast(Union[Unset, str], UNSET)

        entry_create_attachments = cls(
            folder_id=folder_id,
            name=name,
            review_record=review_record,
            initial_tables=initial_tables,
            attachment_text=attachment_text,
            attachments=attachments,
            author_ids=author_ids,
            custom_fields=custom_fields,
            entry_template_id=entry_template_id,
            fields=fields,
            schema_id=schema_id,
        )

        return entry_create_attachments

    @property
    def folder_id(self) -> str:
        """ ID of the folder that will contain the entry """
        if isinstance(self._folder_id, Unset):
            raise NotPresentError(self, "folder_id")
        return self._folder_id

    @folder_id.setter
    def folder_id(self, value: str) -> None:
        self._folder_id = value

    @property
    def name(self) -> str:
        """ Name of the entry """
        if isinstance(self._name, Unset):
            raise NotPresentError(self, "name")
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def review_record(self) -> EntryCreateAttachmentsReviewRecord:
        if isinstance(self._review_record, Unset):
            raise NotPresentError(self, "review_record")
        return self._review_record

    @review_record.setter
    def review_record(self, value: EntryCreateAttachmentsReviewRecord) -> None:
        self._review_record = value

    @review_record.deleter
    def review_record(self) -> None:
        self._review_record = UNSET

    @property
    def initial_tables(self) -> List[InitialTable]:
        """An array of table API IDs and blob id pairs to seed tables from the template while creating the entry. The entryTemplateId parameter must be set to use this parameter. The table API IDs should be the API Identifiers of the tables in the given template.
        - If a template table has one row, the values in that row act as default values for cloned entries.
        - If a template table has multiple rows, there is no default value and those rows are added to the cloned entry along with the provided csv data.
        - If a table has default values, they will be populated in any respective undefined columns in the csv data.
        - If a table has no default values, undefined columns from csv data will be empty.
        - If no csv data is provided for a table, the table in the entry will be populated with whatever values are in the respective template table.
        """
        if isinstance(self._initial_tables, Unset):
            raise NotPresentError(self, "initial_tables")
        return self._initial_tables

    @initial_tables.setter
    def initial_tables(self, value: List[InitialTable]) -> None:
        self._initial_tables = value

    @initial_tables.deleter
    def initial_tables(self) -> None:
        self._initial_tables = UNSET

    @property
    def attachment_text(self) -> None:
        """Text to include in the entry before the attachments. If not provided, the text will be "File attachments are listed below:" """
        if isinstance(self._attachment_text, Unset):
            raise NotPresentError(self, "attachment_text")
        return self._attachment_text

    @attachment_text.setter
    def attachment_text(self, value: None) -> None:
        self._attachment_text = value

    @attachment_text.deleter
    def attachment_text(self) -> None:
        self._attachment_text = UNSET

    @property
    def attachments(self) -> List[str]:
        """An array of IDs representing Blob objects in Benchling to be attached to the entry."""
        if isinstance(self._attachments, Unset):
            raise NotPresentError(self, "attachments")
        return self._attachments

    @attachments.setter
    def attachments(self, value: List[str]) -> None:
        self._attachments = value

    @attachments.deleter
    def attachments(self) -> None:
        self._attachments = UNSET

    @property
    def author_ids(self) -> Union[str, List[str], UnknownType]:
        if isinstance(self._author_ids, Unset):
            raise NotPresentError(self, "author_ids")
        return self._author_ids

    @author_ids.setter
    def author_ids(self, value: Union[str, List[str], UnknownType]) -> None:
        self._author_ids = value

    @author_ids.deleter
    def author_ids(self) -> None:
        self._author_ids = UNSET

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
    def entry_template_id(self) -> str:
        """ ID of the template to clone the entry from """
        if isinstance(self._entry_template_id, Unset):
            raise NotPresentError(self, "entry_template_id")
        return self._entry_template_id

    @entry_template_id.setter
    def entry_template_id(self, value: str) -> None:
        self._entry_template_id = value

    @entry_template_id.deleter
    def entry_template_id(self) -> None:
        self._entry_template_id = UNSET

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
    def schema_id(self) -> str:
        """ ID of the entry's schema """
        if isinstance(self._schema_id, Unset):
            raise NotPresentError(self, "schema_id")
        return self._schema_id

    @schema_id.setter
    def schema_id(self, value: str) -> None:
        self._schema_id = value

    @schema_id.deleter
    def schema_id(self) -> None:
        self._schema_id = UNSET
