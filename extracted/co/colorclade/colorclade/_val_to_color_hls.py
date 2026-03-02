import random
import typing

import seaborn as sns


def val_to_color_hls(
    val: typing.Any,
    salt: typing.Optional[int] = None,
) -> typing.Tuple[int, int, int]:
    """Converts a value to a color in the HLS (Hue, Lightness, Saturation)
    color space, represented as an RGB tuple in the 0-255 range.

    Parameters
    ----------
    val : typing.Any
        The input value used to generate the color.

        This can be of any type that can be converted to a string.
    salt : typing.Optional[int], optional
        An optional integer used to salt the hash, providing a way to get
        different colors for the same input value.

    Returns
    -------
    typing.Tuple[int, int, int]
        A tuple representing the RGB color corresponding to the input value,
        with each component in the 0-255 range.
    """
    # Convert the hash to a value between 0 and 1
    rand = random.Random()
    rand.seed(str(val) + str(salt))
    rgb_color = rand.choice(sns.hls_palette(1024))

    # Convert RGB values into 0-255 range (suitable for use in digital color)
    rgb_color_255 = tuple(int(c * 255) for c in rgb_color)

    return rgb_color_255
