from enum import StrEnum
from typing import TypedDict

from localstack.aws.api import RequestContext, ServiceException, ServiceRequest, handler

MaxItems = int
_boolean = bool
_double = float
_integer = int
_string = str


class Capability(StrEnum):
    CAPABILITY_IAM = "CAPABILITY_IAM"
    CAPABILITY_NAMED_IAM = "CAPABILITY_NAMED_IAM"
    CAPABILITY_AUTO_EXPAND = "CAPABILITY_AUTO_EXPAND"
    CAPABILITY_RESOURCE_POLICY = "CAPABILITY_RESOURCE_POLICY"


class Status(StrEnum):
    PREPARING = "PREPARING"
    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"


class BadRequestException(ServiceException):
    """One of the parameters in the request is invalid."""

    code: str = "BadRequestException"
    sender_fault: bool = False
    status_code: int = 400
    ErrorCode: _string | None


class ConflictException(ServiceException):
    """The resource already exists."""

    code: str = "ConflictException"
    sender_fault: bool = False
    status_code: int = 409
    ErrorCode: _string | None


class ForbiddenException(ServiceException):
    """The client is not authenticated."""

    code: str = "ForbiddenException"
    sender_fault: bool = False
    status_code: int = 403
    ErrorCode: _string | None


class InternalServerErrorException(ServiceException):
    """The AWS Serverless Application Repository service encountered an
    internal error.
    """

    code: str = "InternalServerErrorException"
    sender_fault: bool = False
    status_code: int = 500
    ErrorCode: _string | None


class NotFoundException(ServiceException):
    """The resource (for example, an access policy statement) specified in the
    request doesn't exist.
    """

    code: str = "NotFoundException"
    sender_fault: bool = False
    status_code: int = 404
    ErrorCode: _string | None


class TooManyRequestsException(ServiceException):
    """The client is sending more than the allowed number of requests per unit
    of time.
    """

    code: str = "TooManyRequestsException"
    sender_fault: bool = False
    status_code: int = 429
    ErrorCode: _string | None


_listOfCapability = list[Capability]
_listOf__string = list[_string]


class ParameterDefinition(TypedDict, total=False):
    """Parameters supported by the application."""

    AllowedPattern: _string | None
    AllowedValues: _listOf__string | None
    ConstraintDescription: _string | None
    DefaultValue: _string | None
    Description: _string | None
    MaxLength: _integer | None
    MaxValue: _integer | None
    MinLength: _integer | None
    MinValue: _integer | None
    Name: _string
    NoEcho: _boolean | None
    ReferencedByResources: _listOf__string
    Type: _string | None


_listOfParameterDefinition = list[ParameterDefinition]


class Version(TypedDict, total=False):
    """Application version details."""

    ApplicationId: _string
    CreationTime: _string
    ParameterDefinitions: _listOfParameterDefinition
    RequiredCapabilities: _listOfCapability
    ResourcesSupported: _boolean
    SemanticVersion: _string
    SourceCodeArchiveUrl: _string | None
    SourceCodeUrl: _string | None
    TemplateUrl: _string


class Application(TypedDict, total=False):
    """Details about the application."""

    ApplicationId: _string
    Author: _string
    CreationTime: _string | None
    Description: _string
    HomePageUrl: _string | None
    IsVerifiedAuthor: _boolean | None
    Labels: _listOf__string | None
    LicenseUrl: _string | None
    Name: _string
    ReadmeUrl: _string | None
    SpdxLicenseId: _string | None
    VerifiedAuthorUrl: _string | None
    Version: Version | None


class ApplicationDependencySummary(TypedDict, total=False):
    """A nested application summary."""

    ApplicationId: _string
    SemanticVersion: _string


_listOfApplicationDependencySummary = list[ApplicationDependencySummary]


class ApplicationDependencyPage(TypedDict, total=False):
    """A list of application summaries nested in the application."""

    Dependencies: _listOfApplicationDependencySummary
    NextToken: _string | None


class ApplicationSummary(TypedDict, total=False):
    """Summary of details about the application."""

    ApplicationId: _string
    Author: _string
    CreationTime: _string | None
    Description: _string
    HomePageUrl: _string | None
    Labels: _listOf__string | None
    Name: _string
    SpdxLicenseId: _string | None


_listOfApplicationSummary = list[ApplicationSummary]


