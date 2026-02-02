'''LDAP Distinguished Name Utilities

Distinguished Names (DNs) identifiy objects in an LDAP directory. In LDAP
protocol messages and when stored in attribute values DNs are encoded with
a string representation scheme described in RFC4514.

This module provides classes to represent `DN` objects and theirs parts
(`RD` and `RDNAssertion`) that correctly implement encoding, decoding and
comparing.

Limitations:

* Hexstring attribute values (`foo=#ABCDEF...`) are not supported
* Attribute values are only validated in from_str
'''

import typing
import re
import functools

from . import exceptions

__all__ = ['DN', 'RDN', 'RDNAssertion', 'DNWithUID']

class DN(tuple):
	'''Distinguished Name consisting of zero ore more :class:`RDN` objects'''
	#:
	schema: typing.Any

	def __new__(cls, schema, *args, **kwargs):
		if len(args) == 1 and isinstance(args[0], DN):
			args = args[0]
		if len(args) == 1 and isinstance(args[0], str):
			args = cls.from_str(schema, args[0])
		for rdn in args:
			if not isinstance(rdn, RDN):
				raise TypeError(f'Argument {repr(rdn)} is of type {repr(type(rdn))}, expected ldapserver.dn.RDN object')
		rdns = tuple(args)
		if kwargs:
			rdns = (RDN(schema, **kwargs),) + rdns
		dn = super().__new__(cls, rdns)
		dn.schema = schema
		return dn

	# Syntax definiton from RFC4514:
	# distinguishedName = [ relativeDistinguishedName *( COMMA relativeDistinguishedName ) ]

	@classmethod
	@functools.lru_cache(maxsize=128, typed=False)
	def from_str(cls, schema, expr):
		'''Parse string representation of a DN according to RFC 4514

		:param schema: Schema for the DN
		:type schema: schema.Schema
		:param expr: DN string representation
		:type expr: str
		:raises ValueError: if expr is invalid
		:returns: Parsed DN
		:rtype: DN'''
		rdns = []
		while expr:
			# relativeDistinguishedName may contain escape sequences including "\,".
			# Split off first token expr at "," while ignoring "\,".
			match = re.match(r'^(([^,\\]|\\.)+)(,|$)', expr)
			if not match:
				raise ValueError(f'Unrecognized token {expr!r}')
			expr = expr[match.end():]
			rdn_expr, _, _ = match.groups()
			rdns.append(RDN.from_str(schema, rdn_expr))
		return cls(schema, *rdns)

	def __str__(self):
		'''Return string representation of DN according to RFC 4514

		:returns: Representation of self
		:rtype: str'''
		return ','.join(map(str, self))

	def __repr__(self):
		return '<ldapserver.DN %s>'%str(self)

	def __eq__(self, obj):
		return type(self) is type(obj) and super().__eq__(obj)

	def __ne__(self, obj):
		return not self == obj

	def __add__(self, value):
		if isinstance(value, DN):
			return DN(self.schema, *(tuple(self) + tuple(value)))
		elif isinstance(value, RDN):
			return self + DN(self.schema, value)
		else:
			raise TypeError(f'Can only add DN or RDN to DN, not {type(value)}')

	def __getitem__(self, key):
		if isinstance(key, slice):
			return type(self)(self.schema, *super().__getitem__(key))
		return super().__getitem__(key)

	def __strip_common_suffix(self, value):
		value = DN(self.schema, value)
		minlen = min(len(self), len(value))
		for i in range(minlen):
			if self[-1 - i] != value[-1 - i]:
				return self[:-i or None], value[:-i or None]
		return self[:-minlen or None], value[:-minlen or None]

	def is_direct_child_of(self, base):
		'''Return whether self is a direct child of base

		:param base: parent DN
		:type base: DN
		:rtype: bool

		Example:

			>>> schema = schema.RFC4519_SCHEMA
			>>> dn1 = DN(schema, 'uid=jsmith,dc=example,dc=net')
			>>> dn2 = DN(schema, 'dc=example,dc=net')
			>>> dn3 = DN(schema, 'dc=net')
			>>> dn1.is_direct_child_of(dn2)
			True
			>>> dn1.is_direct_child_of(dn1) or dn1.is_direct_child_of(dn3)
			False

		'''
		rchild, rbase = self.__strip_common_suffix(DN(self.schema, base))
		return not rbase and len(rchild) == 1

	def in_subtree_of(self, base):
		'''Return whether self is in the subtree of base

		:param base: parent DN
		:type base: DN
		:rtype: bool

		Example:

			>>> schema = schema.RFC4519_SCHEMA
			>>> dn1 = DN(schema, 'uid=jsmith,dc=example,dc=net')
			>>> dn2 = DN(schema, 'dc=example,dc=net')
			>>> dn3 = DN(schema, 'dc=net')
			>>> dn1.in_subtree_of(dn1) and dn1.in_subtree_of(dn2) and dn1.in_subtree_of(dn3)
			True
			>>> dn2.in_subtree_of(dn1)
			False

		'''
		rchild, rbase = self.__strip_common_suffix(DN(self.schema, base)) # pylint: disable=unused-variable
		return not rbase

	@property
	def object_attribute(self):
		'''Attribute name of the first RDN. None if there are no RDNs or if the
		first RDN consists of more than one assertion.'''
		if len(self) == 0:
			return None
		return self[0].attribute # pylint: disable=no-member

	@property
	def object_attribute_type(self):
		''':any:`schema.AttributeType` of the first RDN. None if there are no RDNs
		or if the first RDN consists of more than one assertion.'''
		if len(self) == 0:
			return None
		return self[0].attribute_type # pylint: disable=no-member

	@property
	def object_value(self):
		'''Attribute value of the first RDN. None if there are no RDNs or if the
		first RDN consists of more than one assertion. Type of value depends on
		the syntax of the attribute type.'''
		if len(self) == 0:
			return None
		return self[0].value # pylint: disable=no-member

