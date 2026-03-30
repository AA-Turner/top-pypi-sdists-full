import typing
import collections.abc
import typing_extensions
import numpy.typing as npt
import bl_operators.node
import bpy.ops
import bpy.stub_internal.rna_enums
import bpy.types

class _CLS_activate_viewer(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Activate selected viewer node in compositor and geometry nodes

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_add_closure_zone(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
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

        :param execution_context:
        :param undo:
        :param settings: Settings, Settings to be applied on the newly created node (optional)
        :param use_transform: Use Transform, Start transform operator after inserting the node (optional)
        :param offset: Offset, Offset of nodes from the cursor when added (array of 2 items, in [-inf, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_add_collection(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        name: str = "",
        session_uid: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Add a collection info node to the current node editor

        :param execution_context:
        :param undo:
        :param name: Name, Name of the data-block to use by the operator (optional, never None)
        :param session_uid: Session UID, Session UID of the data-block to use by the operator (in [-inf, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_add_color(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        color: collections.abc.Sequence[float] | None = (0.0, 0.0, 0.0, 0.0),
        gamma: bool | None = False,
        has_alpha: bool | None = False,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Add a color node to the current node editor

        :param execution_context:
        :param undo:
        :param color: Color, Source color (array of 4 items, in [0, inf], optional)
        :param gamma: Gamma Corrected, The source color is gamma corrected (optional)
        :param has_alpha: Has Alpha, The source color contains an Alpha component (optional)
        :return: Result of the operator call.
        """

class _CLS_add_empty_group(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        settings: bpy.types.bpy_prop_collection[bl_operators.node.NodeSetting]
        | None = None,
        use_transform: bool | None = False,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Add a group node with an empty group

        :param execution_context:
        :param undo:
        :param settings: Settings, Settings to be applied on the newly created node (optional)
        :param use_transform: Use Transform, Start transform operator after inserting the node (optional)
        :return: Result of the operator call.
        """

class _CLS_add_foreach_geometry_element_zone(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
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

        :param execution_context:
        :param undo:
        :param settings: Settings, Settings to be applied on the newly created node (optional)
        :param use_transform: Use Transform, Start transform operator after inserting the node (optional)
        :param offset: Offset, Offset of nodes from the cursor when added (array of 2 items, in [-inf, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_add_group(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        name: str = "",
        session_uid: int | None = 0,
        show_datablock_in_node: bool | None = True,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Add an existing node group to the current node editor

        :param execution_context:
        :param undo:
        :param name: Name, Name of the data-block to use by the operator (optional, never None)
        :param session_uid: Session UID, Session UID of the data-block to use by the operator (in [-inf, inf], optional)
        :param show_datablock_in_node: Show the data-block selector in the node, (optional)
        :return: Result of the operator call.
        """

class _CLS_add_group_asset(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
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

        :param execution_context:
        :param undo:
        :param asset_library_type: Asset Library Type, (optional)
        :param asset_library_identifier: Asset Library Identifier, (optional, never None)
        :param relative_asset_identifier: Relative Asset Identifier, (optional, never None)
        :return: Result of the operator call.
        """

class _CLS_add_group_input_node(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        socket_identifier: str = "",
        panel_identifier: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Add a Group Input node with selected sockets to the current node editor

        :param execution_context:
        :param undo:
        :param socket_identifier: Socket Identifier, Socket to include in the added group input/output node (optional, never None)
        :param panel_identifier: Panel Identifier, Panel from which to add sockets to the added group input/output node (in [-inf, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_add_image(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
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

                :param execution_context:
                :param undo:
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

class _CLS_add_import_node(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        directory: str = "",
        files: bpy.types.bpy_prop_collection[bpy.types.OperatorFileListElement]
        | None = None,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Add an import node to the node tree

        :param execution_context:
        :param undo:
        :param directory: Directory, Directory of the file (optional, never None)
        :param files: Files, (optional)
        :return: Result of the operator call.
        """

class _CLS_add_mask(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        name: str = "",
        session_uid: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Add a mask node to the current node editor

        :param execution_context:
        :param undo:
        :param name: Name, Name of the data-block to use by the operator (optional, never None)
        :param session_uid: Session UID, Session UID of the data-block to use by the operator (in [-inf, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_add_material(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        name: str = "",
        session_uid: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Add a material node to the current node editor

        :param execution_context:
        :param undo:
        :param name: Name, Name of the data-block to use by the operator (optional, never None)
        :param session_uid: Session UID, Session UID of the data-block to use by the operator (in [-inf, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_add_node(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
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

        :param execution_context:
        :param undo:
        :param settings: Settings, Settings to be applied on the newly created node (optional)
        :param use_transform: Use Transform, Start transform operator after inserting the node (optional)
        :param type: Node Type, Node type (optional, never None)
        :param visible_output: Output Name, If provided, all outputs that are named differently will be hidden (optional, never None)
        :return: Result of the operator call.
        """

class _CLS_add_object(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        name: str = "",
        session_uid: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Add an object info node to the current node editor

        :param execution_context:
        :param undo:
        :param name: Name, Name of the data-block to use by the operator (optional, never None)
        :param session_uid: Session UID, Session UID of the data-block to use by the operator (in [-inf, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_add_repeat_zone(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
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

        :param execution_context:
        :param undo:
        :param settings: Settings, Settings to be applied on the newly created node (optional)
        :param use_transform: Use Transform, Start transform operator after inserting the node (optional)
        :param offset: Offset, Offset of nodes from the cursor when added (array of 2 items, in [-inf, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_add_reroute(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        path: bpy.types.bpy_prop_collection[bpy.types.OperatorMousePath] | None = None,
        cursor: int | None = 11,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Add a reroute node

        :param execution_context:
        :param undo:
        :param path: Path, (optional)
        :param cursor: Cursor, (in [0, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_add_simulation_zone(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
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

        :param execution_context:
        :param undo:
        :param settings: Settings, Settings to be applied on the newly created node (optional)
        :param use_transform: Use Transform, Start transform operator after inserting the node (optional)
        :param offset: Offset, Offset of nodes from the cursor when added (array of 2 items, in [-inf, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_add_zone(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
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

        :param execution_context:
        :param undo:
        :param settings: Settings, Settings to be applied on the newly created node (optional)
        :param use_transform: Use Transform, Start transform operator after inserting the node (optional)
        :param offset: Offset, Offset of nodes from the cursor when added (array of 2 items, in [-inf, inf], optional)
        :param input_node_type: Input Node, Specifies the input node used by the created zone (optional, never None)
        :param output_node_type: Output Node, Specifies the output node used by the created zone (optional, never None)
        :param add_default_geometry_link: Add Geometry Link, When enabled, create a link between geometry sockets in this zone (optional)
        :return: Result of the operator call.
        """

class _CLS_attach(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Attach active node to a frame

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_backimage_fit(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Fit the background image to the view

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_backimage_move(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Move node backdrop

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_backimage_sample(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Use mouse to sample background image

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_backimage_zoom(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        factor: float | None = 1.2,
        use_mouse_pos: bool | None = True,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Zoom in/out the background image

        :param execution_context:
        :param undo:
        :param factor: Factor, (in [0, 10], optional)
        :param use_mouse_pos: Use Mouse Position, Zoom to mouse position (optional)
        :return: Result of the operator call.
        """

class _CLS_bake_node_item_add(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        node_identifier: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Add item below active item

        :param execution_context:
        :param undo:
        :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_bake_node_item_move(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        direction: typing.Literal["UP", "DOWN"] | None = "UP",
        node_identifier: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Move active item

        :param execution_context:
        :param undo:
        :param direction: Direction, Move direction (optional)
        :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_bake_node_item_remove(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        node_identifier: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Remove active item

        :param execution_context:
        :param undo:
        :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_capture_attribute_item_add(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        node_identifier: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Add item below active item

        :param execution_context:
        :param undo:
        :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_capture_attribute_item_move(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        direction: typing.Literal["UP", "DOWN"] | None = "UP",
        node_identifier: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Move active item

        :param execution_context:
        :param undo:
        :param direction: Direction, Move direction (optional)
        :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_capture_attribute_item_remove(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        node_identifier: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Remove active item

        :param execution_context:
        :param undo:
        :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_clear_viewer_border(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Clear the boundaries for viewer operations

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_clipboard_copy(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Copy the selected nodes to the internal clipboard

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_clipboard_paste(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        offset: collections.abc.Sequence[float] | None = (0.0, 0.0),
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Paste nodes from the internal clipboard to the active node tree

        :param execution_context:
        :param undo:
        :param offset: Location, The 2D view location for the center of the new nodes, or unchanged if not set (array of 2 items, in [-inf, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_closure_input_item_add(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        node_identifier: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Add item below active item

        :param execution_context:
        :param undo:
        :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_closure_input_item_move(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        direction: typing.Literal["UP", "DOWN"] | None = "UP",
        node_identifier: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Move active item

        :param execution_context:
        :param undo:
        :param direction: Direction, Move direction (optional)
        :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_closure_input_item_remove(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        node_identifier: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Remove active item

        :param execution_context:
        :param undo:
        :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_closure_output_item_add(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        node_identifier: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Add item below active item

        :param execution_context:
        :param undo:
        :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_closure_output_item_move(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        direction: typing.Literal["UP", "DOWN"] | None = "UP",
        node_identifier: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Move active item

        :param execution_context:
        :param undo:
        :param direction: Direction, Move direction (optional)
        :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_closure_output_item_remove(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        node_identifier: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Remove active item

        :param execution_context:
        :param undo:
        :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_collapse_hide_unused_toggle(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Toggle collapsed nodes and hide unused sockets

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_combine_bundle_item_add(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        node_identifier: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Add item below active item

        :param execution_context:
        :param undo:
        :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_combine_bundle_item_move(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        direction: typing.Literal["UP", "DOWN"] | None = "UP",
        node_identifier: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Move active item

        :param execution_context:
        :param undo:
        :param direction: Direction, Move direction (optional)
        :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_combine_bundle_item_remove(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        node_identifier: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Remove active item

        :param execution_context:
        :param undo:
        :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_connect_to_output(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        run_in_geometry_nodes: bool | None = True,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Connect active node to the active output node of the node tree

        :param execution_context:
        :param undo:
        :param run_in_geometry_nodes: Run in Geometry Nodes Editor, (optional)
        :return: Result of the operator call.
        """

class _CLS_cryptomatte_layer_add(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Add a new input layer to a Cryptomatte node

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_cryptomatte_layer_remove(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Remove layer from a Cryptomatte node

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_deactivate_viewer(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Deactivate selected viewer node in geometry nodes

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_default_group_width_set(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Set the width based on the parent group node in the current context

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_delete(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Remove selected nodes

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_delete_copy_reconnect(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        NODE_OT_clipboard_copy: dict[str, typing.Any] | None = {},
        NODE_OT_delete_reconnect: dict[str, typing.Any] | None = {},
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Copy nodes to clipboard, remove and reconnect them.

        :param execution_context:
        :param undo:
        :param NODE_OT_clipboard_copy: Copy to Clipboard, Copy the selected nodes to the internal clipboard (optional, `bpy.ops.node.clipboard_copy` keyword arguments)
        :param NODE_OT_delete_reconnect: Delete with Reconnect, Remove nodes and reconnect nodes as if deletion was muted (optional, `bpy.ops.node.delete_reconnect` keyword arguments)
        :return: Result of the operator call.
        """

class _CLS_delete_reconnect(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Remove nodes and reconnect nodes as if deletion was muted

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_detach(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Detach selected nodes from parents

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_detach_translate_attach(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        NODE_OT_detach: dict[str, typing.Any] | None = {},
        TRANSFORM_OT_translate: dict[str, typing.Any] | None = {},
        NODE_OT_attach: dict[str, typing.Any] | None = {},
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Detach nodes, move and attach to frame

        :param execution_context:
        :param undo:
        :param NODE_OT_detach: Detach Nodes, Detach selected nodes from parents (optional, `bpy.ops.node.detach` keyword arguments)
        :param TRANSFORM_OT_translate: Move, Move selected items (optional, `bpy.ops.transform.translate` keyword arguments)
        :param NODE_OT_attach: Attach Nodes, Attach active node to a frame (optional, `bpy.ops.node.attach` keyword arguments)
        :return: Result of the operator call.
        """

class _CLS_duplicate(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        keep_inputs: bool | None = False,
        linked: bool | None = True,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Duplicate selected nodes

        :param execution_context:
        :param undo:
        :param keep_inputs: Keep Inputs, Keep the input links to duplicated nodes (optional)
        :param linked: Linked, Duplicate node but not node trees, linking to the original data (optional)
        :return: Result of the operator call.
        """

class _CLS_duplicate_compositing_modifier_node_group(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Duplicate the currently assigned compositing node group.

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_duplicate_compositing_node_group(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Duplicate the currently assigned compositing node group.

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_duplicate_move(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        NODE_OT_duplicate: dict[str, typing.Any] | None = {},
        NODE_OT_translate_attach: dict[str, typing.Any] | None = {},
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Duplicate selected nodes and move them

        :param execution_context:
        :param undo:
        :param NODE_OT_duplicate: Duplicate Nodes, Duplicate selected nodes (optional, `bpy.ops.node.duplicate` keyword arguments)
        :param NODE_OT_translate_attach: Move and Attach, Move nodes and attach to frame (optional, `bpy.ops.node.translate_attach` keyword arguments)
        :return: Result of the operator call.
        """

class _CLS_duplicate_move_keep_inputs(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        NODE_OT_duplicate: dict[str, typing.Any] | None = {},
        NODE_OT_translate_attach: dict[str, typing.Any] | None = {},
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Duplicate selected nodes keeping input links and move them

        :param execution_context:
        :param undo:
        :param NODE_OT_duplicate: Duplicate Nodes, Duplicate selected nodes (optional, `bpy.ops.node.duplicate` keyword arguments)
        :param NODE_OT_translate_attach: Move and Attach, Move nodes and attach to frame (optional, `bpy.ops.node.translate_attach` keyword arguments)
        :return: Result of the operator call.
        """

class _CLS_duplicate_move_linked(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        NODE_OT_duplicate: dict[str, typing.Any] | None = {},
        NODE_OT_translate_attach: dict[str, typing.Any] | None = {},
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Duplicate selected nodes, but not their node trees, and move them

        :param execution_context:
        :param undo:
        :param NODE_OT_duplicate: Duplicate Nodes, Duplicate selected nodes (optional, `bpy.ops.node.duplicate` keyword arguments)
        :param NODE_OT_translate_attach: Move and Attach, Move nodes and attach to frame (optional, `bpy.ops.node.translate_attach` keyword arguments)
        :return: Result of the operator call.
        """

class _CLS_enum_definition_item_add(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        node_identifier: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Add item below active item

        :param execution_context:
        :param undo:
        :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_enum_definition_item_move(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        direction: typing.Literal["UP", "DOWN"] | None = "UP",
        node_identifier: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Move active item

        :param execution_context:
        :param undo:
        :param direction: Direction, Move direction (optional)
        :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_enum_definition_item_remove(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        node_identifier: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Remove active item

        :param execution_context:
        :param undo:
        :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_evaluate_closure_input_item_add(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        node_identifier: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Add item below active item

        :param execution_context:
        :param undo:
        :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_evaluate_closure_input_item_move(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        direction: typing.Literal["UP", "DOWN"] | None = "UP",
        node_identifier: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Move active item

        :param execution_context:
        :param undo:
        :param direction: Direction, Move direction (optional)
        :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_evaluate_closure_input_item_remove(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        node_identifier: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Remove active item

        :param execution_context:
        :param undo:
        :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_evaluate_closure_output_item_add(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        node_identifier: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Add item below active item

        :param execution_context:
        :param undo:
        :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_evaluate_closure_output_item_move(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        direction: typing.Literal["UP", "DOWN"] | None = "UP",
        node_identifier: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Move active item

        :param execution_context:
        :param undo:
        :param direction: Direction, Move direction (optional)
        :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_evaluate_closure_output_item_remove(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        node_identifier: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Remove active item

        :param execution_context:
        :param undo:
        :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_field_to_grid_item_add(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        node_identifier: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Add item below active item

        :param execution_context:
        :param undo:
        :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_field_to_grid_item_move(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        direction: typing.Literal["UP", "DOWN"] | None = "UP",
        node_identifier: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Move active item

        :param execution_context:
        :param undo:
        :param direction: Direction, Move direction (optional)
        :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_field_to_grid_item_remove(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        node_identifier: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Remove active item

        :param execution_context:
        :param undo:
        :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_field_to_list_item_add(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        node_identifier: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Add item below active item

        :param execution_context:
        :param undo:
        :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_field_to_list_item_move(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        direction: typing.Literal["UP", "DOWN"] | None = "UP",
        node_identifier: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Move active item

        :param execution_context:
        :param undo:
        :param direction: Direction, Move direction (optional)
        :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_field_to_list_item_remove(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        node_identifier: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Remove active item

        :param execution_context:
        :param undo:
        :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_file_output_item_add(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        node_identifier: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Add item below active item

        :param execution_context:
        :param undo:
        :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_file_output_item_move(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        direction: typing.Literal["UP", "DOWN"] | None = "UP",
        node_identifier: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Move active item

        :param execution_context:
        :param undo:
        :param direction: Direction, Move direction (optional)
        :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_file_output_item_remove(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        node_identifier: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Remove active item

        :param execution_context:
        :param undo:
        :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_find_node(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Search for a node by name and focus and select it

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_foreach_geometry_element_zone_generation_item_add(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        node_identifier: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Add item below active item

        :param execution_context:
        :param undo:
        :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_foreach_geometry_element_zone_generation_item_move(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        direction: typing.Literal["UP", "DOWN"] | None = "UP",
        node_identifier: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Move active item

        :param execution_context:
        :param undo:
        :param direction: Direction, Move direction (optional)
        :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_foreach_geometry_element_zone_generation_item_remove(
    bpy.ops._BPyOpsSubModOp
):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        node_identifier: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Remove active item

        :param execution_context:
        :param undo:
        :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_foreach_geometry_element_zone_input_item_add(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        node_identifier: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Add item below active item

        :param execution_context:
        :param undo:
        :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_foreach_geometry_element_zone_input_item_move(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        direction: typing.Literal["UP", "DOWN"] | None = "UP",
        node_identifier: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Move active item

        :param execution_context:
        :param undo:
        :param direction: Direction, Move direction (optional)
        :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_foreach_geometry_element_zone_input_item_remove(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        node_identifier: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Remove active item

        :param execution_context:
        :param undo:
        :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_foreach_geometry_element_zone_main_item_add(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        node_identifier: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Add item below active item

        :param execution_context:
        :param undo:
        :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_foreach_geometry_element_zone_main_item_move(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        direction: typing.Literal["UP", "DOWN"] | None = "UP",
        node_identifier: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Move active item

        :param execution_context:
        :param undo:
        :param direction: Direction, Move direction (optional)
        :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_foreach_geometry_element_zone_main_item_remove(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        node_identifier: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Remove active item

        :param execution_context:
        :param undo:
        :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_format_string_item_add(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        node_identifier: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Add item below active item

        :param execution_context:
        :param undo:
        :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_format_string_item_move(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        direction: typing.Literal["UP", "DOWN"] | None = "UP",
        node_identifier: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Move active item

        :param execution_context:
        :param undo:
        :param direction: Direction, Move direction (optional)
        :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_format_string_item_remove(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        node_identifier: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Remove active item

        :param execution_context:
        :param undo:
        :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_geometry_nodes_viewer_item_add(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        node_identifier: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Add item below active item

        :param execution_context:
        :param undo:
        :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_geometry_nodes_viewer_item_move(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        direction: typing.Literal["UP", "DOWN"] | None = "UP",
        node_identifier: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Move active item

        :param execution_context:
        :param undo:
        :param direction: Direction, Move direction (optional)
        :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_geometry_nodes_viewer_item_remove(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        node_identifier: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Remove active item

        :param execution_context:
        :param undo:
        :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_gltf_settings_node_operator(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Add a node to the active tree for glTF export

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_group_edit(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        exit: bool | None = False,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Edit node group

        :param execution_context:
        :param undo:
        :param exit: Exit, (optional)
        :return: Result of the operator call.
        """

class _CLS_group_enter_exit(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Enter or exit node group based on cursor location

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_group_insert(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Insert selected nodes into a node group

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_group_make(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Make group from selected nodes

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_group_separate(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        type: typing.Literal["COPY", "MOVE"] | None = "COPY",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Separate selected nodes from the node group

                :param execution_context:
                :param undo:
                :param type: Type, (optional)

        COPY
        Copy -- Copy to parent node tree, keep group intact.

        MOVE
        Move -- Move to parent node tree, remove from group.
                :return: Result of the operator call.
        """

class _CLS_group_ungroup(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Ungroup selected nodes

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_hide_socket_toggle(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Toggle unused node socket display

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_hide_toggle(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Toggle collapsing of selected nodes

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_index_switch_item_add(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        node_identifier: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Add an item to the index switch

        :param execution_context:
        :param undo:
        :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_index_switch_item_remove(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        index: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Remove an item from the index switch

        :param execution_context:
        :param undo:
        :param index: Index, Index to remove (in [0, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_insert_offset(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Automatically offset nodes on insertion

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_interface_item_duplicate(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Add a copy of the active item to the interface

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_interface_item_make_panel_toggle(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Make the active boolean socket a toggle for its parent panel

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_interface_item_new(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        item_type: typing.Literal["INPUT", "OUTPUT", "PANEL"] | None = "INPUT",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Add a new item to the interface

        :param execution_context:
        :param undo:
        :param item_type: Item Type, Type of the item to create (optional)
        :return: Result of the operator call.
        """

class _CLS_interface_item_new_panel_toggle(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Add a checkbox to the currently selected panel

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_interface_item_remove(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Remove selected items from the interface

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_interface_item_unlink_panel_toggle(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Make the panel toggle a stand-alone socket

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_join(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Attach selected nodes to a new common frame

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_join_named(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        NODE_OT_join: dict[str, typing.Any] | None = {},
        WM_OT_call_panel: dict[str, typing.Any] | None = {},
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Create a new frame node around the selected nodes and name it immediately

        :param execution_context:
        :param undo:
        :param NODE_OT_join: Join Nodes in Frame, Attach selected nodes to a new common frame (optional, `bpy.ops.node.join` keyword arguments)
        :param WM_OT_call_panel: Call Panel, Open a predefined panel (optional, `bpy.ops.wm.call_panel` keyword arguments)
        :return: Result of the operator call.
        """

class _CLS_join_nodes(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Merge selected group input nodes into one if possible

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_link(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
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

        :param execution_context:
        :param undo:
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

class _CLS_link_drag_operation_test(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        find_link_operations: bool | None = False,
        link_operation_index: int | None = -1,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Run a node link-drag operation for testing

        :param execution_context:
        :param undo:
        :param find_link_operations: Find Link Operations, Write link operation names for the context socket the "link_operation_names" property of the node tree (optional)
        :param link_operation_index: Link Operation Index, Link operation to execute on the context socket (in [-1, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_link_make(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        replace: bool | None = False,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Make a link between selected output and input sockets

        :param execution_context:
        :param undo:
        :param replace: Replace, Replace socket connections with the new links (optional)
        :return: Result of the operator call.
        """

class _CLS_link_viewer(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Link to viewer node

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_links_cut(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        path: bpy.types.bpy_prop_collection[bpy.types.OperatorMousePath] | None = None,
        cursor: int | None = 15,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Use the mouse to cut (remove) some links

        :param execution_context:
        :param undo:
        :param path: Path, (optional)
        :param cursor: Cursor, (in [0, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_links_detach(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Remove all links to selected nodes, and try to connect neighbor nodes together

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_links_mute(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        path: bpy.types.bpy_prop_collection[bpy.types.OperatorMousePath] | None = None,
        cursor: int | None = 39,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Use the mouse to mute links

        :param execution_context:
        :param undo:
        :param path: Path, (optional)
        :param cursor: Cursor, (in [0, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_move_detach_links(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        NODE_OT_links_detach: dict[str, typing.Any] | None = {},
        TRANSFORM_OT_translate: dict[str, typing.Any] | None = {},
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Move a node to detach links

        :param execution_context:
        :param undo:
        :param NODE_OT_links_detach: Detach Links, Remove all links to selected nodes, and try to connect neighbor nodes together (optional, `bpy.ops.node.links_detach` keyword arguments)
        :param TRANSFORM_OT_translate: Move, Move selected items (optional, `bpy.ops.transform.translate` keyword arguments)
        :return: Result of the operator call.
        """

class _CLS_move_detach_links_release(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        NODE_OT_links_detach: dict[str, typing.Any] | None = {},
        NODE_OT_translate_attach: dict[str, typing.Any] | None = {},
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Move a node to detach links

        :param execution_context:
        :param undo:
        :param NODE_OT_links_detach: Detach Links, Remove all links to selected nodes, and try to connect neighbor nodes together (optional, `bpy.ops.node.links_detach` keyword arguments)
        :param NODE_OT_translate_attach: Move and Attach, Move nodes and attach to frame (optional, `bpy.ops.node.translate_attach` keyword arguments)
        :return: Result of the operator call.
        """

class _CLS_mute_toggle(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Toggle muting of selected nodes

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_new_compositing_node_group(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        name: str = "",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Create a new compositing node group and initialize it with default nodes

        :param execution_context:
        :param undo:
        :param name: Name, (optional, never None)
        :return: Result of the operator call.
        """

class _CLS_new_compositor_sequencer_node_group(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        name: str = "Sequencer Compositor Nodes",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Create a new compositor node group for sequencer

        :param execution_context:
        :param undo:
        :param name: Name, (optional, never None)
        :return: Result of the operator call.
        """

class _CLS_new_geometry_node_group_assign(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Create a new geometry node group and assign it to the active modifier

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_new_geometry_node_group_tool(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Create a new geometry node group for a tool

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_new_geometry_nodes_modifier(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Create a new modifier with a new geometry node group

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_new_node_tree(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        type: str | None = "",
        name: str = "NodeTree",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Create a new node tree

        :param execution_context:
        :param undo:
        :param type: Tree Type, (optional)
        :param name: Name, (optional, never None)
        :return: Result of the operator call.
        """

class _CLS_node_color_preset_add(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        name: str = "",
        remove_name: bool | None = False,
        remove_active: bool | None = False,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Add or remove a Node Color Preset

        :param execution_context:
        :param undo:
        :param name: Name, Name of the preset, used to make the path name (optional, never None)
        :param remove_name: remove_name, (optional)
        :param remove_active: remove_active, (optional)
        :return: Result of the operator call.
        """

class _CLS_node_copy_color(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Copy color to all selected nodes

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_options_toggle(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Toggle option buttons display for selected nodes

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_parent_set(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Attach selected nodes

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_preview_toggle(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Toggle preview display for selected nodes

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_read_viewlayers(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Read all render layers of all used scenes

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_render_changed(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Render current scene, when input nodes layer has been changed

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_repeat_zone_item_add(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        node_identifier: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Add item below active item

        :param execution_context:
        :param undo:
        :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_repeat_zone_item_move(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        direction: typing.Literal["UP", "DOWN"] | None = "UP",
        node_identifier: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Move active item

        :param execution_context:
        :param undo:
        :param direction: Direction, Move direction (optional)
        :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_repeat_zone_item_remove(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        node_identifier: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Remove active item

        :param execution_context:
        :param undo:
        :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_resize(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Resize a node

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
        location: collections.abc.Sequence[int] | None = (0, 0),
        socket_select: bool | None = False,
        clear_viewer: bool | None = False,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Select the node under the cursor

        :param execution_context:
        :param undo:
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

class _CLS_select_all(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        action: typing.Literal["TOGGLE", "SELECT", "DESELECT", "INVERT"]
        | None = "TOGGLE",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """(De)select all nodes

                :param execution_context:
                :param undo:
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

class _CLS_select_box(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
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

                :param execution_context:
                :param undo:
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
        """Use circle selection to select nodes

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

class _CLS_select_grouped(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        extend: bool | None = False,
        type: typing.Literal["TYPE", "COLOR", "PREFIX", "SUFFIX"] | None = "TYPE",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Select nodes with similar properties

        :param execution_context:
        :param undo:
        :param extend: Extend, Extend selection instead of deselecting everything first (optional)
        :param type: Type, (optional)
        :return: Result of the operator call.
        """

class _CLS_select_lasso(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
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

                :param execution_context:
                :param undo:
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

class _CLS_select_link_viewer(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        NODE_OT_select: dict[str, typing.Any] | None = {},
        NODE_OT_link_viewer: dict[str, typing.Any] | None = {},
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Select node and link it to a viewer node

        :param execution_context:
        :param undo:
        :param NODE_OT_select: Select, Select the node under the cursor (optional, `bpy.ops.node.select` keyword arguments)
        :param NODE_OT_link_viewer: Link to Viewer Node, Link to viewer node (optional, `bpy.ops.node.link_viewer` keyword arguments)
        :return: Result of the operator call.
        """

class _CLS_select_linked_from(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Select nodes linked from the selected ones

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_select_linked_to(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Select nodes linked to the selected ones

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_select_same_type_step(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        prev: bool | None = False,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Activate and view same node type, step by step

        :param execution_context:
        :param undo:
        :param prev: Previous, (optional)
        :return: Result of the operator call.
        """

class _CLS_separate_bundle_item_add(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        node_identifier: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Add item below active item

        :param execution_context:
        :param undo:
        :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_separate_bundle_item_move(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        direction: typing.Literal["UP", "DOWN"] | None = "UP",
        node_identifier: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Move active item

        :param execution_context:
        :param undo:
        :param direction: Direction, Move direction (optional)
        :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_separate_bundle_item_remove(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        node_identifier: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Remove active item

        :param execution_context:
        :param undo:
        :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_shader_script_update(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Update shader script node with new sockets and options from the script

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_simulation_zone_item_add(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        node_identifier: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Add item below active item

        :param execution_context:
        :param undo:
        :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_simulation_zone_item_move(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        direction: typing.Literal["UP", "DOWN"] | None = "UP",
        node_identifier: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Move active item

        :param execution_context:
        :param undo:
        :param direction: Direction, Move direction (optional)
        :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_simulation_zone_item_remove(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        node_identifier: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Remove active item

        :param execution_context:
        :param undo:
        :param node_identifier: Node Identifier, Optional identifier of the node to operate on (in [0, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_sockets_sync(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        node_name: str = "",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Update sockets to match what is actually used

        :param execution_context:
        :param undo:
        :param node_name: Node Name, (optional, never None)
        :return: Result of the operator call.
        """

class _CLS_swap_empty_group(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        settings: bpy.types.bpy_prop_collection[bl_operators.node.NodeSetting]
        | None = None,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Replace active node with an empty group

        :param execution_context:
        :param undo:
        :param settings: Settings, Settings to be applied on the newly created node (optional)
        :return: Result of the operator call.
        """

class _CLS_swap_group_asset(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
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

        :param execution_context:
        :param undo:
        :param asset_library_type: Asset Library Type, (optional)
        :param asset_library_identifier: Asset Library Identifier, (optional, never None)
        :param relative_asset_identifier: Relative Asset Identifier, (optional, never None)
        :return: Result of the operator call.
        """

class _CLS_swap_node(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
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

        :param execution_context:
        :param undo:
        :param settings: Settings, Settings to be applied on the newly created node (optional)
        :param type: Node Type, Node type (optional, never None)
        :param visible_output: Output Name, If provided, all outputs that are named differently will be hidden (optional, never None)
        :return: Result of the operator call.
        """

class _CLS_swap_zone(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
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

        :param execution_context:
        :param undo:
        :param settings: Settings, Settings to be applied on the newly created node (optional)
        :param offset: Offset, Offset of nodes from the cursor when added (array of 2 items, in [-inf, inf], optional)
        :param input_node_type: Input Node, Specifies the input node used by the created zone (optional, never None)
        :param output_node_type: Output Node, Specifies the output node used by the created zone (optional, never None)
        :param add_default_geometry_link: Add Geometry Link, When enabled, create a link between geometry sockets in this zone (optional)
        :return: Result of the operator call.
        """

class _CLS_test_inlining_shader_nodes(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Create a new inlined shader node tree as is consumed by renderers

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_toggle_viewer(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Toggle selected viewer node in compositor and geometry nodes

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_translate_attach(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        TRANSFORM_OT_translate: dict[str, typing.Any] | None = {},
        NODE_OT_attach: dict[str, typing.Any] | None = {},
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Move nodes and attach to frame

        :param execution_context:
        :param undo:
        :param TRANSFORM_OT_translate: Move, Move selected items (optional, `bpy.ops.transform.translate` keyword arguments)
        :param NODE_OT_attach: Attach Nodes, Attach active node to a frame (optional, `bpy.ops.node.attach` keyword arguments)
        :return: Result of the operator call.
        """

class _CLS_translate_attach_remove_on_cancel(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        TRANSFORM_OT_translate: dict[str, typing.Any] | None = {},
        NODE_OT_attach: dict[str, typing.Any] | None = {},
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Move nodes and attach to frame

        :param execution_context:
        :param undo:
        :param TRANSFORM_OT_translate: Move, Move selected items (optional, `bpy.ops.transform.translate` keyword arguments)
        :param NODE_OT_attach: Attach Nodes, Attach active node to a frame (optional, `bpy.ops.node.attach` keyword arguments)
        :return: Result of the operator call.
        """

class _CLS_tree_path_parent(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        parent_tree_index: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Go to parent node tree

        :param execution_context:
        :param undo:
        :param parent_tree_index: Parent Index, Parent index in context path (in [-inf, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_view_all(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Resize view so you can see all nodes

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_view_selected(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Resize view so you can see selected nodes

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_viewer_border(bpy.ops._BPyOpsSubModOp):
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
        """Set the boundaries for viewer operations (Not implemented)

        :param execution_context:
        :param undo:
        :param xmin: X Min, (in [-inf, inf], optional)
        :param xmax: X Max, (in [-inf, inf], optional)
        :param ymin: Y Min, (in [-inf, inf], optional)
        :param ymax: Y Max, (in [-inf, inf], optional)
        :param wait_for_input: Wait for Input, (optional)
        :return: Result of the operator call.
        """

class _CLS_viewer_shortcut_get(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        viewer_index: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Toggle a specific viewer node using 1,2,..,9 keys

        :param execution_context:
        :param undo:
        :param viewer_index: Viewer Index, Index corresponding to the shortcut, e.g. number key 1 corresponds to index 1 etc.. (in [-inf, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_viewer_shortcut_set(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        viewer_index: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Create a viewer shortcut for the selected node by pressing ctrl+1,2,..9

        :param execution_context:
        :param undo:
        :param viewer_index: Viewer Index, Index corresponding to the shortcut, e.g. number key 1 corresponds to index 1 etc.. (in [-inf, inf], optional)
        :return: Result of the operator call.
        """

activate_viewer: _CLS_activate_viewer

add_closure_zone: _CLS_add_closure_zone

add_collection: _CLS_add_collection

add_color: _CLS_add_color

add_empty_group: _CLS_add_empty_group

add_foreach_geometry_element_zone: _CLS_add_foreach_geometry_element_zone

add_group: _CLS_add_group

add_group_asset: _CLS_add_group_asset

add_group_input_node: _CLS_add_group_input_node

add_image: _CLS_add_image

add_import_node: _CLS_add_import_node

add_mask: _CLS_add_mask

add_material: _CLS_add_material

add_node: _CLS_add_node

add_object: _CLS_add_object

add_repeat_zone: _CLS_add_repeat_zone

add_reroute: _CLS_add_reroute

add_simulation_zone: _CLS_add_simulation_zone

add_zone: _CLS_add_zone

attach: _CLS_attach

backimage_fit: _CLS_backimage_fit

backimage_move: _CLS_backimage_move

backimage_sample: _CLS_backimage_sample

backimage_zoom: _CLS_backimage_zoom

bake_node_item_add: _CLS_bake_node_item_add

bake_node_item_move: _CLS_bake_node_item_move

bake_node_item_remove: _CLS_bake_node_item_remove

capture_attribute_item_add: _CLS_capture_attribute_item_add

capture_attribute_item_move: _CLS_capture_attribute_item_move

capture_attribute_item_remove: _CLS_capture_attribute_item_remove

clear_viewer_border: _CLS_clear_viewer_border

clipboard_copy: _CLS_clipboard_copy

clipboard_paste: _CLS_clipboard_paste

closure_input_item_add: _CLS_closure_input_item_add

closure_input_item_move: _CLS_closure_input_item_move

closure_input_item_remove: _CLS_closure_input_item_remove

closure_output_item_add: _CLS_closure_output_item_add

closure_output_item_move: _CLS_closure_output_item_move

closure_output_item_remove: _CLS_closure_output_item_remove

collapse_hide_unused_toggle: _CLS_collapse_hide_unused_toggle

combine_bundle_item_add: _CLS_combine_bundle_item_add

combine_bundle_item_move: _CLS_combine_bundle_item_move

combine_bundle_item_remove: _CLS_combine_bundle_item_remove

connect_to_output: _CLS_connect_to_output

cryptomatte_layer_add: _CLS_cryptomatte_layer_add

cryptomatte_layer_remove: _CLS_cryptomatte_layer_remove

deactivate_viewer: _CLS_deactivate_viewer

default_group_width_set: _CLS_default_group_width_set

delete: _CLS_delete

delete_copy_reconnect: _CLS_delete_copy_reconnect

delete_reconnect: _CLS_delete_reconnect

detach: _CLS_detach

detach_translate_attach: _CLS_detach_translate_attach

duplicate: _CLS_duplicate

duplicate_compositing_modifier_node_group: (
    _CLS_duplicate_compositing_modifier_node_group
)

duplicate_compositing_node_group: _CLS_duplicate_compositing_node_group

duplicate_move: _CLS_duplicate_move

duplicate_move_keep_inputs: _CLS_duplicate_move_keep_inputs

duplicate_move_linked: _CLS_duplicate_move_linked

enum_definition_item_add: _CLS_enum_definition_item_add

enum_definition_item_move: _CLS_enum_definition_item_move

enum_definition_item_remove: _CLS_enum_definition_item_remove

evaluate_closure_input_item_add: _CLS_evaluate_closure_input_item_add

evaluate_closure_input_item_move: _CLS_evaluate_closure_input_item_move

evaluate_closure_input_item_remove: _CLS_evaluate_closure_input_item_remove

evaluate_closure_output_item_add: _CLS_evaluate_closure_output_item_add

evaluate_closure_output_item_move: _CLS_evaluate_closure_output_item_move

evaluate_closure_output_item_remove: _CLS_evaluate_closure_output_item_remove

field_to_grid_item_add: _CLS_field_to_grid_item_add

field_to_grid_item_move: _CLS_field_to_grid_item_move

field_to_grid_item_remove: _CLS_field_to_grid_item_remove

field_to_list_item_add: _CLS_field_to_list_item_add

field_to_list_item_move: _CLS_field_to_list_item_move

field_to_list_item_remove: _CLS_field_to_list_item_remove

file_output_item_add: _CLS_file_output_item_add

file_output_item_move: _CLS_file_output_item_move

file_output_item_remove: _CLS_file_output_item_remove

find_node: _CLS_find_node

foreach_geometry_element_zone_generation_item_add: (
    _CLS_foreach_geometry_element_zone_generation_item_add
)

foreach_geometry_element_zone_generation_item_move: (
    _CLS_foreach_geometry_element_zone_generation_item_move
)

foreach_geometry_element_zone_generation_item_remove: (
    _CLS_foreach_geometry_element_zone_generation_item_remove
)

foreach_geometry_element_zone_input_item_add: (
    _CLS_foreach_geometry_element_zone_input_item_add
)

foreach_geometry_element_zone_input_item_move: (
    _CLS_foreach_geometry_element_zone_input_item_move
)

foreach_geometry_element_zone_input_item_remove: (
    _CLS_foreach_geometry_element_zone_input_item_remove
)

foreach_geometry_element_zone_main_item_add: (
    _CLS_foreach_geometry_element_zone_main_item_add
)

foreach_geometry_element_zone_main_item_move: (
    _CLS_foreach_geometry_element_zone_main_item_move
)

foreach_geometry_element_zone_main_item_remove: (
    _CLS_foreach_geometry_element_zone_main_item_remove
)

format_string_item_add: _CLS_format_string_item_add

format_string_item_move: _CLS_format_string_item_move

format_string_item_remove: _CLS_format_string_item_remove

geometry_nodes_viewer_item_add: _CLS_geometry_nodes_viewer_item_add

geometry_nodes_viewer_item_move: _CLS_geometry_nodes_viewer_item_move

geometry_nodes_viewer_item_remove: _CLS_geometry_nodes_viewer_item_remove

gltf_settings_node_operator: _CLS_gltf_settings_node_operator

group_edit: _CLS_group_edit

group_enter_exit: _CLS_group_enter_exit

group_insert: _CLS_group_insert

group_make: _CLS_group_make

group_separate: _CLS_group_separate

group_ungroup: _CLS_group_ungroup

hide_socket_toggle: _CLS_hide_socket_toggle

hide_toggle: _CLS_hide_toggle

index_switch_item_add: _CLS_index_switch_item_add

index_switch_item_remove: _CLS_index_switch_item_remove

insert_offset: _CLS_insert_offset

interface_item_duplicate: _CLS_interface_item_duplicate

interface_item_make_panel_toggle: _CLS_interface_item_make_panel_toggle

interface_item_new: _CLS_interface_item_new

interface_item_new_panel_toggle: _CLS_interface_item_new_panel_toggle

interface_item_remove: _CLS_interface_item_remove

interface_item_unlink_panel_toggle: _CLS_interface_item_unlink_panel_toggle

join: _CLS_join

join_named: _CLS_join_named

join_nodes: _CLS_join_nodes

link: _CLS_link

link_drag_operation_test: _CLS_link_drag_operation_test

link_make: _CLS_link_make

link_viewer: _CLS_link_viewer

links_cut: _CLS_links_cut

links_detach: _CLS_links_detach

links_mute: _CLS_links_mute

move_detach_links: _CLS_move_detach_links

move_detach_links_release: _CLS_move_detach_links_release

mute_toggle: _CLS_mute_toggle

new_compositing_node_group: _CLS_new_compositing_node_group

new_compositor_sequencer_node_group: _CLS_new_compositor_sequencer_node_group

new_geometry_node_group_assign: _CLS_new_geometry_node_group_assign

new_geometry_node_group_tool: _CLS_new_geometry_node_group_tool

new_geometry_nodes_modifier: _CLS_new_geometry_nodes_modifier

new_node_tree: _CLS_new_node_tree

node_color_preset_add: _CLS_node_color_preset_add

node_copy_color: _CLS_node_copy_color

options_toggle: _CLS_options_toggle

parent_set: _CLS_parent_set

preview_toggle: _CLS_preview_toggle

read_viewlayers: _CLS_read_viewlayers

render_changed: _CLS_render_changed

repeat_zone_item_add: _CLS_repeat_zone_item_add

repeat_zone_item_move: _CLS_repeat_zone_item_move

repeat_zone_item_remove: _CLS_repeat_zone_item_remove

resize: _CLS_resize

select: _CLS_select

select_all: _CLS_select_all

select_box: _CLS_select_box

select_circle: _CLS_select_circle

select_grouped: _CLS_select_grouped

select_lasso: _CLS_select_lasso

select_link_viewer: _CLS_select_link_viewer

select_linked_from: _CLS_select_linked_from

select_linked_to: _CLS_select_linked_to

select_same_type_step: _CLS_select_same_type_step

separate_bundle_item_add: _CLS_separate_bundle_item_add

separate_bundle_item_move: _CLS_separate_bundle_item_move

separate_bundle_item_remove: _CLS_separate_bundle_item_remove

shader_script_update: _CLS_shader_script_update

simulation_zone_item_add: _CLS_simulation_zone_item_add

simulation_zone_item_move: _CLS_simulation_zone_item_move

simulation_zone_item_remove: _CLS_simulation_zone_item_remove

sockets_sync: _CLS_sockets_sync

swap_empty_group: _CLS_swap_empty_group

swap_group_asset: _CLS_swap_group_asset

swap_node: _CLS_swap_node

swap_zone: _CLS_swap_zone

test_inlining_shader_nodes: _CLS_test_inlining_shader_nodes

toggle_viewer: _CLS_toggle_viewer

translate_attach: _CLS_translate_attach

translate_attach_remove_on_cancel: _CLS_translate_attach_remove_on_cancel

tree_path_parent: _CLS_tree_path_parent

view_all: _CLS_view_all

view_selected: _CLS_view_selected

viewer_border: _CLS_viewer_border

viewer_shortcut_get: _CLS_viewer_shortcut_get

viewer_shortcut_set: _CLS_viewer_shortcut_set
