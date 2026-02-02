import collections.abc
import enum

from . import ldap, exceptions
from .dn import DN, RDN, RDNAssertion

__all__ = ['AttributeDict', 'Entry', 'ObjectEntry', 'RootDSE', 'WILDCARD', 'EntryTemplate', 'SubschemaSubentry']

class TypeKeysView(collections.abc.Set):
	def __init__(self, attributes):
		self.__attributes = attributes

	def __iter__(self):
		for attribute_type, values in self.__attributes.items():
			if values:
				yield attribute_type

	def __len__(self):
		return len(list(iter(self)))

	def __contains__(self, value):
		return bool(self.__attributes.get(value))

class TypeItemsView(collections.abc.Set):
	def __init__(self, attributes):
		self.__attributes = attributes

	def __iter__(self):
		for attribute_type, values in self.__attributes.items():
			if values:
				yield attribute_type, values

	def __len__(self):
		return len(list(iter(self)))

	def __contains__(self, value):
		key, values = value
		return self.__attributes.get(key) == values

class AttributeDict(collections.abc.MutableMapping):
	'''Special dictionary holding LDAP attribute values

	Attribute values can be set and accessed by their attribute type's numeric
	OID or short descriptive name. Attribute types must be defined within the
	schema to be used. Attribute values are always lists. Accessing an unset
	attribute behaves the same as accessing an empty attribute. List items must
	conform to the attribute's syntax.'''
	def __init__(self, schema, **attributes):
		self.__attributes = {}
		#:
		self.schema = schema
		for key, values in attributes.items():
			self[key] = values

	def __getitem__(self, key):
		return self.__attributes.setdefault(self.schema.attribute_types[key], [])

	def __setitem__(self, key, values):
		self.__attributes[self.schema.attribute_types[key]] = values

	def __delitem__(self, key):
		self[key] = []

	def __iter__(self):
		for attribute_type, values in self.__attributes.items():
			if values:
				yield attribute_type.ref

	def __len__(self):
		return len(list(iter(self)))

	def get(self, key, default=None, subtypes=False): # pylint: disable=arguments-differ
		attribute_type = self.schema.attribute_types.get(key)
		attribute_types = [attribute_type]
		if subtypes and attribute_type:
			attribute_types += attribute_type.subtypes
		result = []
		for attribute_type in attribute_types:
			result += self.__attributes.get(attribute_type, [])
		if not result:
			result = default if default is not None else []
		return result

	def keys(self, types=False): # pylint: disable=arguments-differ
		if not types:
			return super().keys()
		return TypeKeysView(self.__attributes)

	def items(self, types=False): # pylint: disable=arguments-differ
		if not types:
			return super().items()
		return TypeItemsView(self.__attributes)

	def __contains__(self, key):
		try:
			return bool(self[key])
		except KeyError:
			return False

	def setdefault(self, key, default=False):
		if key in self:
			return self[key]
		if default is None:
			default = []
		self[key] = default
		return default

class FilterResult(enum.Enum):
	TRUE = enum.auto()
	FALSE = enum.auto()
	UNDEFINED = enum.auto()

