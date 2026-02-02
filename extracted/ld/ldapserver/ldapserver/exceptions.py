from .ldap import LDAPResultCode

class LDAPError(Exception):
	'''Base class for all LDAP errors'''

	RESULT_CODE: LDAPResultCode

	def __init__(self, message=''):
		super().__init__()
		self.code = self.RESULT_CODE
		self.message = message

#class LDAPSuccess(LDAPError):
#	RESULT_CODE = LDAPResultCode.success

class LDAPOperationsError(LDAPError):
	'''Indicates that the operation is not properly sequenced with relation to
	other operations (of same or different type). (RFC 4511)'''
	RESULT_CODE = LDAPResultCode.operationsError

class LDAPProtocolError(LDAPError):
	'''Indicates the server received data that is not well-formed. (RFC 4511)'''
	RESULT_CODE = LDAPResultCode.protocolError

class LDAPTimeLimitExceeded(LDAPError):
	'''Indicates that the time limit specified by the client was
	exceeded before the operation could be completed. (RFC 4511)'''
	RESULT_CODE = LDAPResultCode.timeLimitExceeded

class LDAPSizeLimitExceeded(LDAPError):
	'''Indicates that the size limit specified by the client was
	exceeded before the operation could be completed. (RFC 4511)'''
	RESULT_CODE = LDAPResultCode.sizeLimitExceeded

#class LDAPCompareFalse(LDAPError):
#	RESULT_CODE = LDAPResultCode.compareFalse

#class LDAPCompareTrue(LDAPError):
#	RESULT_CODE = LDAPResultCode.compareTrue

class LDAPAuthMethodNotSupported(LDAPError):
	'''Indicates that the authentication method or mechanism is not
	supported. (RFC 4511)'''
	RESULT_CODE = LDAPResultCode.authMethodNotSupported

class LDAPStrongerAuthRequired(LDAPError):
	'''Indicates the server requires strong(er) authentication in
	order to complete the operation. (RFC 4511)'''
	RESULT_CODE = LDAPResultCode.strongerAuthRequired

#class LDAPReferral(LDAPError):
#	RESULT_CODE = LDAPResultCode.referral

class LDAPAdminLimitExceeded(LDAPError):
	'''Indicates that an administrative limit has been exceeded. (RFC 4511)'''
	RESULT_CODE = LDAPResultCode.adminLimitExceeded

class LDAPUnavailableCriticalExtension(LDAPError):
	'''Indicates a critical control is unrecognized. (RFC 4511)'''
	RESULT_CODE = LDAPResultCode.unavailableCriticalExtension

class LDAPConfidentialityRequired(LDAPError):
	'''Indicates that data confidentiality protections are required. (RFC 4511)'''
	RESULT_CODE = LDAPResultCode.confidentialityRequired

#class LDAPSaslBindInProgress(LDAPError):
#	RESULT_CODE = LDAPResultCode.saslBindInProgress

class LDAPNoSuchAttribute(LDAPError):
	'''Indicates that the named entry does not contain the specified
	attribute or attribute value. (RFC 4511)'''
	RESULT_CODE = LDAPResultCode.noSuchAttribute

class LDAPUndefinedAttributeType(LDAPError):
	'''Indicates that a request field contains an unrecognized
	attribute description. (RFC 4511)'''
	RESULT_CODE = LDAPResultCode.undefinedAttributeType

class LDAPInappropriateMatching(LDAPError):
	'''Indicates that an attempt was made (e.g., in an assertion) to
	use a matching rule not defined for the attribute type
	concerned. (RFC 4511)'''
	RESULT_CODE = LDAPResultCode.inappropriateMatching

class LDAPConstraintViolation(LDAPError):
	'''Indicates that the client supplied an attribute value that
	does not conform to the constraints placed upon it by the
	data model. (RFC 4511)'''
	RESULT_CODE = LDAPResultCode.constraintViolation

class LDAPAttributeOrValueExists(LDAPError):
	'''Indicates that the client supplied an attribute or value to
	be added to an entry, but the attribute or value already
	exists. (RFC 4511)'''
	RESULT_CODE = LDAPResultCode.attributeOrValueExists

class LDAPInvalidAttributeSyntax(LDAPError):
	''' Indicates that a purported attribute value does not conform
 to the syntax of the attribute. (RFC 4511)'''
	RESULT_CODE = LDAPResultCode.invalidAttributeSyntax

class LDAPNoSuchObject(LDAPError):
	'''Indicates that the object does not exist in the DIT. (RFC 4511)'''
	RESULT_CODE = LDAPResultCode.noSuchObject

