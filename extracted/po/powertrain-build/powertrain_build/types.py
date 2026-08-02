# Copyright 2024 Volvo Car Corporation
# Licensed under Apache 2.0.

"""Common functions and properties for types."""

TL_TYPES = dict(
    Float32=dict(
        size=4,
        a2l_type='FLOAT32_IEEE',
        a2l_range=('-1e38', '1e38')
    ),
    UInt32=dict(
        size=4,
        a2l_type='ULONG',
        a2l_range=(0, 4294967295)
    ),
    Int32=dict(
        size=4,
        a2l_type='SLONG',
        a2l_range=(-2147483648, 2147483647)
    ),
    UInt16=dict(
        size=2,
        a2l_type='UWORD',
        a2l_range=(0, 65535)
    ),
    Int16=dict(
        size=2,
        a2l_type='SWORD',
        a2l_range=(-32768, 32767)
    ),
    UInt8=dict(
        size=1,
        a2l_type='UBYTE',
        a2l_range=(0, 255)
    ),
    Int8=dict(
        size=1,
        a2l_type='SBYTE',
        a2l_range=(-128, 127)
    ),
    Bool=dict(
        size=1,
        a2l_type='UBYTE',
        a2l_range=(0, 1),
        bitmask='0x01'
    )
)

EC_TYPES = dict(
    real64_T=dict(
        size=8,
        a2l_type='FLOAT64_IEEE',
        a2l_ranger=('-1.8e308', '1.8e308')
    ),
    real_T=dict(
        size=8,
        a2l_type='FLOAT64_IEEE',
        a2l_ranger=('-1.8e308', '1.8e308')
    ),
    time_T=dict(
        size=8,
        a2l_type='FLOAT64_IEEE',
        a2l_ranger=('-1.8e308', '1.8e308')
    ),
    ulong_T=dict(
        size=4,
        a2l_type='ULONG',
        a2l_range=(0, 4294967295)
    ),
    real32_T=dict(
        size=4,
        a2l_type='FLOAT32_IEEE',
        a2l_range=('-1e38', '1e38')
    ),
    uint32_T=dict(
        size=4,
        a2l_type='ULONG',
        a2l_range=(0, 4294967295)
    ),
    uint_T=dict(
        size=4,
        a2l_type='ULONG',
        a2l_range=(0, 4294967295)
    ),
    int32_T=dict(
        size=4,
        a2l_type='SLONG',
        a2l_range=(-2147483648, 2147483647)
    ),
    int_T=dict(
        size=4,
        a2l_type='SLONG',
        a2l_range=(-2147483648, 2147483647)
    ),
    uint16_T=dict(
        size=2,
        a2l_type='UWORD',
        a2l_range=(0, 65535)
    ),
    int16_T=dict(
        size=2,
        a2l_type='SWORD',
        a2l_range=(-32768, 32767)
    ),
    uint8_T=dict(
        size=1,
        a2l_type='UBYTE',
        a2l_range=(0, 255)
    ),
    int8_T=dict(
        size=1,
        a2l_type='SBYTE',
        a2l_range=(-128, 127)
    ),
    boolean_T=dict(
        size=1,
        a2l_type='UBYTE',
        a2l_range=(0, 1),
        bitmask='0x01'
    ),
    uchar_T=dict(
        size=1,
        a2l_type='UBYTE',
        a2l_range=(0, 255)
    ),
    char_T=dict(
        size=1,
        a2l_type='SBYTE',
        a2l_range=(-128, 127)
    ),
    byte_T=dict(
        size=1,
        a2l_type='SBYTE',
        a2l_range=(-128, 127)
    )
)


def _validate_c_type(c_type):
    """Make sure given c-type is handled."""
    if c_type in TL_TYPES:
        return TL_TYPES[c_type]
    if c_type in EC_TYPES:
        return EC_TYPES[c_type]
    raise KeyError(f'Invalid data type: {c_type}')


def byte_size(c_type):
    """Get byte size of a c-type as an int."""
    type_dict = _validate_c_type(c_type)
    return type_dict['size']


def byte_size_string(c_type):
    """Get byte size of a c-type as a string."""
    return str(byte_size(c_type))


def a2l_type(c_type):
    """Get a2l-type of a c-type."""
    type_dict = _validate_c_type(c_type)
    return type_dict['a2l_type']


def a2l_range(c_type):
    """Get a2l-range of a c-type."""
    # TODO: Find out why we default to float32 in a2l.py
    # Probably due to vc_dummy.
    if c_type == 'float32' or c_type is None:
        # TODO Assuming TL for now
        return TL_TYPES['Float32']['a2l_range']
    type_dict = _validate_c_type(c_type)
    return type_dict['a2l_range']


def get_bitmask(c_type):
    """Get bit mask of a c-type.

    Defaults to None for types other than Bool.
    """
    type_dict = _validate_c_type(c_type)
    return type_dict.get('bitmask')


def get_ec_type(tl_type):
    """Get equivalent EC type for a given TL type.

    Args:
        tl_type (str): TL type

    Returns:
        str: EC type
    """
    tl_ec = dict(
        Float32='real32_T',
        UInt32='uint32_T',
        Int32='int32_T',
        UInt16='uint16_T',
        Int16='int16_T',
        UInt8='uint8_T',
        Int8='int8_T',
        Bool='boolean_T'
    )
    return tl_ec[tl_type]


def get_float32_types():
    """Get all EC types that are equivalent to Float32.

    Returns:
        set: EC types
    """
    float32_types = {'Float32'}
    for ec_type, ec_type_def in EC_TYPES.items():
        if ec_type_def == TL_TYPES['Float32']:
            float32_types.add(ec_type)
    return float32_types
