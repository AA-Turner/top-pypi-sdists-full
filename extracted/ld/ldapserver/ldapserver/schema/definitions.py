import enum
import re

from .. import exceptions

__all__ = [
	'SyntaxDefinition',
	'MatchingRuleKind',
	'MatchingRuleDefinition',
	'MatchingRuleUseDefinition',
	'AttributeTypeUsage',
	'AttributeTypeDefinition',
	'ObjectClassKind',
	'ObjectClassDefinition',
]

def escape(string):
	return string.replace('\\', '\\5C').replace('\'', '\\27')

def qdescr_to_token(descr):
	return '\''+descr+'\''

def qdescrs_to_tokens(descrs):
	if len(descrs) == 1:
		return [qdescr_to_token(descrs[0])]
	return ['('] + [qdescr_to_token(descr) for descr in descrs] + [')']

def oids_to_tokens(oids):
	if len(oids) == 1:
		return [oids[0]]
	tokens = ['(', oids[0]]
	for oid in oids[1:]:
		tokens += ['$', oid]
	return tokens + [')']

def qdstring_to_token(qdstring):
	return '\''+escape(qdstring)+'\''

def qdstrings_to_tokens(qdstrings):
	if len(qdstrings) == 1:
		return [qdstring_to_token(qdstrings[0])]
	return ['('] + [qdstring_to_token(qdstring) for qdstring in qdstrings] + [')']

def extensions_to_tokens(extensions):
	tokens = []
	if not extensions:
		return []
	for key, values in extensions.items():
		if not key.startswith('X-'):
			raise ValueError('Extention names must start with "X-"')
		tokens += [key] + qdstrings_to_tokens(values)
	return tokens

def tokenize(string):
	tokens = []
	offset = 0
	while string:
		match = re.match(r" *([()$]|[A-Za-z0-9.{}-]+|'[^']*') *", string)
		if not match:
			string_abbrev = string[:20] + '...'
			raise ValueError(f'Unrecognized token at offset {offset}: "{string_abbrev}"')
		tokens.append(match.groups()[0])
		string = string[match.end():]
		offset += match.end()
	return tokens

def pop_token(tokens):
	if not tokens:
		raise ValueError('Unexpected end of input')
	return tokens.pop(0)

def check_token(tokens, expected_token):
	if not tokens or tokens[0] != expected_token:
		return False
	tokens.pop(0)
	return True

def parse_token(tokens, expected_token):
	token = pop_token(tokens)
	if token != expected_token:
		raise ValueError(f'Expected "{expected_token}" but got "{token}"')
	return token

def parse_numericoid(tokens):
	token = pop_token(tokens)
	if not re.fullmatch(r"([0-9]|[1-9][0-9]*)(\.([0-9]|[1-9][0-9]*))*", token):
		raise ValueError(f'Invalid numeric OID "{token}"')
	return token

def parse_qdescr(tokens):
	token = pop_token(tokens)
	match = re.fullmatch(r"'([A-Za-z][A-Za-z0-9-]*)'", token)
	if not match:
		raise ValueError(f'Invalid quoted descriptor "{token}"')
	return match.groups()[0]

def parse_qdescrs(tokens):
	if check_token(tokens, '('):
		result = []
		while not check_token(tokens, ')'):
			result.append(parse_qdescr(tokens))
		return result
	return [parse_qdescr(tokens)]

def parse_qdstring(tokens):
	token = pop_token(tokens)
	match = re.fullmatch(r"'(([^'\\]|\\27|\\5C|\\5c)+)'", token)
	if not match:
		raise ValueError(f'Invalid quoted string "{token}"')
	return match.groups()[0].replace('\\27', '\'').replace('\\5C', '\\').replace('\\5c', '\\')

def parse_qdstrings(tokens):
	if check_token(tokens, '('):
		result = []
		while not check_token(tokens, ')'):
			result.append(parse_qdstring(tokens))
		return result
	return [parse_qdstring(tokens)]

