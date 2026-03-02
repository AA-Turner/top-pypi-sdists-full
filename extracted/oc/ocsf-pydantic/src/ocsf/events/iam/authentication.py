from enum import Enum

from ocsf.events.iam import IAM

from ocsf.objects.actor import Actor
from ocsf.objects.auth_factor import AuthenticationFactor
from ocsf.objects.certificate import DigitalCertificate
from ocsf.objects.user import User
from ocsf.objects.network_endpoint import NetworkEndpoint
from ocsf.objects.process import Process
from ocsf.objects.service import Service
from ocsf.objects.session import Session


class AuthenticationActivityId(Enum):
    Logon: int = 1 # A new logon session was requested.
    Logoff: int = 2 # A logon session was terminated and no longer exists.
    Authentication_Ticket: int = 3 # A Kerberos authentication ticket (TGT) was requested.
    Service_Ticket_Request: int = 4 # A Kerberos service ticket was requested.
    Service_Ticket_Renew: int = 5 # A Kerberos service ticket was renewed.
    Preauth: int = 6 # A preauthentication stage was engaged.


class Authentication(IAM):
    """
    Authentication events report authentication session activities such as user
    attempts a logon or logoff, successfully or otherwise.
    """

    class_uid = 3002
    class_name = 'Authentication'

    user: User # The subject (user/role or account) to authenticate.

    # Recommended:
    auth_protocol: str | None = None
    auth_protocol_id: int | None = None
    certificate: DigitalCertificate | None = None # The certificate associated with the
                                                  # authentication or pre-authentication (Kerberos).
    dst_endpoint: NetworkEndpoint | None = None # The endpoint to which the authentication was
                                                # targeted.
    is_mfa: bool | None = None
    is_remote: bool | None = None # The attempted authentication is over a remote connection.
    logon_type: str | None = None
    logon_type_id: int | None = None
    service: Service | None = None # The service or gateway to which the user or process is being
                                   # authenticated
    session: Session | None = None

    # Optional:
    activity_id: AuthenticationActivityId | None = None
    actor: Actor | None = None # The actor that requested the authentication.
    auth_factors: list[AuthenticationFactor] | None = None
    is_cleartext: bool | None = None
    is_new_logon: bool | None = None
    logon_process: Process | None = None
    status_detail: str | None = None # The details about the authentication request
