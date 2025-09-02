__author__ = 'Bart van Vliet'

import binascii
import struct

class Conversion:

    ####################################
    # Conversions between uint and int #
    ####################################
    @staticmethod
    def uint8_to_int8(byte):
        """	Convert a uint8 to an int8 """
        res = byte
        if res > 127:
            res -= 256
        return res

    @staticmethod
    def int8_to_uint8(byte):
        """	Convert an int8 to a uint8 """
        res = byte
        if res < 0:
            res += 256
        return res

    @staticmethod
    def uint16_to_int16(val):
        """ Convert a uint16 to an int16 """
        res = val
        if res > 32767:
            res -= 65536
        return res

    @staticmethod
    def int16_to_uint16(val):
        """ Convert an int16 to a uint16 """
        res = val
        if res < 0:
            res += 65536
        return res

    @staticmethod
    def uint32_to_int32(val):
        """ Convert an uint32 to a int32 """
        res = val
        if res > 2147483647:
            res -= 4294967296
        return res

    @staticmethod
    def int32_to_uint32(val):
        """ Convert an int32 to a uint32 """
        res = val
        if res < 0:
            res += 4294967296
        return res

    #######################################
    # Conversions between uint8 and float #
    #######################################
    @staticmethod
    def uint8_array_to_float(arr8):
        """ Convert an array of 4 bytes to a float """
        return struct.unpack('<f', bytearray(arr8))[0]

    @staticmethod
    def float_to_uint8_array(val):
        """ Convert a float to an array of 4 bytes """
        return bytearray(struct.pack('<f', val))

    ########################################
    # Conversions between uint8 and uint16 #
    ########################################
    @staticmethod
    def uint8_to_uint16(byte0, byte1):
        """ Convert 2 bytes to a uint16 """
        return (byte1 << 8) + byte0

    @staticmethod
    def uint8_array_to_uint16(arr8):
        """ Convert an array of 2 bytes to a uint16 """
        return (arr8[1] << 8) + arr8[0]

    @staticmethod
    def uint8_array_to_int16(arr8):
        """ Convert an array of 2 bytes to a uint16 """
        return Conversion.uint16_to_int16(Conversion.uint8_array_to_uint16(arr8))

    @staticmethod
    def uint16_to_uint8_array(value):
        """ Convert a number into an array of 2 bytes. """
        return [
            (value >> 0 & 0xFF),
            (value >> 8 & 0xFF)
        ]

    @staticmethod
    def int16_to_uint8_array(value):
        return Conversion.uint16_to_uint8_array(Conversion.int16_to_uint16(value))

    @staticmethod
    def uint8_to_uint8_array(value):
        """ Convert a number into an array of 1 bytes. """
        return [ value & 0xFF ]

    @staticmethod
    def uint8_array_to_uint16_array(arr8):
        """	Convert a uint8 array to a uint16 array	"""
        arr16 = []
        for i in range(1, len(arr8), 2):
#			arr16.append(Conversion.uint8_array_to_uint16(arr8[i-1 : i+1]))
            arr16.append(Conversion.uint8_to_uint16(arr8[i-1], arr8[i]))
        return arr16

    @staticmethod
    def uint16_array_to_uint8_array(arr16):
        """	Convert a uint16 array to a byte array """
        arr8 = []
        for val in arr16:
            arr8.extend(Conversion.uint16_to_uint8_array(val))
        return arr8


    ########################################
    # Conversions between uint8 and uint32 #
    ########################################
    @staticmethod
    def uint8_to_uint32(byte0, byte1, byte2, byte3):
        """ Convert 4 bytes to a uint32 """
        return (byte3 << 24) + (byte2 << 16) + (byte1 << 8) + byte0

    @staticmethod
    def uint8_array_to_uint32(arr8):
        """ Convert an array of 4 bytes to a uint32 """
        return (arr8[3] << 24) + (arr8[2] << 16) + (arr8[1] << 8) + arr8[0]

    @staticmethod
    def uint8_array_to_uint64(arr8):
        """ Convert an array of 4 bytes to a uint32 """
        return (arr8[7] << 56) + \
               (arr8[6] << 48) + \
               (arr8[5] << 40) + \
               (arr8[4] << 32) + \
               (arr8[3] << 24) + \
               (arr8[2] << 16) + \
               (arr8[1] << 8) + \
               arr8[0]


    @staticmethod
    def uint8_array_to_int32(arr8):
        """ Convert an array of 4 bytes to a uint32 """
        return Conversion.uint32_to_int32(Conversion.uint8_array_to_uint32(arr8))

    @staticmethod
    def uint8_array_to_uint32_array(arr8):
        """	Convert a uint8 array to a uint16 array	"""
        arr32 = []
        for i in range(3, len(arr8), 4):