class Entry(AttributeDict):
	'''Base class for all directory entries

	All entries implement the methods :any:`Entry.search` and
	:any:`Entry.compare`. :class:`LDAPRequestHandler` uses them to process the
	corresponding LDAP requests.

	Entries also provide dict-like access to attributes. See
	:class:`AttributeDict`.'''
	def __init__(self, schema, dn, **attributes):
		super().__init__(schema, **attributes)
		#: Entry's distinguished name (:class:`DN`)
		self.dn = DN(schema, dn)

	def __search_match_dn(self, basedn, scope):
		if scope == ldap.SearchScope.baseObject:
			return self.dn == basedn
		elif scope == ldap.SearchScope.singleLevel:
			return self.dn.is_direct_child_of(basedn)
		elif scope == ldap.SearchScope.wholeSubtree:
			return self.dn.in_subtree_of(basedn)
		else:
			return False

	def __search_match_filter(self, filter_obj):
		# pylint: disable=too-many-branches,too-many-return-statements,too-many-statements,too-many-nested-blocks
		if isinstance(filter_obj, ldap.FilterAnd):
			# RFC4526: An 'and' filter consisting of an empty set of filters SHALL evaluate to True.
			result = FilterResult.TRUE
			for subfilter in filter_obj.filters:
				subresult = self.__search_match_filter(subfilter)
				if subresult == FilterResult.FALSE:
					return FilterResult.FALSE
				elif subresult == FilterResult.UNDEFINED:
					result = FilterResult.UNDEFINED
			return result
		elif isinstance(filter_obj, ldap.FilterOr):
			# RFC4526: An 'or' filter consisting of an empty set of filters SHALL evaluate to False.
			result = FilterResult.FALSE
			for subfilter in filter_obj.filters:
				subresult = self.__search_match_filter(subfilter)
				if subresult == FilterResult.TRUE:
					return FilterResult.TRUE
				elif subresult == FilterResult.UNDEFINED:
					result = FilterResult.UNDEFINED
			return result
		elif isinstance(filter_obj, ldap.FilterNot):
			subresult = self.__search_match_filter(filter_obj.filter)
			if subresult == FilterResult.TRUE:
				return FilterResult.FALSE
			elif subresult == FilterResult.FALSE:
				return FilterResult.TRUE
			else:
				return subresult
		elif isinstance(filter_obj, (ldap.FilterPresent,
		                             ldap.FilterEqual,
		                             ldap.FilterSubstrings,
		                             ldap.FilterApproxMatch,
		                             ldap.FilterGreaterOrEqual,
		                             ldap.FilterLessOrEqual)):
			try:
				attribute_type = self.schema.attribute_types[filter_obj.attribute]
			except KeyError:
				return FilterResult.UNDEFINED
			values = self.get(filter_obj.attribute, subtypes=True)
			try:
				if isinstance(filter_obj, ldap.FilterPresent):
					result = values != []
				elif isinstance(filter_obj, ldap.FilterEqual):
					result = attribute_type.match_equal(values, filter_obj.value)
				elif isinstance(filter_obj, ldap.FilterSubstrings):
					result = attribute_type.match_substr(values,
							filter_obj.initial_substring, filter_obj.any_substrings, filter_obj.final_substring)
				elif isinstance(filter_obj, ldap.FilterApproxMatch):
					result = attribute_type.match_approx(values, filter_obj.value)
				elif isinstance(filter_obj, ldap.FilterGreaterOrEqual):
					result = attribute_type.match_greater_or_equal(values, filter_obj.value)
				elif isinstance(filter_obj, ldap.FilterLessOrEqual):
					result = attribute_type.match_less_or_equal(values, filter_obj.value)
				else:
					return FilterResult.UNDEFINED
				return FilterResult.TRUE if result else FilterResult.FALSE
			except exceptions.LDAPError:
				return FilterResult.UNDEFINED
		elif isinstance(filter_obj, ldap.FilterExtensibleMatch):
			attribute_types = []
			matching_rule = None
			try:
				if filter_obj.type is not None and filter_obj.matchingRule is not None:
					attribute_types = [self.schema.attribute_types[filter_obj.type]]
					matching_rule = self.schema.matching_rules[filter_obj.matchingRule]
				elif filter_obj.type is not None:
					attribute_types = [self.schema.attribute_types[filter_obj.type]]
				elif filter_obj.matchingRule is not None:
					matching_rule = self.schema.matching_rules[filter_obj.matchingRule]
					attribute_types = matching_rule.compatible_attribute_types
			except KeyError:
				pass
			result = FilterResult.FALSE
			for attribute_type in attribute_types:
				values = self.get(attribute_type.oid, subtypes=True)
				if filter_obj.dnAttributes:
					for rdn in self.dn:
						for assertion in rdn:
							if assertion.attribute.lower() == attribute_type.ref.lower():
								values.append(assertion.value)
				try:
					if attribute_type.match_extensible(values, filter_obj.matchValue, matching_rule):
						return FilterResult.TRUE
				except exceptions.LDAPError:
					result = FilterResult.UNDEFINED
			return result
		else:
			return FilterResult.UNDEFINED

	def match_search(self, base_obj, scope, filter_obj):
		return self.__search_match_dn(DN.from_str(self.schema, base_obj), scope) and \
		       self.__search_match_filter(filter_obj) == FilterResult.TRUE

	def search(self, base_obj, scope, filter_obj, attributes, types_only):
		'''Return SEARCH result for the entry if it matches the operation
		parameters

		:param base_obj: DN of the base entry
		:type base_obj: str
		:param scope: Scope of base_obj
		:type scope: ldap.SearchScope
		:param filter_obj: Search filter
		:type filter_obj: ldap.Filter
		:param attributes: Requested attributes
		:type attributes: list of str
		:param types_only: Omit values in :class:`ldap.PartialAttribute`
		:type types_only: bool
		:returns: SEARCH result for the entry if it matches the operation
		          parameters, None otherwise
		:rtype: ldap.SearchResultEntry or None

		Conforms to RFC4511 and RFC4526 (empty AND/OR filters are supported and
		treated as absolute TRUE/FALSE).'''
		if not self.match_search(base_obj, scope, filter_obj):
			return None
		selected_attributes = set()
		for selector in attributes or ['*']:
			if selector == '*':
				selected_attributes |= self.schema.user_attribute_types
			elif selector == '+':
				selected_attributes |= self.schema.operational_attribute_types
			elif selector == '1.1':
				continue
			elif selector in self.schema.attribute_types:
				selected_attributes.add(self.schema.attribute_types[selector])
		partial_attributes = []
		for attribute_type, values in self.items(types=True):
			if attribute_type in selected_attributes:
				if types_only:
					values = []
				encoded_values = [attribute_type.encode(value) for value in values]
				partial_attributes.append(ldap.PartialAttribute(attribute_type.ref, encoded_values))
		return ldap.SearchResultEntry(str(self.dn), partial_attributes)

	def compare(self, dn, attribute, value):
		'''Return the result of the COMPARE operation applied to the entry

		:param dn: DN of the entry to be compared
		:type dn: str
		:param attribute: Attribute OID or short descriptive name
		:type attribute: str
		:param value: Assertion value
		:type value: bytes
		:raises exceptions.LDAPNoSuchObject: if dn does not refer to the entry
		:raises exceptions.LDAPError: if operation results to anything other than
		                              TRUE/FALSE
		:return: True/False if COMPARE operation evaluates to TRUE/FALSE
		:rtype: bool

		Evaluation is essentially applying the EQUALITY matching rule of attribute
		on the values of attribute with the assertion value.'''
		try:
			dn = DN.from_str(self.schema, dn)
		except ValueError as exc:
			raise exceptions.LDAPNoSuchObject() from exc
		if dn != self.dn:
			raise exceptions.LDAPNoSuchObject()
		try:
			attribute_type = self.schema.attribute_types[attribute]
		except KeyError as exc:
			raise exceptions.LDAPUndefinedAttributeType() from exc
		return attribute_type.match_equal(self.get(attribute_type, subtypes=True), value)

