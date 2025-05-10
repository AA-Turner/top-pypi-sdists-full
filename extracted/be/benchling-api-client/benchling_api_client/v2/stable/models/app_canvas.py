from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError, UnknownType
from ..models.app_canvas_app import AppCanvasApp
from ..models.app_canvas_base_archive_record import AppCanvasBaseArchiveRecord
from ..models.button_ui_block import ButtonUiBlock
from ..models.chip_ui_block import ChipUiBlock
from ..models.dropdown_multi_value_ui_block import DropdownMultiValueUiBlock
from ..models.dropdown_ui_block import DropdownUiBlock
from ..models.file_upload_ui_block import FileUploadUiBlock
from ..models.markdown_ui_block import MarkdownUiBlock
from ..models.search_input_multi_value_ui_block import SearchInputMultiValueUiBlock
from ..models.search_input_ui_block import SearchInputUiBlock
from ..models.section_ui_block import SectionUiBlock
from ..models.selector_input_multi_value_ui_block import SelectorInputMultiValueUiBlock
from ..models.selector_input_ui_block import SelectorInputUiBlock
from ..models.table_ui_block import TableUiBlock
from ..models.text_input_ui_block import TextInputUiBlock
from ..types import UNSET, Unset

T = TypeVar("T", bound="AppCanvas")


