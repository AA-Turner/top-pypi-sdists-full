import re
import datetime

from .definitions import SyntaxDefinition
from .. import dn, exceptions

class BytesSyntaxDefinition(SyntaxDefinition):
	def encode(self, schema, value):
		return value

	def decode(self, schema, raw_value):
		return raw_value

class StringSyntaxDefinition(SyntaxDefinition):
	def __init__(self, oid, encoding='utf-8', re_pattern='.*', **kwargs):
		super().__init__(oid, **kwargs)
		self.encoding = encoding
		self.re_pattern = re.compile(re_pattern)

	def encode(self, schema, value):
		return value.encode(self.encoding)

	def decode(self, schema, raw_value):
		try:
			value = raw_value.decode(self.encoding)
		except UnicodeDecodeError as exc:
			raise exceptions.LDAPInvalidAttributeSyntax(exc.reason) from exc
		if not re.fullmatch(self.re_pattern, value):
			raise exceptions.LDAPInvalidAttributeSyntax()
		return value

class IntegerSyntaxDefinition(StringSyntaxDefinition):
	def __init__(self, oid, **kwargs):
		super().__init__(oid, encoding='ascii', re_pattern='([0-9]|-?[1-9][0-9]+)', **kwargs)

	def encode(self, schema, value):
		return super().encode(schema, str(value))

	def decode(self, schema, raw_value):
		try:
			return int(super().decode(schema, raw_value))
		except ValueError as exc:
			raise exceptions.LDAPInvalidAttributeSyntax() from exc

class SchemaElementSyntaxDefinition(SyntaxDefinition):
	def encode(self, schema, value):
		return str(value).encode('utf8')

class BooleanSyntaxDefinition(SyntaxDefinition):
	def encode(self, schema, value):
		return b'TRUE' if value else b'FALSE'

	def decode(self, schema, raw_value):
		if raw_value == b'TRUE':
			return True
		elif raw_value == b'FALSE':
			return False
		else:
			raise exceptions.LDAPInvalidAttributeSyntax()

class DNSyntaxDefinition(SyntaxDefinition):
	def encode(self, schema, value):
		return str(value).encode('utf8')

	def decode(self, schema, raw_value):
		try:
			return dn.DN.from_str(schema, raw_value.decode('utf8'))
		except (UnicodeDecodeError, TypeError, ValueError) as exc:
			raise exceptions.LDAPInvalidAttributeSyntax() from exc

class NameAndOptionalUIDSyntaxDefinition(StringSyntaxDefinition):
	def encode(self, schema, value):
		return str(value).encode('utf8')

	def decode(self, schema, raw_value):
		try:
			return dn.DNWithUID.from_str(schema, raw_value.decode('utf8'))
		except (UnicodeDecodeError, TypeError, ValueError) as exc:
			raise exceptions.LDAPInvalidAttributeSyntax() from exc

