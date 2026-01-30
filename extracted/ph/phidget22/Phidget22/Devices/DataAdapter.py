import sys
import ctypes
from Phidget22.PhidgetSupport import PhidgetSupport
from Phidget22.Async import *
from Phidget22.DataAdapterVoltage import DataAdapterVoltage
from Phidget22.DataAdapterEndianness import DataAdapterEndianness
from Phidget22.DataAdapterFrequency import DataAdapterFrequency
from Phidget22.DataAdapterSPIChipSelect import DataAdapterSPIChipSelect
from Phidget22.DataAdapterSPIMode import DataAdapterSPIMode
from Phidget22.PhidgetException import PhidgetException

from Phidget22.Phidget import Phidget

class DataAdapter(Phidget):

	def __init__(self):
		Phidget.__init__(self)
		self.handle = ctypes.c_void_p()
		self._sendPacket_async = None
		self._onsendPacket_async = None

		__func = PhidgetSupport.getDll().PhidgetDataAdapter_create
		__func.restype = ctypes.c_int32
		res = __func(ctypes.byref(self.handle))

		if res > 0:
			raise PhidgetException(res)

	def __del__(self):
		Phidget.__del__(self)

	def getDataAdapterVoltage(self):
		_DataAdapterVoltage = ctypes.c_int()

		__func = PhidgetSupport.getDll().PhidgetDataAdapter_getDataAdapterVoltage
		__func.restype = ctypes.c_int32
		result = __func(self.handle, ctypes.byref(_DataAdapterVoltage))

		if result > 0:
			raise PhidgetException(result)

		return _DataAdapterVoltage.value

	def setDataAdapterVoltage(self, DataAdapterVoltage):
		_DataAdapterVoltage = ctypes.c_int(DataAdapterVoltage)

		__func = PhidgetSupport.getDll().PhidgetDataAdapter_setDataAdapterVoltage
		__func.restype = ctypes.c_int32
		result = __func(self.handle, _DataAdapterVoltage)

		if result > 0:
			raise PhidgetException(result)


	def getDataBits(self):
		_DataBits = ctypes.c_uint32()

		__func = PhidgetSupport.getDll().PhidgetDataAdapter_getDataBits
		__func.restype = ctypes.c_int32
		result = __func(self.handle, ctypes.byref(_DataBits))

		if result > 0:
			raise PhidgetException(result)

		return _DataBits.value

	def setDataBits(self, DataBits):
		_DataBits = ctypes.c_uint32(DataBits)

		__func = PhidgetSupport.getDll().PhidgetDataAdapter_setDataBits
		__func.restype = ctypes.c_int32
		result = __func(self.handle, _DataBits)

		if result > 0:
			raise PhidgetException(result)


	def getMinDataBits(self):
		_MinDataBits = ctypes.c_uint32()

		__func = PhidgetSupport.getDll().PhidgetDataAdapter_getMinDataBits
		__func.restype = ctypes.c_int32
		result = __func(self.handle, ctypes.byref(_MinDataBits))

		if result > 0:
			raise PhidgetException(result)

		return _MinDataBits.value

	def getMaxDataBits(self):
		_MaxDataBits = ctypes.c_uint32()

		__func = PhidgetSupport.getDll().PhidgetDataAdapter_getMaxDataBits
		__func.restype = ctypes.c_int32
		result = __func(self.handle, ctypes.byref(_MaxDataBits))

		if result > 0:
			raise PhidgetException(result)

		return _MaxDataBits.value

	def getEndianness(self):
		_Endianness = ctypes.c_int()

		__func = PhidgetSupport.getDll().PhidgetDataAdapter_getEndianness
		__func.restype = ctypes.c_int32
		result = __func(self.handle, ctypes.byref(_Endianness))

		if result > 0:
			raise PhidgetException(result)

		return _Endianness.value

	def setEndianness(self, Endianness):
		_Endianness = ctypes.c_int(Endianness)

		__func = PhidgetSupport.getDll().PhidgetDataAdapter_setEndianness
		__func.restype = ctypes.c_int32
		result = __func(self.handle, _Endianness)

		if result > 0:
			raise PhidgetException(result)


	def getFrequency(self):
		_Frequency = ctypes.c_int()

		__func = PhidgetSupport.getDll().PhidgetDataAdapter_getFrequency
		__func.restype = ctypes.c_int32
		result = __func(self.handle, ctypes.byref(_Frequency))

		if result > 0:
			raise PhidgetException(result)

		return _Frequency.value

	def setFrequency(self, Frequency):
		_Frequency = ctypes.c_int(Frequency)

		__func = PhidgetSupport.getDll().PhidgetDataAdapter_setFrequency
		__func.restype = ctypes.c_int32
		result = __func(self.handle, _Frequency)

		if result > 0:
			raise PhidgetException(result)


	def i2cComplexTransaction(self, address, I2CPacketString, data):
		_address = ctypes.c_int32(address)
		_I2CPacketString = ctypes.create_string_buffer(I2CPacketString.encode('utf-8'))
		_data = (ctypes.c_uint8 * len(data))(*data)
		_dataLen = ctypes.c_size_t(len(data))
		_recvData = (ctypes.c_uint8 * 127)()
		_recvDataLen = ctypes.c_size_t(127)

		__func = PhidgetSupport.getDll().PhidgetDataAdapter_i2cComplexTransaction
		__func.restype = ctypes.c_int32
		result = __func(self.handle, _address, ctypes.byref(_I2CPacketString), ctypes.byref(_data), _dataLen, ctypes.byref(_recvData), ctypes.byref(_recvDataLen))

		if result > 0:
			raise PhidgetException(result)

		return list(_recvData[:_recvDataLen.value])

	def i2cSendReceive(self, address, data, receiveLength):
		_address = ctypes.c_int32(address)
		_data = (ctypes.c_uint8 * len(data))(*data)
		_dataLen = ctypes.c_size_t(len(data))
		_recvData = (ctypes.c_uint8 * receiveLength)()
		_receiveLength = ctypes.c_size_t(receiveLength)

		__func = PhidgetSupport.getDll().PhidgetDataAdapter_i2cSendReceive
		__func.restype = ctypes.c_int32
		result = __func(self.handle, _address, ctypes.byref(_data), _dataLen, ctypes.byref(_recvData), _receiveLength)

		if result > 0:
			raise PhidgetException(result)

		return list(_recvData[:_receiveLength.value])

	def getMaxReceivePacketLength(self):
		_MaxReceivePacketLength = ctypes.c_uint32()

		__func = PhidgetSupport.getDll().PhidgetDataAdapter_getMaxReceivePacketLength
		__func.restype = ctypes.c_int32
		result = __func(self.handle, ctypes.byref(_MaxReceivePacketLength))

		if result > 0:
			raise PhidgetException(result)

		return _MaxReceivePacketLength.value

	def sendPacket(self, data):
		_data = (ctypes.c_uint8 * len(data))(*data)
		_dataLen = ctypes.c_size_t(len(data))

		__func = PhidgetSupport.getDll().PhidgetDataAdapter_sendPacket
		__func.restype = ctypes.c_int32
		result = __func(self.handle, ctypes.byref(_data), _dataLen)

		if result > 0:
			raise PhidgetException(result)


	def sendPacket_async(self, data, asyncHandler):
		_data = (ctypes.c_uint8 * len(data))(*data)
		_dataLen = ctypes.c_size_t(len(data))

		_ctx = ctypes.c_void_p()
		if asyncHandler != None:
			_ctx = ctypes.c_void_p(AsyncSupport.add(asyncHandler, self))
		_asyncHandler = AsyncSupport.getCallback()

		__func = PhidgetSupport.getDll().PhidgetDataAdapter_sendPacket_async
		__func(self.handle, ctypes.byref(_data), _dataLen, _asyncHandler, _ctx)


	def getMaxSendPacketLength(self):
		_MaxSendPacketLength = ctypes.c_uint32()

		__func = PhidgetSupport.getDll().PhidgetDataAdapter_getMaxSendPacketLength
		__func.restype = ctypes.c_int32
		result = __func(self.handle, ctypes.byref(_MaxSendPacketLength))

		if result > 0:
			raise PhidgetException(result)

		return _MaxSendPacketLength.value

	def sendPacketWaitResponse(self, data):
		_data = (ctypes.c_uint8 * len(data))(*data)
		_dataLen = ctypes.c_size_t(len(data))
		_recvData = (ctypes.c_uint8 * 1024)()
		_recvDataLen = ctypes.c_size_t(1024)

		__func = PhidgetSupport.getDll().PhidgetDataAdapter_sendPacketWaitResponse
		__func.restype = ctypes.c_int32
		result = __func(self.handle, ctypes.byref(_data), _dataLen, ctypes.byref(_recvData), ctypes.byref(_recvDataLen))

		if result > 0:
			raise PhidgetException(result)

		return list(_recvData[:_recvDataLen.value])

	def getSPIChipSelect(self):
		_SPIChipSelect = ctypes.c_int()

		__func = PhidgetSupport.getDll().PhidgetDataAdapter_getSPIChipSelect
		__func.restype = ctypes.c_int32
		result = __func(self.handle, ctypes.byref(_SPIChipSelect))

		if result > 0:
			raise PhidgetException(result)

		return _SPIChipSelect.value

	def setSPIChipSelect(self, SPIChipSelect):
		_SPIChipSelect = ctypes.c_int(SPIChipSelect)

		__func = PhidgetSupport.getDll().PhidgetDataAdapter_setSPIChipSelect
		__func.restype = ctypes.c_int32
		result = __func(self.handle, _SPIChipSelect)

		if result > 0:
			raise PhidgetException(result)


	def getSPIMode(self):
		_SPIMode = ctypes.c_int()

		__func = PhidgetSupport.getDll().PhidgetDataAdapter_getSPIMode
		__func.restype = ctypes.c_int32
		result = __func(self.handle, ctypes.byref(_SPIMode))

		if result > 0:
			raise PhidgetException(result)

		return _SPIMode.value

	def setSPIMode(self, SPIMode):
		_SPIMode = ctypes.c_int(SPIMode)

		__func = PhidgetSupport.getDll().PhidgetDataAdapter_setSPIMode
		__func.restype = ctypes.c_int32
		result = __func(self.handle, _SPIMode)

		if result > 0:
			raise PhidgetException(result)

