from crownstone_core.util.BufferReader import BufferReader
from crownstone_core.util.BufferWriter import BufferWriter


class BasePacket:
	def _deserialize(self, reader: BufferReader):
		"""
		The deserialization function to be implemented by derived classes.
		:param reader: The class with data to be parsed.
		"""
		raise NotImplementedError

	def _serialize(self, writer: BufferWriter):
		"""
		The serialization function to be implemented by derived classes.
		:param writer: The class to write the data to.
		"""
		raise NotImplementedError

	def deserialize(self, data):
		if isinstance(data, BufferReader):
			self._deserialize(data)
		elif isinstance(data, list):
			reader = BufferReader(data)
			self._deserialize(reader)
		else:
			raise TypeError(f"Invalid type: {type(data)}")

	def serialize(self, data = None) -> list:
		if isinstance(data, BufferWriter):
			writer = data
			self._serialize(writer)
			buf = writer.getBuffer()
			return buf
		else:
			writer = BufferWriter()
			self._serialize(writer)
			buf = writer.getBuffer()
			if data is None:
				return buf
			else:
				data.extend(buf)
				return data
