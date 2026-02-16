import typing
import collections.abc
import typing_extensions
import numpy.typing as npt
import bpy.stub_internal.rna_enums

def bone_select_menu(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    name: str | None = "",
    extend: bool | None = False,
    deselect: bool | None = False,
    toggle: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Menu bone selection

    :param name: Bone Name, (optional)
    :param extend: Extend, (optional)
    :param deselect: Deselect, (optional)
    :param toggle: Toggle, (optional)
    :return: Result of the operator call.
    """

def camera_background_image_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    filepath: str | None = "",
    relative_path: bool | None = True,
    name: str | None = "",
    session_uid: int | None = 0,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add a new background image to the active camera

    :param filepath: Filepath, Path to image file (optional, never None, blend relative // prefix supported)
    :param relative_path: Relative Path, Select the file relative to the blend file (optional)
    :param name: Name, Name of the data-block to use by the operator (optional, never None)
    :param session_uid: Session UID, Session UID of the data-block to use by the operator (in [-inf, inf], optional)
    :return: Result of the operator call.
    """

def camera_background_image_remove(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    index: int | None = 0,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove a background image from the camera

    :param index: Index, Background image index to remove (in [0, inf], optional)
    :return: Result of the operator call.
    """

def camera_to_view(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Set camera view to active view

    :return: Result of the operator call.
    """

def camera_to_view_selected(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Move the camera so selected objects are framed

    :return: Result of the operator call.
    """

def clear_render_border(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Clear the boundaries of the border render and disable border render

    :return: Result of the operator call.
    """

def clip_border(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    xmin: int | None = 0,
    xmax: int | None = 0,
    ymin: int | None = 0,
    ymax: int | None = 0,
    wait_for_input: bool | None = True,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Set the view clipping region

    :param xmin: X Min, (in [-inf, inf], optional)
    :param xmax: X Max, (in [-inf, inf], optional)
    :param ymin: Y Min, (in [-inf, inf], optional)
    :param ymax: Y Max, (in [-inf, inf], optional)
    :param wait_for_input: Wait for Input, (optional)
    :return: Result of the operator call.
    """

def copybuffer(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Copy the selected objects to the internal clipboard

    :return: Result of the operator call.
    """

def cursor3d(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    use_depth: bool | None = True,
    orientation: typing.Literal["NONE", "VIEW", "XFORM", "GEOM"] | None = "VIEW",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Set the location of the 3D cursor

        :param use_depth: Surface Project, Project onto the surface (optional)
        :param orientation: Orientation, Preset viewpoint to use (optional)

    NONE
    None -- Leave orientation unchanged.

    VIEW
    View -- Orient to the viewport.

    XFORM
    Transform -- Orient to the current transform setting.

    GEOM
    Geometry -- Match the surface normal.
        :return: Result of the operator call.
    """

def dolly(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    mx: int | None = 0,
    my: int | None = 0,
    delta: int | None = 0,
    use_cursor_init: bool | None = True,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Dolly in/out in the view

    :param mx: Region Position X, (in [0, inf], optional)
    :param my: Region Position Y, (in [0, inf], optional)
    :param delta: Delta, (in [-inf, inf], optional)
    :param use_cursor_init: Use Mouse Position, Allow the initial mouse position to be used (optional)
    :return: Result of the operator call.
    """

def drop_world(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    name: str | None = "",
    session_uid: int | None = 0,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Drop a world into the scene

    :param name: Name, Name of the data-block to use by the operator (optional, never None)
    :param session_uid: Session UID, Session UID of the data-block to use by the operator (in [-inf, inf], optional)
    :return: Result of the operator call.
    """

def edit_mesh_extrude_individual_move(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Extrude each individual face separately along local normals

    :return: Result of the operator call.
    """

def edit_mesh_extrude_manifold_normal(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Extrude manifold region along normals

    :return: Result of the operator call.
    """

def edit_mesh_extrude_move_normal(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    dissolve_and_intersect: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Extrude region together along the average normal

    :param dissolve_and_intersect: dissolve_and_intersect, Dissolves adjacent faces and intersects new geometry (optional)
    :return: Result of the operator call.
    """

def edit_mesh_extrude_move_shrink_fatten(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Extrude region together along local normals

    :return: Result of the operator call.
    """

def fly(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Interactively fly around the scene

    :return: Result of the operator call.
    """

def interactive_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    primitive_type: typing.Literal[
        "CUBE", "CYLINDER", "CONE", "SPHERE_UV", "SPHERE_ICO"
    ]
    | None = "CUBE",
    plane_origin_base: typing.Literal["EDGE", "CENTER"] | None = "EDGE",
    plane_origin_depth: typing.Literal["EDGE", "CENTER"] | None = "EDGE",
    plane_aspect_base: typing.Literal["FREE", "FIXED"] | None = "FREE",
    plane_aspect_depth: typing.Literal["FREE", "FIXED"] | None = "FREE",
    wait_for_input: bool | None = True,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Interactively add an object

        :param primitive_type: Primitive, (optional)
        :param plane_origin_base: Origin, The initial position for placement (optional)

    EDGE
    Edge -- Start placing the edge position.

    CENTER
    Center -- Start placing the center position.
        :param plane_origin_depth: Origin, The initial position for placement (optional)

    EDGE
    Edge -- Start placing the edge position.

    CENTER
    Center -- Start placing the center position.
        :param plane_aspect_base: Aspect, The initial aspect setting (optional)

    FREE
    Free -- Use an unconstrained aspect.

    FIXED
    Fixed -- Use a fixed 1:1 aspect.
        :param plane_aspect_depth: Aspect, The initial aspect setting (optional)

    FREE
    Free -- Use an unconstrained aspect.

    FIXED
    Fixed -- Use a fixed 1:1 aspect.
        :param wait_for_input: Wait for Input, (optional)
        :return: Result of the operator call.
    """

def localview(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    frame_selected: bool | None = True,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Toggle display of selected object(s) separately and centered in view

    :param frame_selected: Frame Selected, Move the view to frame the selected objects (optional)
    :return: Result of the operator call.
    """

def localview_remove_from(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Move selected objects out of local view

    :return: Result of the operator call.
    """

def move(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    use_cursor_init: bool | None = True,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Move the view

    :param use_cursor_init: Use Mouse Position, Allow the initial mouse position to be used (optional)
    :return: Result of the operator call.
    """

def navigate(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Interactively navigate around the scene (uses the mode (walk/fly) preference)

    :return: Result of the operator call.
    """

def ndof_all(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Pan and rotate the view with the 3D mouse

    :return: Result of the operator call.
    """

def ndof_orbit(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Orbit the view using the 3D mouse

    :return: Result of the operator call.
    """

def ndof_orbit_zoom(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Orbit and zoom the view using the 3D mouse

    :return: Result of the operator call.
    """

def ndof_pan(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Pan the view with the 3D mouse

    :return: Result of the operator call.
    """

def object_as_camera(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Set the active object as the active camera for this view or scene

    :return: Result of the operator call.
    """

def object_mode_pie_or_toggle(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Undocumented, consider contributing.

    :return: Result of the operator call.
    """

def pastebuffer(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    autoselect: bool | None = True,
    active_collection: bool | None = True,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Paste objects from the internal clipboard

    :param autoselect: Select, Select pasted objects (optional)
    :param active_collection: Active Collection, Put pasted objects in the active collection (optional)
    :return: Result of the operator call.
    """

def render_border(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    xmin: int | None = 0,
    xmax: int | None = 0,
    ymin: int | None = 0,
    ymax: int | None = 0,
    wait_for_input: bool | None = True,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Set the boundaries of the border render and enable border render

    :param xmin: X Min, (in [-inf, inf], optional)
    :param xmax: X Max, (in [-inf, inf], optional)
    :param ymin: Y Min, (in [-inf, inf], optional)
    :param ymax: Y Max, (in [-inf, inf], optional)
    :param wait_for_input: Wait for Input, (optional)
    :return: Result of the operator call.
    """

def rotate(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    use_cursor_init: bool | None = True,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Rotate the view

    :param use_cursor_init: Use Mouse Position, Allow the initial mouse position to be used (optional)
    :return: Result of the operator call.
    """

def ruler_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add ruler

    :return: Result of the operator call.
    """

def ruler_remove(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Undocumented, consider contributing.

    :return: Result of the operator call.
    """

def select(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    extend: bool | None = False,
    deselect: bool | None = False,
    toggle: bool | None = False,
    deselect_all: bool | None = False,
    select_passthrough: bool | None = False,
    center: bool | None = False,
    enumerate: bool | None = False,
    object: bool | None = False,
    location: collections.abc.Sequence[int] | None = (0, 0),
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select and activate item(s)

    :param extend: Extend, Extend selection instead of deselecting everything first (optional)
    :param deselect: Deselect, Remove from selection (optional)
    :param toggle: Toggle Selection, Toggle the selection (optional)
    :param deselect_all: Deselect On Nothing, Deselect all when nothing under the cursor (optional)
    :param select_passthrough: Only Select Unselected, Ignore the select action when the element is already selected (optional)
    :param center: Center, Use the object center when selecting, in edit mode used to extend object selection (optional)
    :param enumerate: Enumerate, List objects under the mouse (object mode only) (optional)
    :param object: Object, Use object selection (edit mode only) (optional)
    :param location: Location, Mouse location (array of 2 items, in [-inf, inf], optional)
    :return: Result of the operator call.
    """

def select_box(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    xmin: int | None = 0,
    xmax: int | None = 0,
    ymin: int | None = 0,
    ymax: int | None = 0,
    wait_for_input: bool | None = True,
    mode: typing.Literal["SET", "ADD", "SUB", "XOR", "AND"] | None = "SET",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select items using box selection

        :param xmin: X Min, (in [-inf, inf], optional)
        :param xmax: X Max, (in [-inf, inf], optional)
        :param ymin: Y Min, (in [-inf, inf], optional)
        :param ymax: Y Max, (in [-inf, inf], optional)
        :param wait_for_input: Wait for Input, (optional)
        :param mode: Mode, (optional)

    SET
    Set -- Set a new selection.

    ADD
    Extend -- Extend existing selection.

    SUB
    Subtract -- Subtract existing selection.

    XOR
    Difference -- Invert existing selection.

    AND
    Intersect -- Intersect existing selection.
        :return: Result of the operator call.
    """

def select_circle(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    x: int | None = 0,
    y: int | None = 0,
    radius: int | None = 25,
    wait_for_input: bool | None = True,
    mode: typing.Literal["SET", "ADD", "SUB"] | None = "SET",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select items using circle selection

        :param x: X, (in [-inf, inf], optional)
        :param y: Y, (in [-inf, inf], optional)
        :param radius: Radius, (in [1, inf], optional)
        :param wait_for_input: Wait for Input, (optional)
        :param mode: Mode, (optional)

    SET
    Set -- Set a new selection.

    ADD
    Extend -- Extend existing selection.

    SUB
    Subtract -- Subtract existing selection.
        :return: Result of the operator call.
    """

def select_lasso(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    path=None,
    use_smooth_stroke: bool | None = False,
    smooth_stroke_factor: float | None = 0.75,
    smooth_stroke_radius: int | None = 35,
    mode: typing.Literal["SET", "ADD", "SUB", "XOR", "AND"] | None = "SET",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select items using lasso selection

        :param path: Path, (optional)
        :param use_smooth_stroke: Stabilize Stroke, Selection lags behind mouse and follows a smoother path (optional)
        :param smooth_stroke_factor: Smooth Stroke Factor, Higher values gives a smoother stroke (in [0.5, 0.99], optional)
        :param smooth_stroke_radius: Smooth Stroke Radius, Minimum distance from last point before selection continues (in [10, 200], optional)
        :param mode: Mode, (optional)

    SET
    Set -- Set a new selection.

    ADD
    Extend -- Extend existing selection.

    SUB
    Subtract -- Subtract existing selection.

    XOR
    Difference -- Invert existing selection.

    AND
    Intersect -- Intersect existing selection.
        :return: Result of the operator call.
    """

def select_menu(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    name: str | None = "",
    extend: bool | None = False,
    deselect: bool | None = False,
    toggle: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Menu object selection

    :param name: Object Name, (optional)
    :param extend: Extend, (optional)
    :param deselect: Deselect, (optional)
    :param toggle: Toggle, (optional)
    :return: Result of the operator call.
    """

def smoothview(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Undocumented, consider contributing.

    :return: Result of the operator call.
    """

def snap_cursor_to_active(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Snap 3D cursor to the active item

    :return: Result of the operator call.
    """

def snap_cursor_to_center(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Snap 3D cursor to the world origin

    :return: Result of the operator call.
    """

def snap_cursor_to_grid(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Snap 3D cursor to the nearest grid division

    :return: Result of the operator call.
    """

def snap_cursor_to_selected(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Snap 3D cursor to the middle of the selected item(s)

    :return: Result of the operator call.
    """

def snap_selected_to_active(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Snap selected item(s) to the active item

    :return: Result of the operator call.
    """

def snap_selected_to_cursor(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    use_offset: bool | None = True,
    use_rotation: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Snap selected item(s) to the 3D cursor

    :param use_offset: Offset, If the selection should be snapped as a whole or by each object center (optional)
    :param use_rotation: Rotation, If the selection should be rotated to match the cursor (optional)
    :return: Result of the operator call.
    """

def snap_selected_to_grid(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Snap selected item(s) to their nearest grid division

    :return: Result of the operator call.
    """

def toggle_matcap_flip(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Flip MatCap

    :return: Result of the operator call.
    """

def toggle_shading(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: typing.Literal["WIREFRAME", "SOLID", "MATERIAL", "RENDERED"]
    | None = "WIREFRAME",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Toggle shading type in 3D viewport

        :param type: Type, Shading type to toggle (optional)

    WIREFRAME
    Wireframe -- Toggle wireframe shading.

    SOLID
    Solid -- Toggle solid shading.

    MATERIAL
    Material Preview -- Toggle material preview shading.

    RENDERED
    Rendered -- Toggle rendered shading.
        :return: Result of the operator call.
    """

def toggle_xray(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Transparent scene display. Allow selecting through items

    :return: Result of the operator call.
    """

def transform_gizmo_set(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    extend: bool | None = False,
    type: set[typing.Literal["TRANSLATE", "ROTATE", "SCALE"]] | None = {},
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Set the current transform gizmo

    :param extend: Extend, (optional)
    :param type: Type, (optional)
    :return: Result of the operator call.
    """

def view_all(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    use_all_regions: bool | None = False,
    center: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """View all objects in scene

    :param use_all_regions: All Regions, View selected for all regions (optional)
    :param center: Center, (optional)
    :return: Result of the operator call.
    """

def view_axis(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: typing.Literal["LEFT", "RIGHT", "BOTTOM", "TOP", "FRONT", "BACK"]
    | None = "LEFT",
    align_active: bool | None = False,
    relative: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Use a preset viewpoint

        :param type: View, Preset viewpoint to use (optional)

    LEFT
    Left -- View from the left.

    RIGHT
    Right -- View from the right.

    BOTTOM
    Bottom -- View from the bottom.

    TOP
    Top -- View from the top.

    FRONT
    Front -- View from the front.

    BACK
    Back -- View from the back.
        :param align_active: Align Active, Align to the active objects axis (optional)
        :param relative: Relative, Rotate relative to the current orientation (optional)
        :return: Result of the operator call.
    """

def view_camera(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Toggle the camera view

    :return: Result of the operator call.
    """

def view_center_camera(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Center the camera view, resizing the view to fit its bounds

    :return: Result of the operator call.
    """

def view_center_cursor(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Center the view so that the cursor is in the middle of the view

    :return: Result of the operator call.
    """

def view_center_lock(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Center the view lock offset

    :return: Result of the operator call.
    """

def view_center_pick(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Center the view to the Z-depth position under the mouse cursor

    :return: Result of the operator call.
    """

def view_lock_clear(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Clear all view locking

    :return: Result of the operator call.
    """

def view_lock_to_active(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Lock the view to the active object/bone

    :return: Result of the operator call.
    """

def view_orbit(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    angle: float | None = 0.0,
    type: typing.Literal["ORBITLEFT", "ORBITRIGHT", "ORBITUP", "ORBITDOWN"]
    | None = "ORBITLEFT",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Orbit the view

        :param angle: Roll, (in [-inf, inf], optional)
        :param type: Orbit, Direction of View Orbit (optional)

    ORBITLEFT
    Orbit Left -- Orbit the view around to the left.

    ORBITRIGHT
    Orbit Right -- Orbit the view around to the right.

    ORBITUP
    Orbit Up -- Orbit the view up.

    ORBITDOWN
    Orbit Down -- Orbit the view down.
        :return: Result of the operator call.
    """

def view_pan(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: typing.Literal["PANLEFT", "PANRIGHT", "PANUP", "PANDOWN"] | None = "PANLEFT",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Pan the view in a given direction

        :param type: Pan, Direction of View Pan (optional)

    PANLEFT
    Pan Left -- Pan the view to the left.

    PANRIGHT
    Pan Right -- Pan the view to the right.

    PANUP
    Pan Up -- Pan the view up.

    PANDOWN
    Pan Down -- Pan the view down.
        :return: Result of the operator call.
    """

def view_persportho(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Switch the current view from perspective/orthographic projection

    :return: Result of the operator call.
    """

def view_roll(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    angle: float | None = 0.0,
    type: typing.Literal["ANGLE", "LEFT", "RIGHT"] | None = "ANGLE",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Roll the view

        :param angle: Roll, (in [-inf, inf], optional)
        :param type: Roll Angle Source, How roll angle is calculated (optional)

    ANGLE
    Roll Angle -- Roll the view using an angle value.

    LEFT
    Roll Left -- Roll the view around to the left.

    RIGHT
    Roll Right -- Roll the view around to the right.
        :return: Result of the operator call.
    """

def view_selected(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    use_all_regions: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Move the view to the selection center

    :param use_all_regions: All Regions, View selected for all regions (optional)
    :return: Result of the operator call.
    """

def walk(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Interactively walk around the scene

    :return: Result of the operator call.
    """

def zoom(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    mx: int | None = 0,
    my: int | None = 0,
    delta: int | None = 0,
    use_cursor_init: bool | None = True,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Zoom in/out in the view

    :param mx: Region Position X, (in [0, inf], optional)
    :param my: Region Position Y, (in [0, inf], optional)
    :param delta: Delta, (in [-inf, inf], optional)
    :param use_cursor_init: Use Mouse Position, Allow the initial mouse position to be used (optional)
    :return: Result of the operator call.
    """

def zoom_border(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    xmin: int | None = 0,
    xmax: int | None = 0,
    ymin: int | None = 0,
    ymax: int | None = 0,
    wait_for_input: bool | None = True,
    zoom_out: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Zoom in the view to the nearest object contained in the border

    :param xmin: X Min, (in [-inf, inf], optional)
    :param xmax: X Max, (in [-inf, inf], optional)
    :param ymin: Y Min, (in [-inf, inf], optional)
    :param ymax: Y Max, (in [-inf, inf], optional)
    :param wait_for_input: Wait for Input, (optional)
    :param zoom_out: Zoom Out, (optional)
    :return: Result of the operator call.
    """

def zoom_camera_1_to_1(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Match the camera to 1:1 to the render output

    :return: Result of the operator call.
    """
