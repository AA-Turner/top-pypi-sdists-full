# Convert rgb colour values to hex
def convertRGBToHex(rgb: list):
    if len(rgb) > 3:
        raise IndexError(f"The list should have 3 value for the red, green, and blue channels! You have: {len(rgb)} values in your list.")
    elif rgb[0] > 255 or rgb[0] < 0 or rgb[1] > 255 or rgb[1] < 0 or rgb[2] > 255 or rgb[2] < 0:
        raise ValueError(f"The values should be between 0 and 255 inclusive! Your input is: {rgb}.")
    elif (type(rgb[0]) != int and type(rgb[0]) != float) or (type(rgb[1]) != int and type(rgb[1]) != float) or (type(rgb[2]) != int and type(rgb[2]) != float):
        raise TypeError("The values in the list are not of the correct type! It should either be an int or a float.")
    else:
        return int("{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2]), 16)