class ApplicationPage(TypedDict, total=False):
    """A list of application details."""

    Applications: _listOfApplicationSummary
    NextToken: _string | None


class ApplicationPolicyStatement(TypedDict, total=False):
    """Policy statement applied to the application."""

    Actions: _listOf__string
    PrincipalOrgIDs: _listOf__string | None
    Principals: _listOf__string
    StatementId: _string | None


_listOfApplicationPolicyStatement = list[ApplicationPolicyStatement]


class ApplicationPolicy(TypedDict, total=False):
    """Policy statements applied to the application."""

    Statements: _listOfApplicationPolicyStatement


class VersionSummary(TypedDict, total=False):
    """An application version summary."""

    ApplicationId: _string
    CreationTime: _string
    SemanticVersion: _string
    SourceCodeUrl: _string | None


_listOfVersionSummary = list[VersionSummary]


class ApplicationVersionPage(TypedDict, total=False):
    """A list of version summaries for the application."""

    NextToken: _string | None
    Versions: _listOfVersionSummary


class ChangeSetDetails(TypedDict, total=False):
    """Details of the change set."""

    ApplicationId: _string
    ChangeSetId: _string
    SemanticVersion: _string
    StackId: _string


class CreateApplicationInput(TypedDict, total=False):
    """Create an application request."""

    Author: _string
    Description: _string
    HomePageUrl: _string | None
    Labels: _listOf__string | None
    LicenseBody: _string | None
    LicenseUrl: _string | None
    Name: _string
    ReadmeBody: _string | None
    ReadmeUrl: _string | None
    SemanticVersion: _string | None
    SourceCodeArchiveUrl: _string | None
    SourceCodeUrl: _string | None
    SpdxLicenseId: _string | None
    TemplateBody: _string | None
    TemplateUrl: _string | None


class CreateApplicationRequest(ServiceRequest):
    Author: _string
    Description: _string
    HomePageUrl: _string | None
    Labels: _listOf__string | None
    LicenseBody: _string | None
    LicenseUrl: _string | None
    Name: _string
    ReadmeBody: _string | None
    ReadmeUrl: _string | None
    SemanticVersion: _string | None
    SourceCodeArchiveUrl: _string | None
    SourceCodeUrl: _string | None
    SpdxLicenseId: _string | None
    TemplateBody: _string | None
    TemplateUrl: _string | None


class CreateApplicationResponse(TypedDict, total=False):
    ApplicationId: _string | None
    Author: _string | None
    CreationTime: _string | None
    Description: _string | None
    HomePageUrl: _string | None
    IsVerifiedAuthor: _boolean | None
    Labels: _listOf__string | None
    LicenseUrl: _string | None
    Name: _string | None
    ReadmeUrl: _string | None
    SpdxLicenseId: _string | None
    VerifiedAuthorUrl: _string | None
    Version: Version | None


class CreateApplicationVersionInput(TypedDict, total=False):
    """Create a version request."""

    SourceCodeArchiveUrl: _string | None
    SourceCodeUrl: _string | None
    TemplateBody: _string | None
    TemplateUrl: _string | None


class CreateApplicationVersionRequest(ServiceRequest):
    ApplicationId: _string
    SemanticVersion: _string
    SourceCodeArchiveUrl: _string | None
    SourceCodeUrl: _string | None
    TemplateBody: _string | None
    TemplateUrl: _string | None


class CreateApplicationVersionResponse(TypedDict, total=False):
    ApplicationId: _string | None
    CreationTime: _string | None
    ParameterDefinitions: _listOfParameterDefinition | None
    RequiredCapabilities: _listOfCapability | None
    ResourcesSupported: _boolean | None
    SemanticVersion: _string | None
    SourceCodeArchiveUrl: _string | None
    SourceCodeUrl: _string | None
    TemplateUrl: _string | None


class Tag(TypedDict, total=False):
    """This property corresponds to the *AWS
    CloudFormation* `Tag <https://docs.aws.amazon.com/goto/WebAPI/cloudformation-2010-05-15/Tag>`__
    Data Type.
    """

    Key: _string
    Value: _string


_listOfTag = list[Tag]


class RollbackTrigger(TypedDict, total=False):
    """This property corresponds to the *AWS
    CloudFormation* `RollbackTrigger <https://docs.aws.amazon.com/goto/WebAPI/cloudformation-2010-05-15/RollbackTrigger>`__
    Data Type.
    """

    Arn: _string
    Type: _string


