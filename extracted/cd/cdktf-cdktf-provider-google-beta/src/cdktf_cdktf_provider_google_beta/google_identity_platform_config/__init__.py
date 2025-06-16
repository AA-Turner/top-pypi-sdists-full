r'''
# `google_identity_platform_config`

Refer to the Terraform Registry for docs: [`google_identity_platform_config`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config).
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


class GoogleIdentityPlatformConfig(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformConfig.GoogleIdentityPlatformConfig",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config google_identity_platform_config}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        authorized_domains: typing.Optional[typing.Sequence[builtins.str]] = None,
        autodelete_anonymous_users: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        blocking_functions: typing.Optional[typing.Union["GoogleIdentityPlatformConfigBlockingFunctions", typing.Dict[builtins.str, typing.Any]]] = None,
        client: typing.Optional[typing.Union["GoogleIdentityPlatformConfigClient", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        mfa: typing.Optional[typing.Union["GoogleIdentityPlatformConfigMfa", typing.Dict[builtins.str, typing.Any]]] = None,
        monitoring: typing.Optional[typing.Union["GoogleIdentityPlatformConfigMonitoring", typing.Dict[builtins.str, typing.Any]]] = None,
        multi_tenant: typing.Optional[typing.Union["GoogleIdentityPlatformConfigMultiTenant", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        quota: typing.Optional[typing.Union["GoogleIdentityPlatformConfigQuota", typing.Dict[builtins.str, typing.Any]]] = None,
        sign_in: typing.Optional[typing.Union["GoogleIdentityPlatformConfigSignIn", typing.Dict[builtins.str, typing.Any]]] = None,
        sms_region_config: typing.Optional[typing.Union["GoogleIdentityPlatformConfigSmsRegionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleIdentityPlatformConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config google_identity_platform_config} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param authorized_domains: List of domains authorized for OAuth redirects. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#authorized_domains GoogleIdentityPlatformConfig#authorized_domains}
        :param autodelete_anonymous_users: Whether anonymous users will be auto-deleted after a period of 30 days. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#autodelete_anonymous_users GoogleIdentityPlatformConfig#autodelete_anonymous_users}
        :param blocking_functions: blocking_functions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#blocking_functions GoogleIdentityPlatformConfig#blocking_functions}
        :param client: client block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#client GoogleIdentityPlatformConfig#client}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#id GoogleIdentityPlatformConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param mfa: mfa block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#mfa GoogleIdentityPlatformConfig#mfa}
        :param monitoring: monitoring block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#monitoring GoogleIdentityPlatformConfig#monitoring}
        :param multi_tenant: multi_tenant block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#multi_tenant GoogleIdentityPlatformConfig#multi_tenant}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#project GoogleIdentityPlatformConfig#project}.
        :param quota: quota block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#quota GoogleIdentityPlatformConfig#quota}
        :param sign_in: sign_in block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#sign_in GoogleIdentityPlatformConfig#sign_in}
        :param sms_region_config: sms_region_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#sms_region_config GoogleIdentityPlatformConfig#sms_region_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#timeouts GoogleIdentityPlatformConfig#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4312f084d832f9f93da5084069dfe91ece481d88685ba5f9e10c685b42a70ba0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleIdentityPlatformConfigConfig(
            authorized_domains=authorized_domains,
            autodelete_anonymous_users=autodelete_anonymous_users,
            blocking_functions=blocking_functions,
            client=client,
            id=id,
            mfa=mfa,
            monitoring=monitoring,
            multi_tenant=multi_tenant,
            project=project,
            quota=quota,
            sign_in=sign_in,
            sms_region_config=sms_region_config,
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
        '''Generates CDKTF code for importing a GoogleIdentityPlatformConfig resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleIdentityPlatformConfig to import.
        :param import_from_id: The id of the existing GoogleIdentityPlatformConfig that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleIdentityPlatformConfig to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba032ddfdd5ffe37128d34032eaee2af1806089a183b36cfdc4e10837c951556)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putBlockingFunctions")
    def put_blocking_functions(
        self,
        *,
        triggers: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleIdentityPlatformConfigBlockingFunctionsTriggers", typing.Dict[builtins.str, typing.Any]]]],
        forward_inbound_credentials: typing.Optional[typing.Union["GoogleIdentityPlatformConfigBlockingFunctionsForwardInboundCredentials", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param triggers: triggers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#triggers GoogleIdentityPlatformConfig#triggers}
        :param forward_inbound_credentials: forward_inbound_credentials block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#forward_inbound_credentials GoogleIdentityPlatformConfig#forward_inbound_credentials}
        '''
        value = GoogleIdentityPlatformConfigBlockingFunctions(
            triggers=triggers, forward_inbound_credentials=forward_inbound_credentials
        )

        return typing.cast(None, jsii.invoke(self, "putBlockingFunctions", [value]))

    @jsii.member(jsii_name="putClient")
    def put_client(
        self,
        *,
        permissions: typing.Optional[typing.Union["GoogleIdentityPlatformConfigClientPermissions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param permissions: permissions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#permissions GoogleIdentityPlatformConfig#permissions}
        '''
        value = GoogleIdentityPlatformConfigClient(permissions=permissions)

        return typing.cast(None, jsii.invoke(self, "putClient", [value]))

    @jsii.member(jsii_name="putMfa")
    def put_mfa(
        self,
        *,
        enabled_providers: typing.Optional[typing.Sequence[builtins.str]] = None,
        provider_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleIdentityPlatformConfigMfaProviderConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        state: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled_providers: A list of usable second factors for this project. Possible values: ["PHONE_SMS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#enabled_providers GoogleIdentityPlatformConfig#enabled_providers}
        :param provider_configs: provider_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#provider_configs GoogleIdentityPlatformConfig#provider_configs}
        :param state: Whether MultiFactor Authentication has been enabled for this project. Possible values: ["DISABLED", "ENABLED", "MANDATORY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#state GoogleIdentityPlatformConfig#state}
        '''
        value = GoogleIdentityPlatformConfigMfa(
            enabled_providers=enabled_providers,
            provider_configs=provider_configs,
            state=state,
        )

        return typing.cast(None, jsii.invoke(self, "putMfa", [value]))

    @jsii.member(jsii_name="putMonitoring")
    def put_monitoring(
        self,
        *,
        request_logging: typing.Optional[typing.Union["GoogleIdentityPlatformConfigMonitoringRequestLogging", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param request_logging: request_logging block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#request_logging GoogleIdentityPlatformConfig#request_logging}
        '''
        value = GoogleIdentityPlatformConfigMonitoring(request_logging=request_logging)

        return typing.cast(None, jsii.invoke(self, "putMonitoring", [value]))

    @jsii.member(jsii_name="putMultiTenant")
    def put_multi_tenant(
        self,
        *,
        allow_tenants: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        default_tenant_location: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allow_tenants: Whether this project can have tenants or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#allow_tenants GoogleIdentityPlatformConfig#allow_tenants}
        :param default_tenant_location: The default cloud parent org or folder that the tenant project should be created under. The parent resource name should be in the format of "/", such as "folders/123" or "organizations/456". If the value is not set, the tenant will be created under the same organization or folder as the agent project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#default_tenant_location GoogleIdentityPlatformConfig#default_tenant_location}
        '''
        value = GoogleIdentityPlatformConfigMultiTenant(
            allow_tenants=allow_tenants,
            default_tenant_location=default_tenant_location,
        )

        return typing.cast(None, jsii.invoke(self, "putMultiTenant", [value]))

    @jsii.member(jsii_name="putQuota")
    def put_quota(
        self,
        *,
        sign_up_quota_config: typing.Optional[typing.Union["GoogleIdentityPlatformConfigQuotaSignUpQuotaConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param sign_up_quota_config: sign_up_quota_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#sign_up_quota_config GoogleIdentityPlatformConfig#sign_up_quota_config}
        '''
        value = GoogleIdentityPlatformConfigQuota(
            sign_up_quota_config=sign_up_quota_config
        )

        return typing.cast(None, jsii.invoke(self, "putQuota", [value]))

    @jsii.member(jsii_name="putSignIn")
    def put_sign_in(
        self,
        *,
        allow_duplicate_emails: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        anonymous: typing.Optional[typing.Union["GoogleIdentityPlatformConfigSignInAnonymous", typing.Dict[builtins.str, typing.Any]]] = None,
        email: typing.Optional[typing.Union["GoogleIdentityPlatformConfigSignInEmail", typing.Dict[builtins.str, typing.Any]]] = None,
        phone_number: typing.Optional[typing.Union["GoogleIdentityPlatformConfigSignInPhoneNumber", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_duplicate_emails: Whether to allow more than one account to have the same email. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#allow_duplicate_emails GoogleIdentityPlatformConfig#allow_duplicate_emails}
        :param anonymous: anonymous block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#anonymous GoogleIdentityPlatformConfig#anonymous}
        :param email: email block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#email GoogleIdentityPlatformConfig#email}
        :param phone_number: phone_number block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#phone_number GoogleIdentityPlatformConfig#phone_number}
        '''
        value = GoogleIdentityPlatformConfigSignIn(
            allow_duplicate_emails=allow_duplicate_emails,
            anonymous=anonymous,
            email=email,
            phone_number=phone_number,
        )

        return typing.cast(None, jsii.invoke(self, "putSignIn", [value]))

    @jsii.member(jsii_name="putSmsRegionConfig")
    def put_sms_region_config(
        self,
        *,
        allow_by_default: typing.Optional[typing.Union["GoogleIdentityPlatformConfigSmsRegionConfigAllowByDefault", typing.Dict[builtins.str, typing.Any]]] = None,
        allowlist_only: typing.Optional[typing.Union["GoogleIdentityPlatformConfigSmsRegionConfigAllowlistOnly", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_by_default: allow_by_default block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#allow_by_default GoogleIdentityPlatformConfig#allow_by_default}
        :param allowlist_only: allowlist_only block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#allowlist_only GoogleIdentityPlatformConfig#allowlist_only}
        '''
        value = GoogleIdentityPlatformConfigSmsRegionConfig(
            allow_by_default=allow_by_default, allowlist_only=allowlist_only
        )

        return typing.cast(None, jsii.invoke(self, "putSmsRegionConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#create GoogleIdentityPlatformConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#delete GoogleIdentityPlatformConfig#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#update GoogleIdentityPlatformConfig#update}.
        '''
        value = GoogleIdentityPlatformConfigTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAuthorizedDomains")
    def reset_authorized_domains(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthorizedDomains", []))

    @jsii.member(jsii_name="resetAutodeleteAnonymousUsers")
    def reset_autodelete_anonymous_users(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutodeleteAnonymousUsers", []))

    @jsii.member(jsii_name="resetBlockingFunctions")
    def reset_blocking_functions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBlockingFunctions", []))

    @jsii.member(jsii_name="resetClient")
    def reset_client(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClient", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMfa")
    def reset_mfa(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMfa", []))

    @jsii.member(jsii_name="resetMonitoring")
    def reset_monitoring(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonitoring", []))

    @jsii.member(jsii_name="resetMultiTenant")
    def reset_multi_tenant(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMultiTenant", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetQuota")
    def reset_quota(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQuota", []))

    @jsii.member(jsii_name="resetSignIn")
    def reset_sign_in(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSignIn", []))

    @jsii.member(jsii_name="resetSmsRegionConfig")
    def reset_sms_region_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSmsRegionConfig", []))

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
    @jsii.member(jsii_name="blockingFunctions")
    def blocking_functions(
        self,
    ) -> "GoogleIdentityPlatformConfigBlockingFunctionsOutputReference":
        return typing.cast("GoogleIdentityPlatformConfigBlockingFunctionsOutputReference", jsii.get(self, "blockingFunctions"))

    @builtins.property
    @jsii.member(jsii_name="client")
    def client(self) -> "GoogleIdentityPlatformConfigClientOutputReference":
        return typing.cast("GoogleIdentityPlatformConfigClientOutputReference", jsii.get(self, "client"))

    @builtins.property
    @jsii.member(jsii_name="mfa")
    def mfa(self) -> "GoogleIdentityPlatformConfigMfaOutputReference":
        return typing.cast("GoogleIdentityPlatformConfigMfaOutputReference", jsii.get(self, "mfa"))

    @builtins.property
    @jsii.member(jsii_name="monitoring")
    def monitoring(self) -> "GoogleIdentityPlatformConfigMonitoringOutputReference":
        return typing.cast("GoogleIdentityPlatformConfigMonitoringOutputReference", jsii.get(self, "monitoring"))

    @builtins.property
    @jsii.member(jsii_name="multiTenant")
    def multi_tenant(self) -> "GoogleIdentityPlatformConfigMultiTenantOutputReference":
        return typing.cast("GoogleIdentityPlatformConfigMultiTenantOutputReference", jsii.get(self, "multiTenant"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="quota")
    def quota(self) -> "GoogleIdentityPlatformConfigQuotaOutputReference":
        return typing.cast("GoogleIdentityPlatformConfigQuotaOutputReference", jsii.get(self, "quota"))

    @builtins.property
    @jsii.member(jsii_name="signIn")
    def sign_in(self) -> "GoogleIdentityPlatformConfigSignInOutputReference":
        return typing.cast("GoogleIdentityPlatformConfigSignInOutputReference", jsii.get(self, "signIn"))

    @builtins.property
    @jsii.member(jsii_name="smsRegionConfig")
    def sms_region_config(
        self,
    ) -> "GoogleIdentityPlatformConfigSmsRegionConfigOutputReference":
        return typing.cast("GoogleIdentityPlatformConfigSmsRegionConfigOutputReference", jsii.get(self, "smsRegionConfig"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleIdentityPlatformConfigTimeoutsOutputReference":
        return typing.cast("GoogleIdentityPlatformConfigTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="authorizedDomainsInput")
    def authorized_domains_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "authorizedDomainsInput"))

    @builtins.property
    @jsii.member(jsii_name="autodeleteAnonymousUsersInput")
    def autodelete_anonymous_users_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "autodeleteAnonymousUsersInput"))

    @builtins.property
    @jsii.member(jsii_name="blockingFunctionsInput")
    def blocking_functions_input(
        self,
    ) -> typing.Optional["GoogleIdentityPlatformConfigBlockingFunctions"]:
        return typing.cast(typing.Optional["GoogleIdentityPlatformConfigBlockingFunctions"], jsii.get(self, "blockingFunctionsInput"))

    @builtins.property
    @jsii.member(jsii_name="clientInput")
    def client_input(self) -> typing.Optional["GoogleIdentityPlatformConfigClient"]:
        return typing.cast(typing.Optional["GoogleIdentityPlatformConfigClient"], jsii.get(self, "clientInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="mfaInput")
    def mfa_input(self) -> typing.Optional["GoogleIdentityPlatformConfigMfa"]:
        return typing.cast(typing.Optional["GoogleIdentityPlatformConfigMfa"], jsii.get(self, "mfaInput"))

    @builtins.property
    @jsii.member(jsii_name="monitoringInput")
    def monitoring_input(
        self,
    ) -> typing.Optional["GoogleIdentityPlatformConfigMonitoring"]:
        return typing.cast(typing.Optional["GoogleIdentityPlatformConfigMonitoring"], jsii.get(self, "monitoringInput"))

    @builtins.property
    @jsii.member(jsii_name="multiTenantInput")
    def multi_tenant_input(
        self,
    ) -> typing.Optional["GoogleIdentityPlatformConfigMultiTenant"]:
        return typing.cast(typing.Optional["GoogleIdentityPlatformConfigMultiTenant"], jsii.get(self, "multiTenantInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="quotaInput")
    def quota_input(self) -> typing.Optional["GoogleIdentityPlatformConfigQuota"]:
        return typing.cast(typing.Optional["GoogleIdentityPlatformConfigQuota"], jsii.get(self, "quotaInput"))

    @builtins.property
    @jsii.member(jsii_name="signInInput")
    def sign_in_input(self) -> typing.Optional["GoogleIdentityPlatformConfigSignIn"]:
        return typing.cast(typing.Optional["GoogleIdentityPlatformConfigSignIn"], jsii.get(self, "signInInput"))

    @builtins.property
    @jsii.member(jsii_name="smsRegionConfigInput")
    def sms_region_config_input(
        self,
    ) -> typing.Optional["GoogleIdentityPlatformConfigSmsRegionConfig"]:
        return typing.cast(typing.Optional["GoogleIdentityPlatformConfigSmsRegionConfig"], jsii.get(self, "smsRegionConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleIdentityPlatformConfigTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleIdentityPlatformConfigTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="authorizedDomains")
    def authorized_domains(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "authorizedDomains"))

    @authorized_domains.setter
    def authorized_domains(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba6bba04ed831e6d658275035e1712c220185a20a89175cafa467a9f9a063b10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authorizedDomains", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="autodeleteAnonymousUsers")
    def autodelete_anonymous_users(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "autodeleteAnonymousUsers"))

    @autodelete_anonymous_users.setter
    def autodelete_anonymous_users(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b69e944ee15ea1fca1d15dfe0206c5c93fbb90eab2b3fed2e76394b185d38594)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autodeleteAnonymousUsers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9ffd676711ee304a2f67b67a45241b02ccb77b283bcaf2d410baa8394ae2283)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da00d7ef74141ec56423b5470d86c28b839dc1a80634b9b4409ddb02d445aa84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformConfig.GoogleIdentityPlatformConfigBlockingFunctions",
    jsii_struct_bases=[],
    name_mapping={
        "triggers": "triggers",
        "forward_inbound_credentials": "forwardInboundCredentials",
    },
)
class GoogleIdentityPlatformConfigBlockingFunctions:
    def __init__(
        self,
        *,
        triggers: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleIdentityPlatformConfigBlockingFunctionsTriggers", typing.Dict[builtins.str, typing.Any]]]],
        forward_inbound_credentials: typing.Optional[typing.Union["GoogleIdentityPlatformConfigBlockingFunctionsForwardInboundCredentials", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param triggers: triggers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#triggers GoogleIdentityPlatformConfig#triggers}
        :param forward_inbound_credentials: forward_inbound_credentials block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#forward_inbound_credentials GoogleIdentityPlatformConfig#forward_inbound_credentials}
        '''
        if isinstance(forward_inbound_credentials, dict):
            forward_inbound_credentials = GoogleIdentityPlatformConfigBlockingFunctionsForwardInboundCredentials(**forward_inbound_credentials)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e760b62a4ebf752e5a28ec528d3ddb67e173f2964070e49af5e068d8e647c89b)
            check_type(argname="argument triggers", value=triggers, expected_type=type_hints["triggers"])
            check_type(argname="argument forward_inbound_credentials", value=forward_inbound_credentials, expected_type=type_hints["forward_inbound_credentials"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "triggers": triggers,
        }
        if forward_inbound_credentials is not None:
            self._values["forward_inbound_credentials"] = forward_inbound_credentials

    @builtins.property
    def triggers(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleIdentityPlatformConfigBlockingFunctionsTriggers"]]:
        '''triggers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#triggers GoogleIdentityPlatformConfig#triggers}
        '''
        result = self._values.get("triggers")
        assert result is not None, "Required property 'triggers' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleIdentityPlatformConfigBlockingFunctionsTriggers"]], result)

    @builtins.property
    def forward_inbound_credentials(
        self,
    ) -> typing.Optional["GoogleIdentityPlatformConfigBlockingFunctionsForwardInboundCredentials"]:
        '''forward_inbound_credentials block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#forward_inbound_credentials GoogleIdentityPlatformConfig#forward_inbound_credentials}
        '''
        result = self._values.get("forward_inbound_credentials")
        return typing.cast(typing.Optional["GoogleIdentityPlatformConfigBlockingFunctionsForwardInboundCredentials"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIdentityPlatformConfigBlockingFunctions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformConfig.GoogleIdentityPlatformConfigBlockingFunctionsForwardInboundCredentials",
    jsii_struct_bases=[],
    name_mapping={
        "access_token": "accessToken",
        "id_token": "idToken",
        "refresh_token": "refreshToken",
    },
)
class GoogleIdentityPlatformConfigBlockingFunctionsForwardInboundCredentials:
    def __init__(
        self,
        *,
        access_token: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id_token: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        refresh_token: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param access_token: Whether to pass the user's OAuth identity provider's access token. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#access_token GoogleIdentityPlatformConfig#access_token}
        :param id_token: Whether to pass the user's OIDC identity provider's ID token. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#id_token GoogleIdentityPlatformConfig#id_token}
        :param refresh_token: Whether to pass the user's OAuth identity provider's refresh token. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#refresh_token GoogleIdentityPlatformConfig#refresh_token}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b5e9f0f21c65f1e68fafc7f7e999939bee330ef374023061efb61bcb26028bb)
            check_type(argname="argument access_token", value=access_token, expected_type=type_hints["access_token"])
            check_type(argname="argument id_token", value=id_token, expected_type=type_hints["id_token"])
            check_type(argname="argument refresh_token", value=refresh_token, expected_type=type_hints["refresh_token"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_token is not None:
            self._values["access_token"] = access_token
        if id_token is not None:
            self._values["id_token"] = id_token
        if refresh_token is not None:
            self._values["refresh_token"] = refresh_token

    @builtins.property
    def access_token(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to pass the user's OAuth identity provider's access token.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#access_token GoogleIdentityPlatformConfig#access_token}
        '''
        result = self._values.get("access_token")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id_token(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to pass the user's OIDC identity provider's ID token.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#id_token GoogleIdentityPlatformConfig#id_token}
        '''
        result = self._values.get("id_token")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def refresh_token(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to pass the user's OAuth identity provider's refresh token.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#refresh_token GoogleIdentityPlatformConfig#refresh_token}
        '''
        result = self._values.get("refresh_token")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIdentityPlatformConfigBlockingFunctionsForwardInboundCredentials(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIdentityPlatformConfigBlockingFunctionsForwardInboundCredentialsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformConfig.GoogleIdentityPlatformConfigBlockingFunctionsForwardInboundCredentialsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__262eb45a7a724798a5251622822d5622ba183dc9b5744f50571851b6a5ad0171)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAccessToken")
    def reset_access_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessToken", []))

    @jsii.member(jsii_name="resetIdToken")
    def reset_id_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdToken", []))

    @jsii.member(jsii_name="resetRefreshToken")
    def reset_refresh_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRefreshToken", []))

    @builtins.property
    @jsii.member(jsii_name="accessTokenInput")
    def access_token_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "accessTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="idTokenInput")
    def id_token_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "idTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="refreshTokenInput")
    def refresh_token_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "refreshTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="accessToken")
    def access_token(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "accessToken"))

    @access_token.setter
    def access_token(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c7c659e383a95194fdbc28da76769f05cd4c248e0da1d19168cab3943cc02f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessToken", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="idToken")
    def id_token(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "idToken"))

    @id_token.setter
    def id_token(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__519d09bcb79d67294f25021e06bfe6d0b18b52f790a18f86c1c17abdb217d0f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "idToken", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="refreshToken")
    def refresh_token(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "refreshToken"))

    @refresh_token.setter
    def refresh_token(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e2e316be60ba19affc3b8c38f345b6ed4398d02b6ee1fb5709167ee04a2c91c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "refreshToken", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIdentityPlatformConfigBlockingFunctionsForwardInboundCredentials]:
        return typing.cast(typing.Optional[GoogleIdentityPlatformConfigBlockingFunctionsForwardInboundCredentials], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIdentityPlatformConfigBlockingFunctionsForwardInboundCredentials],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d21057ba622f0922bff29ddba3656f044a0cc73238804ec9a64a3f56de78556)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleIdentityPlatformConfigBlockingFunctionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformConfig.GoogleIdentityPlatformConfigBlockingFunctionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d87f8255b76515af500c37f64de8cfca187f939e1249411efdb754b6d8c3691)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putForwardInboundCredentials")
    def put_forward_inbound_credentials(
        self,
        *,
        access_token: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id_token: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        refresh_token: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param access_token: Whether to pass the user's OAuth identity provider's access token. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#access_token GoogleIdentityPlatformConfig#access_token}
        :param id_token: Whether to pass the user's OIDC identity provider's ID token. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#id_token GoogleIdentityPlatformConfig#id_token}
        :param refresh_token: Whether to pass the user's OAuth identity provider's refresh token. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#refresh_token GoogleIdentityPlatformConfig#refresh_token}
        '''
        value = GoogleIdentityPlatformConfigBlockingFunctionsForwardInboundCredentials(
            access_token=access_token, id_token=id_token, refresh_token=refresh_token
        )

        return typing.cast(None, jsii.invoke(self, "putForwardInboundCredentials", [value]))

    @jsii.member(jsii_name="putTriggers")
    def put_triggers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleIdentityPlatformConfigBlockingFunctionsTriggers", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__398b263ea25f410cb0050565af7c92f6e102b5d6015b4cdc0c076f12826c920d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTriggers", [value]))

    @jsii.member(jsii_name="resetForwardInboundCredentials")
    def reset_forward_inbound_credentials(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForwardInboundCredentials", []))

    @builtins.property
    @jsii.member(jsii_name="forwardInboundCredentials")
    def forward_inbound_credentials(
        self,
    ) -> GoogleIdentityPlatformConfigBlockingFunctionsForwardInboundCredentialsOutputReference:
        return typing.cast(GoogleIdentityPlatformConfigBlockingFunctionsForwardInboundCredentialsOutputReference, jsii.get(self, "forwardInboundCredentials"))

    @builtins.property
    @jsii.member(jsii_name="triggers")
    def triggers(self) -> "GoogleIdentityPlatformConfigBlockingFunctionsTriggersList":
        return typing.cast("GoogleIdentityPlatformConfigBlockingFunctionsTriggersList", jsii.get(self, "triggers"))

    @builtins.property
    @jsii.member(jsii_name="forwardInboundCredentialsInput")
    def forward_inbound_credentials_input(
        self,
    ) -> typing.Optional[GoogleIdentityPlatformConfigBlockingFunctionsForwardInboundCredentials]:
        return typing.cast(typing.Optional[GoogleIdentityPlatformConfigBlockingFunctionsForwardInboundCredentials], jsii.get(self, "forwardInboundCredentialsInput"))

    @builtins.property
    @jsii.member(jsii_name="triggersInput")
    def triggers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleIdentityPlatformConfigBlockingFunctionsTriggers"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleIdentityPlatformConfigBlockingFunctionsTriggers"]]], jsii.get(self, "triggersInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIdentityPlatformConfigBlockingFunctions]:
        return typing.cast(typing.Optional[GoogleIdentityPlatformConfigBlockingFunctions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIdentityPlatformConfigBlockingFunctions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef3cf4350abc132dd59cc84c6cff90ace361ccdc01c2d931e71f21870b94fa0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformConfig.GoogleIdentityPlatformConfigBlockingFunctionsTriggers",
    jsii_struct_bases=[],
    name_mapping={"event_type": "eventType", "function_uri": "functionUri"},
)
class GoogleIdentityPlatformConfigBlockingFunctionsTriggers:
    def __init__(self, *, event_type: builtins.str, function_uri: builtins.str) -> None:
        '''
        :param event_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#event_type GoogleIdentityPlatformConfig#event_type}.
        :param function_uri: HTTP URI trigger for the Cloud Function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#function_uri GoogleIdentityPlatformConfig#function_uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da792164b4d269f5c1fcf2ede0584376c10adf486cae79d82e5e5fc45e966f37)
            check_type(argname="argument event_type", value=event_type, expected_type=type_hints["event_type"])
            check_type(argname="argument function_uri", value=function_uri, expected_type=type_hints["function_uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "event_type": event_type,
            "function_uri": function_uri,
        }

    @builtins.property
    def event_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#event_type GoogleIdentityPlatformConfig#event_type}.'''
        result = self._values.get("event_type")
        assert result is not None, "Required property 'event_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def function_uri(self) -> builtins.str:
        '''HTTP URI trigger for the Cloud Function.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#function_uri GoogleIdentityPlatformConfig#function_uri}
        '''
        result = self._values.get("function_uri")
        assert result is not None, "Required property 'function_uri' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIdentityPlatformConfigBlockingFunctionsTriggers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIdentityPlatformConfigBlockingFunctionsTriggersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformConfig.GoogleIdentityPlatformConfigBlockingFunctionsTriggersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d7e63e1e0d62e6127b28797e9207c1247ae1f550b9c8632a7eef1dfa80535289)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleIdentityPlatformConfigBlockingFunctionsTriggersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__616a6b6480b0158c9d4249025445fe2b38ae20a95f3c3bcc89f177282103f769)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleIdentityPlatformConfigBlockingFunctionsTriggersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddfff4bb9e2ff1b0f468b09154baf34b6296ac1359a001b40cb586bad10041f5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f6040c424009d28a7661f21505a35f443554c804407b697e16c5c8377ee13274)
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
            type_hints = typing.get_type_hints(_typecheckingstub__267f9fd8a589daa32d3b480514f08926dac26cc2e77eafac533edfc88dba91c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIdentityPlatformConfigBlockingFunctionsTriggers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIdentityPlatformConfigBlockingFunctionsTriggers]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIdentityPlatformConfigBlockingFunctionsTriggers]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc0a959e25f15fb8578ac42f92850338cc1b574134d5f523953d490678a90ab0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleIdentityPlatformConfigBlockingFunctionsTriggersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformConfig.GoogleIdentityPlatformConfigBlockingFunctionsTriggersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2afd3a6ff4cb246d680be9933dfcd7dde66702f0929ccbf7dbcf0b5035e5119)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="eventTypeInput")
    def event_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="functionUriInput")
    def function_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "functionUriInput"))

    @builtins.property
    @jsii.member(jsii_name="eventType")
    def event_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventType"))

    @event_type.setter
    def event_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eca8be2d54e7b0d998fa3deae3ad348b2f3ded1b761ac570f60512c16bae530e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="functionUri")
    def function_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "functionUri"))

    @function_uri.setter
    def function_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00b328dc3fd0137c9927b68309f1e74ea76e1d691fbdf084059b2ff525f6cba9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "functionUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIdentityPlatformConfigBlockingFunctionsTriggers]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIdentityPlatformConfigBlockingFunctionsTriggers]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIdentityPlatformConfigBlockingFunctionsTriggers]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d4709dec81844de7eec6aa6fdd321a6784d23964ea66746e04ab1d1b5b1b597)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformConfig.GoogleIdentityPlatformConfigClient",
    jsii_struct_bases=[],
    name_mapping={"permissions": "permissions"},
)
class GoogleIdentityPlatformConfigClient:
    def __init__(
        self,
        *,
        permissions: typing.Optional[typing.Union["GoogleIdentityPlatformConfigClientPermissions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param permissions: permissions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#permissions GoogleIdentityPlatformConfig#permissions}
        '''
        if isinstance(permissions, dict):
            permissions = GoogleIdentityPlatformConfigClientPermissions(**permissions)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f188d4551fd12632e56fd6e9c1853885c4dbdaf80e048ccdbba13f93c12f6cb9)
            check_type(argname="argument permissions", value=permissions, expected_type=type_hints["permissions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if permissions is not None:
            self._values["permissions"] = permissions

    @builtins.property
    def permissions(
        self,
    ) -> typing.Optional["GoogleIdentityPlatformConfigClientPermissions"]:
        '''permissions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#permissions GoogleIdentityPlatformConfig#permissions}
        '''
        result = self._values.get("permissions")
        return typing.cast(typing.Optional["GoogleIdentityPlatformConfigClientPermissions"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIdentityPlatformConfigClient(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIdentityPlatformConfigClientOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformConfig.GoogleIdentityPlatformConfigClientOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d555ad76c73176c7fc03ee725acccca8638fb80fdd7f2be19dfc632d0efb940)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPermissions")
    def put_permissions(
        self,
        *,
        disabled_user_deletion: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disabled_user_signup: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param disabled_user_deletion: When true, end users cannot delete their account on the associated project through any of our API methods. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#disabled_user_deletion GoogleIdentityPlatformConfig#disabled_user_deletion}
        :param disabled_user_signup: When true, end users cannot sign up for a new account on the associated project through any of our API methods. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#disabled_user_signup GoogleIdentityPlatformConfig#disabled_user_signup}
        '''
        value = GoogleIdentityPlatformConfigClientPermissions(
            disabled_user_deletion=disabled_user_deletion,
            disabled_user_signup=disabled_user_signup,
        )

        return typing.cast(None, jsii.invoke(self, "putPermissions", [value]))

    @jsii.member(jsii_name="resetPermissions")
    def reset_permissions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPermissions", []))

    @builtins.property
    @jsii.member(jsii_name="apiKey")
    def api_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiKey"))

    @builtins.property
    @jsii.member(jsii_name="firebaseSubdomain")
    def firebase_subdomain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "firebaseSubdomain"))

    @builtins.property
    @jsii.member(jsii_name="permissions")
    def permissions(
        self,
    ) -> "GoogleIdentityPlatformConfigClientPermissionsOutputReference":
        return typing.cast("GoogleIdentityPlatformConfigClientPermissionsOutputReference", jsii.get(self, "permissions"))

    @builtins.property
    @jsii.member(jsii_name="permissionsInput")
    def permissions_input(
        self,
    ) -> typing.Optional["GoogleIdentityPlatformConfigClientPermissions"]:
        return typing.cast(typing.Optional["GoogleIdentityPlatformConfigClientPermissions"], jsii.get(self, "permissionsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleIdentityPlatformConfigClient]:
        return typing.cast(typing.Optional[GoogleIdentityPlatformConfigClient], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIdentityPlatformConfigClient],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e053de35c3a7e11d51243f2d71ae9158ad1c507bb1d0b238f34882f3a6f87715)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformConfig.GoogleIdentityPlatformConfigClientPermissions",
    jsii_struct_bases=[],
    name_mapping={
        "disabled_user_deletion": "disabledUserDeletion",
        "disabled_user_signup": "disabledUserSignup",
    },
)
class GoogleIdentityPlatformConfigClientPermissions:
    def __init__(
        self,
        *,
        disabled_user_deletion: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disabled_user_signup: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param disabled_user_deletion: When true, end users cannot delete their account on the associated project through any of our API methods. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#disabled_user_deletion GoogleIdentityPlatformConfig#disabled_user_deletion}
        :param disabled_user_signup: When true, end users cannot sign up for a new account on the associated project through any of our API methods. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#disabled_user_signup GoogleIdentityPlatformConfig#disabled_user_signup}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be044133d9fa5d2b098fdfdafd8f71355747e34d32017d61323a9f790fabf44e)
            check_type(argname="argument disabled_user_deletion", value=disabled_user_deletion, expected_type=type_hints["disabled_user_deletion"])
            check_type(argname="argument disabled_user_signup", value=disabled_user_signup, expected_type=type_hints["disabled_user_signup"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if disabled_user_deletion is not None:
            self._values["disabled_user_deletion"] = disabled_user_deletion
        if disabled_user_signup is not None:
            self._values["disabled_user_signup"] = disabled_user_signup

    @builtins.property
    def disabled_user_deletion(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When true, end users cannot delete their account on the associated project through any of our API methods.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#disabled_user_deletion GoogleIdentityPlatformConfig#disabled_user_deletion}
        '''
        result = self._values.get("disabled_user_deletion")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def disabled_user_signup(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When true, end users cannot sign up for a new account on the associated project through any of our API methods.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#disabled_user_signup GoogleIdentityPlatformConfig#disabled_user_signup}
        '''
        result = self._values.get("disabled_user_signup")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIdentityPlatformConfigClientPermissions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIdentityPlatformConfigClientPermissionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformConfig.GoogleIdentityPlatformConfigClientPermissionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b7465ce84e473b422d9afdf88bb40021b6110e88de5266209193a9856e627786)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDisabledUserDeletion")
    def reset_disabled_user_deletion(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisabledUserDeletion", []))

    @jsii.member(jsii_name="resetDisabledUserSignup")
    def reset_disabled_user_signup(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisabledUserSignup", []))

    @builtins.property
    @jsii.member(jsii_name="disabledUserDeletionInput")
    def disabled_user_deletion_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disabledUserDeletionInput"))

    @builtins.property
    @jsii.member(jsii_name="disabledUserSignupInput")
    def disabled_user_signup_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disabledUserSignupInput"))

    @builtins.property
    @jsii.member(jsii_name="disabledUserDeletion")
    def disabled_user_deletion(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disabledUserDeletion"))

    @disabled_user_deletion.setter
    def disabled_user_deletion(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5511410f416ab8bb3970cbd4c1fe538b482d02e9389d609b202d82cbf203b6f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disabledUserDeletion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disabledUserSignup")
    def disabled_user_signup(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disabledUserSignup"))

    @disabled_user_signup.setter
    def disabled_user_signup(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20bb536b927bc7a405a0fc6779a10977d3bd47a82f98f0d4469d00ee5958772b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disabledUserSignup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIdentityPlatformConfigClientPermissions]:
        return typing.cast(typing.Optional[GoogleIdentityPlatformConfigClientPermissions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIdentityPlatformConfigClientPermissions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82764503b1a7744dd2dd7a9532accbeb0be764a759db4c2646e9d1a2e6b4bfd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformConfig.GoogleIdentityPlatformConfigConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "authorized_domains": "authorizedDomains",
        "autodelete_anonymous_users": "autodeleteAnonymousUsers",
        "blocking_functions": "blockingFunctions",
        "client": "client",
        "id": "id",
        "mfa": "mfa",
        "monitoring": "monitoring",
        "multi_tenant": "multiTenant",
        "project": "project",
        "quota": "quota",
        "sign_in": "signIn",
        "sms_region_config": "smsRegionConfig",
        "timeouts": "timeouts",
    },
)
class GoogleIdentityPlatformConfigConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        authorized_domains: typing.Optional[typing.Sequence[builtins.str]] = None,
        autodelete_anonymous_users: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        blocking_functions: typing.Optional[typing.Union[GoogleIdentityPlatformConfigBlockingFunctions, typing.Dict[builtins.str, typing.Any]]] = None,
        client: typing.Optional[typing.Union[GoogleIdentityPlatformConfigClient, typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        mfa: typing.Optional[typing.Union["GoogleIdentityPlatformConfigMfa", typing.Dict[builtins.str, typing.Any]]] = None,
        monitoring: typing.Optional[typing.Union["GoogleIdentityPlatformConfigMonitoring", typing.Dict[builtins.str, typing.Any]]] = None,
        multi_tenant: typing.Optional[typing.Union["GoogleIdentityPlatformConfigMultiTenant", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        quota: typing.Optional[typing.Union["GoogleIdentityPlatformConfigQuota", typing.Dict[builtins.str, typing.Any]]] = None,
        sign_in: typing.Optional[typing.Union["GoogleIdentityPlatformConfigSignIn", typing.Dict[builtins.str, typing.Any]]] = None,
        sms_region_config: typing.Optional[typing.Union["GoogleIdentityPlatformConfigSmsRegionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleIdentityPlatformConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param authorized_domains: List of domains authorized for OAuth redirects. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#authorized_domains GoogleIdentityPlatformConfig#authorized_domains}
        :param autodelete_anonymous_users: Whether anonymous users will be auto-deleted after a period of 30 days. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#autodelete_anonymous_users GoogleIdentityPlatformConfig#autodelete_anonymous_users}
        :param blocking_functions: blocking_functions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#blocking_functions GoogleIdentityPlatformConfig#blocking_functions}
        :param client: client block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#client GoogleIdentityPlatformConfig#client}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#id GoogleIdentityPlatformConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param mfa: mfa block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#mfa GoogleIdentityPlatformConfig#mfa}
        :param monitoring: monitoring block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#monitoring GoogleIdentityPlatformConfig#monitoring}
        :param multi_tenant: multi_tenant block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#multi_tenant GoogleIdentityPlatformConfig#multi_tenant}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#project GoogleIdentityPlatformConfig#project}.
        :param quota: quota block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#quota GoogleIdentityPlatformConfig#quota}
        :param sign_in: sign_in block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#sign_in GoogleIdentityPlatformConfig#sign_in}
        :param sms_region_config: sms_region_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#sms_region_config GoogleIdentityPlatformConfig#sms_region_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#timeouts GoogleIdentityPlatformConfig#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(blocking_functions, dict):
            blocking_functions = GoogleIdentityPlatformConfigBlockingFunctions(**blocking_functions)
        if isinstance(client, dict):
            client = GoogleIdentityPlatformConfigClient(**client)
        if isinstance(mfa, dict):
            mfa = GoogleIdentityPlatformConfigMfa(**mfa)
        if isinstance(monitoring, dict):
            monitoring = GoogleIdentityPlatformConfigMonitoring(**monitoring)
        if isinstance(multi_tenant, dict):
            multi_tenant = GoogleIdentityPlatformConfigMultiTenant(**multi_tenant)
        if isinstance(quota, dict):
            quota = GoogleIdentityPlatformConfigQuota(**quota)
        if isinstance(sign_in, dict):
            sign_in = GoogleIdentityPlatformConfigSignIn(**sign_in)
        if isinstance(sms_region_config, dict):
            sms_region_config = GoogleIdentityPlatformConfigSmsRegionConfig(**sms_region_config)
        if isinstance(timeouts, dict):
            timeouts = GoogleIdentityPlatformConfigTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0865745b6f40a84c0cf16ad1d456019a31ec0a068a697d8ae97b69cd465dab73)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument authorized_domains", value=authorized_domains, expected_type=type_hints["authorized_domains"])
            check_type(argname="argument autodelete_anonymous_users", value=autodelete_anonymous_users, expected_type=type_hints["autodelete_anonymous_users"])
            check_type(argname="argument blocking_functions", value=blocking_functions, expected_type=type_hints["blocking_functions"])
            check_type(argname="argument client", value=client, expected_type=type_hints["client"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument mfa", value=mfa, expected_type=type_hints["mfa"])
            check_type(argname="argument monitoring", value=monitoring, expected_type=type_hints["monitoring"])
            check_type(argname="argument multi_tenant", value=multi_tenant, expected_type=type_hints["multi_tenant"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument quota", value=quota, expected_type=type_hints["quota"])
            check_type(argname="argument sign_in", value=sign_in, expected_type=type_hints["sign_in"])
            check_type(argname="argument sms_region_config", value=sms_region_config, expected_type=type_hints["sms_region_config"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
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
        if authorized_domains is not None:
            self._values["authorized_domains"] = authorized_domains
        if autodelete_anonymous_users is not None:
            self._values["autodelete_anonymous_users"] = autodelete_anonymous_users
        if blocking_functions is not None:
            self._values["blocking_functions"] = blocking_functions
        if client is not None:
            self._values["client"] = client
        if id is not None:
            self._values["id"] = id
        if mfa is not None:
            self._values["mfa"] = mfa
        if monitoring is not None:
            self._values["monitoring"] = monitoring
        if multi_tenant is not None:
            self._values["multi_tenant"] = multi_tenant
        if project is not None:
            self._values["project"] = project
        if quota is not None:
            self._values["quota"] = quota
        if sign_in is not None:
            self._values["sign_in"] = sign_in
        if sms_region_config is not None:
            self._values["sms_region_config"] = sms_region_config
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
    def authorized_domains(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of domains authorized for OAuth redirects.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#authorized_domains GoogleIdentityPlatformConfig#authorized_domains}
        '''
        result = self._values.get("authorized_domains")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def autodelete_anonymous_users(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether anonymous users will be auto-deleted after a period of 30 days.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#autodelete_anonymous_users GoogleIdentityPlatformConfig#autodelete_anonymous_users}
        '''
        result = self._values.get("autodelete_anonymous_users")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def blocking_functions(
        self,
    ) -> typing.Optional[GoogleIdentityPlatformConfigBlockingFunctions]:
        '''blocking_functions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#blocking_functions GoogleIdentityPlatformConfig#blocking_functions}
        '''
        result = self._values.get("blocking_functions")
        return typing.cast(typing.Optional[GoogleIdentityPlatformConfigBlockingFunctions], result)

    @builtins.property
    def client(self) -> typing.Optional[GoogleIdentityPlatformConfigClient]:
        '''client block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#client GoogleIdentityPlatformConfig#client}
        '''
        result = self._values.get("client")
        return typing.cast(typing.Optional[GoogleIdentityPlatformConfigClient], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#id GoogleIdentityPlatformConfig#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mfa(self) -> typing.Optional["GoogleIdentityPlatformConfigMfa"]:
        '''mfa block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#mfa GoogleIdentityPlatformConfig#mfa}
        '''
        result = self._values.get("mfa")
        return typing.cast(typing.Optional["GoogleIdentityPlatformConfigMfa"], result)

    @builtins.property
    def monitoring(self) -> typing.Optional["GoogleIdentityPlatformConfigMonitoring"]:
        '''monitoring block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#monitoring GoogleIdentityPlatformConfig#monitoring}
        '''
        result = self._values.get("monitoring")
        return typing.cast(typing.Optional["GoogleIdentityPlatformConfigMonitoring"], result)

    @builtins.property
    def multi_tenant(
        self,
    ) -> typing.Optional["GoogleIdentityPlatformConfigMultiTenant"]:
        '''multi_tenant block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#multi_tenant GoogleIdentityPlatformConfig#multi_tenant}
        '''
        result = self._values.get("multi_tenant")
        return typing.cast(typing.Optional["GoogleIdentityPlatformConfigMultiTenant"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#project GoogleIdentityPlatformConfig#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def quota(self) -> typing.Optional["GoogleIdentityPlatformConfigQuota"]:
        '''quota block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#quota GoogleIdentityPlatformConfig#quota}
        '''
        result = self._values.get("quota")
        return typing.cast(typing.Optional["GoogleIdentityPlatformConfigQuota"], result)

    @builtins.property
    def sign_in(self) -> typing.Optional["GoogleIdentityPlatformConfigSignIn"]:
        '''sign_in block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#sign_in GoogleIdentityPlatformConfig#sign_in}
        '''
        result = self._values.get("sign_in")
        return typing.cast(typing.Optional["GoogleIdentityPlatformConfigSignIn"], result)

    @builtins.property
    def sms_region_config(
        self,
    ) -> typing.Optional["GoogleIdentityPlatformConfigSmsRegionConfig"]:
        '''sms_region_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#sms_region_config GoogleIdentityPlatformConfig#sms_region_config}
        '''
        result = self._values.get("sms_region_config")
        return typing.cast(typing.Optional["GoogleIdentityPlatformConfigSmsRegionConfig"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleIdentityPlatformConfigTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#timeouts GoogleIdentityPlatformConfig#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleIdentityPlatformConfigTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIdentityPlatformConfigConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformConfig.GoogleIdentityPlatformConfigMfa",
    jsii_struct_bases=[],
    name_mapping={
        "enabled_providers": "enabledProviders",
        "provider_configs": "providerConfigs",
        "state": "state",
    },
)
class GoogleIdentityPlatformConfigMfa:
    def __init__(
        self,
        *,
        enabled_providers: typing.Optional[typing.Sequence[builtins.str]] = None,
        provider_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleIdentityPlatformConfigMfaProviderConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        state: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled_providers: A list of usable second factors for this project. Possible values: ["PHONE_SMS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#enabled_providers GoogleIdentityPlatformConfig#enabled_providers}
        :param provider_configs: provider_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#provider_configs GoogleIdentityPlatformConfig#provider_configs}
        :param state: Whether MultiFactor Authentication has been enabled for this project. Possible values: ["DISABLED", "ENABLED", "MANDATORY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#state GoogleIdentityPlatformConfig#state}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b18702fffe3caffd16c3ae5f2c904a7e1e8a3e4da8029686384e2b43fc7e85c)
            check_type(argname="argument enabled_providers", value=enabled_providers, expected_type=type_hints["enabled_providers"])
            check_type(argname="argument provider_configs", value=provider_configs, expected_type=type_hints["provider_configs"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled_providers is not None:
            self._values["enabled_providers"] = enabled_providers
        if provider_configs is not None:
            self._values["provider_configs"] = provider_configs
        if state is not None:
            self._values["state"] = state

    @builtins.property
    def enabled_providers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of usable second factors for this project. Possible values: ["PHONE_SMS"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#enabled_providers GoogleIdentityPlatformConfig#enabled_providers}
        '''
        result = self._values.get("enabled_providers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def provider_configs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleIdentityPlatformConfigMfaProviderConfigs"]]]:
        '''provider_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#provider_configs GoogleIdentityPlatformConfig#provider_configs}
        '''
        result = self._values.get("provider_configs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleIdentityPlatformConfigMfaProviderConfigs"]]], result)

    @builtins.property
    def state(self) -> typing.Optional[builtins.str]:
        '''Whether MultiFactor Authentication has been enabled for this project. Possible values: ["DISABLED", "ENABLED", "MANDATORY"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#state GoogleIdentityPlatformConfig#state}
        '''
        result = self._values.get("state")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIdentityPlatformConfigMfa(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIdentityPlatformConfigMfaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformConfig.GoogleIdentityPlatformConfigMfaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__be4bca7e4553de0ddba65462033c02814236ba5ef7326a74621d6cba01657153)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putProviderConfigs")
    def put_provider_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleIdentityPlatformConfigMfaProviderConfigs", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__568f402db9ea425819cc8f7b8bfcc4865961b63d6882d51ab2b291de16376e43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putProviderConfigs", [value]))

    @jsii.member(jsii_name="resetEnabledProviders")
    def reset_enabled_providers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabledProviders", []))

    @jsii.member(jsii_name="resetProviderConfigs")
    def reset_provider_configs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProviderConfigs", []))

    @jsii.member(jsii_name="resetState")
    def reset_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetState", []))

    @builtins.property
    @jsii.member(jsii_name="providerConfigs")
    def provider_configs(self) -> "GoogleIdentityPlatformConfigMfaProviderConfigsList":
        return typing.cast("GoogleIdentityPlatformConfigMfaProviderConfigsList", jsii.get(self, "providerConfigs"))

    @builtins.property
    @jsii.member(jsii_name="enabledProvidersInput")
    def enabled_providers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "enabledProvidersInput"))

    @builtins.property
    @jsii.member(jsii_name="providerConfigsInput")
    def provider_configs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleIdentityPlatformConfigMfaProviderConfigs"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleIdentityPlatformConfigMfaProviderConfigs"]]], jsii.get(self, "providerConfigsInput"))

    @builtins.property
    @jsii.member(jsii_name="stateInput")
    def state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stateInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledProviders")
    def enabled_providers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "enabledProviders"))

    @enabled_providers.setter
    def enabled_providers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b68ef2fe2b9660762fbaee9bd4d27f7cb0d844508c4a183d098e209d725bd402)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabledProviders", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @state.setter
    def state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a35fa5946e093ae7399e5c4871a1a40c96d9d9a99e51d69ab87b9d86a4f3ed8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleIdentityPlatformConfigMfa]:
        return typing.cast(typing.Optional[GoogleIdentityPlatformConfigMfa], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIdentityPlatformConfigMfa],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ee14ae177b281551aab39bd2f196c42dc7c7ed756d04f3deabdf283d48fb396)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformConfig.GoogleIdentityPlatformConfigMfaProviderConfigs",
    jsii_struct_bases=[],
    name_mapping={"state": "state", "totp_provider_config": "totpProviderConfig"},
)
class GoogleIdentityPlatformConfigMfaProviderConfigs:
    def __init__(
        self,
        *,
        state: typing.Optional[builtins.str] = None,
        totp_provider_config: typing.Optional[typing.Union["GoogleIdentityPlatformConfigMfaProviderConfigsTotpProviderConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param state: Whether MultiFactor Authentication has been enabled for this project. Possible values: ["DISABLED", "ENABLED", "MANDATORY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#state GoogleIdentityPlatformConfig#state}
        :param totp_provider_config: totp_provider_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#totp_provider_config GoogleIdentityPlatformConfig#totp_provider_config}
        '''
        if isinstance(totp_provider_config, dict):
            totp_provider_config = GoogleIdentityPlatformConfigMfaProviderConfigsTotpProviderConfig(**totp_provider_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e17fa3beefe666917575254fb3bdbb8cc57f24cf897ab882090e9a1c9a640726)
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
            check_type(argname="argument totp_provider_config", value=totp_provider_config, expected_type=type_hints["totp_provider_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if state is not None:
            self._values["state"] = state
        if totp_provider_config is not None:
            self._values["totp_provider_config"] = totp_provider_config

    @builtins.property
    def state(self) -> typing.Optional[builtins.str]:
        '''Whether MultiFactor Authentication has been enabled for this project. Possible values: ["DISABLED", "ENABLED", "MANDATORY"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#state GoogleIdentityPlatformConfig#state}
        '''
        result = self._values.get("state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def totp_provider_config(
        self,
    ) -> typing.Optional["GoogleIdentityPlatformConfigMfaProviderConfigsTotpProviderConfig"]:
        '''totp_provider_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#totp_provider_config GoogleIdentityPlatformConfig#totp_provider_config}
        '''
        result = self._values.get("totp_provider_config")
        return typing.cast(typing.Optional["GoogleIdentityPlatformConfigMfaProviderConfigsTotpProviderConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIdentityPlatformConfigMfaProviderConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIdentityPlatformConfigMfaProviderConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformConfig.GoogleIdentityPlatformConfigMfaProviderConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__699d87b28a8b53f26a4cd42591a9582d6e87cd69e8c82523b2e4e6510c724dae)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleIdentityPlatformConfigMfaProviderConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7174a7e6885231fa164783ac1dec577dc902aba0c0dcaac91172fb7d8366497)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleIdentityPlatformConfigMfaProviderConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58a2e9c397ab0ff5247bb73bd63c0fabba6a55d0f19519db327b94e7fb9e2c4f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__65c9bdcf0f0b6072b189a694755f2c4b857eae7f564a64d9b1eeebdbb7ab975d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__97613a43c7c620b6b2a7fb5d4063f937bb0364317568c2fa33ff2b3ad20682d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIdentityPlatformConfigMfaProviderConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIdentityPlatformConfigMfaProviderConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIdentityPlatformConfigMfaProviderConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e3cd536686b10d665bef790c20356e8a24bcfb864b1919f612c0eb45c97bd95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleIdentityPlatformConfigMfaProviderConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformConfig.GoogleIdentityPlatformConfigMfaProviderConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d5cc9603ea077e6ebf6cdde47d81b12b1e9a3dfc99e58a828ff559f352c53f8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putTotpProviderConfig")
    def put_totp_provider_config(
        self,
        *,
        adjacent_intervals: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param adjacent_intervals: The allowed number of adjacent intervals that will be used for verification to avoid clock skew. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#adjacent_intervals GoogleIdentityPlatformConfig#adjacent_intervals}
        '''
        value = GoogleIdentityPlatformConfigMfaProviderConfigsTotpProviderConfig(
            adjacent_intervals=adjacent_intervals
        )

        return typing.cast(None, jsii.invoke(self, "putTotpProviderConfig", [value]))

    @jsii.member(jsii_name="resetState")
    def reset_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetState", []))

    @jsii.member(jsii_name="resetTotpProviderConfig")
    def reset_totp_provider_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTotpProviderConfig", []))

    @builtins.property
    @jsii.member(jsii_name="totpProviderConfig")
    def totp_provider_config(
        self,
    ) -> "GoogleIdentityPlatformConfigMfaProviderConfigsTotpProviderConfigOutputReference":
        return typing.cast("GoogleIdentityPlatformConfigMfaProviderConfigsTotpProviderConfigOutputReference", jsii.get(self, "totpProviderConfig"))

    @builtins.property
    @jsii.member(jsii_name="stateInput")
    def state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stateInput"))

    @builtins.property
    @jsii.member(jsii_name="totpProviderConfigInput")
    def totp_provider_config_input(
        self,
    ) -> typing.Optional["GoogleIdentityPlatformConfigMfaProviderConfigsTotpProviderConfig"]:
        return typing.cast(typing.Optional["GoogleIdentityPlatformConfigMfaProviderConfigsTotpProviderConfig"], jsii.get(self, "totpProviderConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @state.setter
    def state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2a2320f505b8459e7e74f16c07467f95d33128146bbe01c076c34e2b8032bfe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIdentityPlatformConfigMfaProviderConfigs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIdentityPlatformConfigMfaProviderConfigs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIdentityPlatformConfigMfaProviderConfigs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b96cec9a84e64981f162138b2769154f2685ab7fc964531ca989a932cdfbbf88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformConfig.GoogleIdentityPlatformConfigMfaProviderConfigsTotpProviderConfig",
    jsii_struct_bases=[],
    name_mapping={"adjacent_intervals": "adjacentIntervals"},
)
class GoogleIdentityPlatformConfigMfaProviderConfigsTotpProviderConfig:
    def __init__(
        self,
        *,
        adjacent_intervals: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param adjacent_intervals: The allowed number of adjacent intervals that will be used for verification to avoid clock skew. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#adjacent_intervals GoogleIdentityPlatformConfig#adjacent_intervals}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__715e84f5ecf14e42b6870e7184047c850497c86c74d2a9c7b9fc69e3b46c5607)
            check_type(argname="argument adjacent_intervals", value=adjacent_intervals, expected_type=type_hints["adjacent_intervals"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if adjacent_intervals is not None:
            self._values["adjacent_intervals"] = adjacent_intervals

    @builtins.property
    def adjacent_intervals(self) -> typing.Optional[jsii.Number]:
        '''The allowed number of adjacent intervals that will be used for verification to avoid clock skew.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#adjacent_intervals GoogleIdentityPlatformConfig#adjacent_intervals}
        '''
        result = self._values.get("adjacent_intervals")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIdentityPlatformConfigMfaProviderConfigsTotpProviderConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIdentityPlatformConfigMfaProviderConfigsTotpProviderConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformConfig.GoogleIdentityPlatformConfigMfaProviderConfigsTotpProviderConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5799b2e970021ac862452fea19a00c2002bc147a081f4aa428b02408e767f838)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAdjacentIntervals")
    def reset_adjacent_intervals(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdjacentIntervals", []))

    @builtins.property
    @jsii.member(jsii_name="adjacentIntervalsInput")
    def adjacent_intervals_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "adjacentIntervalsInput"))

    @builtins.property
    @jsii.member(jsii_name="adjacentIntervals")
    def adjacent_intervals(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "adjacentIntervals"))

    @adjacent_intervals.setter
    def adjacent_intervals(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f537f9f3df0e0b41d9fb26a5dbc5bf919c27ee5dd4c9f4198bc77a54bef6b21a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adjacentIntervals", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIdentityPlatformConfigMfaProviderConfigsTotpProviderConfig]:
        return typing.cast(typing.Optional[GoogleIdentityPlatformConfigMfaProviderConfigsTotpProviderConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIdentityPlatformConfigMfaProviderConfigsTotpProviderConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf9a10641cb1d67794fe47107f12ff086ea192de8098777e043883ad8129670e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformConfig.GoogleIdentityPlatformConfigMonitoring",
    jsii_struct_bases=[],
    name_mapping={"request_logging": "requestLogging"},
)
class GoogleIdentityPlatformConfigMonitoring:
    def __init__(
        self,
        *,
        request_logging: typing.Optional[typing.Union["GoogleIdentityPlatformConfigMonitoringRequestLogging", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param request_logging: request_logging block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#request_logging GoogleIdentityPlatformConfig#request_logging}
        '''
        if isinstance(request_logging, dict):
            request_logging = GoogleIdentityPlatformConfigMonitoringRequestLogging(**request_logging)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54132a9fee1d05bdf1cac5db671f66f7b0bc2fa98b6bbf3ce99628e3c1a9912b)
            check_type(argname="argument request_logging", value=request_logging, expected_type=type_hints["request_logging"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if request_logging is not None:
            self._values["request_logging"] = request_logging

    @builtins.property
    def request_logging(
        self,
    ) -> typing.Optional["GoogleIdentityPlatformConfigMonitoringRequestLogging"]:
        '''request_logging block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#request_logging GoogleIdentityPlatformConfig#request_logging}
        '''
        result = self._values.get("request_logging")
        return typing.cast(typing.Optional["GoogleIdentityPlatformConfigMonitoringRequestLogging"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIdentityPlatformConfigMonitoring(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIdentityPlatformConfigMonitoringOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformConfig.GoogleIdentityPlatformConfigMonitoringOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__203059c233ad1a753c77c26c1349929977a37f0dd08e7116ec67dd2d1da0c16d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRequestLogging")
    def put_request_logging(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Whether logging is enabled for this project or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#enabled GoogleIdentityPlatformConfig#enabled}
        '''
        value = GoogleIdentityPlatformConfigMonitoringRequestLogging(enabled=enabled)

        return typing.cast(None, jsii.invoke(self, "putRequestLogging", [value]))

    @jsii.member(jsii_name="resetRequestLogging")
    def reset_request_logging(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestLogging", []))

    @builtins.property
    @jsii.member(jsii_name="requestLogging")
    def request_logging(
        self,
    ) -> "GoogleIdentityPlatformConfigMonitoringRequestLoggingOutputReference":
        return typing.cast("GoogleIdentityPlatformConfigMonitoringRequestLoggingOutputReference", jsii.get(self, "requestLogging"))

    @builtins.property
    @jsii.member(jsii_name="requestLoggingInput")
    def request_logging_input(
        self,
    ) -> typing.Optional["GoogleIdentityPlatformConfigMonitoringRequestLogging"]:
        return typing.cast(typing.Optional["GoogleIdentityPlatformConfigMonitoringRequestLogging"], jsii.get(self, "requestLoggingInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleIdentityPlatformConfigMonitoring]:
        return typing.cast(typing.Optional[GoogleIdentityPlatformConfigMonitoring], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIdentityPlatformConfigMonitoring],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbefa8755fa6a3646ddf6eb1d6f84a22660d65d79a17ea195409718adbc4e436)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformConfig.GoogleIdentityPlatformConfigMonitoringRequestLogging",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class GoogleIdentityPlatformConfigMonitoringRequestLogging:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Whether logging is enabled for this project or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#enabled GoogleIdentityPlatformConfig#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58bbc80869022df553e6a886e90f023a84eaf7bc8db5fa492da698170b1714f4)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether logging is enabled for this project or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#enabled GoogleIdentityPlatformConfig#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIdentityPlatformConfigMonitoringRequestLogging(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIdentityPlatformConfigMonitoringRequestLoggingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformConfig.GoogleIdentityPlatformConfigMonitoringRequestLoggingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b2669f52275f56ba3202eba95fe52859fd66cfea414ec9f7dc0d83b25ead90b9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__b180df7663e0abb2cf2a698e1e8c4a80809994b0c40e2d639770d4af8f5747a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIdentityPlatformConfigMonitoringRequestLogging]:
        return typing.cast(typing.Optional[GoogleIdentityPlatformConfigMonitoringRequestLogging], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIdentityPlatformConfigMonitoringRequestLogging],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e2d7b785403148d9abacb3fc53168605f21765e0f58272f79b24026672c5cc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformConfig.GoogleIdentityPlatformConfigMultiTenant",
    jsii_struct_bases=[],
    name_mapping={
        "allow_tenants": "allowTenants",
        "default_tenant_location": "defaultTenantLocation",
    },
)
class GoogleIdentityPlatformConfigMultiTenant:
    def __init__(
        self,
        *,
        allow_tenants: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        default_tenant_location: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allow_tenants: Whether this project can have tenants or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#allow_tenants GoogleIdentityPlatformConfig#allow_tenants}
        :param default_tenant_location: The default cloud parent org or folder that the tenant project should be created under. The parent resource name should be in the format of "/", such as "folders/123" or "organizations/456". If the value is not set, the tenant will be created under the same organization or folder as the agent project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#default_tenant_location GoogleIdentityPlatformConfig#default_tenant_location}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__226a802c3ecf50d1ce7935044f37b5c63508baeacf072e943696f64b73ab8a2b)
            check_type(argname="argument allow_tenants", value=allow_tenants, expected_type=type_hints["allow_tenants"])
            check_type(argname="argument default_tenant_location", value=default_tenant_location, expected_type=type_hints["default_tenant_location"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allow_tenants is not None:
            self._values["allow_tenants"] = allow_tenants
        if default_tenant_location is not None:
            self._values["default_tenant_location"] = default_tenant_location

    @builtins.property
    def allow_tenants(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether this project can have tenants or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#allow_tenants GoogleIdentityPlatformConfig#allow_tenants}
        '''
        result = self._values.get("allow_tenants")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def default_tenant_location(self) -> typing.Optional[builtins.str]:
        '''The default cloud parent org or folder that the tenant project should be created under.

        The parent resource name should be in the format of "/", such as "folders/123" or "organizations/456".
        If the value is not set, the tenant will be created under the same organization or folder as the agent project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#default_tenant_location GoogleIdentityPlatformConfig#default_tenant_location}
        '''
        result = self._values.get("default_tenant_location")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIdentityPlatformConfigMultiTenant(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIdentityPlatformConfigMultiTenantOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformConfig.GoogleIdentityPlatformConfigMultiTenantOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e124c7d18a77530d47c84805fbd049de1718b456f48cfb857afadb800e08340b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAllowTenants")
    def reset_allow_tenants(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowTenants", []))

    @jsii.member(jsii_name="resetDefaultTenantLocation")
    def reset_default_tenant_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultTenantLocation", []))

    @builtins.property
    @jsii.member(jsii_name="allowTenantsInput")
    def allow_tenants_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowTenantsInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultTenantLocationInput")
    def default_tenant_location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultTenantLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="allowTenants")
    def allow_tenants(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowTenants"))

    @allow_tenants.setter
    def allow_tenants(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2906aa2649b3fdb6e45507017626a83a820253e232122424e227a7f8d1cb4b24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowTenants", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultTenantLocation")
    def default_tenant_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultTenantLocation"))

    @default_tenant_location.setter
    def default_tenant_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7520be5c6b1a3c629ea7cf592d31d01997123dfba13e1cec841b56b6e48db304)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultTenantLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIdentityPlatformConfigMultiTenant]:
        return typing.cast(typing.Optional[GoogleIdentityPlatformConfigMultiTenant], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIdentityPlatformConfigMultiTenant],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f2695f6fd37e475173b883271fe9cd71118bed1a6fb699dd814a242c88ace1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformConfig.GoogleIdentityPlatformConfigQuota",
    jsii_struct_bases=[],
    name_mapping={"sign_up_quota_config": "signUpQuotaConfig"},
)
class GoogleIdentityPlatformConfigQuota:
    def __init__(
        self,
        *,
        sign_up_quota_config: typing.Optional[typing.Union["GoogleIdentityPlatformConfigQuotaSignUpQuotaConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param sign_up_quota_config: sign_up_quota_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#sign_up_quota_config GoogleIdentityPlatformConfig#sign_up_quota_config}
        '''
        if isinstance(sign_up_quota_config, dict):
            sign_up_quota_config = GoogleIdentityPlatformConfigQuotaSignUpQuotaConfig(**sign_up_quota_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d98b0ebe76f7e6e9fca844775113921e1673aade2f2bb62dcb026394d7b8646)
            check_type(argname="argument sign_up_quota_config", value=sign_up_quota_config, expected_type=type_hints["sign_up_quota_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if sign_up_quota_config is not None:
            self._values["sign_up_quota_config"] = sign_up_quota_config

    @builtins.property
    def sign_up_quota_config(
        self,
    ) -> typing.Optional["GoogleIdentityPlatformConfigQuotaSignUpQuotaConfig"]:
        '''sign_up_quota_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#sign_up_quota_config GoogleIdentityPlatformConfig#sign_up_quota_config}
        '''
        result = self._values.get("sign_up_quota_config")
        return typing.cast(typing.Optional["GoogleIdentityPlatformConfigQuotaSignUpQuotaConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIdentityPlatformConfigQuota(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIdentityPlatformConfigQuotaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformConfig.GoogleIdentityPlatformConfigQuotaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac56b812638aaf22bb149a82e178f02b4c42c6336b6e3468f7979b652c4a715a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSignUpQuotaConfig")
    def put_sign_up_quota_config(
        self,
        *,
        quota: typing.Optional[jsii.Number] = None,
        quota_duration: typing.Optional[builtins.str] = None,
        start_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param quota: A sign up APIs quota that customers can override temporarily. Value can be in between 1 and 1000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#quota GoogleIdentityPlatformConfig#quota}
        :param quota_duration: How long this quota will be active for. It is measurred in seconds, e.g., Example: "9.615s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#quota_duration GoogleIdentityPlatformConfig#quota_duration}
        :param start_time: When this quota will take affect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#start_time GoogleIdentityPlatformConfig#start_time}
        '''
        value = GoogleIdentityPlatformConfigQuotaSignUpQuotaConfig(
            quota=quota, quota_duration=quota_duration, start_time=start_time
        )

        return typing.cast(None, jsii.invoke(self, "putSignUpQuotaConfig", [value]))

    @jsii.member(jsii_name="resetSignUpQuotaConfig")
    def reset_sign_up_quota_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSignUpQuotaConfig", []))

    @builtins.property
    @jsii.member(jsii_name="signUpQuotaConfig")
    def sign_up_quota_config(
        self,
    ) -> "GoogleIdentityPlatformConfigQuotaSignUpQuotaConfigOutputReference":
        return typing.cast("GoogleIdentityPlatformConfigQuotaSignUpQuotaConfigOutputReference", jsii.get(self, "signUpQuotaConfig"))

    @builtins.property
    @jsii.member(jsii_name="signUpQuotaConfigInput")
    def sign_up_quota_config_input(
        self,
    ) -> typing.Optional["GoogleIdentityPlatformConfigQuotaSignUpQuotaConfig"]:
        return typing.cast(typing.Optional["GoogleIdentityPlatformConfigQuotaSignUpQuotaConfig"], jsii.get(self, "signUpQuotaConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleIdentityPlatformConfigQuota]:
        return typing.cast(typing.Optional[GoogleIdentityPlatformConfigQuota], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIdentityPlatformConfigQuota],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a986885c0c9d05260ca48597a7bbfeb2f827e95483b06c1ede6b738ff53b231)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformConfig.GoogleIdentityPlatformConfigQuotaSignUpQuotaConfig",
    jsii_struct_bases=[],
    name_mapping={
        "quota": "quota",
        "quota_duration": "quotaDuration",
        "start_time": "startTime",
    },
)
class GoogleIdentityPlatformConfigQuotaSignUpQuotaConfig:
    def __init__(
        self,
        *,
        quota: typing.Optional[jsii.Number] = None,
        quota_duration: typing.Optional[builtins.str] = None,
        start_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param quota: A sign up APIs quota that customers can override temporarily. Value can be in between 1 and 1000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#quota GoogleIdentityPlatformConfig#quota}
        :param quota_duration: How long this quota will be active for. It is measurred in seconds, e.g., Example: "9.615s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#quota_duration GoogleIdentityPlatformConfig#quota_duration}
        :param start_time: When this quota will take affect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#start_time GoogleIdentityPlatformConfig#start_time}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4dd6a6f79d93692d6ffd7aa47cee1623d50e025a41f5978ce80279e8b9bd4ac)
            check_type(argname="argument quota", value=quota, expected_type=type_hints["quota"])
            check_type(argname="argument quota_duration", value=quota_duration, expected_type=type_hints["quota_duration"])
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if quota is not None:
            self._values["quota"] = quota
        if quota_duration is not None:
            self._values["quota_duration"] = quota_duration
        if start_time is not None:
            self._values["start_time"] = start_time

    @builtins.property
    def quota(self) -> typing.Optional[jsii.Number]:
        '''A sign up APIs quota that customers can override temporarily. Value can be in between 1 and 1000.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#quota GoogleIdentityPlatformConfig#quota}
        '''
        result = self._values.get("quota")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def quota_duration(self) -> typing.Optional[builtins.str]:
        '''How long this quota will be active for. It is measurred in seconds, e.g., Example: "9.615s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#quota_duration GoogleIdentityPlatformConfig#quota_duration}
        '''
        result = self._values.get("quota_duration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start_time(self) -> typing.Optional[builtins.str]:
        '''When this quota will take affect.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#start_time GoogleIdentityPlatformConfig#start_time}
        '''
        result = self._values.get("start_time")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIdentityPlatformConfigQuotaSignUpQuotaConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIdentityPlatformConfigQuotaSignUpQuotaConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformConfig.GoogleIdentityPlatformConfigQuotaSignUpQuotaConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__94eead2bc62a8e734ef7faf4060698783889c157984907739ebdbc8c442dd1f0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetQuota")
    def reset_quota(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQuota", []))

    @jsii.member(jsii_name="resetQuotaDuration")
    def reset_quota_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQuotaDuration", []))

    @jsii.member(jsii_name="resetStartTime")
    def reset_start_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartTime", []))

    @builtins.property
    @jsii.member(jsii_name="quotaDurationInput")
    def quota_duration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "quotaDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="quotaInput")
    def quota_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "quotaInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeInput")
    def start_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="quota")
    def quota(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "quota"))

    @quota.setter
    def quota(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__845c6f2f1e0353424c7d5f82c2a6b57a027a710d543c2d28178bdef51ca3dc85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "quota", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="quotaDuration")
    def quota_duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "quotaDuration"))

    @quota_duration.setter
    def quota_duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bde8fe475e3d923622e99966633f432a12c69155a4eff7858f6f153b9c2893ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "quotaDuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc2b95c7cab0ea58770c431091ae7b514358b65db4022242febfbb1ed381ea71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIdentityPlatformConfigQuotaSignUpQuotaConfig]:
        return typing.cast(typing.Optional[GoogleIdentityPlatformConfigQuotaSignUpQuotaConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIdentityPlatformConfigQuotaSignUpQuotaConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3e3e48b3c67cd1ab1608a1be0fb5234a3c5a85e73e46f4993cff9228185fbe0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformConfig.GoogleIdentityPlatformConfigSignIn",
    jsii_struct_bases=[],
    name_mapping={
        "allow_duplicate_emails": "allowDuplicateEmails",
        "anonymous": "anonymous",
        "email": "email",
        "phone_number": "phoneNumber",
    },
)
class GoogleIdentityPlatformConfigSignIn:
    def __init__(
        self,
        *,
        allow_duplicate_emails: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        anonymous: typing.Optional[typing.Union["GoogleIdentityPlatformConfigSignInAnonymous", typing.Dict[builtins.str, typing.Any]]] = None,
        email: typing.Optional[typing.Union["GoogleIdentityPlatformConfigSignInEmail", typing.Dict[builtins.str, typing.Any]]] = None,
        phone_number: typing.Optional[typing.Union["GoogleIdentityPlatformConfigSignInPhoneNumber", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_duplicate_emails: Whether to allow more than one account to have the same email. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#allow_duplicate_emails GoogleIdentityPlatformConfig#allow_duplicate_emails}
        :param anonymous: anonymous block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#anonymous GoogleIdentityPlatformConfig#anonymous}
        :param email: email block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#email GoogleIdentityPlatformConfig#email}
        :param phone_number: phone_number block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#phone_number GoogleIdentityPlatformConfig#phone_number}
        '''
        if isinstance(anonymous, dict):
            anonymous = GoogleIdentityPlatformConfigSignInAnonymous(**anonymous)
        if isinstance(email, dict):
            email = GoogleIdentityPlatformConfigSignInEmail(**email)
        if isinstance(phone_number, dict):
            phone_number = GoogleIdentityPlatformConfigSignInPhoneNumber(**phone_number)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a7f43e6870f618862c0fc4a6fb8a607000e7a2bbd95f2a45e74763c7a63d667)
            check_type(argname="argument allow_duplicate_emails", value=allow_duplicate_emails, expected_type=type_hints["allow_duplicate_emails"])
            check_type(argname="argument anonymous", value=anonymous, expected_type=type_hints["anonymous"])
            check_type(argname="argument email", value=email, expected_type=type_hints["email"])
            check_type(argname="argument phone_number", value=phone_number, expected_type=type_hints["phone_number"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allow_duplicate_emails is not None:
            self._values["allow_duplicate_emails"] = allow_duplicate_emails
        if anonymous is not None:
            self._values["anonymous"] = anonymous
        if email is not None:
            self._values["email"] = email
        if phone_number is not None:
            self._values["phone_number"] = phone_number

    @builtins.property
    def allow_duplicate_emails(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to allow more than one account to have the same email.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#allow_duplicate_emails GoogleIdentityPlatformConfig#allow_duplicate_emails}
        '''
        result = self._values.get("allow_duplicate_emails")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def anonymous(
        self,
    ) -> typing.Optional["GoogleIdentityPlatformConfigSignInAnonymous"]:
        '''anonymous block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#anonymous GoogleIdentityPlatformConfig#anonymous}
        '''
        result = self._values.get("anonymous")
        return typing.cast(typing.Optional["GoogleIdentityPlatformConfigSignInAnonymous"], result)

    @builtins.property
    def email(self) -> typing.Optional["GoogleIdentityPlatformConfigSignInEmail"]:
        '''email block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#email GoogleIdentityPlatformConfig#email}
        '''
        result = self._values.get("email")
        return typing.cast(typing.Optional["GoogleIdentityPlatformConfigSignInEmail"], result)

    @builtins.property
    def phone_number(
        self,
    ) -> typing.Optional["GoogleIdentityPlatformConfigSignInPhoneNumber"]:
        '''phone_number block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#phone_number GoogleIdentityPlatformConfig#phone_number}
        '''
        result = self._values.get("phone_number")
        return typing.cast(typing.Optional["GoogleIdentityPlatformConfigSignInPhoneNumber"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIdentityPlatformConfigSignIn(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformConfig.GoogleIdentityPlatformConfigSignInAnonymous",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class GoogleIdentityPlatformConfigSignInAnonymous:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Whether anonymous user auth is enabled for the project or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#enabled GoogleIdentityPlatformConfig#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46b4d67995507aec4aabe4b404eebbafb24a25dbfeea4b0c8f3e6fc31d87d30d)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether anonymous user auth is enabled for the project or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#enabled GoogleIdentityPlatformConfig#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIdentityPlatformConfigSignInAnonymous(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIdentityPlatformConfigSignInAnonymousOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformConfig.GoogleIdentityPlatformConfigSignInAnonymousOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__281cba689dbf66ab17d8bdc39d3f54be576fca5f3570286191fb0e9afd664a27)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__86d438273968febf33bacd9068106e8a6f20b450e7a959a91f4d565aef0241f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIdentityPlatformConfigSignInAnonymous]:
        return typing.cast(typing.Optional[GoogleIdentityPlatformConfigSignInAnonymous], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIdentityPlatformConfigSignInAnonymous],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8087a115196e560c5ebd2934f0decedacae3066adda1e034112857559f5e9c04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformConfig.GoogleIdentityPlatformConfigSignInEmail",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "password_required": "passwordRequired"},
)
class GoogleIdentityPlatformConfigSignInEmail:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        password_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Whether email auth is enabled for the project or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#enabled GoogleIdentityPlatformConfig#enabled}
        :param password_required: Whether a password is required for email auth or not. If true, both an email and password must be provided to sign in. If false, a user may sign in via either email/password or email link. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#password_required GoogleIdentityPlatformConfig#password_required}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a21de46d12a029c54282417ac2dcbf67a70cb58abc9c9aa5908bfac046525aa0)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument password_required", value=password_required, expected_type=type_hints["password_required"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }
        if password_required is not None:
            self._values["password_required"] = password_required

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether email auth is enabled for the project or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#enabled GoogleIdentityPlatformConfig#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def password_required(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether a password is required for email auth or not.

        If true, both an email and
        password must be provided to sign in. If false, a user may sign in via either
        email/password or email link.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#password_required GoogleIdentityPlatformConfig#password_required}
        '''
        result = self._values.get("password_required")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIdentityPlatformConfigSignInEmail(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIdentityPlatformConfigSignInEmailOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformConfig.GoogleIdentityPlatformConfigSignInEmailOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__391485f41c3b9d54320324b0c787a0a76aac16649ebef6a5733414824e8edad6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPasswordRequired")
    def reset_password_required(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPasswordRequired", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordRequiredInput")
    def password_required_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "passwordRequiredInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__e9069f48b83ed9b0ae8c00685d1badd4048985474fdfa2050e594b92e90d9ffa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="passwordRequired")
    def password_required(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "passwordRequired"))

    @password_required.setter
    def password_required(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f4b42b9aebbd228c242c65d29bc18c498621c310569471a3798ccc2adbf6db4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passwordRequired", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIdentityPlatformConfigSignInEmail]:
        return typing.cast(typing.Optional[GoogleIdentityPlatformConfigSignInEmail], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIdentityPlatformConfigSignInEmail],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__601a4f0f726bcf81c13ecc049e56823126cd28402cd135f38d5d474a1cf7533d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformConfig.GoogleIdentityPlatformConfigSignInHashConfig",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleIdentityPlatformConfigSignInHashConfig:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIdentityPlatformConfigSignInHashConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIdentityPlatformConfigSignInHashConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformConfig.GoogleIdentityPlatformConfigSignInHashConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__651fee5cd3e05dc92e245d765044efe913322213b64e73d3523cf36a81e2ffb5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleIdentityPlatformConfigSignInHashConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d5d5dc1526b58f79a457d58a06e29aa1f95bbfc1c4b115ff1f49fbe955d6324)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleIdentityPlatformConfigSignInHashConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e060a284ea7ab8fb57674d2849d6260aaaf021649ac39d9ed94f1caf66d24129)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fa23608eb7d945d2891e9c657e036265bdec352447ed4ceb22a66a426fca9197)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3df16a76ebc48660f05e009487e347406e4af42816d960bedb63c95e38455e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleIdentityPlatformConfigSignInHashConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformConfig.GoogleIdentityPlatformConfigSignInHashConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d18e8ba42ef55ad113cb7a8a92b1f135a6b287393a6e67e914fd1176fa9dcda)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="algorithm")
    def algorithm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "algorithm"))

    @builtins.property
    @jsii.member(jsii_name="memoryCost")
    def memory_cost(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memoryCost"))

    @builtins.property
    @jsii.member(jsii_name="rounds")
    def rounds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "rounds"))

    @builtins.property
    @jsii.member(jsii_name="saltSeparator")
    def salt_separator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "saltSeparator"))

    @builtins.property
    @jsii.member(jsii_name="signerKey")
    def signer_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "signerKey"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIdentityPlatformConfigSignInHashConfig]:
        return typing.cast(typing.Optional[GoogleIdentityPlatformConfigSignInHashConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIdentityPlatformConfigSignInHashConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62a8db3de47f0751afe600129719097ef7681c0794f8043c3285c8ed2ff7011c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleIdentityPlatformConfigSignInOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformConfig.GoogleIdentityPlatformConfigSignInOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__80f2a7efcbca1faa5bf0e27181a1bba66cb76e664434dc2574929684e72b0531)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAnonymous")
    def put_anonymous(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Whether anonymous user auth is enabled for the project or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#enabled GoogleIdentityPlatformConfig#enabled}
        '''
        value = GoogleIdentityPlatformConfigSignInAnonymous(enabled=enabled)

        return typing.cast(None, jsii.invoke(self, "putAnonymous", [value]))

    @jsii.member(jsii_name="putEmail")
    def put_email(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        password_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Whether email auth is enabled for the project or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#enabled GoogleIdentityPlatformConfig#enabled}
        :param password_required: Whether a password is required for email auth or not. If true, both an email and password must be provided to sign in. If false, a user may sign in via either email/password or email link. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#password_required GoogleIdentityPlatformConfig#password_required}
        '''
        value = GoogleIdentityPlatformConfigSignInEmail(
            enabled=enabled, password_required=password_required
        )

        return typing.cast(None, jsii.invoke(self, "putEmail", [value]))

    @jsii.member(jsii_name="putPhoneNumber")
    def put_phone_number(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        test_phone_numbers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param enabled: Whether phone number auth is enabled for the project or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#enabled GoogleIdentityPlatformConfig#enabled}
        :param test_phone_numbers: A map of <test phone number, fake code> that can be used for phone auth testing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#test_phone_numbers GoogleIdentityPlatformConfig#test_phone_numbers}
        '''
        value = GoogleIdentityPlatformConfigSignInPhoneNumber(
            enabled=enabled, test_phone_numbers=test_phone_numbers
        )

        return typing.cast(None, jsii.invoke(self, "putPhoneNumber", [value]))

    @jsii.member(jsii_name="resetAllowDuplicateEmails")
    def reset_allow_duplicate_emails(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowDuplicateEmails", []))

    @jsii.member(jsii_name="resetAnonymous")
    def reset_anonymous(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnonymous", []))

    @jsii.member(jsii_name="resetEmail")
    def reset_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmail", []))

    @jsii.member(jsii_name="resetPhoneNumber")
    def reset_phone_number(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPhoneNumber", []))

    @builtins.property
    @jsii.member(jsii_name="anonymous")
    def anonymous(self) -> GoogleIdentityPlatformConfigSignInAnonymousOutputReference:
        return typing.cast(GoogleIdentityPlatformConfigSignInAnonymousOutputReference, jsii.get(self, "anonymous"))

    @builtins.property
    @jsii.member(jsii_name="email")
    def email(self) -> GoogleIdentityPlatformConfigSignInEmailOutputReference:
        return typing.cast(GoogleIdentityPlatformConfigSignInEmailOutputReference, jsii.get(self, "email"))

    @builtins.property
    @jsii.member(jsii_name="hashConfig")
    def hash_config(self) -> GoogleIdentityPlatformConfigSignInHashConfigList:
        return typing.cast(GoogleIdentityPlatformConfigSignInHashConfigList, jsii.get(self, "hashConfig"))

    @builtins.property
    @jsii.member(jsii_name="phoneNumber")
    def phone_number(
        self,
    ) -> "GoogleIdentityPlatformConfigSignInPhoneNumberOutputReference":
        return typing.cast("GoogleIdentityPlatformConfigSignInPhoneNumberOutputReference", jsii.get(self, "phoneNumber"))

    @builtins.property
    @jsii.member(jsii_name="allowDuplicateEmailsInput")
    def allow_duplicate_emails_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowDuplicateEmailsInput"))

    @builtins.property
    @jsii.member(jsii_name="anonymousInput")
    def anonymous_input(
        self,
    ) -> typing.Optional[GoogleIdentityPlatformConfigSignInAnonymous]:
        return typing.cast(typing.Optional[GoogleIdentityPlatformConfigSignInAnonymous], jsii.get(self, "anonymousInput"))

    @builtins.property
    @jsii.member(jsii_name="emailInput")
    def email_input(self) -> typing.Optional[GoogleIdentityPlatformConfigSignInEmail]:
        return typing.cast(typing.Optional[GoogleIdentityPlatformConfigSignInEmail], jsii.get(self, "emailInput"))

    @builtins.property
    @jsii.member(jsii_name="phoneNumberInput")
    def phone_number_input(
        self,
    ) -> typing.Optional["GoogleIdentityPlatformConfigSignInPhoneNumber"]:
        return typing.cast(typing.Optional["GoogleIdentityPlatformConfigSignInPhoneNumber"], jsii.get(self, "phoneNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="allowDuplicateEmails")
    def allow_duplicate_emails(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowDuplicateEmails"))

    @allow_duplicate_emails.setter
    def allow_duplicate_emails(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__079c43d26a2d15726a2b0e8143c532c3c959c7589732801959e814bf7e9ba386)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowDuplicateEmails", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleIdentityPlatformConfigSignIn]:
        return typing.cast(typing.Optional[GoogleIdentityPlatformConfigSignIn], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIdentityPlatformConfigSignIn],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a2e447e8ef7ab5e05e8ea601238e6276928f2b57b063fd78840ff84d688b516)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformConfig.GoogleIdentityPlatformConfigSignInPhoneNumber",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "test_phone_numbers": "testPhoneNumbers"},
)
class GoogleIdentityPlatformConfigSignInPhoneNumber:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        test_phone_numbers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param enabled: Whether phone number auth is enabled for the project or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#enabled GoogleIdentityPlatformConfig#enabled}
        :param test_phone_numbers: A map of <test phone number, fake code> that can be used for phone auth testing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#test_phone_numbers GoogleIdentityPlatformConfig#test_phone_numbers}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85b0f8b8938ef63993ef7b4c8b94220689c2d7146bd92e8172d4d4e2fec7361c)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument test_phone_numbers", value=test_phone_numbers, expected_type=type_hints["test_phone_numbers"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }
        if test_phone_numbers is not None:
            self._values["test_phone_numbers"] = test_phone_numbers

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether phone number auth is enabled for the project or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#enabled GoogleIdentityPlatformConfig#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def test_phone_numbers(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map of <test phone number, fake code> that can be used for phone auth testing.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#test_phone_numbers GoogleIdentityPlatformConfig#test_phone_numbers}
        '''
        result = self._values.get("test_phone_numbers")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIdentityPlatformConfigSignInPhoneNumber(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIdentityPlatformConfigSignInPhoneNumberOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformConfig.GoogleIdentityPlatformConfigSignInPhoneNumberOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5be16f3aaf37b8cccdc347391fd907a11e443b5b320f1318dee2b66626e8071e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetTestPhoneNumbers")
    def reset_test_phone_numbers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTestPhoneNumbers", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="testPhoneNumbersInput")
    def test_phone_numbers_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "testPhoneNumbersInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__581c8401ad046e819a76bc40fedb1ab050984342c8e1436e375a4870528adc42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="testPhoneNumbers")
    def test_phone_numbers(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "testPhoneNumbers"))

    @test_phone_numbers.setter
    def test_phone_numbers(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd5aeaa35aaf81683b3de2c1c02683c013424d8f96225be4f0535f6ddd04f502)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "testPhoneNumbers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIdentityPlatformConfigSignInPhoneNumber]:
        return typing.cast(typing.Optional[GoogleIdentityPlatformConfigSignInPhoneNumber], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIdentityPlatformConfigSignInPhoneNumber],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1b6628b2b6ccc7978de768fab436f089b7ce1cfb1d384bf03a9286e92e649cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformConfig.GoogleIdentityPlatformConfigSmsRegionConfig",
    jsii_struct_bases=[],
    name_mapping={
        "allow_by_default": "allowByDefault",
        "allowlist_only": "allowlistOnly",
    },
)
class GoogleIdentityPlatformConfigSmsRegionConfig:
    def __init__(
        self,
        *,
        allow_by_default: typing.Optional[typing.Union["GoogleIdentityPlatformConfigSmsRegionConfigAllowByDefault", typing.Dict[builtins.str, typing.Any]]] = None,
        allowlist_only: typing.Optional[typing.Union["GoogleIdentityPlatformConfigSmsRegionConfigAllowlistOnly", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_by_default: allow_by_default block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#allow_by_default GoogleIdentityPlatformConfig#allow_by_default}
        :param allowlist_only: allowlist_only block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#allowlist_only GoogleIdentityPlatformConfig#allowlist_only}
        '''
        if isinstance(allow_by_default, dict):
            allow_by_default = GoogleIdentityPlatformConfigSmsRegionConfigAllowByDefault(**allow_by_default)
        if isinstance(allowlist_only, dict):
            allowlist_only = GoogleIdentityPlatformConfigSmsRegionConfigAllowlistOnly(**allowlist_only)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db4776b00142a03658ed201f6e90a1ff867a5683aeeac395ba974163992cfd36)
            check_type(argname="argument allow_by_default", value=allow_by_default, expected_type=type_hints["allow_by_default"])
            check_type(argname="argument allowlist_only", value=allowlist_only, expected_type=type_hints["allowlist_only"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allow_by_default is not None:
            self._values["allow_by_default"] = allow_by_default
        if allowlist_only is not None:
            self._values["allowlist_only"] = allowlist_only

    @builtins.property
    def allow_by_default(
        self,
    ) -> typing.Optional["GoogleIdentityPlatformConfigSmsRegionConfigAllowByDefault"]:
        '''allow_by_default block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#allow_by_default GoogleIdentityPlatformConfig#allow_by_default}
        '''
        result = self._values.get("allow_by_default")
        return typing.cast(typing.Optional["GoogleIdentityPlatformConfigSmsRegionConfigAllowByDefault"], result)

    @builtins.property
    def allowlist_only(
        self,
    ) -> typing.Optional["GoogleIdentityPlatformConfigSmsRegionConfigAllowlistOnly"]:
        '''allowlist_only block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#allowlist_only GoogleIdentityPlatformConfig#allowlist_only}
        '''
        result = self._values.get("allowlist_only")
        return typing.cast(typing.Optional["GoogleIdentityPlatformConfigSmsRegionConfigAllowlistOnly"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIdentityPlatformConfigSmsRegionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformConfig.GoogleIdentityPlatformConfigSmsRegionConfigAllowByDefault",
    jsii_struct_bases=[],
    name_mapping={"disallowed_regions": "disallowedRegions"},
)
class GoogleIdentityPlatformConfigSmsRegionConfigAllowByDefault:
    def __init__(
        self,
        *,
        disallowed_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param disallowed_regions: Two letter unicode region codes to disallow as defined by https://cldr.unicode.org/ The full list of these region codes is here: https://github.com/unicode-cldr/cldr-localenames-full/blob/master/main/en/territories.json. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#disallowed_regions GoogleIdentityPlatformConfig#disallowed_regions}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20b9bbc751366e3de85f16c0c685401683013b57ac2dc3d40c179e459f3b899c)
            check_type(argname="argument disallowed_regions", value=disallowed_regions, expected_type=type_hints["disallowed_regions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if disallowed_regions is not None:
            self._values["disallowed_regions"] = disallowed_regions

    @builtins.property
    def disallowed_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Two letter unicode region codes to disallow as defined by https://cldr.unicode.org/ The full list of these region codes is here: https://github.com/unicode-cldr/cldr-localenames-full/blob/master/main/en/territories.json.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#disallowed_regions GoogleIdentityPlatformConfig#disallowed_regions}
        '''
        result = self._values.get("disallowed_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIdentityPlatformConfigSmsRegionConfigAllowByDefault(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIdentityPlatformConfigSmsRegionConfigAllowByDefaultOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformConfig.GoogleIdentityPlatformConfigSmsRegionConfigAllowByDefaultOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__416465784549a65012da91b0b97bd047da76226ef4c6e8bfb47f87611795dc6e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDisallowedRegions")
    def reset_disallowed_regions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisallowedRegions", []))

    @builtins.property
    @jsii.member(jsii_name="disallowedRegionsInput")
    def disallowed_regions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "disallowedRegionsInput"))

    @builtins.property
    @jsii.member(jsii_name="disallowedRegions")
    def disallowed_regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "disallowedRegions"))

    @disallowed_regions.setter
    def disallowed_regions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c32de9370b87518cbc3b13e5435ace3e966a904ea9a1f26f8b28736330d607b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disallowedRegions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIdentityPlatformConfigSmsRegionConfigAllowByDefault]:
        return typing.cast(typing.Optional[GoogleIdentityPlatformConfigSmsRegionConfigAllowByDefault], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIdentityPlatformConfigSmsRegionConfigAllowByDefault],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2fa9a5accdd6be5b4a58ecad3321edee8d3cc169b008f4b8b8a5d08d3723bbf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformConfig.GoogleIdentityPlatformConfigSmsRegionConfigAllowlistOnly",
    jsii_struct_bases=[],
    name_mapping={"allowed_regions": "allowedRegions"},
)
class GoogleIdentityPlatformConfigSmsRegionConfigAllowlistOnly:
    def __init__(
        self,
        *,
        allowed_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param allowed_regions: Two letter unicode region codes to allow as defined by https://cldr.unicode.org/ The full list of these region codes is here: https://github.com/unicode-cldr/cldr-localenames-full/blob/master/main/en/territories.json. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#allowed_regions GoogleIdentityPlatformConfig#allowed_regions}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f8a76c229f695d1a882e2559e1bfda6f6b3108bc868c34bf8ace3f2ebe00ea9)
            check_type(argname="argument allowed_regions", value=allowed_regions, expected_type=type_hints["allowed_regions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allowed_regions is not None:
            self._values["allowed_regions"] = allowed_regions

    @builtins.property
    def allowed_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Two letter unicode region codes to allow as defined by https://cldr.unicode.org/ The full list of these region codes is here: https://github.com/unicode-cldr/cldr-localenames-full/blob/master/main/en/territories.json.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#allowed_regions GoogleIdentityPlatformConfig#allowed_regions}
        '''
        result = self._values.get("allowed_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIdentityPlatformConfigSmsRegionConfigAllowlistOnly(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIdentityPlatformConfigSmsRegionConfigAllowlistOnlyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformConfig.GoogleIdentityPlatformConfigSmsRegionConfigAllowlistOnlyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c75d7be641bb3cd1f3f860ee224428e51739873c254260162fcb861e0dcaf69)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAllowedRegions")
    def reset_allowed_regions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedRegions", []))

    @builtins.property
    @jsii.member(jsii_name="allowedRegionsInput")
    def allowed_regions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedRegionsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedRegions")
    def allowed_regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedRegions"))

    @allowed_regions.setter
    def allowed_regions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1220593239539114c1a6e6a2b4404ee511918fce560c8a6060b1799edd874d58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedRegions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIdentityPlatformConfigSmsRegionConfigAllowlistOnly]:
        return typing.cast(typing.Optional[GoogleIdentityPlatformConfigSmsRegionConfigAllowlistOnly], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIdentityPlatformConfigSmsRegionConfigAllowlistOnly],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9643979a0a6faac6262fea32cddfdef06b22f8d9cfd98d8d8b661846e2ed4d89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleIdentityPlatformConfigSmsRegionConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformConfig.GoogleIdentityPlatformConfigSmsRegionConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd9c4da54fa2e79f955a96bda8cc4beb3fde2a809a09cef0ba12634808087a35)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAllowByDefault")
    def put_allow_by_default(
        self,
        *,
        disallowed_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param disallowed_regions: Two letter unicode region codes to disallow as defined by https://cldr.unicode.org/ The full list of these region codes is here: https://github.com/unicode-cldr/cldr-localenames-full/blob/master/main/en/territories.json. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#disallowed_regions GoogleIdentityPlatformConfig#disallowed_regions}
        '''
        value = GoogleIdentityPlatformConfigSmsRegionConfigAllowByDefault(
            disallowed_regions=disallowed_regions
        )

        return typing.cast(None, jsii.invoke(self, "putAllowByDefault", [value]))

    @jsii.member(jsii_name="putAllowlistOnly")
    def put_allowlist_only(
        self,
        *,
        allowed_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param allowed_regions: Two letter unicode region codes to allow as defined by https://cldr.unicode.org/ The full list of these region codes is here: https://github.com/unicode-cldr/cldr-localenames-full/blob/master/main/en/territories.json. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#allowed_regions GoogleIdentityPlatformConfig#allowed_regions}
        '''
        value = GoogleIdentityPlatformConfigSmsRegionConfigAllowlistOnly(
            allowed_regions=allowed_regions
        )

        return typing.cast(None, jsii.invoke(self, "putAllowlistOnly", [value]))

    @jsii.member(jsii_name="resetAllowByDefault")
    def reset_allow_by_default(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowByDefault", []))

    @jsii.member(jsii_name="resetAllowlistOnly")
    def reset_allowlist_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowlistOnly", []))

    @builtins.property
    @jsii.member(jsii_name="allowByDefault")
    def allow_by_default(
        self,
    ) -> GoogleIdentityPlatformConfigSmsRegionConfigAllowByDefaultOutputReference:
        return typing.cast(GoogleIdentityPlatformConfigSmsRegionConfigAllowByDefaultOutputReference, jsii.get(self, "allowByDefault"))

    @builtins.property
    @jsii.member(jsii_name="allowlistOnly")
    def allowlist_only(
        self,
    ) -> GoogleIdentityPlatformConfigSmsRegionConfigAllowlistOnlyOutputReference:
        return typing.cast(GoogleIdentityPlatformConfigSmsRegionConfigAllowlistOnlyOutputReference, jsii.get(self, "allowlistOnly"))

    @builtins.property
    @jsii.member(jsii_name="allowByDefaultInput")
    def allow_by_default_input(
        self,
    ) -> typing.Optional[GoogleIdentityPlatformConfigSmsRegionConfigAllowByDefault]:
        return typing.cast(typing.Optional[GoogleIdentityPlatformConfigSmsRegionConfigAllowByDefault], jsii.get(self, "allowByDefaultInput"))

    @builtins.property
    @jsii.member(jsii_name="allowlistOnlyInput")
    def allowlist_only_input(
        self,
    ) -> typing.Optional[GoogleIdentityPlatformConfigSmsRegionConfigAllowlistOnly]:
        return typing.cast(typing.Optional[GoogleIdentityPlatformConfigSmsRegionConfigAllowlistOnly], jsii.get(self, "allowlistOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIdentityPlatformConfigSmsRegionConfig]:
        return typing.cast(typing.Optional[GoogleIdentityPlatformConfigSmsRegionConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIdentityPlatformConfigSmsRegionConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2faa982811b2f50695e0a1f35fe9a8978fd4d511104bebd77915b43e39985e86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformConfig.GoogleIdentityPlatformConfigTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleIdentityPlatformConfigTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#create GoogleIdentityPlatformConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#delete GoogleIdentityPlatformConfig#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#update GoogleIdentityPlatformConfig#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5556e26d89c8d6201715a0a3ea716f4ae344d2b1c73063b8401a418067b7914)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#create GoogleIdentityPlatformConfig#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#delete GoogleIdentityPlatformConfig#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_identity_platform_config#update GoogleIdentityPlatformConfig#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIdentityPlatformConfigTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIdentityPlatformConfigTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformConfig.GoogleIdentityPlatformConfigTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__47977a805017c893a1f555f0f98cb096f9e8b948ef1aa97d24ad3b04ee979fc1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9dd64e6a20b1b6c495bd5d3b663d0be37699afec373eb513f49cb1e186f6117d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ade2541fe85cb51a427d418e9b502c28d2a6037adcdbb9aae5614ddc3dc13774)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e357fadd88601fbd87a168c2c13b57be5c4c4713e918b917f75bf7937d3fe368)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIdentityPlatformConfigTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIdentityPlatformConfigTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIdentityPlatformConfigTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca230490c66e1128fe5ab5ec342fc5bb7ac1cfbb9c8bd65a501663ce345a481e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleIdentityPlatformConfig",
    "GoogleIdentityPlatformConfigBlockingFunctions",
    "GoogleIdentityPlatformConfigBlockingFunctionsForwardInboundCredentials",
    "GoogleIdentityPlatformConfigBlockingFunctionsForwardInboundCredentialsOutputReference",
    "GoogleIdentityPlatformConfigBlockingFunctionsOutputReference",
    "GoogleIdentityPlatformConfigBlockingFunctionsTriggers",
    "GoogleIdentityPlatformConfigBlockingFunctionsTriggersList",
    "GoogleIdentityPlatformConfigBlockingFunctionsTriggersOutputReference",
    "GoogleIdentityPlatformConfigClient",
    "GoogleIdentityPlatformConfigClientOutputReference",
    "GoogleIdentityPlatformConfigClientPermissions",
    "GoogleIdentityPlatformConfigClientPermissionsOutputReference",
    "GoogleIdentityPlatformConfigConfig",
    "GoogleIdentityPlatformConfigMfa",
    "GoogleIdentityPlatformConfigMfaOutputReference",
    "GoogleIdentityPlatformConfigMfaProviderConfigs",
    "GoogleIdentityPlatformConfigMfaProviderConfigsList",
    "GoogleIdentityPlatformConfigMfaProviderConfigsOutputReference",
    "GoogleIdentityPlatformConfigMfaProviderConfigsTotpProviderConfig",
    "GoogleIdentityPlatformConfigMfaProviderConfigsTotpProviderConfigOutputReference",
    "GoogleIdentityPlatformConfigMonitoring",
    "GoogleIdentityPlatformConfigMonitoringOutputReference",
    "GoogleIdentityPlatformConfigMonitoringRequestLogging",
    "GoogleIdentityPlatformConfigMonitoringRequestLoggingOutputReference",
    "GoogleIdentityPlatformConfigMultiTenant",
    "GoogleIdentityPlatformConfigMultiTenantOutputReference",
    "GoogleIdentityPlatformConfigQuota",
    "GoogleIdentityPlatformConfigQuotaOutputReference",
    "GoogleIdentityPlatformConfigQuotaSignUpQuotaConfig",
    "GoogleIdentityPlatformConfigQuotaSignUpQuotaConfigOutputReference",
    "GoogleIdentityPlatformConfigSignIn",
    "GoogleIdentityPlatformConfigSignInAnonymous",
    "GoogleIdentityPlatformConfigSignInAnonymousOutputReference",
    "GoogleIdentityPlatformConfigSignInEmail",
    "GoogleIdentityPlatformConfigSignInEmailOutputReference",
    "GoogleIdentityPlatformConfigSignInHashConfig",
    "GoogleIdentityPlatformConfigSignInHashConfigList",
    "GoogleIdentityPlatformConfigSignInHashConfigOutputReference",
    "GoogleIdentityPlatformConfigSignInOutputReference",
    "GoogleIdentityPlatformConfigSignInPhoneNumber",
    "GoogleIdentityPlatformConfigSignInPhoneNumberOutputReference",
    "GoogleIdentityPlatformConfigSmsRegionConfig",
    "GoogleIdentityPlatformConfigSmsRegionConfigAllowByDefault",
    "GoogleIdentityPlatformConfigSmsRegionConfigAllowByDefaultOutputReference",
    "GoogleIdentityPlatformConfigSmsRegionConfigAllowlistOnly",
    "GoogleIdentityPlatformConfigSmsRegionConfigAllowlistOnlyOutputReference",
    "GoogleIdentityPlatformConfigSmsRegionConfigOutputReference",
    "GoogleIdentityPlatformConfigTimeouts",
    "GoogleIdentityPlatformConfigTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__4312f084d832f9f93da5084069dfe91ece481d88685ba5f9e10c685b42a70ba0(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    authorized_domains: typing.Optional[typing.Sequence[builtins.str]] = None,
    autodelete_anonymous_users: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    blocking_functions: typing.Optional[typing.Union[GoogleIdentityPlatformConfigBlockingFunctions, typing.Dict[builtins.str, typing.Any]]] = None,
    client: typing.Optional[typing.Union[GoogleIdentityPlatformConfigClient, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    mfa: typing.Optional[typing.Union[GoogleIdentityPlatformConfigMfa, typing.Dict[builtins.str, typing.Any]]] = None,
    monitoring: typing.Optional[typing.Union[GoogleIdentityPlatformConfigMonitoring, typing.Dict[builtins.str, typing.Any]]] = None,
    multi_tenant: typing.Optional[typing.Union[GoogleIdentityPlatformConfigMultiTenant, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    quota: typing.Optional[typing.Union[GoogleIdentityPlatformConfigQuota, typing.Dict[builtins.str, typing.Any]]] = None,
    sign_in: typing.Optional[typing.Union[GoogleIdentityPlatformConfigSignIn, typing.Dict[builtins.str, typing.Any]]] = None,
    sms_region_config: typing.Optional[typing.Union[GoogleIdentityPlatformConfigSmsRegionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleIdentityPlatformConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__ba032ddfdd5ffe37128d34032eaee2af1806089a183b36cfdc4e10837c951556(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba6bba04ed831e6d658275035e1712c220185a20a89175cafa467a9f9a063b10(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b69e944ee15ea1fca1d15dfe0206c5c93fbb90eab2b3fed2e76394b185d38594(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9ffd676711ee304a2f67b67a45241b02ccb77b283bcaf2d410baa8394ae2283(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da00d7ef74141ec56423b5470d86c28b839dc1a80634b9b4409ddb02d445aa84(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e760b62a4ebf752e5a28ec528d3ddb67e173f2964070e49af5e068d8e647c89b(
    *,
    triggers: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleIdentityPlatformConfigBlockingFunctionsTriggers, typing.Dict[builtins.str, typing.Any]]]],
    forward_inbound_credentials: typing.Optional[typing.Union[GoogleIdentityPlatformConfigBlockingFunctionsForwardInboundCredentials, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b5e9f0f21c65f1e68fafc7f7e999939bee330ef374023061efb61bcb26028bb(
    *,
    access_token: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id_token: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    refresh_token: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__262eb45a7a724798a5251622822d5622ba183dc9b5744f50571851b6a5ad0171(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c7c659e383a95194fdbc28da76769f05cd4c248e0da1d19168cab3943cc02f7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__519d09bcb79d67294f25021e06bfe6d0b18b52f790a18f86c1c17abdb217d0f1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e2e316be60ba19affc3b8c38f345b6ed4398d02b6ee1fb5709167ee04a2c91c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d21057ba622f0922bff29ddba3656f044a0cc73238804ec9a64a3f56de78556(
    value: typing.Optional[GoogleIdentityPlatformConfigBlockingFunctionsForwardInboundCredentials],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d87f8255b76515af500c37f64de8cfca187f939e1249411efdb754b6d8c3691(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__398b263ea25f410cb0050565af7c92f6e102b5d6015b4cdc0c076f12826c920d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleIdentityPlatformConfigBlockingFunctionsTriggers, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef3cf4350abc132dd59cc84c6cff90ace361ccdc01c2d931e71f21870b94fa0d(
    value: typing.Optional[GoogleIdentityPlatformConfigBlockingFunctions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da792164b4d269f5c1fcf2ede0584376c10adf486cae79d82e5e5fc45e966f37(
    *,
    event_type: builtins.str,
    function_uri: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7e63e1e0d62e6127b28797e9207c1247ae1f550b9c8632a7eef1dfa80535289(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__616a6b6480b0158c9d4249025445fe2b38ae20a95f3c3bcc89f177282103f769(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddfff4bb9e2ff1b0f468b09154baf34b6296ac1359a001b40cb586bad10041f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6040c424009d28a7661f21505a35f443554c804407b697e16c5c8377ee13274(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__267f9fd8a589daa32d3b480514f08926dac26cc2e77eafac533edfc88dba91c6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc0a959e25f15fb8578ac42f92850338cc1b574134d5f523953d490678a90ab0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIdentityPlatformConfigBlockingFunctionsTriggers]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2afd3a6ff4cb246d680be9933dfcd7dde66702f0929ccbf7dbcf0b5035e5119(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eca8be2d54e7b0d998fa3deae3ad348b2f3ded1b761ac570f60512c16bae530e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00b328dc3fd0137c9927b68309f1e74ea76e1d691fbdf084059b2ff525f6cba9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d4709dec81844de7eec6aa6fdd321a6784d23964ea66746e04ab1d1b5b1b597(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIdentityPlatformConfigBlockingFunctionsTriggers]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f188d4551fd12632e56fd6e9c1853885c4dbdaf80e048ccdbba13f93c12f6cb9(
    *,
    permissions: typing.Optional[typing.Union[GoogleIdentityPlatformConfigClientPermissions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d555ad76c73176c7fc03ee725acccca8638fb80fdd7f2be19dfc632d0efb940(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e053de35c3a7e11d51243f2d71ae9158ad1c507bb1d0b238f34882f3a6f87715(
    value: typing.Optional[GoogleIdentityPlatformConfigClient],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be044133d9fa5d2b098fdfdafd8f71355747e34d32017d61323a9f790fabf44e(
    *,
    disabled_user_deletion: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disabled_user_signup: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7465ce84e473b422d9afdf88bb40021b6110e88de5266209193a9856e627786(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5511410f416ab8bb3970cbd4c1fe538b482d02e9389d609b202d82cbf203b6f0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20bb536b927bc7a405a0fc6779a10977d3bd47a82f98f0d4469d00ee5958772b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82764503b1a7744dd2dd7a9532accbeb0be764a759db4c2646e9d1a2e6b4bfd8(
    value: typing.Optional[GoogleIdentityPlatformConfigClientPermissions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0865745b6f40a84c0cf16ad1d456019a31ec0a068a697d8ae97b69cd465dab73(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    authorized_domains: typing.Optional[typing.Sequence[builtins.str]] = None,
    autodelete_anonymous_users: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    blocking_functions: typing.Optional[typing.Union[GoogleIdentityPlatformConfigBlockingFunctions, typing.Dict[builtins.str, typing.Any]]] = None,
    client: typing.Optional[typing.Union[GoogleIdentityPlatformConfigClient, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    mfa: typing.Optional[typing.Union[GoogleIdentityPlatformConfigMfa, typing.Dict[builtins.str, typing.Any]]] = None,
    monitoring: typing.Optional[typing.Union[GoogleIdentityPlatformConfigMonitoring, typing.Dict[builtins.str, typing.Any]]] = None,
    multi_tenant: typing.Optional[typing.Union[GoogleIdentityPlatformConfigMultiTenant, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    quota: typing.Optional[typing.Union[GoogleIdentityPlatformConfigQuota, typing.Dict[builtins.str, typing.Any]]] = None,
    sign_in: typing.Optional[typing.Union[GoogleIdentityPlatformConfigSignIn, typing.Dict[builtins.str, typing.Any]]] = None,
    sms_region_config: typing.Optional[typing.Union[GoogleIdentityPlatformConfigSmsRegionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleIdentityPlatformConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b18702fffe3caffd16c3ae5f2c904a7e1e8a3e4da8029686384e2b43fc7e85c(
    *,
    enabled_providers: typing.Optional[typing.Sequence[builtins.str]] = None,
    provider_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleIdentityPlatformConfigMfaProviderConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    state: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be4bca7e4553de0ddba65462033c02814236ba5ef7326a74621d6cba01657153(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__568f402db9ea425819cc8f7b8bfcc4865961b63d6882d51ab2b291de16376e43(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleIdentityPlatformConfigMfaProviderConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b68ef2fe2b9660762fbaee9bd4d27f7cb0d844508c4a183d098e209d725bd402(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a35fa5946e093ae7399e5c4871a1a40c96d9d9a99e51d69ab87b9d86a4f3ed8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ee14ae177b281551aab39bd2f196c42dc7c7ed756d04f3deabdf283d48fb396(
    value: typing.Optional[GoogleIdentityPlatformConfigMfa],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e17fa3beefe666917575254fb3bdbb8cc57f24cf897ab882090e9a1c9a640726(
    *,
    state: typing.Optional[builtins.str] = None,
    totp_provider_config: typing.Optional[typing.Union[GoogleIdentityPlatformConfigMfaProviderConfigsTotpProviderConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__699d87b28a8b53f26a4cd42591a9582d6e87cd69e8c82523b2e4e6510c724dae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7174a7e6885231fa164783ac1dec577dc902aba0c0dcaac91172fb7d8366497(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58a2e9c397ab0ff5247bb73bd63c0fabba6a55d0f19519db327b94e7fb9e2c4f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65c9bdcf0f0b6072b189a694755f2c4b857eae7f564a64d9b1eeebdbb7ab975d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97613a43c7c620b6b2a7fb5d4063f937bb0364317568c2fa33ff2b3ad20682d2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e3cd536686b10d665bef790c20356e8a24bcfb864b1919f612c0eb45c97bd95(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIdentityPlatformConfigMfaProviderConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d5cc9603ea077e6ebf6cdde47d81b12b1e9a3dfc99e58a828ff559f352c53f8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2a2320f505b8459e7e74f16c07467f95d33128146bbe01c076c34e2b8032bfe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b96cec9a84e64981f162138b2769154f2685ab7fc964531ca989a932cdfbbf88(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIdentityPlatformConfigMfaProviderConfigs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__715e84f5ecf14e42b6870e7184047c850497c86c74d2a9c7b9fc69e3b46c5607(
    *,
    adjacent_intervals: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5799b2e970021ac862452fea19a00c2002bc147a081f4aa428b02408e767f838(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f537f9f3df0e0b41d9fb26a5dbc5bf919c27ee5dd4c9f4198bc77a54bef6b21a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf9a10641cb1d67794fe47107f12ff086ea192de8098777e043883ad8129670e(
    value: typing.Optional[GoogleIdentityPlatformConfigMfaProviderConfigsTotpProviderConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54132a9fee1d05bdf1cac5db671f66f7b0bc2fa98b6bbf3ce99628e3c1a9912b(
    *,
    request_logging: typing.Optional[typing.Union[GoogleIdentityPlatformConfigMonitoringRequestLogging, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__203059c233ad1a753c77c26c1349929977a37f0dd08e7116ec67dd2d1da0c16d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbefa8755fa6a3646ddf6eb1d6f84a22660d65d79a17ea195409718adbc4e436(
    value: typing.Optional[GoogleIdentityPlatformConfigMonitoring],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58bbc80869022df553e6a886e90f023a84eaf7bc8db5fa492da698170b1714f4(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2669f52275f56ba3202eba95fe52859fd66cfea414ec9f7dc0d83b25ead90b9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b180df7663e0abb2cf2a698e1e8c4a80809994b0c40e2d639770d4af8f5747a7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e2d7b785403148d9abacb3fc53168605f21765e0f58272f79b24026672c5cc0(
    value: typing.Optional[GoogleIdentityPlatformConfigMonitoringRequestLogging],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__226a802c3ecf50d1ce7935044f37b5c63508baeacf072e943696f64b73ab8a2b(
    *,
    allow_tenants: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    default_tenant_location: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e124c7d18a77530d47c84805fbd049de1718b456f48cfb857afadb800e08340b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2906aa2649b3fdb6e45507017626a83a820253e232122424e227a7f8d1cb4b24(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7520be5c6b1a3c629ea7cf592d31d01997123dfba13e1cec841b56b6e48db304(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f2695f6fd37e475173b883271fe9cd71118bed1a6fb699dd814a242c88ace1a(
    value: typing.Optional[GoogleIdentityPlatformConfigMultiTenant],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d98b0ebe76f7e6e9fca844775113921e1673aade2f2bb62dcb026394d7b8646(
    *,
    sign_up_quota_config: typing.Optional[typing.Union[GoogleIdentityPlatformConfigQuotaSignUpQuotaConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac56b812638aaf22bb149a82e178f02b4c42c6336b6e3468f7979b652c4a715a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a986885c0c9d05260ca48597a7bbfeb2f827e95483b06c1ede6b738ff53b231(
    value: typing.Optional[GoogleIdentityPlatformConfigQuota],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4dd6a6f79d93692d6ffd7aa47cee1623d50e025a41f5978ce80279e8b9bd4ac(
    *,
    quota: typing.Optional[jsii.Number] = None,
    quota_duration: typing.Optional[builtins.str] = None,
    start_time: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94eead2bc62a8e734ef7faf4060698783889c157984907739ebdbc8c442dd1f0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__845c6f2f1e0353424c7d5f82c2a6b57a027a710d543c2d28178bdef51ca3dc85(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bde8fe475e3d923622e99966633f432a12c69155a4eff7858f6f153b9c2893ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc2b95c7cab0ea58770c431091ae7b514358b65db4022242febfbb1ed381ea71(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3e3e48b3c67cd1ab1608a1be0fb5234a3c5a85e73e46f4993cff9228185fbe0(
    value: typing.Optional[GoogleIdentityPlatformConfigQuotaSignUpQuotaConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a7f43e6870f618862c0fc4a6fb8a607000e7a2bbd95f2a45e74763c7a63d667(
    *,
    allow_duplicate_emails: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    anonymous: typing.Optional[typing.Union[GoogleIdentityPlatformConfigSignInAnonymous, typing.Dict[builtins.str, typing.Any]]] = None,
    email: typing.Optional[typing.Union[GoogleIdentityPlatformConfigSignInEmail, typing.Dict[builtins.str, typing.Any]]] = None,
    phone_number: typing.Optional[typing.Union[GoogleIdentityPlatformConfigSignInPhoneNumber, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46b4d67995507aec4aabe4b404eebbafb24a25dbfeea4b0c8f3e6fc31d87d30d(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__281cba689dbf66ab17d8bdc39d3f54be576fca5f3570286191fb0e9afd664a27(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86d438273968febf33bacd9068106e8a6f20b450e7a959a91f4d565aef0241f3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8087a115196e560c5ebd2934f0decedacae3066adda1e034112857559f5e9c04(
    value: typing.Optional[GoogleIdentityPlatformConfigSignInAnonymous],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a21de46d12a029c54282417ac2dcbf67a70cb58abc9c9aa5908bfac046525aa0(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    password_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__391485f41c3b9d54320324b0c787a0a76aac16649ebef6a5733414824e8edad6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9069f48b83ed9b0ae8c00685d1badd4048985474fdfa2050e594b92e90d9ffa(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f4b42b9aebbd228c242c65d29bc18c498621c310569471a3798ccc2adbf6db4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__601a4f0f726bcf81c13ecc049e56823126cd28402cd135f38d5d474a1cf7533d(
    value: typing.Optional[GoogleIdentityPlatformConfigSignInEmail],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__651fee5cd3e05dc92e245d765044efe913322213b64e73d3523cf36a81e2ffb5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d5d5dc1526b58f79a457d58a06e29aa1f95bbfc1c4b115ff1f49fbe955d6324(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e060a284ea7ab8fb57674d2849d6260aaaf021649ac39d9ed94f1caf66d24129(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa23608eb7d945d2891e9c657e036265bdec352447ed4ceb22a66a426fca9197(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3df16a76ebc48660f05e009487e347406e4af42816d960bedb63c95e38455e3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d18e8ba42ef55ad113cb7a8a92b1f135a6b287393a6e67e914fd1176fa9dcda(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62a8db3de47f0751afe600129719097ef7681c0794f8043c3285c8ed2ff7011c(
    value: typing.Optional[GoogleIdentityPlatformConfigSignInHashConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80f2a7efcbca1faa5bf0e27181a1bba66cb76e664434dc2574929684e72b0531(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__079c43d26a2d15726a2b0e8143c532c3c959c7589732801959e814bf7e9ba386(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a2e447e8ef7ab5e05e8ea601238e6276928f2b57b063fd78840ff84d688b516(
    value: typing.Optional[GoogleIdentityPlatformConfigSignIn],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85b0f8b8938ef63993ef7b4c8b94220689c2d7146bd92e8172d4d4e2fec7361c(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    test_phone_numbers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5be16f3aaf37b8cccdc347391fd907a11e443b5b320f1318dee2b66626e8071e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__581c8401ad046e819a76bc40fedb1ab050984342c8e1436e375a4870528adc42(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd5aeaa35aaf81683b3de2c1c02683c013424d8f96225be4f0535f6ddd04f502(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1b6628b2b6ccc7978de768fab436f089b7ce1cfb1d384bf03a9286e92e649cf(
    value: typing.Optional[GoogleIdentityPlatformConfigSignInPhoneNumber],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db4776b00142a03658ed201f6e90a1ff867a5683aeeac395ba974163992cfd36(
    *,
    allow_by_default: typing.Optional[typing.Union[GoogleIdentityPlatformConfigSmsRegionConfigAllowByDefault, typing.Dict[builtins.str, typing.Any]]] = None,
    allowlist_only: typing.Optional[typing.Union[GoogleIdentityPlatformConfigSmsRegionConfigAllowlistOnly, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20b9bbc751366e3de85f16c0c685401683013b57ac2dc3d40c179e459f3b899c(
    *,
    disallowed_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__416465784549a65012da91b0b97bd047da76226ef4c6e8bfb47f87611795dc6e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c32de9370b87518cbc3b13e5435ace3e966a904ea9a1f26f8b28736330d607b6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2fa9a5accdd6be5b4a58ecad3321edee8d3cc169b008f4b8b8a5d08d3723bbf(
    value: typing.Optional[GoogleIdentityPlatformConfigSmsRegionConfigAllowByDefault],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f8a76c229f695d1a882e2559e1bfda6f6b3108bc868c34bf8ace3f2ebe00ea9(
    *,
    allowed_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c75d7be641bb3cd1f3f860ee224428e51739873c254260162fcb861e0dcaf69(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1220593239539114c1a6e6a2b4404ee511918fce560c8a6060b1799edd874d58(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9643979a0a6faac6262fea32cddfdef06b22f8d9cfd98d8d8b661846e2ed4d89(
    value: typing.Optional[GoogleIdentityPlatformConfigSmsRegionConfigAllowlistOnly],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd9c4da54fa2e79f955a96bda8cc4beb3fde2a809a09cef0ba12634808087a35(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2faa982811b2f50695e0a1f35fe9a8978fd4d511104bebd77915b43e39985e86(
    value: typing.Optional[GoogleIdentityPlatformConfigSmsRegionConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5556e26d89c8d6201715a0a3ea716f4ae344d2b1c73063b8401a418067b7914(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47977a805017c893a1f555f0f98cb096f9e8b948ef1aa97d24ad3b04ee979fc1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dd64e6a20b1b6c495bd5d3b663d0be37699afec373eb513f49cb1e186f6117d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ade2541fe85cb51a427d418e9b502c28d2a6037adcdbb9aae5614ddc3dc13774(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e357fadd88601fbd87a168c2c13b57be5c4c4713e918b917f75bf7937d3fe368(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca230490c66e1128fe5ab5ec342fc5bb7ac1cfbb9c8bd65a501663ce345a481e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIdentityPlatformConfigTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
