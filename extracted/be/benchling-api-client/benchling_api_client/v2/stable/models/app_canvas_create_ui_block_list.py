from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError, UnknownType
from ..models.button_ui_block_create import ButtonUiBlockCreate
from ..models.chip_ui_block_create import ChipUiBlockCreate
from ..models.dropdown_multi_value_ui_block_create import DropdownMultiValueUiBlockCreate
from ..models.dropdown_ui_block_create import DropdownUiBlockCreate
from ..models.file_upload_ui_block_create import FileUploadUiBlockCreate
from ..models.markdown_ui_block_create import MarkdownUiBlockCreate
from ..models.search_input_multi_value_ui_block_create import SearchInputMultiValueUiBlockCreate
from ..models.search_input_ui_block_create import SearchInputUiBlockCreate
from ..models.section_ui_block_create import SectionUiBlockCreate
from ..models.selector_input_multi_value_ui_block_create import SelectorInputMultiValueUiBlockCreate
from ..models.selector_input_ui_block_create import SelectorInputUiBlockCreate
from ..models.table_ui_block_create import TableUiBlockCreate
from ..models.text_input_ui_block_create import TextInputUiBlockCreate
from ..types import UNSET, Unset

T = TypeVar("T", bound="AppCanvasCreateUiBlockList")


