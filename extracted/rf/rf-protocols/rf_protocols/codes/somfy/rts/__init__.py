"""Somfy RTS button codes."""

from enum import IntEnum

from ....commands.somfy_rts import SomfyRTSCommand


class SomfyRTSButton(IntEnum):
    """Somfy RTS button identifiers.

    Values are the protocol command nibbles transmitted in the frame.
    """

    MY = 0x1
    UP = 0x2
    DOWN = 0x4
    PROG = 0x8

    def to_command(
        self,
        *,
        address: int,
        rolling_code: int,
        frame_repeats: int = 3,
    ) -> SomfyRTSCommand:
        """Build a SomfyRTSCommand for this button."""
        return SomfyRTSCommand(
            address=address,
            rolling_code=rolling_code,
            button=self.value,
            frame_repeats=frame_repeats,
        )
