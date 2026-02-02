# pylint: disable=too-many-instance-attributes,too-many-arguments,too-many-locals

import collections.abc

from .definitions import MatchingRuleKind, AttributeTypeUsage, MatchingRuleUseDefinition, AttributeTypeDefinition, ObjectClassDefinition
from .. import exceptions

__all__ = [
	'Syntax',
	'EqualityMatchingRule',
	'OrderingMatchingRule',
	'SubstrMatchingRule',
	'AttributeType',
	'ObjectClass',
	'Schema',
]

class Syntax:
	'''LDAP syntax for attribute and assertion values'''
	def __init__(self, schema, definition, syntaxes_by_tag):
		#:
		self.schema = schema
		#: Corresponding :class:`SyntaxDefinition` object
		self.definition = definition
		#: Numeric OID of syntax (string, e.g. ``'1.3.6.1.4.1.1466.115.121.1.15'``)
		self.oid = definition.oid
		#: Preferred name for syntax (same as :any:`oid`)
		self.ref = self.oid
		schema._register(self, self.oid, self.ref)
		schema.syntaxes._register(self, self.oid, self.ref)
		for tag in definition.compatability_tags:
			syntaxes_by_tag.setdefault(tag, set()).add(self)
		# Populated by MatchingRule.__init__
		#: Set of all matching rules wihin the schema that can be applied to values of the syntax
		self.compatible_matching_rules = set()

	def __repr__(self):
		return f'<ldapserver.schema.Syntax {self.ref}>'

	def encode(self, value):
		'''Encode value to its LDAP-specific encoding

		:param value: Native value
		:type value: any
		:rtype: bytes'''
		return self.definition.encode(self.schema, value)

	def decode(self, raw_value):
		'''Decode LDAP-specific encoding of a value

		:param raw_value: LDAP-specific encoding
		:type raw_value: bytes
		:rtype: any'''
		return self.definition.decode(self.schema, raw_value)

class MatchingRule:
	def __init__(self, schema, definition, syntaxes_by_tag):
		#:
		self.schema = schema
		#: Corresponding :class:`MatchingRuleDefinition` object
		self.definition = definition
		#: Numeric OID of matching rule (string, e.g. ``'2.5.13.2'``)
		self.oid = definition.oid
		#: Syntax of assertion values. For
		#: :any:`schema.SubstrMatchingRule.match_substr` the syntax of the
		#: attribute's equality matching rule is used instead.
		self.syntax = schema.syntaxes[definition.syntax]
		#: List of short descriptive names of the matching rule (list of strings, e.g. ``['caseIgnoreMatch']``)
		self.names = self.definition.name
		#: Preferred name of matching rule (first item of :any:`names` or :any:`oid`, e.g. ``'caseIgnoreMatch'``)
		self.ref = self.names[0] if self.names else self.oid
		schema._register(self, self.oid, self.ref, *self.names)
		schema.matching_rules._register(self, self.oid, self.ref, *self.names)
		#: Set of all compatible syntaxes within the schema whose values the matching rule can be applied to
		self.compatible_syntaxes = syntaxes_by_tag.setdefault(definition.compatability_tag, set())
		for syntax in self.compatible_syntaxes:
			syntax.compatible_matching_rules.add(self)
		# Populated by AttributeType.__init__
		#: Set of all compatible attribute types within the schema whose values the matching rule can be applied to
		self.compatible_attribute_types = set()

	def match_extensible(self, attribute_values, assertion_value):
		raise exceptions.LDAPInappropriateMatching()

class EqualityMatchingRule(MatchingRule):
	def __repr__(self):
		return f'<ldapserver.schema.EqualityMatchingRule {self.ref}>'

	def match_extensible(self, attribute_values, assertion_value):
		'''Return whether any attribute value equals the assertion value

		:returns: True if any attribute values matches, False otherwise
		:rtype: bool
		:raises exceptions.LDAPError: if the result is undefined'''
		return self.definition.match_equal(self.schema, attribute_values, assertion_value)

	def match_equal(self, attribute_values, assertion_value):
		'''Return whether any attribute value equals the assertion value

		:returns: True if any attribute values matches, False otherwise
		:rtype: bool
		:raises exceptions.LDAPError: if the result is undefined'''
		return self.definition.match_equal(self.schema, attribute_values, assertion_value)

	def match_approx(self, attribute_values, assertion_value):
		'''Return whether any attribute value approximatly equals the assertion value

		:returns: True if any attribute values matches, False otherwise
		:rtype: bool
		:raises exceptions.LDAPError: if the result is undefined'''
		return self.definition.match_approx(self.schema, attribute_values, assertion_value)

