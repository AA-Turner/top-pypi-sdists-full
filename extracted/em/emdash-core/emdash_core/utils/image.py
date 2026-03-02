"""Image utilities for clipboard image handling and encoding.

Provides functions to:
- Read images from system clipboard
- Encode images to base64 data URLs
- Check clipboard image availability
- Get image dimensions

Uses pypng for pure-Python PNG handling (no compilation required).
"""

import base64
import io
import os
import platform
import subprocess
from enum import Enum
from typing import Optional


class ImageFormat(str, Enum):
    """Supported image formats."""
    PNG = "png"


# Maximum image size for LLM processing (5MB)
MAX_IMAGE_SIZE_BYTES = 5 * 1024 * 1024

# Tokens per image for context estimation
ESTIMATED_TOKENS_PER_IMAGE = 500


class ClipboardImageError(Exception):
    """Error reading image from clipboard."""
    pass


class ImageProcessingError(Exception):
    """Error processing image data."""
    pass


def _import_png():
    """Try to import pypng, return None if not available."""
    try:
        import png
        return png
    except ImportError:
        return None


def _import_windows_clipboard():
    """Try to import Windows clipboard modules."""
    try:
        import win32clipboard
        import win32con
        return win32clipboard, win32con
    except ImportError:
        return None, None


def _import_mac_clipboard():
    """Try to import macOS clipboard modules."""
    try:
        import AppKit
        return AppKit
    except ImportError:
        return None


def is_clipboard_image_available() -> bool:
    """Check if the clipboard contains image data.

    Returns:
        True if clipboard has image data, False otherwise.
    """
    system = platform.system()

    if system == "Windows":
        return _check_windows_clipboard()
    elif system == "Darwin":  # macOS
        return _check_macos_clipboard()
    elif system == "Linux":
        return _check_linux_clipboard()
    else:
        return False


def _check_windows_clipboard() -> bool:
    """Check Windows clipboard for image data."""
    win32clipboard, win32con = _import_windows_clipboard()
    if win32clipboard is None:
        return False

    try:
        win32clipboard.OpenClipboard(0)
        try:
            return win32clipboard.IsClipboardFormatAvailable(win32con.CF_DIB)
        finally:
            win32clipboard.CloseClipboard()
    except Exception:
        return False


def _check_macos_clipboard() -> bool:
    """Check macOS clipboard for image data."""
    AppKit = _import_mac_clipboard()
    if AppKit is None:
        return False

    try:
        pasteboard = AppKit.NSPasteboard.generalPasteboard()
        # Check for PNG or TIFF (macOS screenshots use TIFF)
        return bool(
            pasteboard.dataForType_("public.png") or
            pasteboard.dataForType_("public.tiff")
        )
    except Exception:
        return False


def _check_linux_clipboard() -> bool:
    """Check Linux clipboard for image data (via wl-paste or xclip)."""
    # Try wl-paste (Wayland)
    result = os.system("which wl-paste > /dev/null 2>&1") == 0
    if result:
        # Check if clipboard has image
        return os.system("wl-paste -t image/png > /dev/null 2>&1") == 0

    # Try xclip (X11)
    result = os.system("which xclip > /dev/null 2>&1") == 0
    if result:
        return os.system("xclip -selection clipboard -t image/png -o > /dev/null 2>&1") == 0

    return False


def read_clipboard_image() -> Optional[bytes]:
    """Read an image from the system clipboard.

    Returns:
        Raw image bytes (PNG format), or None if no image available.

    Raises:
        ClipboardImageError: If clipboard access fails unexpectedly.
    """
    system = platform.system()

    if system == "Windows":
        return _read_windows_clipboard()
    elif system == "Darwin":  # macOS
        return _read_macos_clipboard()
    elif system == "Linux":
        return _read_linux_clipboard()
    else:
        raise ClipboardImageError(
            f"Unsupported platform: {system}. "
            "Image paste is supported on Windows, macOS, and Linux (with wl-paste or xclip)."
        )


def _read_windows_clipboard() -> Optional[bytes]:
    """Read image from Windows clipboard."""
    win32clipboard, win32con = _import_windows_clipboard()
    if win32clipboard is None:
        raise ClipboardImageError(
            "pywin32 is required for clipboard access on Windows. "
            "Install with: pip install pywin32"
        )

    try:
        win32clipboard.OpenClipboard(0)
        try:
            # Try to get PNG format first
            png_format = win32clipboard.RegisterClipboardFormat("PNG")
            if win32clipboard.IsClipboardFormatAvailable(png_format):
                data = win32clipboard.GetClipboardData(png_format)
                return bytes(data)

            # Fall back to DIB and convert
            if win32clipboard.IsClipboardFormatAvailable(win32con.CF_DIB):
                data = win32clipboard.GetClipboardData(win32con.CF_DIB)
                return _dib_to_png(data)
            return None
        finally:
            win32clipboard.CloseClipboard()
    except Exception as e:
        raise ClipboardImageError(f"Failed to read Windows clipboard: {e}")


