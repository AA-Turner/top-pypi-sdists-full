##
# Copyright (c) 2006-2013 Apple Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##

"""
PyKerberos Function Description.
"""

class KrbError(Exception):
    pass

class BasicAuthError(KrbError):
    pass

class GSSError(KrbError):
    pass

def checkPassword(user, pswd, service, default_realm, verify=True):
    """
    This function provides a simple way to verify that a user name and password match
    those normally used for Kerberos authentication. It does this by checking that the
    supplied user name and password can be used to get a ticket for the supplied service.
    If the user name does not contain a realm, then the default realm supplied is used.

    NB For this to work properly the Kerberos must be configured properly on this machine.
    That will likely mean ensuring that the edu.mit.Kerberos preference file has the correct
    realms and KDCs listed.

    @param user:          a string containing the Kerberos user name. A realm may be
        included by appending an '@' followed by the realm string to the actual user id.
        If no realm is supplied, then the realm set in the default_realm argument will
        be used.
    @param pswd:          a string containing the password for the user.
    @param service:       a string containging the Kerberos service to check access for.
        This will be of the form 'sss/xx.yy.zz', where 'sss' is the service identifier
        (e.g., 'http', 'krbtgt'), and 'xx.yy.zz' is the hostname of the server.
    @param default_realm: a string containing the default realm to use if one is not
        supplied in the user argument. Note that Kerberos realms are normally all
        uppercase (e.g., 'EXAMPLE.COM').
    @param verify: a boolean flagging KDC verification as enabled or disabled
        (default: True, i.e. enabled).
    @return:              True if authentication succeeds, False otherwise.
    """

def changePassword(user, oldpswd, newpswd):
    """
    This function allows to change the user password on the KDC.

    @param user:          a string containing the Kerberos user name. A realm may be
        included by appending an '@' followed by the realm string to the actual user id.
        If no realm is supplied, then the realm set in the default_realm argument will
        be used.
    @param oldpswd:       a string containing the old (current) password for the user.
    @param newpswd:       a string containging the new password for the user.
    @return:              True if password changing succeeds, False otherwise.
    """

def getServerPrincipalDetails(service, hostname):
    """
    This function returns the service principal for the server given a service type
    and hostname. Details are looked up via the /etc/keytab file.

    @param service:       a string containing the Kerberos service type for the server.
    @param hostname:      a string containing the hostname of the server.
    @return:              a string containing the service principal.
    """

"""
GSSAPI Function Result Codes:

    -1 : Error
    0  : GSSAPI step continuation (only returned by 'Step' function)
    1  : GSSAPI step complete, or function return OK

"""

# Some useful result codes
AUTH_GSS_CONTINUE     = 0
AUTH_GSS_COMPLETE     = 1

# Some useful gss flags
GSS_C_DELEG_FLAG      = 1
GSS_C_MUTUAL_FLAG     = 2
GSS_C_REPLAY_FLAG     = 4
GSS_C_SEQUENCE_FLAG   = 8
GSS_C_CONF_FLAG       = 16
GSS_C_INTEG_FLAG      = 32
GSS_C_ANON_FLAG       = 64
GSS_C_PROT_READY_FLAG = 128
GSS_C_TRANS_FLAG      = 256

def authGSSClientInit(service, principal=None, gssflags=GSS_C_MUTUAL_FLAG|GSS_C_SEQUENCE_FLAG, mech_oid=None):
    """
    Initializes a context for GSSAPI client-side authentication with the given service principal.
    authGSSClientClean must be called after this function returns an OK result to dispose of
    the context once all GSSAPI operations are complete.

    @param service: a string containing the service principal in the form 'type@fqdn'
        (e.g. 'imap@mail.apple.com').
    @param principal: optional string containing the client principal in the form 'user@realm'
        (e.g. 'jdoe@example.com').
    @param gssflags: optional integer used to set GSS flags.
        (e.g.  GSS_C_DELEG_FLAG|GSS_C_MUTUAL_FLAG|GSS_C_SEQUENCE_FLAG will allow
        for forwarding credentials to the remote host)
    @param mech_oid: Optional GSS mech OID. Defaults to None (GSS_C_NO_OID).
        Other possible values are GSS_MECH_OID_KRB5, GSS_MECH_OID_SPNEGO.
    @return: a tuple of (result, context) where result is the result code (see above) and
        context is an opaque value that will need to be passed to subsequent functions.
    """

def authGSSClientClean(context):
    """
    Destroys the context for GSSAPI client-side authentication. This function is provided for API
    compatibility with original pykerberos but does nothing. The context object destroys itself
    when it is reclaimed.

    @param context: the context object returned from authGSSClientInit.
    @return: a result code (see above).
    """

def authGSSClientStep(context, challenge, **kwargs):
    """
    Processes a single GSSAPI client-side step using the supplied server data.

    @param context: the context object returned from authGSSClientInit.
    @param challenge: a string containing the base64-encoded server data (which may be empty
        for the first step).
    @param channel_bindings: Optional channel bindings to bind onto the auth request. This
        struct can be built using the channelBindings function and it not specified, this process
        will pass along GSS_C_NO_CHANNEL_BINDINGS as a default
    @return: a result code (see above).
    """

def authGSSClientResponse(context):
    """
    Get the client response from the last successful GSSAPI client-side step.

    @param context: the context object returned from authGSSClientInit.
    @return: a string containing the base64-encoded client data to be sent to the server.
    """

def authGSSClientResponseConf(context):
    """
    Returns 1 if confidentiality was enabled in the previously unwrapped buffer.  0 otherwise.

    @param context: the context object returned from authGSSClientInit.
    @return: an integer representing the confidentiality of the previously unwrapped buffer.
    """

