from ._entity import Entity


class SchemaExtension(Entity):
    """
    The OCSF Schema Extension object provides detailed information about the schema
    extension used to construct the event. The schema extensions are registered in
    the <a target='_blank' href='https://github.com/ocsf/ocsf-
    schema/blob/main/extensions.md'>extensions.md</a> file.
    """

    name: str # The schema extension name. For example: `dev`.
    uid: str # The schema extension unique identifier. For example: `999`.
    version: str # The schema extension version. For example: `1.0.0-alpha.2`.

