import re

from .definitions import MatchingRuleDefinition, MatchingRuleKind
from .. import rfc4518_stringprep, exceptions
from . import syntaxes

class GenericMatchingRuleDefinition(MatchingRuleDefinition):
	def match_equal(self, schema, attribute_values, assertion_value):
		for attribute_value in attribute_values:
			if attribute_value == assertion_value:
				return True
		return False

	def match_less(self, schema, attribute_values, assertion_value):
		for attribute_value in attribute_values:
			if attribute_value < assertion_value:
				return True
		return False

	def match_greater_or_equal(self, schema, attribute_values, assertion_value):
		for attribute_value in attribute_values:
			if attribute_value >= assertion_value:
				return True
		return False

def _substr_match(attribute_value, inital_substring, any_substrings, final_substring):
	if inital_substring:
		if not attribute_value.startswith(inital_substring):
			return False
		attribute_value = attribute_value[len(inital_substring):]
	if final_substring:
		if not attribute_value.endswith(final_substring):
			return False
		attribute_value = attribute_value[:-len(final_substring)]
	for substring in any_substrings:
		index = attribute_value.find(substring)
		if index == -1:
			return False
		attribute_value = attribute_value[index+len(substring):]
	return True

class StringMatchingRuleDefinition(MatchingRuleDefinition):
	def __init__(self, oid, matching_type=rfc4518_stringprep.MatchingType.EXACT_STRING, **kwargs):
		super().__init__(oid, **kwargs)
		self.matching_type = matching_type

	def prepare_assertion_value(self, attribute_value):
		try:
			return rfc4518_stringprep.prepare(attribute_value, self.matching_type)
		except ValueError as exc:
			raise exceptions.LDAPInvalidAttributeSyntax('Assertion value contains characters prohibited by RFC4518') from exc

	def prepare_attribute_values(self, attribute_values):
		for attribute_value in attribute_values:
			try:
				yield rfc4518_stringprep.prepare(attribute_value, self.matching_type)
			except ValueError:
				pass

	def match_equal(self, schema, attribute_values, assertion_value):
		assertion_value = self.prepare_assertion_value(assertion_value)
		for attribute_value in self.prepare_attribute_values(attribute_values):
			if attribute_value == assertion_value:
				return True
		return False

	def match_less(self, schema, attribute_values, assertion_value):
		assertion_value = self.prepare_assertion_value(assertion_value)
		for attribute_value in self.prepare_attribute_values(attribute_values):
			if attribute_value < assertion_value:
				return True
		return False

	def match_greater_or_equal(self, schema, attribute_values, assertion_value):
		assertion_value = self.prepare_assertion_value(assertion_value)
		for attribute_value in self.prepare_attribute_values(attribute_values):
			if attribute_value >= assertion_value:
				return True
		return False

	def match_substr(self, schema, attribute_values, inital_substring, any_substrings, final_substring):
		try:
			if inital_substring:
				inital_substring = rfc4518_stringprep.prepare(inital_substring, self.matching_type, rfc4518_stringprep.SubstringType.INITIAL)
			any_substrings = [rfc4518_stringprep.prepare(substring, self.matching_type, rfc4518_stringprep.SubstringType.ANY) for substring in any_substrings]
			if final_substring:
				final_substring = rfc4518_stringprep.prepare(final_substring, self.matching_type, rfc4518_stringprep.SubstringType.FINAL)
		except ValueError as exc:
			raise exceptions.LDAPInvalidAttributeSyntax('Assertion value contains characters prohibited by RFC4518') from exc
		for attribute_value in self.prepare_attribute_values(attribute_values):
			if _substr_match(attribute_value, inital_substring, any_substrings, final_substring):
				return True
		return False