class GeneralizedTimeSyntaxDefinition(SyntaxDefinition):
	def encode(self, schema, value):
		if value.microsecond:
			str_value = value.strftime('%Y%m%d%H%M%S.%f')
		elif value.second:
			str_value = value.strftime('%Y%m%d%H%M%S')
		else:
			str_value = value.strftime('%Y%m%d%H%M')
		if value.tzinfo == datetime.timezone.utc:
			str_value += 'Z'
		elif value.tzinfo is not None:
			delta_seconds = value.tzinfo.utcoffset(value).total_seconds()
			if delta_seconds < 0:
				str_value += '-'
				delta_seconds = -delta_seconds
			else:
				str_value += '+'
			hour = delta_seconds // 3600
			minute = (delta_seconds % 3600) // 60
			str_value += '%02d%02d'%(hour, minute)
		return str_value.encode('ascii')

	def decode(self, schema, raw_value):
		try:
			raw_value = raw_value.decode('utf8')
		except UnicodeDecodeError as exc:
			raise exceptions.LDAPInvalidAttributeSyntax() from exc
		match = re.fullmatch(r'([0-9]{10})(|[0-9]{2}|[0-9]{4})(|[,.][0-9]+)(Z|[+-][0-9]{2}|[+-][0-9]{4})', raw_value)
		if match is None:
			raise exceptions.LDAPInvalidAttributeSyntax()
		main, minute_second, fraction, timezone = match.groups()
		fraction = float('0.' + (fraction[1:] or '0'))
		result = datetime.datetime.strptime(main, '%Y%m%d%H')
		if not minute_second:
			result += datetime.timedelta(hours=fraction)
		if len(minute_second) == 2:
			result += datetime.timedelta(minutes=int(minute_second)+fraction)
		elif len(minute_second) == 4:
			minute = minute_second[:2]
			second = minute_second[2:4]
			result += datetime.timedelta(minutes=int(minute), seconds=int(second)+fraction)
		if timezone == 'Z':
			result = result.replace(tzinfo=datetime.timezone.utc)
		elif timezone:
			sign, hour, minute = timezone[0], timezone[1:3], (timezone[3:5] or '00')
			delta = datetime.timedelta(hours=int(hour), minutes=int(minute))
			if sign == '+':
				result = result.replace(tzinfo=datetime.timezone(delta))
			else:
				result = result.replace(tzinfo=datetime.timezone(-delta))
		return result

class PostalAddressSyntaxDefinition(SyntaxDefinition):
	# 3.3.28.  Postal Address
	#
	# A value of the Postal Address syntax is a sequence of strings of one
	# or more arbitrary UCS characters, which form an address in a physical
	# mail system.
	#
	# The LDAP-specific encoding of a value of this syntax is defined by
	# the following ABNF:
	#
	#
	#   PostalAddress = line *( DOLLAR line )
	#   line          = 1*line-char
	#   line-char     = %x00-23
	#                   / (%x5C "24")  ; escaped "$"
	#                   / %x25-5B
	#                   / (%x5C "5C")  ; escaped "\"
	#                   / %x5D-7F
	#                   / UTFMB
	#
	# Each character string (i.e., <line>) of a postal address value is
	# encoded as a UTF-8 [RFC3629] string, except that "\" and "$"
	# characters, if they occur in the string, are escaped by a "\"
	# character followed by the two hexadecimal digit code for the
	# character.  The <DOLLAR> and <UTFMB> rules are defined in [RFC4512].
	#
	# Many servers limit the postal address to no more than six lines of no
	# more than thirty characters each.
	#
	#   Example:
	#      1234 Main St.$Anytown, CA 12345$USA
	#      \241,000,000 Sweepstakes$PO Box 1000000$Anytown, CA 12345$USA
	#
	# The LDAP definition for the Postal Address syntax is:
	#
	#   ( 1.3.6.1.4.1.1466.115.121.1.41 DESC 'Postal Address' )
	#
	# This syntax corresponds to the PostalAddress ASN.1 type from [X.520];
	# that is
	#
	#   PostalAddress ::= SEQUENCE SIZE(1..ub-postal-line) OF
	#       DirectoryString { ub-postal-string }
	#
	# The values of ub-postal-line and ub-postal-string (both integers) are
	# implementation defined.  Non-normative definitions appear in [X.520].

	# Native values are lists of str
	def encode(self, schema, value):
		return '$'.join([line.replace('\\', '\\5C').replace('$', '\\24') for line in value]).encode('utf8')

	def decode(self, schema, raw_value):
		return [line.replace('\\24', '$').replace('\\5C', '\\') for line in raw_value.decode('utf8').split('$')]

class SubstringAssertionSyntaxDefinition(SyntaxDefinition):
	# Native values are lists of str
	def encode(self, schema, value):
		raise NotImplementedError()

	def decode(self, schema, raw_value):
		value = raw_value.decode('utf8')
		if '*' not in value:
			raise exceptions.LDAPInvalidAttributeSyntax()
		substrings = [substring.replace('\\2A', '*').replace('\\5C', '\\') for substring in value.split('*')]
		initial_substring, *any_substring, final_substring = substrings
		return (initial_substring or None, any_substring, final_substring or None)

