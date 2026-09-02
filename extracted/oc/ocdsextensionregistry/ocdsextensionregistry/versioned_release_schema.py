import warnings
from copy import deepcopy

import jsonref

from ocdsextensionregistry.exceptions import (
    VersionedReleaseItemsWarning,
    VersionedReleaseRefWarning,
    VersionedReleaseTypeWarning,
)

_VERSIONED_TEMPLATE = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "releaseDate": {"format": "date-time", "type": "string"},
            "releaseID": {"type": "string"},
            "value": {},
            "releaseTag": {"type": "array", "items": {"type": "string"}},
        },
    },
}
_COMMON_VERSIONED_DEFINITIONS = {
    "StringNullUriVersioned": {
        "type": ["string", "null"],
        "format": "uri",
    },
    "StringNullDateTimeVersioned": {
        "type": ["string", "null"],
        "format": "date-time",
    },
    "StringNullVersioned": {
        "type": ["string", "null"],
        "format": None,
    },
}
_RECOGNIZED_TYPES = (
    # Array
    ["array"],
    ["array", "null"],  # optional string arrays
    # Object
    ["object"],
    ["object", "null"],  # /Organization/details
    # String
    ["string"],
    ["string", "null"],
    # Literal
    ["boolean", "null"],
    ["integer", "null"],
    ["number", "null"],
    # Mixed
    ["integer", "string"],
    ["integer", "string", "null"],
    ["number", "string", "null"],
)
_KEYWORDS_TO_REMOVE = (
    # Metadata keywords
    # https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-6
    "title",
    "description",
    "default",
    # Extended keywords
    # http://os4d.opendataservices.coop/development/schema/#extended-json-schema
    "omitWhenMerged",
    "wholeListMerge",
)


def _cast_as_list(value):
    if isinstance(value, str):
        return [value]
    return sorted(value, key=lambda entry: "~" if entry == "null" else entry)


def _get_common_definition_ref(item):
    """
    Return a schema that references the common definition that the ``item`` matches: "StringNullUriVersioned",
    "StringNullDateTimeVersioned" or "StringNullVersioned".
    """
    for name, keywords in _COMMON_VERSIONED_DEFINITIONS.items():
        # If the item matches the definition.
        if any(item.get(keyword) != value for keyword, value in keywords.items()):
            continue
        # And adds no keywords to the definition.
        if any(keyword not in {*keywords, *_KEYWORDS_TO_REMOVE} for keyword in item):
            continue
        return {"$ref": f"#/definitions/{name}"}
    return None


def _remove_omit_when_merged(schema):
    """Remove properties that set ``omitWhenMerged``."""
    if isinstance(schema, list):
        for item in schema:
            _remove_omit_when_merged(item)
    elif isinstance(schema, dict):
        for key, value in schema.items():
            if key == "properties":
                for prop in list(value):
                    if value[prop].get("omitWhenMerged"):
                        del value[prop]
                        if prop in schema.get("required", []):
                            schema["required"].remove(prop)
            _remove_omit_when_merged(value)


def _update_refs_to_unversioned_definitions(schema):
    """Replace ``$ref`` values with unversioned definitions."""
    for key, value in schema.items():
        if key == "$ref":
            schema[key] = value + "Unversioned"
        elif isinstance(value, dict):
            _update_refs_to_unversioned_definitions(value)