#			arr32.append(Conversion.uint8_array_to_uint32(arr8[i-3 : i+1]))
            arr32.append(Conversion.uint8_to_uint32(arr8[i-3], arr8[i-2], arr8[i-1], arr8[i]))
        return arr32

    @staticmethod
    def uint32_to_uint8_array(value):
        """ Convert a number into an array of 4 bytes. """
        return [
            (value >> 0 & 0xFF),
            (value >> 8 & 0xFF),
            (value >> 16 & 0xFF),
            (value >> 24 & 0xFF)
        ]
    @staticmethod
    def int32_to_uint8_array(value):
        """ Convert a number into an array of 4 bytes. """
        return Conversion.uint32_to_uint8_array(Conversion.int32_to_uint32(value))

    @staticmethod
    def uint64_to_uint8_array(value):
        """ Convert a number into an array of 8 bytes. (little endian) """
        return [ value >> 8*i & 0xFF for i in range(8)]

    @staticmethod
    def uint32_array_to_uint8_array(arr32):
        """	Convert a uint32 array to a byte array """
        arr8 = []
        for val in arr32:
            arr8.extend(Conversion.uint32_to_uint8_array(val))
        return arr8


    @staticmethod
    def uint32_to_uint16_reversed_array(uint32):
        return [
            uint32 >> 16,
            (uint32 >> 0) % (0xFFFF + 1),
        ]

    @staticmethod
    def uint16_reversed_array_to_uint32(uint16Array):
        return uint16Array[1] + (uint16Array[0] * (0xFFFF + 1))


    ##############################
    # uint8 array to/from string #
    ##############################
    @staticmethod
    def uint8_array_to_string(arr8):
#		string = ""
#		for i in range(0, len(arr8)):
#			string += chr(arr8[i])
#		return string
#		return str(bytearray(arr8))
        return bytearray(arr8).decode()

    @staticmethod
    def string_to_uint8_array(string):
        arr8 = []
        for i in range(0, len(string)):
            arr8.append(ord(string[i]))
        return bytes(arr8)

    @staticmethod
    def uint8_array_to_uint8(arr8):
        return int(arr8[0] & 0xFF)

    @staticmethod
    def uint8_array_to_int8(arr8):
        return Conversion.uint8_to_int8(Conversion.uint8_array_to_uint8(arr8))



    ########################
    # Number to hex string #
    ########################
    @staticmethod
    def uint8_to_hex_string(val):
        if val > 255 or val < 0:
            raise Exception(f"Value must be of type uint8. Value = {val}")
        hex_str = "%02x" % val
        return hex_str

    @staticmethod
    def uint8_array_to_hex_string(arr):
#		hex_str = Conversion.uint8_to_hex_string(arr[0])
#		for i in range(1, len(arr)):
#			hex_str += Conversion.uint8_to_hex_string(arr[i])
#		return hex_str
        return binascii.b2a_hex(bytearray(arr)).decode('utf-8')

    @staticmethod
    def uint16_to_hex_string(val):
        arr8 = Conversion.uint16_to_uint8_array(val)
        return Conversion.uint8_array_to_hex_string(arr8)

    @staticmethod
    def uint32_to_hex_string(val):
        arr8 = Conversion.uint32_to_uint8_array(val)
        return Conversion.uint8_array_to_hex_string(arr8)


    #######################
    # Hex string to array #
    #######################

    @staticmethod
    def ibeaconUUIDString_to_uint8_array(inputStr):
        hexStr = inputStr.replace(":","").replace("-","")
        return Conversion.hex_string_to_uint8_array(hexStr)

    @staticmethod
    def ibeaconUUIDString_to_reversed_uint8_array(inputStr):
        arr = Conversion.ibeaconUUIDString_to_uint8_array(inputStr)
        arr.reverse()
        return arr

    @staticmethod
    def ascii_or_hex_string_to_16_byte_array(inputStr):
        if len(inputStr) == 16:
            return Conversion.string_to_uint8_array(inputStr)
        else :
            return Conversion.hex_string_to_uint8_array(inputStr)


    @staticmethod
    def hex_string_to_uint8_array(hexStr):
#		""" Convert a string which represents a hex byte buffer to an uint8 array """
#		""" Only converts buffer from start to start+size bytes """
#		buf = buffer_str.split(" ")
#		if (size == False):
#			size=len(buf)
#		arr = []
#		for i in range(start, start+size):
#			arr.append(int(buf[i], 16))
#		return arr
        """
        Converts a hexadecimal string to a byte array
        :param hexStr: hexadecimal string to be converted
        :type hexStr: str
        :rtype: bytearray
        """
        return bytearray(binascii.a2b_hex(hexStr.encode('utf-8')))

    @staticmethod
    def hex_string_to_uint16_array(hexStr):