def parse_oid(tokens):
	token = pop_token(tokens)
	if not re.fullmatch(r'([0-9]|[1-9][0-9]*)(\.([0-9]|[1-9][0-9]*))*|[A-Za-z][A-Za-z0-9-]*', token):
		raise ValueError(f'Invalid OID "{token}"')
	return token

def parse_oids(tokens):
	if check_token(tokens, '('):
		result = [parse_oid(tokens)]
		while not check_token(tokens, ')'):
			parse_token(tokens, '$')
			result.append(parse_oid(tokens))
		return result
	return [parse_oid(tokens)]

def parse_noidlen(tokens):
	token = pop_token(tokens)
	match = re.fullmatch(r"(([0-9]|[1-9][0-9]*)(\.([0-9]|[1-9][0-9]*))*)(|\{([0-9]|[1-9][0-9]*)\})", token)
	if not match:
		raise ValueError(f'Invalid numeric OID with optional length "{token}"')
	noid, _, _, _, _, length = match.groups()
	if length is not None:
		length = int(length)
	return noid, length

def parse_extensions(tokens):
	results = {}
	while tokens and re.fullmatch(r"X-[A-Z_-]+", tokens[0]):
		name = tokens.pop(0)
		values = parse_qdstrings(tokens)
		results[name] = values
	return results

class SyntaxDefinition:
	def __init__(self, oid, desc='', extensions=None, extra_compatability_tags=None):
		#: Numeric OID (string)
		self.oid = oid
		#: Description (string, empty if there is none)
		self.desc = desc
		#:
		self.extensions = extensions or {}
		#: Set of compatability tags (strings, usually numeric OIDs). Syntaxes
		#: always have at least their own numeric OID as a compatability tag.
		#:
		#: A matching rule can be applied to the values of a syntax if the matching
		#: rules compatability tag is one of the syntaxes compatability tags.
		self.compatability_tags = {oid} | set(extra_compatability_tags or tuple())

	def __str__(self):
		'''Return LDAP syntax definition string according to RFC4512

		Example:

			( 1.3.6.1.4.1.1466.115.121.1.15 DESC 'Directory String' )'''
		tokens = ['(', self.oid]
		if self.desc:
			tokens += ['DESC', qdstring_to_token(self.desc)]
		tokens += extensions_to_tokens(self.extensions) + [')']
		return ' '.join(tokens)

	@property
	def first_component_oid(self):
		'''Used by objectIdentifierFirstComponentMatch matching rule'''
		return self.oid

	def encode(self, schema, value):
		'''Encode native value to its LDAP-specific encoding

		:param schema: Schema of the object in whose context encoding takes place
		:type schema: Schema
		:param value: native value (depends on syntax)
		:type value: any

		:returns: LDAP-specific encoding of the value
		:rtype: bytes'''
		raise NotImplementedError()

	def decode(self, schema, raw_value):
		'''Decode LDAP-specific encoding of a value to a native value

		:param schema: Schema of the object in whose context decoding takes place
		:type schema: Schema
		:param raw_value: LDAP-specific encoding of the value
		:type raw_value: bytes

		:returns: native value (depends on syntax)
		:rtype: any
		:raises exceptions.LDAPError: if raw_value is invalid'''
		raise exceptions.LDAPInvalidAttributeSyntax()

class MatchingRuleKind(enum.Enum):
	'''Values for :any:`MatchingRuleDefinition.kind`'''
	#:
	EQUALITY = enum.auto()
	#:
	ORDERING = enum.auto()
	#:
	SUBSTR = enum.auto()

