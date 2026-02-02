import traceback
import ssl
import socketserver
import typing
import logging
import time
import random
import string
import itertools

from . import asn1, exceptions, ldap, schema, entries

__all__ = ['BaseLDAPRequestHandler', 'LDAPRequestHandler']

def pop_control(controls, oid):
	result = None
	remaining_controls = []
	for control in controls or []:
		if control.controlType == oid:
			result = control
			break
		remaining_controls.append(control)
	return result, remaining_controls

def reject_critical_controls(controls=None):
	for control in controls or []:
		if control.criticality:
			raise exceptions.LDAPUnavailableCriticalExtension()

def mark_last(iterable):
	'''Yield (item, is_last) for all items in iterable

	is_last is True for the last items and False for other items.'''
	prev_item = None
	for item in iterable:
		if prev_item is not None:
			yield prev_item, False
		prev_item = item
	if prev_item is not None:
		yield prev_item, True

def enforce_size_limit(iterable, limit):
	for index, item in enumerate(iterable):
		if index >= limit:
			raise exceptions.LDAPSizeLimitExceeded()
		yield item

class RequestLogAdapter(logging.LoggerAdapter):
	def process(self, msg, kwargs):
		return self.extra['trace_id'] + ': ' + msg, kwargs

class BaseLDAPRequestHandler(socketserver.BaseRequestHandler):
	#: Logger for request processing
	#:
	#: For every connection the logger object is wrapped with a
	#: :any:`logging.LoggerAdapter` that prefixes messages with a unique token
	#: for connetcion tracing.
	logger = logging.getLogger('ldapserver.server')

	def setup(self):
		super().setup()
		self.trace_id = ''.join([random.choice(string.ascii_letters) for _ in range(10)])
		self.logger = RequestLogAdapter(self.logger, {'trace_id': self.trace_id})
		self.keep_running = True

	def handle(self):
		time_connect = time.perf_counter()
		self.logger.info('Connection from %r', self.client_address)
		buf = b''
		while self.keep_running:
			try:
				shallowmsg, buf = ldap.ShallowLDAPMessage.from_ber(buf)
				for respmsg in self.handle_message(shallowmsg):
					self.request.sendall(ldap.LDAPMessage.to_ber(respmsg))
			except asn1.IncompleteBERError:
				chunk = self.request.recv(4096)
				if not chunk:
					self.keep_running = False
					self.request.close()
				else:
					buf += chunk
		self.request.close()
		time_disconnect = time.perf_counter()
		self.logger.info('Disconnected duration_seconds=%.3f', time_disconnect - time_connect)

	def handle_message(self, shallowmsg: ldap.ShallowLDAPMessage) -> typing.Iterable[ldap.LDAPMessage]:
		msgtypes = {
			ldap.BindRequest: (self.handle_bind, ldap.BindResponse),
			ldap.UnbindRequest: (self.handle_unbind, None),
			ldap.SearchRequest: (self.handle_search, ldap.SearchResultDone),
			ldap.ModifyRequest: (self.handle_modify, ldap.ModifyResponse),
			ldap.AddRequest: (self.handle_add,  ldap.AddResponse),
			ldap.DelRequest: (self.handle_delete, ldap.DelResponse),
			ldap.ModifyDNRequest: (self.handle_modifydn, ldap.ModifyDNResponse),
			ldap.CompareRequest: (self.handle_compare, ldap.CompareResponse),
			ldap.AbandonRequest: (self.handle_abandon, None),
			ldap.ExtendedRequest: (self.handle_extended, ldap.ExtendedResponse),
		}
		handler, response_type = msgtypes.get(shallowmsg.protocolOpType, (None, None))
		try:
			if handler is None:
				raise exceptions.LDAPProtocolError()
			try:
				msg = shallowmsg.decode()[0]
			except ValueError as e:
				self.logger.error('Could not decode message %s, ignoring', shallowmsg)
				raise exceptions.LDAPProtocolError() from e
			for args in handler(msg.protocolOp, msg.controls):
				response, controls = args if isinstance(args, tuple) else (args, None)
				yield ldap.LDAPMessage(shallowmsg.messageID, response, controls)
		except exceptions.LDAPError as e:
			if response_type is not None:
				respmsg = ldap.LDAPMessage(shallowmsg.messageID, response_type(e.code, diagnosticMessage=e.message))
				yield respmsg
				self.logger.info('Operation aborted, responded with result code "%s" msg="%s"', e.code.name, e.message)
		except Exception as e: # pylint: disable=broad-except
			if response_type is not None:
				respmsg = ldap.LDAPMessage(shallowmsg.messageID, response_type(ldap.LDAPResultCode.other))
				yield respmsg
				self.logger.exception('Uncaught exception, responded with result code "other"')
			else:
				self.logger.exception('Uncaught exception, ignored request')

	def handle_bind(self, op: ldap.BindRequest, controls=None) -> typing.Iterable[ldap.ProtocolOp]:
		self.logger.info('BIND %s', op)
		reject_critical_controls(controls)
		raise exceptions.LDAPAuthMethodNotSupported()

	def handle_unbind(self, op: ldap.UnbindRequest, controls=None) -> typing.NoReturn:
		self.logger.info('UNBIND %s', op)
		reject_critical_controls(controls)
		self.keep_running = False
		return []

	def handle_search(self, op: ldap.SearchRequest, controls=None) -> typing.Iterable[ldap.ProtocolOp]:
		self.logger.info('SEARCH %s', op)
		reject_critical_controls(controls)
		yield ldap.SearchResultDone(ldap.LDAPResultCode.success)

	def handle_modify(self, op: ldap.ModifyRequest, controls=None) -> typing.Iterable[ldap.ProtocolOp]:
		self.logger.info('MODIFY %s', op)
		reject_critical_controls(controls)
		raise exceptions.LDAPInsufficientAccessRights()

	def handle_add(self, op: ldap.AddRequest, controls=None) -> typing.Iterable[ldap.ProtocolOp]:
		self.logger.info('ADD %s', op)
		reject_critical_controls(controls)
		raise exceptions.LDAPInsufficientAccessRights()

	def handle_delete(self, op: ldap.DelRequest, controls=None) -> typing.Iterable[ldap.ProtocolOp]:
		self.logger.info('DELETE %s', op)
		reject_critical_controls(controls)
		raise exceptions.LDAPInsufficientAccessRights()

	def handle_modifydn(self, op: ldap.ModifyDNRequest, controls=None) -> typing.Iterable[ldap.ProtocolOp]:
		self.logger.info('MODIFYDN %s', op)
		reject_critical_controls(controls)
		raise exceptions.LDAPInsufficientAccessRights()

	def handle_compare(self, op: ldap.CompareRequest, controls=None) -> typing.Iterable[ldap.ProtocolOp]:
		self.logger.info('COMPRAE %s', op)
		reject_critical_controls(controls)
		raise exceptions.LDAPInsufficientAccessRights()

	def handle_abandon(self, op: ldap.AbandonRequest, controls=None) -> typing.NoReturn:
		self.logger.info('ABANDON %s', op)
		reject_critical_controls(controls)

	def handle_extended(self, op: ldap.ExtendedRequest, controls=None) -> typing.Iterable[ldap.ProtocolOp]:
		self.logger.info('EXTENDED %s', op)
		reject_critical_controls(controls)
		raise exceptions.LDAPProtocolError()

