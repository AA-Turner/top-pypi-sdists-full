import typing
import collections.abc
import typing_extensions
import numpy.typing as npt
import bpy.stub_internal.rna_enums
import mathutils

def primitive_nurbs_surface_circle_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    radius: float | None = 1.0,
    enter_editmode: bool | None = False,
    align: typing.Literal["WORLD", "VIEW", "CURSOR"] | None = "WORLD",
    location: collections.abc.Sequence[float] | mathutils.Vector | None = (
        0.0,
        0.0,
        0.0,
    ),
    rotation: collections.abc.Sequence[float] | mathutils.Euler | None = (
        0.0,
        0.0,
        0.0,
    ),
    scale: collections.abc.Sequence[float] | mathutils.Vector | None = (0.0, 0.0, 0.0),
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Construct a NURBS surface circle

        :param radius: Radius, (in [0, inf], optional)
        :param enter_editmode: Enter Edit Mode, Enter edit mode when adding this object (optional)
        :param align: Align, The alignment of the new object (optional)

    WORLD
    World -- Align the new object to the world.

    VIEW
    View -- Align the new object to the view.

    CURSOR
    3D Cursor -- Use the 3D cursor orientation for the new object.
        :param location: Location, Location for the newly added object (array of 3 items, in [-inf, inf], optional)
        :param rotation: Rotation, Rotation for the newly added object (array of 3 items, in [-inf, inf], optional)
        :param scale: Scale, Scale for the newly added object (array of 3 items, in [-inf, inf], optional)
        :return: Result of the operator call.
    """

def primitive_nurbs_surface_curve_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    radius: float | None = 1.0,
    enter_editmode: bool | None = False,
    align: typing.Literal["WORLD", "VIEW", "CURSOR"] | None = "WORLD",
    location: collections.abc.Sequence[float] | mathutils.Vector | None = (
        0.0,
        0.0,
        0.0,
    ),
    rotation: collections.abc.Sequence[float] | mathutils.Euler | None = (
        0.0,
        0.0,
        0.0,
    ),
    scale: collections.abc.Sequence[float] | mathutils.Vector | None = (0.0, 0.0, 0.0),
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Construct a NURBS surface curve

        :param radius: Radius, (in [0, inf], optional)
        :param enter_editmode: Enter Edit Mode, Enter edit mode when adding this object (optional)
        :param align: Align, The alignment of the new object (optional)

    WORLD
    World -- Align the new object to the world.

    VIEW
    View -- Align the new object to the view.

    CURSOR
    3D Cursor -- Use the 3D cursor orientation for the new object.
        :param location: Location, Location for the newly added object (array of 3 items, in [-inf, inf], optional)
        :param rotation: Rotation, Rotation for the newly added object (array of 3 items, in [-inf, inf], optional)
        :param scale: Scale, Scale for the newly added object (array of 3 items, in [-inf, inf], optional)
        :return: Result of the operator call.
    """