class MatchingRuleDefinition:
	# pylint: disable=too-many-arguments
	def __init__(self, oid, name=None, desc='', obsolete=False, syntax=None, extensions=None, compatability_tag=None, kind=None):
		if not syntax:
			raise ValueError('syntax must be specified')
		if not kind:
			raise ValueError('kind must be specified')
		#: Numeric OID (string)
		self.oid = oid
		#: OID of assertion value syntax (string)
		self.syntax = syntax
		#: Short descriptive names (list of strings, may be empty)
		self.name = name or []
		#: Description (string, empty if there is none)
		self.desc = desc
		#: bool
		self.obsolete = obsolete
		#:
		self.extensions = extensions or {}
		#: Compatability tag (string, usually a numeric OIDs). Defaults to the OID
		#: of its syntax.
		#:
		#: A matching rule can be applied to the values of a syntax if the matching
		#: rules compatability tag is one of the syntaxes compatability tags.
		self.compatability_tag = compatability_tag or syntax
		#:
		self.kind = kind

	def __str__(self):
		'''Return matching rule definition string according to RFC4512

		Example:

			( 2.5.13.2 NAME 'caseIgnoreMatch' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 )'''
		tokens = ['(', self.oid]
		if self.name:
			tokens += ['NAME'] + qdescrs_to_tokens(self.name)
		if self.desc:
			tokens += ['DESC', qdstring_to_token(self.desc)]
		if self.obsolete:
			tokens += ['OBSOLETE']
		tokens += ['SYNTAX', self.syntax]
		tokens += extensions_to_tokens(self.extensions) + [')']
		return ' '.join(tokens)

	@property
	def first_component_oid(self):
		'''Used by objectIdentifierFirstComponentMatch matching rule'''
		return self.oid

	def match_equal(self, schema, attribute_values, assertion_value):
		'''Return whether any attribute value equals the assertion value

		Only available for EQUALITY matching rules.

		:returns: True if any attribute values matches, False otherwise
		:rtype: bool
		:raises exceptions.LDAPError: if the result is undefined'''
		raise exceptions.LDAPInappropriateMatching()

	def match_approx(self, schema, attribute_values, assertion_value):
		'''Return whether any attribute value approximatly equals the assertion value

		Only available for EQUALITY matching rules.

		:returns: True if any attribute values matches, False otherwise
		:rtype: bool
		:raises exceptions.LDAPError: if the result is undefined'''
		return self.match_equal(schema, attribute_values, assertion_value)

	def match_less(self, schema, attribute_values, assertion_value):
		'''Return whether any attribute value is less than assertion value

		Only available for ORDERING matching rules.

		:returns: True if any attribute values matches, False otherwise
		:rtype: bool
		:raises exceptions.LDAPError: if the result is undefined'''
		raise exceptions.LDAPInappropriateMatching()

	def match_greater_or_equal(self, schema, attribute_values, assertion_value):
		'''Return whether any attribute value is greater than or equal to assertion value

		Only available for ORDERING matching rules.

		:returns: True if any attribute values matches, False otherwise
		:rtype: bool
		:raises exceptions.LDAPError: if the result is undefined'''
		raise exceptions.LDAPInappropriateMatching()

	def match_substr(self, schema, attribute_values, inital_substring, any_substrings, final_substring):
		'''Return whether any attribute value matches the substring assertion

		Only available for SUBSTR matching rules.

		The type of `inital_substring`, `any_substrings` and `final_substring`
		depends on the syntax of the attribute's equality matching rule!

		:param schema: Schema of the object whose attribute values are matched
		:type schema: Schema
		:param attribute_values: Attribute values (type according to attribute's syntax)
		:type attribute_values: List of any
		:param inital_substring: Substring to match the beginning (optional)
		:type inital_substring: any
		:param any_substrings: List of substrings to match between initial and final in order
		:type any_substrings: list of any
		:param final_substring: Substring to match the end (optional)
		:type final_substring: any
		:returns: True if any attribute values matches, False otherwise
		:rtype: bool
		:raises exceptions.LDAPError: if the result is undefined'''
		raise exceptions.LDAPInappropriateMatching()