class ObjectEntry(Entry):
	'''Regular object entry'''

class RootDSE(Entry):
	'''Root DSA-specific (server-specific) Entry

	Root of the Directory Information Tree (DIT). It's always identified by the
	emtpy DN. Provides information about the server, like supported features.'''
	def __init__(self, schema, **attributes):
		super().__init__(schema, DN(schema), **attributes)
		self.setdefault('objectClass', ['top'])

	def match_search(self, base_obj, scope, filter_obj):
		return not DN.from_str(self.schema, base_obj) and scope == ldap.SearchScope.baseObject and \
		       isinstance(filter_obj, ldap.FilterPresent) and \
		       filter_obj.attribute.lower() == 'objectclass'

class WildcardValue:
	pass

WILDCARD_VALUE = WildcardValue()

WILDCARD = (WILDCARD_VALUE,)

class TemplateFilterResult(enum.Enum):
	TRUE = enum.auto()
	FALSE = enum.auto()
	UNDEFINED = enum.auto()
	MAYBE_TRUE = enum.auto()

class EntryTemplate(AttributeDict):
	'''Utility class for dynamically generated object entries

	Set all entry-specific attributes to the special :data:`WILDCARD` value
	and call :any:EntryTemplate.match_search` to decide if any entries based
	on the template might match a SEARCH request. Call
	:any:EntryTemplate.create_entry` with the actual values to create entries
	based on a template.'''
	def __init__(self, schema, parent_dn, rdn_attribute, **attributes):
		super().__init__(schema, **attributes)
		self.parent_dn = DN(schema, parent_dn)
		self.rdn_attribute = rdn_attribute

	def __match_extract_dn_constraints(self, basedn, scope):
		if scope == ldap.SearchScope.baseObject:
			if basedn[1:] != self.parent_dn or basedn.object_attribute.lower() != self.rdn_attribute.lower():
				return False, AttributeDict(self.schema)
			return True, AttributeDict(self.schema, **{self.rdn_attribute: [basedn.object_value]})
		elif scope == ldap.SearchScope.singleLevel:
			return basedn == self.parent_dn, AttributeDict(self.schema)
		elif scope == ldap.SearchScope.wholeSubtree:
			if self.parent_dn.in_subtree_of(basedn):
				return True, AttributeDict(self.schema)
			if basedn[1:] != self.parent_dn or basedn.object_attribute.lower() != self.rdn_attribute.lower():
				return False, AttributeDict(self.schema)
			return True, AttributeDict(self.schema, **{self.rdn_attribute: [basedn.object_value]})
		else:
			return False, AttributeDict(self.schema)

	def __search_match_dn(self, basedn, scope):
		'''Return whether entries from this template might match the provided parameters'''
		return self.__match_extract_dn_constraints(basedn, scope)[0]

	def __extract_dn_constraints(self, basedn, scope):
		return self.__match_extract_dn_constraints(basedn, scope)[1]

	def __search_match_filter(self, filter_obj):
		# pylint: disable=too-many-return-statements,too-many-branches,too-many-nested-blocks,too-many-statements
		if isinstance(filter_obj, ldap.FilterAnd):
			# RFC4526: An 'and' filter consisting of an empty set of filters SHALL evaluate to True.
			result = TemplateFilterResult.TRUE
			for subfilter in filter_obj.filters:
				subresult = self.__search_match_filter(subfilter)
				if subresult == TemplateFilterResult.FALSE:
					return TemplateFilterResult.FALSE
				elif subresult == TemplateFilterResult.UNDEFINED:
					result = TemplateFilterResult.UNDEFINED
				elif subresult == TemplateFilterResult.MAYBE_TRUE and result == TemplateFilterResult.TRUE:
					result = TemplateFilterResult.MAYBE_TRUE
			return result
		elif isinstance(filter_obj, ldap.FilterOr):
			# RFC4526: An 'or' filter consisting of an empty set of filters SHALL evaluate to False.
			result = TemplateFilterResult.FALSE
			for subfilter in filter_obj.filters:
				subresult = self.__search_match_filter(subfilter)
				if subresult == TemplateFilterResult.TRUE:
					return TemplateFilterResult.TRUE
				elif subresult == TemplateFilterResult.MAYBE_TRUE:
					result = TemplateFilterResult.MAYBE_TRUE
				elif subresult == TemplateFilterResult.UNDEFINED and result == TemplateFilterResult.FALSE:
					result = TemplateFilterResult.UNDEFINED
			return result
		elif isinstance(filter_obj, ldap.FilterNot):
			subresult = self.__search_match_filter(filter_obj.filter)
			if subresult == TemplateFilterResult.TRUE:
				return TemplateFilterResult.FALSE
			elif subresult == TemplateFilterResult.FALSE:
				return TemplateFilterResult.TRUE
			else:
				return subresult
		elif isinstance(filter_obj, (ldap.FilterPresent,
		                             ldap.FilterEqual,
		                             ldap.FilterSubstrings,
		                             ldap.FilterApproxMatch,
		                             ldap.FilterGreaterOrEqual,
		                             ldap.FilterLessOrEqual)):
			try:
				attribute_type = self.schema.attribute_types[filter_obj.attribute]
			except KeyError:
				return TemplateFilterResult.UNDEFINED
			values = self.get(filter_obj.attribute, subtypes=True)
			is_wildcard = WILDCARD_VALUE in values
			if is_wildcard:
				values = []
			try:
				if isinstance(filter_obj, ldap.FilterPresent):
					result = values != []
				elif isinstance(filter_obj, ldap.FilterEqual):
					result = attribute_type.match_equal(values, filter_obj.value)
				elif isinstance(filter_obj, ldap.FilterSubstrings):
					result = attribute_type.match_substr(values,
							filter_obj.initial_substring, filter_obj.any_substrings, filter_obj.final_substring)
				elif isinstance(filter_obj, ldap.FilterApproxMatch):
					result = attribute_type.match_approx(values, filter_obj.value)
				elif isinstance(filter_obj, ldap.FilterGreaterOrEqual):
					result = attribute_type.match_greater_or_equal(values, filter_obj.value)
				elif isinstance(filter_obj, ldap.FilterLessOrEqual):
					result = attribute_type.match_less_or_equal(values, filter_obj.value)
				else:
					return TemplateFilterResult.UNDEFINED
				if result:
					return TemplateFilterResult.TRUE
			except exceptions.LDAPError:
				return TemplateFilterResult.UNDEFINED
			if is_wildcard:
				return TemplateFilterResult.MAYBE_TRUE
			return TemplateFilterResult.FALSE
		elif isinstance(filter_obj, ldap.FilterExtensibleMatch):
			attribute_types = []
			matching_rule = None
			try:
				if filter_obj.type is not None and filter_obj.matchingRule is not None:
					attribute_types = [self.schema.attribute_types[filter_obj.type]]
					matching_rule = self.schema.matching_rules[filter_obj.matchingRule]
				elif filter_obj.type is not None:
					attribute_types = [self.schema.attribute_types[filter_obj.type]]
				elif filter_obj.matchingRule is not None:
					matching_rule = self.schema.matching_rules[filter_obj.matchingRule]
					attribute_types = matching_rule.compatible_attribute_types
			except KeyError:
				pass
			result = TemplateFilterResult.FALSE
			for attribute_type in attribute_types:
				values = self.get(attribute_type.oid, subtypes=True)
				if filter_obj.dnAttributes:
					for rdn in self.parent_dn:
						for assertion in rdn:
							if assertion.attribute.lower() == attribute_type.ref.lower():
								values.append(assertion.value)
				is_wildcard = WILDCARD_VALUE in values
				if is_wildcard:
					values = []
				is_undefined = False
				try:
					if attribute_type.match_extensible(values, filter_obj.matchValue, matching_rule):
						return TemplateFilterResult.TRUE
				except exceptions.LDAPError:
					is_undefined = True
				if is_undefined and result == TemplateFilterResult.FALSE:
					result = TemplateFilterResult.UNDEFINED
				elif not is_undefined and is_wildcard:
					result = TemplateFilterResult.MAYBE_TRUE
			return result
		else:
			return TemplateFilterResult.UNDEFINED

	def __extract_filter_constraints(self, filter_obj):
		if isinstance(filter_obj, ldap.FilterEqual):
			try:
				attribute_type = self.schema.attribute_types[filter_obj.attribute]
			except KeyError:
				return AttributeDict(self.schema)
			if attribute_type.equality is None:
				return AttributeDict(self.schema)
			assertion_value = attribute_type.equality.syntax.decode(filter_obj.value)
			if assertion_value is None:
				return AttributeDict(self.schema)
			return AttributeDict(self.schema, **{filter_obj.attribute: [assertion_value]})
		if isinstance(filter_obj, ldap.FilterAnd):
			result = AttributeDict(self.schema)
			for subfilter in filter_obj.filters:
				for name, values in self.__extract_filter_constraints(subfilter).items():
					result[name] += values
			return result
		if isinstance(filter_obj, ldap.FilterOr) and len(filter_obj.filters) == 1:
			return self.__extract_filter_constraints(filter_obj.filters[0])
		return AttributeDict(self.schema)

	def match_search(self, base_obj, scope, filter_obj):
		'''Return whether entries based on this template might match the search parameters

		:param base_obj: DN of the base entry
		:type base_obj: str
		:param scope: Scope of base_obj
		:type scope: ldap.SearchScope
		:param filter_obj: Search filter
		:type filter_obj: ldap.Filter
		:returns: True if entries based on this template might match the SEARCH
		          parameters or False if they do not match
		:rtype: bool'''
		return self.__search_match_dn(DN.from_str(self.schema, base_obj), scope) and \
		       self.__search_match_filter(filter_obj) in (TemplateFilterResult.TRUE,
		                                                  TemplateFilterResult.MAYBE_TRUE)

	def extract_search_constraints(self, base_obj, scope, filter_obj):
		'''Return approximate value constraints for entries that match SEARCH parameters

		:returns: :class:`AttributeDict` with values that any entry must have
		          to match potentially match SEARCH parameters
		:rtype: AttributeDict

		Example:

			>>> subschema = SubschemaSubentry(schema.RFC4519_SCHEMA, 'cn=Subschema')
			>>> template = subschema.EntryTemplate('ou=users,dc=example,dc=com', 'cn', objectclass=['person', 'top'], sn=WILDCARD)
			>>> template.extract_search_constraints('cn=test,ou=users,dc=example,dc=com', ldap.SearchScope.baseObject, ldap.FilterEqual('sn', b'foobar'))
			subschema.AttributeDict(cn=['test'], sn=['foobar'])

		Note that the results are an approximation (i.e. some constrains may be
		missing) and the quality may improve over time. Also note that every entry
		that matches the SEARCH parameters also matches the constrains, but not
		vice versa.'''
		constraints = self.__extract_filter_constraints(filter_obj)
		for key, values in self.__extract_dn_constraints(DN.from_str(self.schema, base_obj), scope).items():
			constraints[key] += values
		return constraints

	def create_entry(self, rdn_value, **attributes):
		'''Instanciate :class:`Entry` based on template

		:param rdn_value: RDN value for DN construction
		:type rdn_value: any
		:rtype: Entry

		Template attributes set to :any:`WILDCARD` are stripped. Only
		template attributes set to :any:`WILDCARD` may be overwritten
		with `attributes`.'''
		obj = Entry(self.schema, DN(self.schema, self.parent_dn, **{self.rdn_attribute: rdn_value}))
		for key, values in attributes.items():
			if WILDCARD_VALUE not in self[key]:
				raise ValueError(f'Cannot set attribute "{key}" that is not set to WILDCARD in the template')
			obj[key] = values
		for attribute_type, values in self.items():
			if WILDCARD_VALUE not in values:
				obj[attribute_type] = values
		return obj

