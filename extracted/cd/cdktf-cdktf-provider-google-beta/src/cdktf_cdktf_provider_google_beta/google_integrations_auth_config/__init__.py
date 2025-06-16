r'''
# `google_integrations_auth_config`

Refer to the Terraform Registry for docs: [`google_integrations_auth_config`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config).
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


class GoogleIntegrationsAuthConfig(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationsAuthConfig.GoogleIntegrationsAuthConfig",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config google_integrations_auth_config}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        display_name: builtins.str,
        location: builtins.str,
        client_certificate: typing.Optional[typing.Union["GoogleIntegrationsAuthConfigClientCertificate", typing.Dict[builtins.str, typing.Any]]] = None,
        decrypted_credential: typing.Optional[typing.Union["GoogleIntegrationsAuthConfigDecryptedCredential", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        expiry_notification_duration: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        override_valid_time: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleIntegrationsAuthConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        visibility: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config google_integrations_auth_config} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param display_name: The name of the auth config. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#display_name GoogleIntegrationsAuthConfig#display_name}
        :param location: Location in which client needs to be provisioned. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#location GoogleIntegrationsAuthConfig#location}
        :param client_certificate: client_certificate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#client_certificate GoogleIntegrationsAuthConfig#client_certificate}
        :param decrypted_credential: decrypted_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#decrypted_credential GoogleIntegrationsAuthConfig#decrypted_credential}
        :param description: A description of the auth config. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#description GoogleIntegrationsAuthConfig#description}
        :param expiry_notification_duration: User can define the time to receive notification after which the auth config becomes invalid. Support up to 30 days. Support granularity in hours. A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#expiry_notification_duration GoogleIntegrationsAuthConfig#expiry_notification_duration}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#id GoogleIntegrationsAuthConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param override_valid_time: User provided expiry time to override. For the example of Salesforce, username/password credentials can be valid for 6 months depending on the instance settings. A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits. Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#override_valid_time GoogleIntegrationsAuthConfig#override_valid_time}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#project GoogleIntegrationsAuthConfig#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#timeouts GoogleIntegrationsAuthConfig#timeouts}
        :param visibility: The visibility of the auth config. Possible values: ["PRIVATE", "CLIENT_VISIBLE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#visibility GoogleIntegrationsAuthConfig#visibility}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee9493c096b6697926a4348d4ad6593f51d999513f08a5bc0b80eb0d8c86c6d6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleIntegrationsAuthConfigConfig(
            display_name=display_name,
            location=location,
            client_certificate=client_certificate,
            decrypted_credential=decrypted_credential,
            description=description,
            expiry_notification_duration=expiry_notification_duration,
            id=id,
            override_valid_time=override_valid_time,
            project=project,
            timeouts=timeouts,
            visibility=visibility,
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
        '''Generates CDKTF code for importing a GoogleIntegrationsAuthConfig resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleIntegrationsAuthConfig to import.
        :param import_from_id: The id of the existing GoogleIntegrationsAuthConfig that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleIntegrationsAuthConfig to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28d4cc60494f0041175dc1cf34a368149ac6e2f7f2d5f46172d9a0dbd9c5b437)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putClientCertificate")
    def put_client_certificate(
        self,
        *,
        encrypted_private_key: builtins.str,
        ssl_certificate: builtins.str,
        passphrase: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param encrypted_private_key: The ssl certificate encoded in PEM format. This string must include the begin header and end footer lines. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#encrypted_private_key GoogleIntegrationsAuthConfig#encrypted_private_key}
        :param ssl_certificate: The ssl certificate encoded in PEM format. This string must include the begin header and end footer lines. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#ssl_certificate GoogleIntegrationsAuthConfig#ssl_certificate}
        :param passphrase: 'passphrase' should be left unset if private key is not encrypted. Note that 'passphrase' is not the password for web server, but an extra layer of security to protected private key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#passphrase GoogleIntegrationsAuthConfig#passphrase}
        '''
        value = GoogleIntegrationsAuthConfigClientCertificate(
            encrypted_private_key=encrypted_private_key,
            ssl_certificate=ssl_certificate,
            passphrase=passphrase,
        )

        return typing.cast(None, jsii.invoke(self, "putClientCertificate", [value]))

    @jsii.member(jsii_name="putDecryptedCredential")
    def put_decrypted_credential(
        self,
        *,
        credential_type: builtins.str,
        auth_token: typing.Optional[typing.Union["GoogleIntegrationsAuthConfigDecryptedCredentialAuthToken", typing.Dict[builtins.str, typing.Any]]] = None,
        jwt: typing.Optional[typing.Union["GoogleIntegrationsAuthConfigDecryptedCredentialJwt", typing.Dict[builtins.str, typing.Any]]] = None,
        oauth2_authorization_code: typing.Optional[typing.Union["GoogleIntegrationsAuthConfigDecryptedCredentialOauth2AuthorizationCode", typing.Dict[builtins.str, typing.Any]]] = None,
        oauth2_client_credentials: typing.Optional[typing.Union["GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentials", typing.Dict[builtins.str, typing.Any]]] = None,
        oidc_token: typing.Optional[typing.Union["GoogleIntegrationsAuthConfigDecryptedCredentialOidcToken", typing.Dict[builtins.str, typing.Any]]] = None,
        service_account_credentials: typing.Optional[typing.Union["GoogleIntegrationsAuthConfigDecryptedCredentialServiceAccountCredentials", typing.Dict[builtins.str, typing.Any]]] = None,
        username_and_password: typing.Optional[typing.Union["GoogleIntegrationsAuthConfigDecryptedCredentialUsernameAndPassword", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param credential_type: Credential type associated with auth configs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#credential_type GoogleIntegrationsAuthConfig#credential_type}
        :param auth_token: auth_token block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#auth_token GoogleIntegrationsAuthConfig#auth_token}
        :param jwt: jwt block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#jwt GoogleIntegrationsAuthConfig#jwt}
        :param oauth2_authorization_code: oauth2_authorization_code block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#oauth2_authorization_code GoogleIntegrationsAuthConfig#oauth2_authorization_code}
        :param oauth2_client_credentials: oauth2_client_credentials block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#oauth2_client_credentials GoogleIntegrationsAuthConfig#oauth2_client_credentials}
        :param oidc_token: oidc_token block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#oidc_token GoogleIntegrationsAuthConfig#oidc_token}
        :param service_account_credentials: service_account_credentials block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#service_account_credentials GoogleIntegrationsAuthConfig#service_account_credentials}
        :param username_and_password: username_and_password block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#username_and_password GoogleIntegrationsAuthConfig#username_and_password}
        '''
        value = GoogleIntegrationsAuthConfigDecryptedCredential(
            credential_type=credential_type,
            auth_token=auth_token,
            jwt=jwt,
            oauth2_authorization_code=oauth2_authorization_code,
            oauth2_client_credentials=oauth2_client_credentials,
            oidc_token=oidc_token,
            service_account_credentials=service_account_credentials,
            username_and_password=username_and_password,
        )

        return typing.cast(None, jsii.invoke(self, "putDecryptedCredential", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#create GoogleIntegrationsAuthConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#delete GoogleIntegrationsAuthConfig#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#update GoogleIntegrationsAuthConfig#update}.
        '''
        value = GoogleIntegrationsAuthConfigTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetClientCertificate")
    def reset_client_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientCertificate", []))

    @jsii.member(jsii_name="resetDecryptedCredential")
    def reset_decrypted_credential(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDecryptedCredential", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetExpiryNotificationDuration")
    def reset_expiry_notification_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpiryNotificationDuration", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetOverrideValidTime")
    def reset_override_valid_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOverrideValidTime", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetVisibility")
    def reset_visibility(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVisibility", []))

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
    @jsii.member(jsii_name="certificateId")
    def certificate_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificateId"))

    @builtins.property
    @jsii.member(jsii_name="clientCertificate")
    def client_certificate(
        self,
    ) -> "GoogleIntegrationsAuthConfigClientCertificateOutputReference":
        return typing.cast("GoogleIntegrationsAuthConfigClientCertificateOutputReference", jsii.get(self, "clientCertificate"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="creatorEmail")
    def creator_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "creatorEmail"))

    @builtins.property
    @jsii.member(jsii_name="credentialType")
    def credential_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "credentialType"))

    @builtins.property
    @jsii.member(jsii_name="decryptedCredential")
    def decrypted_credential(
        self,
    ) -> "GoogleIntegrationsAuthConfigDecryptedCredentialOutputReference":
        return typing.cast("GoogleIntegrationsAuthConfigDecryptedCredentialOutputReference", jsii.get(self, "decryptedCredential"))

    @builtins.property
    @jsii.member(jsii_name="encryptedCredential")
    def encrypted_credential(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encryptedCredential"))

    @builtins.property
    @jsii.member(jsii_name="lastModifierEmail")
    def last_modifier_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastModifierEmail"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="reason")
    def reason(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "reason"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleIntegrationsAuthConfigTimeoutsOutputReference":
        return typing.cast("GoogleIntegrationsAuthConfigTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="validTime")
    def valid_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "validTime"))

    @builtins.property
    @jsii.member(jsii_name="clientCertificateInput")
    def client_certificate_input(
        self,
    ) -> typing.Optional["GoogleIntegrationsAuthConfigClientCertificate"]:
        return typing.cast(typing.Optional["GoogleIntegrationsAuthConfigClientCertificate"], jsii.get(self, "clientCertificateInput"))

    @builtins.property
    @jsii.member(jsii_name="decryptedCredentialInput")
    def decrypted_credential_input(
        self,
    ) -> typing.Optional["GoogleIntegrationsAuthConfigDecryptedCredential"]:
        return typing.cast(typing.Optional["GoogleIntegrationsAuthConfigDecryptedCredential"], jsii.get(self, "decryptedCredentialInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="expiryNotificationDurationInput")
    def expiry_notification_duration_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "expiryNotificationDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="overrideValidTimeInput")
    def override_valid_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "overrideValidTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleIntegrationsAuthConfigTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleIntegrationsAuthConfigTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="visibilityInput")
    def visibility_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "visibilityInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40d6b4352aface14d48de484e0bd0cd920d32ef63a8a72e89a944dd5084db134)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2f9bd1128323bd5a13716e9fc28dc2ecd8816b29b15db7061b2524f07797c43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expiryNotificationDuration")
    def expiry_notification_duration(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "expiryNotificationDuration"))

    @expiry_notification_duration.setter
    def expiry_notification_duration(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__453f6521dca419452da47b8f90aa9558958a1e8e611e674b30e563885800c37c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expiryNotificationDuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d8609649fe8f6fc4f4c939a74d4c70b71c9c6f245c8bacd85da8d7ac255a186)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0cffb2f048b3418bcf294ed1e907fb79118a00328557c7f1699d822b220f58f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="overrideValidTime")
    def override_valid_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "overrideValidTime"))

    @override_valid_time.setter
    def override_valid_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fd45caa23bda6dfefad6f9fd6fe3c9470b3c8a72230c09cd5994b4998d0e290)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "overrideValidTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__839c1605efd4c51ece5ce48161d22838df7fa6856fbbf39818988a94cf057714)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="visibility")
    def visibility(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "visibility"))

    @visibility.setter
    def visibility(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08ed3bd4a8bc2852e5d00f9af822041172d9eb81ecd6fe15a83092f8d4914780)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "visibility", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIntegrationsAuthConfig.GoogleIntegrationsAuthConfigClientCertificate",
    jsii_struct_bases=[],
    name_mapping={
        "encrypted_private_key": "encryptedPrivateKey",
        "ssl_certificate": "sslCertificate",
        "passphrase": "passphrase",
    },
)
class GoogleIntegrationsAuthConfigClientCertificate:
    def __init__(
        self,
        *,
        encrypted_private_key: builtins.str,
        ssl_certificate: builtins.str,
        passphrase: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param encrypted_private_key: The ssl certificate encoded in PEM format. This string must include the begin header and end footer lines. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#encrypted_private_key GoogleIntegrationsAuthConfig#encrypted_private_key}
        :param ssl_certificate: The ssl certificate encoded in PEM format. This string must include the begin header and end footer lines. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#ssl_certificate GoogleIntegrationsAuthConfig#ssl_certificate}
        :param passphrase: 'passphrase' should be left unset if private key is not encrypted. Note that 'passphrase' is not the password for web server, but an extra layer of security to protected private key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#passphrase GoogleIntegrationsAuthConfig#passphrase}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__313726a9c92776aff936e1e7ebbae16f9833cf5b8136472cf4acaff6c1640977)
            check_type(argname="argument encrypted_private_key", value=encrypted_private_key, expected_type=type_hints["encrypted_private_key"])
            check_type(argname="argument ssl_certificate", value=ssl_certificate, expected_type=type_hints["ssl_certificate"])
            check_type(argname="argument passphrase", value=passphrase, expected_type=type_hints["passphrase"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "encrypted_private_key": encrypted_private_key,
            "ssl_certificate": ssl_certificate,
        }
        if passphrase is not None:
            self._values["passphrase"] = passphrase

    @builtins.property
    def encrypted_private_key(self) -> builtins.str:
        '''The ssl certificate encoded in PEM format. This string must include the begin header and end footer lines.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#encrypted_private_key GoogleIntegrationsAuthConfig#encrypted_private_key}
        '''
        result = self._values.get("encrypted_private_key")
        assert result is not None, "Required property 'encrypted_private_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ssl_certificate(self) -> builtins.str:
        '''The ssl certificate encoded in PEM format. This string must include the begin header and end footer lines.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#ssl_certificate GoogleIntegrationsAuthConfig#ssl_certificate}
        '''
        result = self._values.get("ssl_certificate")
        assert result is not None, "Required property 'ssl_certificate' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def passphrase(self) -> typing.Optional[builtins.str]:
        ''''passphrase' should be left unset if private key is not encrypted.

        Note that 'passphrase' is not the password for web server, but an extra layer of security to protected private key.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#passphrase GoogleIntegrationsAuthConfig#passphrase}
        '''
        result = self._values.get("passphrase")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIntegrationsAuthConfigClientCertificate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIntegrationsAuthConfigClientCertificateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationsAuthConfig.GoogleIntegrationsAuthConfigClientCertificateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2f3d733a6be5f6a5033fddbe4b7b37ed4ed96ed369f4e502a806c5a7fa9b9eee)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPassphrase")
    def reset_passphrase(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassphrase", []))

    @builtins.property
    @jsii.member(jsii_name="encryptedPrivateKeyInput")
    def encrypted_private_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "encryptedPrivateKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="passphraseInput")
    def passphrase_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passphraseInput"))

    @builtins.property
    @jsii.member(jsii_name="sslCertificateInput")
    def ssl_certificate_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sslCertificateInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptedPrivateKey")
    def encrypted_private_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encryptedPrivateKey"))

    @encrypted_private_key.setter
    def encrypted_private_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fdd5f394d1f0f9d99d16ddf50134be56a67053299f316f91efba5b646ffaeab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptedPrivateKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="passphrase")
    def passphrase(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "passphrase"))

    @passphrase.setter
    def passphrase(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbd7380534a58e215baa2ecd36d2f20ec37249e9d4526dbdcd6996a9f7f0bd98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passphrase", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sslCertificate")
    def ssl_certificate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sslCertificate"))

    @ssl_certificate.setter
    def ssl_certificate(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d91cf98d904aa888e1094d3c59c80f37c24d8dcf19f8b8a288b388e7fb6ff0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sslCertificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIntegrationsAuthConfigClientCertificate]:
        return typing.cast(typing.Optional[GoogleIntegrationsAuthConfigClientCertificate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIntegrationsAuthConfigClientCertificate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__961785801b82f88a19d5b3da8cd86c5296a67415598d1d368049a21dfe48ccfb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIntegrationsAuthConfig.GoogleIntegrationsAuthConfigConfig",
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
        "location": "location",
        "client_certificate": "clientCertificate",
        "decrypted_credential": "decryptedCredential",
        "description": "description",
        "expiry_notification_duration": "expiryNotificationDuration",
        "id": "id",
        "override_valid_time": "overrideValidTime",
        "project": "project",
        "timeouts": "timeouts",
        "visibility": "visibility",
    },
)
class GoogleIntegrationsAuthConfigConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        location: builtins.str,
        client_certificate: typing.Optional[typing.Union[GoogleIntegrationsAuthConfigClientCertificate, typing.Dict[builtins.str, typing.Any]]] = None,
        decrypted_credential: typing.Optional[typing.Union["GoogleIntegrationsAuthConfigDecryptedCredential", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        expiry_notification_duration: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        override_valid_time: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleIntegrationsAuthConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        visibility: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param display_name: The name of the auth config. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#display_name GoogleIntegrationsAuthConfig#display_name}
        :param location: Location in which client needs to be provisioned. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#location GoogleIntegrationsAuthConfig#location}
        :param client_certificate: client_certificate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#client_certificate GoogleIntegrationsAuthConfig#client_certificate}
        :param decrypted_credential: decrypted_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#decrypted_credential GoogleIntegrationsAuthConfig#decrypted_credential}
        :param description: A description of the auth config. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#description GoogleIntegrationsAuthConfig#description}
        :param expiry_notification_duration: User can define the time to receive notification after which the auth config becomes invalid. Support up to 30 days. Support granularity in hours. A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#expiry_notification_duration GoogleIntegrationsAuthConfig#expiry_notification_duration}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#id GoogleIntegrationsAuthConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param override_valid_time: User provided expiry time to override. For the example of Salesforce, username/password credentials can be valid for 6 months depending on the instance settings. A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits. Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#override_valid_time GoogleIntegrationsAuthConfig#override_valid_time}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#project GoogleIntegrationsAuthConfig#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#timeouts GoogleIntegrationsAuthConfig#timeouts}
        :param visibility: The visibility of the auth config. Possible values: ["PRIVATE", "CLIENT_VISIBLE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#visibility GoogleIntegrationsAuthConfig#visibility}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(client_certificate, dict):
            client_certificate = GoogleIntegrationsAuthConfigClientCertificate(**client_certificate)
        if isinstance(decrypted_credential, dict):
            decrypted_credential = GoogleIntegrationsAuthConfigDecryptedCredential(**decrypted_credential)
        if isinstance(timeouts, dict):
            timeouts = GoogleIntegrationsAuthConfigTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__685871352baed33cb5f97b6ed78dbf48e11cf271446ecb6d89569c77a1bd7a01)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument client_certificate", value=client_certificate, expected_type=type_hints["client_certificate"])
            check_type(argname="argument decrypted_credential", value=decrypted_credential, expected_type=type_hints["decrypted_credential"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument expiry_notification_duration", value=expiry_notification_duration, expected_type=type_hints["expiry_notification_duration"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument override_valid_time", value=override_valid_time, expected_type=type_hints["override_valid_time"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument visibility", value=visibility, expected_type=type_hints["visibility"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "display_name": display_name,
            "location": location,
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
        if client_certificate is not None:
            self._values["client_certificate"] = client_certificate
        if decrypted_credential is not None:
            self._values["decrypted_credential"] = decrypted_credential
        if description is not None:
            self._values["description"] = description
        if expiry_notification_duration is not None:
            self._values["expiry_notification_duration"] = expiry_notification_duration
        if id is not None:
            self._values["id"] = id
        if override_valid_time is not None:
            self._values["override_valid_time"] = override_valid_time
        if project is not None:
            self._values["project"] = project
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if visibility is not None:
            self._values["visibility"] = visibility

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
        '''The name of the auth config.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#display_name GoogleIntegrationsAuthConfig#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Location in which client needs to be provisioned.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#location GoogleIntegrationsAuthConfig#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_certificate(
        self,
    ) -> typing.Optional[GoogleIntegrationsAuthConfigClientCertificate]:
        '''client_certificate block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#client_certificate GoogleIntegrationsAuthConfig#client_certificate}
        '''
        result = self._values.get("client_certificate")
        return typing.cast(typing.Optional[GoogleIntegrationsAuthConfigClientCertificate], result)

    @builtins.property
    def decrypted_credential(
        self,
    ) -> typing.Optional["GoogleIntegrationsAuthConfigDecryptedCredential"]:
        '''decrypted_credential block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#decrypted_credential GoogleIntegrationsAuthConfig#decrypted_credential}
        '''
        result = self._values.get("decrypted_credential")
        return typing.cast(typing.Optional["GoogleIntegrationsAuthConfigDecryptedCredential"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the auth config.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#description GoogleIntegrationsAuthConfig#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def expiry_notification_duration(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''User can define the time to receive notification after which the auth config becomes invalid.

        Support up to 30 days. Support granularity in hours.

        A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.5s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#expiry_notification_duration GoogleIntegrationsAuthConfig#expiry_notification_duration}
        '''
        result = self._values.get("expiry_notification_duration")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#id GoogleIntegrationsAuthConfig#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def override_valid_time(self) -> typing.Optional[builtins.str]:
        '''User provided expiry time to override.

        For the example of Salesforce, username/password credentials can be valid for 6 months depending on the instance settings.

        A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits. Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#override_valid_time GoogleIntegrationsAuthConfig#override_valid_time}
        '''
        result = self._values.get("override_valid_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#project GoogleIntegrationsAuthConfig#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleIntegrationsAuthConfigTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#timeouts GoogleIntegrationsAuthConfig#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleIntegrationsAuthConfigTimeouts"], result)

    @builtins.property
    def visibility(self) -> typing.Optional[builtins.str]:
        '''The visibility of the auth config. Possible values: ["PRIVATE", "CLIENT_VISIBLE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#visibility GoogleIntegrationsAuthConfig#visibility}
        '''
        result = self._values.get("visibility")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIntegrationsAuthConfigConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIntegrationsAuthConfig.GoogleIntegrationsAuthConfigDecryptedCredential",
    jsii_struct_bases=[],
    name_mapping={
        "credential_type": "credentialType",
        "auth_token": "authToken",
        "jwt": "jwt",
        "oauth2_authorization_code": "oauth2AuthorizationCode",
        "oauth2_client_credentials": "oauth2ClientCredentials",
        "oidc_token": "oidcToken",
        "service_account_credentials": "serviceAccountCredentials",
        "username_and_password": "usernameAndPassword",
    },
)
class GoogleIntegrationsAuthConfigDecryptedCredential:
    def __init__(
        self,
        *,
        credential_type: builtins.str,
        auth_token: typing.Optional[typing.Union["GoogleIntegrationsAuthConfigDecryptedCredentialAuthToken", typing.Dict[builtins.str, typing.Any]]] = None,
        jwt: typing.Optional[typing.Union["GoogleIntegrationsAuthConfigDecryptedCredentialJwt", typing.Dict[builtins.str, typing.Any]]] = None,
        oauth2_authorization_code: typing.Optional[typing.Union["GoogleIntegrationsAuthConfigDecryptedCredentialOauth2AuthorizationCode", typing.Dict[builtins.str, typing.Any]]] = None,
        oauth2_client_credentials: typing.Optional[typing.Union["GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentials", typing.Dict[builtins.str, typing.Any]]] = None,
        oidc_token: typing.Optional[typing.Union["GoogleIntegrationsAuthConfigDecryptedCredentialOidcToken", typing.Dict[builtins.str, typing.Any]]] = None,
        service_account_credentials: typing.Optional[typing.Union["GoogleIntegrationsAuthConfigDecryptedCredentialServiceAccountCredentials", typing.Dict[builtins.str, typing.Any]]] = None,
        username_and_password: typing.Optional[typing.Union["GoogleIntegrationsAuthConfigDecryptedCredentialUsernameAndPassword", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param credential_type: Credential type associated with auth configs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#credential_type GoogleIntegrationsAuthConfig#credential_type}
        :param auth_token: auth_token block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#auth_token GoogleIntegrationsAuthConfig#auth_token}
        :param jwt: jwt block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#jwt GoogleIntegrationsAuthConfig#jwt}
        :param oauth2_authorization_code: oauth2_authorization_code block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#oauth2_authorization_code GoogleIntegrationsAuthConfig#oauth2_authorization_code}
        :param oauth2_client_credentials: oauth2_client_credentials block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#oauth2_client_credentials GoogleIntegrationsAuthConfig#oauth2_client_credentials}
        :param oidc_token: oidc_token block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#oidc_token GoogleIntegrationsAuthConfig#oidc_token}
        :param service_account_credentials: service_account_credentials block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#service_account_credentials GoogleIntegrationsAuthConfig#service_account_credentials}
        :param username_and_password: username_and_password block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#username_and_password GoogleIntegrationsAuthConfig#username_and_password}
        '''
        if isinstance(auth_token, dict):
            auth_token = GoogleIntegrationsAuthConfigDecryptedCredentialAuthToken(**auth_token)
        if isinstance(jwt, dict):
            jwt = GoogleIntegrationsAuthConfigDecryptedCredentialJwt(**jwt)
        if isinstance(oauth2_authorization_code, dict):
            oauth2_authorization_code = GoogleIntegrationsAuthConfigDecryptedCredentialOauth2AuthorizationCode(**oauth2_authorization_code)
        if isinstance(oauth2_client_credentials, dict):
            oauth2_client_credentials = GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentials(**oauth2_client_credentials)
        if isinstance(oidc_token, dict):
            oidc_token = GoogleIntegrationsAuthConfigDecryptedCredentialOidcToken(**oidc_token)
        if isinstance(service_account_credentials, dict):
            service_account_credentials = GoogleIntegrationsAuthConfigDecryptedCredentialServiceAccountCredentials(**service_account_credentials)
        if isinstance(username_and_password, dict):
            username_and_password = GoogleIntegrationsAuthConfigDecryptedCredentialUsernameAndPassword(**username_and_password)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93d0b99a71af54e8c11e1815002bc21b6859b8cc337d52741978197b832436be)
            check_type(argname="argument credential_type", value=credential_type, expected_type=type_hints["credential_type"])
            check_type(argname="argument auth_token", value=auth_token, expected_type=type_hints["auth_token"])
            check_type(argname="argument jwt", value=jwt, expected_type=type_hints["jwt"])
            check_type(argname="argument oauth2_authorization_code", value=oauth2_authorization_code, expected_type=type_hints["oauth2_authorization_code"])
            check_type(argname="argument oauth2_client_credentials", value=oauth2_client_credentials, expected_type=type_hints["oauth2_client_credentials"])
            check_type(argname="argument oidc_token", value=oidc_token, expected_type=type_hints["oidc_token"])
            check_type(argname="argument service_account_credentials", value=service_account_credentials, expected_type=type_hints["service_account_credentials"])
            check_type(argname="argument username_and_password", value=username_and_password, expected_type=type_hints["username_and_password"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "credential_type": credential_type,
        }
        if auth_token is not None:
            self._values["auth_token"] = auth_token
        if jwt is not None:
            self._values["jwt"] = jwt
        if oauth2_authorization_code is not None:
            self._values["oauth2_authorization_code"] = oauth2_authorization_code
        if oauth2_client_credentials is not None:
            self._values["oauth2_client_credentials"] = oauth2_client_credentials
        if oidc_token is not None:
            self._values["oidc_token"] = oidc_token
        if service_account_credentials is not None:
            self._values["service_account_credentials"] = service_account_credentials
        if username_and_password is not None:
            self._values["username_and_password"] = username_and_password

    @builtins.property
    def credential_type(self) -> builtins.str:
        '''Credential type associated with auth configs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#credential_type GoogleIntegrationsAuthConfig#credential_type}
        '''
        result = self._values.get("credential_type")
        assert result is not None, "Required property 'credential_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auth_token(
        self,
    ) -> typing.Optional["GoogleIntegrationsAuthConfigDecryptedCredentialAuthToken"]:
        '''auth_token block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#auth_token GoogleIntegrationsAuthConfig#auth_token}
        '''
        result = self._values.get("auth_token")
        return typing.cast(typing.Optional["GoogleIntegrationsAuthConfigDecryptedCredentialAuthToken"], result)

    @builtins.property
    def jwt(
        self,
    ) -> typing.Optional["GoogleIntegrationsAuthConfigDecryptedCredentialJwt"]:
        '''jwt block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#jwt GoogleIntegrationsAuthConfig#jwt}
        '''
        result = self._values.get("jwt")
        return typing.cast(typing.Optional["GoogleIntegrationsAuthConfigDecryptedCredentialJwt"], result)

    @builtins.property
    def oauth2_authorization_code(
        self,
    ) -> typing.Optional["GoogleIntegrationsAuthConfigDecryptedCredentialOauth2AuthorizationCode"]:
        '''oauth2_authorization_code block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#oauth2_authorization_code GoogleIntegrationsAuthConfig#oauth2_authorization_code}
        '''
        result = self._values.get("oauth2_authorization_code")
        return typing.cast(typing.Optional["GoogleIntegrationsAuthConfigDecryptedCredentialOauth2AuthorizationCode"], result)

    @builtins.property
    def oauth2_client_credentials(
        self,
    ) -> typing.Optional["GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentials"]:
        '''oauth2_client_credentials block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#oauth2_client_credentials GoogleIntegrationsAuthConfig#oauth2_client_credentials}
        '''
        result = self._values.get("oauth2_client_credentials")
        return typing.cast(typing.Optional["GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentials"], result)

    @builtins.property
    def oidc_token(
        self,
    ) -> typing.Optional["GoogleIntegrationsAuthConfigDecryptedCredentialOidcToken"]:
        '''oidc_token block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#oidc_token GoogleIntegrationsAuthConfig#oidc_token}
        '''
        result = self._values.get("oidc_token")
        return typing.cast(typing.Optional["GoogleIntegrationsAuthConfigDecryptedCredentialOidcToken"], result)

    @builtins.property
    def service_account_credentials(
        self,
    ) -> typing.Optional["GoogleIntegrationsAuthConfigDecryptedCredentialServiceAccountCredentials"]:
        '''service_account_credentials block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#service_account_credentials GoogleIntegrationsAuthConfig#service_account_credentials}
        '''
        result = self._values.get("service_account_credentials")
        return typing.cast(typing.Optional["GoogleIntegrationsAuthConfigDecryptedCredentialServiceAccountCredentials"], result)

    @builtins.property
    def username_and_password(
        self,
    ) -> typing.Optional["GoogleIntegrationsAuthConfigDecryptedCredentialUsernameAndPassword"]:
        '''username_and_password block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#username_and_password GoogleIntegrationsAuthConfig#username_and_password}
        '''
        result = self._values.get("username_and_password")
        return typing.cast(typing.Optional["GoogleIntegrationsAuthConfigDecryptedCredentialUsernameAndPassword"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIntegrationsAuthConfigDecryptedCredential(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIntegrationsAuthConfig.GoogleIntegrationsAuthConfigDecryptedCredentialAuthToken",
    jsii_struct_bases=[],
    name_mapping={"token": "token", "type": "type"},
)
class GoogleIntegrationsAuthConfigDecryptedCredentialAuthToken:
    def __init__(
        self,
        *,
        token: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param token: The token for the auth type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#token GoogleIntegrationsAuthConfig#token}
        :param type: Authentication type, e.g. "Basic", "Bearer", etc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#type GoogleIntegrationsAuthConfig#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc0446fa5fde5a2aa70772377c7ec14f7190c691a2077fa63a54e608097dab49)
            check_type(argname="argument token", value=token, expected_type=type_hints["token"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if token is not None:
            self._values["token"] = token
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def token(self) -> typing.Optional[builtins.str]:
        '''The token for the auth type.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#token GoogleIntegrationsAuthConfig#token}
        '''
        result = self._values.get("token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Authentication type, e.g. "Basic", "Bearer", etc.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#type GoogleIntegrationsAuthConfig#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIntegrationsAuthConfigDecryptedCredentialAuthToken(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIntegrationsAuthConfigDecryptedCredentialAuthTokenOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationsAuthConfig.GoogleIntegrationsAuthConfigDecryptedCredentialAuthTokenOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ffc89b82ff32a0442a6bbf8a8babcb0669f6ba1d23fcc2ea6ac768d445cbc675)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetToken")
    def reset_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetToken", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="tokenInput")
    def token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tokenInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="token")
    def token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "token"))

    @token.setter
    def token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b43a5d2e80f9e9b46ef6081298804cbfa1205af7601e18b9a4778993aa4a1b37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "token", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab7e9be4b23f704ed38a7573b0cbabe28b76147879da832fd7dfb2250472fefb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIntegrationsAuthConfigDecryptedCredentialAuthToken]:
        return typing.cast(typing.Optional[GoogleIntegrationsAuthConfigDecryptedCredentialAuthToken], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIntegrationsAuthConfigDecryptedCredentialAuthToken],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a222d6f1d7f639343fc3fdff9d85e6805c798207c9e1228cf362c8cc73f440bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIntegrationsAuthConfig.GoogleIntegrationsAuthConfigDecryptedCredentialJwt",
    jsii_struct_bases=[],
    name_mapping={
        "jwt_header": "jwtHeader",
        "jwt_payload": "jwtPayload",
        "secret": "secret",
    },
)
class GoogleIntegrationsAuthConfigDecryptedCredentialJwt:
    def __init__(
        self,
        *,
        jwt_header: typing.Optional[builtins.str] = None,
        jwt_payload: typing.Optional[builtins.str] = None,
        secret: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param jwt_header: Identifies which algorithm is used to generate the signature. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#jwt_header GoogleIntegrationsAuthConfig#jwt_header}
        :param jwt_payload: Contains a set of claims. The JWT specification defines seven Registered Claim Names which are the standard fields commonly included in tokens. Custom claims are usually also included, depending on the purpose of the token. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#jwt_payload GoogleIntegrationsAuthConfig#jwt_payload}
        :param secret: User's pre-shared secret to sign the token. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#secret GoogleIntegrationsAuthConfig#secret}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef91bb89dab7c53f08647db495af9573774b2649d737b98bb1a16a979425ef47)
            check_type(argname="argument jwt_header", value=jwt_header, expected_type=type_hints["jwt_header"])
            check_type(argname="argument jwt_payload", value=jwt_payload, expected_type=type_hints["jwt_payload"])
            check_type(argname="argument secret", value=secret, expected_type=type_hints["secret"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if jwt_header is not None:
            self._values["jwt_header"] = jwt_header
        if jwt_payload is not None:
            self._values["jwt_payload"] = jwt_payload
        if secret is not None:
            self._values["secret"] = secret

    @builtins.property
    def jwt_header(self) -> typing.Optional[builtins.str]:
        '''Identifies which algorithm is used to generate the signature.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#jwt_header GoogleIntegrationsAuthConfig#jwt_header}
        '''
        result = self._values.get("jwt_header")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def jwt_payload(self) -> typing.Optional[builtins.str]:
        '''Contains a set of claims.

        The JWT specification defines seven Registered Claim Names which are the standard fields commonly included in tokens. Custom claims are usually also included, depending on the purpose of the token.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#jwt_payload GoogleIntegrationsAuthConfig#jwt_payload}
        '''
        result = self._values.get("jwt_payload")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret(self) -> typing.Optional[builtins.str]:
        '''User's pre-shared secret to sign the token.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#secret GoogleIntegrationsAuthConfig#secret}
        '''
        result = self._values.get("secret")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIntegrationsAuthConfigDecryptedCredentialJwt(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIntegrationsAuthConfigDecryptedCredentialJwtOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationsAuthConfig.GoogleIntegrationsAuthConfigDecryptedCredentialJwtOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__06f2c1a56b102cd8ce6820695f6f686c85a0768db2a00ec19576aae0e049eec5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetJwtHeader")
    def reset_jwt_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJwtHeader", []))

    @jsii.member(jsii_name="resetJwtPayload")
    def reset_jwt_payload(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJwtPayload", []))

    @jsii.member(jsii_name="resetSecret")
    def reset_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecret", []))

    @builtins.property
    @jsii.member(jsii_name="jwt")
    def jwt(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jwt"))

    @builtins.property
    @jsii.member(jsii_name="jwtHeaderInput")
    def jwt_header_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "jwtHeaderInput"))

    @builtins.property
    @jsii.member(jsii_name="jwtPayloadInput")
    def jwt_payload_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "jwtPayloadInput"))

    @builtins.property
    @jsii.member(jsii_name="secretInput")
    def secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretInput"))

    @builtins.property
    @jsii.member(jsii_name="jwtHeader")
    def jwt_header(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jwtHeader"))

    @jwt_header.setter
    def jwt_header(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__baaf4af9d928d9809cdbe054c9cc068da44be5d9b21c5015ec494a95430807dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jwtHeader", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jwtPayload")
    def jwt_payload(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jwtPayload"))

    @jwt_payload.setter
    def jwt_payload(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3831ebe34a31ea01b7a1ba66c4bfc4f54bf9b34b76d6836baaeb7483cb79f311)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jwtPayload", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secret")
    def secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secret"))

    @secret.setter
    def secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea91ed621d670975b05c56021bafcd7e620ff1441c5797854541cbee43d69f49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIntegrationsAuthConfigDecryptedCredentialJwt]:
        return typing.cast(typing.Optional[GoogleIntegrationsAuthConfigDecryptedCredentialJwt], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIntegrationsAuthConfigDecryptedCredentialJwt],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d40d55aabfde0bac477055fbeafc03770fb2daf9f4e94ac4088dfd670f86ee4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIntegrationsAuthConfig.GoogleIntegrationsAuthConfigDecryptedCredentialOauth2AuthorizationCode",
    jsii_struct_bases=[],
    name_mapping={
        "auth_endpoint": "authEndpoint",
        "client_id": "clientId",
        "client_secret": "clientSecret",
        "scope": "scope",
        "token_endpoint": "tokenEndpoint",
    },
)
class GoogleIntegrationsAuthConfigDecryptedCredentialOauth2AuthorizationCode:
    def __init__(
        self,
        *,
        auth_endpoint: typing.Optional[builtins.str] = None,
        client_id: typing.Optional[builtins.str] = None,
        client_secret: typing.Optional[builtins.str] = None,
        scope: typing.Optional[builtins.str] = None,
        token_endpoint: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param auth_endpoint: The auth url endpoint to send the auth code request to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#auth_endpoint GoogleIntegrationsAuthConfig#auth_endpoint}
        :param client_id: The client's id. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#client_id GoogleIntegrationsAuthConfig#client_id}
        :param client_secret: The client's secret. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#client_secret GoogleIntegrationsAuthConfig#client_secret}
        :param scope: A space-delimited list of requested scope permissions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#scope GoogleIntegrationsAuthConfig#scope}
        :param token_endpoint: The token url endpoint to send the token request to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#token_endpoint GoogleIntegrationsAuthConfig#token_endpoint}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f5ddff7e5fa52f1b180ecc44481b524d1291e8eb5fd46aac50a21060a257703)
            check_type(argname="argument auth_endpoint", value=auth_endpoint, expected_type=type_hints["auth_endpoint"])
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument token_endpoint", value=token_endpoint, expected_type=type_hints["token_endpoint"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auth_endpoint is not None:
            self._values["auth_endpoint"] = auth_endpoint
        if client_id is not None:
            self._values["client_id"] = client_id
        if client_secret is not None:
            self._values["client_secret"] = client_secret
        if scope is not None:
            self._values["scope"] = scope
        if token_endpoint is not None:
            self._values["token_endpoint"] = token_endpoint

    @builtins.property
    def auth_endpoint(self) -> typing.Optional[builtins.str]:
        '''The auth url endpoint to send the auth code request to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#auth_endpoint GoogleIntegrationsAuthConfig#auth_endpoint}
        '''
        result = self._values.get("auth_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_id(self) -> typing.Optional[builtins.str]:
        '''The client's id.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#client_id GoogleIntegrationsAuthConfig#client_id}
        '''
        result = self._values.get("client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_secret(self) -> typing.Optional[builtins.str]:
        '''The client's secret.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#client_secret GoogleIntegrationsAuthConfig#client_secret}
        '''
        result = self._values.get("client_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scope(self) -> typing.Optional[builtins.str]:
        '''A space-delimited list of requested scope permissions.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#scope GoogleIntegrationsAuthConfig#scope}
        '''
        result = self._values.get("scope")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token_endpoint(self) -> typing.Optional[builtins.str]:
        '''The token url endpoint to send the token request to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#token_endpoint GoogleIntegrationsAuthConfig#token_endpoint}
        '''
        result = self._values.get("token_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIntegrationsAuthConfigDecryptedCredentialOauth2AuthorizationCode(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIntegrationsAuthConfigDecryptedCredentialOauth2AuthorizationCodeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationsAuthConfig.GoogleIntegrationsAuthConfigDecryptedCredentialOauth2AuthorizationCodeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__97b51fb44a5df0962d153635b55440b4bdc0a27b101eaf0a057d026af6a7152c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAuthEndpoint")
    def reset_auth_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthEndpoint", []))

    @jsii.member(jsii_name="resetClientId")
    def reset_client_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientId", []))

    @jsii.member(jsii_name="resetClientSecret")
    def reset_client_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientSecret", []))

    @jsii.member(jsii_name="resetScope")
    def reset_scope(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScope", []))

    @jsii.member(jsii_name="resetTokenEndpoint")
    def reset_token_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTokenEndpoint", []))

    @builtins.property
    @jsii.member(jsii_name="authEndpointInput")
    def auth_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretInput")
    def client_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="scopeInput")
    def scope_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scopeInput"))

    @builtins.property
    @jsii.member(jsii_name="tokenEndpointInput")
    def token_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tokenEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="authEndpoint")
    def auth_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authEndpoint"))

    @auth_endpoint.setter
    def auth_endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33fdab18585a0773b13b2423503e5b43e5991741be0ea709098a5bbeee5b5eef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b3caaa1bd7c321c1047793dc53ead08777dde1dbbdfc6f705d118388722736c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecret"))

    @client_secret.setter
    def client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ec393dcbaff798dd64e075e82e3a3668e2ee10b7da356984dd0bc0e75645ec7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scope"))

    @scope.setter
    def scope(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0c9bc372474b2f783f2cfccee96a2eee7752e5e786e53736aaa171c742cba8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scope", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tokenEndpoint")
    def token_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tokenEndpoint"))

    @token_endpoint.setter
    def token_endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b6e594f2d32a5b487c85cc541ac2146889a765e2965a606875294a9e12887b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tokenEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIntegrationsAuthConfigDecryptedCredentialOauth2AuthorizationCode]:
        return typing.cast(typing.Optional[GoogleIntegrationsAuthConfigDecryptedCredentialOauth2AuthorizationCode], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIntegrationsAuthConfigDecryptedCredentialOauth2AuthorizationCode],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6af11264c679af7629801a053b4c54e769df355720c0c0aa352a693cf0bdd575)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIntegrationsAuthConfig.GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentials",
    jsii_struct_bases=[],
    name_mapping={
        "client_id": "clientId",
        "client_secret": "clientSecret",
        "request_type": "requestType",
        "scope": "scope",
        "token_endpoint": "tokenEndpoint",
        "token_params": "tokenParams",
    },
)
class GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentials:
    def __init__(
        self,
        *,
        client_id: typing.Optional[builtins.str] = None,
        client_secret: typing.Optional[builtins.str] = None,
        request_type: typing.Optional[builtins.str] = None,
        scope: typing.Optional[builtins.str] = None,
        token_endpoint: typing.Optional[builtins.str] = None,
        token_params: typing.Optional[typing.Union["GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParams", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param client_id: The client's ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#client_id GoogleIntegrationsAuthConfig#client_id}
        :param client_secret: The client's secret. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#client_secret GoogleIntegrationsAuthConfig#client_secret}
        :param request_type: Represent how to pass parameters to fetch access token Possible values: ["REQUEST_TYPE_UNSPECIFIED", "REQUEST_BODY", "QUERY_PARAMETERS", "ENCODED_HEADER"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#request_type GoogleIntegrationsAuthConfig#request_type}
        :param scope: A space-delimited list of requested scope permissions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#scope GoogleIntegrationsAuthConfig#scope}
        :param token_endpoint: The token endpoint is used by the client to obtain an access token by presenting its authorization grant or refresh token. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#token_endpoint GoogleIntegrationsAuthConfig#token_endpoint}
        :param token_params: token_params block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#token_params GoogleIntegrationsAuthConfig#token_params}
        '''
        if isinstance(token_params, dict):
            token_params = GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParams(**token_params)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30797a6bdd4bf7253f973bc13c7ee451bbdb036467e8f4b2f46de5efb8fded84)
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
            check_type(argname="argument request_type", value=request_type, expected_type=type_hints["request_type"])
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument token_endpoint", value=token_endpoint, expected_type=type_hints["token_endpoint"])
            check_type(argname="argument token_params", value=token_params, expected_type=type_hints["token_params"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if client_id is not None:
            self._values["client_id"] = client_id
        if client_secret is not None:
            self._values["client_secret"] = client_secret
        if request_type is not None:
            self._values["request_type"] = request_type
        if scope is not None:
            self._values["scope"] = scope
        if token_endpoint is not None:
            self._values["token_endpoint"] = token_endpoint
        if token_params is not None:
            self._values["token_params"] = token_params

    @builtins.property
    def client_id(self) -> typing.Optional[builtins.str]:
        '''The client's ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#client_id GoogleIntegrationsAuthConfig#client_id}
        '''
        result = self._values.get("client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_secret(self) -> typing.Optional[builtins.str]:
        '''The client's secret.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#client_secret GoogleIntegrationsAuthConfig#client_secret}
        '''
        result = self._values.get("client_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def request_type(self) -> typing.Optional[builtins.str]:
        '''Represent how to pass parameters to fetch access token Possible values: ["REQUEST_TYPE_UNSPECIFIED", "REQUEST_BODY", "QUERY_PARAMETERS", "ENCODED_HEADER"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#request_type GoogleIntegrationsAuthConfig#request_type}
        '''
        result = self._values.get("request_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scope(self) -> typing.Optional[builtins.str]:
        '''A space-delimited list of requested scope permissions.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#scope GoogleIntegrationsAuthConfig#scope}
        '''
        result = self._values.get("scope")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token_endpoint(self) -> typing.Optional[builtins.str]:
        '''The token endpoint is used by the client to obtain an access token by presenting its authorization grant or refresh token.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#token_endpoint GoogleIntegrationsAuthConfig#token_endpoint}
        '''
        result = self._values.get("token_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token_params(
        self,
    ) -> typing.Optional["GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParams"]:
        '''token_params block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#token_params GoogleIntegrationsAuthConfig#token_params}
        '''
        result = self._values.get("token_params")
        return typing.cast(typing.Optional["GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParams"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentials(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationsAuthConfig.GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__46b3a7d8b833126f69024cd6036aa8da375ffad6375ce5f9a665a5e312da03c6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putTokenParams")
    def put_token_params(
        self,
        *,
        entries: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntries", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param entries: entries block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#entries GoogleIntegrationsAuthConfig#entries}
        '''
        value = GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParams(
            entries=entries
        )

        return typing.cast(None, jsii.invoke(self, "putTokenParams", [value]))

    @jsii.member(jsii_name="resetClientId")
    def reset_client_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientId", []))

    @jsii.member(jsii_name="resetClientSecret")
    def reset_client_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientSecret", []))

    @jsii.member(jsii_name="resetRequestType")
    def reset_request_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestType", []))

    @jsii.member(jsii_name="resetScope")
    def reset_scope(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScope", []))

    @jsii.member(jsii_name="resetTokenEndpoint")
    def reset_token_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTokenEndpoint", []))

    @jsii.member(jsii_name="resetTokenParams")
    def reset_token_params(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTokenParams", []))

    @builtins.property
    @jsii.member(jsii_name="tokenParams")
    def token_params(
        self,
    ) -> "GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsOutputReference":
        return typing.cast("GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsOutputReference", jsii.get(self, "tokenParams"))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretInput")
    def client_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="requestTypeInput")
    def request_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "requestTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="scopeInput")
    def scope_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scopeInput"))

    @builtins.property
    @jsii.member(jsii_name="tokenEndpointInput")
    def token_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tokenEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="tokenParamsInput")
    def token_params_input(
        self,
    ) -> typing.Optional["GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParams"]:
        return typing.cast(typing.Optional["GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParams"], jsii.get(self, "tokenParamsInput"))

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3534691547b63529343556842c85b730830393992b36be355ee36bef6cb3d78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecret"))

    @client_secret.setter
    def client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d13eb92a7f3220d7bd081fe3e870ddbf08eff6bb7b905b58f711915be500de2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requestType")
    def request_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "requestType"))

    @request_type.setter
    def request_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b6184549141a36c4a8405fb37b7ea090de9e7749c4792ca599abe35eeb8711d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scope"))

    @scope.setter
    def scope(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d772bb032ba2981dba40edc17b9482eaada28853075197e22db7de4a5d6bb840)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scope", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tokenEndpoint")
    def token_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tokenEndpoint"))

    @token_endpoint.setter
    def token_endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddcacc24536d2924f895c3f9e23cca3ea779bcfb2fceb7e5804bd68ce43462b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tokenEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentials]:
        return typing.cast(typing.Optional[GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentials], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentials],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5b695f78ddb802a23a0ad4ca19bde41c3710615bd0ccacff960d0d88ab5b8c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIntegrationsAuthConfig.GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParams",
    jsii_struct_bases=[],
    name_mapping={"entries": "entries"},
)
class GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParams:
    def __init__(
        self,
        *,
        entries: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntries", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param entries: entries block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#entries GoogleIntegrationsAuthConfig#entries}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6ac4b047aa7152163364acd54310bec551a569b0f16bcd14d3d89b6d73fdb98)
            check_type(argname="argument entries", value=entries, expected_type=type_hints["entries"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if entries is not None:
            self._values["entries"] = entries

    @builtins.property
    def entries(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntries"]]]:
        '''entries block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#entries GoogleIntegrationsAuthConfig#entries}
        '''
        result = self._values.get("entries")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntries"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParams(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIntegrationsAuthConfig.GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntries",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntries:
    def __init__(
        self,
        *,
        key: typing.Optional[typing.Union["GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKey", typing.Dict[builtins.str, typing.Any]]] = None,
        value: typing.Optional[typing.Union["GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValue", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param key: key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#key GoogleIntegrationsAuthConfig#key}
        :param value: value block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#value GoogleIntegrationsAuthConfig#value}
        '''
        if isinstance(key, dict):
            key = GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKey(**key)
        if isinstance(value, dict):
            value = GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValue(**value)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0f969b322f49d833740c55314ab654ad39a9b1a1a0dbfec445fb61ac8ab006e)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if key is not None:
            self._values["key"] = key
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def key(
        self,
    ) -> typing.Optional["GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKey"]:
        '''key block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#key GoogleIntegrationsAuthConfig#key}
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional["GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKey"], result)

    @builtins.property
    def value(
        self,
    ) -> typing.Optional["GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValue"]:
        '''value block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#value GoogleIntegrationsAuthConfig#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional["GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValue"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntries(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIntegrationsAuthConfig.GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKey",
    jsii_struct_bases=[],
    name_mapping={"literal_value": "literalValue"},
)
class GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKey:
    def __init__(
        self,
        *,
        literal_value: typing.Optional[typing.Union["GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKeyLiteralValue", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param literal_value: literal_value block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#literal_value GoogleIntegrationsAuthConfig#literal_value}
        '''
        if isinstance(literal_value, dict):
            literal_value = GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKeyLiteralValue(**literal_value)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b4ac980fed1b1abebd9cb3d60d3a79aa8c646b07e5d8be1779869fbb7b1dc6a)
            check_type(argname="argument literal_value", value=literal_value, expected_type=type_hints["literal_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if literal_value is not None:
            self._values["literal_value"] = literal_value

    @builtins.property
    def literal_value(
        self,
    ) -> typing.Optional["GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKeyLiteralValue"]:
        '''literal_value block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#literal_value GoogleIntegrationsAuthConfig#literal_value}
        '''
        result = self._values.get("literal_value")
        return typing.cast(typing.Optional["GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKeyLiteralValue"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIntegrationsAuthConfig.GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKeyLiteralValue",
    jsii_struct_bases=[],
    name_mapping={"string_value": "stringValue"},
)
class GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKeyLiteralValue:
    def __init__(self, *, string_value: typing.Optional[builtins.str] = None) -> None:
        '''
        :param string_value: String. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#string_value GoogleIntegrationsAuthConfig#string_value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b36e84cf3ca4cfe50a8ddecd69d0b561cdca2abf866683c4e1c3d73e0fe01aff)
            check_type(argname="argument string_value", value=string_value, expected_type=type_hints["string_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if string_value is not None:
            self._values["string_value"] = string_value

    @builtins.property
    def string_value(self) -> typing.Optional[builtins.str]:
        '''String.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#string_value GoogleIntegrationsAuthConfig#string_value}
        '''
        result = self._values.get("string_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKeyLiteralValue(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKeyLiteralValueOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationsAuthConfig.GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKeyLiteralValueOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8a935ed6e8df532dc1bcd3ae7856e3d6af595eb9984df95c4cab3f758c6260a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetStringValue")
    def reset_string_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStringValue", []))

    @builtins.property
    @jsii.member(jsii_name="stringValueInput")
    def string_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stringValueInput"))

    @builtins.property
    @jsii.member(jsii_name="stringValue")
    def string_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stringValue"))

    @string_value.setter
    def string_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4310c88c7831b92e24d40253ebd260d8597429f9a3902a53a554437c18896c80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stringValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKeyLiteralValue]:
        return typing.cast(typing.Optional[GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKeyLiteralValue], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKeyLiteralValue],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b51f8bea57680c316513dc6d3d246a51b9fb710f92af88cf6d88aa68b790d444)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationsAuthConfig.GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f3c660e57d99a3e2ccfcf6bcdd342cd32b4f3eec5fddb9291609157477abf552)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLiteralValue")
    def put_literal_value(
        self,
        *,
        string_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param string_value: String. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#string_value GoogleIntegrationsAuthConfig#string_value}
        '''
        value = GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKeyLiteralValue(
            string_value=string_value
        )

        return typing.cast(None, jsii.invoke(self, "putLiteralValue", [value]))

    @jsii.member(jsii_name="resetLiteralValue")
    def reset_literal_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLiteralValue", []))

    @builtins.property
    @jsii.member(jsii_name="literalValue")
    def literal_value(
        self,
    ) -> GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKeyLiteralValueOutputReference:
        return typing.cast(GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKeyLiteralValueOutputReference, jsii.get(self, "literalValue"))

    @builtins.property
    @jsii.member(jsii_name="literalValueInput")
    def literal_value_input(
        self,
    ) -> typing.Optional[GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKeyLiteralValue]:
        return typing.cast(typing.Optional[GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKeyLiteralValue], jsii.get(self, "literalValueInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKey]:
        return typing.cast(typing.Optional[GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKey], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKey],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2860b41386298ab6485fd90b53f7f8d709a58119bada3936cb1064610469c83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationsAuthConfig.GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aaee4ab1296b6e8710b96403ebc31b9a2d5ba79af1c685624f0c76c2241b2cdd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bc1bcc5f7ca38e406924e4b1673768a39a2b4a3ba042ad4df0cce47a7e331fb)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2e1f8227bed593ea1a8c05f267e90044b404f1a7e144a7857a2c8edc5fcb311)
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
            type_hints = typing.get_type_hints(_typecheckingstub__743ded25321264f822185d10737f1512bf13ad16a7a51ab7a2a78e0503f4dcf1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__db6c0847a8ec7069fba30cdae8d433723b6adbb9ad54d7f07160819419422941)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntries]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntries]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntries]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e61a46341b6146d85d6c01b9f202711467d1b0c07df9697fc3db93cd5f9d2aa8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationsAuthConfig.GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__62ced7d2f705a706c18b2ad709d267c2d2b34e56d1d1b41e5358336c5d78b243)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putKey")
    def put_key(
        self,
        *,
        literal_value: typing.Optional[typing.Union[GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKeyLiteralValue, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param literal_value: literal_value block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#literal_value GoogleIntegrationsAuthConfig#literal_value}
        '''
        value = GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKey(
            literal_value=literal_value
        )

        return typing.cast(None, jsii.invoke(self, "putKey", [value]))

    @jsii.member(jsii_name="putValue")
    def put_value(
        self,
        *,
        literal_value: typing.Optional[typing.Union["GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValueLiteralValue", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param literal_value: literal_value block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#literal_value GoogleIntegrationsAuthConfig#literal_value}
        '''
        value = GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValue(
            literal_value=literal_value
        )

        return typing.cast(None, jsii.invoke(self, "putValue", [value]))

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(
        self,
    ) -> GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKeyOutputReference:
        return typing.cast(GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKeyOutputReference, jsii.get(self, "key"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(
        self,
    ) -> "GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValueOutputReference":
        return typing.cast("GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValueOutputReference", jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(
        self,
    ) -> typing.Optional[GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKey]:
        return typing.cast(typing.Optional[GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKey], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(
        self,
    ) -> typing.Optional["GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValue"]:
        return typing.cast(typing.Optional["GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValue"], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntries]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntries]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntries]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42662ce7476ae53ac3b9baf5a4ee2569117d7ab88fae127c24b792b40040db93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIntegrationsAuthConfig.GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValue",
    jsii_struct_bases=[],
    name_mapping={"literal_value": "literalValue"},
)
class GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValue:
    def __init__(
        self,
        *,
        literal_value: typing.Optional[typing.Union["GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValueLiteralValue", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param literal_value: literal_value block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#literal_value GoogleIntegrationsAuthConfig#literal_value}
        '''
        if isinstance(literal_value, dict):
            literal_value = GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValueLiteralValue(**literal_value)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a37ad2bef70c0e3a9b5751d7b9050f9c0f1f3abfd2475c7863b5e2ec80e3252)
            check_type(argname="argument literal_value", value=literal_value, expected_type=type_hints["literal_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if literal_value is not None:
            self._values["literal_value"] = literal_value

    @builtins.property
    def literal_value(
        self,
    ) -> typing.Optional["GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValueLiteralValue"]:
        '''literal_value block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#literal_value GoogleIntegrationsAuthConfig#literal_value}
        '''
        result = self._values.get("literal_value")
        return typing.cast(typing.Optional["GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValueLiteralValue"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValue(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIntegrationsAuthConfig.GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValueLiteralValue",
    jsii_struct_bases=[],
    name_mapping={"string_value": "stringValue"},
)
class GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValueLiteralValue:
    def __init__(self, *, string_value: typing.Optional[builtins.str] = None) -> None:
        '''
        :param string_value: String. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#string_value GoogleIntegrationsAuthConfig#string_value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8731c5f245ce26c742d46cf31b190a90fc615d958b1069049342aaf5ef0dd98)
            check_type(argname="argument string_value", value=string_value, expected_type=type_hints["string_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if string_value is not None:
            self._values["string_value"] = string_value

    @builtins.property
    def string_value(self) -> typing.Optional[builtins.str]:
        '''String.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#string_value GoogleIntegrationsAuthConfig#string_value}
        '''
        result = self._values.get("string_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValueLiteralValue(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValueLiteralValueOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationsAuthConfig.GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValueLiteralValueOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6aead4a4ca58793c3b47219d381a49d397e6f4d67d8fdf748511594c0e137f40)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetStringValue")
    def reset_string_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStringValue", []))

    @builtins.property
    @jsii.member(jsii_name="stringValueInput")
    def string_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stringValueInput"))

    @builtins.property
    @jsii.member(jsii_name="stringValue")
    def string_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stringValue"))

    @string_value.setter
    def string_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9b89b6f5d9de8cbdcf2c6d68a8c8c93d69c565a5f604a2d25d6a434c63cba99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stringValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValueLiteralValue]:
        return typing.cast(typing.Optional[GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValueLiteralValue], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValueLiteralValue],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6f8802c42a03e7b9a8eb80f5846406c5769062ffc567c253ab6c23b64a3ca85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValueOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationsAuthConfig.GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValueOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c428141dcf8f19dc1c2468a100eb34c9c451bd6cdcfd513db64025635b8ca1c5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLiteralValue")
    def put_literal_value(
        self,
        *,
        string_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param string_value: String. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#string_value GoogleIntegrationsAuthConfig#string_value}
        '''
        value = GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValueLiteralValue(
            string_value=string_value
        )

        return typing.cast(None, jsii.invoke(self, "putLiteralValue", [value]))

    @jsii.member(jsii_name="resetLiteralValue")
    def reset_literal_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLiteralValue", []))

    @builtins.property
    @jsii.member(jsii_name="literalValue")
    def literal_value(
        self,
    ) -> GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValueLiteralValueOutputReference:
        return typing.cast(GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValueLiteralValueOutputReference, jsii.get(self, "literalValue"))

    @builtins.property
    @jsii.member(jsii_name="literalValueInput")
    def literal_value_input(
        self,
    ) -> typing.Optional[GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValueLiteralValue]:
        return typing.cast(typing.Optional[GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValueLiteralValue], jsii.get(self, "literalValueInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValue]:
        return typing.cast(typing.Optional[GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValue], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValue],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__347e98a8dde3d5eb03935ff0fc00de8cdc0b5261e894a27b102e1e865358f8da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationsAuthConfig.GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__74a7f5afc620e1be8d1e526babb7f3129250a9c333aeed1c5826a63402b3b04f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putEntries")
    def put_entries(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntries, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f87aedc5f5e9e395c091d1cb34c4cac633d47a88ca04939f8bc84eac8136e7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEntries", [value]))

    @jsii.member(jsii_name="resetEntries")
    def reset_entries(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEntries", []))

    @builtins.property
    @jsii.member(jsii_name="entries")
    def entries(
        self,
    ) -> GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesList:
        return typing.cast(GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesList, jsii.get(self, "entries"))

    @builtins.property
    @jsii.member(jsii_name="entriesInput")
    def entries_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntries]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntries]]], jsii.get(self, "entriesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParams]:
        return typing.cast(typing.Optional[GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParams], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParams],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5118a4b25a0bddeb36a9d0c637084a2b9df42bb59a84749f27212e89817252eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIntegrationsAuthConfig.GoogleIntegrationsAuthConfigDecryptedCredentialOidcToken",
    jsii_struct_bases=[],
    name_mapping={
        "audience": "audience",
        "service_account_email": "serviceAccountEmail",
    },
)
class GoogleIntegrationsAuthConfigDecryptedCredentialOidcToken:
    def __init__(
        self,
        *,
        audience: typing.Optional[builtins.str] = None,
        service_account_email: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param audience: Audience to be used when generating OIDC token. The audience claim identifies the recipients that the JWT is intended for. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#audience GoogleIntegrationsAuthConfig#audience}
        :param service_account_email: The service account email to be used as the identity for the token. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#service_account_email GoogleIntegrationsAuthConfig#service_account_email}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87abe8c28ba09bc4a8ed647992bdfaff12d7b4efe255d2d0751ca4e8726249dc)
            check_type(argname="argument audience", value=audience, expected_type=type_hints["audience"])
            check_type(argname="argument service_account_email", value=service_account_email, expected_type=type_hints["service_account_email"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if audience is not None:
            self._values["audience"] = audience
        if service_account_email is not None:
            self._values["service_account_email"] = service_account_email

    @builtins.property
    def audience(self) -> typing.Optional[builtins.str]:
        '''Audience to be used when generating OIDC token.

        The audience claim identifies the recipients that the JWT is intended for.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#audience GoogleIntegrationsAuthConfig#audience}
        '''
        result = self._values.get("audience")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_account_email(self) -> typing.Optional[builtins.str]:
        '''The service account email to be used as the identity for the token.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#service_account_email GoogleIntegrationsAuthConfig#service_account_email}
        '''
        result = self._values.get("service_account_email")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIntegrationsAuthConfigDecryptedCredentialOidcToken(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIntegrationsAuthConfigDecryptedCredentialOidcTokenOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationsAuthConfig.GoogleIntegrationsAuthConfigDecryptedCredentialOidcTokenOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__deadc70ef6b3a1235d0c17a04bab1d323ceb20dc78ebcbf6b1c6c2c8afc64139)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAudience")
    def reset_audience(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAudience", []))

    @jsii.member(jsii_name="resetServiceAccountEmail")
    def reset_service_account_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceAccountEmail", []))

    @builtins.property
    @jsii.member(jsii_name="token")
    def token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "token"))

    @builtins.property
    @jsii.member(jsii_name="tokenExpireTime")
    def token_expire_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tokenExpireTime"))

    @builtins.property
    @jsii.member(jsii_name="audienceInput")
    def audience_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "audienceInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountEmailInput")
    def service_account_email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAccountEmailInput"))

    @builtins.property
    @jsii.member(jsii_name="audience")
    def audience(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "audience"))

    @audience.setter
    def audience(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f961759938a50627cf14f041578689228fa0ce5d87d771b39cc32c6ce2a0d383)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "audience", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccountEmail")
    def service_account_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccountEmail"))

    @service_account_email.setter
    def service_account_email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be3401f346e3667b0a5f1c09f0496644a76e1073aa502693937f2348cbb4e0b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccountEmail", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIntegrationsAuthConfigDecryptedCredentialOidcToken]:
        return typing.cast(typing.Optional[GoogleIntegrationsAuthConfigDecryptedCredentialOidcToken], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIntegrationsAuthConfigDecryptedCredentialOidcToken],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e22827942fcb565e755e336f702afc96b8221d0a20989541606994e7ffcae89b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleIntegrationsAuthConfigDecryptedCredentialOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationsAuthConfig.GoogleIntegrationsAuthConfigDecryptedCredentialOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3ef9cfcd7869587f62509a2aaefe3f0018f6f3a4f0bf449c8b92d331710e8b6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAuthToken")
    def put_auth_token(
        self,
        *,
        token: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param token: The token for the auth type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#token GoogleIntegrationsAuthConfig#token}
        :param type: Authentication type, e.g. "Basic", "Bearer", etc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#type GoogleIntegrationsAuthConfig#type}
        '''
        value = GoogleIntegrationsAuthConfigDecryptedCredentialAuthToken(
            token=token, type=type
        )

        return typing.cast(None, jsii.invoke(self, "putAuthToken", [value]))

    @jsii.member(jsii_name="putJwt")
    def put_jwt(
        self,
        *,
        jwt_header: typing.Optional[builtins.str] = None,
        jwt_payload: typing.Optional[builtins.str] = None,
        secret: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param jwt_header: Identifies which algorithm is used to generate the signature. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#jwt_header GoogleIntegrationsAuthConfig#jwt_header}
        :param jwt_payload: Contains a set of claims. The JWT specification defines seven Registered Claim Names which are the standard fields commonly included in tokens. Custom claims are usually also included, depending on the purpose of the token. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#jwt_payload GoogleIntegrationsAuthConfig#jwt_payload}
        :param secret: User's pre-shared secret to sign the token. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#secret GoogleIntegrationsAuthConfig#secret}
        '''
        value = GoogleIntegrationsAuthConfigDecryptedCredentialJwt(
            jwt_header=jwt_header, jwt_payload=jwt_payload, secret=secret
        )

        return typing.cast(None, jsii.invoke(self, "putJwt", [value]))

    @jsii.member(jsii_name="putOauth2AuthorizationCode")
    def put_oauth2_authorization_code(
        self,
        *,
        auth_endpoint: typing.Optional[builtins.str] = None,
        client_id: typing.Optional[builtins.str] = None,
        client_secret: typing.Optional[builtins.str] = None,
        scope: typing.Optional[builtins.str] = None,
        token_endpoint: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param auth_endpoint: The auth url endpoint to send the auth code request to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#auth_endpoint GoogleIntegrationsAuthConfig#auth_endpoint}
        :param client_id: The client's id. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#client_id GoogleIntegrationsAuthConfig#client_id}
        :param client_secret: The client's secret. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#client_secret GoogleIntegrationsAuthConfig#client_secret}
        :param scope: A space-delimited list of requested scope permissions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#scope GoogleIntegrationsAuthConfig#scope}
        :param token_endpoint: The token url endpoint to send the token request to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#token_endpoint GoogleIntegrationsAuthConfig#token_endpoint}
        '''
        value = GoogleIntegrationsAuthConfigDecryptedCredentialOauth2AuthorizationCode(
            auth_endpoint=auth_endpoint,
            client_id=client_id,
            client_secret=client_secret,
            scope=scope,
            token_endpoint=token_endpoint,
        )

        return typing.cast(None, jsii.invoke(self, "putOauth2AuthorizationCode", [value]))

    @jsii.member(jsii_name="putOauth2ClientCredentials")
    def put_oauth2_client_credentials(
        self,
        *,
        client_id: typing.Optional[builtins.str] = None,
        client_secret: typing.Optional[builtins.str] = None,
        request_type: typing.Optional[builtins.str] = None,
        scope: typing.Optional[builtins.str] = None,
        token_endpoint: typing.Optional[builtins.str] = None,
        token_params: typing.Optional[typing.Union[GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParams, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param client_id: The client's ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#client_id GoogleIntegrationsAuthConfig#client_id}
        :param client_secret: The client's secret. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#client_secret GoogleIntegrationsAuthConfig#client_secret}
        :param request_type: Represent how to pass parameters to fetch access token Possible values: ["REQUEST_TYPE_UNSPECIFIED", "REQUEST_BODY", "QUERY_PARAMETERS", "ENCODED_HEADER"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#request_type GoogleIntegrationsAuthConfig#request_type}
        :param scope: A space-delimited list of requested scope permissions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#scope GoogleIntegrationsAuthConfig#scope}
        :param token_endpoint: The token endpoint is used by the client to obtain an access token by presenting its authorization grant or refresh token. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#token_endpoint GoogleIntegrationsAuthConfig#token_endpoint}
        :param token_params: token_params block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#token_params GoogleIntegrationsAuthConfig#token_params}
        '''
        value = GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentials(
            client_id=client_id,
            client_secret=client_secret,
            request_type=request_type,
            scope=scope,
            token_endpoint=token_endpoint,
            token_params=token_params,
        )

        return typing.cast(None, jsii.invoke(self, "putOauth2ClientCredentials", [value]))

    @jsii.member(jsii_name="putOidcToken")
    def put_oidc_token(
        self,
        *,
        audience: typing.Optional[builtins.str] = None,
        service_account_email: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param audience: Audience to be used when generating OIDC token. The audience claim identifies the recipients that the JWT is intended for. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#audience GoogleIntegrationsAuthConfig#audience}
        :param service_account_email: The service account email to be used as the identity for the token. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#service_account_email GoogleIntegrationsAuthConfig#service_account_email}
        '''
        value = GoogleIntegrationsAuthConfigDecryptedCredentialOidcToken(
            audience=audience, service_account_email=service_account_email
        )

        return typing.cast(None, jsii.invoke(self, "putOidcToken", [value]))

    @jsii.member(jsii_name="putServiceAccountCredentials")
    def put_service_account_credentials(
        self,
        *,
        scope: typing.Optional[builtins.str] = None,
        service_account: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: A space-delimited list of requested scope permissions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#scope GoogleIntegrationsAuthConfig#scope}
        :param service_account: Name of the service account that has the permission to make the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#service_account GoogleIntegrationsAuthConfig#service_account}
        '''
        value = GoogleIntegrationsAuthConfigDecryptedCredentialServiceAccountCredentials(
            scope=scope, service_account=service_account
        )

        return typing.cast(None, jsii.invoke(self, "putServiceAccountCredentials", [value]))

    @jsii.member(jsii_name="putUsernameAndPassword")
    def put_username_and_password(
        self,
        *,
        password: typing.Optional[builtins.str] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param password: Password to be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#password GoogleIntegrationsAuthConfig#password}
        :param username: Username to be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#username GoogleIntegrationsAuthConfig#username}
        '''
        value = GoogleIntegrationsAuthConfigDecryptedCredentialUsernameAndPassword(
            password=password, username=username
        )

        return typing.cast(None, jsii.invoke(self, "putUsernameAndPassword", [value]))

    @jsii.member(jsii_name="resetAuthToken")
    def reset_auth_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthToken", []))

    @jsii.member(jsii_name="resetJwt")
    def reset_jwt(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJwt", []))

    @jsii.member(jsii_name="resetOauth2AuthorizationCode")
    def reset_oauth2_authorization_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauth2AuthorizationCode", []))

    @jsii.member(jsii_name="resetOauth2ClientCredentials")
    def reset_oauth2_client_credentials(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauth2ClientCredentials", []))

    @jsii.member(jsii_name="resetOidcToken")
    def reset_oidc_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOidcToken", []))

    @jsii.member(jsii_name="resetServiceAccountCredentials")
    def reset_service_account_credentials(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceAccountCredentials", []))

    @jsii.member(jsii_name="resetUsernameAndPassword")
    def reset_username_and_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsernameAndPassword", []))

    @builtins.property
    @jsii.member(jsii_name="authToken")
    def auth_token(
        self,
    ) -> GoogleIntegrationsAuthConfigDecryptedCredentialAuthTokenOutputReference:
        return typing.cast(GoogleIntegrationsAuthConfigDecryptedCredentialAuthTokenOutputReference, jsii.get(self, "authToken"))

    @builtins.property
    @jsii.member(jsii_name="jwt")
    def jwt(self) -> GoogleIntegrationsAuthConfigDecryptedCredentialJwtOutputReference:
        return typing.cast(GoogleIntegrationsAuthConfigDecryptedCredentialJwtOutputReference, jsii.get(self, "jwt"))

    @builtins.property
    @jsii.member(jsii_name="oauth2AuthorizationCode")
    def oauth2_authorization_code(
        self,
    ) -> GoogleIntegrationsAuthConfigDecryptedCredentialOauth2AuthorizationCodeOutputReference:
        return typing.cast(GoogleIntegrationsAuthConfigDecryptedCredentialOauth2AuthorizationCodeOutputReference, jsii.get(self, "oauth2AuthorizationCode"))

    @builtins.property
    @jsii.member(jsii_name="oauth2ClientCredentials")
    def oauth2_client_credentials(
        self,
    ) -> GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsOutputReference:
        return typing.cast(GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsOutputReference, jsii.get(self, "oauth2ClientCredentials"))

    @builtins.property
    @jsii.member(jsii_name="oidcToken")
    def oidc_token(
        self,
    ) -> GoogleIntegrationsAuthConfigDecryptedCredentialOidcTokenOutputReference:
        return typing.cast(GoogleIntegrationsAuthConfigDecryptedCredentialOidcTokenOutputReference, jsii.get(self, "oidcToken"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountCredentials")
    def service_account_credentials(
        self,
    ) -> "GoogleIntegrationsAuthConfigDecryptedCredentialServiceAccountCredentialsOutputReference":
        return typing.cast("GoogleIntegrationsAuthConfigDecryptedCredentialServiceAccountCredentialsOutputReference", jsii.get(self, "serviceAccountCredentials"))

    @builtins.property
    @jsii.member(jsii_name="usernameAndPassword")
    def username_and_password(
        self,
    ) -> "GoogleIntegrationsAuthConfigDecryptedCredentialUsernameAndPasswordOutputReference":
        return typing.cast("GoogleIntegrationsAuthConfigDecryptedCredentialUsernameAndPasswordOutputReference", jsii.get(self, "usernameAndPassword"))

    @builtins.property
    @jsii.member(jsii_name="authTokenInput")
    def auth_token_input(
        self,
    ) -> typing.Optional[GoogleIntegrationsAuthConfigDecryptedCredentialAuthToken]:
        return typing.cast(typing.Optional[GoogleIntegrationsAuthConfigDecryptedCredentialAuthToken], jsii.get(self, "authTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="credentialTypeInput")
    def credential_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "credentialTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="jwtInput")
    def jwt_input(
        self,
    ) -> typing.Optional[GoogleIntegrationsAuthConfigDecryptedCredentialJwt]:
        return typing.cast(typing.Optional[GoogleIntegrationsAuthConfigDecryptedCredentialJwt], jsii.get(self, "jwtInput"))

    @builtins.property
    @jsii.member(jsii_name="oauth2AuthorizationCodeInput")
    def oauth2_authorization_code_input(
        self,
    ) -> typing.Optional[GoogleIntegrationsAuthConfigDecryptedCredentialOauth2AuthorizationCode]:
        return typing.cast(typing.Optional[GoogleIntegrationsAuthConfigDecryptedCredentialOauth2AuthorizationCode], jsii.get(self, "oauth2AuthorizationCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="oauth2ClientCredentialsInput")
    def oauth2_client_credentials_input(
        self,
    ) -> typing.Optional[GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentials]:
        return typing.cast(typing.Optional[GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentials], jsii.get(self, "oauth2ClientCredentialsInput"))

    @builtins.property
    @jsii.member(jsii_name="oidcTokenInput")
    def oidc_token_input(
        self,
    ) -> typing.Optional[GoogleIntegrationsAuthConfigDecryptedCredentialOidcToken]:
        return typing.cast(typing.Optional[GoogleIntegrationsAuthConfigDecryptedCredentialOidcToken], jsii.get(self, "oidcTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountCredentialsInput")
    def service_account_credentials_input(
        self,
    ) -> typing.Optional["GoogleIntegrationsAuthConfigDecryptedCredentialServiceAccountCredentials"]:
        return typing.cast(typing.Optional["GoogleIntegrationsAuthConfigDecryptedCredentialServiceAccountCredentials"], jsii.get(self, "serviceAccountCredentialsInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameAndPasswordInput")
    def username_and_password_input(
        self,
    ) -> typing.Optional["GoogleIntegrationsAuthConfigDecryptedCredentialUsernameAndPassword"]:
        return typing.cast(typing.Optional["GoogleIntegrationsAuthConfigDecryptedCredentialUsernameAndPassword"], jsii.get(self, "usernameAndPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="credentialType")
    def credential_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "credentialType"))

    @credential_type.setter
    def credential_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63f987ef32e94cca040ac4816b07ec1d4da1c07d553b885aae14ab54e4fb96a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "credentialType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIntegrationsAuthConfigDecryptedCredential]:
        return typing.cast(typing.Optional[GoogleIntegrationsAuthConfigDecryptedCredential], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIntegrationsAuthConfigDecryptedCredential],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3892322fe456afb8ad198edcdfc68357f66f3400a95543ece9889e27fc05d251)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIntegrationsAuthConfig.GoogleIntegrationsAuthConfigDecryptedCredentialServiceAccountCredentials",
    jsii_struct_bases=[],
    name_mapping={"scope": "scope", "service_account": "serviceAccount"},
)
class GoogleIntegrationsAuthConfigDecryptedCredentialServiceAccountCredentials:
    def __init__(
        self,
        *,
        scope: typing.Optional[builtins.str] = None,
        service_account: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: A space-delimited list of requested scope permissions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#scope GoogleIntegrationsAuthConfig#scope}
        :param service_account: Name of the service account that has the permission to make the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#service_account GoogleIntegrationsAuthConfig#service_account}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__397067c075e1b17e68d2d667d7dde60ee85754009255578d2156db8be4f67265)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument service_account", value=service_account, expected_type=type_hints["service_account"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if scope is not None:
            self._values["scope"] = scope
        if service_account is not None:
            self._values["service_account"] = service_account

    @builtins.property
    def scope(self) -> typing.Optional[builtins.str]:
        '''A space-delimited list of requested scope permissions.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#scope GoogleIntegrationsAuthConfig#scope}
        '''
        result = self._values.get("scope")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_account(self) -> typing.Optional[builtins.str]:
        '''Name of the service account that has the permission to make the request.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#service_account GoogleIntegrationsAuthConfig#service_account}
        '''
        result = self._values.get("service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIntegrationsAuthConfigDecryptedCredentialServiceAccountCredentials(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIntegrationsAuthConfigDecryptedCredentialServiceAccountCredentialsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationsAuthConfig.GoogleIntegrationsAuthConfigDecryptedCredentialServiceAccountCredentialsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__de53380a3cb7308a431c9929b6c93943f9fed05221933bed5381acdbdd5b5524)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetScope")
    def reset_scope(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScope", []))

    @jsii.member(jsii_name="resetServiceAccount")
    def reset_service_account(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceAccount", []))

    @builtins.property
    @jsii.member(jsii_name="scopeInput")
    def scope_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scopeInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountInput")
    def service_account_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scope"))

    @scope.setter
    def scope(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9efbd83507f67a9d8c08d003de81bff96c498ea13b5ffbf5c57b4f20d504e59b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scope", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccount")
    def service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccount"))

    @service_account.setter
    def service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf23af7fd28f021dc9ed9c7ca627c7766bb189299604da1d44ac7f9bc560566d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIntegrationsAuthConfigDecryptedCredentialServiceAccountCredentials]:
        return typing.cast(typing.Optional[GoogleIntegrationsAuthConfigDecryptedCredentialServiceAccountCredentials], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIntegrationsAuthConfigDecryptedCredentialServiceAccountCredentials],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__775e65fd0054924b5d57078f79cbbbfae5810f9abb326991d5a5a22d2ebbe735)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIntegrationsAuthConfig.GoogleIntegrationsAuthConfigDecryptedCredentialUsernameAndPassword",
    jsii_struct_bases=[],
    name_mapping={"password": "password", "username": "username"},
)
class GoogleIntegrationsAuthConfigDecryptedCredentialUsernameAndPassword:
    def __init__(
        self,
        *,
        password: typing.Optional[builtins.str] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param password: Password to be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#password GoogleIntegrationsAuthConfig#password}
        :param username: Username to be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#username GoogleIntegrationsAuthConfig#username}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d12e0aed0ed12927058bd0e1f05b6ceb11fe5bd1cdced9739a5010bf9b489d5f)
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if password is not None:
            self._values["password"] = password
        if username is not None:
            self._values["username"] = username

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Password to be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#password GoogleIntegrationsAuthConfig#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''Username to be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#username GoogleIntegrationsAuthConfig#username}
        '''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIntegrationsAuthConfigDecryptedCredentialUsernameAndPassword(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIntegrationsAuthConfigDecryptedCredentialUsernameAndPasswordOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationsAuthConfig.GoogleIntegrationsAuthConfigDecryptedCredentialUsernameAndPasswordOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__34fde1dd2636e1fb21e038cc275fd850858df230702aa557fbddeb7aed695d97)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @jsii.member(jsii_name="resetUsername")
    def reset_username(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsername", []))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3872d6f71e29b31a2418e5bb0bcb05e083e0fcf1f841aac767a9b7e1b0947658)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85759bb7163462df56d3dda161b52ba3e3a09dd56df6215c350bbad064e35f4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIntegrationsAuthConfigDecryptedCredentialUsernameAndPassword]:
        return typing.cast(typing.Optional[GoogleIntegrationsAuthConfigDecryptedCredentialUsernameAndPassword], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIntegrationsAuthConfigDecryptedCredentialUsernameAndPassword],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52cc7b688f794f7db96bb997dba2d6687a2eacb26ba16c9116e65875038e6f52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIntegrationsAuthConfig.GoogleIntegrationsAuthConfigTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleIntegrationsAuthConfigTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#create GoogleIntegrationsAuthConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#delete GoogleIntegrationsAuthConfig#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#update GoogleIntegrationsAuthConfig#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2995c0be143addd13cb7d76b0caff320fe7a654eec202df8a295d9ae4acccde)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#create GoogleIntegrationsAuthConfig#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#delete GoogleIntegrationsAuthConfig#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_auth_config#update GoogleIntegrationsAuthConfig#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIntegrationsAuthConfigTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIntegrationsAuthConfigTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationsAuthConfig.GoogleIntegrationsAuthConfigTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__31d463f66486e68d4508881564c6c7420d18b7ffb89902d34665277a927ed59f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f413d46793fcb67b101397f0f5bb047c66f402547fd4247bb5437851977f23e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bcff442f1bc1c2af3a46de41c798911864b9a5e00a11d04426d99a01f983423)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ea63d25bbc4cf54b5c68416d405f880781f3b4eb4a8eafe7a28b421c6ded9af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIntegrationsAuthConfigTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIntegrationsAuthConfigTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIntegrationsAuthConfigTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e944e934a4220a9247a15138527616fd65d3cf345751424fe9147b3c736116c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleIntegrationsAuthConfig",
    "GoogleIntegrationsAuthConfigClientCertificate",
    "GoogleIntegrationsAuthConfigClientCertificateOutputReference",
    "GoogleIntegrationsAuthConfigConfig",
    "GoogleIntegrationsAuthConfigDecryptedCredential",
    "GoogleIntegrationsAuthConfigDecryptedCredentialAuthToken",
    "GoogleIntegrationsAuthConfigDecryptedCredentialAuthTokenOutputReference",
    "GoogleIntegrationsAuthConfigDecryptedCredentialJwt",
    "GoogleIntegrationsAuthConfigDecryptedCredentialJwtOutputReference",
    "GoogleIntegrationsAuthConfigDecryptedCredentialOauth2AuthorizationCode",
    "GoogleIntegrationsAuthConfigDecryptedCredentialOauth2AuthorizationCodeOutputReference",
    "GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentials",
    "GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsOutputReference",
    "GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParams",
    "GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntries",
    "GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKey",
    "GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKeyLiteralValue",
    "GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKeyLiteralValueOutputReference",
    "GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKeyOutputReference",
    "GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesList",
    "GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesOutputReference",
    "GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValue",
    "GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValueLiteralValue",
    "GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValueLiteralValueOutputReference",
    "GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValueOutputReference",
    "GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsOutputReference",
    "GoogleIntegrationsAuthConfigDecryptedCredentialOidcToken",
    "GoogleIntegrationsAuthConfigDecryptedCredentialOidcTokenOutputReference",
    "GoogleIntegrationsAuthConfigDecryptedCredentialOutputReference",
    "GoogleIntegrationsAuthConfigDecryptedCredentialServiceAccountCredentials",
    "GoogleIntegrationsAuthConfigDecryptedCredentialServiceAccountCredentialsOutputReference",
    "GoogleIntegrationsAuthConfigDecryptedCredentialUsernameAndPassword",
    "GoogleIntegrationsAuthConfigDecryptedCredentialUsernameAndPasswordOutputReference",
    "GoogleIntegrationsAuthConfigTimeouts",
    "GoogleIntegrationsAuthConfigTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__ee9493c096b6697926a4348d4ad6593f51d999513f08a5bc0b80eb0d8c86c6d6(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    display_name: builtins.str,
    location: builtins.str,
    client_certificate: typing.Optional[typing.Union[GoogleIntegrationsAuthConfigClientCertificate, typing.Dict[builtins.str, typing.Any]]] = None,
    decrypted_credential: typing.Optional[typing.Union[GoogleIntegrationsAuthConfigDecryptedCredential, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    expiry_notification_duration: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    override_valid_time: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleIntegrationsAuthConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    visibility: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__28d4cc60494f0041175dc1cf34a368149ac6e2f7f2d5f46172d9a0dbd9c5b437(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40d6b4352aface14d48de484e0bd0cd920d32ef63a8a72e89a944dd5084db134(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2f9bd1128323bd5a13716e9fc28dc2ecd8816b29b15db7061b2524f07797c43(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__453f6521dca419452da47b8f90aa9558958a1e8e611e674b30e563885800c37c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d8609649fe8f6fc4f4c939a74d4c70b71c9c6f245c8bacd85da8d7ac255a186(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0cffb2f048b3418bcf294ed1e907fb79118a00328557c7f1699d822b220f58f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fd45caa23bda6dfefad6f9fd6fe3c9470b3c8a72230c09cd5994b4998d0e290(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__839c1605efd4c51ece5ce48161d22838df7fa6856fbbf39818988a94cf057714(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08ed3bd4a8bc2852e5d00f9af822041172d9eb81ecd6fe15a83092f8d4914780(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__313726a9c92776aff936e1e7ebbae16f9833cf5b8136472cf4acaff6c1640977(
    *,
    encrypted_private_key: builtins.str,
    ssl_certificate: builtins.str,
    passphrase: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f3d733a6be5f6a5033fddbe4b7b37ed4ed96ed369f4e502a806c5a7fa9b9eee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fdd5f394d1f0f9d99d16ddf50134be56a67053299f316f91efba5b646ffaeab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbd7380534a58e215baa2ecd36d2f20ec37249e9d4526dbdcd6996a9f7f0bd98(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d91cf98d904aa888e1094d3c59c80f37c24d8dcf19f8b8a288b388e7fb6ff0f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__961785801b82f88a19d5b3da8cd86c5296a67415598d1d368049a21dfe48ccfb(
    value: typing.Optional[GoogleIntegrationsAuthConfigClientCertificate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__685871352baed33cb5f97b6ed78dbf48e11cf271446ecb6d89569c77a1bd7a01(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    display_name: builtins.str,
    location: builtins.str,
    client_certificate: typing.Optional[typing.Union[GoogleIntegrationsAuthConfigClientCertificate, typing.Dict[builtins.str, typing.Any]]] = None,
    decrypted_credential: typing.Optional[typing.Union[GoogleIntegrationsAuthConfigDecryptedCredential, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    expiry_notification_duration: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    override_valid_time: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleIntegrationsAuthConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    visibility: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93d0b99a71af54e8c11e1815002bc21b6859b8cc337d52741978197b832436be(
    *,
    credential_type: builtins.str,
    auth_token: typing.Optional[typing.Union[GoogleIntegrationsAuthConfigDecryptedCredentialAuthToken, typing.Dict[builtins.str, typing.Any]]] = None,
    jwt: typing.Optional[typing.Union[GoogleIntegrationsAuthConfigDecryptedCredentialJwt, typing.Dict[builtins.str, typing.Any]]] = None,
    oauth2_authorization_code: typing.Optional[typing.Union[GoogleIntegrationsAuthConfigDecryptedCredentialOauth2AuthorizationCode, typing.Dict[builtins.str, typing.Any]]] = None,
    oauth2_client_credentials: typing.Optional[typing.Union[GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentials, typing.Dict[builtins.str, typing.Any]]] = None,
    oidc_token: typing.Optional[typing.Union[GoogleIntegrationsAuthConfigDecryptedCredentialOidcToken, typing.Dict[builtins.str, typing.Any]]] = None,
    service_account_credentials: typing.Optional[typing.Union[GoogleIntegrationsAuthConfigDecryptedCredentialServiceAccountCredentials, typing.Dict[builtins.str, typing.Any]]] = None,
    username_and_password: typing.Optional[typing.Union[GoogleIntegrationsAuthConfigDecryptedCredentialUsernameAndPassword, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc0446fa5fde5a2aa70772377c7ec14f7190c691a2077fa63a54e608097dab49(
    *,
    token: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffc89b82ff32a0442a6bbf8a8babcb0669f6ba1d23fcc2ea6ac768d445cbc675(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b43a5d2e80f9e9b46ef6081298804cbfa1205af7601e18b9a4778993aa4a1b37(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab7e9be4b23f704ed38a7573b0cbabe28b76147879da832fd7dfb2250472fefb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a222d6f1d7f639343fc3fdff9d85e6805c798207c9e1228cf362c8cc73f440bf(
    value: typing.Optional[GoogleIntegrationsAuthConfigDecryptedCredentialAuthToken],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef91bb89dab7c53f08647db495af9573774b2649d737b98bb1a16a979425ef47(
    *,
    jwt_header: typing.Optional[builtins.str] = None,
    jwt_payload: typing.Optional[builtins.str] = None,
    secret: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06f2c1a56b102cd8ce6820695f6f686c85a0768db2a00ec19576aae0e049eec5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__baaf4af9d928d9809cdbe054c9cc068da44be5d9b21c5015ec494a95430807dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3831ebe34a31ea01b7a1ba66c4bfc4f54bf9b34b76d6836baaeb7483cb79f311(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea91ed621d670975b05c56021bafcd7e620ff1441c5797854541cbee43d69f49(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d40d55aabfde0bac477055fbeafc03770fb2daf9f4e94ac4088dfd670f86ee4(
    value: typing.Optional[GoogleIntegrationsAuthConfigDecryptedCredentialJwt],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f5ddff7e5fa52f1b180ecc44481b524d1291e8eb5fd46aac50a21060a257703(
    *,
    auth_endpoint: typing.Optional[builtins.str] = None,
    client_id: typing.Optional[builtins.str] = None,
    client_secret: typing.Optional[builtins.str] = None,
    scope: typing.Optional[builtins.str] = None,
    token_endpoint: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97b51fb44a5df0962d153635b55440b4bdc0a27b101eaf0a057d026af6a7152c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33fdab18585a0773b13b2423503e5b43e5991741be0ea709098a5bbeee5b5eef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b3caaa1bd7c321c1047793dc53ead08777dde1dbbdfc6f705d118388722736c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ec393dcbaff798dd64e075e82e3a3668e2ee10b7da356984dd0bc0e75645ec7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0c9bc372474b2f783f2cfccee96a2eee7752e5e786e53736aaa171c742cba8f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b6e594f2d32a5b487c85cc541ac2146889a765e2965a606875294a9e12887b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6af11264c679af7629801a053b4c54e769df355720c0c0aa352a693cf0bdd575(
    value: typing.Optional[GoogleIntegrationsAuthConfigDecryptedCredentialOauth2AuthorizationCode],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30797a6bdd4bf7253f973bc13c7ee451bbdb036467e8f4b2f46de5efb8fded84(
    *,
    client_id: typing.Optional[builtins.str] = None,
    client_secret: typing.Optional[builtins.str] = None,
    request_type: typing.Optional[builtins.str] = None,
    scope: typing.Optional[builtins.str] = None,
    token_endpoint: typing.Optional[builtins.str] = None,
    token_params: typing.Optional[typing.Union[GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParams, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46b3a7d8b833126f69024cd6036aa8da375ffad6375ce5f9a665a5e312da03c6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3534691547b63529343556842c85b730830393992b36be355ee36bef6cb3d78(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d13eb92a7f3220d7bd081fe3e870ddbf08eff6bb7b905b58f711915be500de2b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b6184549141a36c4a8405fb37b7ea090de9e7749c4792ca599abe35eeb8711d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d772bb032ba2981dba40edc17b9482eaada28853075197e22db7de4a5d6bb840(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddcacc24536d2924f895c3f9e23cca3ea779bcfb2fceb7e5804bd68ce43462b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5b695f78ddb802a23a0ad4ca19bde41c3710615bd0ccacff960d0d88ab5b8c2(
    value: typing.Optional[GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentials],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6ac4b047aa7152163364acd54310bec551a569b0f16bcd14d3d89b6d73fdb98(
    *,
    entries: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntries, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0f969b322f49d833740c55314ab654ad39a9b1a1a0dbfec445fb61ac8ab006e(
    *,
    key: typing.Optional[typing.Union[GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKey, typing.Dict[builtins.str, typing.Any]]] = None,
    value: typing.Optional[typing.Union[GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValue, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b4ac980fed1b1abebd9cb3d60d3a79aa8c646b07e5d8be1779869fbb7b1dc6a(
    *,
    literal_value: typing.Optional[typing.Union[GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKeyLiteralValue, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b36e84cf3ca4cfe50a8ddecd69d0b561cdca2abf866683c4e1c3d73e0fe01aff(
    *,
    string_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8a935ed6e8df532dc1bcd3ae7856e3d6af595eb9984df95c4cab3f758c6260a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4310c88c7831b92e24d40253ebd260d8597429f9a3902a53a554437c18896c80(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b51f8bea57680c316513dc6d3d246a51b9fb710f92af88cf6d88aa68b790d444(
    value: typing.Optional[GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKeyLiteralValue],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3c660e57d99a3e2ccfcf6bcdd342cd32b4f3eec5fddb9291609157477abf552(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2860b41386298ab6485fd90b53f7f8d709a58119bada3936cb1064610469c83(
    value: typing.Optional[GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKey],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaee4ab1296b6e8710b96403ebc31b9a2d5ba79af1c685624f0c76c2241b2cdd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bc1bcc5f7ca38e406924e4b1673768a39a2b4a3ba042ad4df0cce47a7e331fb(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2e1f8227bed593ea1a8c05f267e90044b404f1a7e144a7857a2c8edc5fcb311(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__743ded25321264f822185d10737f1512bf13ad16a7a51ab7a2a78e0503f4dcf1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db6c0847a8ec7069fba30cdae8d433723b6adbb9ad54d7f07160819419422941(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e61a46341b6146d85d6c01b9f202711467d1b0c07df9697fc3db93cd5f9d2aa8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntries]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62ced7d2f705a706c18b2ad709d267c2d2b34e56d1d1b41e5358336c5d78b243(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42662ce7476ae53ac3b9baf5a4ee2569117d7ab88fae127c24b792b40040db93(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntries]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a37ad2bef70c0e3a9b5751d7b9050f9c0f1f3abfd2475c7863b5e2ec80e3252(
    *,
    literal_value: typing.Optional[typing.Union[GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValueLiteralValue, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8731c5f245ce26c742d46cf31b190a90fc615d958b1069049342aaf5ef0dd98(
    *,
    string_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6aead4a4ca58793c3b47219d381a49d397e6f4d67d8fdf748511594c0e137f40(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9b89b6f5d9de8cbdcf2c6d68a8c8c93d69c565a5f604a2d25d6a434c63cba99(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6f8802c42a03e7b9a8eb80f5846406c5769062ffc567c253ab6c23b64a3ca85(
    value: typing.Optional[GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValueLiteralValue],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c428141dcf8f19dc1c2468a100eb34c9c451bd6cdcfd513db64025635b8ca1c5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__347e98a8dde3d5eb03935ff0fc00de8cdc0b5261e894a27b102e1e865358f8da(
    value: typing.Optional[GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValue],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74a7f5afc620e1be8d1e526babb7f3129250a9c333aeed1c5826a63402b3b04f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f87aedc5f5e9e395c091d1cb34c4cac633d47a88ca04939f8bc84eac8136e7f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntries, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5118a4b25a0bddeb36a9d0c637084a2b9df42bb59a84749f27212e89817252eb(
    value: typing.Optional[GoogleIntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParams],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87abe8c28ba09bc4a8ed647992bdfaff12d7b4efe255d2d0751ca4e8726249dc(
    *,
    audience: typing.Optional[builtins.str] = None,
    service_account_email: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__deadc70ef6b3a1235d0c17a04bab1d323ceb20dc78ebcbf6b1c6c2c8afc64139(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f961759938a50627cf14f041578689228fa0ce5d87d771b39cc32c6ce2a0d383(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be3401f346e3667b0a5f1c09f0496644a76e1073aa502693937f2348cbb4e0b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e22827942fcb565e755e336f702afc96b8221d0a20989541606994e7ffcae89b(
    value: typing.Optional[GoogleIntegrationsAuthConfigDecryptedCredentialOidcToken],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3ef9cfcd7869587f62509a2aaefe3f0018f6f3a4f0bf449c8b92d331710e8b6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63f987ef32e94cca040ac4816b07ec1d4da1c07d553b885aae14ab54e4fb96a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3892322fe456afb8ad198edcdfc68357f66f3400a95543ece9889e27fc05d251(
    value: typing.Optional[GoogleIntegrationsAuthConfigDecryptedCredential],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__397067c075e1b17e68d2d667d7dde60ee85754009255578d2156db8be4f67265(
    *,
    scope: typing.Optional[builtins.str] = None,
    service_account: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de53380a3cb7308a431c9929b6c93943f9fed05221933bed5381acdbdd5b5524(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9efbd83507f67a9d8c08d003de81bff96c498ea13b5ffbf5c57b4f20d504e59b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf23af7fd28f021dc9ed9c7ca627c7766bb189299604da1d44ac7f9bc560566d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__775e65fd0054924b5d57078f79cbbbfae5810f9abb326991d5a5a22d2ebbe735(
    value: typing.Optional[GoogleIntegrationsAuthConfigDecryptedCredentialServiceAccountCredentials],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d12e0aed0ed12927058bd0e1f05b6ceb11fe5bd1cdced9739a5010bf9b489d5f(
    *,
    password: typing.Optional[builtins.str] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34fde1dd2636e1fb21e038cc275fd850858df230702aa557fbddeb7aed695d97(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3872d6f71e29b31a2418e5bb0bcb05e083e0fcf1f841aac767a9b7e1b0947658(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85759bb7163462df56d3dda161b52ba3e3a09dd56df6215c350bbad064e35f4c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52cc7b688f794f7db96bb997dba2d6687a2eacb26ba16c9116e65875038e6f52(
    value: typing.Optional[GoogleIntegrationsAuthConfigDecryptedCredentialUsernameAndPassword],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2995c0be143addd13cb7d76b0caff320fe7a654eec202df8a295d9ae4acccde(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31d463f66486e68d4508881564c6c7420d18b7ffb89902d34665277a927ed59f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f413d46793fcb67b101397f0f5bb047c66f402547fd4247bb5437851977f23e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bcff442f1bc1c2af3a46de41c798911864b9a5e00a11d04426d99a01f983423(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ea63d25bbc4cf54b5c68416d405f880781f3b4eb4a8eafe7a28b421c6ded9af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e944e934a4220a9247a15138527616fd65d3cf345751424fe9147b3c736116c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIntegrationsAuthConfigTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