class LDAPRequestHandler(BaseLDAPRequestHandler):
	#: :class:`SubschemaSubentry` object that describes the schema. Default
	#: value uses :any:`schema.RFC4519_SCHEMA`. Returned by :any:`do_search`.
	subschema = entries.SubschemaSubentry(schema.RFC4519_SCHEMA, 'cn=Subschema', cn=['Subschema'])

	#: :class:`RootDSE` object containing information about the server, such
	#: as supported extentions and SASL authentication mechansims. Content is
	#: determined on setup based on the `supports_*` attributes. Returned by
	#: :any:`do_search`.
	rootdse: typing.Any

	#: Opaque bind/authorization state. Initially `None` and set to `None` on
	#: anonymous bind. Set to whatever the `do_bind_*` callbacks return.
	bind_object: typing.Any

	def setup(self):
		super().setup()
		self.rootdse = self.subschema.RootDSE()
		self.rootdse['objectClass'] = ['top']
		if self.supports_starttls:
			self.rootdse['supportedExtension'].append(ldap.STARTTLS_OID)
		if self.supports_whoami:
			self.rootdse['supportedExtension'].append(ldap.WHOAMI_OID)
		if self.supports_password_modify:
			self.rootdse['supportedExtension'].append(ldap.PASSWORD_MODIFY_OID)
		if self.supports_paged_results:
			self.rootdse['supportedControl'].append(ldap.PAGED_RESULTS_OID)
		if self.supports_sasl_anonymous:
			self.rootdse['supportedSASLMechanisms'].append('ANONYMOUS')
		if self.supports_sasl_plain:
			self.rootdse['supportedSASLMechanisms'].append('PLAIN')
		if self.supports_sasl_external:
			self.rootdse['supportedSASLMechanisms'].append('EXTERNAL')
		self.rootdse['supportedFeatures'].append(ldap.ALL_OPERATIONAL_ATTRS_OID)
		self.rootdse['supportedFeatures'].append(ldap.ABSOLUTE_TRUE_FALSE_OID)
		self.rootdse['supportedLDAPVersion'] = ['3']
		self.bind_object = None
		self.__bind_sasl_state = None # Set to (mechanism, iterator) by handle_bind
		self.__paged_searches = {} # pagination cookie -> (iterator, orig_op)
		self.__paged_cookie_counter = 0 # Used to generate unique cookie values

	def handle_bind(self, op, controls=None):
		reject_critical_controls(controls)
		if op.version != 3:
			raise exceptions.LDAPProtocolError('Unsupported protocol version')
		auth = op.authentication
		# Resume ongoing SASL dialog
		if self.__bind_sasl_state and isinstance(auth, ldap.SaslCredentials) \
				and auth.mechanism == self.__bind_sasl_state[0]:
			mechanism, iterator = self.__bind_sasl_state
			self.__bind_sasl_state = None
			resp_code = ldap.LDAPResultCode.saslBindInProgress
			try:
				resp = iterator.send(auth.credentials)
				self.__bind_sasl_state = (mechanism, iterator)
			except StopIteration as e:
				resp_code = ldap.LDAPResultCode.success
				self.bind_object, resp = e.value # pylint: disable=unpacking-non-sequence
			yield ldap.BindResponse(resp_code, serverSaslCreds=resp)
			return
		# If auth type or SASL method changed, abort SASL dialog
		self.__bind_sasl_state = None
		if isinstance(auth, ldap.SimpleAuthentication):
			self.logger.info('BIND dn=%r', op.name)
			self.bind_object = self.do_bind_simple(op.name, auth.password)
			yield ldap.BindResponse(ldap.LDAPResultCode.success)
		elif isinstance(auth, ldap.SaslCredentials):
			ret = self.do_bind_sasl(auth.mechanism, auth.credentials)
			if isinstance(ret, tuple):
				self.bind_object, resp = ret
				yield ldap.BindResponse(ldap.LDAPResultCode.success, serverSaslCreds=resp)
				return
			iterator = iter(ret)
			resp_code = ldap.LDAPResultCode.saslBindInProgress
			try:
				resp = next(iterator)
				self.__bind_sasl_state = (auth.mechanism, iterator)
			except StopIteration as e:
				resp_code = ldap.LDAPResultCode.success
				self.bind_object, resp = e.value # pylint: disable=unpacking-non-sequence
			yield ldap.BindResponse(resp_code, serverSaslCreds=resp)
		else:
			yield from super().handle_bind(op, controls) # pylint: disable=not-an-iterable

	def do_bind_simple(self, dn='', password=b''):
		'''Do LDAP BIND with simple authentication

		:param dn: Distinguished name of object to be authenticated, may be empty
		:type dn: str
		:param password: Password, may be empty
		:type password: bytes

		:returns: Bind object
		:rtype: obj

		Delegates implementation to :any:`do_bind_simple_anonymous`,
		:any:`do_bind_simple_unauthenticated` or :any:`do_bind_simple_authenticated`
		according to `RFC 4513`_.'''
		if not dn and not password:
			return self.do_bind_simple_anonymous()
		if not password:
			return self.do_bind_simple_unauthenticated(dn)
		return self.do_bind_simple_authenticated(dn, password)

	def do_bind_simple_anonymous(self):
		'''Do LDAP BIND with simple anonymous authentication (`RFC 4513 5.1.1.`_)

		:raises exceptions.LDAPInvalidCredentials: if authentication failed
		:returns: Bind object on success (see :any:`bind_object`)

		The default implementation always returns None.'''
		return None

	def do_bind_simple_unauthenticated(self, dn):
		'''Do LDAP BIND with simple unauthenticated authentication (`RFC 4513 5.1.2.`_)

		:param dn: DN of the object to be authenticated as
		:type dn: str
		:raises exceptions.LDAPInvalidCredentials: if authentication failed
		:returns: Bind object on success (see :any:`bind_object`)

		The default implementation always raises :any:`LDAPInvalidCredentials`.'''
		raise exceptions.LDAPInvalidCredentials()

	def do_bind_simple_authenticated(self, dn, password):
		'''Do LDAP BIND with simple name/password authentication (`RFC 4513 5.1.3.`_)

		:param dn: Distinguished name of the object to be authenticated
		:type dn: str
		:param password: Password for object
		:type password: bytes
		:raises exceptions.LDAPInvalidCredentials: if authentication failed
		:returns: Bind object on success (see :any:`bind_object`)

		The default implementation always raises :any:`LDAPInvalidCredentials`.'''
		raise exceptions.LDAPInvalidCredentials()

	def do_bind_sasl(self, mechanism, credentials=None, dn=None):
		'''Do LDAP BIND with SASL authentication (RFC 4513 and 4422)

		:param mechanism: Name of the selected SASL mechanism
		:type mechanism: str
		:param credentials: Initial client response
		:type credentials: bytes, optional
		:param dn: Distinguished name in LDAP BIND request, should be ignored for
		           SASL authentication
		:type dn: str, optional

		:returns: Bind object and final server challenge, only returns on success
		:rtype: Tuple (obj, bytes/None)

		The call only returns if authentication succeeded. In any other case,
		an appropriate :any:`exceptions.LDAPError` is raised.

		Some SASL methods require additional challenge-response round trips. These
		can be achieved with the `yield` statement:

		    client_response = yield server_challenge

		Generally all server challenges and client responses can always be absent
		(indicated by None), empty (empty bytes object) or consist of any number
		of bytes. Whether a challenge or response may or must be absent or present
		is defined by the individual SASL mechanism.

		IANA list of SASL mechansims: https://www.iana.org/assignments/sasl-mechanisms/sasl-mechanisms.xhtml
		'''
		if not mechanism:
			# Request to abort current negotiation (RFC4513 5.2.1.2)
			raise exceptions.LDAPAuthMethodNotSupported()
		if mechanism == 'ANONYMOUS' and self.supports_sasl_anonymous:
			self.logger.info('BIND SASL ANONYMOUS')
			if credentials is not None:
				credentials = credentials.decode()
			return self.do_bind_sasl_anonymous(trace_info=credentials), None
		if mechanism == 'PLAIN' and self.supports_sasl_plain:
			if credentials is None:
				raise exceptions.LDAPProtocolError('Unsupported protocol version')
			authzid, authcid, password = credentials.split(b'\0', 2)
			self.logger.info('BIND SASL PLAIN authcid=%r', authcid)
			return self.do_bind_sasl_plain(authcid.decode(), password.decode(), authzid.decode() or None), None
		if mechanism == 'EXTERNAL' and self.supports_sasl_external:
			if credentials is not None:
				credentials = credentials.decode()
			self.logger.info('BIND SASL EXTERNAL')
			return self.do_bind_sasl_external(authzid=credentials), None
		raise exceptions.LDAPAuthMethodNotSupported()

	#: Indicate SASL "ANONYMOUS" support
	supports_sasl_anonymous = False

	def do_bind_sasl_anonymous(self, trace_info=None):
		'''Do LDAP BIND with SASL "ANONYMOUS" mechanism (RFC 4505)

		:param trace_info: Trace information, either an email address or an
		                   opaque string that does not contain the '@' character
		:type trace_info: str, optional

		:raises exceptions.LDAPError: if authentication failed

		:returns: Bind object on success
		:rtype: obj

		Only called if :any:`supports_sasl_anonymous` is True.
		The default implementation raises :any:`LDAPAuthMethodNotSupported`.'''
		raise exceptions.LDAPAuthMethodNotSupported()

	#: Indicate SASL "PLAIN" support
	supports_sasl_plain = False

	def do_bind_sasl_plain(self, identity, password, authzid=None):
		'''Do LDAP BIND with SASL "PLAIN" mechanism (RFC 4616)

		:param identity: Authentication identity (authcid)
		:type identity: str
		:param password: Password (passwd)
		:type password: str
		:param authzid: Authorization identity
		:type authzid: str, optional

		:raises exceptions.LDAPError: if authentication failed

		:returns: Bind object on success
		:rtype: obj

		Only called if :any:`supports_sasl_plain` is True.
		The default implementation raises :any:`LDAPAuthMethodNotSupported`.'''
		raise exceptions.LDAPAuthMethodNotSupported()

	#: Indicate SASL "EXTERNAL" support
	supports_sasl_external = False

	def do_bind_sasl_external(self, authzid=None):
		'''Do LDAP BIND with SASL "EXTERNAL" mechanism (RFC 4422 and 4513)

		:param authzid: Authorization identity
		:type authzid: str, optional

		:raises exceptions.LDAPError: if authentication failed

		:returns: Bind object on success
		:rtype: obj

		EXTERNAL is commonly used for TLS client certificate authentication or
		system user based authentication on UNIX sockets.

		Only called if :any:`supports_sasl_external` is True.
		The default implementation raises :any:`LDAPAuthMethodNotSupported`.'''
		raise exceptions.LDAPAuthMethodNotSupported()

	#: Enable/disable support for "Simple Paged Results Manipulation" control
	#: (RFC2696). Paginated search uses :any:`do_search` like non-paginated
	#: search does.
	supports_paged_results = True

	def __handle_search_paged(self, op, paged_control, controls=None):
		def build_control(size=0, cookie=b''):
			value = ldap.PagedResultsValue(size=size, cookie=cookie)
			return ldap.Control(controlType=ldap.PAGED_RESULTS_OID,
			                    criticality=True, controlValue=bytes(value))

		# pylint: disable=no-member
		paged_control = ldap.PagedResultsValue.from_ber(paged_control.controlValue)[0]
		if not paged_control.cookie: # New paged search request
			results = self.do_search(op.baseObject, op.scope, op.filter)
			results = map(lambda obj: obj.search(op.baseObject, op.scope, op.filter, op.attributes, op.typesOnly), results)
			results = filter(None, results)
			results = mark_last(results)
			if op.sizeLimit:
				results = enforce_size_limit(results, op.sizeLimit)
			iterator = iter(results)
		else: # Continue existing paged search
			try:
				iterator, orig_op = self.__paged_searches.pop(paged_control.cookie)
			except KeyError as exc:
				raise exceptions.LDAPUnwillingToPerform('Invalid pagination cookie') from exc
			if ldap.ProtocolOp.to_ber(orig_op) != ldap.ProtocolOp.to_ber(op):
				raise exceptions.LDAPUnwillingToPerform('Search parameter mismatch')
			if not paged_control.size: # Cancel paged search
				yield ldap.SearchResultDone(ldap.LDAPResultCode.success), [build_control()]
				return
		is_last = True
		result_count = 0
		time_start = time.perf_counter()
		for entry, is_last in itertools.islice(iterator, 0, paged_control.size):
			self.logger.debug('SEARCH entry %r', entry)
			result_count += 1
			yield entry
		cookie = b''
		if not is_last:
			cookie = str(self.__paged_cookie_counter).encode()
			self.__paged_cookie_counter += 1
			self.__paged_searches[cookie] = iterator, op
		yield ldap.SearchResultDone(ldap.LDAPResultCode.success), [build_control(cookie=cookie)]
		time_end = time.perf_counter()
		self.logger.info('SEARCH dn=%r dn_scope=%s filter=%s attributes=%r page_cookie=%r result_count=%d duration_seconds=%.3f',
		                 op.baseObject, op.scope.name, op.filter, ' '.join(op.attributes), cookie, result_count, time_end - time_start)

	def handle_search(self, op, controls=None):
		self.logger.debug('SEARCH request dn=%r dn_scope=%s filter=%r attributes=%r',
		                  op.baseObject, op.scope.name, str(op.filter), ' '.join(op.attributes))
		paged_control = None
		if self.supports_paged_results:
			paged_control, controls = pop_control(controls, ldap.PAGED_RESULTS_OID)
		reject_critical_controls(controls)
		if paged_control:
			yield from self.__handle_search_paged(op, paged_control, controls)
			return
		result_count = 0
		time_start = time.perf_counter()
		for obj in self.do_search(op.baseObject, op.scope, op.filter):
			entry = obj.search(op.baseObject, op.scope, op.filter, op.attributes, op.typesOnly)
			if entry:
				if op.sizeLimit and result_count >= op.sizeLimit:
					raise exceptions.LDAPSizeLimitExceeded()
				self.logger.debug('SEARCH entry %r', entry)
				result_count += 1
				yield entry
		yield ldap.SearchResultDone(ldap.LDAPResultCode.success)
		time_end = time.perf_counter()
		self.logger.info('SEARCH dn=%r dn_scope=%s filter=\'%s\' attributes=%r result_count=%d duration_seconds=%.3f',
		                 op.baseObject, op.scope.name, op.filter, ' '.join(op.attributes), result_count, time_end - time_start)

	def do_search(self, baseobj, scope, filterobj):
		'''Return result candidates for a SEARCH operation

		:param baseobj: Distinguished name of the LDAP entry relative to which the
		                search is to be performed
		:type baseobj: str
		:param scope: Search scope
		:type scope: ldap.SearchScope
		:param filterobj: Filter object
		:type filterobj: ldap.Filter
		:raises exceptions.LDAPError: on error
		:returns: All entries that might match the parameters of the SEARCH
		          operation.
		:rtype: Iterable of :class:`Entry`

		The default implementation yields :any:`rootdse` and :any:`subschema`.
		Both are importent for feature detection, so make sure to also return
		them (e.g. with ``yield from super().do_search(...)``).

		For every returned object :any:`Entry.search` is called to filter out
		non-matching entries and to construct the response.

		Note that if this method is as an iterator, its execution may be paused
		for extended periods of time or aborted prematurly.'''
		yield self.rootdse
		yield self.subschema

	def handle_compare(self, op, controls=None):
		self.logger.info('COMPRAE request "%s" %s=%s', op.entry, op.ava.attributeDesc, repr(op.ava.assertionValue))
		obj = self.do_compare(op.entry, op.ava.attributeDesc, op.ava.assertionValue)
		if obj is not None:
			if obj.compare(op.entry, op.ava.attributeDesc, op.ava.assertionValue):
				return [ldap.CompareResponse(ldap.LDAPResultCode.compareTrue)]
			else:
				return [ldap.CompareResponse(ldap.LDAPResultCode.compareFalse)]
		raise exceptions.LDAPNoSuchObject()

	def do_compare(self, dn, attribute, value):
		'''Lookup object for COMPARE operation

		:param dn: Distinguished name of the LDAP entry
		:type dn: str
		:param attribute: Attribute type
		:type attribute: str
		:param value: Attribute value
		:type value: bytes
		:raises exceptions.LDAPError: on error
		:returns: `Entry` or None

		The default implementation calls `do_search` and returns the first object
		for which :any:`Entry.compare` does not raise
		:any:`exceptions.LDAPNoSuchObject` (i.e. the object has the requested DN).'''
		objs = self.do_search(dn, ldap.SearchScope.baseObject, ldap.FilterPresent(attribute='objectClass'))
		for obj in objs:
			try:
				obj.compare(dn, attribute, value)
				return obj
			except exceptions.LDAPNoSuchObject:
				pass
			except exceptions.LDAPError:
				return obj
		raise exceptions.LDAPNoSuchObject()

	def handle_unbind(self, op, controls=None):
		self.logger.info('UNBIND')
		reject_critical_controls(controls)
		self.keep_running = False
		return []

	def handle_extended(self, op, controls=None):
		reject_critical_controls(controls)
		if op.requestName == ldap.STARTTLS_OID and self.supports_starttls:
			self.logger.info('EXTENDED STARTTLS')
			# StartTLS (RFC 4511)
			yield ldap.ExtendedResponse(ldap.LDAPResultCode.success, responseName=ldap.STARTTLS_OID)
			try:
				self.do_starttls()
			except Exception: # pylint: disable=broad-except
				traceback.print_exc()
				self.keep_running = False
			if ldap.STARTTLS_OID in self.rootdse['supportedExtension']:
				self.rootdse['supportedExtension'].remove(ldap.STARTTLS_OID)
		elif op.requestName == ldap.WHOAMI_OID and self.supports_whoami:
			self.logger.info('EXTENDED WHOAMI')
			# "Who am I?" Operation (RFC 4532)
			identity = (self.do_whoami() or '').encode()
			yield ldap.ExtendedResponse(ldap.LDAPResultCode.success, responseValue=identity)
		elif op.requestName == ldap.PASSWORD_MODIFY_OID and self.supports_password_modify:
			self.logger.info('EXTENDED PASSWORD_MODIFY')
			# Password Modify Extended Operation (RFC 3062)
			newpw = None
			if op.requestValue is None:
				newpw = self.do_password_modify()
			else:
				decoded, _ = ldap.PasswdModifyRequestValue.from_ber(op.requestValue)
				# pylint: disable=no-member
				newpw = self.do_password_modify(decoded.userIdentity, decoded.oldPasswd, decoded.newPasswd)
			if newpw is None:
				yield ldap.ExtendedResponse(ldap.LDAPResultCode.success)
			else:
				encoded = ldap.PasswdModifyResponseValue.to_ber(ldap.PasswdModifyResponseValue(newpw))
				yield ldap.ExtendedResponse(ldap.LDAPResultCode.success, responseValue=encoded)
		else:
			self.logger.warning('Unsupported or disabled EXTENDED operation %r', op.requestName)
			yield from super().handle_extended(op, controls) # pylint: disable=not-an-iterable

	#: :any:`ssl.SSLContext` for StartTLS
	ssl_context = None

	@property
	def supports_starttls(self):
		'''
		'''
		return self.ssl_context is not None and not isinstance(self.request, ssl.SSLSocket)

	def do_starttls(self):
		'''Do StartTLS extended operation (RFC 4511)

		Called by `handle_extended()` if :any:`supports_starttls` is True. The default
		implementation uses `ssl_context`.

		Note that the (success) response to the request is sent before this method
		is called. If a call to this method fails, the LDAP connection is
		immediately terminated.'''
		self.request = self.ssl_context.wrap_socket(self.request, server_side=True)

	#:
	supports_whoami = False

	def do_whoami(self):
		'''Do "Who am I?" extended operation (RFC 4532)

		:returns: Current authorization identity (authzid) or empty string for anonymous sessions
		:rtype: str

		Called by `handle_extended()` if `supports_whoami` is True. The default
		implementation always returns an empty string.'''
		return ''

	#:
	supports_password_modify = False

	def do_password_modify(self, user=None, old_password=None, new_password=None):
		'''Do password modify extended operation (RFC 3062)

		:param user: User the request relates to, may or may not be a
		             distinguished name. If absent, the request relates to the
		             user currently associated with the LDAP connection
		:type user: str, optional
		:param old_password: Current password of user
		:type old_password: bytes, optional
		:param new_password: Desired password for user
		:type new_password: bytes, optional

		Called by `handle_extended()` if :any:`supports_password_modify` is True. The
		default implementation always raises an :any:`LDAPUnwillingToPerform` error.'''
		raise exceptions.LDAPUnwillingToPerform()
