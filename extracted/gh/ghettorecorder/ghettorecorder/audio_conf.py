"""Module reads and returns values from index tables.
Tables http://www.mp3-tech.org/programmer/frame_header.html

"""
bitrate_dict = {
    'bits': ['V1;L1', 'V1;L2', 'V1;L3', 'V2;L1', 'V2;L2;L3'],  # mpeg version; Layer
    0: ['free', 'free', 'free', 'free', 'free'],  # test int(), custom rate allowed, we ignore this
    1: [32, 32, 32, 32, 8],
    2: [64, 48, 40, 48, 16],
    3: [96, 56, 48, 56, 24],
    4: [128, 64, 56, 64, 32],
    5: [160, 80, 64, 80, 40],
    6: [192, 96, 80, 96, 48],
    7: [224, 112, 96, 112, 56],
    8: [256, 128, 112, 128, 64],
    9: [288, 160, 128, 144, 80],
    10: [320, 192, 160, 160, 96],
    11: [352, 224, 192, 176, 112],
    12: [384, 256, 224, 192, 128],
    13: [416, 320, 256, 224, 144],
    14: [448, 384, 320, 256, 160],
    15: ['bad', 'bad', 'bad', 'bad', 'bad'],  # not allowed
}

sampling_dict = {
    'bits': ['MPEG1', 'MPEG2', 'MPEG2.5'],
    0: [44100, 22050, 11025],
    1: [48000, 24000, 12000],
    2: [32000, 16000, 8000],
    3: ['reserv.', 'reserv.', 'reserv.'],
}


def bitrate_matrix(mpeg_ver=None, layer=None, bit_rate_bits=None):
    """Bitrate assignment. Caller got int val from bit shift.
    - Version [00 = MPEG Version 2.5] [01 = reserved] [10 = MPEG Version 2] [11 = MPEG Version 1]
    - Layer [00 = reserviert] [01 = Layer III] [10 = Layer II] [11 = Layer I]

    :params: mpeg_ver: int 1, 2 or 2.5
    :params: bit_rate_bits: int
    :returns: bitrate for given args
    :rtype: False if not found or bad
    """
    if bit_rate_bits == 15 or bit_rate_bits == 0:
        return False
    if layer == 0 or mpeg_ver == 1:
        return False
    # 00=0 01=1 10=2 11=3
    if mpeg_ver == 3 and layer == 3:
        col = 0
    elif mpeg_ver == 3 and layer == 2:
        col = 1
    elif mpeg_ver == 3 and layer == 1:
        col = 2
    elif mpeg_ver == 2 and layer == 3:
        col = 3
    else:
        col = 4
    return bitrate_dict[bit_rate_bits][col]


def sample_matrix(mpeg_ver=None, sample_bits=None):
    """Sample assignment.

    :params: mpeg_ver: int 1, 2 or 2.5
    :params: sample_bits: int two bits
    :returns: sample rate for given args
    :rtype: False if not found or reserved
    """
    if sample_bits == 3 or mpeg_ver == 1:
        return False
    # 00=0 01=1 10=2 11=3
    if mpeg_ver == 3:
        col = 0
    elif mpeg_ver == 2:
        col = 1
    else:
        col = 2
    return sampling_dict[sample_bits][col]
