"""
Event Decoder

Decodes G13 USB HID reports into button and joystick events.

CRITICAL: This module requires reverse engineering with physical G13 hardware.
The button mapping (BUTTON_MAP) is currently a stub and needs to be determined
through systematic testing by pressing each button and recording the raw USB data.
"""

from dataclasses import dataclass


@dataclass
class G13ButtonState:
    """Represents decoded button and joystick states from a USB HID report"""

    g_buttons: int  # Bitmask for G1-G22 (bit 1-22)
    m_buttons: int  # Bitmask for M1-M3 (bit 1-3)
    joystick_x: int  # Analog X position (0-255)
    joystick_y: int  # Analog Y position (0-255)
    raw_data: bytes  # Original raw report for debugging


class EventDecoder:
    """
    Decodes G13 USB HID reports (64 bytes) into structured button/joystick data.

    IMPLEMENTATION STATUS: STUB - Requires hardware testing

    To complete this implementation:
    1. Run: python -m g13_linux.cli
    2. Press each button (G1-G22, M1-M3) individually
    3. Record the RAW output showing which bytes change
    4. Update BUTTON_MAP with correct (byte_index, bit_position) for each button
    5. Update JOYSTICK_X_BYTE and JOYSTICK_Y_BYTE with correct positions

    Reference implementation: https://github.com/ecraven/g13
    """

    # Button bit positions - CONFIRMED via hardware testing (2024-12-31)
    # Format: 'button_id': (byte_index, bit_position)
    # Based on capture data showing 8-byte HID reports
    BUTTON_MAP = {
        # G-keys Row 1 (Byte 3, bits 0-7) - ALL CONFIRMED
        "G1": (3, 0),  # 0x01 ✓
        "G2": (3, 1),  # 0x02 ✓
        "G3": (3, 2),  # 0x04 ✓
        "G4": (3, 3),  # 0x08 ✓
        "G5": (3, 4),  # 0x10 ✓
        "G6": (3, 5),  # 0x20 ✓
        "G7": (3, 6),  # 0x40 ✓
        "G8": (3, 7),  # 0x80 ✓
        # G-keys Row 2 (Byte 4, bits 0-7) - ALL CONFIRMED
        "G9": (4, 0),  # 0x01 ✓
        "G10": (4, 1),  # 0x02 ✓
        "G11": (4, 2),  # 0x04 ✓
        "G12": (4, 3),  # 0x08 ✓
        "G13": (4, 4),  # 0x10 ✓
        "G14": (4, 5),  # 0x20 ✓
        "G15": (4, 6),  # 0x40 ✓
        "G16": (4, 7),  # 0x80 ✓
        # G-keys Row 3-4 (Byte 5, bits 0-5) - ALL CONFIRMED
        # NOTE: These are on Byte 5, NOT Byte 6 as previously predicted!
        # Byte 5 bit 7 (0x80) is always set - status flag, not a button
        "G17": (5, 0),  # 0x01 ✓
        "G18": (5, 1),  # 0x02 ✓
        "G19": (5, 2),  # 0x04 ✓
        "G20": (5, 3),  # 0x08 ✓
        "G21": (5, 4),  # 0x10 ✓
        "G22": (5, 5),  # 0x20 ✓
        # Byte 6: Mode and function buttons (from ecraven/g13 reference)
        "BD": (6, 0),  # 0x01 - Backlight/Display toggle
        "L1": (6, 1),  # 0x02 - Left button 1 (if present)
        "L2": (6, 2),  # 0x04 - Left button 2 (if present)
        "L3": (6, 3),  # 0x08 - Left button 3 (if present)
        "L4": (6, 4),  # 0x10 - Left button 4 (if present)
        "M1": (6, 5),  # 0x20 ✓ - Mode 1
        "M2": (6, 6),  # 0x40 ✓ - Mode 2
        "M3": (6, 7),  # 0x80 ✓ - Mode 3
        # Byte 7: MR and thumb/joystick buttons
        "MR": (7, 0),  # 0x01 ✓ - Macro Record
        "LEFT": (7, 1),  # 0x02 - Left thumb button (adjacent to joystick)
        "DOWN": (7, 2),  # 0x04 - Down thumb button (adjacent to joystick)
        "STICK": (7, 3),  # 0x08 - Joystick click (press down on stick)
    }

    # Joystick byte positions - CONFIRMED via hardware testing
    JOYSTICK_X_BYTE = 1  # Byte 1: X-axis (centered at ~120)
    JOYSTICK_Y_BYTE = 2  # Byte 2: Y-axis (centered at ~127)

    def __init__(self):
        self.last_state: G13ButtonState | None = None

    def decode_report(self, data: bytes | list) -> G13ButtonState:
        """
        Decode 8-byte HID report into structured data.

        Args:
            data: Raw 8-byte report from device (or padded to 64 bytes)

        Returns:
            Decoded button and joystick state

        Raises:
            ValueError: If data is less than 8 bytes
        """
        # Convert list to bytes if needed
        if isinstance(data, list):
            data = bytes(data)

        if len(data) < 8:
            raise ValueError(f"Expected at least 8 bytes, got {len(data)}")

        # Decode button states
        g_buttons = self._decode_g_buttons(data)
        m_buttons = self._decode_m_buttons(data)

        # Decode joystick (if bytes are within range)
        joystick_x = data[self.JOYSTICK_X_BYTE] if len(data) > self.JOYSTICK_X_BYTE else 128
        joystick_y = data[self.JOYSTICK_Y_BYTE] if len(data) > self.JOYSTICK_Y_BYTE else 128

        state = G13ButtonState(
            g_buttons=g_buttons,
            m_buttons=m_buttons,
            joystick_x=joystick_x,
            joystick_y=joystick_y,
            raw_data=data,
        )

        # NOTE: Don't update last_state here - let get_button_changes do it
        # so it can compare old vs new properly
        return state

    def _decode_g_buttons(self, data: bytes) -> int:
        """
        Extract G1-G22 button states as bitmask.

        Returns:
            Integer bitmask where bit N represents button G{N}
        """
        result = 0

        # STUB IMPLEMENTATION - needs hardware testing
        # Iterate through BUTTON_MAP to extract bits
        for button_name, (byte_idx, bit_pos) in self.BUTTON_MAP.items():
            if button_name.startswith("G") and len(button_name) > 1:
                try:
                    button_num = int(button_name[1:])
                    if 1 <= button_num <= 22:
                        # Check if bit is set in the specified byte
                        if data[byte_idx] & (1 << bit_pos):
                            result |= 1 << button_num
                except (ValueError, IndexError):
                    pass

        return result

    def _decode_m_buttons(self, data: bytes) -> int:
        """
        Extract M1-M3 button states as bitmask.

        Returns:
            Integer bitmask where bit N represents button M{N}
        """
        result = 0

        # STUB IMPLEMENTATION - needs hardware testing
        for button_name, (byte_idx, bit_pos) in self.BUTTON_MAP.items():
            if button_name.startswith("M") and len(button_name) > 1:
                try:
                    button_num = int(button_name[1:])
                    if 1 <= button_num <= 3:
                        if data[byte_idx] & (1 << bit_pos):
                            result |= 1 << button_num
                except (ValueError, IndexError):
                    pass

        return result

    # Buttons to check directly from raw data (not G1-G22 or M1-M3)
    OTHER_BUTTONS = ["BD", "L1", "L2", "L3", "L4", "MR", "LEFT", "DOWN", "STICK"]

    def _get_bitmask_buttons(self, bitmask: int, prefix: str, count: int) -> list[str]:
        """Extract pressed button names from a bitmask."""
        return [f"{prefix}{i}" for i in range(1, count + 1) if bitmask & (1 << i)]

    def _get_other_pressed(self, raw_data: bytes) -> list[str]:
        """Extract pressed 'other' buttons from raw data."""
        pressed = []
        for button_name in self.OTHER_BUTTONS:
            if button_name in self.BUTTON_MAP:
                byte_idx, bit_pos = self.BUTTON_MAP[button_name]
                if byte_idx < len(raw_data) and raw_data[byte_idx] & (1 << bit_pos):
                    pressed.append(button_name)
        return pressed

    def get_pressed_buttons(self, state: G13ButtonState | None = None) -> list[str]:
        """
        Return list of currently pressed button names.

        Args:
            state: Button state to check (uses last_state if None)

        Returns:
            List of button IDs (e.g., ['G1', 'M2', 'TOP'])
        """
        if state is None:
            state = self.last_state
        if state is None:
            return []

        pressed = self._get_bitmask_buttons(state.g_buttons, "G", 22)
        pressed.extend(self._get_bitmask_buttons(state.m_buttons, "M", 3))

        if state.raw_data and len(state.raw_data) >= 8:
            pressed.extend(self._get_other_pressed(state.raw_data))

        return pressed

    def get_button_changes(self, new_state: G13ButtonState) -> tuple[list[str], list[str]]:
        """
        Compare with previous state to detect button press/release events.

        Args:
            new_state: New button state

        Returns:
            Tuple of (pressed_buttons, released_buttons)
        """
        if self.last_state is None:
            # First state - consider all pressed buttons as new
            pressed = self.get_pressed_buttons(new_state)
            self.last_state = new_state
            return (pressed, [])

        old_pressed = set(self.get_pressed_buttons(self.last_state))
        new_pressed = set(self.get_pressed_buttons(new_state))

        pressed = list(new_pressed - old_pressed)
        released = list(old_pressed - new_pressed)

        # Update last_state for next comparison
        self.last_state = new_state

        return (pressed, released)

    def analyze_raw_report(self, data: bytes) -> str:
        """
        Analyze raw report for reverse engineering.

        Returns human-readable hex dump for debugging.

        Args:
            data: 8-byte (or longer) HID report

        Returns:
            Formatted hex string
        """
        if len(data) < 8:
            return f"Invalid length: {len(data)} bytes (expected at least 8)"

        lines = []
        lines.append(f"USB HID Report Analysis ({len(data)} bytes):")
        lines.append("=" * 60)

        # Show in groups of 16 bytes
        for i in range(0, len(data), 16):
            chunk = data[i : i + 16]
            hex_str = " ".join(f"{b:02x}" for b in chunk)
            ascii_str = "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)
            lines.append(f"{i:04x}:  {hex_str}  {ascii_str}")

        lines.append("=" * 60)

        # Show non-zero bytes
        non_zero = [(i, b) for i, b in enumerate(data) if b != 0]
        if non_zero:
            lines.append("Non-zero bytes:")
            for idx, val in non_zero:
                lines.append(f"  Byte {idx:2d}: 0x{val:02x} ({val:3d}) = {bin(val)}")
        else:
            lines.append("All bytes are zero")

        return "\n".join(lines)


# Helper function for testing/reverse engineering
def analyze_sample_data(sample_data: bytes):
    """
    Debug function for analyzing sample HID reports.

    Usage:
        from g13_linux.gui.models.event_decoder import analyze_sample_data

        # Record output when pressing G1
        g1_data = bytes([...])
        analyze_sample_data(g1_data)
    """
    decoder = EventDecoder()

    print("Raw Data Analysis:")
    print(decoder.analyze_raw_report(sample_data))
    print()

    state = decoder.decode_report(sample_data)
    print("Decoded State:")
    print(f"  G-buttons bitmask: {state.g_buttons:022b}")
    print(f"  M-buttons bitmask: {state.m_buttons:03b}")
    print(f"  Joystick X: {state.joystick_x}")
    print(f"  Joystick Y: {state.joystick_y}")
    print(f"  Pressed buttons: {decoder.get_pressed_buttons(state)}")