class MatchingRuleUseDefinition:
	def __init__(self, oid, name=None, desc='', obsolete=False, applies=None, extensions=None):
		#: Numeric OID (string)
		self.oid = oid
		#: Short descriptive names (list of strings, may be empty)
		self.name = name or []
		#: Description (string, empty if there is none)
		self.desc = desc
		#: bool
		self.obsolete = obsolete
		#: OIDs or short descriptive names of attribute types the matching rule can
		#: be applied to (list of strings)
		self.applies = applies or []
		#:
		self.extensions = extensions or {}

	def __str__(self):
		'''Return matching rule use definition string according to RFC4512

		Example:

			( 2.5.13.0 NAME 'objectIdentifierMatch' APPLIES ( supportedControl $ supportedExtension $ supportedFeatures $ supportedApplicationContext ) )'''
		tokens = ['(', self.oid]
		if self.name:
			tokens += ['NAME'] + qdescrs_to_tokens(self.name)
		if self.desc:
			tokens += ['DESC', qdstring_to_token(self.desc)]
		if self.obsolete:
			tokens += ['OBSOLETE']
		tokens += ['APPLIES'] + oids_to_tokens(self.applies)
		tokens += extensions_to_tokens(self.extensions) + [')']
		return ' '.join(tokens)

	@property
	def first_component_oid(self):
		'''Used by objectIdentifierFirstComponentMatch matching rule'''
		return self.oid


class AttributeTypeUsage(enum.Enum):
	'''Values for :any:`AttributeTypeDefinition.usage`'''
	# pylint: disable=invalid-name
	#: user (not an operational attribute)
	userApplications = enum.auto()
	#: directory operational
	directoryOperation = enum.auto()
	#: DSA-shared operational
	distributedOperation = enum.auto()
	#: DSA-specific operational
	dSAOperation = enum.auto()

