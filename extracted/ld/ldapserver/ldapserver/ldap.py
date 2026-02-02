import typing
from abc import ABC, abstractmethod
import enum

from . import asn1

class LDAPString(asn1.OctetString):
	@classmethod
	def from_ber(cls, data):
		raw, rest = super().from_ber(data)
		return raw.decode(), rest

	@classmethod
	def to_ber(cls, obj):
		if not isinstance(obj, str):
			raise TypeError()
		return super().to_ber(obj.encode())

class LDAPOID(LDAPString):
	pass

class AttributeValueAssertion(asn1.Sequence):
	SEQUENCE_FIELDS = [
		(LDAPString, 'attributeDesc', None, False),
		(asn1.OctetString, 'assertionValue', None, False),
	]

	attributeDesc: str
	assertionValue: bytes

def escape_filter_assertionvalue(value):
	allowed_bytes = b'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'+,-./:;<=>?@[\\]^_`{|}~ '
	res = []
	for byte in value:
		if byte not in allowed_bytes:
			res += b'\\%02X'%byte
		else:
			res.append(byte)
	return bytes(res).decode()

class Filter(asn1.Choice, ABC):
	'''Base class for filters in SEARCH operations

	All subclasses implement ``__str__`` according to RFC4515 "String
	Representation of Search Filters".'''

	@abstractmethod
	def __str__(self):
		raise NotImplementedError()

class FilterAnd(asn1.Wrapper, Filter):
	'''AND conjunction of multiple filters ``(&filters...)``

	Supports RFC4526: Empty AND filters (``(&)``) are considered valid and
	evaluate to TRUE.'''
	BER_TAG = (2, True, 0)
	WRAPPED_ATTRIBUTE = 'filters'
	WRAPPED_TYPE = asn1.Set
	WRAPPED_CLSATTRS = {'SET_TYPE': Filter}

	#:
	filters: typing.List[Filter]

	def __init__(self, filters=None):
		super().__init__(filters=filters)

	def __str__(self):
		return '(&%s)'%(''.join([str(subfilter) for subfilter in self.filters]))

class FilterOr(asn1.Wrapper, Filter):
	'''OR conjunction of multiple filters ``(|filters...)``

	Supports RFC4526: Empty OR filters (``(|)``) are considered valid and
	evaluate to FALSE.'''
	BER_TAG = (2, True, 1)
	WRAPPED_ATTRIBUTE = 'filters'
	WRAPPED_TYPE = asn1.Set
	WRAPPED_CLSATTRS = {'SET_TYPE': Filter}

	#:
	filters: typing.List[Filter]

	def __init__(self, filters=None):
		super().__init__(filters=filters)

	def __str__(self):
		return '(|%s)'%(''.join([str(subfilter) for subfilter in self.filters]))

class FilterNot(asn1.Sequence, Filter):
	'''Negation of a filter ``(!filter)``'''

	BER_TAG = (2, True, 2)
	SEQUENCE_FIELDS = [
		(Filter, 'filter', None, False)
	]

	#:
	filter: Filter

	# pylint: disable=redefined-builtin
	def __init__(self, filter=None):
		super().__init__(filter=filter)

	def __str__(self):
		return '(!%s)'%str(self.filter)

class FilterEqual(asn1.Sequence, Filter):
	'''Attribute equal filter ``(attribute=value)``'''
	BER_TAG = (2, True, 3)
	SEQUENCE_FIELDS = [
		(LDAPString, 'attribute', None, False),
		(asn1.OctetString, 'value', None, False)
	]

	#:
	attribute: str
	#:
	value: bytes

	def __init__(self, attribute=None, value=None):
		super().__init__(attribute=attribute, value=value)

	def __str__(self):
		return '(%s=%s)'%(self.attribute, escape_filter_assertionvalue(self.value))

class Substring(asn1.Choice, ABC):
	pass

class InitialSubstring(asn1.Wrapper, Substring):
	BER_TAG = (2, False, 0)

	WRAPPED_ATTRIBUTE = 'value'
	WRAPPED_TYPE = asn1.OctetString
	WRAPPED_DEFAULT = b''

class AnySubstring(asn1.Wrapper, Substring):
	BER_TAG = (2, False, 1)

	WRAPPED_ATTRIBUTE = 'value'
	WRAPPED_TYPE = asn1.OctetString
	WRAPPED_DEFAULT = b''

class FinalSubstring(asn1.Wrapper, Substring):
	BER_TAG = (2, False, 2)

	WRAPPED_ATTRIBUTE = 'value'
	WRAPPED_TYPE = asn1.OctetString
	WRAPPED_DEFAULT = b''

class Substrings(asn1.SequenceOf):
	SET_TYPE = Substring

class FilterSubstrings(asn1.Sequence, Filter):
	'''Attribute substrings filter ``(attribute=initial*any1*any2*final)``'''
	BER_TAG = (2, True, 4)
	SEQUENCE_FIELDS = [
		(LDAPString, 'attribute', None, False),
		(Substrings, 'substrings', lambda: [], False)
	]

	#:
	attribute: str
	substrings: typing.List[Substring]

	@property
	def initial_substring(self):
		'''Initial substring (:any:`bytes`). None if there is no initial substring or if the filter is invalid.'''
		results = [substring.value for substring in self.substrings if isinstance(substring, InitialSubstring)]
		if len(results) != 1:
			return None
		return results[0]

	@property
	def any_substrings(self):
		'''List of "any" substrings (list of :any:`bytes`, may be empty)'''
		return [substring.value for substring in self.substrings if isinstance(substring, AnySubstring)]

	@property
	def final_substring(self):
		'''Final substring (:any:`bytes`). None if there is no final substring or if the filter is invalid.'''
		results = [substring.value for substring in self.substrings if isinstance(substring, FinalSubstring)]
		if len(results) != 1:
			return None
		return results[0]

	def __str__(self):
		substrings = [self.initial_substring or b''] + self.any_substrings + [self.final_substring or b'']
		value = '*'.join(map(escape_filter_assertionvalue, substrings))
		return f'({self.attribute}={value})'

class FilterGreaterOrEqual(asn1.Sequence, Filter):
	'''Attribute greater or equal filter ``(attribute>=value)``'''
	BER_TAG = (2, True, 5)
	SEQUENCE_FIELDS = [
		(LDAPString, 'attribute', None, False),
		(asn1.OctetString, 'value', None, False)
	]

	attribute: str
	value: bytes

	def __init__(self, attribute=None, value=None):
		super().__init__(attribute=attribute, value=value)

	def __str__(self):
		return '(%s>=%s)'%(self.attribute, escape_filter_assertionvalue(self.value))

class FilterLessOrEqual(asn1.Sequence, Filter):
	'''Attribute less or equal filter ``(attribute<=value)``'''
	BER_TAG = (2, True, 6)
	SEQUENCE_FIELDS = [
		(LDAPString, 'attribute', None, False),
		(asn1.OctetString, 'value', None, False)
	]

	#:
	attribute: str
	#:
	value: bytes

	def __init__(self, attribute=None, value=None):
		super().__init__(attribute=attribute, value=value)

	def __str__(self):
		return '(%s<=%s)'%(self.attribute, escape_filter_assertionvalue(self.value))

class FilterPresent(asn1.Wrapper, Filter):
	'''Attribute present filter ``(attribute=*)``'''
	BER_TAG = (2, False, 7)
	WRAPPED_ATTRIBUTE = 'attribute'
	WRAPPED_TYPE = LDAPString
	WRAPPED_DEFAULT = None

	#:
	attribute: str

	def __init__(self, attribute=None):
		super().__init__(attribute=attribute)

	def __str__(self):
		return '(%s=*)'%(self.attribute)

class FilterApproxMatch(asn1.Sequence, Filter):
	'''Attribute approximately equal filter ``(attribute~=value)``'''
	BER_TAG = (2, True, 8)
	SEQUENCE_FIELDS = [
		(LDAPString, 'attribute', None, False),
		(asn1.OctetString, 'value', None, False)
	]

	#:
	attribute: str
	#:
	value: bytes

	def __init__(self, attribute=None, value=None):
		super().__init__(attribute=attribute, value=value)

	def __str__(self):
		return '(%s~=%s)'%(self.attribute, escape_filter_assertionvalue(self.value))

class FilterExtensibleMatch(asn1.Sequence, Filter):
	'''Extensible match filter ``(attribute:caseExactMatch:=value)``'''
	BER_TAG = (2, True, 9)
	SEQUENCE_FIELDS = [
		(asn1.retag(LDAPString, (2, False, 1)), 'matchingRule', None, True),
		(asn1.retag(LDAPString, (2, False, 2)), 'type', None, True),
		(asn1.retag(asn1.OctetString, (2, False, 3)), 'matchValue', None, False),
		(asn1.retag(asn1.Boolean, (2, False, 4)), 'dnAttributes', None, True),
	]

	#: Matching rule OID or short descriptive name (optional, str or None)
	matchingRule: str
	#: Attribute type OID or short descriptive name (optional, str or None)
	type: str
	#: Assertion value (bytes, encoded with LDAP-specific encoding according to matching rule syntax)
	matchValue: bytes
	#: Apply matching to all RDN assertions in addition to attribute values
	#: (e.g. ``(dc:dn:=example)`` matches ``cn=test,dc=example,dc=com`` even
	#: if it has no ``dc`` attribute, because ``dc=example`` is part of its DN)
	dnAttributes: bool

	def __str__(self):
		key = ''
		if self.type is not None:
			key += self.type
		if self.dnAttributes:
			key += ':dn'
		if self.matchingRule is not None:
			key += ':' + self.matchingRule
		return '(%s:=%s)'%(key, escape_filter_assertionvalue(self.matchValue))

class SearchScope(enum.Enum):
	''':any:`enum.Enum` of `scope` values in SEARCH operations'''
	# pylint: disable=invalid-name
	#: Search is constrained to the base object
	baseObject = 0
	#: Search is constrained to the immediate subordinates of the base object
	singleLevel = 1
	#: Search is constrained to the base object and to all its subordinates
	wholeSubtree = 2

class DerefAliases(enum.Enum):
	# pylint: disable=invalid-name
	neverDerefAliases = 0
	derefInSearching = 1
	derefFindingBaseObj = 2
	derefAlways = 3

class LDAPResultCode(enum.Enum):
	# pylint: disable=invalid-name
	success                      = 0
	operationsError              = 1
	protocolError                = 2
	timeLimitExceeded            = 3
	sizeLimitExceeded            = 4
	compareFalse                 = 5
	compareTrue                  = 6
	authMethodNotSupported       = 7
	strongerAuthRequired         = 8
	# -- 9 reserved --
	referral                     = 10
	adminLimitExceeded           = 11
	unavailableCriticalExtension = 12
	confidentialityRequired      = 13
	saslBindInProgress           = 14
	noSuchAttribute              = 16
	undefinedAttributeType       = 17
	inappropriateMatching        = 18
	constraintViolation          = 19
	attributeOrValueExists       = 20
	invalidAttributeSyntax       = 21
	# -- 22-31 unused --
	noSuchObject                 = 32
	aliasProblem                 = 33
	invalidDNSyntax              = 34
	# -- 35 reserved for undefined isLeaf --
	aliasDereferencingProblem    = 36
	# -- 37-47 unused --
	inappropriateAuthentication  = 48
	invalidCredentials           = 49
	insufficientAccessRights     = 50
	busy                         = 51
	unavailable                  = 52
	unwillingToPerform           = 53
	loopDetect                   = 54
	# -- 55-63 unused --
	namingViolation              = 64
	objectClassViolation         = 65
	notAllowedOnNonLeaf          = 66
	notAllowedOnRDN              = 67
	entryAlreadyExists           = 68
	objectClassModsProhibited    = 69
	# -- 70 reserved for CLDAP --
	affectsMultipleDSAs          = 71
	# -- 72-79 unused --
	other                        = 80

class LDAPResult(asn1.Sequence):
	BER_TAG = (5, True, 1)
	SEQUENCE_FIELDS = [
		(asn1.wrapenum(LDAPResultCode), 'resultCode', LDAPResultCode.success, False),
		(LDAPString, 'matchedDN', '', False),
		(LDAPString, 'diagnosticMessage', '', False),
	]

	resultCode: LDAPResultCode
	matchedDN: str
	diagnosticMessage: str

class AttributeSelection(asn1.SequenceOf):
	SET_TYPE = LDAPString

class AuthenticationChoice(asn1.Choice):
	pass

class SimpleAuthentication(asn1.Wrapper, AuthenticationChoice):
	BER_TAG = (2, False, 0)
	WRAPPED_ATTRIBUTE = 'password'
	WRAPPED_TYPE = asn1.OctetString
	WRAPPED_DEFAULT = b''

	password: bytes

	def __repr__(self):
		if not self.password:
			return '<%s(EMPTY PASSWORD)>'%(type(self).__name__)
		return '<%s(PASSWORD HIDDEN)>'%(type(self).__name__)

class SaslCredentials(asn1.Sequence, AuthenticationChoice):
	BER_TAG = (2, True, 3)
	SEQUENCE_FIELDS = [
		(LDAPString, 'mechanism', None, False),
		(asn1.OctetString, 'credentials', None, True),
	]

	mechanism: str
	credentials: bytes

class AttributeValueSet(asn1.Set):
	SET_TYPE = asn1.OctetString

class PartialAttribute(asn1.Sequence):
	SEQUENCE_FIELDS = [
		(LDAPString, 'type', None, False),
		(AttributeValueSet, 'vals', lambda: [], False),
	]

	#:
	type: str
	#:
	vals: typing.List[bytes]

class PartialAttributeList(asn1.SequenceOf):
	SET_TYPE = PartialAttribute

class Attribute(asn1.Sequence):
	# Constrain: vals must not be empty
	SEQUENCE_FIELDS = [
		(LDAPString, 'type', None, False),
		(AttributeValueSet, 'vals', lambda: [], False),
	]

	type: str
	vals: typing.List[bytes]

class AttributeList(asn1.SequenceOf):
	SET_TYPE = Attribute

class ProtocolOp(asn1.Choice):
	pass

class BindRequest(asn1.Sequence, ProtocolOp):
	BER_TAG = (1, True, 0)
	SEQUENCE_FIELDS = [
		(asn1.Integer, 'version', 3, False),
		(LDAPString, 'name', '', False),
		(AuthenticationChoice, 'authentication', lambda: SimpleAuthentication(), False) # pylint: disable=unnecessary-lambda
	]

	version: int
	name: str
	authentication: AuthenticationChoice

class BindResponse(asn1.Sequence, ProtocolOp):
	BER_TAG = (1, True, 1)
	SEQUENCE_FIELDS = [
		(asn1.wrapenum(LDAPResultCode), 'resultCode', None, False),
		(LDAPString, 'matchedDN', '', False),
		(LDAPString, 'diagnosticMessage', '', False),
		(asn1.retag(asn1.OctetString, (2, False, 7)), 'serverSaslCreds', None, True)
	]

	resultCode: LDAPResultCode
	matchedDN: str
	diagnosticMessage: str
	serverSaslCreds: bytes

class UnbindRequest(asn1.Sequence, ProtocolOp):
	BER_TAG = (1, False, 2)

class SearchRequest(asn1.Sequence, ProtocolOp):
	BER_TAG = (1, True, 3)
	SEQUENCE_FIELDS = [
		(LDAPString, 'baseObject', '', False),
		(asn1.wrapenum(SearchScope), 'scope', SearchScope.wholeSubtree, False),
		(asn1.wrapenum(DerefAliases), 'derefAliases', DerefAliases.neverDerefAliases, False),
		(asn1.Integer, 'sizeLimit', 0, False),
		(asn1.Integer, 'timeLimit', 0, False),
		(asn1.Boolean, 'typesOnly', False, False),
		(Filter, 'filter', lambda: FilterPresent('objectClass'), False),
		(AttributeSelection, 'attributes', lambda: [], False)
	]

	baseObject: str
	scope: SearchScope
	derefAliases: DerefAliases
	sizeLimit: int
	timeLimit: int
	typesOnly: bool
	filter: Filter
	attributes: typing.List[str]

	@classmethod
	def from_ber(cls, data):
		return super().from_ber(data)

class SearchResultEntry(asn1.Sequence, ProtocolOp):
	BER_TAG = (1, True, 4)
	SEQUENCE_FIELDS = [
		(LDAPString, 'objectName', '', False),
		(PartialAttributeList, 'attributes', lambda: [], False),
	]

	#:
	objectName: str
	#:
	attributes: typing.List[PartialAttribute]

class SearchResultDone(LDAPResult, ProtocolOp):
	BER_TAG = (1, True, 5)

class ModifyOperation(enum.Enum):
	# pylint: disable=invalid-name
	add = 0
	delete = 1
	replace = 2

class ModifyChange(asn1.Sequence):
	SEQUENCE_FIELDS = [
		(asn1.wrapenum(ModifyOperation), 'operation', None, False),
		(PartialAttribute, 'modification', None, False),
	]
	operation: ModifyOperation
	modification: PartialAttribute

class ModifyChanges(asn1.SequenceOf):
	SET_TYPE = ModifyChange

class ModifyRequest(asn1.Sequence, ProtocolOp):
	BER_TAG = (1, True, 6)
	SEQUENCE_FIELDS = [
		(LDAPString, 'object', None, False),
		(ModifyChanges, 'changes', None, False),
	]
	object: str
	changes: typing.List[ModifyChange]

class ModifyResponse(LDAPResult, ProtocolOp):
	BER_TAG = (1, True, 7)

class AddRequest(asn1.Sequence, ProtocolOp):
	BER_TAG = (1, True, 8)
	SEQUENCE_FIELDS = [
		(LDAPString, 'entry', None, False),
		(AttributeList, 'attributes', None, False),
	]
	entry: str
	attributes: Attribute

class AddResponse(LDAPResult, ProtocolOp):
	BER_TAG = (1, True, 9)

class DelRequest(asn1.Wrapper, ProtocolOp):
	BER_TAG = (1, False, 10)
	WRAPPED_ATTRIBUTE = 'dn'
	WRAPPED_TYPE = LDAPString
	WRAPPED_DEFAULT = None

	dn: str

class DelResponse(LDAPResult, ProtocolOp):
	BER_TAG = (1, True, 11)

class ModifyDNRequest(asn1.Sequence, ProtocolOp):
	BER_TAG = (1, True, 12)
	SEQUENCE_FIELDS = [
		(LDAPString, 'entry', None, False),
		(LDAPString, 'newrdn', None, False),
		(asn1.Boolean, 'deleteoldrdn', None, False),
		(asn1.retag(LDAPString, (2, False, 0)), 'newSuperior', None, True),
	]

	entry: str
	newrdn: str
	deleteoldrdn: bool
	newSuperior: str

class ModifyDNResponse(LDAPResult, ProtocolOp):
	BER_TAG = (1, True, 13)

class CompareRequest(asn1.Sequence, ProtocolOp):
	BER_TAG = (1, True, 14)
	SEQUENCE_FIELDS = [
		(LDAPString, 'entry', None, False),
		(AttributeValueAssertion, 'ava', None, False),
	]

	entry: str
	ava: AttributeValueAssertion

class CompareResponse(LDAPResult, ProtocolOp):
	BER_TAG = (1, True, 15)

class AbandonRequest(asn1.Wrapper, ProtocolOp):
	BER_TAG = (1, False, 16)
	WRAPPED_ATTRIBUTE = 'messageID'
	WRAPPED_TYPE = asn1.Integer
	WRAPPED_DEFAULT = None

	messageID: int

class ExtendedRequest(asn1.Sequence, ProtocolOp):
	BER_TAG = (1, True, 23)
	SEQUENCE_FIELDS = [
		(asn1.retag(LDAPOID, (2, False, 0)), 'requestName', None, True),
		(asn1.retag(asn1.OctetString, (2, False, 1)), 'requestValue', None, True),
	]

	requestName: str
	requestValue: bytes

class ExtendedResponse(asn1.Sequence, ProtocolOp):
	BER_TAG = (1, True, 24)
	SEQUENCE_FIELDS = [
		(asn1.wrapenum(LDAPResultCode), 'resultCode', None, False),
		(LDAPString, 'matchedDN', '', False),
		(LDAPString, 'diagnosticMessage', '', False),
		(asn1.retag(LDAPOID, (2, False, 10)), 'responseName', None, True),
		(asn1.retag(asn1.OctetString, (2, False, 11)), 'responseValue', None, True),
	]

	resultCode: LDAPResultCode
	matchedDN: str
	diagnosticMessage: str
	responseName: str
	responseValue: bytes

class IntermediateResponse(asn1.Sequence, ProtocolOp):
	BER_TAG = (1, True, 25)
	SEQUENCE_FIELDS = [
		(asn1.retag(LDAPOID, (2, False, 0)), 'responseName', None, True),
		(asn1.retag(asn1.OctetString, (2, False, 1)), 'responseValue', None, True),
	]

	responseName: str
	responseValue: bytes

class Control(asn1.Sequence):
	SEQUENCE_FIELDS = [
		(LDAPOID, 'controlType', None, False),
		(asn1.Boolean, 'criticality', None, True),
		(asn1.OctetString, 'controlValue', None, True),
	]

	controlType: str
	criticality: bool
	controlValue: bytes

class Controls(asn1.SequenceOf):
	BER_TAG = (2, True, 0)
	SET_TYPE = Control

class LDAPMessage(asn1.Sequence):
	SEQUENCE_FIELDS = [
		(asn1.Integer, 'messageID', None, False),
		(ProtocolOp, 'protocolOp', None, False),
		(Controls, 'controls', None, True)
	]

	messageID: int
	protocolOp: ProtocolOp
	controls: typing.List[Control]

class ShallowLDAPMessage(asn1.BERType):
	BER_TAG = (0, True, 16)
	# pylint: disable=invalid-name

	messageID: int
	protocolOpType: typing.Type[ProtocolOp]
	data: bytes

	def __init__(self, messageID=None, protocolOpType=None, data=None):
		self.messageID = messageID
		self.protocolOpType = protocolOpType
		self.data = data

	def decode(self):
		return LDAPMessage.from_ber(self.data)

	@classmethod
	def from_ber(cls, data):
		seq, rest = asn1.decode_ber(data)
		data = data[:len(data)-len(rest)]
		if seq.tag != cls.BER_TAG:
			raise ValueError()
		content = seq.content
		messageID, content = asn1.Integer.from_ber(content)
		op, content = asn1.decode_ber(content)
		for subcls in ProtocolOp.__subclasses__():
			if subcls.BER_TAG == op.tag:
				return cls(messageID, subcls, data), rest
		return cls(messageID, None, data), rest

	@classmethod
	def to_ber(cls, obj):
		if not isinstance(obj, cls):
			raise TypeError()
		return obj.data

# StartTLS Extended Operation (RFC4511)
STARTTLS_OID = '1.3.6.1.4.1.1466.20037'

# "Who am I?" Extended Operation (RFC4532)
WHOAMI_OID = '1.3.6.1.4.1.4203.1.11.3'

# Password Modify Extended Operation (RFC3062)
PASSWORD_MODIFY_OID = '1.3.6.1.4.1.4203.1.11.1'

class PasswdModifyRequestValue(asn1.Sequence):
	SEQUENCE_FIELDS = [
		(asn1.retag(LDAPString, (2, False, 0)), 'userIdentity', None, True),
		(asn1.retag(asn1.OctetString, (2, False, 1)), 'oldPasswd', None, True),
		(asn1.retag(asn1.OctetString, (2, False, 2)), 'newPasswd', None, True),
	]

	userIdentity: str
	oldPasswd: bytes
	newPasswd: bytes

class PasswdModifyResponseValue(asn1.Sequence):
	SEQUENCE_FIELDS = [
		(asn1.retag(asn1.OctetString, (2, False, 0)), 'genPasswd', None, True),
	]

	genPasswd: bytes

# LDAP Control Extension for Simple Paged Results Manipulation (RFC2696)
PAGED_RESULTS_OID = '1.2.840.113556.1.4.319'

class PagedResultsValue(asn1.Sequence):
	SEQUENCE_FIELDS = [
		(asn1.Integer, 'size', 0, False),
		(asn1.OctetString, 'cookie', b'', False)
	]

	size: int
	cookie: bytes

# LDAP All Operational Attributes (RFC3673)
ALL_OPERATIONAL_ATTRS_OID = '1.3.6.1.4.1.4203.1.5.1'

# LDAP Absolute True and False Filters (RFC4526)
ABSOLUTE_TRUE_FALSE_OID = '1.3.6.1.4.1.4203.1.5.3'
