import typing
import collections.abc
import typing_extensions
import numpy.typing as npt
import bpy.ops
import bpy.stub_internal.rna_enums
import bpy.types

class _CLS_bone_select_menu(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        name: str | None = "",
        extend: bool | None = False,
        deselect: bool | None = False,
        toggle: bool | None = False,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Menu bone selection

        :param execution_context:
        :param undo:
        :param name: Bone Name, (optional)
        :param extend: Extend, (optional)
        :param deselect: Deselect, (optional)
        :param toggle: Toggle, (optional)
        :return: Result of the operator call.
        """

class _CLS_camera_background_image_add(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        filepath: str | None = "",
        relative_path: bool | None = True,
        name: str = "",
        session_uid: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Add a new background image to the active camera

        :param execution_context:
        :param undo:
        :param filepath: Filepath, Path to image file (optional, never None, blend relative // prefix supported)
        :param relative_path: Relative Path, Select the file relative to the blend file (optional)
        :param name: Name, Name of the data-block to use by the operator (optional, never None)
        :param session_uid: Session UID, Session UID of the data-block to use by the operator (in [-inf, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_camera_background_image_remove(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        index: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Remove a background image from the camera

        :param execution_context:
        :param undo:
        :param index: Index, Background image index to remove (in [0, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_camera_to_view(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Set camera view to active view

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_camera_to_view_selected(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Move the camera so selected objects are framed

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_clear_render_border(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Clear the boundaries of the border render and disable border render

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_clip_border(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        xmin: int | None = 0,
        xmax: int | None = 0,
        ymin: int | None = 0,
        ymax: int | None = 0,
        wait_for_input: bool | None = True,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Set the view clipping region

        :param execution_context:
        :param undo:
        :param xmin: X Min, (in [-inf, inf], optional)
        :param xmax: X Max, (in [-inf, inf], optional)
        :param ymin: Y Min, (in [-inf, inf], optional)
        :param ymax: Y Max, (in [-inf, inf], optional)
        :param wait_for_input: Wait for Input, (optional)
        :return: Result of the operator call.
        """

class _CLS_copybuffer(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Copy the selected objects to the internal clipboard

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_cursor3d(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        use_depth: bool | None = True,
        orientation: typing.Literal["NONE", "VIEW", "XFORM", "GEOM"] | None = "VIEW",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Set the location of the 3D cursor

                :param execution_context:
                :param undo:
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

class _CLS_dolly(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        mx: int | None = 0,
        my: int | None = 0,
        delta: int | None = 0,
        use_cursor_init: bool | None = True,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Dolly in/out in the view

        :param execution_context:
        :param undo:
        :param mx: Region Position X, (in [0, inf], optional)
        :param my: Region Position Y, (in [0, inf], optional)
        :param delta: Delta, (in [-inf, inf], optional)
        :param use_cursor_init: Use Mouse Position, Allow the initial mouse position to be used (optional)
        :return: Result of the operator call.
        """

class _CLS_drop_world(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        name: str = "",
        session_uid: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Drop a world into the scene

        :param execution_context:
        :param undo:
        :param name: Name, Name of the data-block to use by the operator (optional, never None)
        :param session_uid: Session UID, Session UID of the data-block to use by the operator (in [-inf, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_edit_mesh_extrude_individual_move(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Extrude each individual face separately along local normals

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_edit_mesh_extrude_manifold_normal(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Extrude manifold region along normals

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_edit_mesh_extrude_move_normal(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        dissolve_and_intersect: bool | None = False,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Extrude region together along the average normal

        :param execution_context:
        :param undo:
        :param dissolve_and_intersect: Dissolve and Intersect, Dissolves adjacent faces and intersects new geometry (optional)
        :return: Result of the operator call.
        """

class _CLS_edit_mesh_extrude_move_shrink_fatten(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Extrude region together along local normals

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_fly(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Interactively fly around the scene

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_interactive_add(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
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
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Interactively add an object

                :param execution_context:
                :param undo:
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

class _CLS_localview(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        frame_selected: bool | None = True,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Toggle display of selected object(s) separately and centered in view

        :param execution_context:
        :param undo:
        :param frame_selected: Frame Selected, Move the view to frame the selected objects (optional)
        :return: Result of the operator call.
        """

class _CLS_localview_remove_from(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Move selected objects out of local view

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_move(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        use_cursor_init: bool | None = True,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Move the view

        :param execution_context:
        :param undo:
        :param use_cursor_init: Use Mouse Position, Allow the initial mouse position to be used (optional)
        :return: Result of the operator call.
        """

class _CLS_navigate(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Interactively navigate around the scene (uses the mode (walk/fly) preference)

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_ndof_all(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Pan and rotate the view with the 3D mouse

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_ndof_orbit(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Orbit the view using the 3D mouse

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_ndof_orbit_zoom(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Orbit and zoom the view using the 3D mouse

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_ndof_pan(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Pan the view with the 3D mouse

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_object_as_camera(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Set the active object as the active camera for this view or scene

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_object_mode_pie_or_toggle(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Undocumented, consider contributing.

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_pastebuffer(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        autoselect: bool | None = True,
        active_collection: bool | None = True,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Paste objects from the internal clipboard

        :param execution_context:
        :param undo:
        :param autoselect: Select, Select pasted objects (optional)
        :param active_collection: Active Collection, Put pasted objects in the active collection (optional)
        :return: Result of the operator call.
        """

class _CLS_render_border(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        xmin: int | None = 0,
        xmax: int | None = 0,
        ymin: int | None = 0,
        ymax: int | None = 0,
        wait_for_input: bool | None = True,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Set the boundaries of the border render and enable border render

        :param execution_context:
        :param undo:
        :param xmin: X Min, (in [-inf, inf], optional)
        :param xmax: X Max, (in [-inf, inf], optional)
        :param ymin: Y Min, (in [-inf, inf], optional)
        :param ymax: Y Max, (in [-inf, inf], optional)
        :param wait_for_input: Wait for Input, (optional)
        :return: Result of the operator call.
        """

class _CLS_rotate(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        use_cursor_init: bool | None = True,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Rotate the view

        :param execution_context:
        :param undo:
        :param use_cursor_init: Use Mouse Position, Allow the initial mouse position to be used (optional)
        :return: Result of the operator call.
        """

class _CLS_ruler_add(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Add ruler

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_ruler_remove(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Undocumented, consider contributing.

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_select(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
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
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Select and activate item(s)

        :param execution_context:
        :param undo:
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

class _CLS_select_box(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
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
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Select items using box selection

                :param execution_context:
                :param undo:
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

class _CLS_select_circle(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        x: int | None = 0,
        y: int | None = 0,
        radius: int | None = 25,
        wait_for_input: bool | None = True,
        mode: typing.Literal["SET", "ADD", "SUB"] | None = "SET",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Select items using circle selection

                :param execution_context:
                :param undo:
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

class _CLS_select_lasso(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        path: bpy.types.bpy_prop_collection[bpy.types.OperatorMousePath] | None = None,
        use_smooth_stroke: bool | None = False,
        smooth_stroke_factor: float | None = 0.75,
        smooth_stroke_radius: int | None = 35,
        mode: typing.Literal["SET", "ADD", "SUB", "XOR", "AND"] | None = "SET",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Select items using lasso selection

                :param execution_context:
                :param undo:
                :param path: Path, (optional)
                :param use_smooth_stroke: Stabilize Stroke, Selection lags behind mouse and follows a smoother path (optional)
                :param smooth_stroke_factor: Smooth Stroke Factor, Higher values give a smoother stroke (in [0.5, 0.99], optional)
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

class _CLS_select_menu(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        name: str | None = "",
        extend: bool | None = False,
        deselect: bool | None = False,
        toggle: bool | None = False,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Menu object selection

        :param execution_context:
        :param undo:
        :param name: Object Name, (optional)
        :param extend: Extend, (optional)
        :param deselect: Deselect, (optional)
        :param toggle: Toggle, (optional)
        :return: Result of the operator call.
        """

class _CLS_smoothview(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Undocumented, consider contributing.

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_snap_cursor_to_active(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Snap 3D cursor to the active item

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_snap_cursor_to_center(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Snap 3D cursor to the world origin

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_snap_cursor_to_grid(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Snap 3D cursor to the nearest grid division

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_snap_cursor_to_selected(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Snap 3D cursor to the middle of the selected item(s)

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_snap_selected_to_active(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Snap selected item(s) to the active item

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_snap_selected_to_cursor(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        use_offset: bool | None = True,
        use_rotation: bool | None = False,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Snap selected item(s) to the 3D cursor

        :param execution_context:
        :param undo:
        :param use_offset: Offset, If the selection should be snapped as a whole or by each object center (optional)
        :param use_rotation: Rotation, If the selection should be rotated to match the cursor (optional)
        :return: Result of the operator call.
        """

class _CLS_snap_selected_to_grid(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Snap selected item(s) to their nearest grid division

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_toggle_matcap_flip(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Flip MatCap

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_toggle_shading(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        type: typing.Literal["WIREFRAME", "SOLID", "MATERIAL", "RENDERED"]
        | None = "WIREFRAME",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Toggle shading type in 3D viewport

                :param execution_context:
                :param undo:
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

class _CLS_toggle_xray(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Transparent scene display. Allow selecting through items

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_transform_gizmo_set(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        extend: bool | None = False,
        type: set[typing.Literal["TRANSLATE", "ROTATE", "SCALE"]] | None = set(),
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Set the current transform gizmo

        :param execution_context:
        :param undo:
        :param extend: Extend, (optional)
        :param type: Type, (optional)
        :return: Result of the operator call.
        """

class _CLS_view_all(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        use_all_regions: bool | None = False,
        center: bool | None = False,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """View all objects in scene

        :param execution_context:
        :param undo:
        :param use_all_regions: All Regions, View selected for all regions (optional)
        :param center: Center, (optional)
        :return: Result of the operator call.
        """

class _CLS_view_axis(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        type: typing.Literal["LEFT", "RIGHT", "BOTTOM", "TOP", "FRONT", "BACK"]
        | None = "LEFT",
        align_active: bool | None = False,
        relative: bool | None = False,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Use a preset viewpoint

                :param execution_context:
                :param undo:
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

class _CLS_view_camera(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Toggle the camera view

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_view_center_camera(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Center the camera view, resizing the view to fit its bounds

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_view_center_cursor(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Center the view so that the cursor is in the middle of the view

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_view_center_lock(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Center the view lock offset

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_view_center_pick(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Center the view to the Z-depth position under the mouse cursor

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_view_lock_clear(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Clear all view locking

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_view_lock_to_active(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Lock the view to the active object/bone

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_view_orbit(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        angle: float | None = 0.0,
        type: typing.Literal["ORBITLEFT", "ORBITRIGHT", "ORBITUP", "ORBITDOWN"]
        | None = "ORBITLEFT",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Orbit the view

                :param execution_context:
                :param undo:
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

class _CLS_view_pan(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        type: typing.Literal["PANLEFT", "PANRIGHT", "PANUP", "PANDOWN"]
        | None = "PANLEFT",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Pan the view in a given direction

                :param execution_context:
                :param undo:
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

class _CLS_view_persportho(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Switch the current view from perspective/orthographic projection

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_view_roll(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        angle: float | None = 0.0,
        type: typing.Literal["ANGLE", "LEFT", "RIGHT"] | None = "ANGLE",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Roll the view

                :param execution_context:
                :param undo:
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

class _CLS_view_selected(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        use_all_regions: bool | None = False,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Move the view to the selection center

        :param execution_context:
        :param undo:
        :param use_all_regions: All Regions, View selected for all regions (optional)
        :return: Result of the operator call.
        """

class _CLS_walk(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Interactively walk around the scene

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_zoom(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        mx: int | None = 0,
        my: int | None = 0,
        delta: int | None = 0,
        use_cursor_init: bool | None = True,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Zoom in/out in the view

        :param execution_context:
        :param undo:
        :param mx: Region Position X, (in [0, inf], optional)
        :param my: Region Position Y, (in [0, inf], optional)
        :param delta: Delta, (in [-inf, inf], optional)
        :param use_cursor_init: Use Mouse Position, Allow the initial mouse position to be used (optional)
        :return: Result of the operator call.
        """

class _CLS_zoom_border(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
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
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Zoom in the view to the nearest object contained in the border

        :param execution_context:
        :param undo:
        :param xmin: X Min, (in [-inf, inf], optional)
        :param xmax: X Max, (in [-inf, inf], optional)
        :param ymin: Y Min, (in [-inf, inf], optional)
        :param ymax: Y Max, (in [-inf, inf], optional)
        :param wait_for_input: Wait for Input, (optional)
        :param zoom_out: Zoom Out, (optional)
        :return: Result of the operator call.
        """

class _CLS_zoom_camera_1_to_1(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Match the camera to 1:1 to the render output

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

bone_select_menu: _CLS_bone_select_menu

camera_background_image_add: _CLS_camera_background_image_add

camera_background_image_remove: _CLS_camera_background_image_remove

camera_to_view: _CLS_camera_to_view

camera_to_view_selected: _CLS_camera_to_view_selected

clear_render_border: _CLS_clear_render_border

clip_border: _CLS_clip_border

copybuffer: _CLS_copybuffer

cursor3d: _CLS_cursor3d

dolly: _CLS_dolly

drop_world: _CLS_drop_world

edit_mesh_extrude_individual_move: _CLS_edit_mesh_extrude_individual_move

edit_mesh_extrude_manifold_normal: _CLS_edit_mesh_extrude_manifold_normal

edit_mesh_extrude_move_normal: _CLS_edit_mesh_extrude_move_normal

edit_mesh_extrude_move_shrink_fatten: _CLS_edit_mesh_extrude_move_shrink_fatten

fly: _CLS_fly

interactive_add: _CLS_interactive_add

localview: _CLS_localview

localview_remove_from: _CLS_localview_remove_from

move: _CLS_move

navigate: _CLS_navigate

ndof_all: _CLS_ndof_all

ndof_orbit: _CLS_ndof_orbit

ndof_orbit_zoom: _CLS_ndof_orbit_zoom

ndof_pan: _CLS_ndof_pan

object_as_camera: _CLS_object_as_camera

object_mode_pie_or_toggle: _CLS_object_mode_pie_or_toggle

pastebuffer: _CLS_pastebuffer

render_border: _CLS_render_border

rotate: _CLS_rotate

ruler_add: _CLS_ruler_add

ruler_remove: _CLS_ruler_remove

select: _CLS_select

select_box: _CLS_select_box

select_circle: _CLS_select_circle

select_lasso: _CLS_select_lasso

select_menu: _CLS_select_menu

smoothview: _CLS_smoothview

snap_cursor_to_active: _CLS_snap_cursor_to_active

snap_cursor_to_center: _CLS_snap_cursor_to_center

snap_cursor_to_grid: _CLS_snap_cursor_to_grid

snap_cursor_to_selected: _CLS_snap_cursor_to_selected

snap_selected_to_active: _CLS_snap_selected_to_active

snap_selected_to_cursor: _CLS_snap_selected_to_cursor

snap_selected_to_grid: _CLS_snap_selected_to_grid

toggle_matcap_flip: _CLS_toggle_matcap_flip

toggle_shading: _CLS_toggle_shading

toggle_xray: _CLS_toggle_xray

transform_gizmo_set: _CLS_transform_gizmo_set

view_all: _CLS_view_all

view_axis: _CLS_view_axis

view_camera: _CLS_view_camera

view_center_camera: _CLS_view_center_camera

view_center_cursor: _CLS_view_center_cursor

view_center_lock: _CLS_view_center_lock

view_center_pick: _CLS_view_center_pick

view_lock_clear: _CLS_view_lock_clear

view_lock_to_active: _CLS_view_lock_to_active

view_orbit: _CLS_view_orbit

view_pan: _CLS_view_pan

view_persportho: _CLS_view_persportho

view_roll: _CLS_view_roll

view_selected: _CLS_view_selected

walk: _CLS_walk

zoom: _CLS_zoom

zoom_border: _CLS_zoom_border

zoom_camera_1_to_1: _CLS_zoom_camera_1_to_1