class UTCTimeSyntaxDefinition(SyntaxDefinition):
	def encode(self, schema, value):
		if value.second:
			str_value = value.strftime('%y%m%d%H%M%S')
		else:
			str_value = value.strftime('%y%m%d%H%M')
		if value.tzinfo == datetime.timezone.utc:
			str_value += 'Z'
		elif value.tzinfo is not None:
			delta_seconds = value.tzinfo.utcoffset(value).total_seconds()
			if delta_seconds < 0:
				str_value += '-'
				delta_seconds = -delta_seconds
			else:
				str_value += '+'
			hour = delta_seconds // 3600
			minute = (delta_seconds % 3600) // 60
			str_value += '%02d%02d'%(hour, minute)
		return str_value.encode('ascii')

	def decode(self, schema, raw_value):
		try:
			raw_value = raw_value.decode('utf8')
		except UnicodeDecodeError as exc:
			raise exceptions.LDAPInvalidAttributeSyntax() from exc
		match = re.fullmatch(r'([0-9]{10})(|[0-9]{2})(|Z|[+-][0-9]{4})', raw_value)
		if match is None:
			raise exceptions.LDAPInvalidAttributeSyntax()
		main, seconds, timezone = match.groups()
		result = datetime.datetime.strptime(main, '%y%m%d%H%M')
		if seconds:
			result = result.replace(second=int(seconds))
		if timezone == 'Z':
			result = result.replace(tzinfo=datetime.timezone.utc)
		elif timezone:
			sign, hour, minute = timezone[0], timezone[1:3], timezone[3:5]
			delta = datetime.timedelta(hours=int(hour), minutes=int(minute))
			if sign == '+':
				result = result.replace(tzinfo=datetime.timezone(delta))
			else:
				result = result.replace(tzinfo=datetime.timezone(-delta))
		return result

class StubSyntaxDefinition(SyntaxDefinition):
	def encode(self, schema, value):
		raise NotImplementedError()

# RFC2252 (deprecated legacy syntaxes required for some schemas)
Binary =  BytesSyntaxDefinition('1.3.6.1.4.1.1466.115.121.1.5', desc='Binary')

