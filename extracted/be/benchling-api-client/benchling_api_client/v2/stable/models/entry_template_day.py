from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError, UnknownType
from ..models.app_canvas_note_part import AppCanvasNotePart
from ..models.assay_run_note_part import AssayRunNotePart
from ..models.box_creation_table_note_part import BoxCreationTableNotePart
from ..models.chart_note_part import ChartNotePart
from ..models.checkbox_note_part import CheckboxNotePart
from ..models.external_file_note_part import ExternalFileNotePart
from ..models.inventory_container_table_note_part import InventoryContainerTableNotePart
from ..models.inventory_plate_table_note_part import InventoryPlateTableNotePart
from ..models.lookup_table_note_part import LookupTableNotePart
from ..models.mixture_prep_table_note_part import MixturePrepTableNotePart
from ..models.plate_creation_table_note_part import PlateCreationTableNotePart
from ..models.registration_table_note_part import RegistrationTableNotePart
from ..models.results_table_note_part import ResultsTableNotePart
from ..models.simple_note_part import SimpleNotePart
from ..models.table_note_part import TableNotePart
from ..models.text_box_note_part import TextBoxNotePart
from ..types import UNSET, Unset

T = TypeVar("T", bound="EntryTemplateDay")


@attr.s(auto_attribs=True, repr=False)
class EntryTemplateDay:
    """  """

    _day: Union[Unset, int] = UNSET
    _notes: Union[
        Unset,
        List[
            Union[
                SimpleNotePart,
                TableNotePart,
                TextBoxNotePart,
                CheckboxNotePart,
                ExternalFileNotePart,
                AssayRunNotePart,
                LookupTableNotePart,
                ResultsTableNotePart,
                RegistrationTableNotePart,
                PlateCreationTableNotePart,
                BoxCreationTableNotePart,
                MixturePrepTableNotePart,
                InventoryContainerTableNotePart,
                InventoryPlateTableNotePart,
                ChartNotePart,
                AppCanvasNotePart,
                UnknownType,
            ]
        ],
    ] = UNSET
    _title: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("day={}".format(repr(self._day)))
        fields.append("notes={}".format(repr(self._notes)))
        fields.append("title={}".format(repr(self._title)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "EntryTemplateDay({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        day = self._day
        notes: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._notes, Unset):
            notes = []
            for notes_item_data in self._notes:
                if isinstance(notes_item_data, UnknownType):
                    notes_item = notes_item_data.value
                elif isinstance(notes_item_data, SimpleNotePart):
                    notes_item = notes_item_data.to_dict()

                elif isinstance(notes_item_data, TableNotePart):
                    notes_item = notes_item_data.to_dict()

                elif isinstance(notes_item_data, TextBoxNotePart):
                    notes_item = notes_item_data.to_dict()

                elif isinstance(notes_item_data, CheckboxNotePart):
                    notes_item = notes_item_data.to_dict()

                elif isinstance(notes_item_data, ExternalFileNotePart):
                    notes_item = notes_item_data.to_dict()

                elif isinstance(notes_item_data, AssayRunNotePart):
                    notes_item = notes_item_data.to_dict()

                elif isinstance(notes_item_data, LookupTableNotePart):
                    notes_item = notes_item_data.to_dict()

                elif isinstance(notes_item_data, ResultsTableNotePart):
                    notes_item = notes_item_data.to_dict()

                elif isinstance(notes_item_data, RegistrationTableNotePart):
                    notes_item = notes_item_data.to_dict()

                elif isinstance(notes_item_data, PlateCreationTableNotePart):
                    notes_item = notes_item_data.to_dict()

                elif isinstance(notes_item_data, BoxCreationTableNotePart):
                    notes_item = notes_item_data.to_dict()

                elif isinstance(notes_item_data, MixturePrepTableNotePart):
                    notes_item = notes_item_data.to_dict()

                elif isinstance(notes_item_data, InventoryContainerTableNotePart):
                    notes_item = notes_item_data.to_dict()

                elif isinstance(notes_item_data, InventoryPlateTableNotePart):
                    notes_item = notes_item_data.to_dict()

                elif isinstance(notes_item_data, ChartNotePart):
                    notes_item = notes_item_data.to_dict()

                else:
                    notes_item = notes_item_data.to_dict()

                notes.append(notes_item)

        title = self._title

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if day is not UNSET:
            field_dict["day"] = day
        if notes is not UNSET:
            field_dict["notes"] = notes
        if title is not UNSET:
            field_dict["title"] = title

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_day() -> Union[Unset, int]:
            day = d.pop("day")
            return day

        try:
            day = get_day()
        except KeyError:
            if strict:
                raise
            day = cast(Union[Unset, int], UNSET)

        def get_notes() -> Union[
            Unset,
            List[
                Union[
                    SimpleNotePart,
                    TableNotePart,
                    TextBoxNotePart,
                    CheckboxNotePart,
                    ExternalFileNotePart,
                    AssayRunNotePart,
                    LookupTableNotePart,
                    ResultsTableNotePart,
                    RegistrationTableNotePart,
                    PlateCreationTableNotePart,
                    BoxCreationTableNotePart,
                    MixturePrepTableNotePart,
                    InventoryContainerTableNotePart,
                    InventoryPlateTableNotePart,
                    ChartNotePart,
                    AppCanvasNotePart,
                    UnknownType,
                ]
            ],
        ]:
            notes = []
            _notes = d.pop("notes")
            for notes_item_data in _notes or []:

                def _parse_notes_item(
                    data: Union[Dict[str, Any]]
                ) -> Union[
                    SimpleNotePart,
                    TableNotePart,
                    TextBoxNotePart,
                    CheckboxNotePart,
                    ExternalFileNotePart,
                    AssayRunNotePart,
                    LookupTableNotePart,
                    ResultsTableNotePart,
                    RegistrationTableNotePart,
                    PlateCreationTableNotePart,
                    BoxCreationTableNotePart,
                    MixturePrepTableNotePart,
                    InventoryContainerTableNotePart,
                    InventoryPlateTableNotePart,
                    ChartNotePart,
                    AppCanvasNotePart,
                    UnknownType,
                ]:
                    notes_item: Union[
                        SimpleNotePart,
                        TableNotePart,
                        TextBoxNotePart,
                        CheckboxNotePart,
                        ExternalFileNotePart,
                        AssayRunNotePart,
                        LookupTableNotePart,
                        ResultsTableNotePart,
                        RegistrationTableNotePart,
                        PlateCreationTableNotePart,
                        BoxCreationTableNotePart,
                        MixturePrepTableNotePart,
                        InventoryContainerTableNotePart,
                        InventoryPlateTableNotePart,
                        ChartNotePart,
                        AppCanvasNotePart,
                        UnknownType,
                    ]
                    discriminator_value: str = cast(str, data.get("type"))
                    if discriminator_value is not None:
                        entry_note_part: Union[
                            SimpleNotePart,
                            TableNotePart,
                            TextBoxNotePart,
                            CheckboxNotePart,
                            ExternalFileNotePart,
                            AssayRunNotePart,
                            LookupTableNotePart,
                            ResultsTableNotePart,
                            RegistrationTableNotePart,
                            PlateCreationTableNotePart,
                            BoxCreationTableNotePart,
                            MixturePrepTableNotePart,
                            InventoryContainerTableNotePart,
                            InventoryPlateTableNotePart,
                            ChartNotePart,
                            AppCanvasNotePart,
                            UnknownType,
                        ]
                        if discriminator_value == "app_canvas":
                            entry_note_part = AppCanvasNotePart.from_dict(data, strict=False)

                            return entry_note_part
                        if discriminator_value == "assay_run":
                            entry_note_part = AssayRunNotePart.from_dict(data, strict=False)

                            return entry_note_part
                        if discriminator_value == "box_creation_table":
                            entry_note_part = BoxCreationTableNotePart.from_dict(data, strict=False)

                            return entry_note_part
                        if discriminator_value == "code":
                            entry_note_part = SimpleNotePart.from_dict(data, strict=False)

                            return entry_note_part
                        if discriminator_value == "external_file":
                            entry_note_part = ExternalFileNotePart.from_dict(data, strict=False)

                            return entry_note_part
                        if discriminator_value == "inventory_container_table":
                            entry_note_part = InventoryContainerTableNotePart.from_dict(data, strict=False)

                            return entry_note_part
                        if discriminator_value == "inventory_plate_table":
                            entry_note_part = InventoryPlateTableNotePart.from_dict(data, strict=False)

                            return entry_note_part
                        if discriminator_value == "list_bullet":
                            entry_note_part = SimpleNotePart.from_dict(data, strict=False)

                            return entry_note_part
                        if discriminator_value == "list_checkbox":
                            entry_note_part = CheckboxNotePart.from_dict(data, strict=False)

                            return entry_note_part
                        if discriminator_value == "list_number":
                            entry_note_part = SimpleNotePart.from_dict(data, strict=False)

                            return entry_note_part
                        if discriminator_value == "lookup_table":
                            entry_note_part = LookupTableNotePart.from_dict(data, strict=False)

                            return entry_note_part
                        if discriminator_value == "mixture_prep_table":
                            entry_note_part = MixturePrepTableNotePart.from_dict(data, strict=False)

                            return entry_note_part
                        if discriminator_value == "note_linked_chart":
                            entry_note_part = ChartNotePart.from_dict(data, strict=False)

                            return entry_note_part
                        if discriminator_value == "plate_creation_table":
                            entry_note_part = PlateCreationTableNotePart.from_dict(data, strict=False)

                            return entry_note_part
                        if discriminator_value == "registration_table":
                            entry_note_part = RegistrationTableNotePart.from_dict(data, strict=False)

                            return entry_note_part
                        if discriminator_value == "results_table":
                            entry_note_part = ResultsTableNotePart.from_dict(data, strict=False)

                            return entry_note_part
                        if discriminator_value == "table":
                            entry_note_part = TableNotePart.from_dict(data, strict=False)

                            return entry_note_part
                        if discriminator_value == "text":
                            entry_note_part = SimpleNotePart.from_dict(data, strict=False)

                            return entry_note_part
                        if discriminator_value == "text_box":
                            entry_note_part = TextBoxNotePart.from_dict(data, strict=False)

                            return entry_note_part

                        return UnknownType(value=data)
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        entry_note_part = SimpleNotePart.from_dict(data, strict=True)

                        return entry_note_part
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        entry_note_part = TableNotePart.from_dict(data, strict=True)

                        return entry_note_part
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        entry_note_part = TextBoxNotePart.from_dict(data, strict=True)

                        return entry_note_part
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        entry_note_part = CheckboxNotePart.from_dict(data, strict=True)

                        return entry_note_part
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        entry_note_part = ExternalFileNotePart.from_dict(data, strict=True)

                        return entry_note_part
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        entry_note_part = AssayRunNotePart.from_dict(data, strict=True)

                        return entry_note_part
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        entry_note_part = LookupTableNotePart.from_dict(data, strict=True)

                        return entry_note_part
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        entry_note_part = ResultsTableNotePart.from_dict(data, strict=True)

                        return entry_note_part
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        entry_note_part = RegistrationTableNotePart.from_dict(data, strict=True)

                        return entry_note_part
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        entry_note_part = PlateCreationTableNotePart.from_dict(data, strict=True)

                        return entry_note_part
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        entry_note_part = BoxCreationTableNotePart.from_dict(data, strict=True)

                        return entry_note_part
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        entry_note_part = MixturePrepTableNotePart.from_dict(data, strict=True)

                        return entry_note_part
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        entry_note_part = InventoryContainerTableNotePart.from_dict(data, strict=True)

                        return entry_note_part
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        entry_note_part = InventoryPlateTableNotePart.from_dict(data, strict=True)

                        return entry_note_part
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        entry_note_part = ChartNotePart.from_dict(data, strict=True)

                        return entry_note_part
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        entry_note_part = AppCanvasNotePart.from_dict(data, strict=True)

                        return entry_note_part
                    except:  # noqa: E722
                        pass
                    return UnknownType(data)

                notes_item = _parse_notes_item(notes_item_data)

                notes.append(notes_item)

            return notes

        try:
            notes = get_notes()
        except KeyError:
            if strict:
                raise
            notes = cast(
                Union[
                    Unset,
                    List[
                        Union[
                            SimpleNotePart,
                            TableNotePart,
                            TextBoxNotePart,
                            CheckboxNotePart,
                            ExternalFileNotePart,
                            AssayRunNotePart,
                            LookupTableNotePart,
                            ResultsTableNotePart,
                            RegistrationTableNotePart,
                            PlateCreationTableNotePart,
                            BoxCreationTableNotePart,
                            MixturePrepTableNotePart,
                            InventoryContainerTableNotePart,
                            InventoryPlateTableNotePart,
                            ChartNotePart,
                            AppCanvasNotePart,
                            UnknownType,
                        ]
                    ],
                ],
                UNSET,
            )

        def get_title() -> Union[Unset, None, str]:
            title = d.pop("title")
            return title

        try:
            title = get_title()
        except KeyError:
            if strict:
                raise
            title = cast(Union[Unset, None, str], UNSET)

        entry_template_day = cls(
            day=day,
            notes=notes,
            title=title,
        )

        entry_template_day.additional_properties = d
        return entry_template_day

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
    def day(self) -> int:
        """ 1 indexed day signifier. If 0 is returned, that means the EntryTemplateDay is a section with a title but no specified Day. """
        if isinstance(self._day, Unset):
            raise NotPresentError(self, "day")
        return self._day

    @day.setter
    def day(self, value: int) -> None:
        self._day = value

    @day.deleter
    def day(self) -> None:
        self._day = UNSET

    @property
    def notes(
        self,
    ) -> List[
        Union[
            SimpleNotePart,
            TableNotePart,
            TextBoxNotePart,
            CheckboxNotePart,
            ExternalFileNotePart,
            AssayRunNotePart,
            LookupTableNotePart,
            ResultsTableNotePart,
            RegistrationTableNotePart,
            PlateCreationTableNotePart,
            BoxCreationTableNotePart,
            MixturePrepTableNotePart,
            InventoryContainerTableNotePart,
            InventoryPlateTableNotePart,
            ChartNotePart,
            AppCanvasNotePart,
            UnknownType,
        ]
    ]:
        if isinstance(self._notes, Unset):
            raise NotPresentError(self, "notes")
        return self._notes

    @notes.setter
    def notes(
        self,
        value: List[
            Union[
                SimpleNotePart,
                TableNotePart,
                TextBoxNotePart,
                CheckboxNotePart,
                ExternalFileNotePart,
                AssayRunNotePart,
                LookupTableNotePart,
                ResultsTableNotePart,
                RegistrationTableNotePart,
                PlateCreationTableNotePart,
                BoxCreationTableNotePart,
                MixturePrepTableNotePart,
                InventoryContainerTableNotePart,
                InventoryPlateTableNotePart,
                ChartNotePart,
                AppCanvasNotePart,
                UnknownType,
            ]
        ],
    ) -> None:
        self._notes = value

    @notes.deleter
    def notes(self) -> None:
        self._notes = UNSET

    @property
    def title(self) -> Optional[str]:
        """ Optional title of a section if sections are enabled. """
        if isinstance(self._title, Unset):
            raise NotPresentError(self, "title")
        return self._title

    @title.setter
    def title(self, value: Optional[str]) -> None:
        self._title = value

    @title.deleter
    def title(self) -> None:
        self._title = UNSET
