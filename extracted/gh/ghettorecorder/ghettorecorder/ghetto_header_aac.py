"""
Use as input for further aac stream processing.
String manipulation here. Dump the complete header to get frame count to calculate bitrate.
For prod read only necessary bits with bit shift calculation.
Bit shift exercise in 'ghetto_header_mp3'.

"""
from aacrepair import audio_conf, crc


def header_info(aac_object, frame_bytes=None, print_out=None):
    """Caller can name a slice of the object ``aac_object[start idx:]`` to work.
    Example how to move the header_info in ``header_aac.read_all_header()``.

    :param: aac_object: full object or slice
    :param: frame_bytes: dump whole frame to header_dict['FRAME_BYTES']
    :param: print_out: enable print to screen

    :return: frame header properties
    :rtype: dict
    """
    # 7 Bytes of obj; loop over Byte, bin() out is string plus lead '0b', remove '0b' fill 0's left to get an 8 row
    header_bit_str_list = [(bin(bits)[2:].zfill(8)) for bits in aac_object[:7]]
    h_bit_str = ''.join(header_bit_str_list)

    sync_word = all([int(bit) for bit in h_bit_str[:12]])  # list of 'True' here 1; must contain int or bool
    if not sync_word:
        return False

    # get next header start bytes
    try:
        frame_length = int(h_bit_str[30:43], 2)
    except ValueError:
        return False
    header = ['fff1', 'fff9']  # 0|001   1|001   1, 9   mpeg-4 , mpeg-2
    next_frame_start_bytes = aac_object[frame_length:frame_length + 2]
    is_last_frame = True if not next_frame_start_bytes.hex() in header else False
    crc_bool = True if h_bit_str[15:16] == '0' else False   # --> trip wire, bit is set 1 for no CRC

    crc_16_sum_dict = {}
    if crc_bool:
        crc_byte_list = [
            aac_object[7:8],
            aac_object[8:9],
        ]
        crc_16_sum_dict = crc.reveal_crc(crc_byte_list)

    profile = int(h_bit_str[16:18], 2)
    sampling = int(h_bit_str[18:22], 2)
    channel = int(h_bit_str[23:26], 2)

    header_dict = {
        "SYNC_WORD_BOOL": sync_word,
        "MPEG4_BOOL": True if h_bit_str[12:13] == '0' else False,  # mpeg-4 is set 0
        "Layer_BOOL": True if h_bit_str[13:15] == '1' else True,  # must be 0
        "CRC_16_IS_SET_BOOL": crc_bool,
        "PROFILE_INT": profile,
        "PROFILE_STR": audio_conf.profile[profile],  # 3: AAC SSR (Scalable Sample Rate)
        "SAMPLING_FREQUENCY_INT": sampling,
        "SAMPLING_FREQUENCY_STR": audio_conf.sampling[sampling],  # 3: 48000 Hz
        "PRIVATE_BIT_BOOL": True if h_bit_str[22:23] == '1' else False,  # must be 0
        "CHANNEL_CONFIG_INT": channel,
        "CHANNEL_CONFIG_STR": audio_conf.channel[channel],  # 2: 2 channels: front-left, front-right
        "ORIGINALITY_BOOL": True if h_bit_str[26:27] == '1' else False,
        "HOME_BOOL": True if h_bit_str[27:28] == '1' else False,
        "COPYRIGHT_ID_INT": int(h_bit_str[28:29]),
        "COPYRIGHT_START_INT": int(h_bit_str[29:30]),
        "FRAME_LENGTH_INT": frame_length,
        "BIT_RESERVOIR_INT": int(h_bit_str[43:54], 2),
        "FRAME_NUMBER_INT": int(h_bit_str[54:56], 2),
        "CRC_16": crc_16_sum_dict,
        "IS_LAST_FRAME_BOOL": is_last_frame,
        "ERROR_STR": "",
        "FRAME_BYTES": b'',
    }

    if frame_bytes:
        header_dict['FRAME_BYTES'] = bytearray(aac_object[:header_dict['FRAME_LENGTH_INT']])
        if len(header_dict['FRAME_BYTES']) != header_dict['FRAME_LENGTH_INT']:
            header_dict['ERROR_STR'] = "--> frame length don't match"

    if print_out:
        fh = f'\nFirst Header & crc: {h_bit_str[0:72]}' if crc_bool else f'\nFirst Header: {h_bit_str[0:56]}'
        print(fh)
        print(*[f'{header_prop}: {prop_val} \n' for header_prop, prop_val in header_dict.items()])
        lf = "This is the last frame." if header_dict["IS_LAST_FRAME_BOOL"] else "Not last frame."
        print(lf)

    return header_dict