class DNWithUID(DN):
	'''Distinguished Name with an optional bit string

	Used to represent values of the "Name and Optional UID" syntax (see RFC4517)
	This syntax is used for e.g. the "uniqueMember" attribute type (RFC4519).

	If created without the optional bit string (uid) part, a regular DN object is
	returned.'''
	#:
	schema: typing.Any

	# pylint: disable=arguments-differ,no-member
	def __new__(cls, schema, dn, uid=None):
		if not uid:
			return dn
		if not re.fullmatch(r"'[01]*'B", uid):
			raise ValueError('Invalid uid value')
		obj = super().__new__(cls, schema, *dn)
		obj.uid = uid
		return obj

	@classmethod
	def from_str(cls, schema, expr):
		'''Parse string representation

		:param schema: Schema
		:type schema: schema.Schema
		:param expr: DN string representation with optional ``#``-separated bit
		             string part (e.g. ``0b1010``)
		:type expr: str
		:raises ValueError: if expr is invalid
		:returns: :any:`DNWithUID` if expr includes the optional bit string part,
		          :any:`DN` otherwise
		:rtype: DN or DNWithUID
		'''
		dn_part, uid_part = (expr.rsplit('#', 1) + [''])[:2]
		return cls(schema, DN.from_str(schema, dn_part), uid_part or None)

	def __str__(self):
		'''Return string representation

		:returns: Representation of self
		:rtype: str'''
		return super().__str__() + '#' + self.uid

	def __repr__(self):
		return '<ldapserver.DNWithUID %s>'%str(self)

	def __eq__(self, obj):
		return type(self) is type(obj) and super().__eq__(obj) and self.uid == obj.uid

	@property
	def dn(self):
		'''Return DN part as a regular :any:`DN` object'''
		return DN(self.schema, *self)

