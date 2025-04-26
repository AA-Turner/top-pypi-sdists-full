from __future__ import annotations

import json
from typing import cast, Dict, Generic, List, Optional, Protocol, Set, Type, TypeVar, Union

from benchling_api_client.v2.extensions import UnknownType
from benchling_api_client.v2.stable.types import UNSET, Unset

from benchling_sdk.apps.canvas.errors import (
    DuplicateBlockIdError,
    MissingResourceIdError,
    NoMatchingBlocksError,
)
from benchling_sdk.apps.canvas.types import (
    _UI_BLOCK_MAPPINGS_CREATE,
    _UI_BLOCK_MAPPINGS_UPDATE,
    _UiBlockCreate,
    _UiBlockUpdate,
    UiBlock,
    UiBlockType,
)
from benchling_sdk.apps.types import JsonType
from benchling_sdk.models import (
    AppCanvas,
    AppCanvasApp,
    AppCanvasCreate,
    AppCanvasUpdate,
    DropdownMultiValueUiBlock,
    DropdownUiBlock,
    SearchInputMultiValueUiBlock,
    SearchInputUiBlock,
    SectionUiBlock,
    SelectorInputMultiValueUiBlock,
    SelectorInputUiBlock,
    TableUiBlock,
    TextInputUiBlock,
)

S = TypeVar("S", bound="FilteredCanvasBuilderBlockStream")


def _ui_block_to_create(block: UiBlock) -> _UiBlockCreate:
    # Rely on the fact that the read/write shapes are compatible, for now
    if isinstance(block, UnknownType):
        return block
    elif type(block) in _UI_BLOCK_MAPPINGS_CREATE:
        create_block_class = _UI_BLOCK_MAPPINGS_CREATE[type(block)]
        create_block = create_block_class.from_dict(block.to_dict())  # type: ignore
        if isinstance(block, SectionUiBlock) and create_block.children:
            create_block.children = [_ui_block_to_create(child) for child in create_block.children]
        return create_block
    # Allow the block to be serialized as-is rather than runtime error for the user on a type check
    return block  # type: ignore


def _ui_block_to_update(block: UiBlock) -> _UiBlockUpdate:
    # Rely on the fact that the read/write shapes are compatible, for now
    # Update is functionally the same as create at the moment but different for type safety
    # and reserved in case the shapes do diverge later
    if isinstance(block, UnknownType):
        return block
    elif type(block) in _UI_BLOCK_MAPPINGS_UPDATE:
        update_block_class = _UI_BLOCK_MAPPINGS_UPDATE[type(block)]
        update_block = update_block_class.from_dict(block.to_dict())  # type: ignore
        if isinstance(block, SectionUiBlock) and update_block.children:
            update_block.children = [_ui_block_to_update(child) for child in update_block.children]
        return update_block
    # Allow the block to be serialized as-is rather than runtime error for the user on a type check
    return block  # type: ignore