class OrderingMatchingRule(MatchingRule):
	def __repr__(self):
		return f'<ldapserver.schema.OrderingMatchingRule {self.ref}>'

	def match_less(self, attribute_values, assertion_value):
		'''Return whether any attribute value is less than assertion value

		:returns: True if any attribute values matches, False otherwise
		:rtype: bool
		:raises exceptions.LDAPError: if the result is undefined'''
		return self.definition.match_less(self.schema, attribute_values, assertion_value)

	def match_greater_or_equal(self, attribute_values, assertion_value):
		'''Return whether any attribute value is greater than or equal to assertion value

		:returns: True if any attribute values matches, False otherwise
		:rtype: bool
		:raises exceptions.LDAPError: if the result is undefined'''
		return self.definition.match_greater_or_equal(self.schema, attribute_values, assertion_value)

class SubstrMatchingRule(MatchingRule):
	def __repr__(self):
		return f'<ldapserver.schema.SubstrMatchingRule {self.ref}>'

	def match_extensible(self, attribute_values, assertion_value):
		'''Return whether any attribute value matches the substring assertion in assertion_value

		:param attribute_values: Attribute values (type according to attribute's syntax)
		:type attribute_values: List of any
		:param assertion_value: 3-tuple with initial substring, any substrings and final substring
		:type assertion_value: Tuple[any or None, List[any] or None, any or None]
		:returns: True if any attribute values matches, False otherwise
		:rtype: bool
		:raises exceptions.LDAPError: if the result is undefined'''
		return self.definition.match_substr(self.schema, attribute_values, assertion_value[0], assertion_value[1], assertion_value[2])

	def match_substr(self, attribute_values, inital_substring, any_substrings, final_substring):
		'''Return whether any attribute value matches the substring assertion

		The type of `inital_substring`, `any_substrings` and `final_substring`
		depends on the syntax of the attribute's equality matching rule!

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
		return self.definition.match_substr(self.schema, attribute_values, inital_substring, any_substrings, final_substring)

class AttributeType:
	def __init__(self, schema, definition):
		#:
		self.schema = schema
		#: Corresponding :class:`AttributeTypeDefinition` object
		self.definition = definition
		#: Numeric OID of the attribute type (string, e.g. ``'2.5.4.3'``)
		self.oid = definition.oid
		#: List of short descriptive names of the attribute type (list of strings, e.g. ``['cn', 'commonName']``)
		self.names = definition.name or []
		#: Preferred name of attribute type (first item of :any:`names` or :any:`oid`, e.g. ``'cn'``)
		self.ref = self.names[0] if self.names else self.oid
		#: Superior :class:`AttributeType` or `None`
		self.sup = schema.attribute_types[definition.sup] if definition.sup else None
		#: Set of subordinate attribute types
		self.subtypes = set()
		sup = self.sup
		while sup:
			self.sup.subtypes.add(self)
			sup = sup.sup
		#: :class:`EqualityMatchingRule` of the attribute type or `None` if the
		#: attribute type has no equality matching rule
		self.equality = schema.matching_rules[definition.equality] if definition.equality else None
		#: :class:`OrderingMatchingRule` of the attribute type or `None` if the
		#: attribute type has no ordering matching rule
		self.ordering = schema.matching_rules[definition.ordering] if definition.ordering else None
		#: :class:`SubstrMatchingRule` of the attribute type or `None` if the
		#: attribute type has no substring matching rule
		self.substr = schema.matching_rules[definition.substr] if definition.substr else None
		if self.sup:
			self.equality = self.equality or self.sup.equality
			self.ordering = self.ordering or self.sup.ordering
			self.substr = self.substr or self.sup.substr
		#: :class:`Syntax` of attribute values
		self.syntax = schema.syntaxes[definition.syntax] if definition.syntax else self.sup.syntax
		#: :any:`True` if attribute type is operational, :any:`False` if it is a
		#: user application attribute type.
		self.is_operational = (definition.usage != AttributeTypeUsage.userApplications)
		schema._register(self, self.oid, self.ref, *self.names)
		schema.attribute_types._register(self, self.oid, self.ref, *self.names)
		if self.is_operational:
			schema.operational_attribute_types.add(self)
		else:
			schema.user_attribute_types.add(self)
		#: Set of all matching rules in schema that can be applied to values of the attribute type
		self.compatible_matching_rules = self.syntax.compatible_matching_rules
		for matching_rule in self.compatible_matching_rules:
			matching_rule.compatible_attribute_types.add(self)

	def __repr__(self):
		return f'<ldapserver.schema.AttributeType {self.ref}>'

	def encode(self, value):
		'''Encode attribute value to its LDAP-specific encoding

		:param value: Native value
		:type value: any
		:rtype: bytes'''
		return self.syntax.encode(value)

	def decode(self, raw_value):
		'''Decode LDAP-specific encoding of an attribute value

		:param raw_value: LDAP-specific encoding
		:type raw_value: bytes
		:rtype: any'''
		return self.syntax.decode(raw_value)

	def match_equal(self, attribute_values, assertion_value):
		'''Return whether any attribute value equals the assertion value

		:param attribute_values: Attribute values (type according to syntax)
		:type attribute_values: List of any
		:param assertion_value: Assertion value
		:type assertion_value: bytes
		:returns: True if any attribute values matches, False otherwise
		:rtype: bool
		:raises exceptions.LDAPError: if the result is undefined'''
		if self.equality is None:
			raise exceptions.LDAPInappropriateMatching()
		assertion_value = self.equality.syntax.decode(assertion_value)
		return self.equality.match_equal(attribute_values, assertion_value)

	def match_substr(self, attribute_values, inital_substring, any_substrings, final_substring):
		'''Return whether any attribute value matches the substring assertion

		:param attribute_values: Attribute values (type according to syntax)
		:type attribute_values: List of any
		:param inital_substring: Substring to match the beginning (optional)
		:type inital_substring: bytes or None
		:param any_substrings: List of substrings to match between initial and final in order
		:type any_substrings: list of bytes
		:param final_substring: Substring to match the end (optional)
		:type final_substring: bytes or None
		:returns: True if any attribute values matches, False otherwise
		:rtype: bool
		:raises exceptions.LDAPError: if the result is undefined'''
		if self.equality is None or self.substr is None:
			raise exceptions.LDAPInappropriateMatching()
		if inital_substring:
			inital_substring = self.equality.syntax.decode(inital_substring)
		any_substrings = [self.equality.syntax.decode(substring) for substring in any_substrings]
		if final_substring:
			final_substring = self.equality.syntax.decode(final_substring)
		return self.substr.match_substr(attribute_values, inital_substring, any_substrings, final_substring)

	def match_approx(self, attribute_values, assertion_value):
		'''Return whether any attribute value approximatly equals the assertion value

		:param attribute_values: Attribute values (type according to syntax)
		:type attribute_values: List of any
		:param assertion_value: Assertion value
		:type assertion_value: bytes
		:returns: True if any attribute values matches, False otherwise
		:rtype: bool
		:raises exceptions.LDAPError: if the result is undefined'''
		if self.equality is None:
			raise exceptions.LDAPInappropriateMatching()
		assertion_value = self.equality.syntax.decode(assertion_value)
		return self.equality.match_approx(attribute_values, assertion_value)

	def match_greater_or_equal(self, attribute_values, assertion_value):
		'''Return whether any attribute value is greater than or equal to assertion value

		:param attribute_values: Attribute values (type according to syntax)
		:type attribute_values: List of any
		:param assertion_value: Assertion value
		:type assertion_value: bytes
		:returns: True if any attribute values matches, False otherwise
		:rtype: bool
		:raises exceptions.LDAPError: if the result is undefined'''

		if self.ordering is None:
			raise exceptions.LDAPInappropriateMatching()
		assertion_value = self.ordering.syntax.decode(assertion_value)
		return self.ordering.match_greater_or_equal(attribute_values, assertion_value)

	def __match_less(self, attribute_values, assertion_value):
		if self.ordering is None:
			raise exceptions.LDAPInappropriateMatching()
		assertion_value = self.ordering.syntax.decode(assertion_value)
		return self.ordering.match_less(attribute_values, assertion_value)

	def match_less_or_equal(self, attribute_values, assertion_value):
		'''Return whether any attribute value is less than or equal to assertion value

		:param attribute_values: Attribute values (type according to syntax)
		:type attribute_values: List of any
		:param assertion_value: Assertion value
		:type assertion_value: bytes
		:returns: True if any attribute values matches, False otherwise
		:rtype: bool
		:raises exceptions.LDAPError: if the result is undefined'''

		equal_exc = None
		try:
			if self.match_equal(attribute_values, assertion_value):
				return True
		except exceptions.LDAPError as exc:
			equal_exc = exc
		if self.__match_less(attribute_values, assertion_value):
			return True
		if equal_exc is not None:
			raise equal_exc
		return False

	def match_extensible(self, attribute_values, assertion_value, matching_rule=None):
		'''Return whether any attribute value matches the assertion value

		:param attribute_values: Attribute values (type according to syntax)
		:type attribute_values: List of any
		:param assertion_value: Assertion value
		:type assertion_value: bytes
		:param matching_rule: Optional matching rule, if None :any:`AttributeType.equality` is used
		:type matching_rule: :class:`EqualityMatchingRule`, :class:`OrderingMatchingRule`, :class:`SubstrMatchingRule` or None
		:returns: True if any attribute values matches, False otherwise
		:rtype: bool
		:raises exceptions.LDAPError: if the result is undefined'''
		if not matching_rule:
			matching_rule = self.equality
		if not matching_rule or matching_rule not in self.compatible_matching_rules:
			raise exceptions.LDAPInappropriateMatching()
		assertion_value = matching_rule.syntax.decode(assertion_value)
		return matching_rule.match_extensible(attribute_values, assertion_value)

class ObjectClass:
	'''Representation of an object class wihin a schema'''
	def __init__(self, schema, definition):
		#:
		self.schema = schema
		#: Corresponding :class:`AttributeTypeDefinition` object
		self.definition = definition
		#: Numeric OID of object class (string, e.g. ``'2.5.6.0'``)
		self.oid = definition.oid
		#: List of short descriptive names of the object class (list of strings, e.g. ``['top']``)
		self.names = definition.name
		#: Preferred name of object class (first item of :any:`names` or :any:`oid`, e.g. ``'top'``)
		self.ref = self.names[0] if self.names else self.oid
		# Lookup dependencies to ensure consistency
		# pylint: disable=pointless-statement
		for sup_oid in definition.sup:
			schema.object_classes[sup_oid]
		for must_oid in definition.must:
			schema.attribute_types[must_oid]
		for may_oid in definition.may:
			schema.attribute_types[may_oid]
		schema._register(self, self.oid, self.ref, *self.names)
		schema.object_classes._register(self, self.oid, self.ref, *self.names)

	def __repr__(self):
		return f'<ldapserver.schema.ObjectClass {self.ref}>'

class OIDDict(collections.abc.Mapping):
	def __init__(self):
		self.__data = {}
		self.__refs = []
		self.__numeric_oid_map = {}

	def _register(self, obj, oid, ref, *names):
		if obj in self.__data:
			return
		if oid in self.__data:
			raise Exception(f'OID "{oid}" already registered')
		for name in (ref,) + names:
			if name.lower().strip() in self.__data:
				raise Exception(f'Short descriptive name "{name}" already registered')
		self.__refs.append(ref)
		self.__data[obj] = obj
		self.__numeric_oid_map[obj] = oid
		for name in (oid, ref) + names:
			self.__data[name.lower().strip()] = obj
			self.__numeric_oid_map[name.lower().strip()] = oid

	def __getitem__(self, key):
		if isinstance(key, str):
			key = key.lower().strip()
		return self.__data[key]

	def __iter__(self):
		return iter(self.__refs)

	def __len__(self):
		return len(self.__refs)

	def get_numeric_oid(self, key, default=None):
		if isinstance(key, str):
			key = key.lower().strip()
		return self.__numeric_oid_map.get(key, default)

class Schema(OIDDict):
	'''Consistent collection of syntaxes, matching rules, attribute types and
	object classes forming an LDAP schema

	:param object_class_definitions: List of :class:`ObjectClassDefinition` or :any:`str`
	:param attribute_type_definitions: List of :class:`AttributeTypeDefinition` or :any:`str`
	:param matching_rule_definitions: List of :class:`MatchingRuleDefinition`
	:param syntax_definitions: List of :class:`SyntaxDefinition`

	Is also a mapping of OIDs and short descriptive names to the respective
	schema element objects (:any:`Syntax`, ...).
	'''
	# pylint: disable=too-many-branches,too-many-statements
	def __init__(self, object_class_definitions=None, attribute_type_definitions=None,
	             matching_rule_definitions=None, syntax_definitions=None):
		super().__init__()
		syntaxes_by_tag = {}

		# Add syntaxes
		#: Mapping of syntax OIDs to :any:`Syntax` objects
		self.syntaxes = OIDDict()
		for definition in syntax_definitions or []:
			if definition.oid not in self.syntaxes:
				Syntax(self, definition, syntaxes_by_tag)
		#: Sequence of :any:`SyntaxDefinition` objects
		self.syntax_definitions = [syntax.definition for syntax in self.syntaxes.values()]

		# Add matching rules
		#: Mapping of matching rule OIDs and short descriptive names to :any:`EqualityMatchingRule`, :any:`OrderingMatchingRule` and :any:`SubstrMatchingRule`  objects
		self.matching_rules = OIDDict()
		for definition in matching_rule_definitions or []:
			if definition.kind == MatchingRuleKind.EQUALITY:
				cls = EqualityMatchingRule
			elif definition.kind == MatchingRuleKind.ORDERING:
				cls = OrderingMatchingRule
			elif definition.kind == MatchingRuleKind.SUBSTR:
				cls = SubstrMatchingRule
			else:
				raise ValueError('Invalid matching rule kind')
			if definition.oid not in self.matching_rules:
				cls(self, definition, syntaxes_by_tag)
		#: Sequence of :any:`MatchingRuleDefinition` objects
		self.matching_rule_definitions = [matching_rule.definition for matching_rule in self.matching_rules.values()]

		# Add attribute types
		attribute_type_definitions = [AttributeTypeDefinition.from_str(item)
		                              if isinstance(item, str) else item
		                              for item in attribute_type_definitions or []]
		#: Mapping of attribute type OIDs and short descriptive names to :any:`AttributeType` objects
		self.attribute_types = OIDDict()
		#: Set of user (non-operational) attribute types
		self.user_attribute_types = set()
		#: Set of operational (non-user) attribute types
		self.operational_attribute_types = set()
		# Attribute types may refer to other (superior) attribute types. To resolve
		# these dependencies we cycle through the definitions, each time adding
		# those not added yet with fulfilled dependencies. Finally we add all the
		# remaining ones to provoke exceptions.
		keep_running = True
		while keep_running:
			keep_running = False
			for definition in attribute_type_definitions:
				if definition.oid in self.attribute_types:
					continue
				if definition.sup and definition.sup not in self.attribute_types:
					continue
				AttributeType(self, definition)
				keep_running = True
		for definition in attribute_type_definitions:
			if definition.oid not in self.attribute_types:
				AttributeType(self, definition)
		#: Sequence of :any:`AttributeTypeDefinition` objects
		self.attribute_type_definitions = [attribute_type.definition for attribute_type in self.attribute_types.values()]

		# Add object classes
		object_class_definitions = [ObjectClassDefinition.from_str(item)
		                            if isinstance(item, str) else item
		                            for item in object_class_definitions or []]
		#: Mapping of object class OIDs and short descriptive names to :any:`ObjectClass` objects
		self.object_classes = OIDDict()
		# Object classes may refer to other (superior) object classes. To resolve
		# these dependencies we cycle through the definitions, each time adding
		# those not added yet with fulfilled dependencies. Finally we add all the
		# remaining ones to provoke exceptions.
		keep_running = True
		while keep_running:
			keep_running = False
			for definition in object_class_definitions:
				if definition.oid in self.object_classes:
					continue
				if any(map(lambda oid: oid and oid not in self.object_classes, definition.sup)):
					continue
				ObjectClass(self, definition)
				keep_running = True
		for definition in object_class_definitions:
			if definition.oid not in self.object_classes:
				ObjectClass(self, definition)
		#: Sequence of :any:`ObjectClassDefinition` objects
		self.object_class_definitions = [object_class.definition for object_class in self.object_classes.values()]

		# Generate and add matching rules
		#: Sequence of :any:`MatchingRuleUseDefinition` objects
		self.matching_rule_use_definitions = []
		for matching_rule in self.matching_rules.values():
			definition = matching_rule.definition
			applies = [attribute_type.ref for attribute_type in matching_rule.compatible_attribute_types]
			rule_use = MatchingRuleUseDefinition(definition.oid, name=definition.name,
					desc=definition.desc, obsolete=definition.obsolete, applies=applies,
					extensions=definition.extensions)
			if applies:
				self.matching_rule_use_definitions.append(rule_use)

	def extend(self, object_class_definitions=None, attribute_type_definitions=None,
	           matching_rule_definitions=None, syntax_definitions=None):
		'''Return new schema with all schema elements and additional ones'''
		syntax_definitions = self.syntax_definitions + (syntax_definitions or [])
		matching_rule_definitions = self.matching_rule_definitions + (matching_rule_definitions or [])
		attribute_type_definitions = self.attribute_type_definitions + (attribute_type_definitions or [])
		object_class_definitions = self.object_class_definitions + (object_class_definitions or [])
		return type(self)(syntax_definitions=syntax_definitions,
		                  matching_rule_definitions=matching_rule_definitions,
		                  attribute_type_definitions=attribute_type_definitions,
		                  object_class_definitions=object_class_definitions)

	def __or__(self, value):
		return self.extend(syntax_definitions=value.syntax_definitions,
		                   matching_rule_definitions=value.matching_rule_definitions,
		                   attribute_type_definitions=value.attribute_type_definitions,
		                   object_class_definitions=value.object_class_definitions)

	def __hash__(self):
		return id(self)
