r'''
# `snowflake_api_integration`

Refer to the Terraform Registry for docs: [`snowflake_api_integration`](https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_integration).
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from .._jsii import *

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class ApiIntegration(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.apiIntegration.ApiIntegration",
):
    '''Represents a {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_integration snowflake_api_integration}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        api_allowed_prefixes: typing.Sequence[builtins.str],
        api_provider: builtins.str,
        name: builtins.str,
        api_aws_role_arn: typing.Optional[builtins.str] = None,
        api_blocked_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
        api_gcp_service_account: typing.Optional[builtins.str] = None,
        api_key: typing.Optional[builtins.str] = None,
        azure_ad_application_id: typing.Optional[builtins.str] = None,
        azure_tenant_id: typing.Optional[builtins.str] = None,
        comment: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        google_audience: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_integration snowflake_api_integration} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param api_allowed_prefixes: Explicitly limits external functions that use the integration to reference one or more HTTPS proxy service endpoints and resources within those proxies. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_integration#api_allowed_prefixes ApiIntegration#api_allowed_prefixes}
        :param api_provider: Specifies the HTTPS proxy service type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_integration#api_provider ApiIntegration#api_provider}
        :param name: Specifies the name of the API integration. This name follows the rules for Object Identifiers. The name should be unique among api integrations in your account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_integration#name ApiIntegration#name}
        :param api_aws_role_arn: ARN of a cloud platform role. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_integration#api_aws_role_arn ApiIntegration#api_aws_role_arn}
        :param api_blocked_prefixes: Lists the endpoints and resources in the HTTPS proxy service that are not allowed to be called from Snowflake. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_integration#api_blocked_prefixes ApiIntegration#api_blocked_prefixes}
        :param api_gcp_service_account: The service account used for communication with the Google API Gateway. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_integration#api_gcp_service_account ApiIntegration#api_gcp_service_account}
        :param api_key: The API key (also called a “subscription key”). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_integration#api_key ApiIntegration#api_key}
        :param azure_ad_application_id: The 'Application (client) id' of the Azure AD app for your remote service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_integration#azure_ad_application_id ApiIntegration#azure_ad_application_id}
        :param azure_tenant_id: Specifies the ID for your Office 365 tenant that all Azure API Management instances belong to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_integration#azure_tenant_id ApiIntegration#azure_tenant_id}
        :param comment: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_integration#comment ApiIntegration#comment}.
        :param enabled: Specifies whether this API integration is enabled or disabled. If the API integration is disabled, any external function that relies on it will not work. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_integration#enabled ApiIntegration#enabled}
        :param google_audience: The audience claim when generating the JWT (JSON Web Token) to authenticate to the Google API Gateway. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_integration#google_audience ApiIntegration#google_audience}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_integration#id ApiIntegration#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__204eb5fba5f9443c11ac1c6e430df6b8c3ba4b4d846d99c1b4702b0042416674)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ApiIntegrationConfig(
            api_allowed_prefixes=api_allowed_prefixes,
            api_provider=api_provider,
            name=name,
            api_aws_role_arn=api_aws_role_arn,
            api_blocked_prefixes=api_blocked_prefixes,
            api_gcp_service_account=api_gcp_service_account,
            api_key=api_key,
            azure_ad_application_id=azure_ad_application_id,
            azure_tenant_id=azure_tenant_id,
            comment=comment,
            enabled=enabled,
            google_audience=google_audience,
            id=id,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a ApiIntegration resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ApiIntegration to import.
        :param import_from_id: The id of the existing ApiIntegration that should be imported. Refer to the {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_integration#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ApiIntegration to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbec1a39a2a4226e43abc922dbefff345c917c05c9daf8f6f7f37bc505e0139e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetApiAwsRoleArn")
    def reset_api_aws_role_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiAwsRoleArn", []))

    @jsii.member(jsii_name="resetApiBlockedPrefixes")
    def reset_api_blocked_prefixes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiBlockedPrefixes", []))

    @jsii.member(jsii_name="resetApiGcpServiceAccount")
    def reset_api_gcp_service_account(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiGcpServiceAccount", []))

    @jsii.member(jsii_name="resetApiKey")
    def reset_api_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiKey", []))

    @jsii.member(jsii_name="resetAzureAdApplicationId")
    def reset_azure_ad_application_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAzureAdApplicationId", []))

    @jsii.member(jsii_name="resetAzureTenantId")
    def reset_azure_tenant_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAzureTenantId", []))

    @jsii.member(jsii_name="resetComment")
    def reset_comment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComment", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetGoogleAudience")
    def reset_google_audience(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGoogleAudience", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.member(jsii_name="synthesizeHclAttributes")
    def _synthesize_hcl_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeHclAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="apiAwsExternalId")
    def api_aws_external_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiAwsExternalId"))

    @builtins.property
    @jsii.member(jsii_name="apiAwsIamUserArn")
    def api_aws_iam_user_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiAwsIamUserArn"))

    @builtins.property
    @jsii.member(jsii_name="azureConsentUrl")
    def azure_consent_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "azureConsentUrl"))

    @builtins.property
    @jsii.member(jsii_name="azureMultiTenantAppName")
    def azure_multi_tenant_app_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "azureMultiTenantAppName"))

    @builtins.property
    @jsii.member(jsii_name="createdOn")
    def created_on(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdOn"))

    @builtins.property
    @jsii.member(jsii_name="fullyQualifiedName")
    def fully_qualified_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fullyQualifiedName"))

    @builtins.property
    @jsii.member(jsii_name="apiAllowedPrefixesInput")
    def api_allowed_prefixes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "apiAllowedPrefixesInput"))

    @builtins.property
    @jsii.member(jsii_name="apiAwsRoleArnInput")
    def api_aws_role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiAwsRoleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="apiBlockedPrefixesInput")
    def api_blocked_prefixes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "apiBlockedPrefixesInput"))

    @builtins.property
    @jsii.member(jsii_name="apiGcpServiceAccountInput")
    def api_gcp_service_account_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiGcpServiceAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="apiKeyInput")
    def api_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="apiProviderInput")
    def api_provider_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiProviderInput"))

    @builtins.property
    @jsii.member(jsii_name="azureAdApplicationIdInput")
    def azure_ad_application_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "azureAdApplicationIdInput"))

    @builtins.property
    @jsii.member(jsii_name="azureTenantIdInput")
    def azure_tenant_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "azureTenantIdInput"))

    @builtins.property
    @jsii.member(jsii_name="commentInput")
    def comment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commentInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="googleAudienceInput")
    def google_audience_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "googleAudienceInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="apiAllowedPrefixes")
    def api_allowed_prefixes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "apiAllowedPrefixes"))

    @api_allowed_prefixes.setter
    def api_allowed_prefixes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c87689f386cf331039e96f8145e3b0b9906faf0d175525a8fffce5dcad539b37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiAllowedPrefixes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="apiAwsRoleArn")
    def api_aws_role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiAwsRoleArn"))

    @api_aws_role_arn.setter
    def api_aws_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c89dbb600f17c551cab2570c9deecd7b542c9620a45f037780deccc43fe6263e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiAwsRoleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="apiBlockedPrefixes")
    def api_blocked_prefixes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "apiBlockedPrefixes"))

    @api_blocked_prefixes.setter
    def api_blocked_prefixes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c573bc6ee1c20bfa60207496b342746b238e01bd07e3f3b88175b730dbfa9017)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiBlockedPrefixes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="apiGcpServiceAccount")
    def api_gcp_service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiGcpServiceAccount"))

    @api_gcp_service_account.setter
    def api_gcp_service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f3195e0eeaf462e2f923cbc041b5bbdbb97a3e097c3063fffab6e209358d09b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiGcpServiceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="apiKey")
    def api_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiKey"))

    @api_key.setter
    def api_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__731ffb86b5005537ca5b4558d829a62d790ff35a882890e0fe766e2fb365be01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="apiProvider")
    def api_provider(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiProvider"))

    @api_provider.setter
    def api_provider(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92d4f05423677ac779f5bad25c752b8e195fecc4579936cde47996bddb8a5416)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiProvider", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="azureAdApplicationId")
    def azure_ad_application_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "azureAdApplicationId"))

    @azure_ad_application_id.setter
    def azure_ad_application_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__104be51f679e32c7dd5d9b2f31c20ca14ef8c65ba0f43d6bff85e6c881a54c2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "azureAdApplicationId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="azureTenantId")
    def azure_tenant_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "azureTenantId"))

    @azure_tenant_id.setter
    def azure_tenant_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65cb421ab5e94a46d1baccfe80f78ca3551f4ef88776b87eda483b9dadcfed1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "azureTenantId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comment"))

    @comment.setter
    def comment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__982190183217405c5c35d89d09c076fa18657a77a1e38380f931f485c361d01b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59241600f54cec13075440cffd445a80e640dbcc0256c0cc958753cc196c0ba7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="googleAudience")
    def google_audience(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "googleAudience"))

    @google_audience.setter
    def google_audience(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e34f7fd36f10f7d3a57072b3f21b687f5ec8ab9cbdc4538a31ba55668f199f70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "googleAudience", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bd97d10039590fd96a7ae8c8f4c4d679af7738b370560dfd0993a444aadb02d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35b64be6c5915badf9567d980fb6b6797df79cd4173656c8c16a97f6d817e234)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.apiIntegration.ApiIntegrationConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "api_allowed_prefixes": "apiAllowedPrefixes",
        "api_provider": "apiProvider",
        "name": "name",
        "api_aws_role_arn": "apiAwsRoleArn",
        "api_blocked_prefixes": "apiBlockedPrefixes",
        "api_gcp_service_account": "apiGcpServiceAccount",
        "api_key": "apiKey",
        "azure_ad_application_id": "azureAdApplicationId",
        "azure_tenant_id": "azureTenantId",
        "comment": "comment",
        "enabled": "enabled",
        "google_audience": "googleAudience",
        "id": "id",
    },
)
class ApiIntegrationConfig(_cdktf_9a9027ec.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
        api_allowed_prefixes: typing.Sequence[builtins.str],
        api_provider: builtins.str,
        name: builtins.str,
        api_aws_role_arn: typing.Optional[builtins.str] = None,
        api_blocked_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
        api_gcp_service_account: typing.Optional[builtins.str] = None,
        api_key: typing.Optional[builtins.str] = None,
        azure_ad_application_id: typing.Optional[builtins.str] = None,
        azure_tenant_id: typing.Optional[builtins.str] = None,
        comment: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        google_audience: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param api_allowed_prefixes: Explicitly limits external functions that use the integration to reference one or more HTTPS proxy service endpoints and resources within those proxies. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_integration#api_allowed_prefixes ApiIntegration#api_allowed_prefixes}
        :param api_provider: Specifies the HTTPS proxy service type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_integration#api_provider ApiIntegration#api_provider}
        :param name: Specifies the name of the API integration. This name follows the rules for Object Identifiers. The name should be unique among api integrations in your account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_integration#name ApiIntegration#name}
        :param api_aws_role_arn: ARN of a cloud platform role. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_integration#api_aws_role_arn ApiIntegration#api_aws_role_arn}
        :param api_blocked_prefixes: Lists the endpoints and resources in the HTTPS proxy service that are not allowed to be called from Snowflake. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_integration#api_blocked_prefixes ApiIntegration#api_blocked_prefixes}
        :param api_gcp_service_account: The service account used for communication with the Google API Gateway. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_integration#api_gcp_service_account ApiIntegration#api_gcp_service_account}
        :param api_key: The API key (also called a “subscription key”). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_integration#api_key ApiIntegration#api_key}
        :param azure_ad_application_id: The 'Application (client) id' of the Azure AD app for your remote service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_integration#azure_ad_application_id ApiIntegration#azure_ad_application_id}
        :param azure_tenant_id: Specifies the ID for your Office 365 tenant that all Azure API Management instances belong to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_integration#azure_tenant_id ApiIntegration#azure_tenant_id}
        :param comment: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_integration#comment ApiIntegration#comment}.
        :param enabled: Specifies whether this API integration is enabled or disabled. If the API integration is disabled, any external function that relies on it will not work. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_integration#enabled ApiIntegration#enabled}
        :param google_audience: The audience claim when generating the JWT (JSON Web Token) to authenticate to the Google API Gateway. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_integration#google_audience ApiIntegration#google_audience}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_integration#id ApiIntegration#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__599fea4ee0fc1c0ff8b2a16fef2ca6f3f89d9400f965f49111252edb04b93814)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument api_allowed_prefixes", value=api_allowed_prefixes, expected_type=type_hints["api_allowed_prefixes"])
            check_type(argname="argument api_provider", value=api_provider, expected_type=type_hints["api_provider"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument api_aws_role_arn", value=api_aws_role_arn, expected_type=type_hints["api_aws_role_arn"])
            check_type(argname="argument api_blocked_prefixes", value=api_blocked_prefixes, expected_type=type_hints["api_blocked_prefixes"])
            check_type(argname="argument api_gcp_service_account", value=api_gcp_service_account, expected_type=type_hints["api_gcp_service_account"])
            check_type(argname="argument api_key", value=api_key, expected_type=type_hints["api_key"])
            check_type(argname="argument azure_ad_application_id", value=azure_ad_application_id, expected_type=type_hints["azure_ad_application_id"])
            check_type(argname="argument azure_tenant_id", value=azure_tenant_id, expected_type=type_hints["azure_tenant_id"])
            check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument google_audience", value=google_audience, expected_type=type_hints["google_audience"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "api_allowed_prefixes": api_allowed_prefixes,
            "api_provider": api_provider,
            "name": name,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if api_aws_role_arn is not None:
            self._values["api_aws_role_arn"] = api_aws_role_arn
        if api_blocked_prefixes is not None:
            self._values["api_blocked_prefixes"] = api_blocked_prefixes
        if api_gcp_service_account is not None:
            self._values["api_gcp_service_account"] = api_gcp_service_account
        if api_key is not None:
            self._values["api_key"] = api_key
        if azure_ad_application_id is not None:
            self._values["azure_ad_application_id"] = azure_ad_application_id
        if azure_tenant_id is not None:
            self._values["azure_tenant_id"] = azure_tenant_id
        if comment is not None:
            self._values["comment"] = comment
        if enabled is not None:
            self._values["enabled"] = enabled
        if google_audience is not None:
            self._values["google_audience"] = google_audience
        if id is not None:
            self._values["id"] = id

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]], result)

    @builtins.property
    def api_allowed_prefixes(self) -> typing.List[builtins.str]:
        '''Explicitly limits external functions that use the integration to reference one or more HTTPS proxy service endpoints and resources within those proxies.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_integration#api_allowed_prefixes ApiIntegration#api_allowed_prefixes}
        '''
        result = self._values.get("api_allowed_prefixes")
        assert result is not None, "Required property 'api_allowed_prefixes' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def api_provider(self) -> builtins.str:
        '''Specifies the HTTPS proxy service type.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_integration#api_provider ApiIntegration#api_provider}
        '''
        result = self._values.get("api_provider")
        assert result is not None, "Required property 'api_provider' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Specifies the name of the API integration.

        This name follows the rules for Object Identifiers. The name should be unique among api integrations in your account.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_integration#name ApiIntegration#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def api_aws_role_arn(self) -> typing.Optional[builtins.str]:
        '''ARN of a cloud platform role.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_integration#api_aws_role_arn ApiIntegration#api_aws_role_arn}
        '''
        result = self._values.get("api_aws_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def api_blocked_prefixes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Lists the endpoints and resources in the HTTPS proxy service that are not allowed to be called from Snowflake.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_integration#api_blocked_prefixes ApiIntegration#api_blocked_prefixes}
        '''
        result = self._values.get("api_blocked_prefixes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def api_gcp_service_account(self) -> typing.Optional[builtins.str]:
        '''The service account used for communication with the Google API Gateway.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_integration#api_gcp_service_account ApiIntegration#api_gcp_service_account}
        '''
        result = self._values.get("api_gcp_service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def api_key(self) -> typing.Optional[builtins.str]:
        '''The API key (also called a “subscription key”).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_integration#api_key ApiIntegration#api_key}
        '''
        result = self._values.get("api_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def azure_ad_application_id(self) -> typing.Optional[builtins.str]:
        '''The 'Application (client) id' of the Azure AD app for your remote service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_integration#azure_ad_application_id ApiIntegration#azure_ad_application_id}
        '''
        result = self._values.get("azure_ad_application_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def azure_tenant_id(self) -> typing.Optional[builtins.str]:
        '''Specifies the ID for your Office 365 tenant that all Azure API Management instances belong to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_integration#azure_tenant_id ApiIntegration#azure_tenant_id}
        '''
        result = self._values.get("azure_tenant_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_integration#comment ApiIntegration#comment}.'''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether this API integration is enabled or disabled.

        If the API integration is disabled, any external function that relies on it will not work.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_integration#enabled ApiIntegration#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def google_audience(self) -> typing.Optional[builtins.str]:
        '''The audience claim when generating the JWT (JSON Web Token) to authenticate to the Google API Gateway.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_integration#google_audience ApiIntegration#google_audience}
        '''
        result = self._values.get("google_audience")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/api_integration#id ApiIntegration#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiIntegrationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "ApiIntegration",
    "ApiIntegrationConfig",
]