class CanvasBuilderUiBlock(Generic[UiBlockType]):
    """Internal UI block wrapper for CanvasBuilder."""

    _block: UiBlockType
    _builder: CanvasBuilder

    def __init__(self, block: UiBlockType, builder: CanvasBuilder):
        """Init CanvasBuilderUiBlock."""
        self._block = block
        self._builder = builder

    @classmethod
    def from_api_model(cls, block: UiBlockType, builder: CanvasBuilder) -> CanvasBuilderUiBlock[UiBlockType]:
        """Create a _CanvasBuilderUiBlock from an underlying API model."""
        return cls(block, builder)

    def to_api_model(self) -> UiBlockType:
        """Convert to the underlying API model."""
        return self._block

    def children(self) -> CanvasBuilderBlockStream:
        """
        Return children for blocks when applicable, such as for section blocks.

        If not applicable, returns an empty canvas block stream with no blocks.
        """
        model = self.to_api_model()
        if isinstance(model, SectionUiBlock):
            # MyPy can't recognize the type narrowing when we check .children below
            section_block = cast(SectionUiBlock, model)
            child_blocks = [
                CanvasBuilderUiBlock.from_api_model(block, self._builder) for block in section_block.children
            ]
            # Pass reference to parent block (self)
            return CanvasBuilderBlockStream(self._builder, child_blocks, child_blocks, self)
        return CanvasBuilderBlockStream(self._builder, [], [])

    def replace(self, new_blocks: List[UiBlock]) -> None:
        """Replace block with provided new_blocks."""
        parent = self._parent_block()
        model = cast(UiBlock, self.to_api_model())
        if parent:
            self.insert_after(new_blocks)
            # Keeps MyPy happy; SectionUiBlock is not valid for .children of SectionUiBlock
            assert not (isinstance(model, SectionUiBlock) or isinstance(model, TableUiBlock))
            parent.children.remove(model)
        else:
            self.insert_after(new_blocks)
            # noinspection PyProtectedMember
            self._builder._source_canvas.blocks.remove(model)

    def remove(self) -> None:
        """Remove block."""
        parent = self._parent_block()
        model = cast(UiBlock, self.to_api_model())
        if parent:
            # Keeps MyPy happy; SectionUiBlock is not valid for .children of SectionUiBlock
            assert not (isinstance(model, SectionUiBlock) or isinstance(model, TableUiBlock))
            parent.children.remove(model)
        else:
            # noinspection PyProtectedMember
            self._builder._source_canvas.blocks.remove(model)

    def insert_after(self, new_blocks: List[UiBlock]) -> None:
        """Insert new_blocks after block."""
        self._nested_insert(new_blocks, 1)

    def insert_before(self, new_blocks: List[UiBlock]) -> None:
        """Insert new_blocks before block."""
        self._nested_insert(new_blocks, 0)

    def _nested_insert(self, new_blocks: List[UiBlock], offset: int) -> None:
        """
        Nested insert.

        This is used to handle the case that an insert is being performed and it's contextual within
        another block.

        For instance, the children of a SectionUiBlock.
        """
        parent_block = self._parent_block()
        if parent_block:
            child_blocks = parent_block.children
            # Using list() to solve "List" is invariant creates a copy which means this stops working
            self._insert(new_blocks, offset, child_blocks, self.to_api_model())  # type: ignore
            parent_block.children = child_blocks
            parent_builder_block = CanvasBuilderUiBlock.from_api_model(parent_block, self._builder)
            parent_builder_block.insert_after([parent_block])
            # noinspection PyProtectedMember
            self._builder._source_canvas.blocks.remove(parent_builder_block.to_api_model())
        else:
            # noinspection PyProtectedMember
            self._insert(new_blocks, offset, self._builder._source_canvas.blocks, self.to_api_model())

    @staticmethod
    def _insert(new_blocks: List[UiBlock], offset: int, blocks: List[UiBlock], target_block: UiBlock) -> None:
        """Insert new_blocks before block as a side effect."""
        index = blocks.index(target_block)
        for count, new_block in enumerate(new_blocks):
            blocks.insert(index + count + offset, new_block)

    def _parent_block(self) -> Optional[SectionUiBlock]:
        # noinspection PyProtectedMember
        for parent_block in self._builder._source_canvas.blocks:
            if isinstance(parent_block, SectionUiBlock):
                if self.to_api_model() in parent_block.children:
                    return parent_block
        return None


class CanvasBuilderFilter(Protocol):
    """Callable protocol for specifying a predicate for filtering UiBlocks."""

    def __call__(self, block: UiBlockType) -> bool:
        """Return True if the UiBlock matches specified conditions."""
        pass


