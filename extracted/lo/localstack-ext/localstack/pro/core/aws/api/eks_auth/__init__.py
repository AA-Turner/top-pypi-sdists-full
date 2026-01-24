from datetime import datetime
from typing import TypedDict

from localstack.aws.api import RequestContext, ServiceException, ServiceRequest, handler

ClusterName = str
JwtToken = str
String = str


class AccessDeniedException(ServiceException):
    """You don't have permissions to perform the requested operation. The IAM
    principal making the request must have at least one IAM permissions
    policy attached that grants the required permissions. For more
    information, see `Access
    management <https://docs.aws.amazon.com/IAM/latest/UserGuide/access.html>`__
    in the *IAM User Guide*.
    """

    code: str = "AccessDeniedException"
    sender_fault: bool = True
    status_code: int = 400


class ExpiredTokenException(ServiceException):
    """The specified Kubernetes service account token is expired."""

    code: str = "ExpiredTokenException"
    sender_fault: bool = True
    status_code: int = 400


class InternalServerException(ServiceException):
    """These errors are usually caused by a server-side issue."""

    code: str = "InternalServerException"
    sender_fault: bool = False
    status_code: int = 500


class InvalidParameterException(ServiceException):
    """The specified parameter is invalid. Review the available parameters for
    the API request.
    """

    code: str = "InvalidParameterException"
    sender_fault: bool = True
    status_code: int = 400


class InvalidRequestException(ServiceException):
    """This exception is thrown if the request contains a semantic error. The
    precise meaning will depend on the API, and will be documented in the
    error message.
    """

    code: str = "InvalidRequestException"
    sender_fault: bool = True
    status_code: int = 400


class InvalidTokenException(ServiceException):
    """The specified Kubernetes service account token is invalid."""

    code: str = "InvalidTokenException"
    sender_fault: bool = True
    status_code: int = 400


class ResourceNotFoundException(ServiceException):
    """The specified resource could not be found."""

    code: str = "ResourceNotFoundException"
    sender_fault: bool = True
    status_code: int = 404


class ServiceUnavailableException(ServiceException):
    """The service is unavailable. Back off and retry the operation."""

    code: str = "ServiceUnavailableException"
    sender_fault: bool = False
    status_code: int = 503


class ThrottlingException(ServiceException):
    """The request was denied because your request rate is too high. Reduce the
    frequency of requests.
    """

    code: str = "ThrottlingException"
    sender_fault: bool = True
    status_code: int = 429


class AssumeRoleForPodIdentityRequest(ServiceRequest):
    clusterName: ClusterName
    token: JwtToken


Timestamp = datetime


class Credentials(TypedDict, total=False):
    """The *Amazon Web Services Signature Version 4* type of temporary
    credentials.
    """

    sessionToken: String
    secretAccessKey: String
    accessKeyId: String
    expiration: Timestamp


class AssumedRoleUser(TypedDict, total=False):
    """An object with the permanent IAM role identity and the temporary session
    name.
    """

    arn: String
    assumeRoleId: String


class PodIdentityAssociation(TypedDict, total=False):
    """Amazon EKS Pod Identity associations provide the ability to manage
    credentials for your applications, similar to the way that Amazon EC2
    instance profiles provide credentials to Amazon EC2 instances.
    """

    associationArn: String
    associationId: String


class Subject(TypedDict, total=False):
    """An object containing the name of the Kubernetes service account inside
    the cluster to associate the IAM credentials with.
    """

    namespace: String
    serviceAccount: String


class AssumeRoleForPodIdentityResponse(TypedDict, total=False):
    subject: Subject
    audience: String
    podIdentityAssociation: PodIdentityAssociation
    assumedRoleUser: AssumedRoleUser
    credentials: Credentials


class EksAuthApi:
    service: str = "eks-auth"
    version: str = "2023-11-26"

    @handler("AssumeRoleForPodIdentity")
    def assume_role_for_pod_identity(
        self, context: RequestContext, cluster_name: ClusterName, token: JwtToken, **kwargs
    ) -> AssumeRoleForPodIdentityResponse:
        """The Amazon EKS Auth API and the ``AssumeRoleForPodIdentity`` action are
        only used by the EKS Pod Identity Agent.

        We recommend that applications use the Amazon Web Services SDKs to
        connect to Amazon Web Services services; if credentials from an EKS Pod
        Identity association are available in the pod, the latest versions of
        the SDKs use them automatically.

        :param cluster_name: The name of the cluster for the request.
        :param token: The token of the Kubernetes service account for the pod.
        :returns: AssumeRoleForPodIdentityResponse
        :raises ThrottlingException:
        :raises InvalidRequestException:
        :raises AccessDeniedException:
        :raises InternalServerException:
        :raises InvalidTokenException:
        :raises InvalidParameterException:
        :raises ExpiredTokenException:
        :raises ResourceNotFoundException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError
