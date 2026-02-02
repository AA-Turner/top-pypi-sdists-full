import typing
import enum
from abc import ABC, abstractmethod
from collections import namedtuple

BERObject = namedtuple('BERObject', ['tag', 'content'])

class IncompleteBERError(ValueError):
	def __init__(self, expected_length=-1):
		super().__init__()
		self.expected_length = expected_length

def decode_ber(data):
	index = 0
	if len(data) < 2:
		raise IncompleteBERError(2)
	identifier = data[index]
	ber_class = identifier >> 6
	ber_constructed = bool(identifier & 0x20)
	ber_type = identifier & 0x1f
	index += 1
	if not data[index] & 0x80:
		length = data[index]
		index += 1
	elif data[index] == 0x80:
		raise ValueError('Indefinite form not implemented')
	elif data[index] == 0xff:
		raise ValueError('BER length invalid')
	else:
		num = data[index] & ~0x80
		index += 1
		if len(data) < index + num:
			raise IncompleteBERError(index + num)
		length = 0
		for octet in data[index:index + num]:
			length = length << 8 | octet
		index += num
	if len(data) < index + length:
		raise IncompleteBERError(index + length)
	ber_content = data[index: index + length]
	rest = data[index + length:]
	return BERObject((ber_class, ber_constructed, ber_type), ber_content), rest

def encode_ber(obj):
	tag = (obj.tag[0] & 0b11) << 6 | (obj.tag[1] & 1) << 5 | (obj.tag[2] & 0b11111)
	length = len(obj.content)
	if length < 127:
		return bytes([tag, length]) + obj.content
	octets = []
	while length:
		octets.append(length & 0xff)
		length = length >> 8
	return bytes([tag, 0x80 | len(octets)]) + bytes(reversed(octets)) + obj.content

class BERType(ABC):
	@classmethod
	@abstractmethod
	def from_ber(cls, data):
		raise NotImplementedError()

	@classmethod
	@abstractmethod
	def to_ber(cls, obj):
		raise NotImplementedError()

	def __bytes__(self):
		return type(self).to_ber(self)

class OctetString(BERType):
	BER_TAG = (0, False, 4)

	@classmethod
	def from_ber(cls, data):
		obj, rest = decode_ber(data)
		if obj.tag != cls.BER_TAG:
			raise ValueError('Expected tag %s but found %s'%(cls.BER_TAG, obj.tag))
		return obj.content, rest

	@classmethod
	def to_ber(cls, obj):
		if not isinstance(obj, bytes):
			raise TypeError()
		return encode_ber(BERObject(cls.BER_TAG, obj))

class Integer(BERType):
	BER_TAG = (0, False, 2)

	@classmethod
	def from_ber(cls, data):
		obj, rest = decode_ber(data)
		if obj.tag != cls.BER_TAG:
			raise ValueError()
		return int.from_bytes(obj.content, 'big', signed=True), rest

	@classmethod
	def to_ber(cls, obj):
		if not isinstance(obj, int):
			raise TypeError()
		if obj < 0:
			res = obj.to_bytes((8 + (obj + 1).bit_length()) // 8, byteorder='big', signed=True)
		else:
			res = obj.to_bytes(max(1, (obj.bit_length() + 7) // 8), 'big', signed=False)
			if res[0] & 0x80:
				res = b'\x00' + res
		return encode_ber(BERObject(cls.BER_TAG, res))

class Boolean(BERType):
	BER_TAG = (0, False, 1)

	@classmethod
	def from_ber(cls, data):
		obj, rest = decode_ber(data)
		if obj.tag != cls.BER_TAG or len(obj.content) != 1:
			raise ValueError()
		return bool(obj.content[0]), rest

	@classmethod
	def to_ber(cls, obj):
		if not isinstance(obj, bool):
			raise TypeError()
		content = b'\xff' if obj else b'\x00'
		return encode_ber(BERObject(cls.BER_TAG, content))

class Set(BERType):
	BER_TAG = (0, True, 17)
	SET_TYPE: BERType

	@classmethod
	def from_ber(cls, data):
		setobj, rest = decode_ber(data)
		if setobj.tag != cls.BER_TAG:
			raise ValueError()
		objs = []
		data = setobj.content
		while data:
			obj, data = cls.SET_TYPE.from_ber(data)
			objs.append(obj)
		return list(objs), rest

	@classmethod
	def to_ber(cls, obj):
		content = b''
		for item in obj:
			content += cls.SET_TYPE.to_ber(item)
		return encode_ber(BERObject(cls.BER_TAG, content))

class SequenceOf(Set):
	BER_TAG = (0, True, 16)

class Sequence(BERType):
	BER_TAG = (0, True, 16)
	# (Type, attr_name, default_value, optional?)
	SEQUENCE_FIELDS: typing.ClassVar[typing.List[typing.Tuple[BERType, str, typing.Any, bool]]] = []

	def __init__(self, *args, **kwargs):
		for index, spec in enumerate(type(self).SEQUENCE_FIELDS):
			# pylint: disable=consider-using-get,unused-variable
			field_type, name, default, optional = spec
			if index < len(args):
				value = args[index]
			elif name in kwargs:
				value = kwargs[name]
			else:
				value = default() if callable(default) else default
			setattr(self, name, value)

	def __repr__(self):
		args = []
			# pylint: disable=unused-variable
		for field_type, name, default, optional in type(self).SEQUENCE_FIELDS:
			args.append('%s=%s'%(name, repr(getattr(self, name))))
		return '<%s(%s)>'%(type(self).__name__, ', '.join(args))

	@classmethod
	def from_ber(cls, data):
		seqobj, rest = decode_ber(data)
		if seqobj.tag != cls.BER_TAG:
			raise ValueError()
		args = []
		data = seqobj.content
		# pylint: disable=unused-variable
		for field_type, name, default, optional in cls.SEQUENCE_FIELDS:
			try:
				obj, data = field_type.from_ber(data)
				args.append(obj)
			except ValueError as e:
				if not optional:
					raise e
				args.append(None)
		return cls(*args), rest

	@classmethod
	def to_ber(cls, obj):
		if not isinstance(obj, cls):
			raise TypeError()
		content = b''
		# pylint: disable=unused-variable
		for field_type, name, default, optional in cls.SEQUENCE_FIELDS:
			if not optional or getattr(obj, name) is not None:
				content += field_type.to_ber(getattr(obj, name))
		return encode_ber(BERObject(cls.BER_TAG, content))

class Choice(BERType):
	BER_TAG: typing.ClassVar[typing.Tuple[int, bool, int]]

	@classmethod
	def from_ber(cls, data):
		obj, rest = decode_ber(data)
		for subcls in cls.__subclasses__():
			if subcls.BER_TAG == obj.tag:
				return subcls.from_ber(data)
		return None, rest

	@classmethod
	def to_ber(cls, obj):
		for subcls in cls.__subclasses__():
			if isinstance(obj, subcls):
				return subcls.to_ber(obj)
		raise TypeError()

class Wrapper(BERType):
	BER_TAG: typing.ClassVar[typing.Tuple[int, bool, int]]
	WRAPPED_ATTRIBUTE: typing.ClassVar[str]
	WRAPPED_TYPE: typing.ClassVar[BERType]
	WRAPPED_DEFAULT: typing.ClassVar[typing.Any]
	WRAPPED_CLSATTRS: typing.ClassVar[typing.Dict[str, typing.Any]] = {}

	def __init__(self, *args, **kwargs):
		cls = type(self)
		attribute = cls.WRAPPED_ATTRIBUTE
		if args:
			setattr(self, attribute, args[0])
		elif kwargs:
			setattr(self, attribute, kwargs[attribute])
		else:
			setattr(self, attribute, cls.WRAPPED_DEFAULT() if callable(cls.WRAPPED_DEFAULT) else cls.WRAPPED_DEFAULT)

	def __repr__(self):
		return '<%s(%s)>'%(type(self).__name__, repr(getattr(self, type(self).WRAPPED_ATTRIBUTE)))

	@classmethod
	def from_ber(cls, data):
		class WrappedType(cls.WRAPPED_TYPE):
			BER_TAG = cls.BER_TAG
		for key, value in cls.WRAPPED_CLSATTRS.items():
			setattr(WrappedType, key, value)
		value, rest = WrappedType.from_ber(data)
		return cls(value), rest

	@classmethod
	def to_ber(cls, obj):
		class WrappedType(cls.WRAPPED_TYPE):
			BER_TAG = cls.BER_TAG
		for key, value in cls.WRAPPED_CLSATTRS.items():
			setattr(WrappedType, key, value)
		if not isinstance(obj, cls):
			raise TypeError()
		return WrappedType.to_ber(getattr(obj, cls.WRAPPED_ATTRIBUTE))

def retag(cls, tag):
	class Overwritten(cls):
		BER_TAG = tag
	return Overwritten

class Enum(Integer):
	BER_TAG = (0, False, 10)
	ENUM_TYPE = typing.ClassVar[enum.Enum]

	@classmethod
	def from_ber(cls, data):
		value, rest = super().from_ber(data)
		return cls.ENUM_TYPE(value), rest

	@classmethod
	def to_ber(cls, obj):
		if not isinstance(obj, cls.ENUM_TYPE):
			raise TypeError()
		return super().to_ber(obj.value)

def wrapenum(enumtype):
	class WrappedEnum(Enum):
		ENUM_TYPE = enumtype
	return WrappedEnum