def _get_unversioned_pointers(schema, fields, pointer=""):
    """Return the JSON Pointers to ``id`` fields that must not be versioned if the object is in an array."""
    if isinstance(schema, list):
        for index, item in enumerate(schema):
            _get_unversioned_pointers(item, fields, pointer=f"{pointer}/{index}")
    elif isinstance(schema, dict):
        # Follows the logic of _get_merge_rules in merge.py from ocds-merge.
        types = _cast_as_list(schema.get("type", []))

        # If an array is whole list merge, its items are unversioned.
        if "array" in types and schema.get("wholeListMerge"):
            return
        if "array" in types and (items := schema.get("items")):
            if isinstance(items, dict):
                item_types = _cast_as_list(items.get("type", []))
                # If an array mixes objects and non-objects, it is whole list merge.
                if any(item_type != "object" for item_type in item_types):
                    return
                # If it is an array of objects, any `id` fields are unversioned.
                if "id" in items["properties"]:
                    reference = items.__reference__["$ref"][1:] if hasattr(items, "__reference__") else pointer
                    fields.add(f"{reference}/properties/id")
            # This should only occur in tests.
            else:
                warnings.warn(VersionedReleaseItemsWarning(pointer, schema), stacklevel=2)

        for key, value in schema.items():
            _get_unversioned_pointers(value, fields, pointer=f"{pointer}/{key}")


def _add_versioned_fields(schema, unversioned_pointers, pointer=""):
    """Call ``_add_versioned_field`` on each field."""
    for key, value in schema.get("properties", {}).items():
        new_pointer = f"{pointer}/properties/{key}"
        _add_versioned_field(schema, unversioned_pointers, new_pointer, key, value)

    for key, value in schema.get("definitions", {}).items():
        new_pointer = f"{pointer}/definitions/{key}"
        _add_versioned_fields(value, unversioned_pointers, pointer=new_pointer)


def _add_versioned_field(schema, unversioned_pointers, pointer, key, value):
    """
    Perform the changes to the schema to refer to versioned/unversioned definitions.

    :param schema dict: the schema of the object on which the field is defined
    :param unversioned_pointers set: JSON Pointers to ``id`` fields to leave unversioned if the object is in an array
    :param pointer str: the field's pointer
    :param key str: the field's name
    :param value str: the field's schema
    """
    # Skip unversioned fields.
    if pointer in unversioned_pointers:
        return

    types = _cast_as_list(value.get("type", []))

    # https://github.com/transpresupuestaria/ocds_related_projects_extension
    # planning.relatedProjects has no `type`. planning.relatedProjects.locations has `properties` as "array".
    if "properties" in value and types in ([], ["array"]):
        types = ["object"]

    # If a type is unrecognized, we might need to update this script.
    if (
        "$ref" not in value
        and types not in _RECOGNIZED_TYPES
        and not (pointer == "/definitions/Quantity/properties/value" and types == ["string", "number", "null"])
    ):
        warnings.warn(VersionedReleaseTypeWarning(pointer, types, value), stacklevel=2)

    # For example, if $ref is used.
    if not types:
        # Ignore the `amendment` field, which had no `id` field in OCDS 1.0.
        if "deprecated" not in value:
            if "$ref" in value:
                versioned_pointer = f"{value['$ref'][1:]}/properties/id"
                # If the `id` field is on an object not in an array, it needs to be versioned (like on `buyer`).
                if versioned_pointer in unversioned_pointers:
                    value["$ref"] = value["$ref"] + "VersionedId"
            # This should only occur in tests.
            else:
                warnings.warn(VersionedReleaseRefWarning(pointer, value), stacklevel=2)
        return

    # Reference a common versioned definition if possible, to limit the size of the schema.
    ref = _get_common_definition_ref(value)
    if ref:
        schema["properties"][key] = ref

    # Iterate into objects with properties like `Item.unit`. Otherwise, version objects with no properties as a
    # whole, like `Organization.details`.
    elif types == ["object"] and "properties" in value:
        _add_versioned_fields(value, unversioned_pointers, pointer=pointer)

    else:
        new_value = deepcopy(value)

        if types == ["array"]:
            if (items := value.get("items")) and isinstance(items, dict):
                item_types = _cast_as_list(items.get("type", []))

                # See https://standard.open-contracting.org/latest/en/schema/merging/#whole-list-merge
                if value.get("wholeListMerge"):
                    # Update `$ref` to the unversioned definition.
                    if "$ref" in items:
                        new_value["items"]["$ref"] = items["$ref"] + "Unversioned"
                    # Otherwise, similarly, don't iterate over item properties.
                # See https://standard.open-contracting.org/latest/en/schema/merging/#lists
                elif "$ref" in items:
                    # Leave `$ref` to the versioned definition.
                    return
                # Exceptional case for deprecated `Amendment.changes`.
                elif item_types == ["object"] and pointer == "/definitions/Amendment/properties/changes":
                    return
                # Warn in case new combinations are added to the release schema.
                elif item_types != ["string"]:
                    # Note: Versioning the properties of un-$ref'erenced objects in arrays isn't implemented. However,
                    # this combination hasn't occurred, with the exception of `Amendment/changes`.
                    warnings.warn(VersionedReleaseTypeWarning(f"{pointer}/items", item_types, value), stacklevel=2)
            # This should only occur in tests.
            else:
                warnings.warn(VersionedReleaseItemsWarning(pointer, value), stacklevel=2)

        versioned = deepcopy(_VERSIONED_TEMPLATE)
        versioned["items"]["properties"]["value"] = new_value
        schema["properties"][key] = versioned