class FilteredCanvasBuilderBlockStream:
    """Filtered UI block list wrapper for CanvasBuilder."""

    _builder: CanvasBuilder
    _blocks: List[CanvasBuilderUiBlock]
    _selected_blocks: List[CanvasBuilderUiBlock]
    _cursor: int

    def __init__(
        self,
        builder: CanvasBuilder,
        blocks: List[CanvasBuilderUiBlock],
        selected_blocks: List[CanvasBuilderUiBlock],
    ):
        """Init FilteredCanvasBuilderBlockStream."""
        self._builder = builder
        self._blocks = blocks
        self._selected_blocks = selected_blocks

    def __iter__(self):
        self._cursor = 0
        return self

    def __next__(self):
        if self._cursor >= len(self._blocks):
            raise StopIteration
        block = self._blocks[self._cursor]
        self._cursor += 1
        return block

    @classmethod
    def from_builder(cls: Type[S], builder: CanvasBuilder) -> S:
        """
        From Builder.

        Instantiate a new _FilteredCanvasBuilderBlockStream from a CanvasBuilder.
        """
        # noinspection PyProtectedMember
        blocks = [
            CanvasBuilderUiBlock.from_api_model(block, builder)
            for block in builder._source_canvas.blocks
            if not isinstance(block, UnknownType)
        ]
        return cls(builder, blocks, blocks)

    def filter(self, filter_function: CanvasBuilderFilter) -> FilteredCanvasBuilderBlockStream:
        """
        Filter.

        Accept a predicate that evaluates if a UiBlock should be included in the result or not.
        Returns a new stream of blocks filtered to the predicate, which is further operable.
        """
        return CanvasBuilderBlockStream(
            self._builder,
            self._blocks,
            [block for block in self._selected_blocks if filter_function(block.to_api_model())],
        )

    def get_by_id(self, block_id: str) -> CanvasBuilderUiBlock:
        """
        Get a block by its id.

        Raises NoMatchingBlocksError if the block is not found. To match an id as an optional, use filter().
        """
        matched_block = self._block_by_id(block_id, self._blocks)
        if not matched_block:
            raise NoMatchingBlocksError(f'Could not find a block with id "{block_id}"')
        return matched_block

    def _block_by_id(
        self, block_id: str, blocks: List[CanvasBuilderUiBlock]
    ) -> Optional[CanvasBuilderUiBlock]:
        for block in blocks:
            api_block = block.to_api_model()
            if api_block.id == block_id:
                return block
            children = block.children()
            if children.count() > 0:
                child_block = self._block_by_id(block_id, list(children))
                if child_block:
                    return child_block
        return None

    def count(self) -> int:
        """Return a count of the elements in the list of blocks."""
        return len(self._selected_blocks)

    def first(self) -> CanvasBuilderUiBlock:
        """Return the first block in the list."""
        if len(self._selected_blocks) < 1:
            raise NoMatchingBlocksError
        return self._selected_blocks[0]

    def last(self) -> CanvasBuilderUiBlock:
        """Return the last block in the list."""
        if len(self._selected_blocks) < 1:
            raise NoMatchingBlocksError
        return self._selected_blocks[-1]

    def remove(self) -> None:
        """Remove blocks."""
        updated_blocks = [
            block.to_api_model() for block in self._blocks if block not in self._selected_blocks
        ]
        # noinspection PyProtectedMember
        self._builder._source_canvas.blocks = updated_blocks


class CanvasBuilderBlockStream(FilteredCanvasBuilderBlockStream):
    """
    Internal UI block list wrapper for CanvasBuilder.

    Possesses some additional operations unavailable to filtered block streams.
    """

    _parent: Optional[CanvasBuilderUiBlock]

    def __init__(
        self,
        builder: CanvasBuilder,
        blocks: List[CanvasBuilderUiBlock],
        selected_blocks: List[CanvasBuilderUiBlock],
        parent: Optional[CanvasBuilderUiBlock] = None,
    ):
        """Init CanvasBuilderBlockStream."""
        super().__init__(builder, blocks, selected_blocks)
        self._parent = parent

    def append(self, new_blocks: List[UiBlock]) -> None:
        """
        Append new_blocks to the end of list of blocks.

        Only operates on unfiltered block streams. This can be a list of blocks on a Canvas, or children on a
        block such as SectionUiBlock.
        """
        if self._parent:
            if self.count() > 0:
                self.last().insert_after(new_blocks)
            else:
                self._parent.to_api_model().children.extend(new_blocks)
        else:
            # noinspection PyProtectedMember
            self._builder._source_canvas.blocks.extend(new_blocks)