class AttributeTypeDefinition:
	# pylint: disable=too-many-arguments,too-many-instance-attributes,too-many-locals
	def __init__(self, oid, name=None, desc='', obsolete=False, sup=None,
	             equality=None, ordering=None, substr=None, syntax=None,
               syntax_len=None, single_value=False, collective=False,
		           no_user_modification=False,
	             usage=AttributeTypeUsage.userApplications, extensions=None):
		if not sup and not syntax:
			raise ValueError('Either SUP or SYNTAX must be specified')
		#: Numeric OID (string)
		self.oid = oid
		#: Short descriptive names (list of strings, may be empty)
		self.name = name or []
		#: Description (string, empty if there is none)
		self.desc = desc
		#: bool
		self.obsolete = obsolete
		#: OID or short descriptive name of superior attribute type (string or None)
		self.sup = sup
		#: OID or short descriptive name of equality matching rule (string or None)
		self.equality = equality
		#: OID or short descriptive name of ordering matching rule (string or None)
		self.ordering = ordering
		#: OID or short descriptive name of substrings matching rule (string or None)
		self.substr = substr
		#: OID of attribute value syntax (string or None)
		self.syntax = syntax
		#: Suggested minimum upper bound for attribute value length (int or None)
		self.syntax_len = syntax_len
		#: Whether attribute values are restricted to a single value (bool)
		self.single_value = single_value
		#: bool
		self.collective = collective
		#: bool
		self.no_user_modification = no_user_modification
		#: Value of :class:`AttributeTypeUsage`
		self.usage = usage
		#:
		self.extensions = extensions or {}

	def __str__(self):
		'''Return attribute type definition string according to RFC4512

		Example:

			( 2.5.4.3 NAME ( 'cn' 'commonName' ) DESC 'RFC4519: common name(s) for which the entity is known by' SUP name )

		The string can be decoded into an equalivalent
		:class:`AttributeTypeDefinition` object with :any:`from_str`.'''
		tokens = ['(', self.oid]
		if self.name:
			tokens += ['NAME'] + qdescrs_to_tokens(self.name)
		if self.desc:
			tokens += ['DESC', qdstring_to_token(self.desc)]
		if self.obsolete:
			tokens += ['OBSOLETE']
		if self.sup:
			tokens += ['SUP', self.sup]
		if self.equality:
			tokens += ['EQUALITY', self.equality]
		if self.ordering:
			tokens += ['ORDERING', self.ordering]
		if self.substr:
			tokens += ['SUBSTR', self.substr]
		if self.syntax:
			if self.syntax_len is None:
				tokens += ['SYNTAX', self.syntax]
			else:
				tokens += ['SYNTAX', self.syntax+'{'+str(self.syntax_len)+'}']
		if self.single_value:
			tokens += ['SINGLE-VALUE']
		if self.collective:
			tokens += ['COLLECTIVE']
		if self.no_user_modification:
			tokens += ['NO-USER-MODIFICATION']
		if self.usage != AttributeTypeUsage.userApplications:
			tokens += ['USAGE', self.usage.name]
		tokens += extensions_to_tokens(self.extensions) + [')']
		return ' '.join(tokens)

	@classmethod
	def from_str(cls, string):
		'''Decode attribute type definition string according to RFC4512

		:returns: Equivalent attribute type definition object
		:rtype: AttributeTypeDefinition

		See :any:`__str__` for the string format.'''
		tokens = tokenize(string)
		parse_token(tokens, '(')
		oid = parse_numericoid(tokens)
		name = []
		if check_token(tokens, 'NAME'):
			name = parse_qdescrs(tokens)
		desc = ''
		if check_token(tokens, 'DESC'):
			desc = parse_qdstring(tokens)
		obsolete = check_token(tokens, 'OBSOLETE')
		sup = None
		if check_token(tokens, 'SUP'):
			sup = parse_oid(tokens)
		equality = None
		if check_token(tokens, 'EQUALITY'):
			equality = parse_oid(tokens)
		ordering = None
		if check_token(tokens, 'ORDERING'):
			ordering = parse_oid(tokens)
		substr = None
		if check_token(tokens, 'SUBSTR'):
			substr = parse_oid(tokens)
		syntax, syntax_len = None, None
		if check_token(tokens, 'SYNTAX'):
			syntax, syntax_len = parse_noidlen(tokens)
		single_value = check_token(tokens, 'SINGLE-VALUE')
		collective = check_token(tokens, 'COLLECTIVE')
		no_user_modification = check_token(tokens, 'NO-USER-MODIFICATION')
		usage = AttributeTypeUsage.userApplications
		if check_token(tokens, 'USAGE'):
			token = tokens.pop(0)
			if token == 'userApplications':
				usage = AttributeTypeUsage.userApplications
			elif token == 'directoryOperation':
				usage = AttributeTypeUsage.directoryOperation
			elif token == 'distributedOperation':
				usage = AttributeTypeUsage.distributedOperation
			elif token == 'dSAOperation':
				usage = AttributeTypeUsage.dSAOperation
			else:
				raise ValueError(f'Invalid usage value "{token}"')
		extensions = parse_extensions(tokens)
		parse_token(tokens, ')')
		if tokens:
			raise ValueError(f'Unexpected token "{tokens[0]}", expected no more input')
		return cls(oid, name=name, desc=desc, obsolete=obsolete, sup=sup,
		           equality=equality, ordering=ordering, substr=substr,
		           syntax=syntax, syntax_len=syntax_len, single_value=single_value,
		           collective=collective, no_user_modification=no_user_modification,
		           usage=usage, extensions=extensions)

	@property
	def first_component_oid(self):
		'''Used by objectIdentifierFirstComponentMatch matching rule'''
		return self.oid

class ObjectClassKind(enum.Enum):
	'''Values for :any:`ObjectClassDefinition.kind`'''
	#:
	ABSTRACT = enum.auto()
	#:
	STRUCTURAL = enum.auto()
	#:
	AUXILIARY = enum.auto()

