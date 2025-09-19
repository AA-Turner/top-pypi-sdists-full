
from typing import TypedDict, Literal, Optional, Union

from nhc.controller import NHCController


# Narrowed literal for known action types
ActionType = Literal[0, 1, 2, 3, 4]


class ActionDict(TypedDict, total=False):
    """TypedDict for action payloads returned by the Niko controller.

    All fields are optional because different action types include different
    keys (e.g. `value1` for lights, `v` for energy, `mode` for thermostat).
    """
    name: str
    channel: int
    id: int
    value1: Union[int, float]
    v: Union[int, float]
    mode: int
    type: ActionType
    location: int


class NHCBaseAction:
    """A Niko Base Action with improved type annotations."""
    _name: str
    _id: int
    _suggested_area: Optional[str] = None
    _state: Optional[Union[str, int]] = None
    _type: Optional[int] = None
    _controller: NHCController

    def __init__(self, controller: NHCController, action: ActionDict) -> None:
        """Init Niko Base Action.

        Args:
            controller: The parent `NHCController` instance (used for lookup).
            action: Raw action mapping from the controller.
        """
        self._name = action["name"]
        self._controller = controller

        # channel is used for some payloads, otherwise fall back to id
        if "channel" in action:
            self._id = action["channel"]
        else:
            self._id = action.get("id")

        # Determine state depending on action shape
        if "value1" in action:
            # Dimmable lights use a 0..100 scale in value1 when type==2
            if action.get("type") == 2:
                self._state = round(action["value1"] * 2.55)
            else:
                self._state = action["value1"]
        elif "v" in action:
            # Energy action
            self._state = action["v"]
        elif "mode" in action:
            # Thermostat
            self._state = action["mode"]

        if "type" in action:
            self._type = action["type"]

        if "location" in action:
            # controller.locations is expected to map location ids to names
            self._suggested_area = controller.locations[action["location"]]

    @property
    def state(self) -> Optional[Union[str, int]]:
        """Current action state (may be int, str or None)."""
        return self._state

    @property
    def type(self) -> Optional[int]:
        """The Niko Action type (0..4) or None if not set."""
        return self._type

    @property
    def suggested_area(self) -> Optional[str]:
        """Human-readable suggested area (if available)."""
        return self._suggested_area

    @property
    def name(self) -> str:
        """Action name."""
        return self._name

    @property
    def id(self) -> Optional[int]:
        """Action id/channel."""
        return self._id

    def update_state(self, state: Union[int, float]) -> None:
        """Update state value, applying dim scaling for type==2."""
        self._state = round(state * 2.55) if self._type == 2 else state


class NHCAction(NHCBaseAction):
    """Generic action helpers."""

    @property
    def is_scene(self) -> bool:
        return self.type == 0

    @property
    def is_light(self) -> bool:
        return self.type == 1

    @property
    def is_dimmable(self) -> bool:
        return self.type == 2

    @property
    def is_fan(self) -> bool:
        return self.type == 3

    @property
    def is_cover(self) -> bool:
        return self.type == 4


class NHCEnergyAction(NHCBaseAction):
    """Energy-specific helpers."""

    @property
    def is_import(self) -> bool:
        # import can be type 0 or 1
        return isinstance(self.type, int) and self.type in (0, 1)

    @property
    def is_export(self) -> bool:
        return self.type == 2