class StringListMatchingRuleDefinition(MatchingRuleDefinition):
	def __init__(self, oid, matching_type=rfc4518_stringprep.MatchingType.EXACT_STRING, **kwargs):
		super().__init__(oid, **kwargs)
		self.matching_type = matching_type

	# Values are both lists of str
	def match_equal(self, schema, attribute_values, assertion_value):
		try:
			assertion_value = [rfc4518_stringprep.prepare(line, self.matching_type) for line in assertion_value]
		except ValueError as exc:
			raise exceptions.LDAPInvalidAttributeSyntax('Assertion value contains characters prohibited by RFC4518') from exc
		for attribute_value in attribute_values:
			try:
				attribute_value = [rfc4518_stringprep.prepare(line, self.matching_type) for line in attribute_value]
				if attribute_value == assertion_value:
					return True
			except ValueError:
				pass
		return False

	def match_substr(self, schema, attribute_values, inital_substring, any_substrings, final_substring):
		try:
			if inital_substring:
				inital_substring = rfc4518_stringprep.prepare(inital_substring, self.matching_type, rfc4518_stringprep.SubstringType.INITIAL)
			any_substrings = [rfc4518_stringprep.prepare(substring, self.matching_type, rfc4518_stringprep.SubstringType.ANY) for substring in any_substrings]
			if final_substring:
				final_substring = rfc4518_stringprep.prepare(final_substring, self.matching_type, rfc4518_stringprep.SubstringType.FINAL)
		except ValueError as exc:
			raise exceptions.LDAPInvalidAttributeSyntax('Assertion value contains characters prohibited by RFC4518') from exc
		for attribute_value in attribute_values:
			try:
				# LF is mapped to SPACE by stringprep, so it is suitable as a seperator
				attribute_value = '\n'.join([rfc4518_stringprep.prepare(line, self.matching_type) for line in attribute_value])
				if _substr_match(attribute_value, inital_substring, any_substrings, final_substring):
					return True
			except ValueError:
				pass
		return False

class FirstComponentMatchingRuleDefinition(MatchingRuleDefinition):
	def __init__(self, oid, attribute_name, matching_rule, compatability_tag=None, **kwargs):
		compatability_tag = compatability_tag or 'FirstComponent:'+matching_rule.compatability_tag
		super().__init__(oid, compatability_tag=compatability_tag, **kwargs)
		self.attribute_name = attribute_name
		self.matching_rule = matching_rule

	def match_equal(self, schema, attribute_values, assertion_value):
		attribute_values = [getattr(value, self.attribute_name)
		                    for value in attribute_values
		                    if hasattr(value, self.attribute_name)]
		return self.matching_rule.match_equal(schema, attribute_values, assertion_value)


class OIDMatchingRuleDefinition(MatchingRuleDefinition):
	NUMERIC_OID_RE = re.compile(r"([0-9]|[1-9][0-9]*)(\.([0-9]|[1-9][0-9]*))*")

	def match_equal(self, schema, attribute_values, assertion_value):
		if not self.NUMERIC_OID_RE.fullmatch(assertion_value):
			assertion_value = schema.get_numeric_oid(assertion_value)
		if assertion_value is None:
			raise exceptions.LDAPInvalidAttributeSyntax('Assertion value is an unknown OID descriptor')
		for attribute_value in attribute_values:
			attribute_value = schema.get_numeric_oid(attribute_value, attribute_value)
			if attribute_value == assertion_value:
				return True
		return False

class StubMatchingRuleDefinition(MatchingRuleDefinition):
	pass

