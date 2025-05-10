from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError, UnknownType
from ..models.button_ui_block_update import ButtonUiBlockUpdate
from ..models.chip_ui_block_update import ChipUiBlockUpdate
from ..models.dropdown_multi_value_ui_block_update import DropdownMultiValueUiBlockUpdate
from ..models.dropdown_ui_block_update import DropdownUiBlockUpdate
from ..models.file_upload_ui_block_update import FileUploadUiBlockUpdate
from ..models.markdown_ui_block_update import MarkdownUiBlockUpdate
from ..models.search_input_multi_value_ui_block_update import SearchInputMultiValueUiBlockUpdate
from ..models.search_input_ui_block_update import SearchInputUiBlockUpdate
from ..models.section_ui_block_update import SectionUiBlockUpdate
from ..models.selector_input_multi_value_ui_block_update import SelectorInputMultiValueUiBlockUpdate
from ..models.selector_input_ui_block_update import SelectorInputUiBlockUpdate
from ..models.table_ui_block_update import TableUiBlockUpdate
from ..models.text_input_ui_block_update import TextInputUiBlockUpdate
from ..types import UNSET, Unset

T = TypeVar("T", bound="AppCanvasUpdateUiBlockList")


@attr.s(auto_attribs=True, repr=False)
class AppCanvasUpdateUiBlockList:
    """  """

    _blocks: Union[
        Unset,
        List[
            Union[
                ButtonUiBlockUpdate,
                ChipUiBlockUpdate,
                DropdownUiBlockUpdate,
                DropdownMultiValueUiBlockUpdate,
                FileUploadUiBlockUpdate,
                MarkdownUiBlockUpdate,
                SearchInputUiBlockUpdate,
                SearchInputMultiValueUiBlockUpdate,
                SectionUiBlockUpdate,
                SelectorInputUiBlockUpdate,
                SelectorInputMultiValueUiBlockUpdate,
                TextInputUiBlockUpdate,
                TableUiBlockUpdate,
                UnknownType,
            ]
        ],
    ] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("blocks={}".format(repr(self._blocks)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "AppCanvasUpdateUiBlockList({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        blocks: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._blocks, Unset):
            blocks = []
            for blocks_item_data in self._blocks:
                if isinstance(blocks_item_data, UnknownType):
                    blocks_item = blocks_item_data.value
                elif isinstance(blocks_item_data, ButtonUiBlockUpdate):
                    blocks_item = blocks_item_data.to_dict()

                elif isinstance(blocks_item_data, ChipUiBlockUpdate):
                    blocks_item = blocks_item_data.to_dict()

                elif isinstance(blocks_item_data, DropdownUiBlockUpdate):
                    blocks_item = blocks_item_data.to_dict()

                elif isinstance(blocks_item_data, DropdownMultiValueUiBlockUpdate):
                    blocks_item = blocks_item_data.to_dict()

                elif isinstance(blocks_item_data, FileUploadUiBlockUpdate):
                    blocks_item = blocks_item_data.to_dict()

                elif isinstance(blocks_item_data, MarkdownUiBlockUpdate):
                    blocks_item = blocks_item_data.to_dict()

                elif isinstance(blocks_item_data, SearchInputUiBlockUpdate):
                    blocks_item = blocks_item_data.to_dict()

                elif isinstance(blocks_item_data, SearchInputMultiValueUiBlockUpdate):
                    blocks_item = blocks_item_data.to_dict()

                elif isinstance(blocks_item_data, SectionUiBlockUpdate):
                    blocks_item = blocks_item_data.to_dict()

                elif isinstance(blocks_item_data, SelectorInputUiBlockUpdate):
                    blocks_item = blocks_item_data.to_dict()

                elif isinstance(blocks_item_data, SelectorInputMultiValueUiBlockUpdate):
                    blocks_item = blocks_item_data.to_dict()

                elif isinstance(blocks_item_data, TextInputUiBlockUpdate):
                    blocks_item = blocks_item_data.to_dict()

                else:
                    blocks_item = blocks_item_data.to_dict()

                blocks.append(blocks_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if blocks is not UNSET:
            field_dict["blocks"] = blocks

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_blocks() -> Union[
            Unset,
            List[
                Union[
                    ButtonUiBlockUpdate,
                    ChipUiBlockUpdate,
                    DropdownUiBlockUpdate,
                    DropdownMultiValueUiBlockUpdate,
                    FileUploadUiBlockUpdate,
                    MarkdownUiBlockUpdate,
                    SearchInputUiBlockUpdate,
                    SearchInputMultiValueUiBlockUpdate,
                    SectionUiBlockUpdate,
                    SelectorInputUiBlockUpdate,
                    SelectorInputMultiValueUiBlockUpdate,
                    TextInputUiBlockUpdate,
                    TableUiBlockUpdate,
                    UnknownType,
                ]
            ],
        ]:
            blocks = []
            _blocks = d.pop("blocks")
            for blocks_item_data in _blocks or []:

                def _parse_blocks_item(
                    data: Union[Dict[str, Any]]
                ) -> Union[
                    ButtonUiBlockUpdate,
                    ChipUiBlockUpdate,
                    DropdownUiBlockUpdate,
                    DropdownMultiValueUiBlockUpdate,
                    FileUploadUiBlockUpdate,
                    MarkdownUiBlockUpdate,
                    SearchInputUiBlockUpdate,
                    SearchInputMultiValueUiBlockUpdate,
                    SectionUiBlockUpdate,
                    SelectorInputUiBlockUpdate,
                    SelectorInputMultiValueUiBlockUpdate,
                    TextInputUiBlockUpdate,
                    TableUiBlockUpdate,
                    UnknownType,
                ]:
                    blocks_item: Union[
                        ButtonUiBlockUpdate,
                        ChipUiBlockUpdate,
                        DropdownUiBlockUpdate,
                        DropdownMultiValueUiBlockUpdate,
                        FileUploadUiBlockUpdate,
                        MarkdownUiBlockUpdate,
                        SearchInputUiBlockUpdate,
                        SearchInputMultiValueUiBlockUpdate,
                        SectionUiBlockUpdate,
                        SelectorInputUiBlockUpdate,
                        SelectorInputMultiValueUiBlockUpdate,
                        TextInputUiBlockUpdate,
                        TableUiBlockUpdate,
                        UnknownType,
                    ]
                    discriminator_value: str = cast(str, data.get("type"))
                    if discriminator_value is not None:
                        if discriminator_value == "BUTTON":
                            blocks_item = ButtonUiBlockUpdate.from_dict(data, strict=False)

                            return blocks_item
                        if discriminator_value == "CHIP":
                            blocks_item = ChipUiBlockUpdate.from_dict(data, strict=False)

                            return blocks_item
                        if discriminator_value == "DROPDOWN":
                            blocks_item = DropdownUiBlockUpdate.from_dict(data, strict=False)

                            return blocks_item
                        if discriminator_value == "DROPDOWN_MULTIVALUE":
                            blocks_item = DropdownMultiValueUiBlockUpdate.from_dict(data, strict=False)

                            return blocks_item
                        if discriminator_value == "FILE_UPLOAD":
                            blocks_item = FileUploadUiBlockUpdate.from_dict(data, strict=False)

                            return blocks_item
                        if discriminator_value == "MARKDOWN":
                            blocks_item = MarkdownUiBlockUpdate.from_dict(data, strict=False)

                            return blocks_item
                        if discriminator_value == "SEARCH_INPUT":
                            blocks_item = SearchInputUiBlockUpdate.from_dict(data, strict=False)

                            return blocks_item
                        if discriminator_value == "SEARCH_INPUT_MULTIVALUE":
                            blocks_item = SearchInputMultiValueUiBlockUpdate.from_dict(data, strict=False)

                            return blocks_item
                        if discriminator_value == "SECTION":
                            blocks_item = SectionUiBlockUpdate.from_dict(data, strict=False)

                            return blocks_item
                        if discriminator_value == "SELECTOR_INPUT":
                            blocks_item = SelectorInputUiBlockUpdate.from_dict(data, strict=False)

                            return blocks_item
                        if discriminator_value == "SELECTOR_INPUT_MULTIVALUE":
                            blocks_item = SelectorInputMultiValueUiBlockUpdate.from_dict(data, strict=False)

                            return blocks_item
                        if discriminator_value == "TABLE":
                            blocks_item = TableUiBlockUpdate.from_dict(data, strict=False)

                            return blocks_item
                        if discriminator_value == "TEXT_INPUT":
                            blocks_item = TextInputUiBlockUpdate.from_dict(data, strict=False)

                            return blocks_item

                        return UnknownType(value=data)
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        blocks_item = ButtonUiBlockUpdate.from_dict(data, strict=True)

                        return blocks_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        blocks_item = ChipUiBlockUpdate.from_dict(data, strict=True)

                        return blocks_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        blocks_item = DropdownUiBlockUpdate.from_dict(data, strict=True)

                        return blocks_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        blocks_item = DropdownMultiValueUiBlockUpdate.from_dict(data, strict=True)

                        return blocks_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        blocks_item = FileUploadUiBlockUpdate.from_dict(data, strict=True)

                        return blocks_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        blocks_item = MarkdownUiBlockUpdate.from_dict(data, strict=True)

                        return blocks_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        blocks_item = SearchInputUiBlockUpdate.from_dict(data, strict=True)

                        return blocks_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        blocks_item = SearchInputMultiValueUiBlockUpdate.from_dict(data, strict=True)

                        return blocks_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        blocks_item = SectionUiBlockUpdate.from_dict(data, strict=True)

                        return blocks_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        blocks_item = SelectorInputUiBlockUpdate.from_dict(data, strict=True)

                        return blocks_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        blocks_item = SelectorInputMultiValueUiBlockUpdate.from_dict(data, strict=True)

                        return blocks_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        blocks_item = TextInputUiBlockUpdate.from_dict(data, strict=True)

                        return blocks_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        blocks_item = TableUiBlockUpdate.from_dict(data, strict=True)

                        return blocks_item
                    except:  # noqa: E722
                        pass
                    return UnknownType(data)

                blocks_item = _parse_blocks_item(blocks_item_data)

                blocks.append(blocks_item)

            return blocks

        try:
            blocks = get_blocks()
        except KeyError:
            if strict:
                raise
            blocks = cast(
                Union[
                    Unset,
                    List[
                        Union[
                            ButtonUiBlockUpdate,
                            ChipUiBlockUpdate,
                            DropdownUiBlockUpdate,
                            DropdownMultiValueUiBlockUpdate,
                            FileUploadUiBlockUpdate,
                            MarkdownUiBlockUpdate,
                            SearchInputUiBlockUpdate,
                            SearchInputMultiValueUiBlockUpdate,
                            SectionUiBlockUpdate,
                            SelectorInputUiBlockUpdate,
                            SelectorInputMultiValueUiBlockUpdate,
                            TextInputUiBlockUpdate,
                            TableUiBlockUpdate,
                            UnknownType,
                        ]
                    ],
                ],
                UNSET,
            )

        app_canvas_update_ui_block_list = cls(
            blocks=blocks,
        )

        app_canvas_update_ui_block_list.additional_properties = d
        return app_canvas_update_ui_block_list

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties

    def get(self, key, default=None) -> Optional[Any]:
        return self.additional_properties.get(key, default)

    @property
    def blocks(
        self,
    ) -> List[
        Union[
            ButtonUiBlockUpdate,
            ChipUiBlockUpdate,
            DropdownUiBlockUpdate,
            DropdownMultiValueUiBlockUpdate,
            FileUploadUiBlockUpdate,
            MarkdownUiBlockUpdate,
            SearchInputUiBlockUpdate,
            SearchInputMultiValueUiBlockUpdate,
            SectionUiBlockUpdate,
            SelectorInputUiBlockUpdate,
            SelectorInputMultiValueUiBlockUpdate,
            TextInputUiBlockUpdate,
            TableUiBlockUpdate,
            UnknownType,
        ]
    ]:
        if isinstance(self._blocks, Unset):
            raise NotPresentError(self, "blocks")
        return self._blocks

    @blocks.setter
    def blocks(
        self,
        value: List[
            Union[
                ButtonUiBlockUpdate,
                ChipUiBlockUpdate,
                DropdownUiBlockUpdate,
                DropdownMultiValueUiBlockUpdate,
                FileUploadUiBlockUpdate,
                MarkdownUiBlockUpdate,
                SearchInputUiBlockUpdate,
                SearchInputMultiValueUiBlockUpdate,
                SectionUiBlockUpdate,
                SelectorInputUiBlockUpdate,
                SelectorInputMultiValueUiBlockUpdate,
                TextInputUiBlockUpdate,
                TableUiBlockUpdate,
                UnknownType,
            ]
        ],
    ) -> None:
        self._blocks = value

    @blocks.deleter
    def blocks(self) -> None:
        self._blocks = UNSET
