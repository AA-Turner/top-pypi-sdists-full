import typing as t


def create_patch_schema(schema_class, **kwargs):
    """
    Instantiate a schema class for use with PATCH operations. Adds the
    following behaviors:

    -   Sets partial=True at the schema so that missing fields are allowed
    -   Sets the allow_none property of each field to True
    """
    if "partial" in kwargs:
        del kwargs["partial"]

    new_schema = schema_class(partial=True, **kwargs)
    for f in new_schema.fields:
        new_schema.fields[f].allow_none = True

    return new_schema


class IdentityMappingConfiguration(t.TypedDict):
    DATA_TYPE: str
