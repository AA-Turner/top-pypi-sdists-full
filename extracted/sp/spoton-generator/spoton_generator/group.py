import random

from .persona import Persona


class Group:
    """Implementation of a group composed of people."""

    def __init__(self, name: str, personas: list[Persona], size: int):
        """Initialisation of the class.

        Parameters
        ----------
        name: str
            name of the group
        personas: list of Persona
            people's kinds to generate the group from
        size: int
            size of the group
        """
        self.name: str = name
        self.personas: list[Persona] = personas
        self.size: int = size
        self.people: list[Persona] = [random.choice(self.personas) for _ in range(self.size)]
        
    @property
    def user_names(self):
        return [p.name for p in self.people]
        
    def __str__(self):
        names = [persona.name for persona in self.personas]
        return f"'{self.name.upper()}' ({self.size} people) from {names}"

    def __repr__(self):
        return f"<{self.__class__.__name__}> '{self.name}'"

    @classmethod
    def load(cls, item: dict):
        """Create class instance from dictionnary.

        Parameters
        ----------
        item: dict
            input to create the instance from.
        """

        group_name: str = item.get("meta", {}).get("name", "default")
        group_size: int = item.get("meta", {}).get("size", 0)
        persona_list: list[dict] = item.get("personas", {})

        personas: list[Persona] = [Persona.load(p) for p in persona_list]
        
        return cls(group_name, personas, group_size)

            