def _dib_to_png(dib_data: bytes) -> bytes:
    """Convert DIB (Device Independent Bitmap) data to PNG bytes.

    DIB format: BITMAPINFOHEADER followed by pixel data.
    """
    import struct

    png = _import_png()
    if png is None:
        raise ClipboardImageError("pypng is required for image processing")

    if len(dib_data) < 40:
        raise ClipboardImageError("Invalid DIB data")

    # Parse BITMAPINFOHEADER (40 bytes)
    header_size = struct.unpack('<I', dib_data[0:4])[0]
    width = struct.unpack('<i', dib_data[4:8])[0]
    height = struct.unpack('<i', dib_data[8:12])[0]
    planes = struct.unpack('<H', dib_data[12:14])[0]
    bit_count = struct.unpack('<H', dib_data[14:16])[0]
    compression = struct.unpack('<I', dib_data[16:20])[0]

    # Handle negative height (top-down DIB)
    top_down = height < 0
    height = abs(height)

    if compression != 0:  # BI_RGB = 0
        raise ClipboardImageError(f"Unsupported DIB compression: {compression}")

    if bit_count not in (24, 32):
        raise ClipboardImageError(f"Unsupported DIB bit depth: {bit_count}")

    # Calculate row stride (rows are padded to 4-byte boundaries)
    bytes_per_pixel = bit_count // 8
    row_size = ((width * bytes_per_pixel + 3) // 4) * 4

    # Pixel data starts after header (and color table for indexed images)
    pixel_offset = header_size

    # Extract rows
    rows = []
    for y in range(height):
        if top_down:
            row_start = pixel_offset + y * row_size
        else:
            # Bottom-up DIB: first row in file is bottom of image
            row_start = pixel_offset + (height - 1 - y) * row_size

        row_data = dib_data[row_start:row_start + width * bytes_per_pixel]

        # Convert BGR(A) to RGB(A)
        row = []
        for x in range(width):
            offset = x * bytes_per_pixel
            b = row_data[offset]
            g = row_data[offset + 1]
            r = row_data[offset + 2]
            row.extend([r, g, b])
        rows.append(row)

    # Write PNG
    output = io.BytesIO()
    writer = png.Writer(width=width, height=height, greyscale=False, alpha=False)
    writer.write(output, rows)
    return output.getvalue()


def _read_macos_clipboard() -> Optional[bytes]:
    """Read image from macOS clipboard."""
    import tempfile

    AppKit = _import_mac_clipboard()
    if AppKit is None:
        raise ClipboardImageError(
            "pyobjc is required for clipboard access on macOS. "
            "Install with: pip install pyobjc"
        )

    try:
        pasteboard = AppKit.NSPasteboard.generalPasteboard()

        # Try PNG first
        data = pasteboard.dataForType_("public.png")
        if data:
            return bytes(data)

        # Try TIFF and convert (macOS screenshots use TIFF internally)
        data = pasteboard.dataForType_("public.tiff")
        if data:
            # Use sips command-line tool to convert TIFF to PNG (via temp files)
            try:
                with tempfile.NamedTemporaryFile(suffix='.tiff', delete=False) as tiff_file:
                    tiff_path = tiff_file.name
                    tiff_file.write(bytes(data))

                png_path = tiff_path.replace('.tiff', '.png')
                try:
                    proc = subprocess.run(
                        ["sips", "-s", "format", "png", tiff_path, "--out", png_path],
                        capture_output=True,
                        timeout=5
                    )
                    if proc.returncode == 0:
                        with open(png_path, 'rb') as f:
                            return f.read()
                finally:
                    # Clean up temp files
                    try:
                        os.unlink(tiff_path)
                    except OSError:
                        pass
                    try:
                        os.unlink(png_path)
                    except OSError:
                        pass
            except (subprocess.TimeoutExpired, FileNotFoundError):
                pass

        return None
    except Exception as e:
        raise ClipboardImageError(f"Failed to read macOS clipboard: {e}")


def _read_linux_clipboard() -> Optional[bytes]:
    """Read image from Linux clipboard (wl-paste or xclip)."""
    # Try wl-paste first (Wayland)
    result = os.system("which wl-paste > /dev/null 2>&1") == 0
    if result:
        try:
            proc = subprocess.run(
                ["wl-paste", "-t", "image/png"],
                capture_output=True,
                timeout=5
            )
            if proc.returncode == 0 and proc.stdout:
                return proc.stdout
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass

    # Try xclip (X11)
    result = os.system("which xclip > /dev/null 2>&1") == 0
    if result:
        try:
            proc = subprocess.run(
                ["xclip", "-selection", "clipboard", "-t", "image/png", "-o"],
                capture_output=True,
                timeout=5
            )
            if proc.returncode == 0 and proc.stdout:
                return proc.stdout
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass

    raise ClipboardImageError(
        "No clipboard image tools found. Install wl-paste (Wayland) or xclip (X11):\n"
        "  Wayland: sudo apt install wl-clipboard  (Debian/Ubuntu)\n"
        "  X11:     sudo apt install xclip        (Debian/Ubuntu)"
    )


def encode_image_to_base64(image_data: bytes, format: ImageFormat = ImageFormat.PNG) -> str:
    """Encode image bytes to base64 data URL.

    Args:
        image_data: Raw image bytes.
        format: Image format (PNG only supported).

    Returns:
        Base64 data URL string: data:image/{format};base64,{encoded_data}
    """
    encoded = base64.b64encode(image_data).decode("utf-8")
    mime_type = f"image/{format.value}"
    return f"data:{mime_type};base64,{encoded}"


def encode_image_for_llm(image_data: bytes, format: ImageFormat = ImageFormat.PNG) -> dict:
    """Encode image for LLM vision API (OpenAI/Anthropic format).

    Args:
        image_data: Raw image bytes.
        format: Image format.

    Returns:
        Dict with base64 image data and media type for LLM APIs.
    """
    encoded = base64.b64encode(image_data).decode("utf-8")
    return {
        "type": "image_url",
        "image_url": {
            "url": f"data:image/{format.value};base64,{encoded}"
        }
    }


def get_image_info(image_data: bytes) -> dict:
    """Get information about a PNG image.

    Args:
        image_data: Raw PNG image bytes.

    Returns:
        Dict with image info: width, height, size, format.
    """
    png = _import_png()
    if png is None:
        return {
            "width": None,
            "height": None,
            "size_bytes": len(image_data),
            "format": "unknown",
            "error": "pypng not available"
        }

    try:
        reader = png.Reader(bytes=image_data)
        width, height, rows, metadata = reader.read()
        return {
            "width": width,
            "height": height,
            "size_bytes": len(image_data),
            "format": "PNG"
        }
    except Exception as e:
        return {
            "width": None,
            "height": None,
            "size_bytes": len(image_data),
            "format": "unknown",
            "error": str(e)
        }


def estimate_image_tokens(image_data: bytes) -> int:
    """Estimate token count for an image.

    This is a rough estimate based on image size and dimensions.
    Actual token count varies by model.

    Args:
        image_data: Raw image bytes.

    Returns:
        Estimated token count.
    """
    info = get_image_info(image_data)

    # Base token estimate
    tokens = ESTIMATED_TOKENS_PER_IMAGE

    # Adjust based on size (larger images have more detail)
    size_factor = len(image_data) / (1024 * 1024)  # MB
    tokens += int(tokens * size_factor * 0.5)

    # Adjust based on dimensions
    if info["width"] and info["height"]:
        dimension_factor = (info["width"] * info["height"]) / (1024 * 1024)  # megapixels
        tokens += int(tokens * dimension_factor * 0.3)

    return tokens


def read_and_prepare_image(
    max_size: int = MAX_IMAGE_SIZE_BYTES,
    raise_errors: bool = True
) -> Optional[bytes]:
    """Read image from clipboard and prepare for LLM.

    Combines checking, reading into one call.
    Note: Image resizing is not supported with pypng.
    Large images will be rejected if they exceed max_size.

    Args:
        max_size: Maximum image size in bytes.
        raise_errors: If True, raises errors on failure. If False, returns None.

    Returns:
        Image bytes, or None if no image available.
    """
    try:
        if not is_clipboard_image_available():
            return None

        image_data = read_clipboard_image()
        if image_data is None:
            return None

        # Check size limit (no resize capability with pypng)
        if len(image_data) > max_size:
            raise ImageProcessingError(
                f"Image too large ({len(image_data)} bytes, max {max_size}). "
                "Please use a smaller image."
            )

        return image_data

    except (ClipboardImageError, ImageProcessingError):
        if raise_errors:
            raise
        return None
