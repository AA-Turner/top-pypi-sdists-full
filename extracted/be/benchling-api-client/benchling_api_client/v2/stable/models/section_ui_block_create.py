from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError, UnknownType
from ..models.button_ui_block import ButtonUiBlock
from ..models.chip_ui_block import ChipUiBlock
from ..models.dropdown_multi_value_ui_block import DropdownMultiValueUiBlock
from ..models.dropdown_ui_block import DropdownUiBlock
from ..models.file_upload_ui_block import FileUploadUiBlock
from ..models.markdown_ui_block import MarkdownUiBlock
from ..models.search_input_multi_value_ui_block import SearchInputMultiValueUiBlock
from ..models.search_input_ui_block import SearchInputUiBlock
from ..models.section_ui_block_type import SectionUiBlockType
from ..models.selector_input_multi_value_ui_block import SelectorInputMultiValueUiBlock
from ..models.selector_input_ui_block import SelectorInputUiBlock
from ..models.text_input_ui_block import TextInputUiBlock
from ..types import UNSET, Unset

T = TypeVar("T", bound="SectionUiBlockCreate")


@attr.s(auto_attribs=True, repr=False)
class SectionUiBlockCreate:
    """  """

    _children: List[
        Union[
            ButtonUiBlock,
            ChipUiBlock,
            DropdownUiBlock,
            DropdownMultiValueUiBlock,
            FileUploadUiBlock,
            MarkdownUiBlock,
            SearchInputUiBlock,
            SearchInputMultiValueUiBlock,
            SelectorInputUiBlock,
            SelectorInputMultiValueUiBlock,
            TextInputUiBlock,
            UnknownType,
        ]
    ]
    _id: Union[Unset, str] = UNSET
    _type: Union[Unset, SectionUiBlockType] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("children={}".format(repr(self._children)))
        fields.append("id={}".format(repr(self._id)))
        fields.append("type={}".format(repr(self._type)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "SectionUiBlockCreate({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        children = []
        for children_item_data in self._children:
            if isinstance(children_item_data, UnknownType):
                children_item = children_item_data.value
            elif isinstance(children_item_data, ButtonUiBlock):
                children_item = children_item_data.to_dict()

            elif isinstance(children_item_data, ChipUiBlock):
                children_item = children_item_data.to_dict()

            elif isinstance(children_item_data, DropdownUiBlock):
                children_item = children_item_data.to_dict()

            elif isinstance(children_item_data, DropdownMultiValueUiBlock):
                children_item = children_item_data.to_dict()

            elif isinstance(children_item_data, FileUploadUiBlock):
                children_item = children_item_data.to_dict()

            elif isinstance(children_item_data, MarkdownUiBlock):
                children_item = children_item_data.to_dict()

            elif isinstance(children_item_data, SearchInputUiBlock):
                children_item = children_item_data.to_dict()

            elif isinstance(children_item_data, SearchInputMultiValueUiBlock):
                children_item = children_item_data.to_dict()

            elif isinstance(children_item_data, SelectorInputUiBlock):
                children_item = children_item_data.to_dict()

            elif isinstance(children_item_data, SelectorInputMultiValueUiBlock):
                children_item = children_item_data.to_dict()

            else:
                children_item = children_item_data.to_dict()

            children.append(children_item)

        id = self._id
        type: Union[Unset, int] = UNSET
        if not isinstance(self._type, Unset):
            type = self._type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if children is not UNSET:
            field_dict["children"] = children
        if id is not UNSET:
            field_dict["id"] = id
        if type is not UNSET:
            field_dict["type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_children() -> List[
            Union[
                ButtonUiBlock,
                ChipUiBlock,
                DropdownUiBlock,
                DropdownMultiValueUiBlock,
                FileUploadUiBlock,
                MarkdownUiBlock,
                SearchInputUiBlock,
                SearchInputMultiValueUiBlock,
                SelectorInputUiBlock,
                SelectorInputMultiValueUiBlock,
                TextInputUiBlock,
                UnknownType,
            ]
        ]:
            children = []
            _children = d.pop("children")
            for children_item_data in _children:

                def _parse_children_item(
                    data: Union[Dict[str, Any]]
                ) -> Union[
                    ButtonUiBlock,
                    ChipUiBlock,
                    DropdownUiBlock,
                    DropdownMultiValueUiBlock,
                    FileUploadUiBlock,
                    MarkdownUiBlock,
                    SearchInputUiBlock,
                    SearchInputMultiValueUiBlock,
                    SelectorInputUiBlock,
                    SelectorInputMultiValueUiBlock,
                    TextInputUiBlock,
                    UnknownType,
                ]:
                    children_item: Union[
                        ButtonUiBlock,
                        ChipUiBlock,
                        DropdownUiBlock,
                        DropdownMultiValueUiBlock,
                        FileUploadUiBlock,
                        MarkdownUiBlock,
                        SearchInputUiBlock,
                        SearchInputMultiValueUiBlock,
                        SelectorInputUiBlock,
                        SelectorInputMultiValueUiBlock,
                        TextInputUiBlock,
                        UnknownType,
                    ]
                    discriminator_value: str = cast(str, data.get("type"))
                    if discriminator_value is not None:
                        if discriminator_value == "BUTTON":
                            children_item = ButtonUiBlock.from_dict(data, strict=False)

                            return children_item
                        if discriminator_value == "CHIP":
                            children_item = ChipUiBlock.from_dict(data, strict=False)

                            return children_item
                        if discriminator_value == "DROPDOWN":
                            children_item = DropdownUiBlock.from_dict(data, strict=False)

                            return children_item
                        if discriminator_value == "DROPDOWN_MULTIVALUE":
                            children_item = DropdownMultiValueUiBlock.from_dict(data, strict=False)

                            return children_item
                        if discriminator_value == "FILE_UPLOAD":
                            children_item = FileUploadUiBlock.from_dict(data, strict=False)

                            return children_item
                        if discriminator_value == "MARKDOWN":
                            children_item = MarkdownUiBlock.from_dict(data, strict=False)

                            return children_item
                        if discriminator_value == "SEARCH_INPUT":
                            children_item = SearchInputUiBlock.from_dict(data, strict=False)

                            return children_item
                        if discriminator_value == "SEARCH_INPUT_MULTIVALUE":
                            children_item = SearchInputMultiValueUiBlock.from_dict(data, strict=False)

                            return children_item
                        if discriminator_value == "SELECTOR_INPUT":
                            children_item = SelectorInputUiBlock.from_dict(data, strict=False)

                            return children_item
                        if discriminator_value == "SELECTOR_INPUT_MULTIVALUE":
                            children_item = SelectorInputMultiValueUiBlock.from_dict(data, strict=False)

                            return children_item
                        if discriminator_value == "TEXT_INPUT":
                            children_item = TextInputUiBlock.from_dict(data, strict=False)

                            return children_item

                        return UnknownType(value=data)
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        children_item = ButtonUiBlock.from_dict(data, strict=True)

                        return children_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        children_item = ChipUiBlock.from_dict(data, strict=True)

                        return children_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        children_item = DropdownUiBlock.from_dict(data, strict=True)

                        return children_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        children_item = DropdownMultiValueUiBlock.from_dict(data, strict=True)

                        return children_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        children_item = FileUploadUiBlock.from_dict(data, strict=True)

                        return children_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        children_item = MarkdownUiBlock.from_dict(data, strict=True)

                        return children_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        children_item = SearchInputUiBlock.from_dict(data, strict=True)

                        return children_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        children_item = SearchInputMultiValueUiBlock.from_dict(data, strict=True)

                        return children_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        children_item = SelectorInputUiBlock.from_dict(data, strict=True)

                        return children_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        children_item = SelectorInputMultiValueUiBlock.from_dict(data, strict=True)

                        return children_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        children_item = TextInputUiBlock.from_dict(data, strict=True)

                        return children_item
                    except:  # noqa: E722
                        pass
                    return UnknownType(data)

                children_item = _parse_children_item(children_item_data)

                children.append(children_item)

            return children

        try:
            children = get_children()
        except KeyError:
            if strict:
                raise
            children = cast(
                List[
                    Union[
                        ButtonUiBlock,
                        ChipUiBlock,
                        DropdownUiBlock,
                        DropdownMultiValueUiBlock,
                        FileUploadUiBlock,
                        MarkdownUiBlock,
                        SearchInputUiBlock,
                        SearchInputMultiValueUiBlock,
                        SelectorInputUiBlock,
                        SelectorInputMultiValueUiBlock,
                        TextInputUiBlock,
                        UnknownType,
                    ]
                ],
                UNSET,
            )

        def get_id() -> Union[Unset, str]:
            id = d.pop("id")
            return id

        try:
            id = get_id()
        except KeyError:
            if strict:
                raise
            id = cast(Union[Unset, str], UNSET)

        def get_type() -> Union[Unset, SectionUiBlockType]:
            type = UNSET
            _type = d.pop("type")
            if _type is not None and _type is not UNSET:
                try:
                    type = SectionUiBlockType(_type)
                except ValueError:
                    type = SectionUiBlockType.of_unknown(_type)

            return type

        try:
            type = get_type()
        except KeyError:
            if strict:
                raise
            type = cast(Union[Unset, SectionUiBlockType], UNSET)

        section_ui_block_create = cls(
            children=children,
            id=id,
            type=type,
        )

        section_ui_block_create.additional_properties = d
        return section_ui_block_create

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
    def children(
        self,
    ) -> List[
        Union[
            ButtonUiBlock,
            ChipUiBlock,
            DropdownUiBlock,
            DropdownMultiValueUiBlock,
            FileUploadUiBlock,
            MarkdownUiBlock,
            SearchInputUiBlock,
            SearchInputMultiValueUiBlock,
            SelectorInputUiBlock,
            SelectorInputMultiValueUiBlock,
            TextInputUiBlock,
            UnknownType,
        ]
    ]:
        if isinstance(self._children, Unset):
            raise NotPresentError(self, "children")
        return self._children

    @children.setter
    def children(
        self,
        value: List[
            Union[
                ButtonUiBlock,
                ChipUiBlock,
                DropdownUiBlock,
                DropdownMultiValueUiBlock,
                FileUploadUiBlock,
                MarkdownUiBlock,
                SearchInputUiBlock,
                SearchInputMultiValueUiBlock,
                SelectorInputUiBlock,
                SelectorInputMultiValueUiBlock,
                TextInputUiBlock,
                UnknownType,
            ]
        ],
    ) -> None:
        self._children = value

    @property
    def id(self) -> str:
        if isinstance(self._id, Unset):
            raise NotPresentError(self, "id")
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        self._id = value

    @id.deleter
    def id(self) -> None:
        self._id = UNSET

    @property
    def type(self) -> SectionUiBlockType:
        if isinstance(self._type, Unset):
            raise NotPresentError(self, "type")
        return self._type

    @type.setter
    def type(self, value: SectionUiBlockType) -> None:
        self._type = value

    @type.deleter
    def type(self) -> None:
        self._type = UNSET