class LDAPAliasProblem(LDAPError):
	'''Indicates that an alias problem has occurred. For example,
	the code may used to indicate an alias has been dereferenced
	that names no object. (RFC 4511)'''
	RESULT_CODE = LDAPResultCode.aliasProblem

class LDAPInvalidDNSyntax(LDAPError):
	'''Indicates that an LDAPDN or RelativeLDAPDN field (e.g., search
	base, target entry, ModifyDN newrdn, etc.) of a request does
	not conform to the required syntax or contains attribute
	values that do not conform to the syntax of the attribute's
	type. (RFC 4511)'''
	RESULT_CODE = LDAPResultCode.invalidDNSyntax

class LDAPAliasDereferencingProblem(LDAPError):
	'''Indicates that a problem occurred while dereferencing an
	alias.  Typically, an alias was encountered in a situation
	where it was not allowed or where access was denied. (RFC 4511)'''
	RESULT_CODE = LDAPResultCode.aliasDereferencingProblem

class LDAPInappropriateAuthentication(LDAPError):
	'''Indicates the server requires the client that had attempted
	to bind anonymously or without supplying credentials to
	provide some form of credentials. (RFC 4511)'''
	RESULT_CODE = LDAPResultCode.inappropriateAuthentication

class LDAPInvalidCredentials(LDAPError):
	'''Indicates that the provided credentials (e.g., the user's name
	and password) are invalid. (RFC 4511)'''
	RESULT_CODE = LDAPResultCode.invalidCredentials

class LDAPInsufficientAccessRights(LDAPError):
	'''Indicates that the client does not have sufficient access
	rights to perform the operation. (RFC 4511)'''
	RESULT_CODE = LDAPResultCode.insufficientAccessRights

class LDAPBusy(LDAPError):
	'''Indicates that the server is too busy to service the
	operation. (RFC 4511)'''
	RESULT_CODE = LDAPResultCode.busy

class LDAPUnavailable(LDAPError):
	'''Indicates that the server is shutting down or a subsystem
	necessary to complete the operation is offline. (RFC 4511)'''
	RESULT_CODE = LDAPResultCode.unavailable

class LDAPUnwillingToPerform(LDAPError):
	'''Indicates that the server is unwilling to perform the
	operation. (RFC 4511)'''
	RESULT_CODE = LDAPResultCode.unwillingToPerform

class LDAPLoopDetect(LDAPError):
	'''Indicates that the server has detected an internal loop (e.g.,
	while dereferencing aliases or chaining an operation). (RFC 4511)'''
	RESULT_CODE = LDAPResultCode.loopDetect

class LDAPNamingViolation(LDAPError):
	'''Indicates that the entry's name violates naming restrictions. (RFC 4511)'''
	RESULT_CODE = LDAPResultCode.namingViolation

class LDAPObjectClassViolation(LDAPError):
	'''Indicates that the entry violates object class restrictions. (RFC 4511)'''
	RESULT_CODE = LDAPResultCode.objectClassViolation

class LDAPNotAllowedOnNonLeaf(LDAPError):
	'''Indicates that the operation is inappropriately acting upon a
	non-leaf entry. (RFC 4511)'''
	RESULT_CODE = LDAPResultCode.notAllowedOnNonLeaf

class LDAPNotAllowedOnRDN(LDAPError):
	'''Indicates that the operation is inappropriately attempting to
	remove a value that forms the entry's relative distinguished
	name. (RFC 4511)'''
	RESULT_CODE = LDAPResultCode.notAllowedOnRDN

class LDAPEntryAlreadyExists(LDAPError):
	'''Indicates that the request cannot be fulfilled (added, moved,
	or renamed) as the target entry already exists. (RFC 4511)'''
	RESULT_CODE = LDAPResultCode.entryAlreadyExists

class LDAPObjectClassModsProhibited(LDAPError):
	'''Indicates that an attempt to modify the object class(es) of
	an entry's 'objectClass' attribute is prohibited. (RFC 4511)'''
	RESULT_CODE = LDAPResultCode.objectClassModsProhibited

class LDAPAffectsMultipleDSAs(LDAPError):
	'''Indicates that the operation cannot be performed as it would
	affect multiple servers (DSAs). (RFC 4511)'''
	RESULT_CODE = LDAPResultCode.affectsMultipleDSAs

class LDAPOther(LDAPError):
	'''Indicates the server has encountered an internal error. (RFC 4511)'''
	RESULT_CODE = LDAPResultCode.other