def primitive_nurbs_surface_cylinder_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    radius: float | None = 1.0,
    enter_editmode: bool | None = False,
    align: typing.Literal["WORLD", "VIEW", "CURSOR"] | None = "WORLD",
    location: collections.abc.Sequence[float] | mathutils.Vector | None = (
        0.0,
        0.0,
        0.0,
    ),
    rotation: collections.abc.Sequence[float] | mathutils.Euler | None = (
        0.0,
        0.0,
        0.0,
    ),
    scale: collections.abc.Sequence[float] | mathutils.Vector | None = (0.0, 0.0, 0.0),
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Construct a NURBS surface cylinder

        :param radius: Radius, (in [0, inf], optional)
        :param enter_editmode: Enter Edit Mode, Enter edit mode when adding this object (optional)
        :param align: Align, The alignment of the new object (optional)

    WORLD
    World -- Align the new object to the world.

    VIEW
    View -- Align the new object to the view.

    CURSOR
    3D Cursor -- Use the 3D cursor orientation for the new object.
        :param location: Location, Location for the newly added object (array of 3 items, in [-inf, inf], optional)
        :param rotation: Rotation, Rotation for the newly added object (array of 3 items, in [-inf, inf], optional)
        :param scale: Scale, Scale for the newly added object (array of 3 items, in [-inf, inf], optional)
        :return: Result of the operator call.
    """

def primitive_nurbs_surface_sphere_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    radius: float | None = 1.0,
    enter_editmode: bool | None = False,
    align: typing.Literal["WORLD", "VIEW", "CURSOR"] | None = "WORLD",
    location: collections.abc.Sequence[float] | mathutils.Vector | None = (
        0.0,
        0.0,
        0.0,
    ),
    rotation: collections.abc.Sequence[float] | mathutils.Euler | None = (
        0.0,
        0.0,
        0.0,
    ),
    scale: collections.abc.Sequence[float] | mathutils.Vector | None = (0.0, 0.0, 0.0),
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Construct a NURBS surface sphere

        :param radius: Radius, (in [0, inf], optional)
        :param enter_editmode: Enter Edit Mode, Enter edit mode when adding this object (optional)
        :param align: Align, The alignment of the new object (optional)

    WORLD
    World -- Align the new object to the world.

    VIEW
    View -- Align the new object to the view.

    CURSOR
    3D Cursor -- Use the 3D cursor orientation for the new object.
        :param location: Location, Location for the newly added object (array of 3 items, in [-inf, inf], optional)
        :param rotation: Rotation, Rotation for the newly added object (array of 3 items, in [-inf, inf], optional)
        :param scale: Scale, Scale for the newly added object (array of 3 items, in [-inf, inf], optional)
        :return: Result of the operator call.
    """

def primitive_nurbs_surface_surface_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    radius: float | None = 1.0,
    enter_editmode: bool | None = False,
    align: typing.Literal["WORLD", "VIEW", "CURSOR"] | None = "WORLD",
    location: collections.abc.Sequence[float] | mathutils.Vector | None = (
        0.0,
        0.0,
        0.0,
    ),
    rotation: collections.abc.Sequence[float] | mathutils.Euler | None = (
        0.0,
        0.0,
        0.0,
    ),
    scale: collections.abc.Sequence[float] | mathutils.Vector | None = (0.0, 0.0, 0.0),
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Construct a NURBS surface patch

        :param radius: Radius, (in [0, inf], optional)
        :param enter_editmode: Enter Edit Mode, Enter edit mode when adding this object (optional)
        :param align: Align, The alignment of the new object (optional)

    WORLD
    World -- Align the new object to the world.

    VIEW
    View -- Align the new object to the view.

    CURSOR
    3D Cursor -- Use the 3D cursor orientation for the new object.
        :param location: Location, Location for the newly added object (array of 3 items, in [-inf, inf], optional)
        :param rotation: Rotation, Rotation for the newly added object (array of 3 items, in [-inf, inf], optional)
        :param scale: Scale, Scale for the newly added object (array of 3 items, in [-inf, inf], optional)
        :return: Result of the operator call.
    """

def primitive_nurbs_surface_torus_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    radius: float | None = 1.0,
    enter_editmode: bool | None = False,
    align: typing.Literal["WORLD", "VIEW", "CURSOR"] | None = "WORLD",
    location: collections.abc.Sequence[float] | mathutils.Vector | None = (
        0.0,
        0.0,
        0.0,
    ),
    rotation: collections.abc.Sequence[float] | mathutils.Euler | None = (
        0.0,
        0.0,
        0.0,
    ),
    scale: collections.abc.Sequence[float] | mathutils.Vector | None = (0.0, 0.0, 0.0),
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Construct a NURBS surface torus

        :param radius: Radius, (in [0, inf], optional)
        :param enter_editmode: Enter Edit Mode, Enter edit mode when adding this object (optional)
        :param align: Align, The alignment of the new object (optional)

    WORLD
    World -- Align the new object to the world.

    VIEW
    View -- Align the new object to the view.

    CURSOR
    3D Cursor -- Use the 3D cursor orientation for the new object.
        :param location: Location, Location for the newly added object (array of 3 items, in [-inf, inf], optional)
        :param rotation: Rotation, Rotation for the newly added object (array of 3 items, in [-inf, inf], optional)
        :param scale: Scale, Scale for the newly added object (array of 3 items, in [-inf, inf], optional)
        :return: Result of the operator call.
    """
