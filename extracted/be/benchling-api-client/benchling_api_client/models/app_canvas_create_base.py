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

T = TypeVar("T", bound="AppCanvasCreateBase")


@attr.s(auto_attribs=True, repr=False)
class AppCanvasCreateBase:
    """  """

    _data: Union[Unset, None, str] = UNSET
    _enabled: Union[Unset, bool] = UNSET
    _feature_id: Union[Unset, str] = UNSET
    _resource_id: Union[Unset, str] = UNSET
    _session_id: Union[Unset, None, str] = UNSET
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
        fields.append("data={}".format(repr(self._data)))
        fields.append("enabled={}".format(repr(self._enabled)))
        fields.append("feature_id={}".format(repr(self._feature_id)))
        fields.append("resource_id={}".format(repr(self._resource_id)))
        fields.append("session_id={}".format(repr(self._session_id)))
        fields.append("blocks={}".format(repr(self._blocks)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "AppCanvasCreateBase({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        data = self._data
        enabled = self._enabled
        feature_id = self._feature_id
        resource_id = self._resource_id
        session_id = self._session_id
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
        if data is not UNSET:
            field_dict["data"] = data
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if feature_id is not UNSET:
            field_dict["featureId"] = feature_id
        if resource_id is not UNSET:
            field_dict["resourceId"] = resource_id
        if session_id is not UNSET:
            field_dict["sessionId"] = session_id
        if blocks is not UNSET:
            field_dict["blocks"] = blocks

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_data() -> Union[Unset, None, str]:
            data = d.pop("data")
            return data

        try:
            data = get_data()
        except KeyError:
            if strict:
                raise
            data = cast(Union[Unset, None, str], UNSET)

        def get_enabled() -> Union[Unset, bool]:
            enabled = d.pop("enabled")
            return enabled

        try:
            enabled = get_enabled()
        except KeyError:
            if strict:
                raise
            enabled = cast(Union[Unset, bool], UNSET)

        def get_feature_id() -> Union[Unset, str]:
            feature_id = d.pop("featureId")
            return feature_id

        try:
            feature_id = get_feature_id()
        except KeyError:
            if strict:
                raise
            feature_id = cast(Union[Unset, str], UNSET)

        def get_resource_id() -> Union[Unset, str]:
            resource_id = d.pop("resourceId")
            return resource_id

        try:
            resource_id = get_resource_id()
        except KeyError:
            if strict:
                raise
            resource_id = cast(Union[Unset, str], UNSET)

        def get_session_id() -> Union[Unset, None, str]:
            session_id = d.pop("sessionId")
            return session_id

        try:
            session_id = get_session_id()
        except KeyError:
            if strict:
                raise
            session_id = cast(Union[Unset, None, str], UNSET)

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

        app_canvas_create_base = cls(
            data=data,
            enabled=enabled,
            feature_id=feature_id,
            resource_id=resource_id,
            session_id=session_id,
            blocks=blocks,
        )

        app_canvas_create_base.additional_properties = d
        return app_canvas_create_base

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
    def data(self) -> Optional[str]:
        """Additional data to associate with the canvas. Can be useful for persisting data associated with the canvas but won't be rendered to the user. If specified, it must be valid JSON in string format less than 5kb in total."""
        if isinstance(self._data, Unset):
            raise NotPresentError(self, "data")
        return self._data

    @data.setter
    def data(self, value: Optional[str]) -> None:
        self._data = value

    @data.deleter
    def data(self) -> None:
        self._data = UNSET

    @property
    def enabled(self) -> bool:
        """Overall control for whether the canvas is interactable or not. If `false`, every block is disabled and will override the individual block's `enabled` property. If `true` or absent, the interactivity status will defer to the block's `enabled` property."""
        if isinstance(self._enabled, Unset):
            raise NotPresentError(self, "enabled")
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool) -> None:
        self._enabled = value

    @enabled.deleter
    def enabled(self) -> None:
        self._enabled = UNSET

    @property
    def feature_id(self) -> str:
        """ Identifier of the feature defined in Benchling App Manifest this canvas corresponds to. """
        if isinstance(self._feature_id, Unset):
            raise NotPresentError(self, "feature_id")
        return self._feature_id

    @feature_id.setter
    def feature_id(self, value: str) -> None:
        self._feature_id = value

    @feature_id.deleter
    def feature_id(self) -> None:
        self._feature_id = UNSET

    @property
    def resource_id(self) -> str:
        """ Identifier of the resource object to attach canvas to. """
        if isinstance(self._resource_id, Unset):
            raise NotPresentError(self, "resource_id")
        return self._resource_id

    @resource_id.setter
    def resource_id(self, value: str) -> None:
        self._resource_id = value

    @resource_id.deleter
    def resource_id(self) -> None:
        self._resource_id = UNSET

    @property
    def session_id(self) -> Optional[str]:
        """Identifier of a session. If specified, app status messages from the session will be reported in the canvas."""
        if isinstance(self._session_id, Unset):
            raise NotPresentError(self, "session_id")
        return self._session_id

    @session_id.setter
    def session_id(self, value: Optional[str]) -> None:
        self._session_id = value

    @session_id.deleter
    def session_id(self) -> None:
        self._session_id = UNSET

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
