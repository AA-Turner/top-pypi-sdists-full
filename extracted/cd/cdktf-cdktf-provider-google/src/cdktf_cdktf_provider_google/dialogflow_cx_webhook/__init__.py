r'''
# `google_dialogflow_cx_webhook`

Refer to the Terraform Registry for docs: [`google_dialogflow_cx_webhook`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook).
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


class DialogflowCxWebhook(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxWebhook.DialogflowCxWebhook",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook google_dialogflow_cx_webhook}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        display_name: builtins.str,
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_spell_correction: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_stackdriver_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        generic_web_service: typing.Optional[typing.Union["DialogflowCxWebhookGenericWebService", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        parent: typing.Optional[builtins.str] = None,
        security_settings: typing.Optional[builtins.str] = None,
        service_directory: typing.Optional[typing.Union["DialogflowCxWebhookServiceDirectory", typing.Dict[builtins.str, typing.Any]]] = None,
        timeout: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DialogflowCxWebhookTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook google_dialogflow_cx_webhook} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param display_name: The human-readable name of the webhook, unique within the agent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#display_name DialogflowCxWebhook#display_name}
        :param disabled: Indicates whether the webhook is disabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#disabled DialogflowCxWebhook#disabled}
        :param enable_spell_correction: Deprecated. Indicates if automatic spell correction is enabled in detect intent requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#enable_spell_correction DialogflowCxWebhook#enable_spell_correction}
        :param enable_stackdriver_logging: Deprecated. Determines whether this agent should log conversation queries. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#enable_stackdriver_logging DialogflowCxWebhook#enable_stackdriver_logging}
        :param generic_web_service: generic_web_service block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#generic_web_service DialogflowCxWebhook#generic_web_service}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#id DialogflowCxWebhook#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param parent: The agent to create a webhook for. Format: projects//locations//agents/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#parent DialogflowCxWebhook#parent}
        :param security_settings: Deprecated. Name of the SecuritySettings reference for the agent. Format: projects//locations//securitySettings/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#security_settings DialogflowCxWebhook#security_settings}
        :param service_directory: service_directory block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#service_directory DialogflowCxWebhook#service_directory}
        :param timeout: Webhook execution timeout. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#timeout DialogflowCxWebhook#timeout}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#timeouts DialogflowCxWebhook#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4b93fcd01ea757e5ec3ab0125b476ed1ce1879e7340c561093f46a6c5c06fd5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DialogflowCxWebhookConfig(
            display_name=display_name,
            disabled=disabled,
            enable_spell_correction=enable_spell_correction,
            enable_stackdriver_logging=enable_stackdriver_logging,
            generic_web_service=generic_web_service,
            id=id,
            parent=parent,
            security_settings=security_settings,
            service_directory=service_directory,
            timeout=timeout,
            timeouts=timeouts,
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
        '''Generates CDKTF code for importing a DialogflowCxWebhook resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DialogflowCxWebhook to import.
        :param import_from_id: The id of the existing DialogflowCxWebhook that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DialogflowCxWebhook to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eacadbbadf684021b4dc36f342b23a0dbcf3b1a4498c56f3a40b4f3ffe71146c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putGenericWebService")
    def put_generic_web_service(
        self,
        *,
        uri: builtins.str,
        allowed_ca_certs: typing.Optional[typing.Sequence[builtins.str]] = None,
        http_method: typing.Optional[builtins.str] = None,
        oauth_config: typing.Optional[typing.Union["DialogflowCxWebhookGenericWebServiceOauthConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        parameter_mapping: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        request_body: typing.Optional[builtins.str] = None,
        request_headers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        secret_version_for_username_password: typing.Optional[builtins.str] = None,
        secret_versions_for_request_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DialogflowCxWebhookGenericWebServiceSecretVersionsForRequestHeaders", typing.Dict[builtins.str, typing.Any]]]]] = None,
        service_agent_auth: typing.Optional[builtins.str] = None,
        webhook_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param uri: The webhook URI for receiving POST requests. It must use https protocol. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#uri DialogflowCxWebhook#uri}
        :param allowed_ca_certs: Specifies a list of allowed custom CA certificates (in DER format) for HTTPS verification. This overrides the default SSL trust store. If this is empty or unspecified, Dialogflow will use Google's default trust store to verify certificates. N.B. Make sure the HTTPS server certificates are signed with "subject alt name". For instance a certificate can be self-signed using the following command, openssl x509 -req -days 200 -in example.com.csr -signkey example.com.key -out example.com.crt -extfile <(printf "\\nsubjectAltName='DNS:www.example.com'") Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#allowed_ca_certs DialogflowCxWebhook#allowed_ca_certs}
        :param http_method: HTTP method for the flexible webhook calls. Standard webhook always uses POST. Possible values: ["POST", "GET", "HEAD", "PUT", "DELETE", "PATCH", "OPTIONS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#http_method DialogflowCxWebhook#http_method}
        :param oauth_config: oauth_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#oauth_config DialogflowCxWebhook#oauth_config}
        :param parameter_mapping: Maps the values extracted from specific fields of the flexible webhook response into session parameters. - Key: session parameter name - Value: field path in the webhook response Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#parameter_mapping DialogflowCxWebhook#parameter_mapping}
        :param request_body: Defines a custom JSON object as request body to send to flexible webhook. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#request_body DialogflowCxWebhook#request_body}
        :param request_headers: The HTTP request headers to send together with webhook requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#request_headers DialogflowCxWebhook#request_headers}
        :param secret_version_for_username_password: The SecretManager secret version resource storing the username:password pair for HTTP Basic authentication. Format: 'projects/{project}/secrets/{secret}/versions/{version}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#secret_version_for_username_password DialogflowCxWebhook#secret_version_for_username_password}
        :param secret_versions_for_request_headers: secret_versions_for_request_headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#secret_versions_for_request_headers DialogflowCxWebhook#secret_versions_for_request_headers}
        :param service_agent_auth: Indicate the auth token type generated from the `Diglogflow service agent <https://cloud.google.com/iam/docs/service-agents#dialogflow-service-agent>`_. The generated token is sent in the Authorization header. Possible values: ["NONE", "ID_TOKEN", "ACCESS_TOKEN"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#service_agent_auth DialogflowCxWebhook#service_agent_auth}
        :param webhook_type: Type of the webhook. Possible values: ["STANDARD", "FLEXIBLE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#webhook_type DialogflowCxWebhook#webhook_type}
        '''
        value = DialogflowCxWebhookGenericWebService(
            uri=uri,
            allowed_ca_certs=allowed_ca_certs,
            http_method=http_method,
            oauth_config=oauth_config,
            parameter_mapping=parameter_mapping,
            request_body=request_body,
            request_headers=request_headers,
            secret_version_for_username_password=secret_version_for_username_password,
            secret_versions_for_request_headers=secret_versions_for_request_headers,
            service_agent_auth=service_agent_auth,
            webhook_type=webhook_type,
        )

        return typing.cast(None, jsii.invoke(self, "putGenericWebService", [value]))

    @jsii.member(jsii_name="putServiceDirectory")
    def put_service_directory(
        self,
        *,
        service: builtins.str,
        generic_web_service: typing.Optional[typing.Union["DialogflowCxWebhookServiceDirectoryGenericWebService", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param service: The name of Service Directory service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#service DialogflowCxWebhook#service}
        :param generic_web_service: generic_web_service block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#generic_web_service DialogflowCxWebhook#generic_web_service}
        '''
        value = DialogflowCxWebhookServiceDirectory(
            service=service, generic_web_service=generic_web_service
        )

        return typing.cast(None, jsii.invoke(self, "putServiceDirectory", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#create DialogflowCxWebhook#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#delete DialogflowCxWebhook#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#update DialogflowCxWebhook#update}.
        '''
        value = DialogflowCxWebhookTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDisabled")
    def reset_disabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisabled", []))

    @jsii.member(jsii_name="resetEnableSpellCorrection")
    def reset_enable_spell_correction(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableSpellCorrection", []))

    @jsii.member(jsii_name="resetEnableStackdriverLogging")
    def reset_enable_stackdriver_logging(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableStackdriverLogging", []))

    @jsii.member(jsii_name="resetGenericWebService")
    def reset_generic_web_service(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGenericWebService", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetParent")
    def reset_parent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParent", []))

    @jsii.member(jsii_name="resetSecuritySettings")
    def reset_security_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecuritySettings", []))

    @jsii.member(jsii_name="resetServiceDirectory")
    def reset_service_directory(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceDirectory", []))

    @jsii.member(jsii_name="resetTimeout")
    def reset_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeout", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

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
    @jsii.member(jsii_name="genericWebService")
    def generic_web_service(
        self,
    ) -> "DialogflowCxWebhookGenericWebServiceOutputReference":
        return typing.cast("DialogflowCxWebhookGenericWebServiceOutputReference", jsii.get(self, "genericWebService"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="serviceDirectory")
    def service_directory(self) -> "DialogflowCxWebhookServiceDirectoryOutputReference":
        return typing.cast("DialogflowCxWebhookServiceDirectoryOutputReference", jsii.get(self, "serviceDirectory"))

    @builtins.property
    @jsii.member(jsii_name="startFlow")
    def start_flow(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startFlow"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "DialogflowCxWebhookTimeoutsOutputReference":
        return typing.cast("DialogflowCxWebhookTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="disabledInput")
    def disabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disabledInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="enableSpellCorrectionInput")
    def enable_spell_correction_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableSpellCorrectionInput"))

    @builtins.property
    @jsii.member(jsii_name="enableStackdriverLoggingInput")
    def enable_stackdriver_logging_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableStackdriverLoggingInput"))

    @builtins.property
    @jsii.member(jsii_name="genericWebServiceInput")
    def generic_web_service_input(
        self,
    ) -> typing.Optional["DialogflowCxWebhookGenericWebService"]:
        return typing.cast(typing.Optional["DialogflowCxWebhookGenericWebService"], jsii.get(self, "genericWebServiceInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="parentInput")
    def parent_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parentInput"))

    @builtins.property
    @jsii.member(jsii_name="securitySettingsInput")
    def security_settings_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "securitySettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceDirectoryInput")
    def service_directory_input(
        self,
    ) -> typing.Optional["DialogflowCxWebhookServiceDirectory"]:
        return typing.cast(typing.Optional["DialogflowCxWebhookServiceDirectory"], jsii.get(self, "serviceDirectoryInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutInput")
    def timeout_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DialogflowCxWebhookTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DialogflowCxWebhookTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="disabled")
    def disabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disabled"))

    @disabled.setter
    def disabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91fae4ab9bfbef0f5e50cd9a79d59df896fec4e69407edcf466c18b222709c5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecaa4d49729a5f2f7a43677750f91c8183ff0c0d004559a967276ac736a51513)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableSpellCorrection")
    def enable_spell_correction(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableSpellCorrection"))

    @enable_spell_correction.setter
    def enable_spell_correction(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20ce4b624bde545de503aab832107743384f8e153f340930022fa9ae8e7285bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableSpellCorrection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableStackdriverLogging")
    def enable_stackdriver_logging(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableStackdriverLogging"))

    @enable_stackdriver_logging.setter
    def enable_stackdriver_logging(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cb96817df275dbc1d2b40b169209465882957a12a7ae2a3f75897816df65965)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableStackdriverLogging", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__207814dd2883697b3454a914745ce5a882928fe1bbf07aa2efc6dd6ba15aeac6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parent")
    def parent(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parent"))

    @parent.setter
    def parent(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4889ec9458daaa19e8ba0819d97cbc01360902452038340b0bf6909613c08e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securitySettings")
    def security_settings(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securitySettings"))

    @security_settings.setter
    def security_settings(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f300ee23ad0c689af98070faa88309f648947661c4bb68b548aaea24169023e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securitySettings", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeout"))

    @timeout.setter
    def timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00fa5f95387ada28f0ba68b5bd718306a2fbc72e6f84059c72240974d003931e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeout", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxWebhook.DialogflowCxWebhookConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "display_name": "displayName",
        "disabled": "disabled",
        "enable_spell_correction": "enableSpellCorrection",
        "enable_stackdriver_logging": "enableStackdriverLogging",
        "generic_web_service": "genericWebService",
        "id": "id",
        "parent": "parent",
        "security_settings": "securitySettings",
        "service_directory": "serviceDirectory",
        "timeout": "timeout",
        "timeouts": "timeouts",
    },
)
class DialogflowCxWebhookConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        display_name: builtins.str,
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_spell_correction: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_stackdriver_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        generic_web_service: typing.Optional[typing.Union["DialogflowCxWebhookGenericWebService", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        parent: typing.Optional[builtins.str] = None,
        security_settings: typing.Optional[builtins.str] = None,
        service_directory: typing.Optional[typing.Union["DialogflowCxWebhookServiceDirectory", typing.Dict[builtins.str, typing.Any]]] = None,
        timeout: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DialogflowCxWebhookTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param display_name: The human-readable name of the webhook, unique within the agent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#display_name DialogflowCxWebhook#display_name}
        :param disabled: Indicates whether the webhook is disabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#disabled DialogflowCxWebhook#disabled}
        :param enable_spell_correction: Deprecated. Indicates if automatic spell correction is enabled in detect intent requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#enable_spell_correction DialogflowCxWebhook#enable_spell_correction}
        :param enable_stackdriver_logging: Deprecated. Determines whether this agent should log conversation queries. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#enable_stackdriver_logging DialogflowCxWebhook#enable_stackdriver_logging}
        :param generic_web_service: generic_web_service block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#generic_web_service DialogflowCxWebhook#generic_web_service}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#id DialogflowCxWebhook#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param parent: The agent to create a webhook for. Format: projects//locations//agents/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#parent DialogflowCxWebhook#parent}
        :param security_settings: Deprecated. Name of the SecuritySettings reference for the agent. Format: projects//locations//securitySettings/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#security_settings DialogflowCxWebhook#security_settings}
        :param service_directory: service_directory block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#service_directory DialogflowCxWebhook#service_directory}
        :param timeout: Webhook execution timeout. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#timeout DialogflowCxWebhook#timeout}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#timeouts DialogflowCxWebhook#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(generic_web_service, dict):
            generic_web_service = DialogflowCxWebhookGenericWebService(**generic_web_service)
        if isinstance(service_directory, dict):
            service_directory = DialogflowCxWebhookServiceDirectory(**service_directory)
        if isinstance(timeouts, dict):
            timeouts = DialogflowCxWebhookTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf107d7e01b697bbc304addf84c487c5b5c722c77a74fd9c7915bf150fd93d19)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument disabled", value=disabled, expected_type=type_hints["disabled"])
            check_type(argname="argument enable_spell_correction", value=enable_spell_correction, expected_type=type_hints["enable_spell_correction"])
            check_type(argname="argument enable_stackdriver_logging", value=enable_stackdriver_logging, expected_type=type_hints["enable_stackdriver_logging"])
            check_type(argname="argument generic_web_service", value=generic_web_service, expected_type=type_hints["generic_web_service"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument parent", value=parent, expected_type=type_hints["parent"])
            check_type(argname="argument security_settings", value=security_settings, expected_type=type_hints["security_settings"])
            check_type(argname="argument service_directory", value=service_directory, expected_type=type_hints["service_directory"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "display_name": display_name,
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
        if disabled is not None:
            self._values["disabled"] = disabled
        if enable_spell_correction is not None:
            self._values["enable_spell_correction"] = enable_spell_correction
        if enable_stackdriver_logging is not None:
            self._values["enable_stackdriver_logging"] = enable_stackdriver_logging
        if generic_web_service is not None:
            self._values["generic_web_service"] = generic_web_service
        if id is not None:
            self._values["id"] = id
        if parent is not None:
            self._values["parent"] = parent
        if security_settings is not None:
            self._values["security_settings"] = security_settings
        if service_directory is not None:
            self._values["service_directory"] = service_directory
        if timeout is not None:
            self._values["timeout"] = timeout
        if timeouts is not None:
            self._values["timeouts"] = timeouts

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
    def display_name(self) -> builtins.str:
        '''The human-readable name of the webhook, unique within the agent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#display_name DialogflowCxWebhook#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates whether the webhook is disabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#disabled DialogflowCxWebhook#disabled}
        '''
        result = self._values.get("disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_spell_correction(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Deprecated. Indicates if automatic spell correction is enabled in detect intent requests.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#enable_spell_correction DialogflowCxWebhook#enable_spell_correction}
        '''
        result = self._values.get("enable_spell_correction")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_stackdriver_logging(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Deprecated. Determines whether this agent should log conversation queries.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#enable_stackdriver_logging DialogflowCxWebhook#enable_stackdriver_logging}
        '''
        result = self._values.get("enable_stackdriver_logging")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def generic_web_service(
        self,
    ) -> typing.Optional["DialogflowCxWebhookGenericWebService"]:
        '''generic_web_service block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#generic_web_service DialogflowCxWebhook#generic_web_service}
        '''
        result = self._values.get("generic_web_service")
        return typing.cast(typing.Optional["DialogflowCxWebhookGenericWebService"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#id DialogflowCxWebhook#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parent(self) -> typing.Optional[builtins.str]:
        '''The agent to create a webhook for. Format: projects//locations//agents/.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#parent DialogflowCxWebhook#parent}
        '''
        result = self._values.get("parent")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_settings(self) -> typing.Optional[builtins.str]:
        '''Deprecated. Name of the SecuritySettings reference for the agent. Format: projects//locations//securitySettings/.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#security_settings DialogflowCxWebhook#security_settings}
        '''
        result = self._values.get("security_settings")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_directory(
        self,
    ) -> typing.Optional["DialogflowCxWebhookServiceDirectory"]:
        '''service_directory block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#service_directory DialogflowCxWebhook#service_directory}
        '''
        result = self._values.get("service_directory")
        return typing.cast(typing.Optional["DialogflowCxWebhookServiceDirectory"], result)

    @builtins.property
    def timeout(self) -> typing.Optional[builtins.str]:
        '''Webhook execution timeout.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#timeout DialogflowCxWebhook#timeout}
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["DialogflowCxWebhookTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#timeouts DialogflowCxWebhook#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DialogflowCxWebhookTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxWebhookConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxWebhook.DialogflowCxWebhookGenericWebService",
    jsii_struct_bases=[],
    name_mapping={
        "uri": "uri",
        "allowed_ca_certs": "allowedCaCerts",
        "http_method": "httpMethod",
        "oauth_config": "oauthConfig",
        "parameter_mapping": "parameterMapping",
        "request_body": "requestBody",
        "request_headers": "requestHeaders",
        "secret_version_for_username_password": "secretVersionForUsernamePassword",
        "secret_versions_for_request_headers": "secretVersionsForRequestHeaders",
        "service_agent_auth": "serviceAgentAuth",
        "webhook_type": "webhookType",
    },
)
class DialogflowCxWebhookGenericWebService:
    def __init__(
        self,
        *,
        uri: builtins.str,
        allowed_ca_certs: typing.Optional[typing.Sequence[builtins.str]] = None,
        http_method: typing.Optional[builtins.str] = None,
        oauth_config: typing.Optional[typing.Union["DialogflowCxWebhookGenericWebServiceOauthConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        parameter_mapping: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        request_body: typing.Optional[builtins.str] = None,
        request_headers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        secret_version_for_username_password: typing.Optional[builtins.str] = None,
        secret_versions_for_request_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DialogflowCxWebhookGenericWebServiceSecretVersionsForRequestHeaders", typing.Dict[builtins.str, typing.Any]]]]] = None,
        service_agent_auth: typing.Optional[builtins.str] = None,
        webhook_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param uri: The webhook URI for receiving POST requests. It must use https protocol. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#uri DialogflowCxWebhook#uri}
        :param allowed_ca_certs: Specifies a list of allowed custom CA certificates (in DER format) for HTTPS verification. This overrides the default SSL trust store. If this is empty or unspecified, Dialogflow will use Google's default trust store to verify certificates. N.B. Make sure the HTTPS server certificates are signed with "subject alt name". For instance a certificate can be self-signed using the following command, openssl x509 -req -days 200 -in example.com.csr -signkey example.com.key -out example.com.crt -extfile <(printf "\\nsubjectAltName='DNS:www.example.com'") Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#allowed_ca_certs DialogflowCxWebhook#allowed_ca_certs}
        :param http_method: HTTP method for the flexible webhook calls. Standard webhook always uses POST. Possible values: ["POST", "GET", "HEAD", "PUT", "DELETE", "PATCH", "OPTIONS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#http_method DialogflowCxWebhook#http_method}
        :param oauth_config: oauth_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#oauth_config DialogflowCxWebhook#oauth_config}
        :param parameter_mapping: Maps the values extracted from specific fields of the flexible webhook response into session parameters. - Key: session parameter name - Value: field path in the webhook response Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#parameter_mapping DialogflowCxWebhook#parameter_mapping}
        :param request_body: Defines a custom JSON object as request body to send to flexible webhook. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#request_body DialogflowCxWebhook#request_body}
        :param request_headers: The HTTP request headers to send together with webhook requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#request_headers DialogflowCxWebhook#request_headers}
        :param secret_version_for_username_password: The SecretManager secret version resource storing the username:password pair for HTTP Basic authentication. Format: 'projects/{project}/secrets/{secret}/versions/{version}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#secret_version_for_username_password DialogflowCxWebhook#secret_version_for_username_password}
        :param secret_versions_for_request_headers: secret_versions_for_request_headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#secret_versions_for_request_headers DialogflowCxWebhook#secret_versions_for_request_headers}
        :param service_agent_auth: Indicate the auth token type generated from the `Diglogflow service agent <https://cloud.google.com/iam/docs/service-agents#dialogflow-service-agent>`_. The generated token is sent in the Authorization header. Possible values: ["NONE", "ID_TOKEN", "ACCESS_TOKEN"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#service_agent_auth DialogflowCxWebhook#service_agent_auth}
        :param webhook_type: Type of the webhook. Possible values: ["STANDARD", "FLEXIBLE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#webhook_type DialogflowCxWebhook#webhook_type}
        '''
        if isinstance(oauth_config, dict):
            oauth_config = DialogflowCxWebhookGenericWebServiceOauthConfig(**oauth_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50e37ce6a32cce4e809bf9baa6d4ce943cfe151d2421d9ea60ccfa89e1488728)
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
            check_type(argname="argument allowed_ca_certs", value=allowed_ca_certs, expected_type=type_hints["allowed_ca_certs"])
            check_type(argname="argument http_method", value=http_method, expected_type=type_hints["http_method"])
            check_type(argname="argument oauth_config", value=oauth_config, expected_type=type_hints["oauth_config"])
            check_type(argname="argument parameter_mapping", value=parameter_mapping, expected_type=type_hints["parameter_mapping"])
            check_type(argname="argument request_body", value=request_body, expected_type=type_hints["request_body"])
            check_type(argname="argument request_headers", value=request_headers, expected_type=type_hints["request_headers"])
            check_type(argname="argument secret_version_for_username_password", value=secret_version_for_username_password, expected_type=type_hints["secret_version_for_username_password"])
            check_type(argname="argument secret_versions_for_request_headers", value=secret_versions_for_request_headers, expected_type=type_hints["secret_versions_for_request_headers"])
            check_type(argname="argument service_agent_auth", value=service_agent_auth, expected_type=type_hints["service_agent_auth"])
            check_type(argname="argument webhook_type", value=webhook_type, expected_type=type_hints["webhook_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "uri": uri,
        }
        if allowed_ca_certs is not None:
            self._values["allowed_ca_certs"] = allowed_ca_certs
        if http_method is not None:
            self._values["http_method"] = http_method
        if oauth_config is not None:
            self._values["oauth_config"] = oauth_config
        if parameter_mapping is not None:
            self._values["parameter_mapping"] = parameter_mapping
        if request_body is not None:
            self._values["request_body"] = request_body
        if request_headers is not None:
            self._values["request_headers"] = request_headers
        if secret_version_for_username_password is not None:
            self._values["secret_version_for_username_password"] = secret_version_for_username_password
        if secret_versions_for_request_headers is not None:
            self._values["secret_versions_for_request_headers"] = secret_versions_for_request_headers
        if service_agent_auth is not None:
            self._values["service_agent_auth"] = service_agent_auth
        if webhook_type is not None:
            self._values["webhook_type"] = webhook_type

    @builtins.property
    def uri(self) -> builtins.str:
        '''The webhook URI for receiving POST requests. It must use https protocol.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#uri DialogflowCxWebhook#uri}
        '''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allowed_ca_certs(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies a list of allowed custom CA certificates (in DER format) for HTTPS verification.

        This overrides the default SSL trust store. If this
        is empty or unspecified, Dialogflow will use Google's default trust store
        to verify certificates.
        N.B. Make sure the HTTPS server certificates are signed with "subject alt
        name". For instance a certificate can be self-signed using the following
        command,
        openssl x509 -req -days 200 -in example.com.csr
        -signkey example.com.key
        -out example.com.crt
        -extfile <(printf "\\nsubjectAltName='DNS:www.example.com'")

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#allowed_ca_certs DialogflowCxWebhook#allowed_ca_certs}
        '''
        result = self._values.get("allowed_ca_certs")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def http_method(self) -> typing.Optional[builtins.str]:
        '''HTTP method for the flexible webhook calls.

        Standard webhook always uses
        POST. Possible values: ["POST", "GET", "HEAD", "PUT", "DELETE", "PATCH", "OPTIONS"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#http_method DialogflowCxWebhook#http_method}
        '''
        result = self._values.get("http_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oauth_config(
        self,
    ) -> typing.Optional["DialogflowCxWebhookGenericWebServiceOauthConfig"]:
        '''oauth_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#oauth_config DialogflowCxWebhook#oauth_config}
        '''
        result = self._values.get("oauth_config")
        return typing.cast(typing.Optional["DialogflowCxWebhookGenericWebServiceOauthConfig"], result)

    @builtins.property
    def parameter_mapping(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Maps the values extracted from specific fields of the flexible webhook response into session parameters.

        - Key: session parameter name
        - Value: field path in the webhook response

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#parameter_mapping DialogflowCxWebhook#parameter_mapping}
        '''
        result = self._values.get("parameter_mapping")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def request_body(self) -> typing.Optional[builtins.str]:
        '''Defines a custom JSON object as request body to send to flexible webhook.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#request_body DialogflowCxWebhook#request_body}
        '''
        result = self._values.get("request_body")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def request_headers(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The HTTP request headers to send together with webhook requests.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#request_headers DialogflowCxWebhook#request_headers}
        '''
        result = self._values.get("request_headers")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def secret_version_for_username_password(self) -> typing.Optional[builtins.str]:
        '''The SecretManager secret version resource storing the username:password pair for HTTP Basic authentication. Format: 'projects/{project}/secrets/{secret}/versions/{version}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#secret_version_for_username_password DialogflowCxWebhook#secret_version_for_username_password}
        '''
        result = self._values.get("secret_version_for_username_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret_versions_for_request_headers(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DialogflowCxWebhookGenericWebServiceSecretVersionsForRequestHeaders"]]]:
        '''secret_versions_for_request_headers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#secret_versions_for_request_headers DialogflowCxWebhook#secret_versions_for_request_headers}
        '''
        result = self._values.get("secret_versions_for_request_headers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DialogflowCxWebhookGenericWebServiceSecretVersionsForRequestHeaders"]]], result)

    @builtins.property
    def service_agent_auth(self) -> typing.Optional[builtins.str]:
        '''Indicate the auth token type generated from the `Diglogflow service agent <https://cloud.google.com/iam/docs/service-agents#dialogflow-service-agent>`_. The generated token is sent in the Authorization header. Possible values: ["NONE", "ID_TOKEN", "ACCESS_TOKEN"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#service_agent_auth DialogflowCxWebhook#service_agent_auth}
        '''
        result = self._values.get("service_agent_auth")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def webhook_type(self) -> typing.Optional[builtins.str]:
        '''Type of the webhook. Possible values: ["STANDARD", "FLEXIBLE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#webhook_type DialogflowCxWebhook#webhook_type}
        '''
        result = self._values.get("webhook_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxWebhookGenericWebService(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxWebhook.DialogflowCxWebhookGenericWebServiceOauthConfig",
    jsii_struct_bases=[],
    name_mapping={
        "client_id": "clientId",
        "token_endpoint": "tokenEndpoint",
        "client_secret": "clientSecret",
        "scopes": "scopes",
        "secret_version_for_client_secret": "secretVersionForClientSecret",
    },
)
class DialogflowCxWebhookGenericWebServiceOauthConfig:
    def __init__(
        self,
        *,
        client_id: builtins.str,
        token_endpoint: builtins.str,
        client_secret: typing.Optional[builtins.str] = None,
        scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
        secret_version_for_client_secret: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param client_id: The client ID provided by the 3rd party platform. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#client_id DialogflowCxWebhook#client_id}
        :param token_endpoint: The token endpoint provided by the 3rd party platform to exchange an access token. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#token_endpoint DialogflowCxWebhook#token_endpoint}
        :param client_secret: The client secret provided by the 3rd party platform. If the 'secret_version_for_client_secret' field is set, this field will be ignored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#client_secret DialogflowCxWebhook#client_secret}
        :param scopes: The OAuth scopes to grant. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#scopes DialogflowCxWebhook#scopes}
        :param secret_version_for_client_secret: The name of the SecretManager secret version resource storing the client secret. If this field is set, the 'client_secret' field will be ignored. Format: 'projects/{project}/secrets/{secret}/versions/{version}' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#secret_version_for_client_secret DialogflowCxWebhook#secret_version_for_client_secret}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b66a1bb2679d8cc9720ad5bca429c4d2d1196cded6a6f55e01f69a461334a52d)
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument token_endpoint", value=token_endpoint, expected_type=type_hints["token_endpoint"])
            check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
            check_type(argname="argument scopes", value=scopes, expected_type=type_hints["scopes"])
            check_type(argname="argument secret_version_for_client_secret", value=secret_version_for_client_secret, expected_type=type_hints["secret_version_for_client_secret"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "client_id": client_id,
            "token_endpoint": token_endpoint,
        }
        if client_secret is not None:
            self._values["client_secret"] = client_secret
        if scopes is not None:
            self._values["scopes"] = scopes
        if secret_version_for_client_secret is not None:
            self._values["secret_version_for_client_secret"] = secret_version_for_client_secret

    @builtins.property
    def client_id(self) -> builtins.str:
        '''The client ID provided by the 3rd party platform.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#client_id DialogflowCxWebhook#client_id}
        '''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def token_endpoint(self) -> builtins.str:
        '''The token endpoint provided by the 3rd party platform to exchange an access token.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#token_endpoint DialogflowCxWebhook#token_endpoint}
        '''
        result = self._values.get("token_endpoint")
        assert result is not None, "Required property 'token_endpoint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_secret(self) -> typing.Optional[builtins.str]:
        '''The client secret provided by the 3rd party platform.  If the 'secret_version_for_client_secret' field is set, this field will be ignored.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#client_secret DialogflowCxWebhook#client_secret}
        '''
        result = self._values.get("client_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The OAuth scopes to grant.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#scopes DialogflowCxWebhook#scopes}
        '''
        result = self._values.get("scopes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def secret_version_for_client_secret(self) -> typing.Optional[builtins.str]:
        '''The name of the SecretManager secret version resource storing the client secret.

        If this field is set, the 'client_secret' field will be
        ignored.
        Format: 'projects/{project}/secrets/{secret}/versions/{version}'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#secret_version_for_client_secret DialogflowCxWebhook#secret_version_for_client_secret}
        '''
        result = self._values.get("secret_version_for_client_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxWebhookGenericWebServiceOauthConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxWebhookGenericWebServiceOauthConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxWebhook.DialogflowCxWebhookGenericWebServiceOauthConfigOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65a8010729e8b2f050c1b97f77f0f94971ca40e06563b51c9b7c22f0e98d5c0e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetClientSecret")
    def reset_client_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientSecret", []))

    @jsii.member(jsii_name="resetScopes")
    def reset_scopes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScopes", []))

    @jsii.member(jsii_name="resetSecretVersionForClientSecret")
    def reset_secret_version_for_client_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretVersionForClientSecret", []))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretInput")
    def client_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="scopesInput")
    def scopes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "scopesInput"))

    @builtins.property
    @jsii.member(jsii_name="secretVersionForClientSecretInput")
    def secret_version_for_client_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretVersionForClientSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="tokenEndpointInput")
    def token_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tokenEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cc6bcaeff0779fd535e97be24ba26f7258fe67225e535c40cdb2fa6a0e355f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecret"))

    @client_secret.setter
    def client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1ae551175023b95a3c25d7456a2930dd24ba197d5cced299eda38ff7ec37afd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scopes")
    def scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "scopes"))

    @scopes.setter
    def scopes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__608e81bfc9f2fe752423c25abc66805f7475a150a208674b4f1aed7f34a942e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scopes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretVersionForClientSecret")
    def secret_version_for_client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretVersionForClientSecret"))

    @secret_version_for_client_secret.setter
    def secret_version_for_client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5250e6a593e2366b53959944ef1ca1174bd66a7279d657986a541698dba8fb71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretVersionForClientSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tokenEndpoint")
    def token_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tokenEndpoint"))

    @token_endpoint.setter
    def token_endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ef5573b323ee99c535879e64984cb358dd28322f926b81cc1079caba619d2cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tokenEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowCxWebhookGenericWebServiceOauthConfig]:
        return typing.cast(typing.Optional[DialogflowCxWebhookGenericWebServiceOauthConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxWebhookGenericWebServiceOauthConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f828c918b576e06ead739baad1e1ed2e57dfeb660cea8deca4caa26805c039a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DialogflowCxWebhookGenericWebServiceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxWebhook.DialogflowCxWebhookGenericWebServiceOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__394bb3f2baadfd13359f5e5e02cbdd2d8d3669bad1d816ff00bddb77b5eae256)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOauthConfig")
    def put_oauth_config(
        self,
        *,
        client_id: builtins.str,
        token_endpoint: builtins.str,
        client_secret: typing.Optional[builtins.str] = None,
        scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
        secret_version_for_client_secret: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param client_id: The client ID provided by the 3rd party platform. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#client_id DialogflowCxWebhook#client_id}
        :param token_endpoint: The token endpoint provided by the 3rd party platform to exchange an access token. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#token_endpoint DialogflowCxWebhook#token_endpoint}
        :param client_secret: The client secret provided by the 3rd party platform. If the 'secret_version_for_client_secret' field is set, this field will be ignored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#client_secret DialogflowCxWebhook#client_secret}
        :param scopes: The OAuth scopes to grant. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#scopes DialogflowCxWebhook#scopes}
        :param secret_version_for_client_secret: The name of the SecretManager secret version resource storing the client secret. If this field is set, the 'client_secret' field will be ignored. Format: 'projects/{project}/secrets/{secret}/versions/{version}' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#secret_version_for_client_secret DialogflowCxWebhook#secret_version_for_client_secret}
        '''
        value = DialogflowCxWebhookGenericWebServiceOauthConfig(
            client_id=client_id,
            token_endpoint=token_endpoint,
            client_secret=client_secret,
            scopes=scopes,
            secret_version_for_client_secret=secret_version_for_client_secret,
        )

        return typing.cast(None, jsii.invoke(self, "putOauthConfig", [value]))

    @jsii.member(jsii_name="putSecretVersionsForRequestHeaders")
    def put_secret_versions_for_request_headers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DialogflowCxWebhookGenericWebServiceSecretVersionsForRequestHeaders", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb59fe3236a54f919a13acb6f5d4acc68d659cddeeb5d3b34ef870c65fbbf569)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSecretVersionsForRequestHeaders", [value]))

    @jsii.member(jsii_name="resetAllowedCaCerts")
    def reset_allowed_ca_certs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedCaCerts", []))

    @jsii.member(jsii_name="resetHttpMethod")
    def reset_http_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpMethod", []))

    @jsii.member(jsii_name="resetOauthConfig")
    def reset_oauth_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauthConfig", []))

    @jsii.member(jsii_name="resetParameterMapping")
    def reset_parameter_mapping(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameterMapping", []))

    @jsii.member(jsii_name="resetRequestBody")
    def reset_request_body(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestBody", []))

    @jsii.member(jsii_name="resetRequestHeaders")
    def reset_request_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestHeaders", []))

    @jsii.member(jsii_name="resetSecretVersionForUsernamePassword")
    def reset_secret_version_for_username_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretVersionForUsernamePassword", []))

    @jsii.member(jsii_name="resetSecretVersionsForRequestHeaders")
    def reset_secret_versions_for_request_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretVersionsForRequestHeaders", []))

    @jsii.member(jsii_name="resetServiceAgentAuth")
    def reset_service_agent_auth(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceAgentAuth", []))

    @jsii.member(jsii_name="resetWebhookType")
    def reset_webhook_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWebhookType", []))

    @builtins.property
    @jsii.member(jsii_name="oauthConfig")
    def oauth_config(
        self,
    ) -> DialogflowCxWebhookGenericWebServiceOauthConfigOutputReference:
        return typing.cast(DialogflowCxWebhookGenericWebServiceOauthConfigOutputReference, jsii.get(self, "oauthConfig"))

    @builtins.property
    @jsii.member(jsii_name="secretVersionsForRequestHeaders")
    def secret_versions_for_request_headers(
        self,
    ) -> "DialogflowCxWebhookGenericWebServiceSecretVersionsForRequestHeadersList":
        return typing.cast("DialogflowCxWebhookGenericWebServiceSecretVersionsForRequestHeadersList", jsii.get(self, "secretVersionsForRequestHeaders"))

    @builtins.property
    @jsii.member(jsii_name="allowedCaCertsInput")
    def allowed_ca_certs_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedCaCertsInput"))

    @builtins.property
    @jsii.member(jsii_name="httpMethodInput")
    def http_method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpMethodInput"))

    @builtins.property
    @jsii.member(jsii_name="oauthConfigInput")
    def oauth_config_input(
        self,
    ) -> typing.Optional[DialogflowCxWebhookGenericWebServiceOauthConfig]:
        return typing.cast(typing.Optional[DialogflowCxWebhookGenericWebServiceOauthConfig], jsii.get(self, "oauthConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="parameterMappingInput")
    def parameter_mapping_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "parameterMappingInput"))

    @builtins.property
    @jsii.member(jsii_name="requestBodyInput")
    def request_body_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "requestBodyInput"))

    @builtins.property
    @jsii.member(jsii_name="requestHeadersInput")
    def request_headers_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "requestHeadersInput"))

    @builtins.property
    @jsii.member(jsii_name="secretVersionForUsernamePasswordInput")
    def secret_version_for_username_password_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretVersionForUsernamePasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="secretVersionsForRequestHeadersInput")
    def secret_versions_for_request_headers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DialogflowCxWebhookGenericWebServiceSecretVersionsForRequestHeaders"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DialogflowCxWebhookGenericWebServiceSecretVersionsForRequestHeaders"]]], jsii.get(self, "secretVersionsForRequestHeadersInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAgentAuthInput")
    def service_agent_auth_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAgentAuthInput"))

    @builtins.property
    @jsii.member(jsii_name="uriInput")
    def uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uriInput"))

    @builtins.property
    @jsii.member(jsii_name="webhookTypeInput")
    def webhook_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "webhookTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedCaCerts")
    def allowed_ca_certs(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedCaCerts"))

    @allowed_ca_certs.setter
    def allowed_ca_certs(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__192c7d0caf0c94d9c288f94f9cc9f8cd82bb6a7521cf65ef139fa16362ed7673)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedCaCerts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpMethod")
    def http_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpMethod"))

    @http_method.setter
    def http_method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd635bdcf82947f630d239be22be30b7e390c5f9c7071d9c8e6bcdf1f5dd0eae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpMethod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parameterMapping")
    def parameter_mapping(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "parameterMapping"))

    @parameter_mapping.setter
    def parameter_mapping(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d0d3f9be36b2768e2f569e6e889473ba5e17ddb1cb4520b528b8175e2dd6b91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameterMapping", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requestBody")
    def request_body(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "requestBody"))

    @request_body.setter
    def request_body(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__397ef6db342161dd8402b7e9cd5d4b9818c7b8cc1fbbf293d2cafddb0f3aa381)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestBody", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requestHeaders")
    def request_headers(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "requestHeaders"))

    @request_headers.setter
    def request_headers(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54ee032cfad305ab6cd0f73585756afc6452c55e52d50c8b9cb3a0dadce0978f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestHeaders", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretVersionForUsernamePassword")
    def secret_version_for_username_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretVersionForUsernamePassword"))

    @secret_version_for_username_password.setter
    def secret_version_for_username_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb2c512bbf2e2abc1f2e0c5077d1059fc9228fc21456eec1efa2907139c37f2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretVersionForUsernamePassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAgentAuth")
    def service_agent_auth(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAgentAuth"))

    @service_agent_auth.setter
    def service_agent_auth(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6adcbb4c8625e01f99569fd92dcab65a2f1d1ea158f8a21823187a0ce247cb66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAgentAuth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0281b7b21ef7f30c48783ae0f2e91e0bdc120f4ecaae23d222a61ba4923865f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="webhookType")
    def webhook_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "webhookType"))

    @webhook_type.setter
    def webhook_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21e4307924efa6ad82ebec9312f697ea298c560b49a68cd64a964cff2b222ccc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "webhookType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DialogflowCxWebhookGenericWebService]:
        return typing.cast(typing.Optional[DialogflowCxWebhookGenericWebService], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxWebhookGenericWebService],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cee718e5524901b06bcf398b6ae38da1fe4bb62c6b4e920d4353f9354ace2915)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxWebhook.DialogflowCxWebhookGenericWebServiceSecretVersionsForRequestHeaders",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "secret_version": "secretVersion"},
)
class DialogflowCxWebhookGenericWebServiceSecretVersionsForRequestHeaders:
    def __init__(self, *, key: builtins.str, secret_version: builtins.str) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#key DialogflowCxWebhook#key}.
        :param secret_version: The SecretManager secret version resource storing the header value. Format: 'projects/{project}/secrets/{secret}/versions/{version}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#secret_version DialogflowCxWebhook#secret_version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d835df2050fec798b3ee604656794d54c95c3d0da19827fba5864839b574744a)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument secret_version", value=secret_version, expected_type=type_hints["secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "secret_version": secret_version,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#key DialogflowCxWebhook#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secret_version(self) -> builtins.str:
        '''The SecretManager secret version resource storing the header value. Format: 'projects/{project}/secrets/{secret}/versions/{version}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#secret_version DialogflowCxWebhook#secret_version}
        '''
        result = self._values.get("secret_version")
        assert result is not None, "Required property 'secret_version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxWebhookGenericWebServiceSecretVersionsForRequestHeaders(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxWebhookGenericWebServiceSecretVersionsForRequestHeadersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxWebhook.DialogflowCxWebhookGenericWebServiceSecretVersionsForRequestHeadersList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c09ca5e55c2e00b62d7945efea65c0ced06e70da00b5ea4d3011681ba6dd7bd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DialogflowCxWebhookGenericWebServiceSecretVersionsForRequestHeadersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f6febc8eaa05d54ee23905e89b0dd032058c68246817272ac017c404978cc59)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DialogflowCxWebhookGenericWebServiceSecretVersionsForRequestHeadersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc9324cc2a4386911ce8b4f85af240c29bcfc16d680f0a390baabcc0406697b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53224a1cbbcdc5e4987c409861ecb5dd9bd0765d3a026cbe780156b169d49023)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c9e730a31d1dba6f05576c68ec72654c9cb586ac70e0f30e60a2e7aa5fe7910)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxWebhookGenericWebServiceSecretVersionsForRequestHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxWebhookGenericWebServiceSecretVersionsForRequestHeaders]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxWebhookGenericWebServiceSecretVersionsForRequestHeaders]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5ab4f626415d69c2b3df3d16ace0fdd15d4188f7ed5f2de4634f0eae5b7b955)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DialogflowCxWebhookGenericWebServiceSecretVersionsForRequestHeadersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxWebhook.DialogflowCxWebhookGenericWebServiceSecretVersionsForRequestHeadersOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f9ceb5f85cf97f171473c240c62b43a10f0833e98113ebf242c972f53d6dd4f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="secretVersionInput")
    def secret_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33d72d4bb78b6402ca32cf59979372b0b44905e47c9db1bac5c01dbd85ce4933)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretVersion")
    def secret_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretVersion"))

    @secret_version.setter
    def secret_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f24c4f12c2e7ca208836cfbe3d56cc147af2289b8f47012870477c601cd04762)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxWebhookGenericWebServiceSecretVersionsForRequestHeaders]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxWebhookGenericWebServiceSecretVersionsForRequestHeaders]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxWebhookGenericWebServiceSecretVersionsForRequestHeaders]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d54b1f35590788c0c8f984d81f1959d1d312e89cdf300d963b82edcd77a57cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxWebhook.DialogflowCxWebhookServiceDirectory",
    jsii_struct_bases=[],
    name_mapping={"service": "service", "generic_web_service": "genericWebService"},
)
class DialogflowCxWebhookServiceDirectory:
    def __init__(
        self,
        *,
        service: builtins.str,
        generic_web_service: typing.Optional[typing.Union["DialogflowCxWebhookServiceDirectoryGenericWebService", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param service: The name of Service Directory service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#service DialogflowCxWebhook#service}
        :param generic_web_service: generic_web_service block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#generic_web_service DialogflowCxWebhook#generic_web_service}
        '''
        if isinstance(generic_web_service, dict):
            generic_web_service = DialogflowCxWebhookServiceDirectoryGenericWebService(**generic_web_service)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4604191929dc5e32d2c60339f6215e0af0fd5775fe76ff7ec057a209c0387da3)
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
            check_type(argname="argument generic_web_service", value=generic_web_service, expected_type=type_hints["generic_web_service"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "service": service,
        }
        if generic_web_service is not None:
            self._values["generic_web_service"] = generic_web_service

    @builtins.property
    def service(self) -> builtins.str:
        '''The name of Service Directory service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#service DialogflowCxWebhook#service}
        '''
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def generic_web_service(
        self,
    ) -> typing.Optional["DialogflowCxWebhookServiceDirectoryGenericWebService"]:
        '''generic_web_service block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#generic_web_service DialogflowCxWebhook#generic_web_service}
        '''
        result = self._values.get("generic_web_service")
        return typing.cast(typing.Optional["DialogflowCxWebhookServiceDirectoryGenericWebService"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxWebhookServiceDirectory(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxWebhook.DialogflowCxWebhookServiceDirectoryGenericWebService",
    jsii_struct_bases=[],
    name_mapping={
        "uri": "uri",
        "allowed_ca_certs": "allowedCaCerts",
        "http_method": "httpMethod",
        "oauth_config": "oauthConfig",
        "parameter_mapping": "parameterMapping",
        "request_body": "requestBody",
        "request_headers": "requestHeaders",
        "secret_version_for_username_password": "secretVersionForUsernamePassword",
        "secret_versions_for_request_headers": "secretVersionsForRequestHeaders",
        "service_agent_auth": "serviceAgentAuth",
        "webhook_type": "webhookType",
    },
)
class DialogflowCxWebhookServiceDirectoryGenericWebService:
    def __init__(
        self,
        *,
        uri: builtins.str,
        allowed_ca_certs: typing.Optional[typing.Sequence[builtins.str]] = None,
        http_method: typing.Optional[builtins.str] = None,
        oauth_config: typing.Optional[typing.Union["DialogflowCxWebhookServiceDirectoryGenericWebServiceOauthConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        parameter_mapping: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        request_body: typing.Optional[builtins.str] = None,
        request_headers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        secret_version_for_username_password: typing.Optional[builtins.str] = None,
        secret_versions_for_request_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DialogflowCxWebhookServiceDirectoryGenericWebServiceSecretVersionsForRequestHeaders", typing.Dict[builtins.str, typing.Any]]]]] = None,
        service_agent_auth: typing.Optional[builtins.str] = None,
        webhook_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param uri: The webhook URI for receiving POST requests. It must use https protocol. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#uri DialogflowCxWebhook#uri}
        :param allowed_ca_certs: Specifies a list of allowed custom CA certificates (in DER format) for HTTPS verification. This overrides the default SSL trust store. If this is empty or unspecified, Dialogflow will use Google's default trust store to verify certificates. N.B. Make sure the HTTPS server certificates are signed with "subject alt name". For instance a certificate can be self-signed using the following command, openssl x509 -req -days 200 -in example.com.csr -signkey example.com.key -out example.com.crt -extfile <(printf "\\nsubjectAltName='DNS:www.example.com'") Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#allowed_ca_certs DialogflowCxWebhook#allowed_ca_certs}
        :param http_method: HTTP method for the flexible webhook calls. Standard webhook always uses POST. Possible values: ["POST", "GET", "HEAD", "PUT", "DELETE", "PATCH", "OPTIONS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#http_method DialogflowCxWebhook#http_method}
        :param oauth_config: oauth_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#oauth_config DialogflowCxWebhook#oauth_config}
        :param parameter_mapping: Maps the values extracted from specific fields of the flexible webhook response into session parameters. - Key: session parameter name - Value: field path in the webhook response Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#parameter_mapping DialogflowCxWebhook#parameter_mapping}
        :param request_body: Defines a custom JSON object as request body to send to flexible webhook. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#request_body DialogflowCxWebhook#request_body}
        :param request_headers: The HTTP request headers to send together with webhook requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#request_headers DialogflowCxWebhook#request_headers}
        :param secret_version_for_username_password: The SecretManager secret version resource storing the username:password pair for HTTP Basic authentication. Format: 'projects/{project}/secrets/{secret}/versions/{version}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#secret_version_for_username_password DialogflowCxWebhook#secret_version_for_username_password}
        :param secret_versions_for_request_headers: secret_versions_for_request_headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#secret_versions_for_request_headers DialogflowCxWebhook#secret_versions_for_request_headers}
        :param service_agent_auth: Indicate the auth token type generated from the `Diglogflow service agent <https://cloud.google.com/iam/docs/service-agents#dialogflow-service-agent>`_. The generated token is sent in the Authorization header. Possible values: ["NONE", "ID_TOKEN", "ACCESS_TOKEN"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#service_agent_auth DialogflowCxWebhook#service_agent_auth}
        :param webhook_type: Type of the webhook. Possible values: ["STANDARD", "FLEXIBLE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#webhook_type DialogflowCxWebhook#webhook_type}
        '''
        if isinstance(oauth_config, dict):
            oauth_config = DialogflowCxWebhookServiceDirectoryGenericWebServiceOauthConfig(**oauth_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0c20721713bf45b99c0b87412272aa5d99d757709d88a13bdbc1c6cc9b07884)
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
            check_type(argname="argument allowed_ca_certs", value=allowed_ca_certs, expected_type=type_hints["allowed_ca_certs"])
            check_type(argname="argument http_method", value=http_method, expected_type=type_hints["http_method"])
            check_type(argname="argument oauth_config", value=oauth_config, expected_type=type_hints["oauth_config"])
            check_type(argname="argument parameter_mapping", value=parameter_mapping, expected_type=type_hints["parameter_mapping"])
            check_type(argname="argument request_body", value=request_body, expected_type=type_hints["request_body"])
            check_type(argname="argument request_headers", value=request_headers, expected_type=type_hints["request_headers"])
            check_type(argname="argument secret_version_for_username_password", value=secret_version_for_username_password, expected_type=type_hints["secret_version_for_username_password"])
            check_type(argname="argument secret_versions_for_request_headers", value=secret_versions_for_request_headers, expected_type=type_hints["secret_versions_for_request_headers"])
            check_type(argname="argument service_agent_auth", value=service_agent_auth, expected_type=type_hints["service_agent_auth"])
            check_type(argname="argument webhook_type", value=webhook_type, expected_type=type_hints["webhook_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "uri": uri,
        }
        if allowed_ca_certs is not None:
            self._values["allowed_ca_certs"] = allowed_ca_certs
        if http_method is not None:
            self._values["http_method"] = http_method
        if oauth_config is not None:
            self._values["oauth_config"] = oauth_config
        if parameter_mapping is not None:
            self._values["parameter_mapping"] = parameter_mapping
        if request_body is not None:
            self._values["request_body"] = request_body
        if request_headers is not None:
            self._values["request_headers"] = request_headers
        if secret_version_for_username_password is not None:
            self._values["secret_version_for_username_password"] = secret_version_for_username_password
        if secret_versions_for_request_headers is not None:
            self._values["secret_versions_for_request_headers"] = secret_versions_for_request_headers
        if service_agent_auth is not None:
            self._values["service_agent_auth"] = service_agent_auth
        if webhook_type is not None:
            self._values["webhook_type"] = webhook_type

    @builtins.property
    def uri(self) -> builtins.str:
        '''The webhook URI for receiving POST requests. It must use https protocol.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#uri DialogflowCxWebhook#uri}
        '''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allowed_ca_certs(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies a list of allowed custom CA certificates (in DER format) for HTTPS verification.

        This overrides the default SSL trust store. If this
        is empty or unspecified, Dialogflow will use Google's default trust store
        to verify certificates.
        N.B. Make sure the HTTPS server certificates are signed with "subject alt
        name". For instance a certificate can be self-signed using the following
        command,
        openssl x509 -req -days 200 -in example.com.csr
        -signkey example.com.key
        -out example.com.crt
        -extfile <(printf "\\nsubjectAltName='DNS:www.example.com'")

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#allowed_ca_certs DialogflowCxWebhook#allowed_ca_certs}
        '''
        result = self._values.get("allowed_ca_certs")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def http_method(self) -> typing.Optional[builtins.str]:
        '''HTTP method for the flexible webhook calls.

        Standard webhook always uses
        POST. Possible values: ["POST", "GET", "HEAD", "PUT", "DELETE", "PATCH", "OPTIONS"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#http_method DialogflowCxWebhook#http_method}
        '''
        result = self._values.get("http_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oauth_config(
        self,
    ) -> typing.Optional["DialogflowCxWebhookServiceDirectoryGenericWebServiceOauthConfig"]:
        '''oauth_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#oauth_config DialogflowCxWebhook#oauth_config}
        '''
        result = self._values.get("oauth_config")
        return typing.cast(typing.Optional["DialogflowCxWebhookServiceDirectoryGenericWebServiceOauthConfig"], result)

    @builtins.property
    def parameter_mapping(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Maps the values extracted from specific fields of the flexible webhook response into session parameters.

        - Key: session parameter name
        - Value: field path in the webhook response

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#parameter_mapping DialogflowCxWebhook#parameter_mapping}
        '''
        result = self._values.get("parameter_mapping")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def request_body(self) -> typing.Optional[builtins.str]:
        '''Defines a custom JSON object as request body to send to flexible webhook.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#request_body DialogflowCxWebhook#request_body}
        '''
        result = self._values.get("request_body")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def request_headers(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The HTTP request headers to send together with webhook requests.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#request_headers DialogflowCxWebhook#request_headers}
        '''
        result = self._values.get("request_headers")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def secret_version_for_username_password(self) -> typing.Optional[builtins.str]:
        '''The SecretManager secret version resource storing the username:password pair for HTTP Basic authentication. Format: 'projects/{project}/secrets/{secret}/versions/{version}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#secret_version_for_username_password DialogflowCxWebhook#secret_version_for_username_password}
        '''
        result = self._values.get("secret_version_for_username_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret_versions_for_request_headers(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DialogflowCxWebhookServiceDirectoryGenericWebServiceSecretVersionsForRequestHeaders"]]]:
        '''secret_versions_for_request_headers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#secret_versions_for_request_headers DialogflowCxWebhook#secret_versions_for_request_headers}
        '''
        result = self._values.get("secret_versions_for_request_headers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DialogflowCxWebhookServiceDirectoryGenericWebServiceSecretVersionsForRequestHeaders"]]], result)

    @builtins.property
    def service_agent_auth(self) -> typing.Optional[builtins.str]:
        '''Indicate the auth token type generated from the `Diglogflow service agent <https://cloud.google.com/iam/docs/service-agents#dialogflow-service-agent>`_. The generated token is sent in the Authorization header. Possible values: ["NONE", "ID_TOKEN", "ACCESS_TOKEN"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#service_agent_auth DialogflowCxWebhook#service_agent_auth}
        '''
        result = self._values.get("service_agent_auth")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def webhook_type(self) -> typing.Optional[builtins.str]:
        '''Type of the webhook. Possible values: ["STANDARD", "FLEXIBLE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#webhook_type DialogflowCxWebhook#webhook_type}
        '''
        result = self._values.get("webhook_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxWebhookServiceDirectoryGenericWebService(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxWebhook.DialogflowCxWebhookServiceDirectoryGenericWebServiceOauthConfig",
    jsii_struct_bases=[],
    name_mapping={
        "client_id": "clientId",
        "token_endpoint": "tokenEndpoint",
        "client_secret": "clientSecret",
        "scopes": "scopes",
        "secret_version_for_client_secret": "secretVersionForClientSecret",
    },
)
class DialogflowCxWebhookServiceDirectoryGenericWebServiceOauthConfig:
    def __init__(
        self,
        *,
        client_id: builtins.str,
        token_endpoint: builtins.str,
        client_secret: typing.Optional[builtins.str] = None,
        scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
        secret_version_for_client_secret: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param client_id: The client ID provided by the 3rd party platform. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#client_id DialogflowCxWebhook#client_id}
        :param token_endpoint: The token endpoint provided by the 3rd party platform to exchange an access token. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#token_endpoint DialogflowCxWebhook#token_endpoint}
        :param client_secret: The client secret provided by the 3rd party platform. If the 'secret_version_for_client_secret' field is set, this field will be ignored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#client_secret DialogflowCxWebhook#client_secret}
        :param scopes: The OAuth scopes to grant. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#scopes DialogflowCxWebhook#scopes}
        :param secret_version_for_client_secret: The name of the SecretManager secret version resource storing the client secret. If this field is set, the 'client_secret' field will be ignored. Format: 'projects/{project}/secrets/{secret}/versions/{version}' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#secret_version_for_client_secret DialogflowCxWebhook#secret_version_for_client_secret}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3de165377f68e4dfac4fcb833658450aeef7a1c0d9cc0aa6617a6b71161a1e5)
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument token_endpoint", value=token_endpoint, expected_type=type_hints["token_endpoint"])
            check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
            check_type(argname="argument scopes", value=scopes, expected_type=type_hints["scopes"])
            check_type(argname="argument secret_version_for_client_secret", value=secret_version_for_client_secret, expected_type=type_hints["secret_version_for_client_secret"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "client_id": client_id,
            "token_endpoint": token_endpoint,
        }
        if client_secret is not None:
            self._values["client_secret"] = client_secret
        if scopes is not None:
            self._values["scopes"] = scopes
        if secret_version_for_client_secret is not None:
            self._values["secret_version_for_client_secret"] = secret_version_for_client_secret

    @builtins.property
    def client_id(self) -> builtins.str:
        '''The client ID provided by the 3rd party platform.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#client_id DialogflowCxWebhook#client_id}
        '''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def token_endpoint(self) -> builtins.str:
        '''The token endpoint provided by the 3rd party platform to exchange an access token.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#token_endpoint DialogflowCxWebhook#token_endpoint}
        '''
        result = self._values.get("token_endpoint")
        assert result is not None, "Required property 'token_endpoint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_secret(self) -> typing.Optional[builtins.str]:
        '''The client secret provided by the 3rd party platform.  If the 'secret_version_for_client_secret' field is set, this field will be ignored.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#client_secret DialogflowCxWebhook#client_secret}
        '''
        result = self._values.get("client_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The OAuth scopes to grant.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#scopes DialogflowCxWebhook#scopes}
        '''
        result = self._values.get("scopes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def secret_version_for_client_secret(self) -> typing.Optional[builtins.str]:
        '''The name of the SecretManager secret version resource storing the client secret.

        If this field is set, the 'client_secret' field will be
        ignored.
        Format: 'projects/{project}/secrets/{secret}/versions/{version}'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#secret_version_for_client_secret DialogflowCxWebhook#secret_version_for_client_secret}
        '''
        result = self._values.get("secret_version_for_client_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxWebhookServiceDirectoryGenericWebServiceOauthConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxWebhookServiceDirectoryGenericWebServiceOauthConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxWebhook.DialogflowCxWebhookServiceDirectoryGenericWebServiceOauthConfigOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e900f59316e4bcbda6a92bb41907065aa22d1e35709ae77eb886f2df9e6117d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetClientSecret")
    def reset_client_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientSecret", []))

    @jsii.member(jsii_name="resetScopes")
    def reset_scopes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScopes", []))

    @jsii.member(jsii_name="resetSecretVersionForClientSecret")
    def reset_secret_version_for_client_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretVersionForClientSecret", []))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretInput")
    def client_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="scopesInput")
    def scopes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "scopesInput"))

    @builtins.property
    @jsii.member(jsii_name="secretVersionForClientSecretInput")
    def secret_version_for_client_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretVersionForClientSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="tokenEndpointInput")
    def token_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tokenEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__351166de62a5fba476c4ec6328f8ea1d79ed0e838ef7d6df45f2ab965e298c09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecret"))

    @client_secret.setter
    def client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ac0ffb65b637fd13b8ce75fcc4a157a897efd46372bdc1b846232f62c6d1ea2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scopes")
    def scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "scopes"))

    @scopes.setter
    def scopes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be60619cfab85a8ecef2cc38dda43ce53db34e6a537a2bde0560b1c36c2ef0bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scopes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretVersionForClientSecret")
    def secret_version_for_client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretVersionForClientSecret"))

    @secret_version_for_client_secret.setter
    def secret_version_for_client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf30f4c5ad27fd61c5466b6547c9508a976cfb6c0684a7e945f53292abd4cc3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretVersionForClientSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tokenEndpoint")
    def token_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tokenEndpoint"))

    @token_endpoint.setter
    def token_endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1035896602b34dd7f2c647cad66e79418d7e5c2c9b417be8db7a6e3cfef388e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tokenEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowCxWebhookServiceDirectoryGenericWebServiceOauthConfig]:
        return typing.cast(typing.Optional[DialogflowCxWebhookServiceDirectoryGenericWebServiceOauthConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxWebhookServiceDirectoryGenericWebServiceOauthConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b343ee8beeca417347871724d144baf66daff3b6d1240a428ca5d6072c39e69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DialogflowCxWebhookServiceDirectoryGenericWebServiceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxWebhook.DialogflowCxWebhookServiceDirectoryGenericWebServiceOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7243adb28c49f1abaf019d0636b2bb9e2304a379be95fa2742e00e9b7321c7b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOauthConfig")
    def put_oauth_config(
        self,
        *,
        client_id: builtins.str,
        token_endpoint: builtins.str,
        client_secret: typing.Optional[builtins.str] = None,
        scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
        secret_version_for_client_secret: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param client_id: The client ID provided by the 3rd party platform. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#client_id DialogflowCxWebhook#client_id}
        :param token_endpoint: The token endpoint provided by the 3rd party platform to exchange an access token. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#token_endpoint DialogflowCxWebhook#token_endpoint}
        :param client_secret: The client secret provided by the 3rd party platform. If the 'secret_version_for_client_secret' field is set, this field will be ignored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#client_secret DialogflowCxWebhook#client_secret}
        :param scopes: The OAuth scopes to grant. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#scopes DialogflowCxWebhook#scopes}
        :param secret_version_for_client_secret: The name of the SecretManager secret version resource storing the client secret. If this field is set, the 'client_secret' field will be ignored. Format: 'projects/{project}/secrets/{secret}/versions/{version}' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#secret_version_for_client_secret DialogflowCxWebhook#secret_version_for_client_secret}
        '''
        value = DialogflowCxWebhookServiceDirectoryGenericWebServiceOauthConfig(
            client_id=client_id,
            token_endpoint=token_endpoint,
            client_secret=client_secret,
            scopes=scopes,
            secret_version_for_client_secret=secret_version_for_client_secret,
        )

        return typing.cast(None, jsii.invoke(self, "putOauthConfig", [value]))

    @jsii.member(jsii_name="putSecretVersionsForRequestHeaders")
    def put_secret_versions_for_request_headers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DialogflowCxWebhookServiceDirectoryGenericWebServiceSecretVersionsForRequestHeaders", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13ba4bd6fed89c1ced606aa9f49b8a24da414593ab5c33747891bef406dd5558)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSecretVersionsForRequestHeaders", [value]))

    @jsii.member(jsii_name="resetAllowedCaCerts")
    def reset_allowed_ca_certs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedCaCerts", []))

    @jsii.member(jsii_name="resetHttpMethod")
    def reset_http_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpMethod", []))

    @jsii.member(jsii_name="resetOauthConfig")
    def reset_oauth_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauthConfig", []))

    @jsii.member(jsii_name="resetParameterMapping")
    def reset_parameter_mapping(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameterMapping", []))

    @jsii.member(jsii_name="resetRequestBody")
    def reset_request_body(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestBody", []))

    @jsii.member(jsii_name="resetRequestHeaders")
    def reset_request_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestHeaders", []))

    @jsii.member(jsii_name="resetSecretVersionForUsernamePassword")
    def reset_secret_version_for_username_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretVersionForUsernamePassword", []))

    @jsii.member(jsii_name="resetSecretVersionsForRequestHeaders")
    def reset_secret_versions_for_request_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretVersionsForRequestHeaders", []))

    @jsii.member(jsii_name="resetServiceAgentAuth")
    def reset_service_agent_auth(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceAgentAuth", []))

    @jsii.member(jsii_name="resetWebhookType")
    def reset_webhook_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWebhookType", []))

    @builtins.property
    @jsii.member(jsii_name="oauthConfig")
    def oauth_config(
        self,
    ) -> DialogflowCxWebhookServiceDirectoryGenericWebServiceOauthConfigOutputReference:
        return typing.cast(DialogflowCxWebhookServiceDirectoryGenericWebServiceOauthConfigOutputReference, jsii.get(self, "oauthConfig"))

    @builtins.property
    @jsii.member(jsii_name="secretVersionsForRequestHeaders")
    def secret_versions_for_request_headers(
        self,
    ) -> "DialogflowCxWebhookServiceDirectoryGenericWebServiceSecretVersionsForRequestHeadersList":
        return typing.cast("DialogflowCxWebhookServiceDirectoryGenericWebServiceSecretVersionsForRequestHeadersList", jsii.get(self, "secretVersionsForRequestHeaders"))

    @builtins.property
    @jsii.member(jsii_name="allowedCaCertsInput")
    def allowed_ca_certs_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedCaCertsInput"))

    @builtins.property
    @jsii.member(jsii_name="httpMethodInput")
    def http_method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpMethodInput"))

    @builtins.property
    @jsii.member(jsii_name="oauthConfigInput")
    def oauth_config_input(
        self,
    ) -> typing.Optional[DialogflowCxWebhookServiceDirectoryGenericWebServiceOauthConfig]:
        return typing.cast(typing.Optional[DialogflowCxWebhookServiceDirectoryGenericWebServiceOauthConfig], jsii.get(self, "oauthConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="parameterMappingInput")
    def parameter_mapping_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "parameterMappingInput"))

    @builtins.property
    @jsii.member(jsii_name="requestBodyInput")
    def request_body_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "requestBodyInput"))

    @builtins.property
    @jsii.member(jsii_name="requestHeadersInput")
    def request_headers_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "requestHeadersInput"))

    @builtins.property
    @jsii.member(jsii_name="secretVersionForUsernamePasswordInput")
    def secret_version_for_username_password_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretVersionForUsernamePasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="secretVersionsForRequestHeadersInput")
    def secret_versions_for_request_headers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DialogflowCxWebhookServiceDirectoryGenericWebServiceSecretVersionsForRequestHeaders"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DialogflowCxWebhookServiceDirectoryGenericWebServiceSecretVersionsForRequestHeaders"]]], jsii.get(self, "secretVersionsForRequestHeadersInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAgentAuthInput")
    def service_agent_auth_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAgentAuthInput"))

    @builtins.property
    @jsii.member(jsii_name="uriInput")
    def uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uriInput"))

    @builtins.property
    @jsii.member(jsii_name="webhookTypeInput")
    def webhook_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "webhookTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedCaCerts")
    def allowed_ca_certs(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedCaCerts"))

    @allowed_ca_certs.setter
    def allowed_ca_certs(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__667abb2b9b45a551ac068c25ecb82867fbc1b3e1f432b5b281461f660deb35f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedCaCerts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpMethod")
    def http_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpMethod"))

    @http_method.setter
    def http_method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b9c9d50bda223c6eb0f481e0ce4f50988c698040aebb9ed7b509244db4136a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpMethod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parameterMapping")
    def parameter_mapping(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "parameterMapping"))

    @parameter_mapping.setter
    def parameter_mapping(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ea4289b2221bd317923e3fc78629b0590a253b46c4e78e5e74efa44d03f59c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameterMapping", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requestBody")
    def request_body(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "requestBody"))

    @request_body.setter
    def request_body(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c688e43b86f36982dd1a42294afc3fe8b37c2c33aff169fc3cadb765d67d5ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestBody", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requestHeaders")
    def request_headers(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "requestHeaders"))

    @request_headers.setter
    def request_headers(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf219bea0d16192e27d3d3ffc41dc580bc44618726a71146c5f537bab33fc7ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestHeaders", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretVersionForUsernamePassword")
    def secret_version_for_username_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretVersionForUsernamePassword"))

    @secret_version_for_username_password.setter
    def secret_version_for_username_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e97bccefee1a935ad0ec18906e0354264152881c22a7f52b3fd6e0161ccf65d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretVersionForUsernamePassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAgentAuth")
    def service_agent_auth(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAgentAuth"))

    @service_agent_auth.setter
    def service_agent_auth(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c70be7f93ac728666dc91ef693e4967f263c2eb40f911d43ec46ec7ab5ab6a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAgentAuth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d341f36e2908672debb8a9dbefd54ce8157c4738157a626a68fb8c84f91e3391)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="webhookType")
    def webhook_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "webhookType"))

    @webhook_type.setter
    def webhook_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c97593b1bb674d101b89207da6db107d900f8964dbd0a51da761ebea3d4c84da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "webhookType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowCxWebhookServiceDirectoryGenericWebService]:
        return typing.cast(typing.Optional[DialogflowCxWebhookServiceDirectoryGenericWebService], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxWebhookServiceDirectoryGenericWebService],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a97006e3de85e85a1b13ddf236ec4414d949a4174eacea826c19c20621be07f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxWebhook.DialogflowCxWebhookServiceDirectoryGenericWebServiceSecretVersionsForRequestHeaders",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "secret_version": "secretVersion"},
)
class DialogflowCxWebhookServiceDirectoryGenericWebServiceSecretVersionsForRequestHeaders:
    def __init__(self, *, key: builtins.str, secret_version: builtins.str) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#key DialogflowCxWebhook#key}.
        :param secret_version: The SecretManager secret version resource storing the header value. Format: 'projects/{project}/secrets/{secret}/versions/{version}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#secret_version DialogflowCxWebhook#secret_version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3275abae74f99a763d96fcdc9d70c6cb14a052433b4335904bf48ca500d7f2c3)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument secret_version", value=secret_version, expected_type=type_hints["secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "secret_version": secret_version,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#key DialogflowCxWebhook#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secret_version(self) -> builtins.str:
        '''The SecretManager secret version resource storing the header value. Format: 'projects/{project}/secrets/{secret}/versions/{version}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#secret_version DialogflowCxWebhook#secret_version}
        '''
        result = self._values.get("secret_version")
        assert result is not None, "Required property 'secret_version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxWebhookServiceDirectoryGenericWebServiceSecretVersionsForRequestHeaders(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxWebhookServiceDirectoryGenericWebServiceSecretVersionsForRequestHeadersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxWebhook.DialogflowCxWebhookServiceDirectoryGenericWebServiceSecretVersionsForRequestHeadersList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3838bfc72172616e059edc3be1c282ac84912c13be5ea809d2bff10d4330cd5e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DialogflowCxWebhookServiceDirectoryGenericWebServiceSecretVersionsForRequestHeadersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__faa415461c81a918720b2009b0db27be4537452b0df88dec6412b91f1f6a5cd4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DialogflowCxWebhookServiceDirectoryGenericWebServiceSecretVersionsForRequestHeadersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a4cbc53a7cfa7e6226aa16f53651cd6db8401bc82d45551e68baf879c1f45b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc08ab0d26780a4c593f4b9a95fb72df922002b069583c4f02c2b1e431e7f1a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41a21509ac49dcda76a99ee27d75856b63e88131ceaae2dd7ed712cc47826aae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxWebhookServiceDirectoryGenericWebServiceSecretVersionsForRequestHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxWebhookServiceDirectoryGenericWebServiceSecretVersionsForRequestHeaders]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxWebhookServiceDirectoryGenericWebServiceSecretVersionsForRequestHeaders]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c68e04def67368fc596666a5ac6457a4c14e4a1ed4ca5f39dc669601c316c5dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DialogflowCxWebhookServiceDirectoryGenericWebServiceSecretVersionsForRequestHeadersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxWebhook.DialogflowCxWebhookServiceDirectoryGenericWebServiceSecretVersionsForRequestHeadersOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9991b97ef14d310810111ffd8d8bb16e4e3a27b4c4f318046e7856d9fb85def)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="secretVersionInput")
    def secret_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1e330b56292238272f8a721b6af36b96bb603a78d3917b665c4a624f7e210ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretVersion")
    def secret_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretVersion"))

    @secret_version.setter
    def secret_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6223708da366abe29561bd231081640d0ba75071b279463bee68521968350613)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxWebhookServiceDirectoryGenericWebServiceSecretVersionsForRequestHeaders]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxWebhookServiceDirectoryGenericWebServiceSecretVersionsForRequestHeaders]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxWebhookServiceDirectoryGenericWebServiceSecretVersionsForRequestHeaders]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d6b6cf81c547574f1a7f7ab81e730a2dd26da81fe4b9b4f519933c9b0ec598b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DialogflowCxWebhookServiceDirectoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxWebhook.DialogflowCxWebhookServiceDirectoryOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b9667b81e7bde05d8706ba3f2f09711c4df997b360ac3e0c685e9a61cf917d2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putGenericWebService")
    def put_generic_web_service(
        self,
        *,
        uri: builtins.str,
        allowed_ca_certs: typing.Optional[typing.Sequence[builtins.str]] = None,
        http_method: typing.Optional[builtins.str] = None,
        oauth_config: typing.Optional[typing.Union[DialogflowCxWebhookServiceDirectoryGenericWebServiceOauthConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        parameter_mapping: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        request_body: typing.Optional[builtins.str] = None,
        request_headers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        secret_version_for_username_password: typing.Optional[builtins.str] = None,
        secret_versions_for_request_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DialogflowCxWebhookServiceDirectoryGenericWebServiceSecretVersionsForRequestHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
        service_agent_auth: typing.Optional[builtins.str] = None,
        webhook_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param uri: The webhook URI for receiving POST requests. It must use https protocol. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#uri DialogflowCxWebhook#uri}
        :param allowed_ca_certs: Specifies a list of allowed custom CA certificates (in DER format) for HTTPS verification. This overrides the default SSL trust store. If this is empty or unspecified, Dialogflow will use Google's default trust store to verify certificates. N.B. Make sure the HTTPS server certificates are signed with "subject alt name". For instance a certificate can be self-signed using the following command, openssl x509 -req -days 200 -in example.com.csr -signkey example.com.key -out example.com.crt -extfile <(printf "\\nsubjectAltName='DNS:www.example.com'") Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#allowed_ca_certs DialogflowCxWebhook#allowed_ca_certs}
        :param http_method: HTTP method for the flexible webhook calls. Standard webhook always uses POST. Possible values: ["POST", "GET", "HEAD", "PUT", "DELETE", "PATCH", "OPTIONS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#http_method DialogflowCxWebhook#http_method}
        :param oauth_config: oauth_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#oauth_config DialogflowCxWebhook#oauth_config}
        :param parameter_mapping: Maps the values extracted from specific fields of the flexible webhook response into session parameters. - Key: session parameter name - Value: field path in the webhook response Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#parameter_mapping DialogflowCxWebhook#parameter_mapping}
        :param request_body: Defines a custom JSON object as request body to send to flexible webhook. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#request_body DialogflowCxWebhook#request_body}
        :param request_headers: The HTTP request headers to send together with webhook requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#request_headers DialogflowCxWebhook#request_headers}
        :param secret_version_for_username_password: The SecretManager secret version resource storing the username:password pair for HTTP Basic authentication. Format: 'projects/{project}/secrets/{secret}/versions/{version}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#secret_version_for_username_password DialogflowCxWebhook#secret_version_for_username_password}
        :param secret_versions_for_request_headers: secret_versions_for_request_headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#secret_versions_for_request_headers DialogflowCxWebhook#secret_versions_for_request_headers}
        :param service_agent_auth: Indicate the auth token type generated from the `Diglogflow service agent <https://cloud.google.com/iam/docs/service-agents#dialogflow-service-agent>`_. The generated token is sent in the Authorization header. Possible values: ["NONE", "ID_TOKEN", "ACCESS_TOKEN"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#service_agent_auth DialogflowCxWebhook#service_agent_auth}
        :param webhook_type: Type of the webhook. Possible values: ["STANDARD", "FLEXIBLE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#webhook_type DialogflowCxWebhook#webhook_type}
        '''
        value = DialogflowCxWebhookServiceDirectoryGenericWebService(
            uri=uri,
            allowed_ca_certs=allowed_ca_certs,
            http_method=http_method,
            oauth_config=oauth_config,
            parameter_mapping=parameter_mapping,
            request_body=request_body,
            request_headers=request_headers,
            secret_version_for_username_password=secret_version_for_username_password,
            secret_versions_for_request_headers=secret_versions_for_request_headers,
            service_agent_auth=service_agent_auth,
            webhook_type=webhook_type,
        )

        return typing.cast(None, jsii.invoke(self, "putGenericWebService", [value]))

    @jsii.member(jsii_name="resetGenericWebService")
    def reset_generic_web_service(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGenericWebService", []))

    @builtins.property
    @jsii.member(jsii_name="genericWebService")
    def generic_web_service(
        self,
    ) -> DialogflowCxWebhookServiceDirectoryGenericWebServiceOutputReference:
        return typing.cast(DialogflowCxWebhookServiceDirectoryGenericWebServiceOutputReference, jsii.get(self, "genericWebService"))

    @builtins.property
    @jsii.member(jsii_name="genericWebServiceInput")
    def generic_web_service_input(
        self,
    ) -> typing.Optional[DialogflowCxWebhookServiceDirectoryGenericWebService]:
        return typing.cast(typing.Optional[DialogflowCxWebhookServiceDirectoryGenericWebService], jsii.get(self, "genericWebServiceInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceInput")
    def service_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceInput"))

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "service"))

    @service.setter
    def service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0ef25b2a04ac685d31a49c9585f3d4f3431c38d9ee5303adad3152ee47d3789)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DialogflowCxWebhookServiceDirectory]:
        return typing.cast(typing.Optional[DialogflowCxWebhookServiceDirectory], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxWebhookServiceDirectory],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12a3087a1cc51c66ccf9838e8284141630e4132d828379befae34a688111da5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxWebhook.DialogflowCxWebhookTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class DialogflowCxWebhookTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#create DialogflowCxWebhook#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#delete DialogflowCxWebhook#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#update DialogflowCxWebhook#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c842b11bc836b822e631dc09ea9fdab93263ac1b64292e9ffd608d1ed25c44f)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#create DialogflowCxWebhook#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#delete DialogflowCxWebhook#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_webhook#update DialogflowCxWebhook#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxWebhookTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxWebhookTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxWebhook.DialogflowCxWebhookTimeoutsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60ac575fdea0be2fbf5413cc727e394d34c52b78f078347252be951ce07fcad3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetUpdate")
    def reset_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdate", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="updateInput")
    def update_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updateInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2473f847b51124ef314bc86732133e30482df838a60d0d987525ce048c84ef1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__759d977d4705eb2376dc398ad1b5b06c420612d49f6665c6e2e7de4e5fb81773)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1cf75d75b1304204cb248c9997afa99925246ca4193adf884a8a55884fc7618)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxWebhookTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxWebhookTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxWebhookTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8e509eeee1e74fc91c8a6b391d92aed9f118c6dc72dcca6aefe30b04b093c26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DialogflowCxWebhook",
    "DialogflowCxWebhookConfig",
    "DialogflowCxWebhookGenericWebService",
    "DialogflowCxWebhookGenericWebServiceOauthConfig",
    "DialogflowCxWebhookGenericWebServiceOauthConfigOutputReference",
    "DialogflowCxWebhookGenericWebServiceOutputReference",
    "DialogflowCxWebhookGenericWebServiceSecretVersionsForRequestHeaders",
    "DialogflowCxWebhookGenericWebServiceSecretVersionsForRequestHeadersList",
    "DialogflowCxWebhookGenericWebServiceSecretVersionsForRequestHeadersOutputReference",
    "DialogflowCxWebhookServiceDirectory",
    "DialogflowCxWebhookServiceDirectoryGenericWebService",
    "DialogflowCxWebhookServiceDirectoryGenericWebServiceOauthConfig",
    "DialogflowCxWebhookServiceDirectoryGenericWebServiceOauthConfigOutputReference",
    "DialogflowCxWebhookServiceDirectoryGenericWebServiceOutputReference",
    "DialogflowCxWebhookServiceDirectoryGenericWebServiceSecretVersionsForRequestHeaders",
    "DialogflowCxWebhookServiceDirectoryGenericWebServiceSecretVersionsForRequestHeadersList",
    "DialogflowCxWebhookServiceDirectoryGenericWebServiceSecretVersionsForRequestHeadersOutputReference",
    "DialogflowCxWebhookServiceDirectoryOutputReference",
    "DialogflowCxWebhookTimeouts",
    "DialogflowCxWebhookTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__f4b93fcd01ea757e5ec3ab0125b476ed1ce1879e7340c561093f46a6c5c06fd5(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    display_name: builtins.str,
    disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_spell_correction: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_stackdriver_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    generic_web_service: typing.Optional[typing.Union[DialogflowCxWebhookGenericWebService, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    parent: typing.Optional[builtins.str] = None,
    security_settings: typing.Optional[builtins.str] = None,
    service_directory: typing.Optional[typing.Union[DialogflowCxWebhookServiceDirectory, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DialogflowCxWebhookTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__eacadbbadf684021b4dc36f342b23a0dbcf3b1a4498c56f3a40b4f3ffe71146c(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91fae4ab9bfbef0f5e50cd9a79d59df896fec4e69407edcf466c18b222709c5c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecaa4d49729a5f2f7a43677750f91c8183ff0c0d004559a967276ac736a51513(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20ce4b624bde545de503aab832107743384f8e153f340930022fa9ae8e7285bd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cb96817df275dbc1d2b40b169209465882957a12a7ae2a3f75897816df65965(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__207814dd2883697b3454a914745ce5a882928fe1bbf07aa2efc6dd6ba15aeac6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4889ec9458daaa19e8ba0819d97cbc01360902452038340b0bf6909613c08e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f300ee23ad0c689af98070faa88309f648947661c4bb68b548aaea24169023e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00fa5f95387ada28f0ba68b5bd718306a2fbc72e6f84059c72240974d003931e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf107d7e01b697bbc304addf84c487c5b5c722c77a74fd9c7915bf150fd93d19(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    display_name: builtins.str,
    disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_spell_correction: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_stackdriver_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    generic_web_service: typing.Optional[typing.Union[DialogflowCxWebhookGenericWebService, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    parent: typing.Optional[builtins.str] = None,
    security_settings: typing.Optional[builtins.str] = None,
    service_directory: typing.Optional[typing.Union[DialogflowCxWebhookServiceDirectory, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DialogflowCxWebhookTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50e37ce6a32cce4e809bf9baa6d4ce943cfe151d2421d9ea60ccfa89e1488728(
    *,
    uri: builtins.str,
    allowed_ca_certs: typing.Optional[typing.Sequence[builtins.str]] = None,
    http_method: typing.Optional[builtins.str] = None,
    oauth_config: typing.Optional[typing.Union[DialogflowCxWebhookGenericWebServiceOauthConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    parameter_mapping: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    request_body: typing.Optional[builtins.str] = None,
    request_headers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    secret_version_for_username_password: typing.Optional[builtins.str] = None,
    secret_versions_for_request_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DialogflowCxWebhookGenericWebServiceSecretVersionsForRequestHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
    service_agent_auth: typing.Optional[builtins.str] = None,
    webhook_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b66a1bb2679d8cc9720ad5bca429c4d2d1196cded6a6f55e01f69a461334a52d(
    *,
    client_id: builtins.str,
    token_endpoint: builtins.str,
    client_secret: typing.Optional[builtins.str] = None,
    scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    secret_version_for_client_secret: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65a8010729e8b2f050c1b97f77f0f94971ca40e06563b51c9b7c22f0e98d5c0e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cc6bcaeff0779fd535e97be24ba26f7258fe67225e535c40cdb2fa6a0e355f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1ae551175023b95a3c25d7456a2930dd24ba197d5cced299eda38ff7ec37afd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__608e81bfc9f2fe752423c25abc66805f7475a150a208674b4f1aed7f34a942e0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5250e6a593e2366b53959944ef1ca1174bd66a7279d657986a541698dba8fb71(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ef5573b323ee99c535879e64984cb358dd28322f926b81cc1079caba619d2cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f828c918b576e06ead739baad1e1ed2e57dfeb660cea8deca4caa26805c039a(
    value: typing.Optional[DialogflowCxWebhookGenericWebServiceOauthConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__394bb3f2baadfd13359f5e5e02cbdd2d8d3669bad1d816ff00bddb77b5eae256(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb59fe3236a54f919a13acb6f5d4acc68d659cddeeb5d3b34ef870c65fbbf569(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DialogflowCxWebhookGenericWebServiceSecretVersionsForRequestHeaders, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__192c7d0caf0c94d9c288f94f9cc9f8cd82bb6a7521cf65ef139fa16362ed7673(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd635bdcf82947f630d239be22be30b7e390c5f9c7071d9c8e6bcdf1f5dd0eae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d0d3f9be36b2768e2f569e6e889473ba5e17ddb1cb4520b528b8175e2dd6b91(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__397ef6db342161dd8402b7e9cd5d4b9818c7b8cc1fbbf293d2cafddb0f3aa381(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54ee032cfad305ab6cd0f73585756afc6452c55e52d50c8b9cb3a0dadce0978f(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb2c512bbf2e2abc1f2e0c5077d1059fc9228fc21456eec1efa2907139c37f2f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6adcbb4c8625e01f99569fd92dcab65a2f1d1ea158f8a21823187a0ce247cb66(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0281b7b21ef7f30c48783ae0f2e91e0bdc120f4ecaae23d222a61ba4923865f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21e4307924efa6ad82ebec9312f697ea298c560b49a68cd64a964cff2b222ccc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cee718e5524901b06bcf398b6ae38da1fe4bb62c6b4e920d4353f9354ace2915(
    value: typing.Optional[DialogflowCxWebhookGenericWebService],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d835df2050fec798b3ee604656794d54c95c3d0da19827fba5864839b574744a(
    *,
    key: builtins.str,
    secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c09ca5e55c2e00b62d7945efea65c0ced06e70da00b5ea4d3011681ba6dd7bd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f6febc8eaa05d54ee23905e89b0dd032058c68246817272ac017c404978cc59(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc9324cc2a4386911ce8b4f85af240c29bcfc16d680f0a390baabcc0406697b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53224a1cbbcdc5e4987c409861ecb5dd9bd0765d3a026cbe780156b169d49023(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c9e730a31d1dba6f05576c68ec72654c9cb586ac70e0f30e60a2e7aa5fe7910(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5ab4f626415d69c2b3df3d16ace0fdd15d4188f7ed5f2de4634f0eae5b7b955(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxWebhookGenericWebServiceSecretVersionsForRequestHeaders]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f9ceb5f85cf97f171473c240c62b43a10f0833e98113ebf242c972f53d6dd4f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33d72d4bb78b6402ca32cf59979372b0b44905e47c9db1bac5c01dbd85ce4933(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f24c4f12c2e7ca208836cfbe3d56cc147af2289b8f47012870477c601cd04762(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d54b1f35590788c0c8f984d81f1959d1d312e89cdf300d963b82edcd77a57cd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxWebhookGenericWebServiceSecretVersionsForRequestHeaders]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4604191929dc5e32d2c60339f6215e0af0fd5775fe76ff7ec057a209c0387da3(
    *,
    service: builtins.str,
    generic_web_service: typing.Optional[typing.Union[DialogflowCxWebhookServiceDirectoryGenericWebService, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0c20721713bf45b99c0b87412272aa5d99d757709d88a13bdbc1c6cc9b07884(
    *,
    uri: builtins.str,
    allowed_ca_certs: typing.Optional[typing.Sequence[builtins.str]] = None,
    http_method: typing.Optional[builtins.str] = None,
    oauth_config: typing.Optional[typing.Union[DialogflowCxWebhookServiceDirectoryGenericWebServiceOauthConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    parameter_mapping: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    request_body: typing.Optional[builtins.str] = None,
    request_headers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    secret_version_for_username_password: typing.Optional[builtins.str] = None,
    secret_versions_for_request_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DialogflowCxWebhookServiceDirectoryGenericWebServiceSecretVersionsForRequestHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
    service_agent_auth: typing.Optional[builtins.str] = None,
    webhook_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3de165377f68e4dfac4fcb833658450aeef7a1c0d9cc0aa6617a6b71161a1e5(
    *,
    client_id: builtins.str,
    token_endpoint: builtins.str,
    client_secret: typing.Optional[builtins.str] = None,
    scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    secret_version_for_client_secret: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e900f59316e4bcbda6a92bb41907065aa22d1e35709ae77eb886f2df9e6117d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__351166de62a5fba476c4ec6328f8ea1d79ed0e838ef7d6df45f2ab965e298c09(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ac0ffb65b637fd13b8ce75fcc4a157a897efd46372bdc1b846232f62c6d1ea2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be60619cfab85a8ecef2cc38dda43ce53db34e6a537a2bde0560b1c36c2ef0bb(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf30f4c5ad27fd61c5466b6547c9508a976cfb6c0684a7e945f53292abd4cc3f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1035896602b34dd7f2c647cad66e79418d7e5c2c9b417be8db7a6e3cfef388e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b343ee8beeca417347871724d144baf66daff3b6d1240a428ca5d6072c39e69(
    value: typing.Optional[DialogflowCxWebhookServiceDirectoryGenericWebServiceOauthConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7243adb28c49f1abaf019d0636b2bb9e2304a379be95fa2742e00e9b7321c7b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13ba4bd6fed89c1ced606aa9f49b8a24da414593ab5c33747891bef406dd5558(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DialogflowCxWebhookServiceDirectoryGenericWebServiceSecretVersionsForRequestHeaders, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__667abb2b9b45a551ac068c25ecb82867fbc1b3e1f432b5b281461f660deb35f1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b9c9d50bda223c6eb0f481e0ce4f50988c698040aebb9ed7b509244db4136a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ea4289b2221bd317923e3fc78629b0590a253b46c4e78e5e74efa44d03f59c0(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c688e43b86f36982dd1a42294afc3fe8b37c2c33aff169fc3cadb765d67d5ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf219bea0d16192e27d3d3ffc41dc580bc44618726a71146c5f537bab33fc7ad(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e97bccefee1a935ad0ec18906e0354264152881c22a7f52b3fd6e0161ccf65d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c70be7f93ac728666dc91ef693e4967f263c2eb40f911d43ec46ec7ab5ab6a4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d341f36e2908672debb8a9dbefd54ce8157c4738157a626a68fb8c84f91e3391(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c97593b1bb674d101b89207da6db107d900f8964dbd0a51da761ebea3d4c84da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a97006e3de85e85a1b13ddf236ec4414d949a4174eacea826c19c20621be07f8(
    value: typing.Optional[DialogflowCxWebhookServiceDirectoryGenericWebService],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3275abae74f99a763d96fcdc9d70c6cb14a052433b4335904bf48ca500d7f2c3(
    *,
    key: builtins.str,
    secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3838bfc72172616e059edc3be1c282ac84912c13be5ea809d2bff10d4330cd5e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__faa415461c81a918720b2009b0db27be4537452b0df88dec6412b91f1f6a5cd4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a4cbc53a7cfa7e6226aa16f53651cd6db8401bc82d45551e68baf879c1f45b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc08ab0d26780a4c593f4b9a95fb72df922002b069583c4f02c2b1e431e7f1a2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41a21509ac49dcda76a99ee27d75856b63e88131ceaae2dd7ed712cc47826aae(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c68e04def67368fc596666a5ac6457a4c14e4a1ed4ca5f39dc669601c316c5dd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxWebhookServiceDirectoryGenericWebServiceSecretVersionsForRequestHeaders]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9991b97ef14d310810111ffd8d8bb16e4e3a27b4c4f318046e7856d9fb85def(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1e330b56292238272f8a721b6af36b96bb603a78d3917b665c4a624f7e210ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6223708da366abe29561bd231081640d0ba75071b279463bee68521968350613(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d6b6cf81c547574f1a7f7ab81e730a2dd26da81fe4b9b4f519933c9b0ec598b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxWebhookServiceDirectoryGenericWebServiceSecretVersionsForRequestHeaders]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b9667b81e7bde05d8706ba3f2f09711c4df997b360ac3e0c685e9a61cf917d2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0ef25b2a04ac685d31a49c9585f3d4f3431c38d9ee5303adad3152ee47d3789(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12a3087a1cc51c66ccf9838e8284141630e4132d828379befae34a688111da5d(
    value: typing.Optional[DialogflowCxWebhookServiceDirectory],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c842b11bc836b822e631dc09ea9fdab93263ac1b64292e9ffd608d1ed25c44f(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60ac575fdea0be2fbf5413cc727e394d34c52b78f078347252be951ce07fcad3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2473f847b51124ef314bc86732133e30482df838a60d0d987525ce048c84ef1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__759d977d4705eb2376dc398ad1b5b06c420612d49f6665c6e2e7de4e5fb81773(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1cf75d75b1304204cb248c9997afa99925246ca4193adf884a8a55884fc7618(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8e509eeee1e74fc91c8a6b391d92aed9f118c6dc72dcca6aefe30b04b093c26(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxWebhookTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
