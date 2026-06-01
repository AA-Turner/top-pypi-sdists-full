import logging
from datetime import datetime

from PIL.Image import Exif, Image
from pydantic.dataclasses import dataclass

from picsellia.utils import filter_payload

logger = logging.getLogger("picsellia")


@dataclass
class ImageMetadata:
    height: int
    width: int
    metadata: dict | None


def read_image_metadata(
    image: Image, metadatum: dict, fill_metadata: bool
) -> ImageMetadata:
    exif_data = image.getexif()
    width, height = _get_image_shape_with_exif_transpose(image, exif_data)

    image_metadata = {}
    if fill_metadata and exif_data:
        image_metadata = _get_image_metadata_from_exif_flags(exif_data)

    if metadatum:
        image_metadata = {**image_metadata, **metadatum}

    if not image_metadata:
        image_metadata = None
    else:
        image_metadata = filter_payload(image_metadata)

    return ImageMetadata(width=width, height=height, metadata=image_metadata)


def _get_image_shape_with_exif_transpose(image: Image, exif_data: Exif):
    """
        This method reads exif tags of an image and invert width and height if needed.
        Orientation flags that need inversion are : TRANSPOSE, ROTATE_90, TRANSVERSE and ROTATE_270
        5: Image.Transpose.TRANSPOSE
        6: Image.Transpose.ROTATE_270
        7: Image.Transpose.TRANSVERSE
        8: Image.Transpose.ROTATE_90
    Args:
        image: PIL Image to read

    Returns:
        width and height of image
    """
    if exif_data:
        # Orientation when height and width are inverted
        orientation = exif_data.get(0x0112)

        if orientation in [5, 6, 7, 8]:
            return image.height, image.width

    return image.width, image.height


def _get_image_metadata_from_exif_flags(exif_data: Exif):
    """
    Extracts specific metadata from the exif data of an image.

    This function reads the exif data and retrieves metadata including the time
    of acquisition, the device that captured the image, resolution details,
    compression used, software used for processing, and color space.

    Args:
        exif_data: The exif data extracted from an image

    Returns:
        A dictionary containing specific metadata extracted from the exif data.
    """
    acquired_at = exif_data.get(0x0132)
    acquired_by = exif_data.get(0x013B)
    resolution_x = exif_data.get(0x011A)
    resolution_y = exif_data.get(0x011B)
    resolution_unit = exif_data.get(0x0128)
    compression = exif_data.get(0x0103)
    manufacturer = exif_data.get(0x010F)
    software = exif_data.get(0x0131)
    color_space = exif_data.get(0xA001)

    return {
        "acquired_at": _parse_datetime(acquired_at),
        "acquired_by": str(acquired_by).strip("\x00") if acquired_by else None,
        "resolution_x": float(resolution_x) if resolution_x else None,
        "resolution_y": float(resolution_y) if resolution_y else None,
        "resolution_unit": _parse_resolution_unit(resolution_unit),
        "compression": _parse_compression(compression),
        "manufacturer": str(manufacturer).strip("\x00") if manufacturer else None,
        "software": str(software).strip("\x00") if software else None,
        "color_space": str(color_space) if color_space else None,
    }


def _parse_resolution_unit(resolution_unit: str | int | None) -> str | None:
    if isinstance(resolution_unit, str):
        return resolution_unit.strip("\x00")
    elif isinstance(resolution_unit, int):
        if resolution_unit == 2:
            return "inches"
        elif resolution_unit == 3:
            return "cm"

    return None


# check https://exiftool.org/TagNames/EXIF.html#Compression
def _parse_compression(compression: str | int | None) -> str | None:  # noqa: C901
    if isinstance(compression, str):
        return compression.strip("\x00")
    elif isinstance(compression, int):
        if compression == 1:
            return "Uncompressed"
        elif compression == 2:
            return "CCITT 1D"
        elif compression == 3:
            return "T4/Group 3 Fax"
        elif compression == 4:
            return "T6/Group 4 Fax"
        elif compression == 5:
            return "LZW"
        elif compression == 6:
            return "JPEG (old-style)"
        elif compression == 7:
            return "JPEG"
        elif compression == 8:
            return "Adobe Deflate"
        elif compression == 9:
            return "JBIG B&W"
        elif compression == 10:
            return "JBIG Color"
        elif compression == 99:
            return "JPEG"

    return None


def _parse_datetime(date: str):
    if not date:
        return None

    try:
        return datetime.strptime(date, "%Y:%m:%d %H:%M:%S")
    except ValueError:
        logger.warning(
            f"Could not parse date '{date}'. Expected format is %Y:%m:%d %H:%M:%S"
        )
        return None