@attr.s(auto_attribs=True, repr=False)
class AppCanvas:
    """  """

    _app: Union[Unset, AppCanvasApp] = UNSET
    _id: Union[Unset, str] = UNSET
    _archive_record: Union[Unset, None, AppCanvasBaseArchiveRecord] = UNSET
    _data: Union[Unset, None, str] = UNSET
    _enabled: Union[Unset, bool] = UNSET
    _feature_id: Union[Unset, str] = UNSET
    _resource_id: Union[Unset, str] = UNSET
    _session_id: Union[Unset, None, str] = UNSET
    _blocks: Union[
        Unset,
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
                SectionUiBlock,
                SelectorInputUiBlock,
                SelectorInputMultiValueUiBlock,
                TextInputUiBlock,
                TableUiBlock,
                UnknownType,
            ]
        ],
    ] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("app={}".format(repr(self._app)))
        fields.append("id={}".format(repr(self._id)))
        fields.append("archive_record={}".format(repr(self._archive_record)))
        fields.append("data={}".format(repr(self._data)))
        fields.append("enabled={}".format(repr(self._enabled)))
        fields.append("feature_id={}".format(repr(self._feature_id)))
        fields.append("resource_id={}".format(repr(self._resource_id)))
        fields.append("session_id={}".format(repr(self._session_id)))
        fields.append("blocks={}".format(repr(self._blocks)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "AppCanvas({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        app: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._app, Unset):
            app = self._app.to_dict()

        id = self._id
        archive_record: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self._archive_record, Unset):
            archive_record = self._archive_record.to_dict() if self._archive_record else None

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
                elif isinstance(blocks_item_data, ButtonUiBlock):
                    blocks_item = blocks_item_data.to_dict()

                elif isinstance(blocks_item_data, ChipUiBlock):
                    blocks_item = blocks_item_data.to_dict()

                elif isinstance(blocks_item_data, DropdownUiBlock):
                    blocks_item = blocks_item_data.to_dict()

                elif isinstance(blocks_item_data, DropdownMultiValueUiBlock):
                    blocks_item = blocks_item_data.to_dict()

                elif isinstance(blocks_item_data, FileUploadUiBlock):
                    blocks_item = blocks_item_data.to_dict()

                elif isinstance(blocks_item_data, MarkdownUiBlock):
                    blocks_item = blocks_item_data.to_dict()

                elif isinstance(blocks_item_data, SearchInputUiBlock):
                    blocks_item = blocks_item_data.to_dict()

                elif isinstance(blocks_item_data, SearchInputMultiValueUiBlock):
                    blocks_item = blocks_item_data.to_dict()

                elif isinstance(blocks_item_data, SectionUiBlock):
                    blocks_item = blocks_item_data.to_dict()

                elif isinstance(blocks_item_data, SelectorInputUiBlock):
                    blocks_item = blocks_item_data.to_dict()

                elif isinstance(blocks_item_data, SelectorInputMultiValueUiBlock):
                    blocks_item = blocks_item_data.to_dict()

                elif isinstance(blocks_item_data, TextInputUiBlock):
                    blocks_item = blocks_item_data.to_dict()

                else:
                    blocks_item = blocks_item_data.to_dict()

                blocks.append(blocks_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if app is not UNSET:
            field_dict["app"] = app
        if id is not UNSET:
            field_dict["id"] = id
        if archive_record is not UNSET:
            field_dict["archiveRecord"] = archive_record
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

        def get_app() -> Union[Unset, AppCanvasApp]:
            app: Union[Unset, Union[Unset, AppCanvasApp]] = UNSET
            _app = d.pop("app")

            if not isinstance(_app, Unset):
                app = AppCanvasApp.from_dict(_app)

            return app

        try:
            app = get_app()
        except KeyError:
            if strict:
                raise
            app = cast(Union[Unset, AppCanvasApp], UNSET)

        def get_id() -> Union[Unset, str]:
            id = d.pop("id")
            return id

        try:
            id = get_id()
        except KeyError:
            if strict:
                raise
            id = cast(Union[Unset, str], UNSET)

        def get_archive_record() -> Union[Unset, None, AppCanvasBaseArchiveRecord]:
            archive_record = None
            _archive_record = d.pop("archiveRecord")

            if _archive_record is not None and not isinstance(_archive_record, Unset):
                archive_record = AppCanvasBaseArchiveRecord.from_dict(_archive_record)

            return archive_record

        try:
            archive_record = get_archive_record()
        except KeyError:
            if strict:
                raise
            archive_record = cast(Union[Unset, None, AppCanvasBaseArchiveRecord], UNSET)

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
                    ButtonUiBlock,
                    ChipUiBlock,
                    DropdownUiBlock,
                    DropdownMultiValueUiBlock,
                    FileUploadUiBlock,
                    MarkdownUiBlock,
                    SearchInputUiBlock,
                    SearchInputMultiValueUiBlock,
                    SectionUiBlock,
                    SelectorInputUiBlock,
                    SelectorInputMultiValueUiBlock,
                    TextInputUiBlock,
                    TableUiBlock,
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
                    ButtonUiBlock,
                    ChipUiBlock,
                    DropdownUiBlock,
                    DropdownMultiValueUiBlock,
                    FileUploadUiBlock,
                    MarkdownUiBlock,
                    SearchInputUiBlock,
                    SearchInputMultiValueUiBlock,
                    SectionUiBlock,
                    SelectorInputUiBlock,
                    SelectorInputMultiValueUiBlock,
                    TextInputUiBlock,
                    TableUiBlock,
                    UnknownType,
                ]:
                    blocks_item: Union[
                        ButtonUiBlock,
                        ChipUiBlock,
                        DropdownUiBlock,
                        DropdownMultiValueUiBlock,
                        FileUploadUiBlock,
                        MarkdownUiBlock,
                        SearchInputUiBlock,
                        SearchInputMultiValueUiBlock,
                        SectionUiBlock,
                        SelectorInputUiBlock,
                        SelectorInputMultiValueUiBlock,
                        TextInputUiBlock,
                        TableUiBlock,
                        UnknownType,
                    ]
                    discriminator_value: str = cast(str, data.get("type"))
                    if discriminator_value is not None:
                        if discriminator_value == "BUTTON":
                            blocks_item = ButtonUiBlock.from_dict(data, strict=False)

                            return blocks_item
                        if discriminator_value == "CHIP":
                            blocks_item = ChipUiBlock.from_dict(data, strict=False)

                            return blocks_item
                        if discriminator_value == "DROPDOWN":
                            blocks_item = DropdownUiBlock.from_dict(data, strict=False)

                            return blocks_item
                        if discriminator_value == "DROPDOWN_MULTIVALUE":
                            blocks_item = DropdownMultiValueUiBlock.from_dict(data, strict=False)

                            return blocks_item
                        if discriminator_value == "FILE_UPLOAD":
                            blocks_item = FileUploadUiBlock.from_dict(data, strict=False)

                            return blocks_item
                        if discriminator_value == "MARKDOWN":
                            blocks_item = MarkdownUiBlock.from_dict(data, strict=False)

                            return blocks_item
                        if discriminator_value == "SEARCH_INPUT":
                            blocks_item = SearchInputUiBlock.from_dict(data, strict=False)

                            return blocks_item
                        if discriminator_value == "SEARCH_INPUT_MULTIVALUE":
                            blocks_item = SearchInputMultiValueUiBlock.from_dict(data, strict=False)

                            return blocks_item
                        if discriminator_value == "SECTION":
                            blocks_item = SectionUiBlock.from_dict(data, strict=False)

                            return blocks_item
                        if discriminator_value == "SELECTOR_INPUT":
                            blocks_item = SelectorInputUiBlock.from_dict(data, strict=False)

                            return blocks_item
                        if discriminator_value == "SELECTOR_INPUT_MULTIVALUE":
                            blocks_item = SelectorInputMultiValueUiBlock.from_dict(data, strict=False)

                            return blocks_item
                        if discriminator_value == "TABLE":
                            blocks_item = TableUiBlock.from_dict(data, strict=False)

                            return blocks_item
                        if discriminator_value == "TEXT_INPUT":
                            blocks_item = TextInputUiBlock.from_dict(data, strict=False)

                            return blocks_item

                        return UnknownType(value=data)
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        blocks_item = ButtonUiBlock.from_dict(data, strict=True)

                        return blocks_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        blocks_item = ChipUiBlock.from_dict(data, strict=True)

                        return blocks_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        blocks_item = DropdownUiBlock.from_dict(data, strict=True)

                        return blocks_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        blocks_item = DropdownMultiValueUiBlock.from_dict(data, strict=True)

                        return blocks_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        blocks_item = FileUploadUiBlock.from_dict(data, strict=True)

                        return blocks_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        blocks_item = MarkdownUiBlock.from_dict(data, strict=True)

                        return blocks_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        blocks_item = SearchInputUiBlock.from_dict(data, strict=True)

                        return blocks_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        blocks_item = SearchInputMultiValueUiBlock.from_dict(data, strict=True)

                        return blocks_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        blocks_item = SectionUiBlock.from_dict(data, strict=True)

                        return blocks_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        blocks_item = SelectorInputUiBlock.from_dict(data, strict=True)

                        return blocks_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        blocks_item = SelectorInputMultiValueUiBlock.from_dict(data, strict=True)

                        return blocks_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        blocks_item = TextInputUiBlock.from_dict(data, strict=True)

                        return blocks_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        blocks_item = TableUiBlock.from_dict(data, strict=True)

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
                            ButtonUiBlock,
                            ChipUiBlock,
                            DropdownUiBlock,
                            DropdownMultiValueUiBlock,
                            FileUploadUiBlock,
                            MarkdownUiBlock,
                            SearchInputUiBlock,
                            SearchInputMultiValueUiBlock,
                            SectionUiBlock,
                            SelectorInputUiBlock,
                            SelectorInputMultiValueUiBlock,
                            TextInputUiBlock,
                            TableUiBlock,
                            UnknownType,
                        ]
                    ],
                ],
                UNSET,
            )

        app_canvas = cls(
            app=app,
            id=id,
            archive_record=archive_record,
            data=data,
            enabled=enabled,
            feature_id=feature_id,
            resource_id=resource_id,
            session_id=session_id,
            blocks=blocks,
        )

        app_canvas.additional_properties = d
        return app_canvas

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
    def app(self) -> AppCanvasApp:
        if isinstance(self._app, Unset):
            raise NotPresentError(self, "app")
        return self._app

    @app.setter
    def app(self, value: AppCanvasApp) -> None:
        self._app = value

    @app.deleter
    def app(self) -> None:
        self._app = UNSET

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
    def archive_record(self) -> Optional[AppCanvasBaseArchiveRecord]:
        if isinstance(self._archive_record, Unset):
            raise NotPresentError(self, "archive_record")
        return self._archive_record

    @archive_record.setter
    def archive_record(self, value: Optional[AppCanvasBaseArchiveRecord]) -> None:
        self._archive_record = value

    @archive_record.deleter
    def archive_record(self) -> None:
        self._archive_record = UNSET

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
            ButtonUiBlock,
            ChipUiBlock,
            DropdownUiBlock,
            DropdownMultiValueUiBlock,
            FileUploadUiBlock,
            MarkdownUiBlock,
            SearchInputUiBlock,
            SearchInputMultiValueUiBlock,
            SectionUiBlock,
            SelectorInputUiBlock,
            SelectorInputMultiValueUiBlock,
            TextInputUiBlock,
            TableUiBlock,
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
                ButtonUiBlock,
                ChipUiBlock,
                DropdownUiBlock,
                DropdownMultiValueUiBlock,
                FileUploadUiBlock,
                MarkdownUiBlock,
                SearchInputUiBlock,
                SearchInputMultiValueUiBlock,
                SectionUiBlock,
                SelectorInputUiBlock,
                SelectorInputMultiValueUiBlock,
                TextInputUiBlock,
                TableUiBlock,
                UnknownType,
            ]
        ],
    ) -> None:
        self._blocks = value

    @blocks.deleter
    def blocks(self) -> None:
        self._blocks = UNSET