class ObjectClassDefinition:
	# pylint: disable=too-many-arguments
	def __init__(self, oid, name=None, desc='', obsolete=False, sup=None,
	             kind=ObjectClassKind.STRUCTURAL, must=None, may=None,
	             extensions=None):
		#: Numeric OID (string)
		self.oid = oid
		#: Short descriptive names (list of strings, may be empty)
		self.name = name or []
		#: Description (string, empty if there is none)
		self.desc = desc
		#: bool
		self.obsolete = obsolete
		#: OIDs and short descriptive names of superior object classes (list of
		#: strings, may be empty)
		self.sup = sup or []
		#: Value of :class:`ObjectClassKind`
		self.kind = kind
		#: OIDs and short descriptive names of attribute types entries with the
		#: object class must have (list of strings, may be empty)
		self.must = must or []
		#: OIDs and short descriptive names of attribute types entries with the
		#: object class may have (list of strings, may be empty)
		self.may = may or []
		#:
		self.extensions = extensions or {}

	def __str__(self):
		'''Return object class definition string according to RFC4512

		Example:

			( 2.5.6.0 NAME 'top' DESC 'top of the superclass chain' ABSTRACT MUST objectClass )

		The string can be decoded into an equalivalent
		:class:`ObjectClassDefinition` object with :any:`from_str`.'''
		tokens = ['(', self.oid]
		if self.name:
			tokens += ['NAME'] + qdescrs_to_tokens(self.name)
		if self.desc:
			tokens += ['DESC', qdstring_to_token(self.desc)]
		if self.obsolete:
			tokens += ['OBSOLETE']
		if self.sup:
			tokens += ['SUP'] + oids_to_tokens(self.sup)
		tokens += [self.kind.name]
		if self.must:
			tokens += ['MUST'] + oids_to_tokens(self.must)
		if self.may:
			tokens += ['MAY'] + oids_to_tokens(self.may)
		tokens += extensions_to_tokens(self.extensions) + [')']
		return ' '.join(tokens)

	@classmethod
	def from_str(cls, string):
		'''Decode object class definition string according to RFC4512

		:returns: Equivalent object class definition object
		:rtype: ObjectClassDefinition

		See :any:`__str__` for the string format.'''
		tokens = tokenize(string)
		parse_token(tokens, '(')
		oid = parse_numericoid(tokens)
		name = []
		if check_token(tokens, 'NAME'):
			name = parse_qdescrs(tokens)
		desc = ''
		if check_token(tokens, 'DESC'):
			desc = parse_qdstring(tokens)
		obsolete = check_token(tokens, 'OBSOLETE')
		sup = []
		if check_token(tokens, 'SUP'):
			sup = parse_oids(tokens)
		kind = ObjectClassKind.STRUCTURAL
		if check_token(tokens, 'ABSTRACT'):
			kind = ObjectClassKind.ABSTRACT
		elif check_token(tokens, 'STRUCTURAL'):
			kind = ObjectClassKind.STRUCTURAL
		elif check_token(tokens, 'AUXILIARY'):
			kind = ObjectClassKind.AUXILIARY
		must = []
		if check_token(tokens, 'MUST'):
			must = parse_oids(tokens)
		may = []
		if check_token(tokens, 'MAY'):
			may = parse_oids(tokens)
		extensions = parse_extensions(tokens)
		parse_token(tokens, ')')
		if tokens:
			raise ValueError(f'Unexpected token "{tokens[0]}", expected no more input')
		return cls(oid, name=name, desc=desc, obsolete=obsolete, sup=sup,
		           kind=kind, must=must, may=may, extensions=extensions)

	@property
	def first_component_oid(self):
		'''Used by objectIdentifierFirstComponentMatch matching rule'''
		return self.oid
