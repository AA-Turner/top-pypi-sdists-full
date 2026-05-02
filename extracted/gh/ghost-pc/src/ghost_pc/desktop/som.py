"""Set-of-Mark (SoM) screenshot annotation.

Draws numbered labels on screenshots at each UIA control's bounding box,
so the Gemini model can reference controls by number instead of guessing
pixel coordinates. Also generates a text description of all controls.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ghost_pc.desktop.uia_inspector import ControlInfo


# Label styling
LABEL_FONT_SIZE = 12
LABEL_BG_COLOR = (255, 50, 50)  # Red background
LABEL_TEXT_COLOR = (255, 255, 255)  # White text
LABEL_PADDING = 2
BORDER_COLOR = (255, 50, 50, 128)  # Semi-transparent red
BORDER_WIDTH = 2


def annotate_screenshot(
    screenshot_bytes: bytes,
    controls: list[ControlInfo],
    screen_width: int | None = None,
    screen_height: int | None = None,
) -> tuple[bytes, str]:
    """Draw numbered labels on screenshot at each UIA control's position.

    Args:
        screenshot_bytes: Raw PNG image bytes.
        controls: List of ControlInfo from UIA inspection.
        screen_width: Image target width (for scaling if needed).
        screen_height: Image target height (for scaling if needed).

    Returns:
        Tuple of (annotated PNG bytes, text description string).
        The text description maps each number to its control info:
        "#0: Button 'Save' at (150,400)\\n#1: TextInput 'Filename' at (150,350)"
    """
    from io import BytesIO

    from PIL import Image, ImageDraw, ImageFont

    img = Image.open(BytesIO(screenshot_bytes))
    draw = ImageDraw.Draw(img, "RGBA")

    # Try to use a system font, fall back to default
    try:
        font = ImageFont.truetype("arial.ttf", LABEL_FONT_SIZE)
    except OSError:
        try:
            dejavu = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
            font = ImageFont.truetype(dejavu, LABEL_FONT_SIZE)
        except OSError:
            font = ImageFont.load_default()

    # Calculate scale factors if screenshot was resized from screen resolution
    scale_x = 1.0
    scale_y = 1.0
    if screen_width and screen_height:
        scale_x = img.width / screen_width
        scale_y = img.height / screen_height

    text_lines: list[str] = []

    for ctrl in controls:
        idx = ctrl["index"]
        name = ctrl["name"]
        ctype = ctrl["control_type"]
        left, top, right, bottom = ctrl["rect"]

        # Scale coordinates to image space
        s_left = int(left * scale_x)
        s_top = int(top * scale_y)
        s_right = int(right * scale_x)
        s_bottom = int(bottom * scale_y)

        # Clamp to image bounds
        s_left = max(0, min(s_left, img.width - 1))
        s_top = max(0, min(s_top, img.height - 1))
        s_right = max(0, min(s_right, img.width - 1))
        s_bottom = max(0, min(s_bottom, img.height - 1))

        if s_right <= s_left or s_bottom <= s_top:
            continue

        # Draw semi-transparent bounding box border
        draw.rectangle(
            [s_left, s_top, s_right, s_bottom],
            outline=BORDER_COLOR,
            width=BORDER_WIDTH,
        )

        # Draw numbered label at top-left corner of the control
        label = str(idx)
        bbox = font.getbbox(label)
        label_w = bbox[2] - bbox[0] + LABEL_PADDING * 2
        label_h = bbox[3] - bbox[1] + LABEL_PADDING * 2

        label_x = s_left
        label_y = max(0, s_top - label_h)

        # Label background
        draw.rectangle(
            [label_x, label_y, label_x + label_w, label_y + label_h],
            fill=LABEL_BG_COLOR,
        )
        # Label text
        draw.text(
            (label_x + LABEL_PADDING, label_y + LABEL_PADDING),
            label,
            fill=LABEL_TEXT_COLOR,
            font=font,
        )

        # Build text description
        center_x = (left + right) // 2
        center_y = (top + bottom) // 2
        desc = f"#{idx}: {ctype}"
        if name:
            desc += f" '{name}'"
        desc += f" at ({center_x},{center_y})"
        if ctrl.get("value"):
            desc += f" value='{ctrl['value'][:50]}'"
        if not ctrl["enabled"]:
            desc += " [disabled]"
        text_lines.append(desc)

    # Encode annotated image back to PNG
    buf = BytesIO()
    img.save(buf, format="PNG", optimize=False, compress_level=1)

    text_description = "\n".join(text_lines)
    return buf.getvalue(), text_description


def build_control_text(controls: list[ControlInfo]) -> str:
    """Build a text-only description of controls (no image annotation).

    Useful when you want to send just the text list to the model
    without modifying the screenshot.
    """
    lines: list[str] = []
    for ctrl in controls:
        idx = ctrl["index"]
        name = ctrl["name"]
        ctype = ctrl["control_type"]
        left, top, right, bottom = ctrl["rect"]
        center_x = (left + right) // 2
        center_y = (top + bottom) // 2

        desc = f"#{idx}: {ctype}"
        if name:
            desc += f" '{name}'"
        desc += f" at ({center_x},{center_y})"
        if ctrl.get("value"):
            desc += f" value='{ctrl['value'][:50]}'"
        if not ctrl["enabled"]:
            desc += " [disabled]"
        lines.append(desc)

    return "\n".join(lines)
