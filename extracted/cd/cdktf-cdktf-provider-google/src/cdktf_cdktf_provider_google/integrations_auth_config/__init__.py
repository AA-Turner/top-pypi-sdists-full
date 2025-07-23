r'''
# `google_integrations_auth_config`

Refer to the Terraform Registry for docs: [`google_integrations_auth_config`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config).
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


class IntegrationsAuthConfig(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationsAuthConfig.IntegrationsAuthConfig",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config google_integrations_auth_config}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        display_name: builtins.str,
        location: builtins.str,
        client_certificate: typing.Optional[typing.Union["IntegrationsAuthConfigClientCertificate", typing.Dict[builtins.str, typing.Any]]] = None,
        decrypted_credential: typing.Optional[typing.Union["IntegrationsAuthConfigDecryptedCredential", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        expiry_notification_duration: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        override_valid_time: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["IntegrationsAuthConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        visibility: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config google_integrations_auth_config} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param display_name: The name of the auth config. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#display_name IntegrationsAuthConfig#display_name}
        :param location: Location in which client needs to be provisioned. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#location IntegrationsAuthConfig#location}
        :param client_certificate: client_certificate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#client_certificate IntegrationsAuthConfig#client_certificate}
        :param decrypted_credential: decrypted_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#decrypted_credential IntegrationsAuthConfig#decrypted_credential}
        :param description: A description of the auth config. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#description IntegrationsAuthConfig#description}
        :param expiry_notification_duration: User can define the time to receive notification after which the auth config becomes invalid. Support up to 30 days. Support granularity in hours. A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#expiry_notification_duration IntegrationsAuthConfig#expiry_notification_duration}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#id IntegrationsAuthConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param override_valid_time: User provided expiry time to override. For the example of Salesforce, username/password credentials can be valid for 6 months depending on the instance settings. A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits. Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#override_valid_time IntegrationsAuthConfig#override_valid_time}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#project IntegrationsAuthConfig#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#timeouts IntegrationsAuthConfig#timeouts}
        :param visibility: The visibility of the auth config. Possible values: ["PRIVATE", "CLIENT_VISIBLE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#visibility IntegrationsAuthConfig#visibility}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28ed39353b561ecfa8fc0a2be3fc95df3f8b11c3e11c38f10c280bb07c7d8ede)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = IntegrationsAuthConfigConfig(
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
        '''Generates CDKTF code for importing a IntegrationsAuthConfig resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the IntegrationsAuthConfig to import.
        :param import_from_id: The id of the existing IntegrationsAuthConfig that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the IntegrationsAuthConfig to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3eb249671825395261449354ebed9f615840f032093efa3438c66a64ec61254e)
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
        :param encrypted_private_key: The ssl certificate encoded in PEM format. This string must include the begin header and end footer lines. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#encrypted_private_key IntegrationsAuthConfig#encrypted_private_key}
        :param ssl_certificate: The ssl certificate encoded in PEM format. This string must include the begin header and end footer lines. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#ssl_certificate IntegrationsAuthConfig#ssl_certificate}
        :param passphrase: 'passphrase' should be left unset if private key is not encrypted. Note that 'passphrase' is not the password for web server, but an extra layer of security to protected private key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#passphrase IntegrationsAuthConfig#passphrase}
        '''
        value = IntegrationsAuthConfigClientCertificate(
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
        auth_token: typing.Optional[typing.Union["IntegrationsAuthConfigDecryptedCredentialAuthToken", typing.Dict[builtins.str, typing.Any]]] = None,
        jwt: typing.Optional[typing.Union["IntegrationsAuthConfigDecryptedCredentialJwt", typing.Dict[builtins.str, typing.Any]]] = None,
        oauth2_authorization_code: typing.Optional[typing.Union["IntegrationsAuthConfigDecryptedCredentialOauth2AuthorizationCode", typing.Dict[builtins.str, typing.Any]]] = None,
        oauth2_client_credentials: typing.Optional[typing.Union["IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentials", typing.Dict[builtins.str, typing.Any]]] = None,
        oidc_token: typing.Optional[typing.Union["IntegrationsAuthConfigDecryptedCredentialOidcToken", typing.Dict[builtins.str, typing.Any]]] = None,
        service_account_credentials: typing.Optional[typing.Union["IntegrationsAuthConfigDecryptedCredentialServiceAccountCredentials", typing.Dict[builtins.str, typing.Any]]] = None,
        username_and_password: typing.Optional[typing.Union["IntegrationsAuthConfigDecryptedCredentialUsernameAndPassword", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param credential_type: Credential type associated with auth configs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#credential_type IntegrationsAuthConfig#credential_type}
        :param auth_token: auth_token block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#auth_token IntegrationsAuthConfig#auth_token}
        :param jwt: jwt block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#jwt IntegrationsAuthConfig#jwt}
        :param oauth2_authorization_code: oauth2_authorization_code block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#oauth2_authorization_code IntegrationsAuthConfig#oauth2_authorization_code}
        :param oauth2_client_credentials: oauth2_client_credentials block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#oauth2_client_credentials IntegrationsAuthConfig#oauth2_client_credentials}
        :param oidc_token: oidc_token block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#oidc_token IntegrationsAuthConfig#oidc_token}
        :param service_account_credentials: service_account_credentials block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#service_account_credentials IntegrationsAuthConfig#service_account_credentials}
        :param username_and_password: username_and_password block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#username_and_password IntegrationsAuthConfig#username_and_password}
        '''
        value = IntegrationsAuthConfigDecryptedCredential(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#create IntegrationsAuthConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#delete IntegrationsAuthConfig#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#update IntegrationsAuthConfig#update}.
        '''
        value = IntegrationsAuthConfigTimeouts(
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
    ) -> "IntegrationsAuthConfigClientCertificateOutputReference":
        return typing.cast("IntegrationsAuthConfigClientCertificateOutputReference", jsii.get(self, "clientCertificate"))

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
    ) -> "IntegrationsAuthConfigDecryptedCredentialOutputReference":
        return typing.cast("IntegrationsAuthConfigDecryptedCredentialOutputReference", jsii.get(self, "decryptedCredential"))

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
    def timeouts(self) -> "IntegrationsAuthConfigTimeoutsOutputReference":
        return typing.cast("IntegrationsAuthConfigTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    ) -> typing.Optional["IntegrationsAuthConfigClientCertificate"]:
        return typing.cast(typing.Optional["IntegrationsAuthConfigClientCertificate"], jsii.get(self, "clientCertificateInput"))

    @builtins.property
    @jsii.member(jsii_name="decryptedCredentialInput")
    def decrypted_credential_input(
        self,
    ) -> typing.Optional["IntegrationsAuthConfigDecryptedCredential"]:
        return typing.cast(typing.Optional["IntegrationsAuthConfigDecryptedCredential"], jsii.get(self, "decryptedCredentialInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "IntegrationsAuthConfigTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "IntegrationsAuthConfigTimeouts"]], jsii.get(self, "timeoutsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__65c49c9277c122dd50be540e0f6f63954515029eb1d10433960db9cf299fdf55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92bbd80c7071182a8e9061820fc1eb03b501fcefecf952e94f49f7afc04bb89c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expiryNotificationDuration")
    def expiry_notification_duration(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "expiryNotificationDuration"))

    @expiry_notification_duration.setter
    def expiry_notification_duration(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f808a81dd6a120741209838b211dff22123b72d841ee2163a212835c494967d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expiryNotificationDuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a91ace91979df34161728719263c6393cb4335599cfe20b98145e9fd5217321c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__373fc424f5cca567efa5a8835bec1bf000995f5b2a6dcac90c61d5fe47152426)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="overrideValidTime")
    def override_valid_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "overrideValidTime"))

    @override_valid_time.setter
    def override_valid_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__862e704e1d6fd1a5645d3f51a77ded265f9379effbfa5c4fab7c1ca7d1436b9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "overrideValidTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c5639d5eac9a866ad3c820f6196f9e19cfb57d861f235c44bf1206503797576)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="visibility")
    def visibility(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "visibility"))

    @visibility.setter
    def visibility(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e10bc03df390f630edb24b91622bfa29c440796acd31d2d05979a63a89e7acb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "visibility", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.integrationsAuthConfig.IntegrationsAuthConfigClientCertificate",
    jsii_struct_bases=[],
    name_mapping={
        "encrypted_private_key": "encryptedPrivateKey",
        "ssl_certificate": "sslCertificate",
        "passphrase": "passphrase",
    },
)
class IntegrationsAuthConfigClientCertificate:
    def __init__(
        self,
        *,
        encrypted_private_key: builtins.str,
        ssl_certificate: builtins.str,
        passphrase: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param encrypted_private_key: The ssl certificate encoded in PEM format. This string must include the begin header and end footer lines. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#encrypted_private_key IntegrationsAuthConfig#encrypted_private_key}
        :param ssl_certificate: The ssl certificate encoded in PEM format. This string must include the begin header and end footer lines. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#ssl_certificate IntegrationsAuthConfig#ssl_certificate}
        :param passphrase: 'passphrase' should be left unset if private key is not encrypted. Note that 'passphrase' is not the password for web server, but an extra layer of security to protected private key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#passphrase IntegrationsAuthConfig#passphrase}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__248680474fffa63e8f19838f9b307a7879c89b440a800452d4d638e8e0060467)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#encrypted_private_key IntegrationsAuthConfig#encrypted_private_key}
        '''
        result = self._values.get("encrypted_private_key")
        assert result is not None, "Required property 'encrypted_private_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ssl_certificate(self) -> builtins.str:
        '''The ssl certificate encoded in PEM format. This string must include the begin header and end footer lines.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#ssl_certificate IntegrationsAuthConfig#ssl_certificate}
        '''
        result = self._values.get("ssl_certificate")
        assert result is not None, "Required property 'ssl_certificate' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def passphrase(self) -> typing.Optional[builtins.str]:
        ''''passphrase' should be left unset if private key is not encrypted.

        Note that 'passphrase' is not the password for web server, but an extra layer of security to protected private key.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#passphrase IntegrationsAuthConfig#passphrase}
        '''
        result = self._values.get("passphrase")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationsAuthConfigClientCertificate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IntegrationsAuthConfigClientCertificateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationsAuthConfig.IntegrationsAuthConfigClientCertificateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__71b9be5f31bb30b69cba0c4ba2b1d2e7f287c1f8b392041703775bc141ceabc8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fec6beee0e8a30b4a2110d2b5755bede4169626d515f4f62e4c1345e52319489)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptedPrivateKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="passphrase")
    def passphrase(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "passphrase"))

    @passphrase.setter
    def passphrase(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96378f8ff680a73761faf05f48ecb2bf28735b523d2d28af691fc82040edb419)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passphrase", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sslCertificate")
    def ssl_certificate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sslCertificate"))

    @ssl_certificate.setter
    def ssl_certificate(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a0b1e5d9fd1e3eb7a3ccf6bc89f91d0963085fd42924ab6ac021ef81afdb990)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sslCertificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IntegrationsAuthConfigClientCertificate]:
        return typing.cast(typing.Optional[IntegrationsAuthConfigClientCertificate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IntegrationsAuthConfigClientCertificate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__069ffbe7173a6ee752a00cefaea07ddb66f94b105cf5de173f3433fde9ee6dca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.integrationsAuthConfig.IntegrationsAuthConfigConfig",
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
class IntegrationsAuthConfigConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        client_certificate: typing.Optional[typing.Union[IntegrationsAuthConfigClientCertificate, typing.Dict[builtins.str, typing.Any]]] = None,
        decrypted_credential: typing.Optional[typing.Union["IntegrationsAuthConfigDecryptedCredential", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        expiry_notification_duration: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        override_valid_time: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["IntegrationsAuthConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
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
        :param display_name: The name of the auth config. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#display_name IntegrationsAuthConfig#display_name}
        :param location: Location in which client needs to be provisioned. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#location IntegrationsAuthConfig#location}
        :param client_certificate: client_certificate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#client_certificate IntegrationsAuthConfig#client_certificate}
        :param decrypted_credential: decrypted_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#decrypted_credential IntegrationsAuthConfig#decrypted_credential}
        :param description: A description of the auth config. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#description IntegrationsAuthConfig#description}
        :param expiry_notification_duration: User can define the time to receive notification after which the auth config becomes invalid. Support up to 30 days. Support granularity in hours. A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#expiry_notification_duration IntegrationsAuthConfig#expiry_notification_duration}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#id IntegrationsAuthConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param override_valid_time: User provided expiry time to override. For the example of Salesforce, username/password credentials can be valid for 6 months depending on the instance settings. A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits. Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#override_valid_time IntegrationsAuthConfig#override_valid_time}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#project IntegrationsAuthConfig#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#timeouts IntegrationsAuthConfig#timeouts}
        :param visibility: The visibility of the auth config. Possible values: ["PRIVATE", "CLIENT_VISIBLE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#visibility IntegrationsAuthConfig#visibility}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(client_certificate, dict):
            client_certificate = IntegrationsAuthConfigClientCertificate(**client_certificate)
        if isinstance(decrypted_credential, dict):
            decrypted_credential = IntegrationsAuthConfigDecryptedCredential(**decrypted_credential)
        if isinstance(timeouts, dict):
            timeouts = IntegrationsAuthConfigTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7435c5bc656395708ad11f02d10e8989a819cddb8fb792bef125a33722f3b9c)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#display_name IntegrationsAuthConfig#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Location in which client needs to be provisioned.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#location IntegrationsAuthConfig#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_certificate(
        self,
    ) -> typing.Optional[IntegrationsAuthConfigClientCertificate]:
        '''client_certificate block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#client_certificate IntegrationsAuthConfig#client_certificate}
        '''
        result = self._values.get("client_certificate")
        return typing.cast(typing.Optional[IntegrationsAuthConfigClientCertificate], result)

    @builtins.property
    def decrypted_credential(
        self,
    ) -> typing.Optional["IntegrationsAuthConfigDecryptedCredential"]:
        '''decrypted_credential block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#decrypted_credential IntegrationsAuthConfig#decrypted_credential}
        '''
        result = self._values.get("decrypted_credential")
        return typing.cast(typing.Optional["IntegrationsAuthConfigDecryptedCredential"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the auth config.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#description IntegrationsAuthConfig#description}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#expiry_notification_duration IntegrationsAuthConfig#expiry_notification_duration}
        '''
        result = self._values.get("expiry_notification_duration")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#id IntegrationsAuthConfig#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#override_valid_time IntegrationsAuthConfig#override_valid_time}
        '''
        result = self._values.get("override_valid_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#project IntegrationsAuthConfig#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["IntegrationsAuthConfigTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#timeouts IntegrationsAuthConfig#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["IntegrationsAuthConfigTimeouts"], result)

    @builtins.property
    def visibility(self) -> typing.Optional[builtins.str]:
        '''The visibility of the auth config. Possible values: ["PRIVATE", "CLIENT_VISIBLE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#visibility IntegrationsAuthConfig#visibility}
        '''
        result = self._values.get("visibility")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationsAuthConfigConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.integrationsAuthConfig.IntegrationsAuthConfigDecryptedCredential",
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
class IntegrationsAuthConfigDecryptedCredential:
    def __init__(
        self,
        *,
        credential_type: builtins.str,
        auth_token: typing.Optional[typing.Union["IntegrationsAuthConfigDecryptedCredentialAuthToken", typing.Dict[builtins.str, typing.Any]]] = None,
        jwt: typing.Optional[typing.Union["IntegrationsAuthConfigDecryptedCredentialJwt", typing.Dict[builtins.str, typing.Any]]] = None,
        oauth2_authorization_code: typing.Optional[typing.Union["IntegrationsAuthConfigDecryptedCredentialOauth2AuthorizationCode", typing.Dict[builtins.str, typing.Any]]] = None,
        oauth2_client_credentials: typing.Optional[typing.Union["IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentials", typing.Dict[builtins.str, typing.Any]]] = None,
        oidc_token: typing.Optional[typing.Union["IntegrationsAuthConfigDecryptedCredentialOidcToken", typing.Dict[builtins.str, typing.Any]]] = None,
        service_account_credentials: typing.Optional[typing.Union["IntegrationsAuthConfigDecryptedCredentialServiceAccountCredentials", typing.Dict[builtins.str, typing.Any]]] = None,
        username_and_password: typing.Optional[typing.Union["IntegrationsAuthConfigDecryptedCredentialUsernameAndPassword", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param credential_type: Credential type associated with auth configs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#credential_type IntegrationsAuthConfig#credential_type}
        :param auth_token: auth_token block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#auth_token IntegrationsAuthConfig#auth_token}
        :param jwt: jwt block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#jwt IntegrationsAuthConfig#jwt}
        :param oauth2_authorization_code: oauth2_authorization_code block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#oauth2_authorization_code IntegrationsAuthConfig#oauth2_authorization_code}
        :param oauth2_client_credentials: oauth2_client_credentials block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#oauth2_client_credentials IntegrationsAuthConfig#oauth2_client_credentials}
        :param oidc_token: oidc_token block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#oidc_token IntegrationsAuthConfig#oidc_token}
        :param service_account_credentials: service_account_credentials block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#service_account_credentials IntegrationsAuthConfig#service_account_credentials}
        :param username_and_password: username_and_password block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#username_and_password IntegrationsAuthConfig#username_and_password}
        '''
        if isinstance(auth_token, dict):
            auth_token = IntegrationsAuthConfigDecryptedCredentialAuthToken(**auth_token)
        if isinstance(jwt, dict):
            jwt = IntegrationsAuthConfigDecryptedCredentialJwt(**jwt)
        if isinstance(oauth2_authorization_code, dict):
            oauth2_authorization_code = IntegrationsAuthConfigDecryptedCredentialOauth2AuthorizationCode(**oauth2_authorization_code)
        if isinstance(oauth2_client_credentials, dict):
            oauth2_client_credentials = IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentials(**oauth2_client_credentials)
        if isinstance(oidc_token, dict):
            oidc_token = IntegrationsAuthConfigDecryptedCredentialOidcToken(**oidc_token)
        if isinstance(service_account_credentials, dict):
            service_account_credentials = IntegrationsAuthConfigDecryptedCredentialServiceAccountCredentials(**service_account_credentials)
        if isinstance(username_and_password, dict):
            username_and_password = IntegrationsAuthConfigDecryptedCredentialUsernameAndPassword(**username_and_password)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb05d451c636faa302295efff29827897186a33f627c1bb8da629482f4047e87)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#credential_type IntegrationsAuthConfig#credential_type}
        '''
        result = self._values.get("credential_type")
        assert result is not None, "Required property 'credential_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auth_token(
        self,
    ) -> typing.Optional["IntegrationsAuthConfigDecryptedCredentialAuthToken"]:
        '''auth_token block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#auth_token IntegrationsAuthConfig#auth_token}
        '''
        result = self._values.get("auth_token")
        return typing.cast(typing.Optional["IntegrationsAuthConfigDecryptedCredentialAuthToken"], result)

    @builtins.property
    def jwt(self) -> typing.Optional["IntegrationsAuthConfigDecryptedCredentialJwt"]:
        '''jwt block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#jwt IntegrationsAuthConfig#jwt}
        '''
        result = self._values.get("jwt")
        return typing.cast(typing.Optional["IntegrationsAuthConfigDecryptedCredentialJwt"], result)

    @builtins.property
    def oauth2_authorization_code(
        self,
    ) -> typing.Optional["IntegrationsAuthConfigDecryptedCredentialOauth2AuthorizationCode"]:
        '''oauth2_authorization_code block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#oauth2_authorization_code IntegrationsAuthConfig#oauth2_authorization_code}
        '''
        result = self._values.get("oauth2_authorization_code")
        return typing.cast(typing.Optional["IntegrationsAuthConfigDecryptedCredentialOauth2AuthorizationCode"], result)

    @builtins.property
    def oauth2_client_credentials(
        self,
    ) -> typing.Optional["IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentials"]:
        '''oauth2_client_credentials block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#oauth2_client_credentials IntegrationsAuthConfig#oauth2_client_credentials}
        '''
        result = self._values.get("oauth2_client_credentials")
        return typing.cast(typing.Optional["IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentials"], result)

    @builtins.property
    def oidc_token(
        self,
    ) -> typing.Optional["IntegrationsAuthConfigDecryptedCredentialOidcToken"]:
        '''oidc_token block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#oidc_token IntegrationsAuthConfig#oidc_token}
        '''
        result = self._values.get("oidc_token")
        return typing.cast(typing.Optional["IntegrationsAuthConfigDecryptedCredentialOidcToken"], result)

    @builtins.property
    def service_account_credentials(
        self,
    ) -> typing.Optional["IntegrationsAuthConfigDecryptedCredentialServiceAccountCredentials"]:
        '''service_account_credentials block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#service_account_credentials IntegrationsAuthConfig#service_account_credentials}
        '''
        result = self._values.get("service_account_credentials")
        return typing.cast(typing.Optional["IntegrationsAuthConfigDecryptedCredentialServiceAccountCredentials"], result)

    @builtins.property
    def username_and_password(
        self,
    ) -> typing.Optional["IntegrationsAuthConfigDecryptedCredentialUsernameAndPassword"]:
        '''username_and_password block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#username_and_password IntegrationsAuthConfig#username_and_password}
        '''
        result = self._values.get("username_and_password")
        return typing.cast(typing.Optional["IntegrationsAuthConfigDecryptedCredentialUsernameAndPassword"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationsAuthConfigDecryptedCredential(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.integrationsAuthConfig.IntegrationsAuthConfigDecryptedCredentialAuthToken",
    jsii_struct_bases=[],
    name_mapping={"token": "token", "type": "type"},
)
class IntegrationsAuthConfigDecryptedCredentialAuthToken:
    def __init__(
        self,
        *,
        token: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param token: The token for the auth type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#token IntegrationsAuthConfig#token}
        :param type: Authentication type, e.g. "Basic", "Bearer", etc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#type IntegrationsAuthConfig#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2f61513080a0e244dc01995e9289d720a0f1abbeba8661c340a8075d17d103d)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#token IntegrationsAuthConfig#token}
        '''
        result = self._values.get("token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Authentication type, e.g. "Basic", "Bearer", etc.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#type IntegrationsAuthConfig#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationsAuthConfigDecryptedCredentialAuthToken(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IntegrationsAuthConfigDecryptedCredentialAuthTokenOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationsAuthConfig.IntegrationsAuthConfigDecryptedCredentialAuthTokenOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6dd1b9e9fa5c6fbe773b1d6e7ed710ec7deba2102d5f7b4e4c21063627171e7c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fad78495f3c9a29d8a80251330beed1ef2bc773ec00c4e94d75937f28c283486)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "token", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e9e729340b065690fbb031a1a529be11694cce66528abb2b1d9afe453ccf5fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IntegrationsAuthConfigDecryptedCredentialAuthToken]:
        return typing.cast(typing.Optional[IntegrationsAuthConfigDecryptedCredentialAuthToken], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IntegrationsAuthConfigDecryptedCredentialAuthToken],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3de29e87965fd59860024749453517ee13ff1faf7750053cf554c69512a51482)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.integrationsAuthConfig.IntegrationsAuthConfigDecryptedCredentialJwt",
    jsii_struct_bases=[],
    name_mapping={
        "jwt_header": "jwtHeader",
        "jwt_payload": "jwtPayload",
        "secret": "secret",
    },
)
class IntegrationsAuthConfigDecryptedCredentialJwt:
    def __init__(
        self,
        *,
        jwt_header: typing.Optional[builtins.str] = None,
        jwt_payload: typing.Optional[builtins.str] = None,
        secret: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param jwt_header: Identifies which algorithm is used to generate the signature. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#jwt_header IntegrationsAuthConfig#jwt_header}
        :param jwt_payload: Contains a set of claims. The JWT specification defines seven Registered Claim Names which are the standard fields commonly included in tokens. Custom claims are usually also included, depending on the purpose of the token. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#jwt_payload IntegrationsAuthConfig#jwt_payload}
        :param secret: User's pre-shared secret to sign the token. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#secret IntegrationsAuthConfig#secret}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38133aed2ea7b86196ac43a9d1f6739001edcfa58838e8bc05e3ab38a9d65bcd)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#jwt_header IntegrationsAuthConfig#jwt_header}
        '''
        result = self._values.get("jwt_header")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def jwt_payload(self) -> typing.Optional[builtins.str]:
        '''Contains a set of claims.

        The JWT specification defines seven Registered Claim Names which are the standard fields commonly included in tokens. Custom claims are usually also included, depending on the purpose of the token.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#jwt_payload IntegrationsAuthConfig#jwt_payload}
        '''
        result = self._values.get("jwt_payload")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret(self) -> typing.Optional[builtins.str]:
        '''User's pre-shared secret to sign the token.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#secret IntegrationsAuthConfig#secret}
        '''
        result = self._values.get("secret")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationsAuthConfigDecryptedCredentialJwt(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IntegrationsAuthConfigDecryptedCredentialJwtOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationsAuthConfig.IntegrationsAuthConfigDecryptedCredentialJwtOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c20108819c50f48f449c380f23692cfea937068a6616587afdd3100f55cc75b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__50ba7422a7f6ab7f6255cf83ed8cbb0933242fde3e0af82691ff37754254842e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jwtHeader", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jwtPayload")
    def jwt_payload(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jwtPayload"))

    @jwt_payload.setter
    def jwt_payload(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__172491dbf1078d56323ef90512e406976532ce7020b48594f44e9a3269446bd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jwtPayload", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secret")
    def secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secret"))

    @secret.setter
    def secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9aaf25ced1da9b598a7e681798b1b5928cdfd9d076977a11b71bee18e19e29f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IntegrationsAuthConfigDecryptedCredentialJwt]:
        return typing.cast(typing.Optional[IntegrationsAuthConfigDecryptedCredentialJwt], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IntegrationsAuthConfigDecryptedCredentialJwt],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad9dc1b9fae688bfcee7ebe8a469fdc63638b7eaa6529884202cdbe5b7dd2978)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.integrationsAuthConfig.IntegrationsAuthConfigDecryptedCredentialOauth2AuthorizationCode",
    jsii_struct_bases=[],
    name_mapping={
        "auth_endpoint": "authEndpoint",
        "client_id": "clientId",
        "client_secret": "clientSecret",
        "scope": "scope",
        "token_endpoint": "tokenEndpoint",
    },
)
class IntegrationsAuthConfigDecryptedCredentialOauth2AuthorizationCode:
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
        :param auth_endpoint: The auth url endpoint to send the auth code request to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#auth_endpoint IntegrationsAuthConfig#auth_endpoint}
        :param client_id: The client's id. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#client_id IntegrationsAuthConfig#client_id}
        :param client_secret: The client's secret. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#client_secret IntegrationsAuthConfig#client_secret}
        :param scope: A space-delimited list of requested scope permissions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#scope IntegrationsAuthConfig#scope}
        :param token_endpoint: The token url endpoint to send the token request to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#token_endpoint IntegrationsAuthConfig#token_endpoint}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49d1f66bf32763276acd3475c3980eaca2d5734f5fef9d49e89961076f9b6287)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#auth_endpoint IntegrationsAuthConfig#auth_endpoint}
        '''
        result = self._values.get("auth_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_id(self) -> typing.Optional[builtins.str]:
        '''The client's id.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#client_id IntegrationsAuthConfig#client_id}
        '''
        result = self._values.get("client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_secret(self) -> typing.Optional[builtins.str]:
        '''The client's secret.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#client_secret IntegrationsAuthConfig#client_secret}
        '''
        result = self._values.get("client_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scope(self) -> typing.Optional[builtins.str]:
        '''A space-delimited list of requested scope permissions.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#scope IntegrationsAuthConfig#scope}
        '''
        result = self._values.get("scope")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token_endpoint(self) -> typing.Optional[builtins.str]:
        '''The token url endpoint to send the token request to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#token_endpoint IntegrationsAuthConfig#token_endpoint}
        '''
        result = self._values.get("token_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationsAuthConfigDecryptedCredentialOauth2AuthorizationCode(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IntegrationsAuthConfigDecryptedCredentialOauth2AuthorizationCodeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationsAuthConfig.IntegrationsAuthConfigDecryptedCredentialOauth2AuthorizationCodeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b57634cbe0a61b2e93455318009ca5e44f421e1f1f228cf390ecb480f1e771f4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__63bffb7c4fd24e1ce2461d72d5a0c13aae4c68c66c50b57260b6d1ac9997b705)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bdbf5c7c3b8dbe9167611972272769aa8704113de2c140cd6b340f2537e7c8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecret"))

    @client_secret.setter
    def client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f82790551d75317b330a59f2cfdada3901c4e8ee72779b9e4f08df91db1ce312)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scope"))

    @scope.setter
    def scope(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fe3fcd1a2fbddda0b80fe5dc4764399ec2357eea72ccbc3153eecee2443e05a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scope", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tokenEndpoint")
    def token_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tokenEndpoint"))

    @token_endpoint.setter
    def token_endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d15ecf6a144e1a6af6da0a3074e43435b499a0b95c15e5ff1b68c77a778f7ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tokenEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IntegrationsAuthConfigDecryptedCredentialOauth2AuthorizationCode]:
        return typing.cast(typing.Optional[IntegrationsAuthConfigDecryptedCredentialOauth2AuthorizationCode], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IntegrationsAuthConfigDecryptedCredentialOauth2AuthorizationCode],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6971457eb0f7c16da7def5af6fe17dbe4b37f75265707bd88822a848dbaa81a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.integrationsAuthConfig.IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentials",
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
class IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentials:
    def __init__(
        self,
        *,
        client_id: typing.Optional[builtins.str] = None,
        client_secret: typing.Optional[builtins.str] = None,
        request_type: typing.Optional[builtins.str] = None,
        scope: typing.Optional[builtins.str] = None,
        token_endpoint: typing.Optional[builtins.str] = None,
        token_params: typing.Optional[typing.Union["IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParams", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param client_id: The client's ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#client_id IntegrationsAuthConfig#client_id}
        :param client_secret: The client's secret. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#client_secret IntegrationsAuthConfig#client_secret}
        :param request_type: Represent how to pass parameters to fetch access token Possible values: ["REQUEST_TYPE_UNSPECIFIED", "REQUEST_BODY", "QUERY_PARAMETERS", "ENCODED_HEADER"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#request_type IntegrationsAuthConfig#request_type}
        :param scope: A space-delimited list of requested scope permissions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#scope IntegrationsAuthConfig#scope}
        :param token_endpoint: The token endpoint is used by the client to obtain an access token by presenting its authorization grant or refresh token. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#token_endpoint IntegrationsAuthConfig#token_endpoint}
        :param token_params: token_params block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#token_params IntegrationsAuthConfig#token_params}
        '''
        if isinstance(token_params, dict):
            token_params = IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParams(**token_params)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efbd34ac407d93931eee7208351bbda118347e1b26342520fd068482a620d76f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#client_id IntegrationsAuthConfig#client_id}
        '''
        result = self._values.get("client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_secret(self) -> typing.Optional[builtins.str]:
        '''The client's secret.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#client_secret IntegrationsAuthConfig#client_secret}
        '''
        result = self._values.get("client_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def request_type(self) -> typing.Optional[builtins.str]:
        '''Represent how to pass parameters to fetch access token Possible values: ["REQUEST_TYPE_UNSPECIFIED", "REQUEST_BODY", "QUERY_PARAMETERS", "ENCODED_HEADER"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#request_type IntegrationsAuthConfig#request_type}
        '''
        result = self._values.get("request_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scope(self) -> typing.Optional[builtins.str]:
        '''A space-delimited list of requested scope permissions.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#scope IntegrationsAuthConfig#scope}
        '''
        result = self._values.get("scope")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token_endpoint(self) -> typing.Optional[builtins.str]:
        '''The token endpoint is used by the client to obtain an access token by presenting its authorization grant or refresh token.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#token_endpoint IntegrationsAuthConfig#token_endpoint}
        '''
        result = self._values.get("token_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token_params(
        self,
    ) -> typing.Optional["IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParams"]:
        '''token_params block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#token_params IntegrationsAuthConfig#token_params}
        '''
        result = self._values.get("token_params")
        return typing.cast(typing.Optional["IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParams"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentials(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationsAuthConfig.IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__78fed2e6c75682cf5cb493cc2a14b4cbfb2874eb5e67378f25f6895015d0271b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putTokenParams")
    def put_token_params(
        self,
        *,
        entries: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntries", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param entries: entries block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#entries IntegrationsAuthConfig#entries}
        '''
        value = IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParams(
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
    ) -> "IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsOutputReference":
        return typing.cast("IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsOutputReference", jsii.get(self, "tokenParams"))

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
    ) -> typing.Optional["IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParams"]:
        return typing.cast(typing.Optional["IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParams"], jsii.get(self, "tokenParamsInput"))

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e634dcae61ddb6e393cfe886376c9c43d3c27467e671d9c1b7f239c68f3426f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecret"))

    @client_secret.setter
    def client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65d13a76360704cfb1f9fe399c0ad33fa4e2a0f20db6617041f714cbc655d5eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requestType")
    def request_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "requestType"))

    @request_type.setter
    def request_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4747e61f0df4773b907bbaecb83f51aa74f234f567843d5d260513e30dbdd98f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scope"))

    @scope.setter
    def scope(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0097046a834a56fa3a957b4da83e32023d9376511257c00b501dd256726be956)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scope", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tokenEndpoint")
    def token_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tokenEndpoint"))

    @token_endpoint.setter
    def token_endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e64955aea03a2b47eb00c479ad9c9761ff025fdb3fa88ad9c5f9dff664b08a14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tokenEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentials]:
        return typing.cast(typing.Optional[IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentials], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentials],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6782ba0cd11f5695e66379d9567a747d5e8e4a04af8bcbabd50fe1e390903dd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.integrationsAuthConfig.IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParams",
    jsii_struct_bases=[],
    name_mapping={"entries": "entries"},
)
class IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParams:
    def __init__(
        self,
        *,
        entries: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntries", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param entries: entries block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#entries IntegrationsAuthConfig#entries}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f19c7bfcd27473c135ddc867744e22c63c3966379cc4930ce97e151b80340071)
            check_type(argname="argument entries", value=entries, expected_type=type_hints["entries"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if entries is not None:
            self._values["entries"] = entries

    @builtins.property
    def entries(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntries"]]]:
        '''entries block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#entries IntegrationsAuthConfig#entries}
        '''
        result = self._values.get("entries")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntries"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParams(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.integrationsAuthConfig.IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntries",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntries:
    def __init__(
        self,
        *,
        key: typing.Optional[typing.Union["IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKey", typing.Dict[builtins.str, typing.Any]]] = None,
        value: typing.Optional[typing.Union["IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValue", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param key: key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#key IntegrationsAuthConfig#key}
        :param value: value block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#value IntegrationsAuthConfig#value}
        '''
        if isinstance(key, dict):
            key = IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKey(**key)
        if isinstance(value, dict):
            value = IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValue(**value)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8f0b92a650e5df7ec8546f4bdb8ec19e67984e78db3f3365cc050f4bffbf697)
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
    ) -> typing.Optional["IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKey"]:
        '''key block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#key IntegrationsAuthConfig#key}
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional["IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKey"], result)

    @builtins.property
    def value(
        self,
    ) -> typing.Optional["IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValue"]:
        '''value block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#value IntegrationsAuthConfig#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional["IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValue"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntries(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.integrationsAuthConfig.IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKey",
    jsii_struct_bases=[],
    name_mapping={"literal_value": "literalValue"},
)
class IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKey:
    def __init__(
        self,
        *,
        literal_value: typing.Optional[typing.Union["IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKeyLiteralValue", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param literal_value: literal_value block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#literal_value IntegrationsAuthConfig#literal_value}
        '''
        if isinstance(literal_value, dict):
            literal_value = IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKeyLiteralValue(**literal_value)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a95297e7fff9b150f69abeb303db00c0add52b9285c715d852b38a1c2f369c20)
            check_type(argname="argument literal_value", value=literal_value, expected_type=type_hints["literal_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if literal_value is not None:
            self._values["literal_value"] = literal_value

    @builtins.property
    def literal_value(
        self,
    ) -> typing.Optional["IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKeyLiteralValue"]:
        '''literal_value block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#literal_value IntegrationsAuthConfig#literal_value}
        '''
        result = self._values.get("literal_value")
        return typing.cast(typing.Optional["IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKeyLiteralValue"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.integrationsAuthConfig.IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKeyLiteralValue",
    jsii_struct_bases=[],
    name_mapping={"string_value": "stringValue"},
)
class IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKeyLiteralValue:
    def __init__(self, *, string_value: typing.Optional[builtins.str] = None) -> None:
        '''
        :param string_value: String. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#string_value IntegrationsAuthConfig#string_value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e86781a4966c307c8d1ffce82923083cc05573c5539e94eeded18acb205598da)
            check_type(argname="argument string_value", value=string_value, expected_type=type_hints["string_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if string_value is not None:
            self._values["string_value"] = string_value

    @builtins.property
    def string_value(self) -> typing.Optional[builtins.str]:
        '''String.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#string_value IntegrationsAuthConfig#string_value}
        '''
        result = self._values.get("string_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKeyLiteralValue(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKeyLiteralValueOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationsAuthConfig.IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKeyLiteralValueOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__283de9e5bd62e2d02068295b403f237e2f0313f51875fc417fc0c85cd52ed4ac)
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
            type_hints = typing.get_type_hints(_typecheckingstub__151b3baa8be5abe4ce48cc26964861f4db7282ce3ff98a88a55eef92408e35c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stringValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKeyLiteralValue]:
        return typing.cast(typing.Optional[IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKeyLiteralValue], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKeyLiteralValue],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__109a59568486904294155ccd158b2626fb7bce4cb37d97996dc99366777da95c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationsAuthConfig.IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f5074e598ef63f2b65c01f475c6000062980d0abc6e880ffa194cfb5504ad458)
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
        :param string_value: String. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#string_value IntegrationsAuthConfig#string_value}
        '''
        value = IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKeyLiteralValue(
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
    ) -> IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKeyLiteralValueOutputReference:
        return typing.cast(IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKeyLiteralValueOutputReference, jsii.get(self, "literalValue"))

    @builtins.property
    @jsii.member(jsii_name="literalValueInput")
    def literal_value_input(
        self,
    ) -> typing.Optional[IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKeyLiteralValue]:
        return typing.cast(typing.Optional[IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKeyLiteralValue], jsii.get(self, "literalValueInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKey]:
        return typing.cast(typing.Optional[IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKey], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKey],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__827d25a8ec626ddd8d42fd2afdf0ef0096def10fcc45d855d68e38ba040350ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationsAuthConfig.IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0db311ffef195997398366ec6e06ea40d9acc332130a03b0b4203b2941a88f49)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a6c889247e2acf95736095137d63c976b8ab8438fcd421a3a307fb97a56c577)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0c23f50d16587baffcec32ca90a82635ca71620f8fdbfe539164f0e8db9d559)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fcd38eca23e39316139bcd0bf5d800750a7dd2e6c640a67f815f0494316986c1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c66e4398ebd364210262397c57e1e165ee153c58cced16409bae8454ad06b46d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntries]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntries]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntries]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe3c4a023bb2bbd13b66b09322bfae5366ddf022255d66acded66c0e64d9de3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationsAuthConfig.IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ee5ee17ffa713ff81a7628fcce1089b1e8342dc0e2525c023f60e60ba428e27)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putKey")
    def put_key(
        self,
        *,
        literal_value: typing.Optional[typing.Union[IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKeyLiteralValue, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param literal_value: literal_value block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#literal_value IntegrationsAuthConfig#literal_value}
        '''
        value = IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKey(
            literal_value=literal_value
        )

        return typing.cast(None, jsii.invoke(self, "putKey", [value]))

    @jsii.member(jsii_name="putValue")
    def put_value(
        self,
        *,
        literal_value: typing.Optional[typing.Union["IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValueLiteralValue", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param literal_value: literal_value block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#literal_value IntegrationsAuthConfig#literal_value}
        '''
        value = IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValue(
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
    ) -> IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKeyOutputReference:
        return typing.cast(IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKeyOutputReference, jsii.get(self, "key"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(
        self,
    ) -> "IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValueOutputReference":
        return typing.cast("IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValueOutputReference", jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(
        self,
    ) -> typing.Optional[IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKey]:
        return typing.cast(typing.Optional[IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKey], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(
        self,
    ) -> typing.Optional["IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValue"]:
        return typing.cast(typing.Optional["IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValue"], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntries]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntries]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntries]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44ef530f218d1cae05b426bd8d1125f72adc622e73040cea02fa6387826020f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.integrationsAuthConfig.IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValue",
    jsii_struct_bases=[],
    name_mapping={"literal_value": "literalValue"},
)
class IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValue:
    def __init__(
        self,
        *,
        literal_value: typing.Optional[typing.Union["IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValueLiteralValue", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param literal_value: literal_value block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#literal_value IntegrationsAuthConfig#literal_value}
        '''
        if isinstance(literal_value, dict):
            literal_value = IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValueLiteralValue(**literal_value)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e432326510916e45906a1a9dbb54ce5752635a9379230a5b8cc492b84503892a)
            check_type(argname="argument literal_value", value=literal_value, expected_type=type_hints["literal_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if literal_value is not None:
            self._values["literal_value"] = literal_value

    @builtins.property
    def literal_value(
        self,
    ) -> typing.Optional["IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValueLiteralValue"]:
        '''literal_value block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#literal_value IntegrationsAuthConfig#literal_value}
        '''
        result = self._values.get("literal_value")
        return typing.cast(typing.Optional["IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValueLiteralValue"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValue(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.integrationsAuthConfig.IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValueLiteralValue",
    jsii_struct_bases=[],
    name_mapping={"string_value": "stringValue"},
)
class IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValueLiteralValue:
    def __init__(self, *, string_value: typing.Optional[builtins.str] = None) -> None:
        '''
        :param string_value: String. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#string_value IntegrationsAuthConfig#string_value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9b140138bae61c9cfdf8e2d48f348dea0341dafc225a6938040734d10120d93)
            check_type(argname="argument string_value", value=string_value, expected_type=type_hints["string_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if string_value is not None:
            self._values["string_value"] = string_value

    @builtins.property
    def string_value(self) -> typing.Optional[builtins.str]:
        '''String.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#string_value IntegrationsAuthConfig#string_value}
        '''
        result = self._values.get("string_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValueLiteralValue(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValueLiteralValueOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationsAuthConfig.IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValueLiteralValueOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f39de32203b9ac7089970d2f933386a08542ac5cc17a98f967e895b867c4b1a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f769b03c5a474d6342f92b773d3faf39d8f7c543e563a028b2f5bfe7a6c343e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stringValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValueLiteralValue]:
        return typing.cast(typing.Optional[IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValueLiteralValue], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValueLiteralValue],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a974d67e0635b0a03019130d165b22b4284628d47ff156ad721f846b0171652a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValueOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationsAuthConfig.IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValueOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__491b1a3ef0ad4c74f7a867038225e1a6f2b88f5a0220af9b1522937d213a4b09)
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
        :param string_value: String. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#string_value IntegrationsAuthConfig#string_value}
        '''
        value = IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValueLiteralValue(
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
    ) -> IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValueLiteralValueOutputReference:
        return typing.cast(IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValueLiteralValueOutputReference, jsii.get(self, "literalValue"))

    @builtins.property
    @jsii.member(jsii_name="literalValueInput")
    def literal_value_input(
        self,
    ) -> typing.Optional[IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValueLiteralValue]:
        return typing.cast(typing.Optional[IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValueLiteralValue], jsii.get(self, "literalValueInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValue]:
        return typing.cast(typing.Optional[IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValue], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValue],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19288eaf19290976b107e35d555fd311e7af1b46c51b52f6dd31898593af4faa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationsAuthConfig.IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca0500db84d4f3c9bee5ab42a13d115adf942ad04f806e895897cc57a2a5666c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putEntries")
    def put_entries(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntries, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55e42629ac0b177bbe20313c9c9e1ec22f17fb01d8c01a85f8fcf495f5579fc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEntries", [value]))

    @jsii.member(jsii_name="resetEntries")
    def reset_entries(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEntries", []))

    @builtins.property
    @jsii.member(jsii_name="entries")
    def entries(
        self,
    ) -> IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesList:
        return typing.cast(IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesList, jsii.get(self, "entries"))

    @builtins.property
    @jsii.member(jsii_name="entriesInput")
    def entries_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntries]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntries]]], jsii.get(self, "entriesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParams]:
        return typing.cast(typing.Optional[IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParams], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParams],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d65f79f512e415c044b0165edf0034d099b89c006396ebc90155499aef365952)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.integrationsAuthConfig.IntegrationsAuthConfigDecryptedCredentialOidcToken",
    jsii_struct_bases=[],
    name_mapping={
        "audience": "audience",
        "service_account_email": "serviceAccountEmail",
    },
)
class IntegrationsAuthConfigDecryptedCredentialOidcToken:
    def __init__(
        self,
        *,
        audience: typing.Optional[builtins.str] = None,
        service_account_email: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param audience: Audience to be used when generating OIDC token. The audience claim identifies the recipients that the JWT is intended for. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#audience IntegrationsAuthConfig#audience}
        :param service_account_email: The service account email to be used as the identity for the token. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#service_account_email IntegrationsAuthConfig#service_account_email}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7076d2577d28dc24244e438a80f313bae1e5eed6ac34c2c502cd62321579bb9)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#audience IntegrationsAuthConfig#audience}
        '''
        result = self._values.get("audience")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_account_email(self) -> typing.Optional[builtins.str]:
        '''The service account email to be used as the identity for the token.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#service_account_email IntegrationsAuthConfig#service_account_email}
        '''
        result = self._values.get("service_account_email")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationsAuthConfigDecryptedCredentialOidcToken(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IntegrationsAuthConfigDecryptedCredentialOidcTokenOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationsAuthConfig.IntegrationsAuthConfigDecryptedCredentialOidcTokenOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e65f8683b49abe53aed751a0c7a25b11ac1e665683d6a533047e51e3efa220b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b989e02d10bf59e4fae87504ab8f98ed5e6eaa072c92509dd499c6ce220bfea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "audience", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccountEmail")
    def service_account_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccountEmail"))

    @service_account_email.setter
    def service_account_email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__632b97945e73e0029a0bee23b4a132bd3f1c4d655b174960a2a52465ea6ca7eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccountEmail", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IntegrationsAuthConfigDecryptedCredentialOidcToken]:
        return typing.cast(typing.Optional[IntegrationsAuthConfigDecryptedCredentialOidcToken], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IntegrationsAuthConfigDecryptedCredentialOidcToken],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4bf4d44c2aa45f7d10c40dc5a6b8ed73b3f522d6e227cca20b0ef3b40adef1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IntegrationsAuthConfigDecryptedCredentialOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationsAuthConfig.IntegrationsAuthConfigDecryptedCredentialOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9a14d19dfbb2ab8ad9174fd275f179f397f21141035e0b23b2a89b3ece058b11)
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
        :param token: The token for the auth type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#token IntegrationsAuthConfig#token}
        :param type: Authentication type, e.g. "Basic", "Bearer", etc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#type IntegrationsAuthConfig#type}
        '''
        value = IntegrationsAuthConfigDecryptedCredentialAuthToken(
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
        :param jwt_header: Identifies which algorithm is used to generate the signature. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#jwt_header IntegrationsAuthConfig#jwt_header}
        :param jwt_payload: Contains a set of claims. The JWT specification defines seven Registered Claim Names which are the standard fields commonly included in tokens. Custom claims are usually also included, depending on the purpose of the token. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#jwt_payload IntegrationsAuthConfig#jwt_payload}
        :param secret: User's pre-shared secret to sign the token. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#secret IntegrationsAuthConfig#secret}
        '''
        value = IntegrationsAuthConfigDecryptedCredentialJwt(
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
        :param auth_endpoint: The auth url endpoint to send the auth code request to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#auth_endpoint IntegrationsAuthConfig#auth_endpoint}
        :param client_id: The client's id. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#client_id IntegrationsAuthConfig#client_id}
        :param client_secret: The client's secret. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#client_secret IntegrationsAuthConfig#client_secret}
        :param scope: A space-delimited list of requested scope permissions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#scope IntegrationsAuthConfig#scope}
        :param token_endpoint: The token url endpoint to send the token request to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#token_endpoint IntegrationsAuthConfig#token_endpoint}
        '''
        value = IntegrationsAuthConfigDecryptedCredentialOauth2AuthorizationCode(
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
        token_params: typing.Optional[typing.Union[IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParams, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param client_id: The client's ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#client_id IntegrationsAuthConfig#client_id}
        :param client_secret: The client's secret. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#client_secret IntegrationsAuthConfig#client_secret}
        :param request_type: Represent how to pass parameters to fetch access token Possible values: ["REQUEST_TYPE_UNSPECIFIED", "REQUEST_BODY", "QUERY_PARAMETERS", "ENCODED_HEADER"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#request_type IntegrationsAuthConfig#request_type}
        :param scope: A space-delimited list of requested scope permissions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#scope IntegrationsAuthConfig#scope}
        :param token_endpoint: The token endpoint is used by the client to obtain an access token by presenting its authorization grant or refresh token. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#token_endpoint IntegrationsAuthConfig#token_endpoint}
        :param token_params: token_params block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#token_params IntegrationsAuthConfig#token_params}
        '''
        value = IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentials(
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
        :param audience: Audience to be used when generating OIDC token. The audience claim identifies the recipients that the JWT is intended for. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#audience IntegrationsAuthConfig#audience}
        :param service_account_email: The service account email to be used as the identity for the token. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#service_account_email IntegrationsAuthConfig#service_account_email}
        '''
        value = IntegrationsAuthConfigDecryptedCredentialOidcToken(
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
        :param scope: A space-delimited list of requested scope permissions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#scope IntegrationsAuthConfig#scope}
        :param service_account: Name of the service account that has the permission to make the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#service_account IntegrationsAuthConfig#service_account}
        '''
        value = IntegrationsAuthConfigDecryptedCredentialServiceAccountCredentials(
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
        :param password: Password to be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#password IntegrationsAuthConfig#password}
        :param username: Username to be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#username IntegrationsAuthConfig#username}
        '''
        value = IntegrationsAuthConfigDecryptedCredentialUsernameAndPassword(
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
    ) -> IntegrationsAuthConfigDecryptedCredentialAuthTokenOutputReference:
        return typing.cast(IntegrationsAuthConfigDecryptedCredentialAuthTokenOutputReference, jsii.get(self, "authToken"))

    @builtins.property
    @jsii.member(jsii_name="jwt")
    def jwt(self) -> IntegrationsAuthConfigDecryptedCredentialJwtOutputReference:
        return typing.cast(IntegrationsAuthConfigDecryptedCredentialJwtOutputReference, jsii.get(self, "jwt"))

    @builtins.property
    @jsii.member(jsii_name="oauth2AuthorizationCode")
    def oauth2_authorization_code(
        self,
    ) -> IntegrationsAuthConfigDecryptedCredentialOauth2AuthorizationCodeOutputReference:
        return typing.cast(IntegrationsAuthConfigDecryptedCredentialOauth2AuthorizationCodeOutputReference, jsii.get(self, "oauth2AuthorizationCode"))

    @builtins.property
    @jsii.member(jsii_name="oauth2ClientCredentials")
    def oauth2_client_credentials(
        self,
    ) -> IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsOutputReference:
        return typing.cast(IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsOutputReference, jsii.get(self, "oauth2ClientCredentials"))

    @builtins.property
    @jsii.member(jsii_name="oidcToken")
    def oidc_token(
        self,
    ) -> IntegrationsAuthConfigDecryptedCredentialOidcTokenOutputReference:
        return typing.cast(IntegrationsAuthConfigDecryptedCredentialOidcTokenOutputReference, jsii.get(self, "oidcToken"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountCredentials")
    def service_account_credentials(
        self,
    ) -> "IntegrationsAuthConfigDecryptedCredentialServiceAccountCredentialsOutputReference":
        return typing.cast("IntegrationsAuthConfigDecryptedCredentialServiceAccountCredentialsOutputReference", jsii.get(self, "serviceAccountCredentials"))

    @builtins.property
    @jsii.member(jsii_name="usernameAndPassword")
    def username_and_password(
        self,
    ) -> "IntegrationsAuthConfigDecryptedCredentialUsernameAndPasswordOutputReference":
        return typing.cast("IntegrationsAuthConfigDecryptedCredentialUsernameAndPasswordOutputReference", jsii.get(self, "usernameAndPassword"))

    @builtins.property
    @jsii.member(jsii_name="authTokenInput")
    def auth_token_input(
        self,
    ) -> typing.Optional[IntegrationsAuthConfigDecryptedCredentialAuthToken]:
        return typing.cast(typing.Optional[IntegrationsAuthConfigDecryptedCredentialAuthToken], jsii.get(self, "authTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="credentialTypeInput")
    def credential_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "credentialTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="jwtInput")
    def jwt_input(
        self,
    ) -> typing.Optional[IntegrationsAuthConfigDecryptedCredentialJwt]:
        return typing.cast(typing.Optional[IntegrationsAuthConfigDecryptedCredentialJwt], jsii.get(self, "jwtInput"))

    @builtins.property
    @jsii.member(jsii_name="oauth2AuthorizationCodeInput")
    def oauth2_authorization_code_input(
        self,
    ) -> typing.Optional[IntegrationsAuthConfigDecryptedCredentialOauth2AuthorizationCode]:
        return typing.cast(typing.Optional[IntegrationsAuthConfigDecryptedCredentialOauth2AuthorizationCode], jsii.get(self, "oauth2AuthorizationCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="oauth2ClientCredentialsInput")
    def oauth2_client_credentials_input(
        self,
    ) -> typing.Optional[IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentials]:
        return typing.cast(typing.Optional[IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentials], jsii.get(self, "oauth2ClientCredentialsInput"))

    @builtins.property
    @jsii.member(jsii_name="oidcTokenInput")
    def oidc_token_input(
        self,
    ) -> typing.Optional[IntegrationsAuthConfigDecryptedCredentialOidcToken]:
        return typing.cast(typing.Optional[IntegrationsAuthConfigDecryptedCredentialOidcToken], jsii.get(self, "oidcTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountCredentialsInput")
    def service_account_credentials_input(
        self,
    ) -> typing.Optional["IntegrationsAuthConfigDecryptedCredentialServiceAccountCredentials"]:
        return typing.cast(typing.Optional["IntegrationsAuthConfigDecryptedCredentialServiceAccountCredentials"], jsii.get(self, "serviceAccountCredentialsInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameAndPasswordInput")
    def username_and_password_input(
        self,
    ) -> typing.Optional["IntegrationsAuthConfigDecryptedCredentialUsernameAndPassword"]:
        return typing.cast(typing.Optional["IntegrationsAuthConfigDecryptedCredentialUsernameAndPassword"], jsii.get(self, "usernameAndPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="credentialType")
    def credential_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "credentialType"))

    @credential_type.setter
    def credential_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4461b5e609000cb95c46acc9b5fadd9b570a7b61a3bd598ce3bb7aff08dd230c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "credentialType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IntegrationsAuthConfigDecryptedCredential]:
        return typing.cast(typing.Optional[IntegrationsAuthConfigDecryptedCredential], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IntegrationsAuthConfigDecryptedCredential],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__836b526f236a8807138883e256df233790d4281359600aca67b50f9e427c3c56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.integrationsAuthConfig.IntegrationsAuthConfigDecryptedCredentialServiceAccountCredentials",
    jsii_struct_bases=[],
    name_mapping={"scope": "scope", "service_account": "serviceAccount"},
)
class IntegrationsAuthConfigDecryptedCredentialServiceAccountCredentials:
    def __init__(
        self,
        *,
        scope: typing.Optional[builtins.str] = None,
        service_account: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: A space-delimited list of requested scope permissions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#scope IntegrationsAuthConfig#scope}
        :param service_account: Name of the service account that has the permission to make the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#service_account IntegrationsAuthConfig#service_account}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b646ff8d4bbc2c533b3adc5e404beba388df1173f86a02e7f370c5cacefec90e)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#scope IntegrationsAuthConfig#scope}
        '''
        result = self._values.get("scope")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_account(self) -> typing.Optional[builtins.str]:
        '''Name of the service account that has the permission to make the request.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#service_account IntegrationsAuthConfig#service_account}
        '''
        result = self._values.get("service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationsAuthConfigDecryptedCredentialServiceAccountCredentials(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IntegrationsAuthConfigDecryptedCredentialServiceAccountCredentialsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationsAuthConfig.IntegrationsAuthConfigDecryptedCredentialServiceAccountCredentialsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5af54dd616e9d5ea8ca8b4f08ae4d16764e83b8c757fc0089f7aef5c8078a6c6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ec39e9493a51dcf621b009ff084fb124bd9ca68020aecf36af371f5f05a4c31c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scope", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccount")
    def service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccount"))

    @service_account.setter
    def service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8c776f1f633db97e157654ae08a9719d838b71bb652603e84339e75722762b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IntegrationsAuthConfigDecryptedCredentialServiceAccountCredentials]:
        return typing.cast(typing.Optional[IntegrationsAuthConfigDecryptedCredentialServiceAccountCredentials], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IntegrationsAuthConfigDecryptedCredentialServiceAccountCredentials],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f6898a7f5060fc852357c119c0b1197e6fe727fb649c291fd5a34e24408a2c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.integrationsAuthConfig.IntegrationsAuthConfigDecryptedCredentialUsernameAndPassword",
    jsii_struct_bases=[],
    name_mapping={"password": "password", "username": "username"},
)
class IntegrationsAuthConfigDecryptedCredentialUsernameAndPassword:
    def __init__(
        self,
        *,
        password: typing.Optional[builtins.str] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param password: Password to be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#password IntegrationsAuthConfig#password}
        :param username: Username to be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#username IntegrationsAuthConfig#username}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c701dc89a8ea1ed564b06e3f32821443ca63fd69aacd284cb09774bc8b5d0b35)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#password IntegrationsAuthConfig#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''Username to be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#username IntegrationsAuthConfig#username}
        '''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationsAuthConfigDecryptedCredentialUsernameAndPassword(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IntegrationsAuthConfigDecryptedCredentialUsernameAndPasswordOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationsAuthConfig.IntegrationsAuthConfigDecryptedCredentialUsernameAndPasswordOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b619c040156b991781aba54675a36b938a2d0f235cfcb2d1922cbdb05206c13)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5afd749caf418a7230db0c7adb7887d3c498082abce60e8bd81d16fe0eaddab5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9bcc43fd06ae172c9a26a8f6525b0b9c6d3c5e51cbf749923417d6b7d9618ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IntegrationsAuthConfigDecryptedCredentialUsernameAndPassword]:
        return typing.cast(typing.Optional[IntegrationsAuthConfigDecryptedCredentialUsernameAndPassword], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IntegrationsAuthConfigDecryptedCredentialUsernameAndPassword],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64f925ce1d4801e3c9711df56584841ecd9e649d8fa659041faee1c7ecdb129c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.integrationsAuthConfig.IntegrationsAuthConfigTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class IntegrationsAuthConfigTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#create IntegrationsAuthConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#delete IntegrationsAuthConfig#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#update IntegrationsAuthConfig#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d0cf6e17d497014fdb03920ff9169dbe500184a9573b01139926b93b0982d66)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#create IntegrationsAuthConfig#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#delete IntegrationsAuthConfig#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integrations_auth_config#update IntegrationsAuthConfig#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationsAuthConfigTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IntegrationsAuthConfigTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationsAuthConfig.IntegrationsAuthConfigTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fecd5f923ec4bd6e985b210ff1472b908ee2f38638a459cc7bb50c83d0ce06f0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4b18dc4ca8fcb2290cf0d100eae2d611393f85a54e1dc6b118855a670a5bea28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f02842f1142c8bcfc0ae447ef27ceaa544ddbfb1f35e2348337d93cbf423fb96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdc3c2ed18acfd6e943fa16b8bbcbbcda3f94992d4c86346ecf917c67e20ee9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationsAuthConfigTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationsAuthConfigTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationsAuthConfigTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__035d0994e4d37c2a20b93e8ea02d29282101db4587232913f382c427295594a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "IntegrationsAuthConfig",
    "IntegrationsAuthConfigClientCertificate",
    "IntegrationsAuthConfigClientCertificateOutputReference",
    "IntegrationsAuthConfigConfig",
    "IntegrationsAuthConfigDecryptedCredential",
    "IntegrationsAuthConfigDecryptedCredentialAuthToken",
    "IntegrationsAuthConfigDecryptedCredentialAuthTokenOutputReference",
    "IntegrationsAuthConfigDecryptedCredentialJwt",
    "IntegrationsAuthConfigDecryptedCredentialJwtOutputReference",
    "IntegrationsAuthConfigDecryptedCredentialOauth2AuthorizationCode",
    "IntegrationsAuthConfigDecryptedCredentialOauth2AuthorizationCodeOutputReference",
    "IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentials",
    "IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsOutputReference",
    "IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParams",
    "IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntries",
    "IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKey",
    "IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKeyLiteralValue",
    "IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKeyLiteralValueOutputReference",
    "IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKeyOutputReference",
    "IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesList",
    "IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesOutputReference",
    "IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValue",
    "IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValueLiteralValue",
    "IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValueLiteralValueOutputReference",
    "IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValueOutputReference",
    "IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsOutputReference",
    "IntegrationsAuthConfigDecryptedCredentialOidcToken",
    "IntegrationsAuthConfigDecryptedCredentialOidcTokenOutputReference",
    "IntegrationsAuthConfigDecryptedCredentialOutputReference",
    "IntegrationsAuthConfigDecryptedCredentialServiceAccountCredentials",
    "IntegrationsAuthConfigDecryptedCredentialServiceAccountCredentialsOutputReference",
    "IntegrationsAuthConfigDecryptedCredentialUsernameAndPassword",
    "IntegrationsAuthConfigDecryptedCredentialUsernameAndPasswordOutputReference",
    "IntegrationsAuthConfigTimeouts",
    "IntegrationsAuthConfigTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__28ed39353b561ecfa8fc0a2be3fc95df3f8b11c3e11c38f10c280bb07c7d8ede(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    display_name: builtins.str,
    location: builtins.str,
    client_certificate: typing.Optional[typing.Union[IntegrationsAuthConfigClientCertificate, typing.Dict[builtins.str, typing.Any]]] = None,
    decrypted_credential: typing.Optional[typing.Union[IntegrationsAuthConfigDecryptedCredential, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    expiry_notification_duration: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    override_valid_time: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[IntegrationsAuthConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__3eb249671825395261449354ebed9f615840f032093efa3438c66a64ec61254e(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65c49c9277c122dd50be540e0f6f63954515029eb1d10433960db9cf299fdf55(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92bbd80c7071182a8e9061820fc1eb03b501fcefecf952e94f49f7afc04bb89c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f808a81dd6a120741209838b211dff22123b72d841ee2163a212835c494967d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a91ace91979df34161728719263c6393cb4335599cfe20b98145e9fd5217321c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__373fc424f5cca567efa5a8835bec1bf000995f5b2a6dcac90c61d5fe47152426(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__862e704e1d6fd1a5645d3f51a77ded265f9379effbfa5c4fab7c1ca7d1436b9f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c5639d5eac9a866ad3c820f6196f9e19cfb57d861f235c44bf1206503797576(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e10bc03df390f630edb24b91622bfa29c440796acd31d2d05979a63a89e7acb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__248680474fffa63e8f19838f9b307a7879c89b440a800452d4d638e8e0060467(
    *,
    encrypted_private_key: builtins.str,
    ssl_certificate: builtins.str,
    passphrase: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71b9be5f31bb30b69cba0c4ba2b1d2e7f287c1f8b392041703775bc141ceabc8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fec6beee0e8a30b4a2110d2b5755bede4169626d515f4f62e4c1345e52319489(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96378f8ff680a73761faf05f48ecb2bf28735b523d2d28af691fc82040edb419(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a0b1e5d9fd1e3eb7a3ccf6bc89f91d0963085fd42924ab6ac021ef81afdb990(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__069ffbe7173a6ee752a00cefaea07ddb66f94b105cf5de173f3433fde9ee6dca(
    value: typing.Optional[IntegrationsAuthConfigClientCertificate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7435c5bc656395708ad11f02d10e8989a819cddb8fb792bef125a33722f3b9c(
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
    client_certificate: typing.Optional[typing.Union[IntegrationsAuthConfigClientCertificate, typing.Dict[builtins.str, typing.Any]]] = None,
    decrypted_credential: typing.Optional[typing.Union[IntegrationsAuthConfigDecryptedCredential, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    expiry_notification_duration: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    override_valid_time: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[IntegrationsAuthConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    visibility: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb05d451c636faa302295efff29827897186a33f627c1bb8da629482f4047e87(
    *,
    credential_type: builtins.str,
    auth_token: typing.Optional[typing.Union[IntegrationsAuthConfigDecryptedCredentialAuthToken, typing.Dict[builtins.str, typing.Any]]] = None,
    jwt: typing.Optional[typing.Union[IntegrationsAuthConfigDecryptedCredentialJwt, typing.Dict[builtins.str, typing.Any]]] = None,
    oauth2_authorization_code: typing.Optional[typing.Union[IntegrationsAuthConfigDecryptedCredentialOauth2AuthorizationCode, typing.Dict[builtins.str, typing.Any]]] = None,
    oauth2_client_credentials: typing.Optional[typing.Union[IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentials, typing.Dict[builtins.str, typing.Any]]] = None,
    oidc_token: typing.Optional[typing.Union[IntegrationsAuthConfigDecryptedCredentialOidcToken, typing.Dict[builtins.str, typing.Any]]] = None,
    service_account_credentials: typing.Optional[typing.Union[IntegrationsAuthConfigDecryptedCredentialServiceAccountCredentials, typing.Dict[builtins.str, typing.Any]]] = None,
    username_and_password: typing.Optional[typing.Union[IntegrationsAuthConfigDecryptedCredentialUsernameAndPassword, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2f61513080a0e244dc01995e9289d720a0f1abbeba8661c340a8075d17d103d(
    *,
    token: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dd1b9e9fa5c6fbe773b1d6e7ed710ec7deba2102d5f7b4e4c21063627171e7c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fad78495f3c9a29d8a80251330beed1ef2bc773ec00c4e94d75937f28c283486(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e9e729340b065690fbb031a1a529be11694cce66528abb2b1d9afe453ccf5fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3de29e87965fd59860024749453517ee13ff1faf7750053cf554c69512a51482(
    value: typing.Optional[IntegrationsAuthConfigDecryptedCredentialAuthToken],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38133aed2ea7b86196ac43a9d1f6739001edcfa58838e8bc05e3ab38a9d65bcd(
    *,
    jwt_header: typing.Optional[builtins.str] = None,
    jwt_payload: typing.Optional[builtins.str] = None,
    secret: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c20108819c50f48f449c380f23692cfea937068a6616587afdd3100f55cc75b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50ba7422a7f6ab7f6255cf83ed8cbb0933242fde3e0af82691ff37754254842e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__172491dbf1078d56323ef90512e406976532ce7020b48594f44e9a3269446bd0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9aaf25ced1da9b598a7e681798b1b5928cdfd9d076977a11b71bee18e19e29f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad9dc1b9fae688bfcee7ebe8a469fdc63638b7eaa6529884202cdbe5b7dd2978(
    value: typing.Optional[IntegrationsAuthConfigDecryptedCredentialJwt],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49d1f66bf32763276acd3475c3980eaca2d5734f5fef9d49e89961076f9b6287(
    *,
    auth_endpoint: typing.Optional[builtins.str] = None,
    client_id: typing.Optional[builtins.str] = None,
    client_secret: typing.Optional[builtins.str] = None,
    scope: typing.Optional[builtins.str] = None,
    token_endpoint: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b57634cbe0a61b2e93455318009ca5e44f421e1f1f228cf390ecb480f1e771f4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63bffb7c4fd24e1ce2461d72d5a0c13aae4c68c66c50b57260b6d1ac9997b705(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bdbf5c7c3b8dbe9167611972272769aa8704113de2c140cd6b340f2537e7c8b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f82790551d75317b330a59f2cfdada3901c4e8ee72779b9e4f08df91db1ce312(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fe3fcd1a2fbddda0b80fe5dc4764399ec2357eea72ccbc3153eecee2443e05a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d15ecf6a144e1a6af6da0a3074e43435b499a0b95c15e5ff1b68c77a778f7ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6971457eb0f7c16da7def5af6fe17dbe4b37f75265707bd88822a848dbaa81a2(
    value: typing.Optional[IntegrationsAuthConfigDecryptedCredentialOauth2AuthorizationCode],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efbd34ac407d93931eee7208351bbda118347e1b26342520fd068482a620d76f(
    *,
    client_id: typing.Optional[builtins.str] = None,
    client_secret: typing.Optional[builtins.str] = None,
    request_type: typing.Optional[builtins.str] = None,
    scope: typing.Optional[builtins.str] = None,
    token_endpoint: typing.Optional[builtins.str] = None,
    token_params: typing.Optional[typing.Union[IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParams, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78fed2e6c75682cf5cb493cc2a14b4cbfb2874eb5e67378f25f6895015d0271b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e634dcae61ddb6e393cfe886376c9c43d3c27467e671d9c1b7f239c68f3426f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65d13a76360704cfb1f9fe399c0ad33fa4e2a0f20db6617041f714cbc655d5eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4747e61f0df4773b907bbaecb83f51aa74f234f567843d5d260513e30dbdd98f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0097046a834a56fa3a957b4da83e32023d9376511257c00b501dd256726be956(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e64955aea03a2b47eb00c479ad9c9761ff025fdb3fa88ad9c5f9dff664b08a14(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6782ba0cd11f5695e66379d9567a747d5e8e4a04af8bcbabd50fe1e390903dd1(
    value: typing.Optional[IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentials],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f19c7bfcd27473c135ddc867744e22c63c3966379cc4930ce97e151b80340071(
    *,
    entries: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntries, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8f0b92a650e5df7ec8546f4bdb8ec19e67984e78db3f3365cc050f4bffbf697(
    *,
    key: typing.Optional[typing.Union[IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKey, typing.Dict[builtins.str, typing.Any]]] = None,
    value: typing.Optional[typing.Union[IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValue, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a95297e7fff9b150f69abeb303db00c0add52b9285c715d852b38a1c2f369c20(
    *,
    literal_value: typing.Optional[typing.Union[IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKeyLiteralValue, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e86781a4966c307c8d1ffce82923083cc05573c5539e94eeded18acb205598da(
    *,
    string_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__283de9e5bd62e2d02068295b403f237e2f0313f51875fc417fc0c85cd52ed4ac(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__151b3baa8be5abe4ce48cc26964861f4db7282ce3ff98a88a55eef92408e35c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__109a59568486904294155ccd158b2626fb7bce4cb37d97996dc99366777da95c(
    value: typing.Optional[IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKeyLiteralValue],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5074e598ef63f2b65c01f475c6000062980d0abc6e880ffa194cfb5504ad458(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__827d25a8ec626ddd8d42fd2afdf0ef0096def10fcc45d855d68e38ba040350ea(
    value: typing.Optional[IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesKey],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0db311ffef195997398366ec6e06ea40d9acc332130a03b0b4203b2941a88f49(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a6c889247e2acf95736095137d63c976b8ab8438fcd421a3a307fb97a56c577(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0c23f50d16587baffcec32ca90a82635ca71620f8fdbfe539164f0e8db9d559(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcd38eca23e39316139bcd0bf5d800750a7dd2e6c640a67f815f0494316986c1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c66e4398ebd364210262397c57e1e165ee153c58cced16409bae8454ad06b46d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe3c4a023bb2bbd13b66b09322bfae5366ddf022255d66acded66c0e64d9de3c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntries]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ee5ee17ffa713ff81a7628fcce1089b1e8342dc0e2525c023f60e60ba428e27(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44ef530f218d1cae05b426bd8d1125f72adc622e73040cea02fa6387826020f8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntries]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e432326510916e45906a1a9dbb54ce5752635a9379230a5b8cc492b84503892a(
    *,
    literal_value: typing.Optional[typing.Union[IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValueLiteralValue, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9b140138bae61c9cfdf8e2d48f348dea0341dafc225a6938040734d10120d93(
    *,
    string_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f39de32203b9ac7089970d2f933386a08542ac5cc17a98f967e895b867c4b1a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f769b03c5a474d6342f92b773d3faf39d8f7c543e563a028b2f5bfe7a6c343e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a974d67e0635b0a03019130d165b22b4284628d47ff156ad721f846b0171652a(
    value: typing.Optional[IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValueLiteralValue],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__491b1a3ef0ad4c74f7a867038225e1a6f2b88f5a0220af9b1522937d213a4b09(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19288eaf19290976b107e35d555fd311e7af1b46c51b52f6dd31898593af4faa(
    value: typing.Optional[IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntriesValue],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca0500db84d4f3c9bee5ab42a13d115adf942ad04f806e895897cc57a2a5666c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55e42629ac0b177bbe20313c9c9e1ec22f17fb01d8c01a85f8fcf495f5579fc0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParamsEntries, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d65f79f512e415c044b0165edf0034d099b89c006396ebc90155499aef365952(
    value: typing.Optional[IntegrationsAuthConfigDecryptedCredentialOauth2ClientCredentialsTokenParams],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7076d2577d28dc24244e438a80f313bae1e5eed6ac34c2c502cd62321579bb9(
    *,
    audience: typing.Optional[builtins.str] = None,
    service_account_email: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e65f8683b49abe53aed751a0c7a25b11ac1e665683d6a533047e51e3efa220b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b989e02d10bf59e4fae87504ab8f98ed5e6eaa072c92509dd499c6ce220bfea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__632b97945e73e0029a0bee23b4a132bd3f1c4d655b174960a2a52465ea6ca7eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4bf4d44c2aa45f7d10c40dc5a6b8ed73b3f522d6e227cca20b0ef3b40adef1f(
    value: typing.Optional[IntegrationsAuthConfigDecryptedCredentialOidcToken],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a14d19dfbb2ab8ad9174fd275f179f397f21141035e0b23b2a89b3ece058b11(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4461b5e609000cb95c46acc9b5fadd9b570a7b61a3bd598ce3bb7aff08dd230c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__836b526f236a8807138883e256df233790d4281359600aca67b50f9e427c3c56(
    value: typing.Optional[IntegrationsAuthConfigDecryptedCredential],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b646ff8d4bbc2c533b3adc5e404beba388df1173f86a02e7f370c5cacefec90e(
    *,
    scope: typing.Optional[builtins.str] = None,
    service_account: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5af54dd616e9d5ea8ca8b4f08ae4d16764e83b8c757fc0089f7aef5c8078a6c6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec39e9493a51dcf621b009ff084fb124bd9ca68020aecf36af371f5f05a4c31c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8c776f1f633db97e157654ae08a9719d838b71bb652603e84339e75722762b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f6898a7f5060fc852357c119c0b1197e6fe727fb649c291fd5a34e24408a2c6(
    value: typing.Optional[IntegrationsAuthConfigDecryptedCredentialServiceAccountCredentials],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c701dc89a8ea1ed564b06e3f32821443ca63fd69aacd284cb09774bc8b5d0b35(
    *,
    password: typing.Optional[builtins.str] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b619c040156b991781aba54675a36b938a2d0f235cfcb2d1922cbdb05206c13(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5afd749caf418a7230db0c7adb7887d3c498082abce60e8bd81d16fe0eaddab5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9bcc43fd06ae172c9a26a8f6525b0b9c6d3c5e51cbf749923417d6b7d9618ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64f925ce1d4801e3c9711df56584841ecd9e649d8fa659041faee1c7ecdb129c(
    value: typing.Optional[IntegrationsAuthConfigDecryptedCredentialUsernameAndPassword],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d0cf6e17d497014fdb03920ff9169dbe500184a9573b01139926b93b0982d66(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fecd5f923ec4bd6e985b210ff1472b908ee2f38638a459cc7bb50c83d0ce06f0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b18dc4ca8fcb2290cf0d100eae2d611393f85a54e1dc6b118855a670a5bea28(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f02842f1142c8bcfc0ae447ef27ceaa544ddbfb1f35e2348337d93cbf423fb96(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdc3c2ed18acfd6e943fa16b8bbcbbcda3f94992d4c86346ecf917c67e20ee9d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__035d0994e4d37c2a20b93e8ea02d29282101db4587232913f382c427295594a1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationsAuthConfigTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
