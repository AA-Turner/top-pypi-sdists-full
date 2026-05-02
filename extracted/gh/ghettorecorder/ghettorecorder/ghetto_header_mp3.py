"""Output is human-readable. Non-destructive.
Use as input for further mp3 stream processing.

* Feed streaming web server with file system sound files. Needs bitrate per second, else browser hangs.

http://www.mp3-tech.org/programmer/frame_header.html

Bytes

       ======== ======== ======== ======== ======== ========
            1       2       3        4        5        6
       ======== ======== ======== ======== ======== ========
       AAAAAAAA AAABBCCD EEEEFFGH IIJJKLMM OOOOOOOO OOOOOOOO
       ======== ======== ======== ======== ======== ========

Bit Groups

       ===== ========= ====== ====================================================================================
       Group    Number  Count  Description
       ===== ========= ====== ====================================================================================
       A         0-11    11 	Syncword, all bits 1
       B        12-13     2 	[00 = MPEG Version 2.5] [01 = reserved] [10 = MPEG Version 2] [11 = MPEG Version 1]
       C        14-15     2 	Layer [00 = reserviert] [01 = Layer III] [10 = Layer II] [11 = Layer I]
       D           16     1 	[[[ ``Warning`` ]]], set to 1 if there is no CRC and 0 if there is CRC
       E        17-20     4 	Bitrate index table, Version and layer read the table
       F        21-22     2 	Sampling rate frequency index
       G           23     1 	Padding bit [0 - frame is not padded] [1 - frame is padded with one extra slot]
       H           24     1 	Private bit. This one is only informative.
       I        25-26     2 	Channel Mode [00 - Stereo] [01 - Joint stereo] [10 - Dual]  [11 - Single (Mono)]
       J        27-28     2 	Mode extension (Only used in Joint stereo)
       K           29     1 	Copyright ID bit
       L           30     1 	Original [0 - Copy of original media] [1 - Original media]
       M        31-32     2 	Emphasis [00 - none] [01 - 50/15 ms] [10 - reserved] [11 - CCIT J.17]
       O        33-48    16 	CRC if existing, D 16 set
       ===== ========= ====== ====================================================================================

       frame length layer 1: FrameLengthInBytes = (12 * BitRate / SampleRate + Padding) * 4
       frame length layer 2: FrameLengthInBytes = 144 * BitRate / SampleRate + Padding

The next line is C code::

       //*************************************************************************************
       //  This reference data is from MPEGAudioInfo app
       // Samples per Frame / 8
       static const u32 m_dwCoefficients[2][3] =
       {
          {  // MPEG 1
             12,   // Layer1   (must be multiplied with 4, because of slot size)
             144,  // Layer2
             144   // Layer3
          },
          {  // MPEG 2, 2.5
             12,   // Layer1   (must be multiplied with 4, because of slot size)
             144,  // Layer2
             72    // Layer3
          }
       };

"""
import io
import ghettorecorder.audio_conf as audio_conf
from collections import defaultdict


class Mp3Header:
    """Find bitrate in header.
    'br_dict' list with most votes wins.

    __init__(self, file)

    :param: file: # can be path string

    """

    def __init__(self, file):
        self.file = file
        self.mp3_object = None
        self.bitrate = None
        self.sampling = None
        self.mpeg_layer = None
        self.mpeg_version = None
        self.bit_rate_table = None
        self.br_dict = defaultdict(list)  # {128: [1,1,1,1], 64: [1], 256: [1,1]} search winner in garbage
        self.mp3_object_to_bytes()

    def mp3_object_to_bytes(self):
        """Convert path to file like object, if path, else it is bytes object"""
        self.mp3_object = open(self.file, "rb").read() if not type(self.file) is bytes else self.file

    def bitrate_get(self):
        """Looking for the first bits of mp3 header.
        Search sync_word. Second byte of word has only 3bit information. Mask and bit-shift.

        :returns: bitrate int, or None
        """
        start, end = 0, 4  # 4 byte, 5 + 6 crc
        sync_word_left = 0b11111111
        sync_word_right = 0b111
        while 1:
            if end > len(self.mp3_object) or end == io.DEFAULT_BUFFER_SIZE:  # Win 8192 bytes
                self.bitrate = self.bitrate_get_from_dict()
                break

            header = self.mp3_object[start:end]
            if header[0] & sync_word_left == 0b11111111 and header[1] >> 5 == sync_word_right:
                self.bitrate_one_frame_get(self.mp3_object[start:])
            start += 1
            end += 1
        return int(self.bitrate) if self.bitrate else None

    def bitrate_one_frame_get(self, mp3_object):
        """Extract bitrate via bit shift and mask into 'br_dict'.
        Bit Groups listed in module's docString.
        and(ing) 11... bits, move resulting bits right and calculate
        """
        version_int = (mp3_object[1] & 0b00011000) >> 3
        layer_int = (mp3_object[1] & 0b00000110) >> 1
        bit_rate_int = (mp3_object[2] & 0b11110000) >> 4
        sample_int = (mp3_object[2] & 0b00001100) >> 2

        if (version_int == 1) or (layer_int == 0):  # 01 and 00 reserved
            return
        bitrate = audio_conf.bitrate_matrix(version_int, layer_int, bit_rate_int)
        sample_rate = audio_conf.sample_matrix(version_int, sample_int)
        if bitrate and sample_rate:
            self.br_dict[bitrate].append(1)

    def bitrate_get_from_dict(self):
        """Calculate the bitrate from dict. We have defective Header and intersections of unknown.
        Key bitrate with most votes wins.

        :returns: bitrate of file like obj, else None
        """
        br_dict = {bitrate: sum(self.br_dict[bitrate]) for bitrate in self.br_dict.keys()}  # sum of 1's
        self.br_dict = defaultdict(list)

        if len(br_dict):
            bitrate_tup = max([(count, bitrate) for bitrate, count in br_dict.items()])
            bitrate = bitrate_tup[1]
            return bitrate


def main(path_str=None):
    """Example to get the bitrate.

    :param: path_str: file path or object
    """
    path_str = r'f:\10\foo.mp3' if not path_str else path_str
    mp3H = Mp3Header(path_str)
    bitrate = mp3H.bitrate_get()
    print(f'--> bitrate: {bitrate}.') if bitrate else print('--> .. no bitrate found.')


if __name__ == '__main__':
    main()