_listOfRollbackTrigger = list[RollbackTrigger]


class RollbackConfiguration(TypedDict, total=False):
    """This property corresponds to the *AWS
    CloudFormation* `RollbackConfiguration <https://docs.aws.amazon.com/goto/WebAPI/cloudformation-2010-05-15/RollbackConfiguration>`__
    Data Type.
    """

    MonitoringTimeInMinutes: _integer | None
    RollbackTriggers: _listOfRollbackTrigger | None


class ParameterValue(TypedDict, total=False):
    """Parameter value of the application."""

    Name: _string
    Value: _string


_listOfParameterValue = list[ParameterValue]


class CreateCloudFormationChangeSetInput(TypedDict, total=False):
    """Create an application change set request."""

    Capabilities: _listOf__string | None
    ChangeSetName: _string | None
    ClientToken: _string | None
    Description: _string | None
    NotificationArns: _listOf__string | None
    ParameterOverrides: _listOfParameterValue | None
    ResourceTypes: _listOf__string | None
    RollbackConfiguration: RollbackConfiguration | None
    SemanticVersion: _string | None
    StackName: _string
    Tags: _listOfTag | None
    TemplateId: _string | None


class CreateCloudFormationChangeSetRequest(ServiceRequest):
    ApplicationId: _string
    Capabilities: _listOf__string | None
    ChangeSetName: _string | None
    ClientToken: _string | None
    Description: _string | None
    NotificationArns: _listOf__string | None
    ParameterOverrides: _listOfParameterValue | None
    ResourceTypes: _listOf__string | None
    RollbackConfiguration: RollbackConfiguration | None
    SemanticVersion: _string | None
    StackName: _string
    Tags: _listOfTag | None
    TemplateId: _string | None


class CreateCloudFormationChangeSetResponse(TypedDict, total=False):
    ApplicationId: _string | None
    ChangeSetId: _string | None
    SemanticVersion: _string | None
    StackId: _string | None


class CreateCloudFormationTemplateRequest(ServiceRequest):
    ApplicationId: _string
    SemanticVersion: _string | None


class CreateCloudFormationTemplateResponse(TypedDict, total=False):
    ApplicationId: _string | None
    CreationTime: _string | None
    ExpirationTime: _string | None
    SemanticVersion: _string | None
    Status: Status | None
    TemplateId: _string | None
    TemplateUrl: _string | None


class DeleteApplicationRequest(ServiceRequest):
    ApplicationId: _string


class GetApplicationPolicyRequest(ServiceRequest):
    ApplicationId: _string


class GetApplicationPolicyResponse(TypedDict, total=False):
    Statements: _listOfApplicationPolicyStatement | None


class GetApplicationRequest(ServiceRequest):
    ApplicationId: _string
    SemanticVersion: _string | None


class GetApplicationResponse(TypedDict, total=False):
    ApplicationId: _string | None
    Author: _string | None
    CreationTime: _string | None
    Description: _string | None
    HomePageUrl: _string | None
    IsVerifiedAuthor: _boolean | None
    Labels: _listOf__string | None
    LicenseUrl: _string | None
    Name: _string | None
    ReadmeUrl: _string | None
    SpdxLicenseId: _string | None
    VerifiedAuthorUrl: _string | None
    Version: Version | None


class GetCloudFormationTemplateRequest(ServiceRequest):
    ApplicationId: _string
    TemplateId: _string


class GetCloudFormationTemplateResponse(TypedDict, total=False):
    ApplicationId: _string | None
    CreationTime: _string | None
    ExpirationTime: _string | None
    SemanticVersion: _string | None
    Status: Status | None
    TemplateId: _string | None
    TemplateUrl: _string | None


class ListApplicationDependenciesRequest(ServiceRequest):
    ApplicationId: _string
    MaxItems: MaxItems | None
    NextToken: _string | None
    SemanticVersion: _string | None


class ListApplicationDependenciesResponse(TypedDict, total=False):
    Dependencies: _listOfApplicationDependencySummary | None
    NextToken: _string | None


class ListApplicationVersionsRequest(ServiceRequest):
    ApplicationId: _string
    MaxItems: MaxItems | None
    NextToken: _string | None