#	def hex_string_to_uint16_array(buffer_str, start=0, size=False):
#		""" Convert a string which represents a hex byte buffer to an uint16 array """
#		""" Only converts buffer from start to start+size*2 bytes """
#		buf = buffer_str.split(" ")
#		if (size == False):
#			size=len(buf)/2
#		arr16 = []
#		for i in range(0, size):
#			arr16.append(Conversion.uint8_array_to_uint16([int(buf[start+2*i], 16), int(buf[start+2*i+1], 16)]))
#		return arr16
        """
        Converts a hexadecimal string to a uint16 array
        :param hexStr: hexadecimal string to be converted
        :type hexStr: str
        :rtype: list
        """
        arr8 = bytearray(binascii.a2b_hex(hexStr.encode('utf-8')))
        return Conversion.uint8_array_to_uint16(arr8)

    @staticmethod
    def hex_string_to_uint32_array(hexStr):
#	def hex_string_to_uint32_array(buffer_str, start=0, size=False):
#		""" Convert a string which represents a hex byte buffer to an uint32 array """
#		""" Only converts buffer from start to start+size*4 bytes """
#		buf = buffer_str.split(" ")
#		if (size == False):
#			size=len(buf)/4
#		arr32 = []
#		for i in range(0, size):
#			arr32.append(Conversion.uint8_array_to_uint32([int(buf[start+4*i], 16), int(buf[start+4*i+1], 16), int(buf[start+4*i+2], 16), int(buf[start+4*i+3], 16)]))
#		return arr32
        """
        Converts a hexadecimal string to a uint32 array
        :param hexStr: hexadecimal string to be converted
        :type hexStr: str
        :rtype: list
        """
        arr8 = bytearray(binascii.a2b_hex(hexStr.encode('utf-8')))
        return Conversion.uint8_array_to_uint32(arr8)

    @staticmethod
    def address_to_uint8_array(addressStr):
        """
        Converts a bluetooth address string to a uint8 array
        :param addressStr: address string to be converted, must be like: "01:23:45:67:89:AB"
        :type addressStr: str
        :rtype: list
        """
        hexStrArr = addressStr.split(":")
        if len(hexStrArr) != 6:
            return []

        arr8 = []
        for p in reversed(hexStrArr):
            arr8.append(Conversion.hex_string_to_uint8_array(p)[0])
        return bytearray(arr8)

    @staticmethod
    def uint8_array_to_address(arr8):
        """
        Converts a uint8 array to a bluetooth address string
        :param arr8: array of uint8, should be 6 long.
        :type arr8: bytearray
        :rtype: str
        """
        if (len(arr8) != 6):
            return ""
        hexStr = Conversion.uint8_to_hex_string(arr8[-1])
        for b in reversed(arr8[0:-1]):
            hexStr = hexStr + ":" + Conversion.uint8_to_hex_string(b)
        return hexStr


    @staticmethod
    def bit_array_to_010_array(bitArray):
        result = [0] * len(bitArray)

        for i in range(0,len(bitArray)):
            if bitArray[i]:
                result[i] = 1

        return result



    @staticmethod
    def uint8_to_bit_array(val):
        result = [False, False, False, False, False, False, False, False]

        one = 1

        result[0] = (val & (one << 0)) != 0
        result[1] = (val & (one << 1)) != 0
        result[2] = (val & (one << 2)) != 0
        result[3] = (val & (one << 3)) != 0
        result[4] = (val & (one << 4)) != 0
        result[5] = (val & (one << 5)) != 0
        result[6] = (val & (one << 6)) != 0
        result[7] = (val & (one << 7)) != 0

        return result

    @staticmethod
    def uint16_to_bit_array(val):
        # TODO: this might be the wrong order
        result = [False] * 16
        one = 1

        for i in range(0, 16):
            result[i] = (val & (one << 15 - i)) != 0

        return result

    @staticmethod
    def uint32_to_bit_array(val):
        # TODO: this might be the wrong order
        result = [False] * 32
        one = 1

        for i in range(0,32):
            result[i] = (val & (one << 31 - i)) != 0

        return result

    @staticmethod
    def uint32_to_bit_array_reversed(val):
        # TODO: this might be the wrong order
        result = [False] * 32
        one = 1

        for i in range(0,32):
            result[i] = (val & (one << 31 - i)) != 0

        return list(reversed(result))
