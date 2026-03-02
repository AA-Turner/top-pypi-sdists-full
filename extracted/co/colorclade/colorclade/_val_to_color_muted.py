import colorsys
import random
import typing


def val_to_color_muted(
    val: typing.Any,
    salt: typing.Optional[int] = None,
    saturation: float = 1.0,
    brightness: float = 0.5,
) -> typing.Tuple[int, int, int]:
    """Converts a value to a color using a muted HSV mapping.

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
    hue = rand.random()

    # Convert the HSV color to an RGB color
    rgb_color = colorsys.hsv_to_rgb(hue, saturation, brightness)

    # Convert RGB values into 0-255 range (suitable for use in digital color)
    rgb_color_255 = tuple(int(c * 255) for c in rgb_color)

    return rgb_color_255