class RDN(tuple):
	'''Relative Distinguished Name consisting of one or more :class:`RDNAssertion` objects'''
	#:
	schema: typing.Any

	def __new__(cls, schema, *assertions, **kwargs):
		for assertion in assertions:
			if not isinstance(assertion, RDNAssertion):
				raise TypeError(f'Argument {repr(assertion)} is of type {repr(type(assertion))}, expected ldapserver.dn.RDNAssertion')
			if assertion.attribute_type.schema is not schema:
				raise ValueError('RDNAssertion has different schema')
		assertions = list(assertions)
		for key, value in kwargs.items():
			assertions.append(RDNAssertion(schema, key, value))
		if not assertions:
			raise ValueError('RDN must have at least one assertion')
		rdn = super().__new__(cls, assertions)
		rdn.schema = schema
		return rdn

	# Syntax definiton from RFC4514:
	# relativeDistinguishedName = attributeTypeAndValue *( PLUS attributeTypeAndValue )

	@classmethod
	def from_str(cls, schema, expr):
		'''Parse string representation of an RDN according to RFC 4514

		:param schema: Schema for the RDN
		:type schema: schema.Schema
		:param expr: RDN string representation
		:type expr: str
		:raises ValueError: if expr is invalid
		:returns: Parsed RDN
		:rtype: RDN'''
		assertions = []
		while expr:
			# attributeTypeAndValue may contain escape sequences including "\+".
			# Split off first token expr at "+" while ignoring "\+".
			match = re.match(r'^(([^+\\]|\\.)+)(\+|$)', expr)
			if not match:
				raise ValueError(f'Unrecognized token {expr!r}')
			expr = expr[match.end():]
			assertion_expr, _, _ = match.groups()
			assertions.append(RDNAssertion.from_str(schema, assertion_expr))
		return cls(schema, *assertions)

	def __str__(self):
		'''Return string representation of RDN according to RFC 4514

		:returns: Representation of self
		:rtype: str

		Example:

			>>> str(RDN(ou='Sales', cn='J.  Smith'))
			'ou=Sales+cn=J.  Smith'
		'''
		return '+'.join(map(str, self))

	def __repr__(self):
		return '<ldapserver.RDN %s>'%str(self)

	def __eq__(self, obj):
		return type(self) is type(obj) and set(self) == set(obj)

	def __ne__(self, obj):
		return not self == obj

	def __add__(self, value):
		if isinstance(value, RDN):
			return DN(self.schema, self, value)
		elif isinstance(value, DN):
			return DN(self.schema, self) + value
		else:
			raise TypeError(f'Can only add DN or RDN to RDN, not {type(value)}')

	@property
	def attribute(self):
		'''Attribute name of the contained assertion. None if the RDN consists of
		more than one assertion.'''
		if len(self) != 1:
			return None
		return self[0].attribute

	@property
	def attribute_type(self):
		'''Attribute type of the contained assertion. None if the RDN consists of
		more than one assertion.'''
		if len(self) != 1:
			return None
		return self[0].attribute_type

	@property
	def value(self):
		'''Attribute value of the contained assertion. None if the RDN consists of
		more than one assertion. Type of value depends on the syntax of the
		attribute type.'''
		if len(self) != 1:
			return None
		return self[0].value

DN_ESCAPED = (
	0x0022, # '"'
	0x002B, # '+'
	0x002C, # ','
	0x003B, # ';'
	0x003C, # '<'
	0x003E, # '>'
)
DN_SPECIAL = DN_ESCAPED + (
	0x0020, # ' '
	0x0023, # '#'
	0x003D, # '='
)
HEXDIGITS = (
	0x0030, # '0'
	0x0031, # '1'
	0x0032, # '2'
	0x0033, # '3'
	0x0034, # '4'
	0x0035, # '5'
	0x0036, # '6'
	0x0037, # '7'
	0x0038, # '8'
	0x0039, # '9'
	0x0041, # 'A'
	0x0042, # 'B'
	0x0043, # 'C'
	0x0044, # 'D'
	0x0045, # 'E'
	0x0046, # 'F'
	0x0061, # 'a'
	0x0062, # 'b'
	0x0063, # 'c'
	0x0064, # 'd'
	0x0065, # 'e'
	0x0066, # 'f'
)

