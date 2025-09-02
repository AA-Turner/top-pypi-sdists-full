from crownstone_core.util.Conversion import Conversion

class BufferWriter :
    """
    Class to fill a data buffer.

    Data will be appended to the buffer for each consecutive set call.

    Function calls will raise an exception on error.
    """
    def __init__(self, data=None):
        """
        Constructor

        data : initial list of bytes, can be None.
        """
        if data is None:
            data = []
        self.data = data

    def getLength(self):
        """ Get the current length of the buffer in bytes. """
        return len(self.data)

    def getBuffer(self):
        """ Get the buffer. """
        return self.data

    def putUInt8(self, value):
        """ Append a uint8 to the buffer. """
        self.data.append(value)

    def putInt8(self, value):
        """ Append an int8 to the buffer. """
        self.putUInt8(Conversion.int8_to_uint8(value))

    def putUInt16(self, value):
        """ Append a uint16 to the buffer. """
        self.data.extend(Conversion.uint16_to_uint8_array(value))

    def putInt16(self, value):
        """ Append an int16 to the buffer. """
        self.putUInt16(Conversion.int16_to_uint16(value))

    def putUInt32(self, value):
        """ Append a uint32 to the buffer. """
        self.data.extend(Conversion.uint32_to_uint8_array(value))

    def putInt32(self, value):
        """ Append an int32 to the buffer. """
        self.putUInt32(Conversion.int32_to_uint32(value))

    def putFloat(self, value):
        """ Append a float to the buffer. """
        self.data.extend(Conversion.float_to_uint8_array(value))

    def putBytes(self, data):
        """ Append a list of bytes to the buffer. """
        self.data.extend(data)
