from enum import Enum
from typing import Optional, Union

import click
from typing_extensions import Literal

from anyscale.anyscale_pydantic import BaseModel


class EntityType(str, Enum):
    ID = "ID"
    NAME = "NAME"


class Entity(BaseModel):
    type: EntityType


class IdBasedEntity(Entity):
    type: Literal[EntityType.ID] = EntityType.ID
    id: str


class NameBasedEntity(Entity):
    type: Literal[EntityType.NAME] = EntityType.NAME
    name: str
    version: Optional[int] = None


def format_inputs_to_entity(
    name: Optional[str], entity_id: Optional[str]
) -> Union[IdBasedEntity, NameBasedEntity]:
    """
    Share method for CLI commands to accept either the name of the id of an entity.
    """
    if int(bool(name)) + int(bool(entity_id)) != 1:
        raise click.ClickException("Please provide exactly one of: name, id.")
    elif name:
        return NameBasedEntity(name=name)
    elif entity_id:
        return IdBasedEntity(id=entity_id)
    else:
        raise click.ClickException("Please provide exactly one of: name, id.")


def validate_exactly_one_name_or_id(
    name: Optional[str],
    entity_id: Optional[str],
    *,
    name_flag: str = "--name",
    id_flag: str = "--id",
) -> None:
    """Make sure the caller gives exactly one of name and id.

    Raise a ``ClickException`` if the caller gives more or fewer than one. This
    function replaces the per-command ``_validate_*_name_and_id`` copies. The
    default flag spellings are ``--name`` and ``--id``. Pass ``name_flag`` or
    ``id_flag`` to show a different spelling in the error message.
    """
    provided = int(name is not None) + int(entity_id is not None)
    if provided == 0:
        raise click.ClickException(
            f"One of '{name_flag}' and '{id_flag}' must be provided."
        )
    if provided > 1:
        raise click.ClickException(
            f"Only one of '{name_flag}' and '{id_flag}' can be provided."
        )
