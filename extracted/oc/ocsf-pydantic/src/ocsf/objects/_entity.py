from pydantic import BaseModel

class Entity(BaseModel):
    """
    The Entity object is an unordered collection of attributes, with a name and
    unique identifier. It serves as a base object that defines a set of attributes
    and default constraints available in all objects that extend it.
    """

    # Recommended:
    name: str | None = None # The name of the entity.
    uid: str | None = None # The unique identifier of the entity.