class RDNAssertion:
	__slots__ = ['attribute', 'attribute_type', 'value', 'schema']
	#: Attribute name
	attribute: str
	#: :class:`schema.AttributeType`
	attribute_type: typing.Any
	#: Attribute value (type depends on the syntax of the attribute type)
	value: typing.Any
	#:
	schema: typing.Any

	def __init__(self, schema, attribute, value):
		try:
			super().__setattr__('attribute_type', schema.attribute_types[attribute])
		except KeyError as exc:
			raise ValueError('Invalid RDN attribute type: Attribute type undefined in schema') from exc
		super().__setattr__('attribute', attribute)
		if not self.attribute_type.equality:
			raise ValueError('Invalid RDN attribute type: Attribute type has no EQUALITY matching rule')
		super().__setattr__('value', value)

	# Syntax definiton from RFC4514 and 4512:
	#
	# attributeTypeAndValue = attributeType EQUALS attributeValue
	# attributeType = descr / numericoid
	# attributeValue = string / hexstring
	#
	# descr = ALPHA *( ALPHA / DIGIT / HYPHEN )
	# numericoid = number 1*( DOT number )
	# number = DIGIT / ( LDIGIT 1*DIGIT )
	#
	# ; The following characters are to be escaped when they appear
	# ; in the value to be encoded: ESC, one of <escaped>, leading
	# ; SHARP or SPACE, trailing SPACE, and NULL.
	# string = [ ( leadchar / pair ) [ *( stringchar / pair ) ( trailchar / pair ) ] ]
	#
	# leadchar = LUTF1 / UTFMB
	# LUTF1 = %x01-1F / %x21 / %x24-2A / %x2D-3A / %x3D / %x3F-5B / %x5D-7F
	#
	# trailchar = TUTF1 / UTFMB
	# TUTF1 = %x01-1F / %x21 / %x23-2A / %x2D-3A / %x3D / %x3F-5B / %x5D-7F
	#
	# stringchar = SUTF1 / UTFMB
	# SUTF1 = %x01-21 / %x23-2A / %x2D-3A / %x3D / %x3F-5B / %x5D-7F
	#
	# pair = ESC ( ESC / special / hexpair )
	# special = escaped / SPACE / SHARP / EQUALS
	# escaped = DQUOTE / PLUS / COMMA / SEMI / LANGLE / RANGLE
	#
	# hexstring = SHARP 1*hexpair
	# hexpair = HEX HEX

	@classmethod
	def from_str(cls, schema, expr):
		'''Parse string representation of an RDN assertion according to RFC 4514

		:param schema: Schema for the RDN assertion
		:type schema: schema.Schema
		:param expr: RDN assertion string representation
		:type expr: str
		:raises ValueError: if expr is invalid
		:returns: Parsed assertion
		:rtype: RDNAssertion'''
		attribute, escaped_value = expr.split('=', 1)
		if escaped_value.startswith('#'):
			# The "#..." form is used for unknown attribute types and those without
			# an LDAP string encoding. Supporting it would require us to somehow
			# handle the hex-encoded BER encoding of the data. We'll stay away from
			# this mess for now.
			raise ValueError('Hex-encoded RDN assertion values are not supported')
		escaped = False
		hexdigit = None
		encoded_value = b''
		for char in escaped_value:
			if hexdigit is not None:
				encoded_value += bytes.fromhex('%s%s'%(hexdigit, char))
				hexdigit = None
			elif escaped:
				if ord(char) in DN_SPECIAL + (b'\\'[0],):
					encoded_value += char.encode('utf8')
				elif ord(char) in HEXDIGITS:
					hexdigit = char
				else:
					raise ValueError('Invalid escape: \\%s'%char)
				escaped = False
			elif char == '\\':
				escaped = True
			else:
				encoded_value += char.encode('utf8')
		try:
			attribute_type = schema.attribute_types[attribute]
		except KeyError as exc:
			raise ValueError('Invalid RDN attribute type: Attribute type undefined in schema') from exc
		try:
			value = attribute_type.syntax.decode(encoded_value)
		except exceptions.LDAPInvalidAttributeSyntax as exc:
			raise ValueError('Invalid RDN assertion value') from exc
		return cls(schema, attribute, value)

	def __str__(self):
		'''Return string representation of the RDN assertion according to RFC 4514

		:returns: Representation of self
		:rtype: str'''
		encoded_value = self.attribute_type.syntax.encode(self.value)
		escaped_value = ''
		for index in range(len(encoded_value)):
			byte = encoded_value[index:index+1]
			if not byte.isascii() or not byte.decode().isprintable():
				escaped_value += '\\%02x'%byte[0]
			elif byte[0] in DN_ESCAPED + (b'\\'[0],):
				escaped_value += '\\' + byte.decode()
			else:
				escaped_value += byte.decode()
		if escaped_value.startswith(' ') or escaped_value.startswith('#'):
			escaped_value = '\\' + escaped_value
		if escaped_value.endswith(' '):
			escaped_value = escaped_value[:-1] + '\\' + escaped_value[-1]
		return '%s=%s'%(self.attribute, escaped_value)

	def __hash__(self):
		return hash(self.attribute_type.oid)

	def __repr__(self):
		return '<ldapserver.RDNAssertion %s>'%str(self)

	def __eq__(self, obj):
		return type(self) is type(obj) and self.attribute_type is obj.attribute_type and \
		       self.attribute_type.equality.match_equal([self.value], obj.value)

	def __ne__(self, obj):
		return not self == obj

	def __setattr__(self, *args):
		raise TypeError('RDNAssertion object is immutable')

	def __delattr__(self, *args):
		raise TypeError('RDNAssertion object is immutable')