def _remove_metadata_and_extended_keywords(schema):
    """Remove metadata and extended keywords from properties and definitions."""
    if isinstance(schema, list):
        for item in schema:
            _remove_metadata_and_extended_keywords(item)
    elif isinstance(schema, dict):
        for key, value in schema.items():
            if key in {"definitions", "properties"}:
                for subschema in value.values():
                    for keyword in _KEYWORDS_TO_REMOVE:
                        subschema.pop(keyword, None)
            _remove_metadata_and_extended_keywords(value)


def get_versioned_release_schema(schema, tag):
    """Return the versioned release schema."""
    schema = deepcopy(schema)

    # Update schema metadata.
    schema["id"] = f"https://standard.open-contracting.org/schema/{tag}/versioned-release-validation-schema.json"
    schema["title"] = "Schema for a compiled, versioned Open Contracting Release."

    # Release IDs, dates and tags appear alongside values in the versioned release schema.
    _remove_omit_when_merged(schema)

    # Create unversioned copies of all definitions.
    unversioned_definitions = {k + "Unversioned": deepcopy(v) for k, v in schema["definitions"].items()}
    _update_refs_to_unversioned_definitions(unversioned_definitions)

    # Determine which `id` fields occur on objects in arrays.
    unversioned_pointers = set()
    _get_unversioned_pointers(jsonref.replace_refs(schema), unversioned_pointers)

    # Omit `ocid` from versioning.
    ocid = schema["properties"].pop("ocid")
    _add_versioned_fields(schema, unversioned_pointers)
    schema["properties"]["ocid"] = ocid

    # Add the common versioned definitions.
    for name, keywords in _COMMON_VERSIONED_DEFINITIONS.items():
        versioned = deepcopy(_VERSIONED_TEMPLATE)
        for keyword, value in keywords.items():
            if value:
                versioned["items"]["properties"]["value"][keyword] = value
        schema["definitions"][name] = versioned

    # Add missing definitions.
    while True:
        try:
            jsonref.replace_refs(schema, lazy_load=False)
            break
        except jsonref.JsonRefError as e:
            name = e.cause.args[0]

            if name.endswith("VersionedId"):
                # Add a copy of an definition with a versioned `id` field, using the same logic as before.
                definition = deepcopy(schema["definitions"][name[:-11]])
                pointer = f"/definitions/{name[:-11]}/properties/id"
                pointers = unversioned_pointers - {pointer}
                _add_versioned_field(definition, pointers, pointer, "id", definition["properties"]["id"])
            else:
                # Add a copy of an definition with no versioned fields.
                definition = unversioned_definitions[name]

            schema["definitions"][name] = definition

    # Remove all metadata and extended keywords.
    _remove_metadata_and_extended_keywords(schema)

    return schema
