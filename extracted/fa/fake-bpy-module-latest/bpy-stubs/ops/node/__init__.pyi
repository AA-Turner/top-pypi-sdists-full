import typing
import collections.abc
import typing_extensions
import numpy.typing as npt
import bl_operators.node
import bpy.stub_internal.rna_enums
import bpy.types

def activate_viewer(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Activate selected viewer node in compositor and geometry nodes

    :return: Result of the operator call.
    """

def add_closure_zone(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    settings: bpy.types.bpy_prop_collection[bl_operators.node.NodeSetting]
    | None = None,
    use_transform: bool | None = False,
    offset: collections.abc.Sequence[float] | None = (150.0, 0.0),
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add a Closure zone

    :param settings: Settings, Settings to be applied on the newly created node (optional)
    :param use_transform: Use Transform, Start transform operator after inserting the node (optional)
    :param offset: Offset, Offset of nodes from the cursor when added (array of 2 items, in [-inf, inf], optional)
    :return: Result of the operator call.
    """

def add_collection(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    name: str = "",
    session_uid: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add a collection info node to the current node editor

    :param name: Name, Name of the data-block to use by the operator (optional, never None)
    :param session_uid: Session UID, Session UID of the data-block to use by the operator (in [-inf, inf], optional)
    :return: Result of the operator call.
    """

def add_color(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    color: collections.abc.Sequence[float] | None = (0.0, 0.0, 0.0, 0.0),
    gamma: bool | None = False,
    has_alpha: bool | None = False,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add a color node to the current node editor

    :param color: Color, Source color (array of 4 items, in [0, inf], optional)
    :param gamma: Gamma Corrected, The source color is gamma corrected (optional)
    :param has_alpha: Has Alpha, The source color contains an Alpha component (optional)
    :return: Result of the operator call.
    """

def add_empty_group(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    settings: bpy.types.bpy_prop_collection[bl_operators.node.NodeSetting]
    | None = None,
    use_transform: bool | None = False,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add a group node with an empty group

    :param settings: Settings, Settings to be applied on the newly created node (optional)
    :param use_transform: Use Transform, Start transform operator after inserting the node (optional)
    :return: Result of the operator call.
    """

def add_foreach_geometry_element_zone(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    settings: bpy.types.bpy_prop_collection[bl_operators.node.NodeSetting]
    | None = None,
    use_transform: bool | None = False,
    offset: collections.abc.Sequence[float] | None = (150.0, 0.0),
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add a For Each Geometry Element zone that allows executing nodes e.g. for each vertex separately

    :param settings: Settings, Settings to be applied on the newly created node (optional)
    :param use_transform: Use Transform, Start transform operator after inserting the node (optional)
    :param offset: Offset, Offset of nodes from the cursor when added (array of 2 items, in [-inf, inf], optional)
    :return: Result of the operator call.
    """

def add_group(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    name: str = "",
    session_uid: int | None = 0,
    show_datablock_in_node: bool | None = True,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add an existing node group to the current node editor

    :param name: Name, Name of the data-block to use by the operator (optional, never None)
    :param session_uid: Session UID, Session UID of the data-block to use by the operator (in [-inf, inf], optional)
    :param show_datablock_in_node: Show the data-block selector in the node, (optional)
    :return: Result of the operator call.
    """

def add_group_asset(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    asset_library_type: typing.Literal[
        bpy.stub_internal.rna_enums.AssetLibraryTypeItems
    ]
    | None = "LOCAL",
    asset_library_identifier: str = "",
    relative_asset_identifier: str = "",
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add a node group asset to the active node tree

    :param asset_library_type: Asset Library Type, (optional)
    :param asset_library_identifier: Asset Library Identifier, (optional, never None)
    :param relative_asset_identifier: Relative Asset Identifier, (optional, never None)
    :return: Result of the operator call.
    """

def add_group_input_node(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    socket_identifier: str = "",
    panel_identifier: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add a Group Input node with selected sockets to the current node editor

    :param socket_identifier: Socket Identifier, Socket to include in the added group input/output node (optional, never None)
    :param panel_identifier: Panel Identifier, Panel from which to add sockets to the added group input/output node (in [-inf, inf], optional)
    :return: Result of the operator call.
    """

def add_image(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    filepath: str = "",
    directory: str = "",
    files: bpy.types.bpy_prop_collection[bpy.types.OperatorFileListElement]
    | None = None,
    hide_props_region: bool | None = True,
    check_existing: bool | None = False,
    filter_blender: bool | None = False,
    filter_backup: bool | None = False,
    filter_image: bool | None = True,
    filter_movie: bool | None = True,
    filter_python: bool | None = False,
    filter_font: bool | None = False,
    filter_sound: bool | None = False,
    filter_text: bool | None = False,
    filter_archive: bool | None = False,
    filter_btx: bool | None = False,
    filter_alembic: bool | None = False,
    filter_usd: bool | None = False,
    filter_obj: bool | None = False,
    filter_volume: bool | None = False,
    filter_folder: bool | None = True,
    filter_blenlib: bool | None = False,
    filemode: int | None = 9,
    relative_path: bool | None = True,
    show_multiview: bool | None = False,
    use_multiview: bool | None = False,
    display_type: typing.Literal[
        "DEFAULT", "LIST_VERTICAL", "LIST_HORIZONTAL", "THUMBNAIL"
    ]
    | None = "DEFAULT",
    sort_method: typing.Literal[
        "DEFAULT",
        "FILE_SORT_ALPHA",
        "FILE_SORT_EXTENSION",
        "FILE_SORT_TIME",
        "FILE_SORT_SIZE",
        "ASSET_CATALOG",
    ]
    | None = "",
    name: str = "",
    session_uid: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add a image/movie file as node to the current node editor

        :param filepath: File Path, Path to file (optional, never None)
        :param directory: Directory, Directory of the file (optional, never None)
        :param files: Files, (optional)
        :param hide_props_region: Hide Operator Properties, Collapse the region displaying the operator settings (optional)
        :param check_existing: Check Existing, Check and warn on overwriting existing files (optional)
        :param filter_blender: Filter .blend files, (optional)
        :param filter_backup: Filter backup .blend files, (optional)
        :param filter_image: Filter image files, (optional)
        :param filter_movie: Filter movie files, (optional)
        :param filter_python: Filter Python files, (optional)
        :param filter_font: Filter font files, (optional)
        :param filter_sound: Filter sound files, (optional)
        :param filter_text: Filter text files, (optional)
        :param filter_archive: Filter archive files, (optional)
        :param filter_btx: Filter btx files, (optional)
        :param filter_alembic: Filter Alembic files, (optional)
        :param filter_usd: Filter USD files, (optional)
        :param filter_obj: Filter OBJ files, (optional)
        :param filter_volume: Filter OpenVDB volume files, (optional)
        :param filter_folder: Filter folders, (optional)
        :param filter_blenlib: Filter Blender IDs, (optional)
        :param filemode: File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file (in [1, 9], optional)
        :param relative_path: Relative Path, Select the file relative to the blend file (optional)
        :param show_multiview: Enable Multi-View, (optional)
        :param use_multiview: Use Multi-View, (optional)
        :param display_type: Display Type, (optional)

    DEFAULT
    Default -- Automatically determine display type for files.

    LIST_VERTICAL
    Short List -- Display files as short list.

    LIST_HORIZONTAL
    Long List -- Display files as a detailed list.

    THUMBNAIL
    Thumbnails -- Display files as thumbnails.
        :param sort_method: File sorting mode, (optional)

    DEFAULT
    Default -- Automatically determine sort method for files.

    FILE_SORT_ALPHA
    Name -- Sort the file list alphabetically.

    FILE_SORT_EXTENSION
    Extension -- Sort the file list by extension/type.

    FILE_SORT_TIME
    Modified Date -- Sort files by modification time.

    FILE_SORT_SIZE
    Size -- Sort files by size.

    ASSET_CATALOG
    Asset Catalog -- Sort the asset list so that assets in the same catalog are kept together. Within a single catalog, assets are ordered by name. The catalogs are in order of the flattened catalog hierarchy..
        :param name: Name, Name of the data-block to use by the operator (optional, never None)
        :param session_uid: Session UID, Session UID of the data-block to use by the operator (in [-inf, inf], optional)
        :return: Result of the operator call.
    """

def add_import_node(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    directory: str = "",
    files: bpy.types.bpy_prop_collection[bpy.types.OperatorFileListElement]
    | None = None,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add an import node to the node tree

    :param directory: Directory, Directory of the file (optional, never None)
    :param files: Files, (optional)
    :return: Result of the operator call.
    """

def add_mask(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    name: str = "",
    session_uid: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add a mask node to the current node editor

    :param name: Name, Name of the data-block to use by the operator (optional, never None)
    :param session_uid: Session UID, Session UID of the data-block to use by the operator (in [-inf, inf], optional)
    :return: Result of the operator call.
    """

def add_material(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    name: str = "",
    session_uid: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add a material node to the current node editor

    :param name: Name, Name of the data-block to use by the operator (optional, never None)
    :param session_uid: Session UID, Session UID of the data-block to use by the operator (in [-inf, inf], optional)
    :return: Result of the operator call.
    """

def add_node(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    settings: bpy.types.bpy_prop_collection[bl_operators.node.NodeSetting]
    | None = None,
    use_transform: bool | None = False,
    type: str = "",
    visible_output: str = "",
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add a node to the active tree

    :param settings: Settings, Settings to be applied on the newly created node (optional)
    :param use_transform: Use Transform, Start transform operator after inserting the node (optional)
    :param type: Node Type, Node type (optional, never None)
    :param visible_output: Output Name, If provided, all outputs that are named differently will be hidden (optional, never None)
    :return: Result of the operator call.
    """

def add_object(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    name: str = "",
    session_uid: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add an object info node to the current node editor

    :param name: Name, Name of the data-block to use by the operator (optional, never None)
    :param session_uid: Session UID, Session UID of the data-block to use by the operator (in [-inf, inf], optional)
    :return: Result of the operator call.
    """

def add_repeat_zone(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    settings: bpy.types.bpy_prop_collection[bl_operators.node.NodeSetting]
    | None = None,
    use_transform: bool | None = False,
    offset: collections.abc.Sequence[float] | None = (150.0, 0.0),
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add a repeat zone that allows executing nodes a dynamic number of times

    :param settings: Settings, Settings to be applied on the newly created node (optional)
    :param use_transform: Use Transform, Start transform operator after inserting the node (optional)
    :param offset: Offset, Offset of nodes from the cursor when added (array of 2 items, in [-inf, inf], optional)
    :return: Result of the operator call.
    """

def add_reroute(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    path: bpy.types.bpy_prop_collection[bpy.types.OperatorMousePath] | None = None,
    cursor: int | None = 11,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add a reroute node

    :param path: Path, (optional)
    :param cursor: Cursor, (in [0, inf], optional)
    :return: Result of the operator call.
    """

def add_simulation_zone(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    settings: bpy.types.bpy_prop_collection[bl_operators.node.NodeSetting]
    | None = None,
    use_transform: bool | None = False,
    offset: collections.abc.Sequence[float] | None = (150.0, 0.0),
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add simulation zone input and output nodes to the active tree

    :param settings: Settings, Settings to be applied on the newly created node (optional)
    :param use_transform: Use Transform, Start transform operator after inserting the node (optional)
    :param offset: Offset, Offset of nodes from the cursor when added (array of 2 items, in [-inf, inf], optional)
    :return: Result of the operator call.
    """

def add_zone(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    settings: bpy.types.bpy_prop_collection[bl_operators.node.NodeSetting]
    | None = None,
    use_transform: bool | None = False,
    offset: collections.abc.Sequence[float] | None = (150.0, 0.0),
    input_node_type: str = "",
    output_node_type: str = "",
    add_default_geometry_link: bool | None = False,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Undocumented, consider contributing.

    :param settings: Settings, Settings to be applied on the newly created node (optional)
    :param use_transform: Use Transform, Start transform operator after inserting the node (optional)
    :param offset: Offset, Offset of nodes from the cursor when added (array of 2 items, in [-inf, inf], optional)
    :param input_node_type: Input Node, Specifies the input node used by the created zone (optional, never None)
    :param output_node_type: Output Node, Specifies the output node used by the created zone (optional, never None)
    :param add_default_geometry_link: Add Geometry Link, When enabled, create a link between geometry sockets in this zone (optional)
    :return: Result of the operator call.
    """

def attach(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Attach active node to a frame

    :return: Result of the operator call.
    """

def backimage_fit(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Fit the background image to the view

    :return: Result of the operator call.
    """

def backimage_move(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Move node backdrop

    :return: Result of the operator call.
    """

def backimage_sample(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Use mouse to sample background image

    :return: Result of the operator call.
    """

def backimage_zoom(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    factor: float | None = 1.2,
    use_mouse_pos: bool | None = True,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Zoom in/out the background image

    :param factor: Factor, (in [0, 10], optional)
    :param use_mouse_pos: Use Mouse Position, Zoom to mouse position (optional)
    :return: Result of the operator call.
    """

def bake_node_item_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    node_identifier: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add item below active item

    :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
    :return: Result of the operator call.
    """

def bake_node_item_move(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    direction: typing.Literal["UP", "DOWN"] | None = "UP",
    node_identifier: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Move active item

    :param direction: Direction, Move direction (optional)
    :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
    :return: Result of the operator call.
    """

def bake_node_item_remove(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    node_identifier: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove active item

    :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
    :return: Result of the operator call.
    """

def capture_attribute_item_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    node_identifier: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add item below active item

    :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
    :return: Result of the operator call.
    """

def capture_attribute_item_move(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    direction: typing.Literal["UP", "DOWN"] | None = "UP",
    node_identifier: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Move active item

    :param direction: Direction, Move direction (optional)
    :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
    :return: Result of the operator call.
    """

def capture_attribute_item_remove(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    node_identifier: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove active item

    :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
    :return: Result of the operator call.
    """

def clear_viewer_border(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Clear the boundaries for viewer operations

    :return: Result of the operator call.
    """

def clipboard_copy(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Copy the selected nodes to the internal clipboard

    :return: Result of the operator call.
    """

def clipboard_paste(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    offset: collections.abc.Sequence[float] | None = (0.0, 0.0),
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Paste nodes from the internal clipboard to the active node tree

    :param offset: Location, The 2D view location for the center of the new nodes, or unchanged if not set (array of 2 items, in [-inf, inf], optional)
    :return: Result of the operator call.
    """

def closure_input_item_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    node_identifier: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add item below active item

    :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
    :return: Result of the operator call.
    """

def closure_input_item_move(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    direction: typing.Literal["UP", "DOWN"] | None = "UP",
    node_identifier: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Move active item

    :param direction: Direction, Move direction (optional)
    :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
    :return: Result of the operator call.
    """

def closure_input_item_remove(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    node_identifier: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove active item

    :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
    :return: Result of the operator call.
    """

def closure_output_item_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    node_identifier: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add item below active item

    :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
    :return: Result of the operator call.
    """

def closure_output_item_move(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    direction: typing.Literal["UP", "DOWN"] | None = "UP",
    node_identifier: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Move active item

    :param direction: Direction, Move direction (optional)
    :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
    :return: Result of the operator call.
    """

def closure_output_item_remove(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    node_identifier: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove active item

    :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
    :return: Result of the operator call.
    """

def collapse_hide_unused_toggle(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Toggle collapsed nodes and hide unused sockets

    :return: Result of the operator call.
    """

def combine_bundle_item_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    node_identifier: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add item below active item

    :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
    :return: Result of the operator call.
    """

def combine_bundle_item_move(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    direction: typing.Literal["UP", "DOWN"] | None = "UP",
    node_identifier: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Move active item

    :param direction: Direction, Move direction (optional)
    :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
    :return: Result of the operator call.
    """

def combine_bundle_item_remove(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    node_identifier: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove active item

    :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
    :return: Result of the operator call.
    """

def connect_to_output(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    run_in_geometry_nodes: bool | None = True,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Connect active node to the active output node of the node tree

    :param run_in_geometry_nodes: Run in Geometry Nodes Editor, (optional)
    :return: Result of the operator call.
    """

def cryptomatte_layer_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add a new input layer to a Cryptomatte node

    :return: Result of the operator call.
    """

def cryptomatte_layer_remove(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove layer from a Cryptomatte node

    :return: Result of the operator call.
    """

def deactivate_viewer(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Deactivate selected viewer node in geometry nodes

    :return: Result of the operator call.
    """

def default_group_width_set(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Set the width based on the parent group node in the current context

    :return: Result of the operator call.
    """

def delete(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove selected nodes

    :return: Result of the operator call.
    """

def delete_copy_reconnect(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    NODE_OT_clipboard_copy: dict[str, typing.Any] | None = {},
    NODE_OT_delete_reconnect: dict[str, typing.Any] | None = {},
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Copy nodes to clipboard, remove and reconnect them.

    :param NODE_OT_clipboard_copy: Copy to Clipboard, Copy the selected nodes to the internal clipboard (optional, `bpy.ops.node.clipboard_copy` keyword arguments)
    :param NODE_OT_delete_reconnect: Delete with Reconnect, Remove nodes and reconnect nodes as if deletion was muted (optional, `bpy.ops.node.delete_reconnect` keyword arguments)
    :return: Result of the operator call.
    """

def delete_reconnect(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove nodes and reconnect nodes as if deletion was muted

    :return: Result of the operator call.
    """

def detach(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Detach selected nodes from parents

    :return: Result of the operator call.
    """

def detach_translate_attach(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    NODE_OT_detach: dict[str, typing.Any] | None = {},
    TRANSFORM_OT_translate: dict[str, typing.Any] | None = {},
    NODE_OT_attach: dict[str, typing.Any] | None = {},
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Detach nodes, move and attach to frame

    :param NODE_OT_detach: Detach Nodes, Detach selected nodes from parents (optional, `bpy.ops.node.detach` keyword arguments)
    :param TRANSFORM_OT_translate: Move, Move selected items (optional, `bpy.ops.transform.translate` keyword arguments)
    :param NODE_OT_attach: Attach Nodes, Attach active node to a frame (optional, `bpy.ops.node.attach` keyword arguments)
    :return: Result of the operator call.
    """

def duplicate(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    keep_inputs: bool | None = False,
    linked: bool | None = True,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Duplicate selected nodes

    :param keep_inputs: Keep Inputs, Keep the input links to duplicated nodes (optional)
    :param linked: Linked, Duplicate node but not node trees, linking to the original data (optional)
    :return: Result of the operator call.
    """

def duplicate_compositing_modifier_node_group(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Duplicate the currently assigned compositing node group.

    :return: Result of the operator call.
    """

def duplicate_compositing_node_group(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Duplicate the currently assigned compositing node group.

    :return: Result of the operator call.
    """

def duplicate_move(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    NODE_OT_duplicate: dict[str, typing.Any] | None = {},
    NODE_OT_translate_attach: dict[str, typing.Any] | None = {},
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Duplicate selected nodes and move them

    :param NODE_OT_duplicate: Duplicate Nodes, Duplicate selected nodes (optional, `bpy.ops.node.duplicate` keyword arguments)
    :param NODE_OT_translate_attach: Move and Attach, Move nodes and attach to frame (optional, `bpy.ops.node.translate_attach` keyword arguments)
    :return: Result of the operator call.
    """

def duplicate_move_keep_inputs(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    NODE_OT_duplicate: dict[str, typing.Any] | None = {},
    NODE_OT_translate_attach: dict[str, typing.Any] | None = {},
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Duplicate selected nodes keeping input links and move them

    :param NODE_OT_duplicate: Duplicate Nodes, Duplicate selected nodes (optional, `bpy.ops.node.duplicate` keyword arguments)
    :param NODE_OT_translate_attach: Move and Attach, Move nodes and attach to frame (optional, `bpy.ops.node.translate_attach` keyword arguments)
    :return: Result of the operator call.
    """

def duplicate_move_linked(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    NODE_OT_duplicate: dict[str, typing.Any] | None = {},
    NODE_OT_translate_attach: dict[str, typing.Any] | None = {},
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Duplicate selected nodes, but not their node trees, and move them

    :param NODE_OT_duplicate: Duplicate Nodes, Duplicate selected nodes (optional, `bpy.ops.node.duplicate` keyword arguments)
    :param NODE_OT_translate_attach: Move and Attach, Move nodes and attach to frame (optional, `bpy.ops.node.translate_attach` keyword arguments)
    :return: Result of the operator call.
    """

def enum_definition_item_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    node_identifier: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add item below active item

    :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
    :return: Result of the operator call.
    """

def enum_definition_item_move(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    direction: typing.Literal["UP", "DOWN"] | None = "UP",
    node_identifier: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Move active item

    :param direction: Direction, Move direction (optional)
    :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
    :return: Result of the operator call.
    """

def enum_definition_item_remove(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    node_identifier: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove active item

    :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
    :return: Result of the operator call.
    """

def evaluate_closure_input_item_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    node_identifier: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add item below active item

    :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
    :return: Result of the operator call.
    """

def evaluate_closure_input_item_move(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    direction: typing.Literal["UP", "DOWN"] | None = "UP",
    node_identifier: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Move active item

    :param direction: Direction, Move direction (optional)
    :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
    :return: Result of the operator call.
    """

def evaluate_closure_input_item_remove(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    node_identifier: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove active item

    :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
    :return: Result of the operator call.
    """

def evaluate_closure_output_item_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    node_identifier: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add item below active item

    :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
    :return: Result of the operator call.
    """

def evaluate_closure_output_item_move(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    direction: typing.Literal["UP", "DOWN"] | None = "UP",
    node_identifier: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Move active item

    :param direction: Direction, Move direction (optional)
    :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
    :return: Result of the operator call.
    """

def evaluate_closure_output_item_remove(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    node_identifier: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove active item

    :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
    :return: Result of the operator call.
    """

def field_to_grid_item_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    node_identifier: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add item below active item

    :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
    :return: Result of the operator call.
    """

def field_to_grid_item_move(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    direction: typing.Literal["UP", "DOWN"] | None = "UP",
    node_identifier: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Move active item

    :param direction: Direction, Move direction (optional)
    :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
    :return: Result of the operator call.
    """

def field_to_grid_item_remove(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    node_identifier: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove active item

    :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
    :return: Result of the operator call.
    """

def field_to_list_item_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    node_identifier: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add item below active item

    :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
    :return: Result of the operator call.
    """

def field_to_list_item_move(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    direction: typing.Literal["UP", "DOWN"] | None = "UP",
    node_identifier: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Move active item

    :param direction: Direction, Move direction (optional)
    :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
    :return: Result of the operator call.
    """

def field_to_list_item_remove(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    node_identifier: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove active item

    :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
    :return: Result of the operator call.
    """

def file_output_item_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    node_identifier: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add item below active item

    :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
    :return: Result of the operator call.
    """

def file_output_item_move(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    direction: typing.Literal["UP", "DOWN"] | None = "UP",
    node_identifier: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Move active item

    :param direction: Direction, Move direction (optional)
    :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
    :return: Result of the operator call.
    """

def file_output_item_remove(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    node_identifier: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove active item

    :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
    :return: Result of the operator call.
    """

def find_node(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Search for a node by name and focus and select it

    :return: Result of the operator call.
    """

def foreach_geometry_element_zone_generation_item_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    node_identifier: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add item below active item

    :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
    :return: Result of the operator call.
    """

def foreach_geometry_element_zone_generation_item_move(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    direction: typing.Literal["UP", "DOWN"] | None = "UP",
    node_identifier: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Move active item

    :param direction: Direction, Move direction (optional)
    :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
    :return: Result of the operator call.
    """

def foreach_geometry_element_zone_generation_item_remove(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    node_identifier: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove active item

    :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
    :return: Result of the operator call.
    """

def foreach_geometry_element_zone_input_item_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    node_identifier: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add item below active item

    :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
    :return: Result of the operator call.
    """

def foreach_geometry_element_zone_input_item_move(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    direction: typing.Literal["UP", "DOWN"] | None = "UP",
    node_identifier: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Move active item

    :param direction: Direction, Move direction (optional)
    :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
    :return: Result of the operator call.
    """

def foreach_geometry_element_zone_input_item_remove(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    node_identifier: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove active item

    :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
    :return: Result of the operator call.
    """

def foreach_geometry_element_zone_main_item_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    node_identifier: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add item below active item

    :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
    :return: Result of the operator call.
    """

def foreach_geometry_element_zone_main_item_move(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    direction: typing.Literal["UP", "DOWN"] | None = "UP",
    node_identifier: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Move active item

    :param direction: Direction, Move direction (optional)
    :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
    :return: Result of the operator call.
    """

def foreach_geometry_element_zone_main_item_remove(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    node_identifier: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove active item

    :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
    :return: Result of the operator call.
    """

def format_string_item_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    node_identifier: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add item below active item

    :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
    :return: Result of the operator call.
    """

def format_string_item_move(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    direction: typing.Literal["UP", "DOWN"] | None = "UP",
    node_identifier: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Move active item

    :param direction: Direction, Move direction (optional)
    :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
    :return: Result of the operator call.
    """

def format_string_item_remove(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    node_identifier: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove active item

    :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
    :return: Result of the operator call.
    """

def geometry_nodes_viewer_item_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    node_identifier: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add item below active item

    :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
    :return: Result of the operator call.
    """

def geometry_nodes_viewer_item_move(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    direction: typing.Literal["UP", "DOWN"] | None = "UP",
    node_identifier: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Move active item

    :param direction: Direction, Move direction (optional)
    :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
    :return: Result of the operator call.
    """

def geometry_nodes_viewer_item_remove(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    node_identifier: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove active item

    :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
    :return: Result of the operator call.
    """

def gltf_settings_node_operator(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add a node to the active tree for glTF export

    :return: Result of the operator call.
    """

def group_edit(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    exit: bool | None = False,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Edit node group

    :param exit: Exit, (optional)
    :return: Result of the operator call.
    """

def group_enter_exit(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Enter or exit node group based on cursor location

    :return: Result of the operator call.
    """

def group_insert(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Insert selected nodes into a node group

    :return: Result of the operator call.
    """

def group_make(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Make group from selected nodes

    :return: Result of the operator call.
    """

def group_separate(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: typing.Literal["COPY", "MOVE"] | None = "COPY",
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Separate selected nodes from the node group

        :param type: Type, (optional)

    COPY
    Copy -- Copy to parent node tree, keep group intact.

    MOVE
    Move -- Move to parent node tree, remove from group.
        :return: Result of the operator call.
    """

def group_ungroup(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Ungroup selected nodes

    :return: Result of the operator call.
    """

def hide_socket_toggle(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Toggle unused node socket display

    :return: Result of the operator call.
    """

def hide_toggle(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Toggle collapsing of selected nodes

    :return: Result of the operator call.
    """

def index_switch_item_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    node_identifier: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add an item to the index switch

    :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
    :return: Result of the operator call.
    """

def index_switch_item_remove(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    index: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove an item from the index switch

    :param index: Index, Index to remove (in [0, inf], optional)
    :return: Result of the operator call.
    """

def insert_offset(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Automatically offset nodes on insertion

    :return: Result of the operator call.
    """

def interface_item_duplicate(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add a copy of the active item to the interface

    :return: Result of the operator call.
    """

def interface_item_make_panel_toggle(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Make the active boolean socket a toggle for its parent panel

    :return: Result of the operator call.
    """

def interface_item_new(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    item_type: typing.Literal["INPUT", "OUTPUT", "PANEL"] | None = "INPUT",
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add a new item to the interface

    :param item_type: Item Type, Type of the item to create (optional)
    :return: Result of the operator call.
    """

def interface_item_new_panel_toggle(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add a checkbox to the currently selected panel

    :return: Result of the operator call.
    """

def interface_item_remove(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove selected items from the interface

    :return: Result of the operator call.
    """

def interface_item_unlink_panel_toggle(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Make the panel toggle a stand-alone socket

    :return: Result of the operator call.
    """

def join(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Attach selected nodes to a new common frame

    :return: Result of the operator call.
    """

def join_named(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    NODE_OT_join: dict[str, typing.Any] | None = {},
    WM_OT_call_panel: dict[str, typing.Any] | None = {},
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Create a new frame node around the selected nodes and name it immediately

    :param NODE_OT_join: Join Nodes in Frame, Attach selected nodes to a new common frame (optional, `bpy.ops.node.join` keyword arguments)
    :param WM_OT_call_panel: Call Panel, Open a predefined panel (optional, `bpy.ops.wm.call_panel` keyword arguments)
    :return: Result of the operator call.
    """

def join_nodes(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Merge selected group input nodes into one if possible

    :return: Result of the operator call.
    """

def link(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    detach: bool | None = False,
    drag_start: collections.abc.Sequence[float] | None = (0.0, 0.0),
    inside_padding: float | None = 2.0,
    outside_padding: float | None = 0.0,
    speed_ramp: float | None = 1.0,
    max_speed: float | None = 26.0,
    delay: float | None = 0.5,
    zoom_influence: float | None = 0.5,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Use the mouse to create a link between two nodes

    :param detach: Detach, Detach and redirect existing links (optional)
    :param drag_start: Drag Start, The position of the mouse cursor at the start of the operation (array of 2 items, in [-6, 6], optional)
    :param inside_padding: Inside Padding, Inside distance in UI units from the edge of the region within which to start panning (in [0, 100], optional)
    :param outside_padding: Outside Padding, Outside distance in UI units from the edge of the region at which to stop panning (in [0, 100], optional)
    :param speed_ramp: Speed Ramp, Width of the zone in UI units where speed increases with distance from the edge (in [0, 100], optional)
    :param max_speed: Max Speed, Maximum speed in UI units per second (in [0, 10000], optional)
    :param delay: Delay, Delay in seconds before maximum speed is reached (in [0, 10], optional)
    :param zoom_influence: Zoom Influence, Influence of the zoom factor on scroll speed (in [0, 1], optional)
    :return: Result of the operator call.
    """

def link_drag_operation_test(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    find_link_operations: bool | None = False,
    link_operation_index: int | None = -1,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Run a node link-drag operation for testing

    :param find_link_operations: Find Link Operations, Write link operation names for the context socket the "link_operation_names" property of the node tree (optional)
    :param link_operation_index: Link Operation Index, Link operation to execute on the context socket (in [-1, inf], optional)
    :return: Result of the operator call.
    """

def link_make(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    replace: bool | None = False,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Make a link between selected output and input sockets

    :param replace: Replace, Replace socket connections with the new links (optional)
    :return: Result of the operator call.
    """

def link_viewer(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Link to viewer node

    :return: Result of the operator call.
    """

def links_cut(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    path: bpy.types.bpy_prop_collection[bpy.types.OperatorMousePath] | None = None,
    cursor: int | None = 15,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Use the mouse to cut (remove) some links

    :param path: Path, (optional)
    :param cursor: Cursor, (in [0, inf], optional)
    :return: Result of the operator call.
    """

def links_detach(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove all links to selected nodes, and try to connect neighbor nodes together

    :return: Result of the operator call.
    """

def links_mute(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    path: bpy.types.bpy_prop_collection[bpy.types.OperatorMousePath] | None = None,
    cursor: int | None = 39,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Use the mouse to mute links

    :param path: Path, (optional)
    :param cursor: Cursor, (in [0, inf], optional)
    :return: Result of the operator call.
    """

def move_detach_links(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    NODE_OT_links_detach: dict[str, typing.Any] | None = {},
    TRANSFORM_OT_translate: dict[str, typing.Any] | None = {},
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Move a node to detach links

    :param NODE_OT_links_detach: Detach Links, Remove all links to selected nodes, and try to connect neighbor nodes together (optional, `bpy.ops.node.links_detach` keyword arguments)
    :param TRANSFORM_OT_translate: Move, Move selected items (optional, `bpy.ops.transform.translate` keyword arguments)
    :return: Result of the operator call.
    """

def move_detach_links_release(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    NODE_OT_links_detach: dict[str, typing.Any] | None = {},
    NODE_OT_translate_attach: dict[str, typing.Any] | None = {},
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Move a node to detach links

    :param NODE_OT_links_detach: Detach Links, Remove all links to selected nodes, and try to connect neighbor nodes together (optional, `bpy.ops.node.links_detach` keyword arguments)
    :param NODE_OT_translate_attach: Move and Attach, Move nodes and attach to frame (optional, `bpy.ops.node.translate_attach` keyword arguments)
    :return: Result of the operator call.
    """

def mute_toggle(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Toggle muting of selected nodes

    :return: Result of the operator call.
    """

def new_compositing_node_group(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    name: str = "",
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Create a new compositing node group and initialize it with default nodes

    :param name: Name, (optional, never None)
    :return: Result of the operator call.
    """

def new_compositor_sequencer_node_group(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    name: str = "Sequencer Compositor Nodes",
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Create a new compositor node group for sequencer

    :param name: Name, (optional, never None)
    :return: Result of the operator call.
    """

def new_geometry_node_group_assign(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Create a new geometry node group and assign it to the active modifier

    :return: Result of the operator call.
    """

def new_geometry_node_group_tool(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Create a new geometry node group for a tool

    :return: Result of the operator call.
    """

def new_geometry_nodes_modifier(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Create a new modifier with a new geometry node group

    :return: Result of the operator call.
    """

def new_node_tree(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: str | None = "",
    name: str = "NodeTree",
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Create a new node tree

    :param type: Tree Type, (optional)
    :param name: Name, (optional, never None)
    :return: Result of the operator call.
    """

def node_color_preset_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    name: str = "",
    remove_name: bool | None = False,
    remove_active: bool | None = False,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add or remove a Node Color Preset

    :param name: Name, Name of the preset, used to make the path name (optional, never None)
    :param remove_name: remove_name, (optional)
    :param remove_active: remove_active, (optional)
    :return: Result of the operator call.
    """

def node_copy_color(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Copy color to all selected nodes

    :return: Result of the operator call.
    """

def options_toggle(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Toggle option buttons display for selected nodes

    :return: Result of the operator call.
    """

def parent_set(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Attach selected nodes

    :return: Result of the operator call.
    """

def preview_toggle(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Toggle preview display for selected nodes

    :return: Result of the operator call.
    """

def read_viewlayers(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Read all render layers of all used scenes

    :return: Result of the operator call.
    """

def render_changed(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Render current scene, when input nodes layer has been changed

    :return: Result of the operator call.
    """

def repeat_zone_item_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    node_identifier: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add item below active item

    :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
    :return: Result of the operator call.
    """

def repeat_zone_item_move(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    direction: typing.Literal["UP", "DOWN"] | None = "UP",
    node_identifier: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Move active item

    :param direction: Direction, Move direction (optional)
    :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
    :return: Result of the operator call.
    """

def repeat_zone_item_remove(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    node_identifier: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove active item

    :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
    :return: Result of the operator call.
    """

def resize(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Resize a node

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
    location: collections.abc.Sequence[int] | None = (0, 0),
    socket_select: bool | None = False,
    clear_viewer: bool | None = False,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select the node under the cursor

    :param extend: Extend, Extend selection instead of deselecting everything first (optional)
    :param deselect: Deselect, Remove from selection (optional)
    :param toggle: Toggle Selection, Toggle the selection (optional)
    :param deselect_all: Deselect On Nothing, Deselect all when nothing under the cursor (optional)
    :param select_passthrough: Only Select Unselected, Ignore the select action when the element is already selected (optional)
    :param location: Location, Mouse location (array of 2 items, in [-inf, inf], optional)
    :param socket_select: Socket Select, (optional)
    :param clear_viewer: Clear Viewer, Deactivate geometry nodes viewer when clicking in empty space (optional)
    :return: Result of the operator call.
    """

def select_all(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    action: typing.Literal["TOGGLE", "SELECT", "DESELECT", "INVERT"] | None = "TOGGLE",
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """(De)select all nodes

        :param action: Action, Selection action to execute (optional)

    TOGGLE
    Toggle -- Toggle selection for all elements.

    SELECT
    Select -- Select all elements.

    DESELECT
    Deselect -- Deselect all elements.

    INVERT
    Invert -- Invert selection of all elements.
        :return: Result of the operator call.
    """

def select_box(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    tweak: bool | None = False,
    xmin: int | None = 0,
    xmax: int | None = 0,
    ymin: int | None = 0,
    ymax: int | None = 0,
    wait_for_input: bool | None = True,
    mode: typing.Literal["SET", "ADD", "SUB"] | None = "SET",
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Use box selection to select nodes

        :param tweak: Tweak, Only activate when mouse is not over a node (useful for tweak gesture) (optional)
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
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Use circle selection to select nodes

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

def select_grouped(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    extend: bool | None = False,
    type: typing.Literal["TYPE", "COLOR", "PREFIX", "SUFFIX"] | None = "TYPE",
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select nodes with similar properties

    :param extend: Extend, Extend selection instead of deselecting everything first (optional)
    :param type: Type, (optional)
    :return: Result of the operator call.
    """

def select_lasso(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    tweak: bool | None = False,
    path: bpy.types.bpy_prop_collection[bpy.types.OperatorMousePath] | None = None,
    use_smooth_stroke: bool | None = False,
    smooth_stroke_factor: float | None = 0.75,
    smooth_stroke_radius: int | None = 35,
    mode: typing.Literal["SET", "ADD", "SUB"] | None = "SET",
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select nodes using lasso selection

        :param tweak: Tweak, Only activate when mouse is not over a node (useful for tweak gesture) (optional)
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
        :return: Result of the operator call.
    """

def select_link_viewer(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    NODE_OT_select: dict[str, typing.Any] | None = {},
    NODE_OT_link_viewer: dict[str, typing.Any] | None = {},
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select node and link it to a viewer node

    :param NODE_OT_select: Select, Select the node under the cursor (optional, `bpy.ops.node.select` keyword arguments)
    :param NODE_OT_link_viewer: Link to Viewer Node, Link to viewer node (optional, `bpy.ops.node.link_viewer` keyword arguments)
    :return: Result of the operator call.
    """

def select_linked_from(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select nodes linked from the selected ones

    :return: Result of the operator call.
    """

def select_linked_to(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select nodes linked to the selected ones

    :return: Result of the operator call.
    """

def select_same_type_step(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    prev: bool | None = False,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Activate and view same node type, step by step

    :param prev: Previous, (optional)
    :return: Result of the operator call.
    """

def separate_bundle_item_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    node_identifier: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add item below active item

    :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
    :return: Result of the operator call.
    """

def separate_bundle_item_move(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    direction: typing.Literal["UP", "DOWN"] | None = "UP",
    node_identifier: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Move active item

    :param direction: Direction, Move direction (optional)
    :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
    :return: Result of the operator call.
    """

def separate_bundle_item_remove(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    node_identifier: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove active item

    :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
    :return: Result of the operator call.
    """

def shader_script_update(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Update shader script node with new sockets and options from the script

    :return: Result of the operator call.
    """

def simulation_zone_item_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    node_identifier: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add item below active item

    :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
    :return: Result of the operator call.
    """

def simulation_zone_item_move(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    direction: typing.Literal["UP", "DOWN"] | None = "UP",
    node_identifier: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Move active item

    :param direction: Direction, Move direction (optional)
    :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
    :return: Result of the operator call.
    """

def simulation_zone_item_remove(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    node_identifier: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove active item

    :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
    :return: Result of the operator call.
    """

def sockets_sync(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    node_name: str = "",
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Update sockets to match what is actually used

    :param node_name: Node Name, (optional, never None)
    :return: Result of the operator call.
    """

def swap_empty_group(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    settings: bpy.types.bpy_prop_collection[bl_operators.node.NodeSetting]
    | None = None,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Replace active node with an empty group

    :param settings: Settings, Settings to be applied on the newly created node (optional)
    :return: Result of the operator call.
    """

def swap_group_asset(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    asset_library_type: typing.Literal[
        bpy.stub_internal.rna_enums.AssetLibraryTypeItems
    ]
    | None = "LOCAL",
    asset_library_identifier: str = "",
    relative_asset_identifier: str = "",
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Swap selected nodes with the specified node group asset

    :param asset_library_type: Asset Library Type, (optional)
    :param asset_library_identifier: Asset Library Identifier, (optional, never None)
    :param relative_asset_identifier: Relative Asset Identifier, (optional, never None)
    :return: Result of the operator call.
    """

def swap_node(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    settings: bpy.types.bpy_prop_collection[bl_operators.node.NodeSetting]
    | None = None,
    type: str = "",
    visible_output: str = "",
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Replace the selected nodes with the specified type

    :param settings: Settings, Settings to be applied on the newly created node (optional)
    :param type: Node Type, Node type (optional, never None)
    :param visible_output: Output Name, If provided, all outputs that are named differently will be hidden (optional, never None)
    :return: Result of the operator call.
    """

def swap_zone(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    settings: bpy.types.bpy_prop_collection[bl_operators.node.NodeSetting]
    | None = None,
    offset: collections.abc.Sequence[float] | None = (150.0, 0.0),
    input_node_type: str = "",
    output_node_type: str = "",
    add_default_geometry_link: bool | None = False,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Undocumented, consider contributing.

    :param settings: Settings, Settings to be applied on the newly created node (optional)
    :param offset: Offset, Offset of nodes from the cursor when added (array of 2 items, in [-inf, inf], optional)
    :param input_node_type: Input Node, Specifies the input node used by the created zone (optional, never None)
    :param output_node_type: Output Node, Specifies the output node used by the created zone (optional, never None)
    :param add_default_geometry_link: Add Geometry Link, When enabled, create a link between geometry sockets in this zone (optional)
    :return: Result of the operator call.
    """

def test_inlining_shader_nodes(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Create a new inlined shader node tree as is consumed by renderers

    :return: Result of the operator call.
    """

def toggle_viewer(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Toggle selected viewer node in compositor and geometry nodes

    :return: Result of the operator call.
    """

def translate_attach(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    TRANSFORM_OT_translate: dict[str, typing.Any] | None = {},
    NODE_OT_attach: dict[str, typing.Any] | None = {},
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Move nodes and attach to frame

    :param TRANSFORM_OT_translate: Move, Move selected items (optional, `bpy.ops.transform.translate` keyword arguments)
    :param NODE_OT_attach: Attach Nodes, Attach active node to a frame (optional, `bpy.ops.node.attach` keyword arguments)
    :return: Result of the operator call.
    """

def translate_attach_remove_on_cancel(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    TRANSFORM_OT_translate: dict[str, typing.Any] | None = {},
    NODE_OT_attach: dict[str, typing.Any] | None = {},
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Move nodes and attach to frame

    :param TRANSFORM_OT_translate: Move, Move selected items (optional, `bpy.ops.transform.translate` keyword arguments)
    :param NODE_OT_attach: Attach Nodes, Attach active node to a frame (optional, `bpy.ops.node.attach` keyword arguments)
    :return: Result of the operator call.
    """

def tree_path_parent(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    parent_tree_index: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Go to parent node tree

    :param parent_tree_index: Parent Index, Parent index in context path (in [-inf, inf], optional)
    :return: Result of the operator call.
    """

def view_all(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Resize view so you can see all nodes

    :return: Result of the operator call.
    """

def view_selected(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Resize view so you can see selected nodes

    :return: Result of the operator call.
    """

def viewer_border(
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
    """Set the boundaries for viewer operations (Not implemented)

    :param xmin: X Min, (in [-inf, inf], optional)
    :param xmax: X Max, (in [-inf, inf], optional)
    :param ymin: Y Min, (in [-inf, inf], optional)
    :param ymax: Y Max, (in [-inf, inf], optional)
    :param wait_for_input: Wait for Input, (optional)
    :return: Result of the operator call.
    """

def viewer_shortcut_get(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    viewer_index: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Toggle a specific viewer node using 1,2,..,9 keys

    :param viewer_index: Viewer Index, Index corresponding to the shortcut, e.g. number key 1 corresponds to index 1 etc.. (in [-inf, inf], optional)
    :return: Result of the operator call.
    """

def viewer_shortcut_set(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    viewer_index: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Create a viewer shortcut for the selected node by pressing ctrl+1,2,..9

    :param viewer_index: Viewer Index, Index corresponding to the shortcut, e.g. number key 1 corresponds to index 1 etc.. (in [-inf, inf], optional)
    :return: Result of the operator call.
    """