class ListApplicationVersionsResponse(TypedDict, total=False):
    NextToken: _string | None
    Versions: _listOfVersionSummary | None


class ListApplicationsRequest(ServiceRequest):
    MaxItems: MaxItems | None
    NextToken: _string | None


class ListApplicationsResponse(TypedDict, total=False):
    Applications: _listOfApplicationSummary | None
    NextToken: _string | None


class PutApplicationPolicyRequest(ServiceRequest):
    ApplicationId: _string
    Statements: _listOfApplicationPolicyStatement


class PutApplicationPolicyResponse(TypedDict, total=False):
    Statements: _listOfApplicationPolicyStatement | None


class TemplateDetails(TypedDict, total=False):
    """Details of the template."""

    ApplicationId: _string
    CreationTime: _string
    ExpirationTime: _string
    SemanticVersion: _string
    Status: Status
    TemplateId: _string
    TemplateUrl: _string


class UnshareApplicationInput(TypedDict, total=False):
    """Unshare application request."""

    OrganizationId: _string


class UnshareApplicationRequest(ServiceRequest):
    ApplicationId: _string
    OrganizationId: _string


class UpdateApplicationInput(TypedDict, total=False):
    """Update the application request."""

    Author: _string | None
    Description: _string | None
    HomePageUrl: _string | None
    Labels: _listOf__string | None
    ReadmeBody: _string | None
    ReadmeUrl: _string | None


class UpdateApplicationRequest(ServiceRequest):
    ApplicationId: _string
    Author: _string | None
    Description: _string | None
    HomePageUrl: _string | None
    Labels: _listOf__string | None
    ReadmeBody: _string | None
    ReadmeUrl: _string | None


class UpdateApplicationResponse(TypedDict, total=False):
    ApplicationId: _string | None
    Author: _string | None
    CreationTime: _string | None
    Description: _string | None
    HomePageUrl: _string | None
    IsVerifiedAuthor: _boolean | None
    Labels: _listOf__string | None
    LicenseUrl: _string | None
    Name: _string | None
    ReadmeUrl: _string | None
    SpdxLicenseId: _string | None
    VerifiedAuthorUrl: _string | None
    Version: Version | None


_long = int


