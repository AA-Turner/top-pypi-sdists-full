from abc import abstractmethod

from rich import style
from rich.console import Console


class BeamlineShowInfo:
    DEFAULT_STYLE = style.Style(color="green")
    ALARM_STYLE = style.Style(color="red", bold=True)

    @staticmethod
    def _get_info_val(info, entry):
        return str(info[entry]["value"])

    def _get_console(self) -> Console:
        return Console()

    @abstractmethod
    def show(self):
        """Display the info"""


class BeamlineMixin:
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._bl_calls = []

    def bl_show_all(self):
        """Display general information about the SLS and the current status of the beamline"""
        for call in self._bl_calls:
            call.show()

    def _bl_info_register(self, bl_info: type[BeamlineShowInfo]) -> None:
        """Register a beamline info class

        Args:
            bl_info (Type[BeamlineShowInfo]): Class whose instance ought to be registered.
        """
        bli = bl_info()
        self._bl_calls.append(bli)
