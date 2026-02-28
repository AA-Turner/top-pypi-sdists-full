from PIL import Image

MAX_IMAGE_DIMENSION = 2000


def constrain_image_size(
    pil_image: Image.Image, max_dimension: int = MAX_IMAGE_DIMENSION
) -> Image.Image:
    """Resize image if any dimension exceeds max_dimension, preserving aspect ratio.

    Returns a new image if resizing is needed, or the original if already within limits.
    """
    width, height = pil_image.size
    if width <= max_dimension and height <= max_dimension:
        return pil_image

    resized = pil_image.copy()
    resized.thumbnail((max_dimension, max_dimension))
    return resized