# RFC4517
Fax = BytesSyntaxDefinition('1.3.6.1.4.1.1466.115.121.1.23', desc='Fax')
JPEG = BytesSyntaxDefinition('1.3.6.1.4.1.1466.115.121.1.28', desc='JPEG')
OctetString = BytesSyntaxDefinition('1.3.6.1.4.1.1466.115.121.1.40', desc='Octet String')
DirectoryString = StringSyntaxDefinition('1.3.6.1.4.1.1466.115.121.1.15', desc='Directory String', re_pattern='.+')
IA5String = StringSyntaxDefinition('1.3.6.1.4.1.1466.115.121.1.26', desc='IA5 String', encoding='ascii', extra_compatability_tags=DirectoryString.compatability_tags)
PrintableString = StringSyntaxDefinition('1.3.6.1.4.1.1466.115.121.1.44', desc='Printable String', encoding='ascii', re_pattern='[A-Za-z0-9\'()+,.=/:? -]*', extra_compatability_tags=IA5String.compatability_tags)
CountryString = StringSyntaxDefinition('1.3.6.1.4.1.1466.115.121.1.11', desc='Country String', encoding='ascii', re_pattern='[A-Za-z0-9\'()+,.=/:? -]{2}', extra_compatability_tags=PrintableString.compatability_tags)
TelephoneNumber = StringSyntaxDefinition('1.3.6.1.4.1.1466.115.121.1.50', desc='Telephone Number', encoding='ascii', re_pattern='[A-Za-z0-9\'()+,.=/:? -]*', extra_compatability_tags=PrintableString.compatability_tags)
OID = StringSyntaxDefinition('1.3.6.1.4.1.1466.115.121.1.38', desc='OID', encoding='ascii', re_pattern=r'[0-9]+(\.[0-9])*|[A-Za-z][A-Za-z0-9-]*')
BitString = StringSyntaxDefinition('1.3.6.1.4.1.1466.115.121.1.6', desc='Bit String', encoding='ascii', re_pattern='\'[01]*\'B')
DeliveryMethod = StringSyntaxDefinition('1.3.6.1.4.1.1466.115.121.1.14', desc='Delivery Method')
FacsimileTelephoneNumber = StringSyntaxDefinition('1.3.6.1.4.1.1466.115.121.1.22', desc='Facsimile Telephone Number')
EnhancedGuide = StringSyntaxDefinition('1.3.6.1.4.1.1466.115.121.1.21', desc='Enhanced Guide')
Guide = StringSyntaxDefinition('1.3.6.1.4.1.1466.115.121.1.25', desc='Guide')
NumericString = StringSyntaxDefinition('1.3.6.1.4.1.1466.115.121.1.36', desc='Numeric String', encoding='ascii', re_pattern='[0-9 ]+')
OtherMailbox = StringSyntaxDefinition('1.3.6.1.4.1.1466.115.121.1.39', desc='Other Mailbox')
TeletexTerminalIdentifier = StringSyntaxDefinition('1.3.6.1.4.1.1466.115.121.1.51', desc='Teletex Terminal Identifier')
TelexNumber = StringSyntaxDefinition('1.3.6.1.4.1.1466.115.121.1.52', desc='Telex Number')
INTEGER = IntegerSyntaxDefinition('1.3.6.1.4.1.1466.115.121.1.27', desc='INTEGER')
AttributeTypeDescription = SchemaElementSyntaxDefinition('1.3.6.1.4.1.1466.115.121.1.3', desc='Attribute Type Description', extra_compatability_tags=['FirstComponent:'+OID.oid])
LDAPSyntaxDescription = SchemaElementSyntaxDefinition('1.3.6.1.4.1.1466.115.121.1.54', desc='LDAP Syntax Description', extra_compatability_tags=['FirstComponent:'+OID.oid])
MatchingRuleDescription = SchemaElementSyntaxDefinition('1.3.6.1.4.1.1466.115.121.1.30', desc='Matching Rule Description', extra_compatability_tags=['FirstComponent:'+OID.oid])
MatchingRuleUseDescription = SchemaElementSyntaxDefinition('1.3.6.1.4.1.1466.115.121.1.31', desc='Matching Rule Use Description', extra_compatability_tags=['FirstComponent:'+OID.oid])
ObjectClassDescription = SchemaElementSyntaxDefinition('1.3.6.1.4.1.1466.115.121.1.37', desc='Object Class Description', extra_compatability_tags=['FirstComponent:'+OID.oid])
Boolean = BooleanSyntaxDefinition('1.3.6.1.4.1.1466.115.121.1.7', desc='Boolean')
DN = DNSyntaxDefinition('1.3.6.1.4.1.1466.115.121.1.12', desc='DN')
NameAndOptionalUID = NameAndOptionalUIDSyntaxDefinition('1.3.6.1.4.1.1466.115.121.1.34', desc='Name And Optional UID')
GeneralizedTime = GeneralizedTimeSyntaxDefinition('1.3.6.1.4.1.1466.115.121.1.24', desc='Generalized Time')
PostalAddress = PostalAddressSyntaxDefinition('1.3.6.1.4.1.1466.115.121.1.41', desc='Postal Address')
SubstringAssertion = SubstringAssertionSyntaxDefinition('1.3.6.1.4.1.1466.115.121.1.58', desc='Substring Assertion')
UTCTime = UTCTimeSyntaxDefinition('1.3.6.1.4.1.1466.115.121.1.53', desc='UTC Time')
DITContentRuleDescription = StubSyntaxDefinition('1.3.6.1.4.1.1466.115.121.1.16', desc='DIT Content Rule Description', extra_compatability_tags=['FirstComponent:'+OID.oid])
DITStructureRuleDescription = StubSyntaxDefinition('1.3.6.1.4.1.1466.115.121.1.17', desc='DIT Structure Rule Description', extra_compatability_tags=['FirstComponent:'+INTEGER.oid])
NameFormDescription = StubSyntaxDefinition('1.3.6.1.4.1.1466.115.121.1.35', desc='Name Form Description', extra_compatability_tags=['FirstComponent:'+OID.oid])