@attr.s(auto_attribs=True, repr=False)
class AppCanvasCreateUiBlockList:
    """  """

    _blocks: Union[
        Unset,
        List[
            Union[
                ButtonUiBlockCreate,
                ChipUiBlockCreate,
                DropdownUiBlockCreate,
                DropdownMultiValueUiBlockCreate,
                FileUploadUiBlockCreate,
                MarkdownUiBlockCreate,
                SearchInputUiBlockCreate,
                SearchInputMultiValueUiBlockCreate,
                SectionUiBlockCreate,
                SelectorInputUiBlockCreate,
                SelectorInputMultiValueUiBlockCreate,
                TextInputUiBlockCreate,
                TableUiBlockCreate,
                UnknownType,
            ]
        ],
    ] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("blocks={}".format(repr(self._blocks)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "AppCanvasCreateUiBlockList({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        blocks: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._blocks, Unset):
            blocks = []
            for blocks_item_data in self._blocks:
                if isinstance(blocks_item_data, UnknownType):
                    blocks_item = blocks_item_data.value
                elif isinstance(blocks_item_data, ButtonUiBlockCreate):
                    blocks_item = blocks_item_data.to_dict()

                elif isinstance(blocks_item_data, ChipUiBlockCreate):
                    blocks_item = blocks_item_data.to_dict()

                elif isinstance(blocks_item_data, DropdownUiBlockCreate):
                    blocks_item = blocks_item_data.to_dict()

                elif isinstance(blocks_item_data, DropdownMultiValueUiBlockCreate):
                    blocks_item = blocks_item_data.to_dict()

                elif isinstance(blocks_item_data, FileUploadUiBlockCreate):
                    blocks_item = blocks_item_data.to_dict()

                elif isinstance(blocks_item_data, MarkdownUiBlockCreate):
                    blocks_item = blocks_item_data.to_dict()

                elif isinstance(blocks_item_data, SearchInputUiBlockCreate):
                    blocks_item = blocks_item_data.to_dict()

                elif isinstance(blocks_item_data, SearchInputMultiValueUiBlockCreate):
                    blocks_item = blocks_item_data.to_dict()

                elif isinstance(blocks_item_data, SectionUiBlockCreate):
                    blocks_item = blocks_item_data.to_dict()

                elif isinstance(blocks_item_data, SelectorInputUiBlockCreate):
                    blocks_item = blocks_item_data.to_dict()

                elif isinstance(blocks_item_data, SelectorInputMultiValueUiBlockCreate):
                    blocks_item = blocks_item_data.to_dict()

                elif isinstance(blocks_item_data, TextInputUiBlockCreate):
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
                    ButtonUiBlockCreate,
                    ChipUiBlockCreate,
                    DropdownUiBlockCreate,
                    DropdownMultiValueUiBlockCreate,
                    FileUploadUiBlockCreate,
                    MarkdownUiBlockCreate,
                    SearchInputUiBlockCreate,
                    SearchInputMultiValueUiBlockCreate,
                    SectionUiBlockCreate,
                    SelectorInputUiBlockCreate,
                    SelectorInputMultiValueUiBlockCreate,
                    TextInputUiBlockCreate,
                    TableUiBlockCreate,
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
                    ButtonUiBlockCreate,
                    ChipUiBlockCreate,
                    DropdownUiBlockCreate,
                    DropdownMultiValueUiBlockCreate,
                    FileUploadUiBlockCreate,
                    MarkdownUiBlockCreate,
                    SearchInputUiBlockCreate,
                    SearchInputMultiValueUiBlockCreate,
                    SectionUiBlockCreate,
                    SelectorInputUiBlockCreate,
                    SelectorInputMultiValueUiBlockCreate,
                    TextInputUiBlockCreate,
                    TableUiBlockCreate,
                    UnknownType,
                ]:
                    blocks_item: Union[
                        ButtonUiBlockCreate,
                        ChipUiBlockCreate,
                        DropdownUiBlockCreate,
                        DropdownMultiValueUiBlockCreate,
                        FileUploadUiBlockCreate,
                        MarkdownUiBlockCreate,
                        SearchInputUiBlockCreate,
                        SearchInputMultiValueUiBlockCreate,
                        SectionUiBlockCreate,
                        SelectorInputUiBlockCreate,
                        SelectorInputMultiValueUiBlockCreate,
                        TextInputUiBlockCreate,
                        TableUiBlockCreate,
                        UnknownType,
                    ]
                    discriminator_value: str = cast(str, data.get("type"))
                    if discriminator_value is not None:
                        if discriminator_value == "BUTTON":
                            blocks_item = ButtonUiBlockCreate.from_dict(data, strict=False)

                            return blocks_item
                        if discriminator_value == "CHIP":
                            blocks_item = ChipUiBlockCreate.from_dict(data, strict=False)

                            return blocks_item
                        if discriminator_value == "DROPDOWN":
                            blocks_item = DropdownUiBlockCreate.from_dict(data, strict=False)

                            return blocks_item
                        if discriminator_value == "DROPDOWN_MULTIVALUE":
                            blocks_item = DropdownMultiValueUiBlockCreate.from_dict(data, strict=False)

                            return blocks_item
                        if discriminator_value == "FILE_UPLOAD":
                            blocks_item = FileUploadUiBlockCreate.from_dict(data, strict=False)

                            return blocks_item
                        if discriminator_value == "MARKDOWN":
                            blocks_item = MarkdownUiBlockCreate.from_dict(data, strict=False)

                            return blocks_item
                        if discriminator_value == "SEARCH_INPUT":
                            blocks_item = SearchInputUiBlockCreate.from_dict(data, strict=False)

                            return blocks_item
                        if discriminator_value == "SEARCH_INPUT_MULTIVALUE":
                            blocks_item = SearchInputMultiValueUiBlockCreate.from_dict(data, strict=False)

                            return blocks_item
                        if discriminator_value == "SECTION":
                            blocks_item = SectionUiBlockCreate.from_dict(data, strict=False)

                            return blocks_item
                        if discriminator_value == "SELECTOR_INPUT":
                            blocks_item = SelectorInputUiBlockCreate.from_dict(data, strict=False)

                            return blocks_item
                        if discriminator_value == "SELECTOR_INPUT_MULTIVALUE":
                            blocks_item = SelectorInputMultiValueUiBlockCreate.from_dict(data, strict=False)

                            return blocks_item
                        if discriminator_value == "TABLE":
                            blocks_item = TableUiBlockCreate.from_dict(data, strict=False)

                            return blocks_item
                        if discriminator_value == "TEXT_INPUT":
                            blocks_item = TextInputUiBlockCreate.from_dict(data, strict=False)

                            return blocks_item

                        return UnknownType(value=data)
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        blocks_item = ButtonUiBlockCreate.from_dict(data, strict=True)

                        return blocks_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        blocks_item = ChipUiBlockCreate.from_dict(data, strict=True)

                        return blocks_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        blocks_item = DropdownUiBlockCreate.from_dict(data, strict=True)

                        return blocks_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        blocks_item = DropdownMultiValueUiBlockCreate.from_dict(data, strict=True)

                        return blocks_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        blocks_item = FileUploadUiBlockCreate.from_dict(data, strict=True)

                        return blocks_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        blocks_item = MarkdownUiBlockCreate.from_dict(data, strict=True)

                        return blocks_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        blocks_item = SearchInputUiBlockCreate.from_dict(data, strict=True)

                        return blocks_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        blocks_item = SearchInputMultiValueUiBlockCreate.from_dict(data, strict=True)

                        return blocks_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        blocks_item = SectionUiBlockCreate.from_dict(data, strict=True)

                        return blocks_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        blocks_item = SelectorInputUiBlockCreate.from_dict(data, strict=True)

                        return blocks_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        blocks_item = SelectorInputMultiValueUiBlockCreate.from_dict(data, strict=True)

                        return blocks_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        blocks_item = TextInputUiBlockCreate.from_dict(data, strict=True)

                        return blocks_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        blocks_item = TableUiBlockCreate.from_dict(data, strict=True)

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
                            ButtonUiBlockCreate,
                            ChipUiBlockCreate,
                            DropdownUiBlockCreate,
                            DropdownMultiValueUiBlockCreate,
                            FileUploadUiBlockCreate,
                            MarkdownUiBlockCreate,
                            SearchInputUiBlockCreate,
                            SearchInputMultiValueUiBlockCreate,
                            SectionUiBlockCreate,
                            SelectorInputUiBlockCreate,
                            SelectorInputMultiValueUiBlockCreate,
                            TextInputUiBlockCreate,
                            TableUiBlockCreate,
                            UnknownType,
                        ]
                    ],
                ],
                UNSET,
            )

        app_canvas_create_ui_block_list = cls(
            blocks=blocks,
        )

        app_canvas_create_ui_block_list.additional_properties = d
        return app_canvas_create_ui_block_list

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
            ButtonUiBlockCreate,
            ChipUiBlockCreate,
            DropdownUiBlockCreate,
            DropdownMultiValueUiBlockCreate,
            FileUploadUiBlockCreate,
            MarkdownUiBlockCreate,
            SearchInputUiBlockCreate,
            SearchInputMultiValueUiBlockCreate,
            SectionUiBlockCreate,
            SelectorInputUiBlockCreate,
            SelectorInputMultiValueUiBlockCreate,
            TextInputUiBlockCreate,
            TableUiBlockCreate,
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
                ButtonUiBlockCreate,
                ChipUiBlockCreate,
                DropdownUiBlockCreate,
                DropdownMultiValueUiBlockCreate,
                FileUploadUiBlockCreate,
                MarkdownUiBlockCreate,
                SearchInputUiBlockCreate,
                SearchInputMultiValueUiBlockCreate,
                SectionUiBlockCreate,
                SelectorInputUiBlockCreate,
                SelectorInputMultiValueUiBlockCreate,
                TextInputUiBlockCreate,
                TableUiBlockCreate,
                UnknownType,
            ]
        ],
    ) -> None:
        self._blocks = value

    @blocks.deleter
    def blocks(self) -> None:
        self._blocks = UNSET
