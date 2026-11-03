from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.call_ai_session_tool_json_body_context_cells_item import CallAiSessionToolJsonBodyContextCellsItem
    from ..models.call_ai_session_tool_json_body_context_live_editors_item import (
        CallAiSessionToolJsonBodyContextLiveEditorsItem,
    )


T = TypeVar("T", bound="CallAiSessionToolJsonBodyContext")


@_attrs_define
class CallAiSessionToolJsonBodyContext:
    """browser-held state the tool reads

    Attributes:
        live_editors (Union[Unset, List['CallAiSessionToolJsonBodyContextLiveEditorsItem']]):
        cells (Union[Unset, List['CallAiSessionToolJsonBodyContextCellsItem']]):
    """

    live_editors: Union[Unset, List["CallAiSessionToolJsonBodyContextLiveEditorsItem"]] = UNSET
    cells: Union[Unset, List["CallAiSessionToolJsonBodyContextCellsItem"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        live_editors: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.live_editors, Unset):
            live_editors = []
            for live_editors_item_data in self.live_editors:
                live_editors_item = live_editors_item_data.to_dict()

                live_editors.append(live_editors_item)

        cells: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.cells, Unset):
            cells = []
            for cells_item_data in self.cells:
                cells_item = cells_item_data.to_dict()

                cells.append(cells_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if live_editors is not UNSET:
            field_dict["live_editors"] = live_editors
        if cells is not UNSET:
            field_dict["cells"] = cells

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.call_ai_session_tool_json_body_context_cells_item import CallAiSessionToolJsonBodyContextCellsItem
        from ..models.call_ai_session_tool_json_body_context_live_editors_item import (
            CallAiSessionToolJsonBodyContextLiveEditorsItem,
        )

        d = src_dict.copy()
        live_editors = []
        _live_editors = d.pop("live_editors", UNSET)
        for live_editors_item_data in _live_editors or []:
            live_editors_item = CallAiSessionToolJsonBodyContextLiveEditorsItem.from_dict(live_editors_item_data)

            live_editors.append(live_editors_item)

        cells = []
        _cells = d.pop("cells", UNSET)
        for cells_item_data in _cells or []:
            cells_item = CallAiSessionToolJsonBodyContextCellsItem.from_dict(cells_item_data)

            cells.append(cells_item)

        call_ai_session_tool_json_body_context = cls(
            live_editors=live_editors,
            cells=cells,
        )

        call_ai_session_tool_json_body_context.additional_properties = d
        return call_ai_session_tool_json_body_context

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