# RFC4517
bitStringMatch = GenericMatchingRuleDefinition('2.5.13.16', name=['bitStringMatch'], syntax=syntaxes.BitString.oid, kind=MatchingRuleKind.EQUALITY)
booleanMatch = GenericMatchingRuleDefinition('2.5.13.13', name=['booleanMatch'], syntax=syntaxes.Boolean.oid, kind=MatchingRuleKind.EQUALITY)
caseExactIA5Match = StringMatchingRuleDefinition('1.3.6.1.4.1.1466.109.114.1', name=['caseExactIA5Match'], syntax=syntaxes.IA5String.oid, matching_type=rfc4518_stringprep.MatchingType.EXACT_STRING, kind=MatchingRuleKind.EQUALITY)
caseExactMatch = StringMatchingRuleDefinition('2.5.13.5', name=['caseExactMatch'], syntax=syntaxes.DirectoryString.oid, matching_type=rfc4518_stringprep.MatchingType.EXACT_STRING, kind=MatchingRuleKind.EQUALITY)
caseExactOrderingMatch = StringMatchingRuleDefinition('2.5.13.6', name=['caseExactOrderingMatch'], syntax=syntaxes.DirectoryString.oid, matching_type=rfc4518_stringprep.MatchingType.EXACT_STRING, kind=MatchingRuleKind.ORDERING)
caseExactSubstringsMatch = StringMatchingRuleDefinition('2.5.13.7', name=['caseExactSubstringsMatch'], syntax=syntaxes.SubstringAssertion.oid, compatability_tag=syntaxes.DirectoryString.oid, matching_type=rfc4518_stringprep.MatchingType.EXACT_STRING, kind=MatchingRuleKind.SUBSTR)
caseIgnoreIA5Match = StringMatchingRuleDefinition('1.3.6.1.4.1.1466.109.114.2', name=['caseIgnoreIA5Match'], syntax=syntaxes.IA5String.oid, matching_type=rfc4518_stringprep.MatchingType.CASE_IGNORE_STRING, kind=MatchingRuleKind.EQUALITY)
caseIgnoreIA5SubstringsMatch = StringMatchingRuleDefinition('1.3.6.1.4.1.1466.109.114.3', name=['caseIgnoreIA5SubstringsMatch'], syntax=syntaxes.SubstringAssertion.oid, compatability_tag=syntaxes.IA5String.oid, matching_type=rfc4518_stringprep.MatchingType.CASE_IGNORE_STRING, kind=MatchingRuleKind.SUBSTR)
caseIgnoreListMatch = StringListMatchingRuleDefinition('2.5.13.11', name=['caseIgnoreListMatch'], syntax=syntaxes.PostalAddress.oid, matching_type=rfc4518_stringprep.MatchingType.CASE_IGNORE_STRING, kind=MatchingRuleKind.EQUALITY)
caseIgnoreListSubstringsMatch = StringListMatchingRuleDefinition('2.5.13.12', name=['caseIgnoreListSubstringsMatch'], syntax=syntaxes.SubstringAssertion.oid, compatability_tag=syntaxes.PostalAddress.oid, matching_type=rfc4518_stringprep.MatchingType.CASE_IGNORE_STRING, kind=MatchingRuleKind.SUBSTR)
caseIgnoreMatch = StringMatchingRuleDefinition('2.5.13.2', name=['caseIgnoreMatch'], syntax=syntaxes.DirectoryString.oid, matching_type=rfc4518_stringprep.MatchingType.CASE_IGNORE_STRING, kind=MatchingRuleKind.EQUALITY)
caseIgnoreOrderingMatch = StringMatchingRuleDefinition('2.5.13.3', name=['caseIgnoreOrderingMatch'], syntax=syntaxes.DirectoryString.oid, matching_type=rfc4518_stringprep.MatchingType.CASE_IGNORE_STRING, kind=MatchingRuleKind.ORDERING)
caseIgnoreSubstringsMatch = StringMatchingRuleDefinition('2.5.13.4', name=['caseIgnoreSubstringsMatch'], syntax=syntaxes.SubstringAssertion.oid, compatability_tag=syntaxes.DirectoryString.oid, matching_type=rfc4518_stringprep.MatchingType.CASE_IGNORE_STRING, kind=MatchingRuleKind.SUBSTR)
directoryStringFirstComponentMatch = FirstComponentMatchingRuleDefinition('2.5.13.31', name=['directoryStringFirstComponentMatch'], syntax=syntaxes.DirectoryString.oid, attribute_name='first_component_string', matching_rule=caseIgnoreMatch, kind=MatchingRuleKind.EQUALITY)
distinguishedNameMatch = GenericMatchingRuleDefinition('2.5.13.1', name=['distinguishedNameMatch'], syntax=syntaxes.DN.oid, kind=MatchingRuleKind.EQUALITY)
generalizedTimeMatch = GenericMatchingRuleDefinition('2.5.13.27', name=['generalizedTimeMatch'], syntax=syntaxes.GeneralizedTime.oid, kind=MatchingRuleKind.EQUALITY)
generalizedTimeOrderingMatch = GenericMatchingRuleDefinition('2.5.13.28', name=['generalizedTimeOrderingMatch'], syntax=syntaxes.GeneralizedTime.oid, kind=MatchingRuleKind.ORDERING)
integerMatch = GenericMatchingRuleDefinition('2.5.13.14', name=['integerMatch'], syntax=syntaxes.INTEGER.oid, kind=MatchingRuleKind.EQUALITY)
integerFirstComponentMatch = FirstComponentMatchingRuleDefinition('2.5.13.29', name=['integerFirstComponentMatch'], syntax=syntaxes.INTEGER.oid, attribute_name='first_component_integer', matching_rule=integerMatch, kind=MatchingRuleKind.EQUALITY)
integerOrderingMatch = GenericMatchingRuleDefinition('2.5.13.15', name=['integerOrderingMatch'], syntax=syntaxes.INTEGER.oid, kind=MatchingRuleKind.ORDERING)
# Optional and implementation-specific, we simply never match
keywordMatch = StubMatchingRuleDefinition('2.5.13.33', name=['keywordMatch'], syntax=syntaxes.DirectoryString.oid, kind=MatchingRuleKind.EQUALITY)
numericStringMatch = StringMatchingRuleDefinition('2.5.13.8', name=['numericStringMatch'], syntax=syntaxes.NumericString.oid, matching_type=rfc4518_stringprep.MatchingType.NUMERIC_STRING, kind=MatchingRuleKind.EQUALITY)
numericStringOrderingMatch = StringMatchingRuleDefinition('2.5.13.9', name=['numericStringOrderingMatch'], syntax=syntaxes.NumericString.oid, matching_type=rfc4518_stringprep.MatchingType.NUMERIC_STRING, kind=MatchingRuleKind.ORDERING)
numericStringSubstringsMatch = StringMatchingRuleDefinition('2.5.13.10', name=['numericStringSubstringsMatch'], syntax=syntaxes.SubstringAssertion.oid, compatability_tag=syntaxes.NumericString.oid, matching_type=rfc4518_stringprep.MatchingType.NUMERIC_STRING, kind=MatchingRuleKind.SUBSTR)
objectIdentifierMatch = OIDMatchingRuleDefinition('2.5.13.0', name=['objectIdentifierMatch'], syntax=syntaxes.OID.oid, kind=MatchingRuleKind.EQUALITY)
objectIdentifierFirstComponentMatch = FirstComponentMatchingRuleDefinition('2.5.13.30', name=['objectIdentifierFirstComponentMatch'], syntax=syntaxes.OID.oid, attribute_name='first_component_oid', matching_rule=objectIdentifierMatch, kind=MatchingRuleKind.EQUALITY)
octetStringMatch = GenericMatchingRuleDefinition('2.5.13.17', name=['octetStringMatch'], syntax=syntaxes.OctetString.oid, kind=MatchingRuleKind.EQUALITY)
octetStringOrderingMatch = GenericMatchingRuleDefinition('2.5.13.18', name=['octetStringOrderingMatch'], syntax=syntaxes.OctetString.oid, kind=MatchingRuleKind.ORDERING)
telephoneNumberMatch = StringMatchingRuleDefinition('2.5.13.20', name=['telephoneNumberMatch'], syntax=syntaxes.TelephoneNumber.oid, matching_type=rfc4518_stringprep.MatchingType.TELEPHONE_NUMBER, kind=MatchingRuleKind.EQUALITY)
telephoneNumberSubstringsMatch = StringMatchingRuleDefinition('2.5.13.21', name=['telephoneNumberSubstringsMatch'], syntax=syntaxes.SubstringAssertion.oid, compatability_tag=syntaxes.TelephoneNumber.oid, matching_type=rfc4518_stringprep.MatchingType.TELEPHONE_NUMBER, kind=MatchingRuleKind.SUBSTR)
uniqueMemberMatch = GenericMatchingRuleDefinition('2.5.13.23', name=['uniqueMemberMatch'], syntax=syntaxes.NameAndOptionalUID.oid, kind=MatchingRuleKind.EQUALITY)
# Optional and implementation-specific, we simply never match
wordMatch = StubMatchingRuleDefinition('2.5.13.32', name=['wordMatch'], syntax=syntaxes.DirectoryString.oid, kind=MatchingRuleKind.EQUALITY)