class CanvasBuilder:
    """
    Canvas Builder.

    This class provides methods to help developers effectively work with Canvas UI Blocks.
    Working with the underlying API models directly can be clunky, as there is no native way to easily find
    blocks based on their attributes, and then operate on them. Some blocks, like SectionUiBlock, have nested
    children blocks, further complicating the unassisted experience.

    The goal of CanvasBuilder is to accept an existing Canvas, and easily change its contents (blocks), then
    send a resulting AppCanvasCreate or AppCanvasUpdate model to the API.

    Some block operations include:
        - Get by Id
        - Filtering by predicate
        - Remove
        - Replace
        - Insert After
        - Insert Before
        - Append

    Sample usage:
        ```
        canvas: Canvas = benchling.apps.get_canvas_by_id("canvas_id")
        builder = CanvasBuilder.from_canvas(canvas).blocks
            .filter(lambda block: isinstance(block, TextInputUiBlock))
            .remove()
        updated_canvas = benchling.apps.update_canvas("canvas_id", builder.to_update())
        ```
    """

    _source_canvas: AppCanvas
    _resource_id: str | Unset

    def __init__(
        self,
        app_id: str,
        feature_id: str,
        resource_id: Optional[str] = None,
        enabled: bool = True,
        session_id: Optional[str] = None,
        blocks: Optional[List[UiBlock]] = None,
        data: Optional[JsonType] = None,
    ):
        """
        Init AppCanvas.

        Create a CanvasBuilder from scratch. Useful when a source AppCanvas is not already created.
        """
        self._source_canvas = AppCanvas(
            app=AppCanvasApp(id=app_id),
            feature_id=feature_id,
            enabled=enabled,
            session_id=session_id,
            blocks=blocks if blocks else [],
            data=json.dumps(data) if data is not None else None,
        )
        self._resource_id = resource_id if resource_id is not None else UNSET

    @property
    def resource_id(self):
        """Returns the underlying resource_id of this CanvasBuilder."""
        return self._resource_id if self._resource_id is not UNSET else None

    @classmethod
    def from_canvas(cls, canvas: AppCanvas) -> CanvasBuilder:
        """
        From Canvas.

        Create a CanvasBuilder from an existing canvas. Preferred when a canvas already exists.
        """
        return cls(
            app_id=canvas.app.id,
            feature_id=canvas.feature_id,
            resource_id=canvas.resource_id,
            enabled=canvas.enabled,
            session_id=canvas.session_id,
            blocks=canvas.blocks,
            data=json.loads(canvas.data) if isinstance(canvas.data, str) else None,
        )

    def _with_enabled(self, value: bool) -> CanvasBuilder:
        # Encapsulated method for toggling Canvas enabled state
        return CanvasBuilder(
            app_id=self._source_canvas.app.id,
            feature_id=self._source_canvas.feature_id,
            resource_id=self.resource_id,
            enabled=value,
            session_id=self._source_canvas.session_id,
            blocks=self._source_canvas.blocks,
            data=self.data_to_json(),
        )

    def with_enabled(self, enabled: bool = True) -> CanvasBuilder:
        """
        Return a new CanvasBuilder with the underlying canvas enabled set to the specified value.

        Specify `False` to disable the canvas.
        This does not call the API, it only assigns state in the CanvasBuilder.
        """
        return self._with_enabled(enabled)

    def with_blocks(self, new_blocks: List[UiBlock]) -> CanvasBuilder:
        """
        Return a new CanvasBuilder with the underlying blocks replaced.

        This does not call the API, it only assigns state in the CanvasBuilder.
        """
        return CanvasBuilder(
            app_id=self._source_canvas.app.id,
            feature_id=self._source_canvas.feature_id,
            resource_id=self.resource_id,
            enabled=self._source_canvas.enabled,
            session_id=self._source_canvas.session_id,
            blocks=new_blocks,
            data=self.data_to_json(),
        )

    def with_data(self, new_data: Optional[JsonType]) -> CanvasBuilder:
        """
        Return a new CanvasBuilder with the underlying data replaced.

        This does not call the API, it only assigns state in the CanvasBuilder.
        """
        return CanvasBuilder(
            app_id=self._source_canvas.app.id,
            feature_id=self._source_canvas.feature_id,
            resource_id=self.resource_id,
            enabled=self._source_canvas.enabled,
            session_id=self._source_canvas.session_id,
            blocks=self._source_canvas.blocks,
            data=new_data,
        )

    def with_session_id(self, session_id: Optional[str]) -> CanvasBuilder:
        """
        Return a new CanvasBuilder with an optional session_id set.

        This does not call the API, it only assigns state in the CanvasBuilder.
        """
        return CanvasBuilder(
            app_id=self._source_canvas.app.id,
            feature_id=self._source_canvas.feature_id,
            resource_id=self.resource_id,
            enabled=self._source_canvas.enabled,
            session_id=session_id,
            blocks=self._source_canvas.blocks,
            data=self.data_to_json(),
        )

    def inputs_to_dict(self) -> Dict[str, Union[str, List[str]]]:
        """
        Read Inputs to dict.

        Return a dictionary of {block_id: block_value} for all blocks on the canvas with input values.
        Includes blocks with a value that can be a str or multivalued. Excludes TableUiBlock.
        Blocks that only have read attributes are omitted.

        List of included blocks:
            DropdownMultiValueUiBlock
            DropdownUiBlock
            SearchInputMultiValueUiBlock
            SearchInputUiBlock
            SelectorInputMultiValueUiBlock
            SelectorInputUiBlock
            TextInputUiBlock

        Raise DuplicateBlockIdError if multiple blocks with the same id are found.
        """
        return self._values_from_blocks(
            self._source_canvas.blocks,
            included_classes={
                DropdownMultiValueUiBlock,
                DropdownUiBlock,
                SearchInputMultiValueUiBlock,
                SearchInputUiBlock,
                SelectorInputMultiValueUiBlock,
                SelectorInputUiBlock,
                TextInputUiBlock,
            },
        )

    def inputs_to_dict_single_value(self) -> Dict[str, str]:
        """
        Read Inputs to dict, but only for single-valued blocks.

        Return a dictionary of {block_id: block_value} for all blocks on the canvas with single input values.
        Blocks that only have read attributes are omitted. Excludes TableUiBlock.

        List of included blocks:
            DropdownUiBlock
            SearchInputUiBlock
            SelectorInputUiBlock
            TextInputUiBlock

        Raise DuplicateBlockIdError if multiple blocks with the same id are found.
        """
        return cast(
            Dict[str, str],
            self._values_from_blocks(
                self._source_canvas.blocks,
                included_classes={
                    DropdownUiBlock,
                    SearchInputUiBlock,
                    SelectorInputUiBlock,
                    TextInputUiBlock,
                },
            ),
        )

    def inputs_to_dict_multi_value(self) -> Dict[str, List[str]]:
        """
        Read Inputs to dict, but only for multivalued blocks.

        Return a dictionary of {block_id: block_value} for all blocks on the canvas with multivalued input values.
        Blocks that only have read attributes are omitted. Excludes TableUiBlock.

        List of included blocks:
            DropdownMultiValueUiBlock
            SearchInputMultiValueUiBlock
            SelectorInputMultiValueUiBlock

        Raise DuplicateBlockIdError if multiple blocks with the same id are found.
        """
        return cast(
            Dict[str, List[str]],
            self._values_from_blocks(
                self._source_canvas.blocks,
                included_classes={
                    DropdownMultiValueUiBlock,
                    SearchInputMultiValueUiBlock,
                    SelectorInputMultiValueUiBlock,
                },
            ),
        )

    def _values_from_blocks(
        self,
        blocks: List[UiBlock],
        existing_keys: Optional[List[str]] = None,
        included_classes: Optional[Set[Type[UiBlock]]] = None,
    ) -> Dict[str, Union[str, List[str]]]:
        existing_keys = existing_keys if existing_keys else []
        values: Dict[str, Union[str, List[str]]] = dict()
        for block in blocks:
            # When included_classes is None, include all blocks
            if not isinstance(block, UnknownType) and (
                included_classes is None
                or isinstance(block, SectionUiBlock)
                or _is_included_class(included_classes, block)
            ):
                if hasattr(block, "value"):
                    if block.id in existing_keys:
                        raise DuplicateBlockIdError(
                            f'More than one block with the id "{block.id}" already exists'
                        )
                    existing_keys.append(block.id)
                    # Ignore type error since we checked hasattr above
                    values[block.id] = block.value  # type: ignore
                elif isinstance(block, SectionUiBlock):
                    # Cast to appease MyPy
                    parent_block = cast(SectionUiBlock, block)
                    # list() prevents MyPy from complaining: "List" is invariant
                    child_values = self._values_from_blocks(
                        list(parent_block.children), existing_keys, included_classes=included_classes
                    )
                    values.update(child_values)
        return values

    def to_update(self) -> AppCanvasUpdate:
        """Return an AppCanvasUpdate API model from the current state of the canvas managed by CanvasBuilder."""
        return AppCanvasUpdate(
            feature_id=self._source_canvas.feature_id,
            resource_id=self._resource_id,
            enabled=self._source_canvas.enabled,
            session_id=self._source_canvas.session_id,
            blocks=[_ui_block_to_update(block) for block in self._source_canvas.blocks],
            data=self._source_canvas.data,
        )

    def to_create(self) -> AppCanvasCreate:
        """
        Return an AppCanvasCreate API model from the current state of the canvas managed by CanvasBuilder.

        Raise MissingResourceIdError if the current state of the canvas managed by CanvasBuilder does not include
        a resource ID. Without a resource ID indicating the Benchling object on which to place the new canvas,
        canvas creation is underspecified and cannot be completed successfully.
        """
        if self.resource_id is None:
            raise MissingResourceIdError

        return AppCanvasCreate(
            app_id=self._source_canvas.app.id,
            feature_id=self._source_canvas.feature_id,
            resource_id=self.resource_id,
            enabled=self._source_canvas.enabled,
            session_id=self._source_canvas.session_id,
            blocks=[_ui_block_to_create(block) for block in self._source_canvas.blocks],
            data=self._source_canvas.data,
        )

    @property
    def blocks(self) -> CanvasBuilderBlockStream:
        """
        Blocks.

        Return a stream of blocks which can be iterated and operated on to mutate the canvas
        stored by the builder.
        """
        return CanvasBuilderBlockStream.from_builder(self)

    def data_to_json(self) -> Optional[JsonType]:
        """
        Convert Canvas data to JSON.

        Return a JSON object parsed from the string of the canvas's `data`, if present. Otherwise, return None.
        """
        return json.loads(self._source_canvas.data) if self._source_canvas.data is not None else None

    def __eq__(self, other) -> bool:
        return isinstance(other, CanvasBuilder) and self._source_canvas == other._source_canvas


def _is_included_class(included_classes: Set[Type[UiBlock]], target_class: UiBlock) -> bool:
    return isinstance(target_class, tuple(c for c in included_classes))