class SubschemaSubentry(Entry):
	'''Subentry providing information on a :class:`Schema`'''
	def __init__(self, schema, dn, **attributes):
		super().__init__(schema, dn, **attributes)
		self['subschemaSubentry'] = [self.dn]
		self['structuralObjectClass'] = ['subtree']
		self['objectClass'] = ['top', 'subtree', 'subschema']
		self['objectClasses'] = schema.object_class_definitions
		self['ldapSyntaxes'] = schema.syntax_definitions
		self['matchingRules'] = schema.matching_rule_definitions
		self['attributeTypes'] = schema.attribute_type_definitions
		self['matchingRuleUse'] = schema.matching_rule_use_definitions
		# pylint: disable=invalid-name
		#: Shorthand for :class:`AttributeDict`
		self.AttributeDict = lambda **attributes: AttributeDict(schema, **attributes)
		#: Shorthand for :class:`ObjectEntry`
		self.ObjectEntry = lambda *args, **attributes: ObjectEntry(schema, *args, subschemaSubentry=[self.dn], **attributes)
		#: Shorthand for :class:`RootDSE`
		self.RootDSE = lambda **attributes: RootDSE(schema, subschemaSubentry=[self.dn], **attributes)
		#: Shorthand for :class:`EntryTemplate`
		self.EntryTemplate = lambda *args, **kwargs: EntryTemplate(schema, *args, subschemaSubentry=[self.dn], **kwargs)
		class Wrapper:
			def __init__(self, cls, schema):
				self.cls = cls
				self.schema = schema

			def __call__(self, *args, **kwargs):
				return self.cls(self.schema, *args, **kwargs)

			def from_str(self, *args, **kwargs):
				return self.cls.from_str(self.schema, *args, **kwargs)

		#: Shorthand for :class:`DN`
		self.DN = Wrapper(DN, schema)
		#: Shorthand for :class:`RDN`
		self.RDN = Wrapper(RDN, schema)
		#: Shorthand for :class:`RDNAssertion`
		self.RDNAssertion = Wrapper(RDNAssertion, schema)

	def match_search(self, base_obj, scope, filter_obj):
		return DN.from_str(self.schema, base_obj) == self.dn and  \
		       scope == ldap.SearchScope.baseObject and \
		       isinstance(filter_obj, ldap.FilterEqual) and \
		       filter_obj.attribute.lower() == 'objectclass' and \
		       filter_obj.value.lower() == b'subschema'