# RFC4523
certificateExactMatch = StubMatchingRuleDefinition('2.5.13.34', name=['certificateExactMatch'], desc='X.509 Certificate Exact Match', syntax='1.3.6.1.1.15.1', kind=MatchingRuleKind.EQUALITY)
certificateMatch = StubMatchingRuleDefinition('2.5.13.35', name=['certificateMatch'], desc='X.509 Certificate Match', syntax='1.3.6.1.1.15.2', kind=MatchingRuleKind.EQUALITY)
certificatePairExactMatch = StubMatchingRuleDefinition('2.5.13.36', name=['certificatePairExactMatch'], desc='X.509 Certificate Pair Exact Match', syntax='1.3.6.1.1.15.3', kind=MatchingRuleKind.EQUALITY)
certificatePairMatch = StubMatchingRuleDefinition('2.5.13.37', name=['certificatePairMatch'], desc='X.509 Certificate Pair Match', syntax='1.3.6.1.1.15.4', kind=MatchingRuleKind.EQUALITY)
certificateListExactMatch = StubMatchingRuleDefinition('2.5.13.38', name=['certificateListExactMatch'], desc='X.509 Certificate List Exact Match', syntax='1.3.6.1.1.15.5', kind=MatchingRuleKind.EQUALITY)
certificateListMatch = StubMatchingRuleDefinition('2.5.13.39', name=['certificateListMatch'], desc='X.509 Certificate List Match', syntax='1.3.6.1.1.15.6', kind=MatchingRuleKind.EQUALITY)
algorithmIdentifierMatch = StubMatchingRuleDefinition('2.5.13.40', name=['algorithmIdentifierMatch'], desc='X.509 Algorithm Identifier Match', syntax='1.3.6.1.1.15.7', kind=MatchingRuleKind.EQUALITY)