publication.publish()

def _typecheckingstub__204eb5fba5f9443c11ac1c6e430df6b8c3ba4b4d846d99c1b4702b0042416674(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    api_allowed_prefixes: typing.Sequence[builtins.str],
    api_provider: builtins.str,
    name: builtins.str,
    api_aws_role_arn: typing.Optional[builtins.str] = None,
    api_blocked_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
    api_gcp_service_account: typing.Optional[builtins.str] = None,
    api_key: typing.Optional[builtins.str] = None,
    azure_ad_application_id: typing.Optional[builtins.str] = None,
    azure_tenant_id: typing.Optional[builtins.str] = None,
    comment: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    google_audience: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbec1a39a2a4226e43abc922dbefff345c917c05c9daf8f6f7f37bc505e0139e(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c87689f386cf331039e96f8145e3b0b9906faf0d175525a8fffce5dcad539b37(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c89dbb600f17c551cab2570c9deecd7b542c9620a45f037780deccc43fe6263e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c573bc6ee1c20bfa60207496b342746b238e01bd07e3f3b88175b730dbfa9017(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f3195e0eeaf462e2f923cbc041b5bbdbb97a3e097c3063fffab6e209358d09b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__731ffb86b5005537ca5b4558d829a62d790ff35a882890e0fe766e2fb365be01(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92d4f05423677ac779f5bad25c752b8e195fecc4579936cde47996bddb8a5416(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__104be51f679e32c7dd5d9b2f31c20ca14ef8c65ba0f43d6bff85e6c881a54c2b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65cb421ab5e94a46d1baccfe80f78ca3551f4ef88776b87eda483b9dadcfed1a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__982190183217405c5c35d89d09c076fa18657a77a1e38380f931f485c361d01b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59241600f54cec13075440cffd445a80e640dbcc0256c0cc958753cc196c0ba7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e34f7fd36f10f7d3a57072b3f21b687f5ec8ab9cbdc4538a31ba55668f199f70(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bd97d10039590fd96a7ae8c8f4c4d679af7738b370560dfd0993a444aadb02d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35b64be6c5915badf9567d980fb6b6797df79cd4173656c8c16a97f6d817e234(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__599fea4ee0fc1c0ff8b2a16fef2ca6f3f89d9400f965f49111252edb04b93814(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    api_allowed_prefixes: typing.Sequence[builtins.str],
    api_provider: builtins.str,
    name: builtins.str,
    api_aws_role_arn: typing.Optional[builtins.str] = None,
    api_blocked_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
    api_gcp_service_account: typing.Optional[builtins.str] = None,
    api_key: typing.Optional[builtins.str] = None,
    azure_ad_application_id: typing.Optional[builtins.str] = None,
    azure_tenant_id: typing.Optional[builtins.str] = None,
    comment: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    google_audience: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