# RFC4523
X509Certificate = StubSyntaxDefinition('1.3.6.1.4.1.1466.115.121.1.8', desc='X.509 Certificate')
X509CertificateList = StubSyntaxDefinition('1.3.6.1.4.1.1466.115.121.1.9', desc='X.509 Certificate List')
X509CertificatePair = StubSyntaxDefinition('1.3.6.1.4.1.1466.115.121.1.10', desc='X.509 Certificate Pair')
X509SupportedAlgorithm = StubSyntaxDefinition('1.3.6.1.4.1.1466.115.121.1.49', desc='X.509 Supported Algorithm')
X509CertificateExactAssertion = StubSyntaxDefinition('1.3.6.1.1.15.1', desc='X.509 Certificate Exact Assertion')
X509CertificateAssertion = StubSyntaxDefinition('1.3.6.1.1.15.2', desc='X.509 Certificate Assertion')
X509CertificatePairExactAssertion = StubSyntaxDefinition('1.3.6.1.1.15.3', desc='X.509 Certificate Pair Exact Assertion')
X509CertificatePairAssertion = StubSyntaxDefinition('1.3.6.1.1.15.4', desc='X.509 Certificate Pair Assertion')
X509CertificateListExactAssertion = StubSyntaxDefinition('1.3.6.1.1.15.5', desc='X.509 Certificate List Exact Assertion')
X509CertificateListAssertion = StubSyntaxDefinition('1.3.6.1.1.15.6', desc='X.509 Certificate List Assertion')
X509AlgorithmIdentifier = StubSyntaxDefinition('1.3.6.1.1.15.7', desc='X.509 Algorithm Identifier')

# RFC3112
AuthPasswordSyntax = StubSyntaxDefinition('1.3.6.1.4.1.4203.1.1.2', desc='authentication password syntax')

ALL = (
	# RFC2252
	Binary,

	# RFC4517
	AttributeTypeDescription,
	BitString,
	Boolean,
	CountryString,
	DeliveryMethod,
	DirectoryString,
	DITContentRuleDescription,
	DITStructureRuleDescription,
	DN,
	EnhancedGuide,
	FacsimileTelephoneNumber,
	Fax,
	GeneralizedTime,
	Guide,
	IA5String,
	INTEGER,
	JPEG,
	LDAPSyntaxDescription,
	MatchingRuleDescription,
	MatchingRuleUseDescription,
	NameAndOptionalUID,
	NameFormDescription,
	NumericString,
	ObjectClassDescription,
	OctetString,
	OID,
	OtherMailbox,
	PostalAddress,
	PrintableString,
	SubstringAssertion,
	TelephoneNumber,
	TeletexTerminalIdentifier,
	TelexNumber,
	UTCTime,

	# RFC4523
	X509Certificate,
	X509CertificateList,
	X509CertificatePair,
	X509SupportedAlgorithm,
	X509CertificateExactAssertion,
	X509CertificateAssertion,
	X509CertificatePairExactAssertion,
	X509CertificatePairAssertion,
	X509CertificateListExactAssertion,
	X509CertificateListAssertion,
	X509AlgorithmIdentifier,

	# RFC3112
	AuthPasswordSyntax,
)
