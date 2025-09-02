MODES = ['low', 'medium', 'high', 'boost']
PRESET_MODES = {'boost': 3, 'high': 2, 'medium': 1, 'low': 0}

COVER_OPEN = 255
COVER_CLOSE = 254
COVER_STOP = 253

DEFAULT_PORT = 8000

THERMOSTAT_MODES = {
    0: "day",
    1: "night",
    2: "eco",
    3: "off",
    4: "cool",
    5: "prog1",
    6: "prog2",
    7: "prog3",
}

THERMOSTAT_MODES_REVERSE = {  
    value: key for key, value in THERMOSTAT_MODES.items()  
}

ENERGY_TYPES = {
    0: "import",
    1: "sub_usage", 
    2: "export",
}