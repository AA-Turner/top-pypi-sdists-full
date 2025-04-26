import datetime
from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..extensions import NotPresentError
from ..models.archive_record import ArchiveRecord
from ..models.constraint_create import ConstraintCreate
from ..models.entity_schema_base_auth_parent_option import EntitySchemaBaseAuthParentOption
from ..models.entity_schema_base_containable_type import EntitySchemaBaseContainableType
from ..models.entity_schema_base_mixture_schema_config import EntitySchemaBaseMixtureSchemaConfig
from ..models.entity_schema_base_type import EntitySchemaBaseType
from ..models.field_create import FieldCreate
from ..models.name_template_part import NameTemplatePart
from ..models.naming_strategy import NamingStrategy
from ..types import UNSET, Unset

T = TypeVar("T", bound="EntitySchema")


@attr.s(auto_attribs=True, repr=False)
class EntitySchema:
    """  """

    _archive_record: Union[Unset, None, ArchiveRecord] = UNSET
    _id: Union[Unset, str] = UNSET
    _modified_at: Union[Unset, datetime.datetime] = UNSET
    _name_template: Union[Unset, List[NameTemplatePart]] = UNSET
    _auth_parent_option: Union[Unset, EntitySchemaBaseAuthParentOption] = UNSET
    _constraint: Union[Unset, None, ConstraintCreate] = UNSET
    _containable_type: Union[Unset, EntitySchemaBaseContainableType] = UNSET
    _fields: Union[Unset, None, List[FieldCreate]] = UNSET
    _include_registry_id_in_chips: Union[Unset, bool] = UNSET
    _is_containable: Union[Unset, bool] = UNSET
    _labeling_strategies: Union[Unset, List[NamingStrategy]] = UNSET
    _mixture_schema_config: Union[Unset, None, EntitySchemaBaseMixtureSchemaConfig] = UNSET
    _name: Union[Unset, str] = UNSET
    _prefix: Union[Unset, str] = UNSET
    _registry_id: Union[Unset, str] = UNSET
    _result_schema_id: Union[Unset, None, str] = UNSET
    _sequence_type: Union[Unset, None, str] = UNSET
    _should_create_as_oligo: Union[Unset, bool] = UNSET
    _should_order_name_parts_by_sequence: Union[Unset, bool] = UNSET
    _show_residues: Union[Unset, bool] = UNSET
    _type: Union[Unset, EntitySchemaBaseType] = UNSET
    _use_organization_collection_alias_for_display_label: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("archive_record={}".format(repr(self._archive_record)))
        fields.append("id={}".format(repr(self._id)))
        fields.append("modified_at={}".format(repr(self._modified_at)))
        fields.append("name_template={}".format(repr(self._name_template)))
        fields.append("auth_parent_option={}".format(repr(self._auth_parent_option)))
        fields.append("constraint={}".format(repr(self._constraint)))
        fields.append("containable_type={}".format(repr(self._containable_type)))
        fields.append("fields={}".format(repr(self._fields)))
        fields.append("include_registry_id_in_chips={}".format(repr(self._include_registry_id_in_chips)))
        fields.append("is_containable={}".format(repr(self._is_containable)))
        fields.append("labeling_strategies={}".format(repr(self._labeling_strategies)))
        fields.append("mixture_schema_config={}".format(repr(self._mixture_schema_config)))
        fields.append("name={}".format(repr(self._name)))
        fields.append("prefix={}".format(repr(self._prefix)))
        fields.append("registry_id={}".format(repr(self._registry_id)))
        fields.append("result_schema_id={}".format(repr(self._result_schema_id)))
        fields.append("sequence_type={}".format(repr(self._sequence_type)))
        fields.append("should_create_as_oligo={}".format(repr(self._should_create_as_oligo)))
        fields.append(
            "should_order_name_parts_by_sequence={}".format(repr(self._should_order_name_parts_by_sequence))
        )
        fields.append("show_residues={}".format(repr(self._show_residues)))
        fields.append("type={}".format(repr(self._type)))
        fields.append(
            "use_organization_collection_alias_for_display_label={}".format(
                repr(self._use_organization_collection_alias_for_display_label)
            )
        )
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "EntitySchema({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        archive_record: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self._archive_record, Unset):
            archive_record = self._archive_record.to_dict() if self._archive_record else None

        id = self._id
        modified_at: Union[Unset, str] = UNSET
        if not isinstance(self._modified_at, Unset):
            modified_at = self._modified_at.isoformat()

        name_template: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._name_template, Unset):
            name_template = []
            for name_template_item_data in self._name_template:
                name_template_item = name_template_item_data.to_dict()

                name_template.append(name_template_item)

        auth_parent_option: Union[Unset, int] = UNSET
        if not isinstance(self._auth_parent_option, Unset):
            auth_parent_option = self._auth_parent_option.value

        constraint: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self._constraint, Unset):
            constraint = self._constraint.to_dict() if self._constraint else None

        containable_type: Union[Unset, int] = UNSET
        if not isinstance(self._containable_type, Unset):
            containable_type = self._containable_type.value

        fields: Union[Unset, None, List[Any]] = UNSET
        if not isinstance(self._fields, Unset):
            if self._fields is None:
                fields = None
            else:
                fields = []
                for fields_item_data in self._fields:
                    fields_item = fields_item_data.to_dict()

                    fields.append(fields_item)

        include_registry_id_in_chips = self._include_registry_id_in_chips
        is_containable = self._is_containable
        labeling_strategies: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._labeling_strategies, Unset):
            labeling_strategies = []
            for labeling_strategies_item_data in self._labeling_strategies:
                labeling_strategies_item = labeling_strategies_item_data.value

                labeling_strategies.append(labeling_strategies_item)

        mixture_schema_config: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self._mixture_schema_config, Unset):
            mixture_schema_config = (
                self._mixture_schema_config.to_dict() if self._mixture_schema_config else None
            )

        name = self._name
        prefix = self._prefix
        registry_id = self._registry_id
        result_schema_id = self._result_schema_id
        sequence_type = self._sequence_type
        should_create_as_oligo = self._should_create_as_oligo
        should_order_name_parts_by_sequence = self._should_order_name_parts_by_sequence
        show_residues = self._show_residues
        type: Union[Unset, int] = UNSET
        if not isinstance(self._type, Unset):
            type = self._type.value

        use_organization_collection_alias_for_display_label = (
            self._use_organization_collection_alias_for_display_label
        )

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if archive_record is not UNSET:
            field_dict["archiveRecord"] = archive_record
        if id is not UNSET:
            field_dict["id"] = id
        if modified_at is not UNSET:
            field_dict["modifiedAt"] = modified_at
        if name_template is not UNSET:
            field_dict["nameTemplate"] = name_template
        if auth_parent_option is not UNSET:
            field_dict["authParentOption"] = auth_parent_option
        if constraint is not UNSET:
            field_dict["constraint"] = constraint
        if containable_type is not UNSET:
            field_dict["containableType"] = containable_type
        if fields is not UNSET:
            field_dict["fields"] = fields
        if include_registry_id_in_chips is not UNSET:
            field_dict["includeRegistryIdInChips"] = include_registry_id_in_chips
        if is_containable is not UNSET:
            field_dict["isContainable"] = is_containable
        if labeling_strategies is not UNSET:
            field_dict["labelingStrategies"] = labeling_strategies
        if mixture_schema_config is not UNSET:
            field_dict["mixtureSchemaConfig"] = mixture_schema_config
        if name is not UNSET:
            field_dict["name"] = name
        if prefix is not UNSET:
            field_dict["prefix"] = prefix
        if registry_id is not UNSET:
            field_dict["registryId"] = registry_id
        if result_schema_id is not UNSET:
            field_dict["resultSchemaId"] = result_schema_id
        if sequence_type is not UNSET:
            field_dict["sequenceType"] = sequence_type
        if should_create_as_oligo is not UNSET:
            field_dict["shouldCreateAsOligo"] = should_create_as_oligo
        if should_order_name_parts_by_sequence is not UNSET:
            field_dict["shouldOrderNamePartsBySequence"] = should_order_name_parts_by_sequence
        if show_residues is not UNSET:
            field_dict["showResidues"] = show_residues
        if type is not UNSET:
            field_dict["type"] = type
        if use_organization_collection_alias_for_display_label is not UNSET:
            field_dict[
                "useOrganizationCollectionAliasForDisplayLabel"
            ] = use_organization_collection_alias_for_display_label

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

        def get_id() -> Union[Unset, str]:
            id = d.pop("id")
            return id

        try:
            id = get_id()
        except KeyError:
            if strict:
                raise
            id = cast(Union[Unset, str], UNSET)

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

        def get_name_template() -> Union[Unset, List[NameTemplatePart]]:
            name_template = []
            _name_template = d.pop("nameTemplate")
            for name_template_item_data in _name_template or []:
                name_template_item = NameTemplatePart.from_dict(name_template_item_data, strict=False)

                name_template.append(name_template_item)

            return name_template

        try:
            name_template = get_name_template()
        except KeyError:
            if strict:
                raise
            name_template = cast(Union[Unset, List[NameTemplatePart]], UNSET)

        def get_auth_parent_option() -> Union[Unset, EntitySchemaBaseAuthParentOption]:
            auth_parent_option = UNSET
            _auth_parent_option = d.pop("authParentOption")
            if _auth_parent_option is not None and _auth_parent_option is not UNSET:
                try:
                    auth_parent_option = EntitySchemaBaseAuthParentOption(_auth_parent_option)
                except ValueError:
                    auth_parent_option = EntitySchemaBaseAuthParentOption.of_unknown(_auth_parent_option)

            return auth_parent_option

        try:
            auth_parent_option = get_auth_parent_option()
        except KeyError:
            if strict:
                raise
            auth_parent_option = cast(Union[Unset, EntitySchemaBaseAuthParentOption], UNSET)

        def get_constraint() -> Union[Unset, None, ConstraintCreate]:
            constraint = None
            _constraint = d.pop("constraint")

            if _constraint is not None and not isinstance(_constraint, Unset):
                constraint = ConstraintCreate.from_dict(_constraint)

            return constraint

        try:
            constraint = get_constraint()
        except KeyError:
            if strict:
                raise
            constraint = cast(Union[Unset, None, ConstraintCreate], UNSET)

        def get_containable_type() -> Union[Unset, EntitySchemaBaseContainableType]:
            containable_type = UNSET
            _containable_type = d.pop("containableType")
            if _containable_type is not None and _containable_type is not UNSET:
                try:
                    containable_type = EntitySchemaBaseContainableType(_containable_type)
                except ValueError:
                    containable_type = EntitySchemaBaseContainableType.of_unknown(_containable_type)

            return containable_type

        try:
            containable_type = get_containable_type()
        except KeyError:
            if strict:
                raise
            containable_type = cast(Union[Unset, EntitySchemaBaseContainableType], UNSET)

        def get_fields() -> Union[Unset, None, List[FieldCreate]]:
            fields = []
            _fields = d.pop("fields")
            for fields_item_data in _fields or []:
                fields_item = FieldCreate.from_dict(fields_item_data, strict=False)

                fields.append(fields_item)

            return fields

        try:
            fields = get_fields()
        except KeyError:
            if strict:
                raise
            fields = cast(Union[Unset, None, List[FieldCreate]], UNSET)

        def get_include_registry_id_in_chips() -> Union[Unset, bool]:
            include_registry_id_in_chips = d.pop("includeRegistryIdInChips")
            return include_registry_id_in_chips

        try:
            include_registry_id_in_chips = get_include_registry_id_in_chips()
        except KeyError:
            if strict:
                raise
            include_registry_id_in_chips = cast(Union[Unset, bool], UNSET)

        def get_is_containable() -> Union[Unset, bool]:
            is_containable = d.pop("isContainable")
            return is_containable

        try:
            is_containable = get_is_containable()
        except KeyError:
            if strict:
                raise
            is_containable = cast(Union[Unset, bool], UNSET)

        def get_labeling_strategies() -> Union[Unset, List[NamingStrategy]]:
            labeling_strategies = []
            _labeling_strategies = d.pop("labelingStrategies")
            for labeling_strategies_item_data in _labeling_strategies or []:
                _labeling_strategies_item = labeling_strategies_item_data
                try:
                    labeling_strategies_item = NamingStrategy(_labeling_strategies_item)
                except ValueError:
                    labeling_strategies_item = NamingStrategy.of_unknown(_labeling_strategies_item)

                labeling_strategies.append(labeling_strategies_item)

            return labeling_strategies

        try:
            labeling_strategies = get_labeling_strategies()
        except KeyError:
            if strict:
                raise
            labeling_strategies = cast(Union[Unset, List[NamingStrategy]], UNSET)

        def get_mixture_schema_config() -> Union[Unset, None, EntitySchemaBaseMixtureSchemaConfig]:
            mixture_schema_config = None
            _mixture_schema_config = d.pop("mixtureSchemaConfig")

            if _mixture_schema_config is not None and not isinstance(_mixture_schema_config, Unset):
                mixture_schema_config = EntitySchemaBaseMixtureSchemaConfig.from_dict(_mixture_schema_config)

            return mixture_schema_config

        try:
            mixture_schema_config = get_mixture_schema_config()
        except KeyError:
            if strict:
                raise
            mixture_schema_config = cast(Union[Unset, None, EntitySchemaBaseMixtureSchemaConfig], UNSET)

        def get_name() -> Union[Unset, str]:
            name = d.pop("name")
            return name

        try:
            name = get_name()
        except KeyError:
            if strict:
                raise
            name = cast(Union[Unset, str], UNSET)

        def get_prefix() -> Union[Unset, str]:
            prefix = d.pop("prefix")
            return prefix

        try:
            prefix = get_prefix()
        except KeyError:
            if strict:
                raise
            prefix = cast(Union[Unset, str], UNSET)

        def get_registry_id() -> Union[Unset, str]:
            registry_id = d.pop("registryId")
            return registry_id

        try:
            registry_id = get_registry_id()
        except KeyError:
            if strict:
                raise
            registry_id = cast(Union[Unset, str], UNSET)

        def get_result_schema_id() -> Union[Unset, None, str]:
            result_schema_id = d.pop("resultSchemaId")
            return result_schema_id

        try:
            result_schema_id = get_result_schema_id()
        except KeyError:
            if strict:
                raise
            result_schema_id = cast(Union[Unset, None, str], UNSET)

        def get_sequence_type() -> Union[Unset, None, str]:
            sequence_type = d.pop("sequenceType")
            return sequence_type

        try:
            sequence_type = get_sequence_type()
        except KeyError:
            if strict:
                raise
            sequence_type = cast(Union[Unset, None, str], UNSET)

        def get_should_create_as_oligo() -> Union[Unset, bool]:
            should_create_as_oligo = d.pop("shouldCreateAsOligo")
            return should_create_as_oligo

        try:
            should_create_as_oligo = get_should_create_as_oligo()
        except KeyError:
            if strict:
                raise
            should_create_as_oligo = cast(Union[Unset, bool], UNSET)

        def get_should_order_name_parts_by_sequence() -> Union[Unset, bool]:
            should_order_name_parts_by_sequence = d.pop("shouldOrderNamePartsBySequence")
            return should_order_name_parts_by_sequence

        try:
            should_order_name_parts_by_sequence = get_should_order_name_parts_by_sequence()
        except KeyError:
            if strict:
                raise
            should_order_name_parts_by_sequence = cast(Union[Unset, bool], UNSET)

        def get_show_residues() -> Union[Unset, bool]:
            show_residues = d.pop("showResidues")
            return show_residues

        try:
            show_residues = get_show_residues()
        except KeyError:
            if strict:
                raise
            show_residues = cast(Union[Unset, bool], UNSET)

        def get_type() -> Union[Unset, EntitySchemaBaseType]:
            type = UNSET
            _type = d.pop("type")
            if _type is not None and _type is not UNSET:
                try:
                    type = EntitySchemaBaseType(_type)
                except ValueError:
                    type = EntitySchemaBaseType.of_unknown(_type)

            return type

        try:
            type = get_type()
        except KeyError:
            if strict:
                raise
            type = cast(Union[Unset, EntitySchemaBaseType], UNSET)

        def get_use_organization_collection_alias_for_display_label() -> Union[Unset, bool]:
            use_organization_collection_alias_for_display_label = d.pop(
                "useOrganizationCollectionAliasForDisplayLabel"
            )
            return use_organization_collection_alias_for_display_label

        try:
            use_organization_collection_alias_for_display_label = (
                get_use_organization_collection_alias_for_display_label()
            )
        except KeyError:
            if strict:
                raise
            use_organization_collection_alias_for_display_label = cast(Union[Unset, bool], UNSET)

        entity_schema = cls(
            archive_record=archive_record,
            id=id,
            modified_at=modified_at,
            name_template=name_template,
            auth_parent_option=auth_parent_option,
            constraint=constraint,
            containable_type=containable_type,
            fields=fields,
            include_registry_id_in_chips=include_registry_id_in_chips,
            is_containable=is_containable,
            labeling_strategies=labeling_strategies,
            mixture_schema_config=mixture_schema_config,
            name=name,
            prefix=prefix,
            registry_id=registry_id,
            result_schema_id=result_schema_id,
            sequence_type=sequence_type,
            should_create_as_oligo=should_create_as_oligo,
            should_order_name_parts_by_sequence=should_order_name_parts_by_sequence,
            show_residues=show_residues,
            type=type,
            use_organization_collection_alias_for_display_label=use_organization_collection_alias_for_display_label,
        )

        entity_schema.additional_properties = d
        return entity_schema

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
    def modified_at(self) -> datetime.datetime:
        """ DateTime the Entity Schema was last modified """
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
    def name_template(self) -> List[NameTemplatePart]:
        if isinstance(self._name_template, Unset):
            raise NotPresentError(self, "name_template")
        return self._name_template

    @name_template.setter
    def name_template(self, value: List[NameTemplatePart]) -> None:
        self._name_template = value

    @name_template.deleter
    def name_template(self) -> None:
        self._name_template = UNSET

    @property
    def auth_parent_option(self) -> EntitySchemaBaseAuthParentOption:
        if isinstance(self._auth_parent_option, Unset):
            raise NotPresentError(self, "auth_parent_option")
        return self._auth_parent_option

    @auth_parent_option.setter
    def auth_parent_option(self, value: EntitySchemaBaseAuthParentOption) -> None:
        self._auth_parent_option = value

    @auth_parent_option.deleter
    def auth_parent_option(self) -> None:
        self._auth_parent_option = UNSET

    @property
    def constraint(self) -> Optional[ConstraintCreate]:
        if isinstance(self._constraint, Unset):
            raise NotPresentError(self, "constraint")
        return self._constraint

    @constraint.setter
    def constraint(self, value: Optional[ConstraintCreate]) -> None:
        self._constraint = value

    @constraint.deleter
    def constraint(self) -> None:
        self._constraint = UNSET

    @property
    def containable_type(self) -> EntitySchemaBaseContainableType:
        if isinstance(self._containable_type, Unset):
            raise NotPresentError(self, "containable_type")
        return self._containable_type

    @containable_type.setter
    def containable_type(self, value: EntitySchemaBaseContainableType) -> None:
        self._containable_type = value

    @containable_type.deleter
    def containable_type(self) -> None:
        self._containable_type = UNSET

    @property
    def fields(self) -> Optional[List[FieldCreate]]:
        if isinstance(self._fields, Unset):
            raise NotPresentError(self, "fields")
        return self._fields

    @fields.setter
    def fields(self, value: Optional[List[FieldCreate]]) -> None:
        self._fields = value

    @fields.deleter
    def fields(self) -> None:
        self._fields = UNSET

    @property
    def include_registry_id_in_chips(self) -> bool:
        if isinstance(self._include_registry_id_in_chips, Unset):
            raise NotPresentError(self, "include_registry_id_in_chips")
        return self._include_registry_id_in_chips

    @include_registry_id_in_chips.setter
    def include_registry_id_in_chips(self, value: bool) -> None:
        self._include_registry_id_in_chips = value

    @include_registry_id_in_chips.deleter
    def include_registry_id_in_chips(self) -> None:
        self._include_registry_id_in_chips = UNSET

    @property
    def is_containable(self) -> bool:
        if isinstance(self._is_containable, Unset):
            raise NotPresentError(self, "is_containable")
        return self._is_containable

    @is_containable.setter
    def is_containable(self, value: bool) -> None:
        self._is_containable = value

    @is_containable.deleter
    def is_containable(self) -> None:
        self._is_containable = UNSET

    @property
    def labeling_strategies(self) -> List[NamingStrategy]:
        if isinstance(self._labeling_strategies, Unset):
            raise NotPresentError(self, "labeling_strategies")
        return self._labeling_strategies

    @labeling_strategies.setter
    def labeling_strategies(self, value: List[NamingStrategy]) -> None:
        self._labeling_strategies = value

    @labeling_strategies.deleter
    def labeling_strategies(self) -> None:
        self._labeling_strategies = UNSET

    @property
    def mixture_schema_config(self) -> Optional[EntitySchemaBaseMixtureSchemaConfig]:
        if isinstance(self._mixture_schema_config, Unset):
            raise NotPresentError(self, "mixture_schema_config")
        return self._mixture_schema_config

    @mixture_schema_config.setter
    def mixture_schema_config(self, value: Optional[EntitySchemaBaseMixtureSchemaConfig]) -> None:
        self._mixture_schema_config = value

    @mixture_schema_config.deleter
    def mixture_schema_config(self) -> None:
        self._mixture_schema_config = UNSET

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
    def prefix(self) -> str:
        if isinstance(self._prefix, Unset):
            raise NotPresentError(self, "prefix")
        return self._prefix

    @prefix.setter
    def prefix(self, value: str) -> None:
        self._prefix = value

    @prefix.deleter
    def prefix(self) -> None:
        self._prefix = UNSET

    @property
    def registry_id(self) -> str:
        if isinstance(self._registry_id, Unset):
            raise NotPresentError(self, "registry_id")
        return self._registry_id

    @registry_id.setter
    def registry_id(self, value: str) -> None:
        self._registry_id = value

    @registry_id.deleter
    def registry_id(self) -> None:
        self._registry_id = UNSET

    @property
    def result_schema_id(self) -> Optional[str]:
        if isinstance(self._result_schema_id, Unset):
            raise NotPresentError(self, "result_schema_id")
        return self._result_schema_id

    @result_schema_id.setter
    def result_schema_id(self, value: Optional[str]) -> None:
        self._result_schema_id = value

    @result_schema_id.deleter
    def result_schema_id(self) -> None:
        self._result_schema_id = UNSET

    @property
    def sequence_type(self) -> Optional[str]:
        if isinstance(self._sequence_type, Unset):
            raise NotPresentError(self, "sequence_type")
        return self._sequence_type

    @sequence_type.setter
    def sequence_type(self, value: Optional[str]) -> None:
        self._sequence_type = value

    @sequence_type.deleter
    def sequence_type(self) -> None:
        self._sequence_type = UNSET

    @property
    def should_create_as_oligo(self) -> bool:
        if isinstance(self._should_create_as_oligo, Unset):
            raise NotPresentError(self, "should_create_as_oligo")
        return self._should_create_as_oligo

    @should_create_as_oligo.setter
    def should_create_as_oligo(self, value: bool) -> None:
        self._should_create_as_oligo = value

    @should_create_as_oligo.deleter
    def should_create_as_oligo(self) -> None:
        self._should_create_as_oligo = UNSET

    @property
    def should_order_name_parts_by_sequence(self) -> bool:
        if isinstance(self._should_order_name_parts_by_sequence, Unset):
            raise NotPresentError(self, "should_order_name_parts_by_sequence")
        return self._should_order_name_parts_by_sequence

    @should_order_name_parts_by_sequence.setter
    def should_order_name_parts_by_sequence(self, value: bool) -> None:
        self._should_order_name_parts_by_sequence = value

    @should_order_name_parts_by_sequence.deleter
    def should_order_name_parts_by_sequence(self) -> None:
        self._should_order_name_parts_by_sequence = UNSET

    @property
    def show_residues(self) -> bool:
        if isinstance(self._show_residues, Unset):
            raise NotPresentError(self, "show_residues")
        return self._show_residues

    @show_residues.setter
    def show_residues(self, value: bool) -> None:
        self._show_residues = value

    @show_residues.deleter
    def show_residues(self) -> None:
        self._show_residues = UNSET

    @property
    def type(self) -> EntitySchemaBaseType:
        if isinstance(self._type, Unset):
            raise NotPresentError(self, "type")
        return self._type

    @type.setter
    def type(self, value: EntitySchemaBaseType) -> None:
        self._type = value

    @type.deleter
    def type(self) -> None:
        self._type = UNSET

    @property
    def use_organization_collection_alias_for_display_label(self) -> bool:
        if isinstance(self._use_organization_collection_alias_for_display_label, Unset):
            raise NotPresentError(self, "use_organization_collection_alias_for_display_label")
        return self._use_organization_collection_alias_for_display_label

    @use_organization_collection_alias_for_display_label.setter
    def use_organization_collection_alias_for_display_label(self, value: bool) -> None:
        self._use_organization_collection_alias_for_display_label = value

    @use_organization_collection_alias_for_display_label.deleter
    def use_organization_collection_alias_for_display_label(self) -> None:
        self._use_organization_collection_alias_for_display_label = UNSET