class ServerlessrepoApi:
    service: str = "serverlessrepo"
    version: str = "2017-09-08"

    @handler("CreateApplication")
    def create_application(
        self,
        context: RequestContext,
        description: _string,
        name: _string,
        author: _string,
        home_page_url: _string | None = None,
        labels: _listOf__string | None = None,
        license_body: _string | None = None,
        license_url: _string | None = None,
        readme_body: _string | None = None,
        readme_url: _string | None = None,
        semantic_version: _string | None = None,
        source_code_archive_url: _string | None = None,
        source_code_url: _string | None = None,
        spdx_license_id: _string | None = None,
        template_body: _string | None = None,
        template_url: _string | None = None,
        **kwargs,
    ) -> CreateApplicationResponse:
        """Creates an application, optionally including an AWS SAM file to create
        the first application version in the same call.

        :param description: The description of the application.
        :param name: The name of the application that you want to publish.
        :param author: The name of the author publishing the app.
        :param home_page_url: A URL with more information about the application, for example the
        location of your GitHub repository for the application.
        :param labels: Labels to improve discovery of apps in search results.
        :param license_body: A local text file that contains the license of the app that matches the
        spdxLicenseID value of your application.
        :param license_url: A link to the S3 object that contains the license of the app that
        matches the spdxLicenseID value of your application.
        :param readme_body: A local text readme file in Markdown language that contains a more
        detailed description of the application and how it works.
        :param readme_url: A link to the S3 object in Markdown language that contains a more
        detailed description of the application and how it works.
        :param semantic_version: The semantic version of the application:

        https://semver.
        :param source_code_archive_url: A link to the S3 object that contains the ZIP archive of the source code
        for this version of your application.
        :param source_code_url: A link to a public repository for the source code of your application,
        for example the URL of a specific GitHub commit.
        :param spdx_license_id: A valid identifier from https://spdx.
        :param template_body: The local raw packaged AWS SAM template file of your application.
        :param template_url: A link to the S3 object containing the packaged AWS SAM template of your
        application.
        :returns: CreateApplicationResponse
        :raises TooManyRequestsException:
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ConflictException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("CreateApplicationVersion")
    def create_application_version(
        self,
        context: RequestContext,
        application_id: _string,
        semantic_version: _string,
        source_code_archive_url: _string | None = None,
        source_code_url: _string | None = None,
        template_body: _string | None = None,
        template_url: _string | None = None,
        **kwargs,
    ) -> CreateApplicationVersionResponse:
        """Creates an application version.

        :param application_id: The Amazon Resource Name (ARN) of the application.
        :param semantic_version: The semantic version of the new version.
        :param source_code_archive_url: A link to the S3 object that contains the ZIP archive of the source code
        for this version of your application.
        :param source_code_url: A link to a public repository for the source code of your application,
        for example the URL of a specific GitHub commit.
        :param template_body: The raw packaged AWS SAM template of your application.
        :param template_url: A link to the packaged AWS SAM template of your application.
        :returns: CreateApplicationVersionResponse
        :raises TooManyRequestsException:
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ConflictException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("CreateCloudFormationChangeSet")
    def create_cloud_formation_change_set(
        self,
        context: RequestContext,
        application_id: _string,
        stack_name: _string,
        capabilities: _listOf__string | None = None,
        change_set_name: _string | None = None,
        client_token: _string | None = None,
        description: _string | None = None,
        notification_arns: _listOf__string | None = None,
        parameter_overrides: _listOfParameterValue | None = None,
        resource_types: _listOf__string | None = None,
        rollback_configuration: RollbackConfiguration | None = None,
        semantic_version: _string | None = None,
        tags: _listOfTag | None = None,
        template_id: _string | None = None,
        **kwargs,
    ) -> CreateCloudFormationChangeSetResponse:
        """Creates an AWS CloudFormation change set for the given application.

        :param application_id: The Amazon Resource Name (ARN) of the application.
        :param stack_name: This property corresponds to the parameter of the same name for the *AWS
        CloudFormation* `CreateChangeSet <https://docs.
        :param capabilities: A list of values that you must specify before you can deploy certain
        applications.
        :param change_set_name: This property corresponds to the parameter of the same name for the *AWS
        CloudFormation* `CreateChangeSet <https://docs.
        :param client_token: This property corresponds to the parameter of the same name for the *AWS
        CloudFormation* `CreateChangeSet <https://docs.
        :param description: This property corresponds to the parameter of the same name for the *AWS
        CloudFormation* `CreateChangeSet <https://docs.
        :param notification_arns: This property corresponds to the parameter of the same name for the *AWS
        CloudFormation* `CreateChangeSet <https://docs.
        :param parameter_overrides: A list of parameter values for the parameters of the application.
        :param resource_types: This property corresponds to the parameter of the same name for the *AWS
        CloudFormation* `CreateChangeSet <https://docs.
        :param rollback_configuration: This property corresponds to the parameter of the same name for the *AWS
        CloudFormation* `CreateChangeSet <https://docs.
        :param semantic_version: The semantic version of the application:

        https://semver.
        :param tags: This property corresponds to the parameter of the same name for the *AWS
        CloudFormation* `CreateChangeSet <https://docs.
        :param template_id: The UUID returned by CreateCloudFormationTemplate.
        :returns: CreateCloudFormationChangeSetResponse
        :raises TooManyRequestsException:
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("CreateCloudFormationTemplate")
    def create_cloud_formation_template(
        self,
        context: RequestContext,
        application_id: _string,
        semantic_version: _string | None = None,
        **kwargs,
    ) -> CreateCloudFormationTemplateResponse:
        """Creates an AWS CloudFormation template.

        :param application_id: The Amazon Resource Name (ARN) of the application.
        :param semantic_version: The semantic version of the application:

        https://semver.
        :returns: CreateCloudFormationTemplateResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("DeleteApplication")
    def delete_application(
        self, context: RequestContext, application_id: _string, **kwargs
    ) -> None:
        """Deletes the specified application.

        :param application_id: The Amazon Resource Name (ARN) of the application.
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("GetApplication")
    def get_application(
        self,
        context: RequestContext,
        application_id: _string,
        semantic_version: _string | None = None,
        **kwargs,
    ) -> GetApplicationResponse:
        """Gets the specified application.

        :param application_id: The Amazon Resource Name (ARN) of the application.
        :param semantic_version: The semantic version of the application to get.
        :returns: GetApplicationResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("GetApplicationPolicy")
    def get_application_policy(
        self, context: RequestContext, application_id: _string, **kwargs
    ) -> GetApplicationPolicyResponse:
        """Retrieves the policy for the application.

        :param application_id: The Amazon Resource Name (ARN) of the application.
        :returns: GetApplicationPolicyResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("GetCloudFormationTemplate")
    def get_cloud_formation_template(
        self, context: RequestContext, application_id: _string, template_id: _string, **kwargs
    ) -> GetCloudFormationTemplateResponse:
        """Gets the specified AWS CloudFormation template.

        :param application_id: The Amazon Resource Name (ARN) of the application.
        :param template_id: The UUID returned by CreateCloudFormationTemplate.
        :returns: GetCloudFormationTemplateResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("ListApplicationDependencies")
    def list_application_dependencies(
        self,
        context: RequestContext,
        application_id: _string,
        max_items: MaxItems | None = None,
        next_token: _string | None = None,
        semantic_version: _string | None = None,
        **kwargs,
    ) -> ListApplicationDependenciesResponse:
        """Retrieves the list of applications nested in the containing application.

        :param application_id: The Amazon Resource Name (ARN) of the application.
        :param max_items: The total number of items to return.
        :param next_token: A token to specify where to start paginating.
        :param semantic_version: The semantic version of the application to get.
        :returns: ListApplicationDependenciesResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("ListApplicationVersions")
    def list_application_versions(
        self,
        context: RequestContext,
        application_id: _string,
        max_items: MaxItems | None = None,
        next_token: _string | None = None,
        **kwargs,
    ) -> ListApplicationVersionsResponse:
        """Lists versions for the specified application.

        :param application_id: The Amazon Resource Name (ARN) of the application.
        :param max_items: The total number of items to return.
        :param next_token: A token to specify where to start paginating.
        :returns: ListApplicationVersionsResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("ListApplications")
    def list_applications(
        self,
        context: RequestContext,
        max_items: MaxItems | None = None,
        next_token: _string | None = None,
        **kwargs,
    ) -> ListApplicationsResponse:
        """Lists applications owned by the requester.

        :param max_items: The total number of items to return.
        :param next_token: A token to specify where to start paginating.
        :returns: ListApplicationsResponse
        :raises NotFoundException:
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("PutApplicationPolicy")
    def put_application_policy(
        self,
        context: RequestContext,
        application_id: _string,
        statements: _listOfApplicationPolicyStatement,
        **kwargs,
    ) -> PutApplicationPolicyResponse:
        """Sets the permission policy for an application. For the list of actions
        supported for this operation, see `Application
        Permissions <https://docs.aws.amazon.com/serverlessrepo/latest/devguide/access-control-resource-based.html#application-permissions>`__
        .

        :param application_id: The Amazon Resource Name (ARN) of the application.
        :param statements: An array of policy statements applied to the application.
        :returns: PutApplicationPolicyResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("UnshareApplication")
    def unshare_application(
        self, context: RequestContext, application_id: _string, organization_id: _string, **kwargs
    ) -> None:
        """Unshares an application from an AWS Organization.

        This operation can be called only from the organization's master
        account.

        :param application_id: The Amazon Resource Name (ARN) of the application.
        :param organization_id: The AWS Organization ID to unshare the application from.
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("UpdateApplication")
    def update_application(
        self,
        context: RequestContext,
        application_id: _string,
        author: _string | None = None,
        description: _string | None = None,
        home_page_url: _string | None = None,
        labels: _listOf__string | None = None,
        readme_body: _string | None = None,
        readme_url: _string | None = None,
        **kwargs,
    ) -> UpdateApplicationResponse:
        """Updates the specified application.

        :param application_id: The Amazon Resource Name (ARN) of the application.
        :param author: The name of the author publishing the app.
        :param description: The description of the application.
        :param home_page_url: A URL with more information about the application, for example the
        location of your GitHub repository for the application.
        :param labels: Labels to improve discovery of apps in search results.
        :param readme_body: A text readme file in Markdown language that contains a more detailed
        description of the application and how it works.
        :param readme_url: A link to the readme file in Markdown language that contains a more
        detailed description of the application and how it works.
        :returns: UpdateApplicationResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        """
        raise NotImplementedError
