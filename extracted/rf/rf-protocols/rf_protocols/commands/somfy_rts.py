"""Somfy RTS RF command definitions."""

from __future__ import annotations

from typing import override

from . import ModulationType, RadioFrequencyCommand

# Somfy RTS operates at 433.42 MHz with OOK modulation.
_SOMFY_RTS_FREQUENCY = 433_420_000
_SOMFY_RTS_REPEAT_COUNT = 2


class SomfyRTSCommand(RadioFrequencyCommand):
    """Somfy RTS rolling code command.

    Encodes a complete Somfy RTS transmission, including wake-up pulse, the
    initial 2-sync frame, and ``frame_repeats`` additional 7-sync frames.

    All frame parameters are supplied at construction time. The rolling code
    counter must be tracked and incremented by the caller between
    transmissions.

    Protocol reference: https://pushstack.wordpress.com/somfy-rts-protocol/
    """

    address: int
    rolling_code: int
    button: int
    frame_repeats: int

    def __init__(
        self,
        *,
        address: int,
        rolling_code: int,
        button: int,
        frame_repeats: int = 3,
    ) -> None:
        """Initialize the Somfy RTS command."""
        super().__init__(
            frequency=_SOMFY_RTS_FREQUENCY,
            modulation=ModulationType.OOK,
            repeat_count=_SOMFY_RTS_REPEAT_COUNT,
        )
        self.address = address
        self.rolling_code = rolling_code
        self.button = button
        self.frame_repeats = frame_repeats

    @override
    def get_raw_timings(self) -> list[int]:
        """Compute Somfy RTS frame timings.

        Builds the 7-byte frame, applies checksum and obfuscation, then
        encodes the result as Manchester-coded OOK pulses. Consecutive
        same-polarity values produced by Manchester transitions are merged so
        the output strictly alternates between positive (mark) and negative
        (space) microseconds.
        """
        # ── Build 7-byte frame ────────────────────────────────────────────
        frame = bytearray(7)
        frame[0] = 0xA7  # encryption key (fixed)
        frame[1] = self.button << 4  # command nibble; lower = checksum
        frame[2] = (self.rolling_code >> 8) & 0xFF
        frame[3] = self.rolling_code & 0xFF
        frame[4] = (self.address >> 16) & 0xFF
        frame[5] = (self.address >> 8) & 0xFF
        frame[6] = self.address & 0xFF

        # Checksum: XOR of all nibbles across all 7 bytes
        cksum = 0
        for byte in frame:
            cksum ^= byte ^ (byte >> 4)
        frame[1] |= cksum & 0x0F

        # Obfuscation: rolling XOR
        for i in range(1, 7):
            frame[i] ^= frame[i - 1]

        # ── Build OOK pulse sequence ──────────────────────────────────────
        # Positive = mark (HIGH), negative = space (LOW), units = µs.
        # Consecutive same-polarity values are merged to maintain alternation.
        timings: list[int] = []

        def add(us: int) -> None:
            if timings and (us > 0) == (timings[-1] > 0):
                timings[-1] += us
            else:
                timings.append(us)

        def encode_frame(sync: int) -> None:
            if sync == 2:
                add(9415)
                add(-89565)  # wake-up pulse + silence
            for _ in range(sync):
                add(2416)
                add(-2416)  # hardware sync pulses
            add(4550)
            add(-604)  # software sync
            # 56 data bits, MSB first, Manchester encoded
            # Bit 1 = rising edge (LOW→HIGH), Bit 0 = falling edge (HIGH→LOW)
            for b in range(56):
                if (frame[b // 8] >> (7 - b % 8)) & 1:
                    add(-604)
                    add(604)
                else:
                    add(604)
                    add(-604)
            add(-30415)  # inter-frame gap

        encode_frame(2)
        for _ in range(self.frame_repeats):
            encode_frame(7)

        return timings