# RFC3112
authPasswordExactMatch = StubMatchingRuleDefinition('1.3.6.1.4.1.4203.1.2.2', name=['authPasswordExactMatch'], desc='authentication password exact matching rule', syntax='1.3.6.1.4.1.1466.115.121.1.40', kind=MatchingRuleKind.EQUALITY)
authPasswordMatch = StubMatchingRuleDefinition('1.3.6.1.4.1.4203.1.2.3', name=['authPasswordMatch'], desc='authentication password matching rule', syntax='1.3.6.1.4.1.1466.115.121.1.40', kind=MatchingRuleKind.EQUALITY)

ALL = (
	# RFC4517
	bitStringMatch,
	booleanMatch,
	caseExactIA5Match,
	caseExactMatch,
	caseExactOrderingMatch,
	caseExactSubstringsMatch,
	caseIgnoreIA5Match,
	caseIgnoreIA5SubstringsMatch,
	caseIgnoreListMatch,
	caseIgnoreListSubstringsMatch,
	caseIgnoreMatch,
	caseIgnoreOrderingMatch,
	caseIgnoreSubstringsMatch,
	directoryStringFirstComponentMatch,
	distinguishedNameMatch,
	generalizedTimeMatch,
	generalizedTimeOrderingMatch,
	integerFirstComponentMatch,
	integerMatch,
	integerOrderingMatch,
	keywordMatch,
	numericStringMatch,
	numericStringOrderingMatch,
	numericStringSubstringsMatch,
	objectIdentifierFirstComponentMatch,
	objectIdentifierMatch,
	octetStringMatch,
	octetStringOrderingMatch,
	telephoneNumberMatch,
	telephoneNumberSubstringsMatch,
	uniqueMemberMatch,
	wordMatch,

	# RFC4523
	certificateExactMatch,
	certificateMatch,
	certificatePairExactMatch,
	certificatePairMatch,
	certificateListExactMatch,
	certificateListMatch,
	algorithmIdentifierMatch,

	# RFC3112
	authPasswordExactMatch,
	authPasswordMatch,
)
