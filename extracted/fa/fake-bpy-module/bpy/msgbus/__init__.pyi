"""
[NOTE]
All subscribers will be cleared on file-load. Subscribers can be re-registered on load,
see bpy.app.handlers.load_post.

"""

import typing
import collections.abc
import typing_extensions
import numpy.typing as npt
import bpy.types

def clear_by_owner(owner: typing.Any | None) -> None:
    """Clear all subscribers using this owner.

    :param owner: The owner handle passed to `subscribe_rna`.
    """

def publish_rna(
    key: bpy.types.Property | bpy.types.Struct | tuple[bpy.types.Struct, str] | None,
) -> None:
    """Notify subscribers of changes to this property
    (this typically doesnt need to be called explicitly since changes will automatically publish updates).
    In some cases it may be useful to publish changes explicitly using more general keys.

        :param key: Represents the type of data being subscribed to

    Arguments include
    - A property instance.
    - A struct type.
    - A tuple representing a (struct, property name) pair.
    """

def subscribe_rna(
    key: bpy.types.Property | bpy.types.Struct | tuple[bpy.types.Struct, str] | None,
    owner: typing.Any | None,
    args: tuple | None,
    notify: collections.abc.Callable[..., None] | None,
    *,
    options: set[typing.Literal["PERSISTENT"]] | None = set(),
) -> None:
    """Register a message bus subscription. It will be cleared when another blend file is
    loaded, or can be cleared explicitly via `bpy.msgbus.clear_by_owner`.

        :param key: Represents the type of data being subscribed to

    Arguments include
    - A property instance.
    - A struct type.
    - A tuple representing a (struct, property name) pair.
        :param owner: Handle for this subscription (compared by identity).
        :param args: Arguments passed to the callback.
        :param notify: The callback function.
        :param options: Change the behavior of the subscriber.

    PERSISTENT when set, the subscriber will be kept when remapping ID data.
    """