def authGSSClientUserName(context):
    """
    Get the user name of the principal authenticated via the now complete GSSAPI client-side operations.
    This method must only be called after authGSSClientStep returns a complete response code.

    @param context:   the context object returned from authGSSClientInit.
    @return: a string containing the user name.
    """

def authGSSClientUnwrap(context, challenge):
    """
    Perform the client side GSSAPI unwrap step

    @param challenge: a string containing the base64-encoded server data.
    @return: a result code (see above)
    """

def authGSSClientWrap(context, data, user=None):
    """
    Perform the client side GSSAPI wrap step.

    @param data:the result of the authGSSClientResponse after the authGSSClientUnwrap
    @param user: the user to authorize
    @return: a result code (see above)
    """

def authGSSServerInit(service):
    """
    Initializes a context for GSSAPI server-side authentication with the given service principal.
    authGSSServerClean must be called after this function returns an OK result to dispose of
    the context once all GSSAPI operations are complete.

    @param service: a string containing the service principal in the form 'type@fqdn'
        (e.g. 'imap@mail.apple.com').
    @return: a tuple of (result, context) where result is the result code (see above) and
        context is an opaque value that will need to be passed to subsequent functions.
    """

def authGSSServerClean(context):
    """
    Destroys the context for GSSAPI server-side authentication. This function is provided for API
    compatibility with original pykerberos but does nothing. The context object destroys itself
    when it is reclaimed.

    @param context: the context object returned from authGSSServerInit.
    @return: a result code (see above).
    """

def authGSSServerStep(context, challenge):
    """
    Processes a single GSSAPI server-side step using the supplied client data.

    @param context: the context object returned from authGSSServerInit.
    @param challenge: a string containing the base64-encoded client data.
    @return: a result code (see above).
    """

def authGSSServerResponse(context):
    """
    Get the server response from the last successful GSSAPI server-side step.

    @param context: the context object returned from authGSSServerInit.
    @return: a string containing the base64-encoded server data to be sent to the client.
    """

def authGSSServerUserName(context):
    """
    Get the user name of the principal trying to authenticate to the server.
    This method must only be called after authGSSServerStep returns a complete or continue response code.

    @param context: the context object returned from authGSSServerInit.
    @return: a string containing the user name.
    """

def authGSSServerTargetName(context):
    """
    Get the target name if the server did not supply its own credentials.
    This method must only be called after authGSSServerStep returns a complete or continue response code.

    @param context: the context object returned from authGSSServerInit.
    @return: a string containing the target name.
    """

"""
Address Types for Channel Bindings
https://docs.oracle.com/cd/E19455-01/806-3814/6jcugr7dp/index.html#reference-9
"""

GSS_C_AF_UNSPEC    = 0
GSS_C_AF_LOCAL     = 1
GSS_C_AF_INET      = 2
GSS_C_AF_IMPLINK   = 3
GSS_C_AF_PUP       = 4
GSS_C_AF_CHAOS     = 5
GSS_C_AF_NS        = 6
GSS_C_AF_NBS       = 7
GSS_C_AF_ECMA      = 8
GSS_C_AF_DATAKIT   = 9
GSS_C_AF_CCITT     = 10
GSS_C_AF_SNA       = 11
GSS_C_AF_DECnet    = 12
GSS_C_AF_DLI       = 13
GSS_C_AF_LAT       = 14
GSS_C_AF_HYLINK    = 15
GSS_C_AF_APPLETALK = 16
GSS_C_AF_BSC       = 17
GSS_C_AF_DSS       = 18
GSS_C_AF_OSI       = 19
GSS_C_AF_X25       = 21
GSS_C_AF_NULLADDR  = 255

def channelBindings(**kwargs):
    """
    Builds a gss_channel_bindings_struct which can be used to pass onto authGSSClientStep to bind
    onto the auth. Details on Channel Bindings can be found at https://tools.ietf.org/html/rfc5929.
    More details on the struct can be found at https://docs.oracle.com/cd/E19455-01/806-3814/overview-52/index.html

    @param initiator_addrtype: Optional integer used to set the
        initiator_addrtype, defaults to GSS_C_AF_UNSPEC if not set
    @param initiator_address: Optional byte string containing the
        initiator_address
    @param acceptor_addrtype: Optional integer used to set the
        acceptor_addrtype, defaults to GSS_C_AF_UNSPEC if not set
    @param acceptor_address: Optional byte string containing the
        acceptor_address
    @param application_data: Optional byte string containing the
        application_data. An example would be 'tls-server-end-point:{cert-hash}'
        where {cert-hash} is the byte string hash of the server's certificate
    @return: The gss_channel_bindings_struct pointer, which is the channel
        bindings structure that can be passed onto authGSSClientStep
    """

def authGSSWinRMEncryptMessage(context, message):
    """
    Encrypts a message body with the current Kerberos session key using IOV settings for WinRM

    @param context: The context object returned from L{authGSSClientInit}.
    @param message: The plaintext message to be encrypted. 
    @return: A tuple of (encrypted_data, header) where encrypted_data is the 
        ciphertext result of the encryption operation, and header is the GSSAPI
        header describing the encryption parameters. Both strings contain opaque
        binary data.
    """

def authGSSWinRMDecryptMessage(context, encrypted_data, header):
    """
    Decrypts a ciphertext message body with the current Kerberos session key using IOV settings for WinRM

    @param context: The context object returned from L{authGSSClientInit}.
    @param encrypted_data: The ciphertext message to be decrypted.
    @param header: The GSSAPI message header containing the encryption parameters.
    @return: The decrypted message text.
    """
