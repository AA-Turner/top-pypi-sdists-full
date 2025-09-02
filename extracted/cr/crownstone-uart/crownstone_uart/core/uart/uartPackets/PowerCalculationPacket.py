from crownstone_core.util.Conversion import Conversion


class PowerCalculationPacket:
	amountOfSamples = 9
	sampleSize = 4
	packetSize = amountOfSamples * sampleSize

	def __init__(self, payload):
		self.currentRmsMA = 0
		self.currentRmsMedianMA = 0
		self.filteredCurrentRmsMA = 0
		self.filteredCurrentRmsMedianMA = 0
		self.avgZeroVoltage = 0
		self.avgZeroCurrent = 0
		self.powerMilliWattApparent = 0
		self.powerMilliWattReal = 0
		self.avgPowerMilliWattReal = 0
		
		if len(payload) < self.packetSize:
			print("ERROR: INVALID PAYLOAD LENGTH", len(payload), payload)
			return

		i = 0
		self.currentRmsMA 				= Conversion.uint8_array_to_int32(payload[i:i+self.sampleSize])
		i += self.sampleSize

		self.currentRmsMedianMA 		= Conversion.uint8_array_to_int32(payload[i:i+self.sampleSize])
		i += self.sampleSize

		self.filteredCurrentRmsMA 		= Conversion.uint8_array_to_int32(payload[i:i+self.sampleSize])
		i += self.sampleSize

		self.filteredCurrentRmsMedianMA = Conversion.uint8_array_to_int32(payload[i:i+self.sampleSize])
		i += self.sampleSize

		self.avgZeroVoltage 			= Conversion.uint8_array_to_int32(payload[i:i+self.sampleSize])
		i += self.sampleSize

		self.avgZeroCurrent 			= Conversion.uint8_array_to_int32(payload[i:i+self.sampleSize])
		i += self.sampleSize

		self.powerMilliWattApparent 	= Conversion.uint8_array_to_int32(payload[i:i+self.sampleSize])
		i += self.sampleSize

		self.powerMilliWattReal 		= Conversion.uint8_array_to_int32(payload[i:i+self.sampleSize])
		i += self.sampleSize

		self.avgPowerMilliWattReal 		= Conversion.uint8_array_to_int32(payload[i:i+self.sampleSize])

	def getDict(self):
		data = {}

		data["id"] = 0  # TODO: get the Crownstone ID here.
		data["currentRmsMA"] = self.currentRmsMA
		data["currentRmsMedianMA"] = self.currentRmsMedianMA
		data["filteredCurrentRmsMA"] = self.filteredCurrentRmsMA
		data["filteredCurrentRmsMedianMA"] = self.filteredCurrentRmsMedianMA
		data["avgZeroVoltage"] = self.avgZeroVoltage
		data["avgZeroCurrent"] = self.avgZeroCurrent
		data["powerMilliWattApparent"] = self.powerMilliWattApparent
		data["powerMilliWattReal"] = self.powerMilliWattReal
		data["avgPowerMilliWattReal"] = self.avgPowerMilliWattReal

		return data