from dataclasses import dataclass, field
from enum import Enum
from orionis.support.entities.base import BaseEntity

class Color(Enum):
    """Enumeration for available colors."""
    RED = 1
    GREEN = 2

@dataclass
class ExampleEntity(BaseEntity):
    """
    Example entity representing a data structure with id, name, color, and tags.

    Attributes
    ----------
    id : int
        Unique identifier for the entity.
    name : str
        Name of the entity.
    color : Color
        Color associated with the entity.
    tags : list
        List of tags associated with the entity.

    Returns
    -------
    ExampleEntity
        An instance of ExampleEntity with specified attributes.
    """
    id: int = 0  # Default id is 0
    name: str = "default"  # Default name is 'default'
    color: Color = Color.RED  # Default color is RED
    tags: list = field(default_factory=list, metadata={"default": ["tag1", "tag2"]})  # Default tags list