def header_index_get(aac_object):
    """Scan the file object for an aac frame. Search frame is hex.

    :param: aac_object: bytes
    :return: INDEX number of the first frame start Byte in the stream
    :rtype: int
    """
    start, end = 0, 2
    header = ["fff9", "fff1"]
    while 1:
        if end > len(aac_object):
            return False
        if aac_object[start:end].hex() in header:
            return start
        start += 1
        end += 1


def bytes_object_get(file_obj):
    """Read file from path (str file_obj), if it is no file stream.
    """
    if not type(file_obj) is bytes:
        file_obj = open(file_obj, "rb").read()
    return file_obj


def read_all_header(aac_object):
    """Example function returns all frame content with header until empty.

    :param: aac_object: bytes type object
    :return: header information and object content
    :rtype: Iterator[`dict`]
    """
    file_obj = bytes_object_get(aac_object)

    start = header_index_get(file_obj)
    if start is None:
        return

    checked = start
    i = 0
    while 1:
        h_dict = header_info(file_obj[checked:], frame_bytes=None, print_out=None)
        if not h_dict:
            break

        # h_dict['FRAME_BYTES'] = bytearray(file_obj[checked:checked + h_dict['FRAME_LENGTH_INT']])
        h_dict['frame_num'] = i
        checked += h_dict['FRAME_LENGTH_INT']
        yield h_dict
        i += 1


def bit_rate_get(aac_object):
    """Get bitrate for a chunk or file
    - aac_samples = 1024 or 960 (DAB+ sat, inet, digital broadcast); per Frame
    - aac_playback_time = (samples × Frame Number) / Sampling Rate in Hz

    :params: aac_object: file name or file stream
    :returns: bitrate
    :rtype: float
    """
    file_obj = bytes_object_get(aac_object)
    aac_sample = 960  # DAB+
    file_size_bit = len(file_obj) * 8
    sample_rate_hz = None

    first_header = pull_first_frame(file_obj)
    if len(first_header["SAMPLING_FREQUENCY_STR"]) >= 2:
        sample_str = first_header["SAMPLING_FREQUENCY_STR"].split(" ")  # (rate hz)
        sample_rate_hz = int(sample_str[0])

    last_header = pull_frames(file_obj)
    frame_count = last_header["frame_num"]
    aac_playback_sec = (aac_sample * frame_count) / sample_rate_hz
    bitrate = (file_size_bit / aac_playback_sec) / 1_000  # kB/s
    return bitrate


def pull_frames(path_str=None):
    """Get last header dict.

    :param: path_str: file path or object
    :returns: Header dict of last frame; can get frame count to calc bitrate
    :rtype: dict
    """
    if not path_str:
        path_str = r'f:\10\foo.aacp'

    gen = read_all_header(path_str)
    header_dict = {}
    for header_dict in list(gen):
        # print(header_dict)
        pass
    return header_dict  # last dict


def pull_first_frame(path_str=None):
    """Get first header dict.

    :param: path_str: file path or object
    """
    if not path_str:
        path_str = r'f:\10\foo.aacp'

    gen = read_all_header(path_str)
    for header_dict in list(gen):
        return header_dict  # one loop


def main():
    pull_frames()


if __name__ == '__main__':
    main()
