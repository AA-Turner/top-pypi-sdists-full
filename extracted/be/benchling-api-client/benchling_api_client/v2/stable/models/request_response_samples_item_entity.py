import datetime
from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..extensions import NotPresentError
from ..models.archive_record import ArchiveRecord
from ..models.custom_fields import CustomFields
from ..models.dna_annotation import DnaAnnotation
from ..models.dna_sequence_part import DnaSequencePart
from ..models.fields import Fields
from ..models.inaccessible_resource_resource_type import InaccessibleResourceResourceType
from ..models.ingredient import Ingredient
from ..models.mixture_measurement_units import MixtureMeasurementUnits
from ..models.oligo_nucleotide_type import OligoNucleotideType
from ..models.primer import Primer
from ..models.registration_origin import RegistrationOrigin
from ..models.schema_summary import SchemaSummary
from ..models.translation import Translation
from ..models.user_summary import UserSummary
from ..types import UNSET, Unset

T = TypeVar("T", bound="RequestResponseSamplesItemEntity")


@attr.s(auto_attribs=True, repr=False)
class RequestResponseSamplesItemEntity:
    """  """

    _inaccessible_id: Union[Unset, str] = UNSET
    _resource_type: Union[Unset, InaccessibleResourceResourceType] = UNSET
    _type: Union[Unset, str] = UNSET
    _aliases: Union[Unset, List[str]] = UNSET
    _api_url: Union[Unset, str] = UNSET
    _archive_record: Union[Unset, None, ArchiveRecord] = UNSET
    _authors: Union[Unset, List[UserSummary]] = UNSET
    _created_at: Union[Unset, datetime.datetime] = UNSET
    _creator: Union[Unset, UserSummary] = UNSET
    _custom_fields: Union[Unset, CustomFields] = UNSET
    _entity_registry_id: Union[Unset, None, str] = UNSET
    _fields: Union[Unset, Fields] = UNSET
    _folder_id: Union[Unset, None, str] = UNSET
    _id: Union[Unset, str] = UNSET
    _modified_at: Union[Unset, datetime.datetime] = UNSET
    _name: Union[Unset, str] = UNSET
    _registration_origin: Union[Unset, None, RegistrationOrigin] = UNSET
    _registry_id: Union[Unset, None, str] = UNSET
    _schema: Union[Unset, None, SchemaSummary] = UNSET
    _web_url: Union[Unset, str] = UNSET
    _annotations: Union[Unset, List[DnaAnnotation]] = UNSET
    _bases: Union[Unset, str] = UNSET
    _custom_notation: Union[Unset, None, str] = UNSET
    _custom_notation_name: Union[Unset, None, str] = UNSET
    _helm: Union[Unset, str] = UNSET
    _nucleotide_type: Union[Unset, OligoNucleotideType] = UNSET
    _length: Union[Unset, int] = UNSET
    _allow_measured_ingredients: Union[Unset, bool] = UNSET
    _amount: Union[Unset, str] = UNSET
    _ingredients: Union[Unset, List[Ingredient]] = UNSET
    _units: Union[Unset, MixtureMeasurementUnits] = UNSET
    _amino_acids: Union[Unset, str] = UNSET
    _is_circular: Union[Unset, bool] = UNSET
    _parts: Union[Unset, List[DnaSequencePart]] = UNSET
    _primers: Union[Unset, List[Primer]] = UNSET
    _translations: Union[Unset, List[Translation]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("inaccessible_id={}".format(repr(self._inaccessible_id)))
        fields.append("resource_type={}".format(repr(self._resource_type)))
        fields.append("type={}".format(repr(self._type)))
        fields.append("aliases={}".format(repr(self._aliases)))
        fields.append("api_url={}".format(repr(self._api_url)))
        fields.append("archive_record={}".format(repr(self._archive_record)))
        fields.append("authors={}".format(repr(self._authors)))
        fields.append("created_at={}".format(repr(self._created_at)))
        fields.append("creator={}".format(repr(self._creator)))
        fields.append("custom_fields={}".format(repr(self._custom_fields)))
        fields.append("entity_registry_id={}".format(repr(self._entity_registry_id)))
        fields.append("fields={}".format(repr(self._fields)))
        fields.append("folder_id={}".format(repr(self._folder_id)))
        fields.append("id={}".format(repr(self._id)))
        fields.append("modified_at={}".format(repr(self._modified_at)))
        fields.append("name={}".format(repr(self._name)))
        fields.append("registration_origin={}".format(repr(self._registration_origin)))
        fields.append("registry_id={}".format(repr(self._registry_id)))
        fields.append("schema={}".format(repr(self._schema)))
        fields.append("web_url={}".format(repr(self._web_url)))
        fields.append("annotations={}".format(repr(self._annotations)))
        fields.append("bases={}".format(repr(self._bases)))
        fields.append("custom_notation={}".format(repr(self._custom_notation)))
        fields.append("custom_notation_name={}".format(repr(self._custom_notation_name)))
        fields.append("helm={}".format(repr(self._helm)))
        fields.append("nucleotide_type={}".format(repr(self._nucleotide_type)))
        fields.append("length={}".format(repr(self._length)))
        fields.append("allow_measured_ingredients={}".format(repr(self._allow_measured_ingredients)))
        fields.append("amount={}".format(repr(self._amount)))
        fields.append("ingredients={}".format(repr(self._ingredients)))
        fields.append("units={}".format(repr(self._units)))
        fields.append("amino_acids={}".format(repr(self._amino_acids)))
        fields.append("is_circular={}".format(repr(self._is_circular)))
        fields.append("parts={}".format(repr(self._parts)))
        fields.append("primers={}".format(repr(self._primers)))
        fields.append("translations={}".format(repr(self._translations)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "RequestResponseSamplesItemEntity({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        inaccessible_id = self._inaccessible_id
        resource_type: Union[Unset, int] = UNSET
        if not isinstance(self._resource_type, Unset):
            resource_type = self._resource_type.value

        type = self._type
        aliases: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._aliases, Unset):
            aliases = self._aliases

        api_url = self._api_url
        archive_record: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self._archive_record, Unset):
            archive_record = self._archive_record.to_dict() if self._archive_record else None

        authors: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._authors, Unset):
            authors = []
            for authors_item_data in self._authors:
                authors_item = authors_item_data.to_dict()

                authors.append(authors_item)

        created_at: Union[Unset, str] = UNSET
        if not isinstance(self._created_at, Unset):
            created_at = self._created_at.isoformat()

        creator: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._creator, Unset):
            creator = self._creator.to_dict()

        custom_fields: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._custom_fields, Unset):
            custom_fields = self._custom_fields.to_dict()

        entity_registry_id = self._entity_registry_id
        fields: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._fields, Unset):
            fields = self._fields.to_dict()

        folder_id = self._folder_id
        id = self._id
        modified_at: Union[Unset, str] = UNSET
        if not isinstance(self._modified_at, Unset):
            modified_at = self._modified_at.isoformat()

        name = self._name
        registration_origin: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self._registration_origin, Unset):
            registration_origin = self._registration_origin.to_dict() if self._registration_origin else None

        registry_id = self._registry_id
        schema: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self._schema, Unset):
            schema = self._schema.to_dict() if self._schema else None

        web_url = self._web_url
        annotations: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._annotations, Unset):
            annotations = []
            for annotations_item_data in self._annotations:
                annotations_item = annotations_item_data.to_dict()

                annotations.append(annotations_item)

        bases = self._bases
        custom_notation = self._custom_notation
        custom_notation_name = self._custom_notation_name
        helm = self._helm
        nucleotide_type: Union[Unset, int] = UNSET
        if not isinstance(self._nucleotide_type, Unset):
            nucleotide_type = self._nucleotide_type.value

        length = self._length
        allow_measured_ingredients = self._allow_measured_ingredients
        amount = self._amount
        ingredients: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._ingredients, Unset):
            ingredients = []
            for ingredients_item_data in self._ingredients:
                ingredients_item = ingredients_item_data.to_dict()

                ingredients.append(ingredients_item)

        units: Union[Unset, int] = UNSET
        if not isinstance(self._units, Unset):
            units = self._units.value

        amino_acids = self._amino_acids
        is_circular = self._is_circular
        parts: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._parts, Unset):
            parts = []
            for parts_item_data in self._parts:
                parts_item = parts_item_data.to_dict()

                parts.append(parts_item)

        primers: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._primers, Unset):
            primers = []
            for primers_item_data in self._primers:
                primers_item = primers_item_data.to_dict()

                primers.append(primers_item)

        translations: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._translations, Unset):
            translations = []
            for translations_item_data in self._translations:
                translations_item = translations_item_data.to_dict()

                translations.append(translations_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if inaccessible_id is not UNSET:
            field_dict["inaccessibleId"] = inaccessible_id
        if resource_type is not UNSET:
            field_dict["resourceType"] = resource_type
        if type is not UNSET:
            field_dict["type"] = type
        if aliases is not UNSET:
            field_dict["aliases"] = aliases
        if api_url is not UNSET:
            field_dict["apiURL"] = api_url
        if archive_record is not UNSET:
            field_dict["archiveRecord"] = archive_record
        if authors is not UNSET:
            field_dict["authors"] = authors
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if creator is not UNSET:
            field_dict["creator"] = creator
        if custom_fields is not UNSET:
            field_dict["customFields"] = custom_fields
        if entity_registry_id is not UNSET:
            field_dict["entityRegistryId"] = entity_registry_id
        if fields is not UNSET:
            field_dict["fields"] = fields
        if folder_id is not UNSET:
            field_dict["folderId"] = folder_id
        if id is not UNSET:
            field_dict["id"] = id
        if modified_at is not UNSET:
            field_dict["modifiedAt"] = modified_at
        if name is not UNSET:
            field_dict["name"] = name
        if registration_origin is not UNSET:
            field_dict["registrationOrigin"] = registration_origin
        if registry_id is not UNSET:
            field_dict["registryId"] = registry_id
        if schema is not UNSET:
            field_dict["schema"] = schema
        if web_url is not UNSET:
            field_dict["webURL"] = web_url
        if annotations is not UNSET:
            field_dict["annotations"] = annotations
        if bases is not UNSET:
            field_dict["bases"] = bases
        if custom_notation is not UNSET:
            field_dict["customNotation"] = custom_notation
        if custom_notation_name is not UNSET:
            field_dict["customNotationName"] = custom_notation_name
        if helm is not UNSET:
            field_dict["helm"] = helm
        if nucleotide_type is not UNSET:
            field_dict["nucleotideType"] = nucleotide_type
        if length is not UNSET:
            field_dict["length"] = length
        if allow_measured_ingredients is not UNSET:
            field_dict["allowMeasuredIngredients"] = allow_measured_ingredients
        if amount is not UNSET:
            field_dict["amount"] = amount
        if ingredients is not UNSET:
            field_dict["ingredients"] = ingredients
        if units is not UNSET:
            field_dict["units"] = units
        if amino_acids is not UNSET:
            field_dict["aminoAcids"] = amino_acids
        if is_circular is not UNSET:
            field_dict["isCircular"] = is_circular
        if parts is not UNSET:
            field_dict["parts"] = parts
        if primers is not UNSET:
            field_dict["primers"] = primers
        if translations is not UNSET:
            field_dict["translations"] = translations

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_inaccessible_id() -> Union[Unset, str]:
            inaccessible_id = d.pop("inaccessibleId")
            return inaccessible_id

        try:
            inaccessible_id = get_inaccessible_id()
        except KeyError:
            if strict:
                raise
            inaccessible_id = cast(Union[Unset, str], UNSET)

        def get_resource_type() -> Union[Unset, InaccessibleResourceResourceType]:
            resource_type = UNSET
            _resource_type = d.pop("resourceType")
            if _resource_type is not None and _resource_type is not UNSET:
                try:
                    resource_type = InaccessibleResourceResourceType(_resource_type)
                except ValueError:
                    resource_type = InaccessibleResourceResourceType.of_unknown(_resource_type)

            return resource_type

        try:
            resource_type = get_resource_type()
        except KeyError:
            if strict:
                raise
            resource_type = cast(Union[Unset, InaccessibleResourceResourceType], UNSET)

        def get_type() -> Union[Unset, str]:
            type = d.pop("type")
            return type

        try:
            type = get_type()
        except KeyError:
            if strict:
                raise
            type = cast(Union[Unset, str], UNSET)

        def get_aliases() -> Union[Unset, List[str]]:
            aliases = cast(List[str], d.pop("aliases"))

            return aliases

        try:
            aliases = get_aliases()
        except KeyError:
            if strict:
                raise
            aliases = cast(Union[Unset, List[str]], UNSET)

        def get_api_url() -> Union[Unset, str]:
            api_url = d.pop("apiURL")
            return api_url

        try:
            api_url = get_api_url()
        except KeyError:
            if strict:
                raise
            api_url = cast(Union[Unset, str], UNSET)

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

        def get_authors() -> Union[Unset, List[UserSummary]]:
            authors = []
            _authors = d.pop("authors")
            for authors_item_data in _authors or []:
                authors_item = UserSummary.from_dict(authors_item_data, strict=False)

                authors.append(authors_item)

            return authors

        try:
            authors = get_authors()
        except KeyError:
            if strict:
                raise
            authors = cast(Union[Unset, List[UserSummary]], UNSET)

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

        def get_entity_registry_id() -> Union[Unset, None, str]:
            entity_registry_id = d.pop("entityRegistryId")
            return entity_registry_id

        try:
            entity_registry_id = get_entity_registry_id()
        except KeyError:
            if strict:
                raise
            entity_registry_id = cast(Union[Unset, None, str], UNSET)

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

        def get_folder_id() -> Union[Unset, None, str]:
            folder_id = d.pop("folderId")
            return folder_id

        try:
            folder_id = get_folder_id()
        except KeyError:
            if strict:
                raise
            folder_id = cast(Union[Unset, None, str], UNSET)

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

        def get_name() -> Union[Unset, str]:
            name = d.pop("name")
            return name

        try:
            name = get_name()
        except KeyError:
            if strict:
                raise
            name = cast(Union[Unset, str], UNSET)

        def get_registration_origin() -> Union[Unset, None, RegistrationOrigin]:
            registration_origin = None
            _registration_origin = d.pop("registrationOrigin")

            if _registration_origin is not None and not isinstance(_registration_origin, Unset):
                registration_origin = RegistrationOrigin.from_dict(_registration_origin)

            return registration_origin

        try:
            registration_origin = get_registration_origin()
        except KeyError:
            if strict:
                raise
            registration_origin = cast(Union[Unset, None, RegistrationOrigin], UNSET)

        def get_registry_id() -> Union[Unset, None, str]:
            registry_id = d.pop("registryId")
            return registry_id

        try:
            registry_id = get_registry_id()
        except KeyError:
            if strict:
                raise
            registry_id = cast(Union[Unset, None, str], UNSET)

        def get_schema() -> Union[Unset, None, SchemaSummary]:
            schema = None
            _schema = d.pop("schema")

            if _schema is not None and not isinstance(_schema, Unset):
                schema = SchemaSummary.from_dict(_schema)

            return schema

        try:
            schema = get_schema()
        except KeyError:
            if strict:
                raise
            schema = cast(Union[Unset, None, SchemaSummary], UNSET)

        def get_web_url() -> Union[Unset, str]:
            web_url = d.pop("webURL")
            return web_url

        try:
            web_url = get_web_url()
        except KeyError:
            if strict:
                raise
            web_url = cast(Union[Unset, str], UNSET)

        def get_annotations() -> Union[Unset, List[DnaAnnotation]]:
            annotations = []
            _annotations = d.pop("annotations")
            for annotations_item_data in _annotations or []:
                annotations_item = DnaAnnotation.from_dict(annotations_item_data, strict=False)

                annotations.append(annotations_item)

            return annotations

        try:
            annotations = get_annotations()
        except KeyError:
            if strict:
                raise
            annotations = cast(Union[Unset, List[DnaAnnotation]], UNSET)

        def get_bases() -> Union[Unset, str]:
            bases = d.pop("bases")
            return bases

        try:
            bases = get_bases()
        except KeyError:
            if strict:
                raise
            bases = cast(Union[Unset, str], UNSET)

        def get_custom_notation() -> Union[Unset, None, str]:
            custom_notation = d.pop("customNotation")
            return custom_notation

        try:
            custom_notation = get_custom_notation()
        except KeyError:
            if strict:
                raise
            custom_notation = cast(Union[Unset, None, str], UNSET)

        def get_custom_notation_name() -> Union[Unset, None, str]:
            custom_notation_name = d.pop("customNotationName")
            return custom_notation_name

        try:
            custom_notation_name = get_custom_notation_name()
        except KeyError:
            if strict:
                raise
            custom_notation_name = cast(Union[Unset, None, str], UNSET)

        def get_helm() -> Union[Unset, str]:
            helm = d.pop("helm")
            return helm

        try:
            helm = get_helm()
        except KeyError:
            if strict:
                raise
            helm = cast(Union[Unset, str], UNSET)

        def get_nucleotide_type() -> Union[Unset, OligoNucleotideType]:
            nucleotide_type = UNSET
            _nucleotide_type = d.pop("nucleotideType")
            if _nucleotide_type is not None and _nucleotide_type is not UNSET:
                try:
                    nucleotide_type = OligoNucleotideType(_nucleotide_type)
                except ValueError:
                    nucleotide_type = OligoNucleotideType.of_unknown(_nucleotide_type)

            return nucleotide_type

        try:
            nucleotide_type = get_nucleotide_type()
        except KeyError:
            if strict:
                raise
            nucleotide_type = cast(Union[Unset, OligoNucleotideType], UNSET)

        def get_length() -> Union[Unset, int]:
            length = d.pop("length")
            return length

        try:
            length = get_length()
        except KeyError:
            if strict:
                raise
            length = cast(Union[Unset, int], UNSET)

        def get_allow_measured_ingredients() -> Union[Unset, bool]:
            allow_measured_ingredients = d.pop("allowMeasuredIngredients")
            return allow_measured_ingredients

        try:
            allow_measured_ingredients = get_allow_measured_ingredients()
        except KeyError:
            if strict:
                raise
            allow_measured_ingredients = cast(Union[Unset, bool], UNSET)

        def get_amount() -> Union[Unset, str]:
            amount = d.pop("amount")
            return amount

        try:
            amount = get_amount()
        except KeyError:
            if strict:
                raise
            amount = cast(Union[Unset, str], UNSET)

        def get_ingredients() -> Union[Unset, List[Ingredient]]:
            ingredients = []
            _ingredients = d.pop("ingredients")
            for ingredients_item_data in _ingredients or []:
                ingredients_item = Ingredient.from_dict(ingredients_item_data, strict=False)

                ingredients.append(ingredients_item)

            return ingredients

        try:
            ingredients = get_ingredients()
        except KeyError:
            if strict:
                raise
            ingredients = cast(Union[Unset, List[Ingredient]], UNSET)

        def get_units() -> Union[Unset, MixtureMeasurementUnits]:
            units = UNSET
            _units = d.pop("units")
            if _units is not None and _units is not UNSET:
                try:
                    units = MixtureMeasurementUnits(_units)
                except ValueError:
                    units = MixtureMeasurementUnits.of_unknown(_units)

            return units

        try:
            units = get_units()
        except KeyError:
            if strict:
                raise
            units = cast(Union[Unset, MixtureMeasurementUnits], UNSET)

        def get_amino_acids() -> Union[Unset, str]:
            amino_acids = d.pop("aminoAcids")
            return amino_acids

        try:
            amino_acids = get_amino_acids()
        except KeyError:
            if strict:
                raise
            amino_acids = cast(Union[Unset, str], UNSET)

        def get_is_circular() -> Union[Unset, bool]:
            is_circular = d.pop("isCircular")
            return is_circular

        try:
            is_circular = get_is_circular()
        except KeyError:
            if strict:
                raise
            is_circular = cast(Union[Unset, bool], UNSET)

        def get_parts() -> Union[Unset, List[DnaSequencePart]]:
            parts = []
            _parts = d.pop("parts")
            for parts_item_data in _parts or []:
                parts_item = DnaSequencePart.from_dict(parts_item_data, strict=False)

                parts.append(parts_item)

            return parts

        try:
            parts = get_parts()
        except KeyError:
            if strict:
                raise
            parts = cast(Union[Unset, List[DnaSequencePart]], UNSET)

        def get_primers() -> Union[Unset, List[Primer]]:
            primers = []
            _primers = d.pop("primers")
            for primers_item_data in _primers or []:
                primers_item = Primer.from_dict(primers_item_data, strict=False)

                primers.append(primers_item)

            return primers

        try:
            primers = get_primers()
        except KeyError:
            if strict:
                raise
            primers = cast(Union[Unset, List[Primer]], UNSET)

        def get_translations() -> Union[Unset, List[Translation]]:
            translations = []
            _translations = d.pop("translations")
            for translations_item_data in _translations or []:
                translations_item = Translation.from_dict(translations_item_data, strict=False)

                translations.append(translations_item)

            return translations

        try:
            translations = get_translations()
        except KeyError:
            if strict:
                raise
            translations = cast(Union[Unset, List[Translation]], UNSET)

        request_response_samples_item_entity = cls(
            inaccessible_id=inaccessible_id,
            resource_type=resource_type,
            type=type,
            aliases=aliases,
            api_url=api_url,
            archive_record=archive_record,
            authors=authors,
            created_at=created_at,
            creator=creator,
            custom_fields=custom_fields,
            entity_registry_id=entity_registry_id,
            fields=fields,
            folder_id=folder_id,
            id=id,
            modified_at=modified_at,
            name=name,
            registration_origin=registration_origin,
            registry_id=registry_id,
            schema=schema,
            web_url=web_url,
            annotations=annotations,
            bases=bases,
            custom_notation=custom_notation,
            custom_notation_name=custom_notation_name,
            helm=helm,
            nucleotide_type=nucleotide_type,
            length=length,
            allow_measured_ingredients=allow_measured_ingredients,
            amount=amount,
            ingredients=ingredients,
            units=units,
            amino_acids=amino_acids,
            is_circular=is_circular,
            parts=parts,
            primers=primers,
            translations=translations,
        )

        request_response_samples_item_entity.additional_properties = d
        return request_response_samples_item_entity

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
    def inaccessible_id(self) -> str:
        if isinstance(self._inaccessible_id, Unset):
            raise NotPresentError(self, "inaccessible_id")
        return self._inaccessible_id

    @inaccessible_id.setter
    def inaccessible_id(self, value: str) -> None:
        self._inaccessible_id = value

    @inaccessible_id.deleter
    def inaccessible_id(self) -> None:
        self._inaccessible_id = UNSET

    @property
    def resource_type(self) -> InaccessibleResourceResourceType:
        if isinstance(self._resource_type, Unset):
            raise NotPresentError(self, "resource_type")
        return self._resource_type

    @resource_type.setter
    def resource_type(self, value: InaccessibleResourceResourceType) -> None:
        self._resource_type = value

    @resource_type.deleter
    def resource_type(self) -> None:
        self._resource_type = UNSET

    @property
    def type(self) -> str:
        """The type of this inaccessible item. Example values: "custom_entity", "container", "plate", "dna_sequence" """
        if isinstance(self._type, Unset):
            raise NotPresentError(self, "type")
        return self._type

    @type.setter
    def type(self, value: str) -> None:
        self._type = value

    @type.deleter
    def type(self) -> None:
        self._type = UNSET

    @property
    def aliases(self) -> List[str]:
        if isinstance(self._aliases, Unset):
            raise NotPresentError(self, "aliases")
        return self._aliases

    @aliases.setter
    def aliases(self, value: List[str]) -> None:
        self._aliases = value

    @aliases.deleter
    def aliases(self) -> None:
        self._aliases = UNSET

    @property
    def api_url(self) -> str:
        """ The canonical url of the DNA Sequence in the API. """
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
    def authors(self) -> List[UserSummary]:
        if isinstance(self._authors, Unset):
            raise NotPresentError(self, "authors")
        return self._authors

    @authors.setter
    def authors(self, value: List[UserSummary]) -> None:
        self._authors = value

    @authors.deleter
    def authors(self) -> None:
        self._authors = UNSET

    @property
    def created_at(self) -> datetime.datetime:
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
    def entity_registry_id(self) -> Optional[str]:
        if isinstance(self._entity_registry_id, Unset):
            raise NotPresentError(self, "entity_registry_id")
        return self._entity_registry_id

    @entity_registry_id.setter
    def entity_registry_id(self, value: Optional[str]) -> None:
        self._entity_registry_id = value

    @entity_registry_id.deleter
    def entity_registry_id(self) -> None:
        self._entity_registry_id = UNSET

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
    def folder_id(self) -> Optional[str]:
        if isinstance(self._folder_id, Unset):
            raise NotPresentError(self, "folder_id")
        return self._folder_id

    @folder_id.setter
    def folder_id(self, value: Optional[str]) -> None:
        self._folder_id = value

    @folder_id.deleter
    def folder_id(self) -> None:
        self._folder_id = UNSET

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
    def registration_origin(self) -> Optional[RegistrationOrigin]:
        if isinstance(self._registration_origin, Unset):
            raise NotPresentError(self, "registration_origin")
        return self._registration_origin

    @registration_origin.setter
    def registration_origin(self, value: Optional[RegistrationOrigin]) -> None:
        self._registration_origin = value

    @registration_origin.deleter
    def registration_origin(self) -> None:
        self._registration_origin = UNSET

    @property
    def registry_id(self) -> Optional[str]:
        if isinstance(self._registry_id, Unset):
            raise NotPresentError(self, "registry_id")
        return self._registry_id

    @registry_id.setter
    def registry_id(self, value: Optional[str]) -> None:
        self._registry_id = value

    @registry_id.deleter
    def registry_id(self) -> None:
        self._registry_id = UNSET

    @property
    def schema(self) -> Optional[SchemaSummary]:
        if isinstance(self._schema, Unset):
            raise NotPresentError(self, "schema")
        return self._schema

    @schema.setter
    def schema(self, value: Optional[SchemaSummary]) -> None:
        self._schema = value

    @schema.deleter
    def schema(self) -> None:
        self._schema = UNSET

    @property
    def web_url(self) -> str:
        if isinstance(self._web_url, Unset):
            raise NotPresentError(self, "web_url")
        return self._web_url

    @web_url.setter
    def web_url(self, value: str) -> None:
        self._web_url = value

    @web_url.deleter
    def web_url(self) -> None:
        self._web_url = UNSET

    @property
    def annotations(self) -> List[DnaAnnotation]:
        if isinstance(self._annotations, Unset):
            raise NotPresentError(self, "annotations")
        return self._annotations

    @annotations.setter
    def annotations(self, value: List[DnaAnnotation]) -> None:
        self._annotations = value

    @annotations.deleter
    def annotations(self) -> None:
        self._annotations = UNSET

    @property
    def bases(self) -> str:
        if isinstance(self._bases, Unset):
            raise NotPresentError(self, "bases")
        return self._bases

    @bases.setter
    def bases(self, value: str) -> None:
        self._bases = value

    @bases.deleter
    def bases(self) -> None:
        self._bases = UNSET

    @property
    def custom_notation(self) -> Optional[str]:
        """ Representation of the oligo in the custom notation specified in the request. Null if no notation was specified. """
        if isinstance(self._custom_notation, Unset):
            raise NotPresentError(self, "custom_notation")
        return self._custom_notation

    @custom_notation.setter
    def custom_notation(self, value: Optional[str]) -> None:
        self._custom_notation = value

    @custom_notation.deleter
    def custom_notation(self) -> None:
        self._custom_notation = UNSET

    @property
    def custom_notation_name(self) -> Optional[str]:
        """ Name of the custom notation specified in the request. Null if no notation was specified. """
        if isinstance(self._custom_notation_name, Unset):
            raise NotPresentError(self, "custom_notation_name")
        return self._custom_notation_name

    @custom_notation_name.setter
    def custom_notation_name(self, value: Optional[str]) -> None:
        self._custom_notation_name = value

    @custom_notation_name.deleter
    def custom_notation_name(self) -> None:
        self._custom_notation_name = UNSET

    @property
    def helm(self) -> str:
        """ Representation of the oligo in HELM syntax, including any chemical modifications """
        if isinstance(self._helm, Unset):
            raise NotPresentError(self, "helm")
        return self._helm

    @helm.setter
    def helm(self, value: str) -> None:
        self._helm = value

    @helm.deleter
    def helm(self) -> None:
        self._helm = UNSET

    @property
    def nucleotide_type(self) -> OligoNucleotideType:
        """ Nucleotide type of the Oligo. """
        if isinstance(self._nucleotide_type, Unset):
            raise NotPresentError(self, "nucleotide_type")
        return self._nucleotide_type

    @nucleotide_type.setter
    def nucleotide_type(self, value: OligoNucleotideType) -> None:
        self._nucleotide_type = value

    @nucleotide_type.deleter
    def nucleotide_type(self) -> None:
        self._nucleotide_type = UNSET

    @property
    def length(self) -> int:
        if isinstance(self._length, Unset):
            raise NotPresentError(self, "length")
        return self._length

    @length.setter
    def length(self, value: int) -> None:
        self._length = value

    @length.deleter
    def length(self) -> None:
        self._length = UNSET

    @property
    def allow_measured_ingredients(self) -> bool:
        """ Derived from the mixture's schema. """
        if isinstance(self._allow_measured_ingredients, Unset):
            raise NotPresentError(self, "allow_measured_ingredients")
        return self._allow_measured_ingredients

    @allow_measured_ingredients.setter
    def allow_measured_ingredients(self, value: bool) -> None:
        self._allow_measured_ingredients = value

    @allow_measured_ingredients.deleter
    def allow_measured_ingredients(self) -> None:
        self._allow_measured_ingredients = UNSET

    @property
    def amount(self) -> str:
        """ The positive numerical amount value of this mixture in string format (to preserve full precision). Pair with `units`. Supports scientific notation (1.23e4). """
        if isinstance(self._amount, Unset):
            raise NotPresentError(self, "amount")
        return self._amount

    @amount.setter
    def amount(self, value: str) -> None:
        self._amount = value

    @amount.deleter
    def amount(self) -> None:
        self._amount = UNSET

    @property
    def ingredients(self) -> List[Ingredient]:
        """ List of ingredients on this mixture. """
        if isinstance(self._ingredients, Unset):
            raise NotPresentError(self, "ingredients")
        return self._ingredients

    @ingredients.setter
    def ingredients(self, value: List[Ingredient]) -> None:
        self._ingredients = value

    @ingredients.deleter
    def ingredients(self) -> None:
        self._ingredients = UNSET

    @property
    def units(self) -> MixtureMeasurementUnits:
        if isinstance(self._units, Unset):
            raise NotPresentError(self, "units")
        return self._units

    @units.setter
    def units(self, value: MixtureMeasurementUnits) -> None:
        self._units = value

    @units.deleter
    def units(self) -> None:
        self._units = UNSET

    @property
    def amino_acids(self) -> str:
        """ Amino acids of the AA sequence. """
        if isinstance(self._amino_acids, Unset):
            raise NotPresentError(self, "amino_acids")
        return self._amino_acids

    @amino_acids.setter
    def amino_acids(self, value: str) -> None:
        self._amino_acids = value

    @amino_acids.deleter
    def amino_acids(self) -> None:
        self._amino_acids = UNSET

    @property
    def is_circular(self) -> bool:
        if isinstance(self._is_circular, Unset):
            raise NotPresentError(self, "is_circular")
        return self._is_circular

    @is_circular.setter
    def is_circular(self, value: bool) -> None:
        self._is_circular = value

    @is_circular.deleter
    def is_circular(self) -> None:
        self._is_circular = UNSET

    @property
    def parts(self) -> List[DnaSequencePart]:
        if isinstance(self._parts, Unset):
            raise NotPresentError(self, "parts")
        return self._parts

    @parts.setter
    def parts(self, value: List[DnaSequencePart]) -> None:
        self._parts = value

    @parts.deleter
    def parts(self) -> None:
        self._parts = UNSET

    @property
    def primers(self) -> List[Primer]:
        if isinstance(self._primers, Unset):
            raise NotPresentError(self, "primers")
        return self._primers

    @primers.setter
    def primers(self, value: List[Primer]) -> None:
        self._primers = value

    @primers.deleter
    def primers(self) -> None:
        self._primers = UNSET

    @property
    def translations(self) -> List[Translation]:
        if isinstance(self._translations, Unset):
            raise NotPresentError(self, "translations")
        return self._translations

    @translations.setter
    def translations(self, value: List[Translation]) -> None:
        self._translations = value

    @translations.deleter
    def translations(self) -> None:
        self._translations = UNSET
