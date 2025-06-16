r'''
# `google_iap_settings`

Refer to the Terraform Registry for docs: [`google_iap_settings`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings).
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


class GoogleIapSettings(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIapSettings.GoogleIapSettings",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings google_iap_settings}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        access_settings: typing.Optional[typing.Union["GoogleIapSettingsAccessSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        application_settings: typing.Optional[typing.Union["GoogleIapSettingsApplicationSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleIapSettingsTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings google_iap_settings} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: The resource name of the IAP protected resource. Name can have below resources: - organizations/{organization_id} - folders/{folder_id} - projects/{project_id} - projects/{project_id}/iap_web - projects/{project_id}/iap_web/compute - projects/{project_id}/iap_web/compute-{region} - projects/{project_id}/iap_web/compute/services/{service_id} - projects/{project_id}/iap_web/compute-{region}/services/{service_id} - projects/{project_id}/iap_web/appengine-{app_id} - projects/{project_id}/iap_web/appengine-{app_id}/services/{service_id} - projects/{project_id}/iap_web/appengine-{app_id}/services/{service_id}/version/{version_id} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#name GoogleIapSettings#name}
        :param access_settings: access_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#access_settings GoogleIapSettings#access_settings}
        :param application_settings: application_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#application_settings GoogleIapSettings#application_settings}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#id GoogleIapSettings#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#timeouts GoogleIapSettings#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__611cd777bb5dff5822d68548397ddcf57684e40e404c93e00b687e7301b7d106)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleIapSettingsConfig(
            name=name,
            access_settings=access_settings,
            application_settings=application_settings,
            id=id,
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
        '''Generates CDKTF code for importing a GoogleIapSettings resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleIapSettings to import.
        :param import_from_id: The id of the existing GoogleIapSettings that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleIapSettings to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfe672fe20a7e58d70291b0219bdd098905301b6ff800b3a546733e3c33d8fbb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAccessSettings")
    def put_access_settings(
        self,
        *,
        allowed_domains_settings: typing.Optional[typing.Union["GoogleIapSettingsAccessSettingsAllowedDomainsSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        cors_settings: typing.Optional[typing.Union["GoogleIapSettingsAccessSettingsCorsSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        gcip_settings: typing.Optional[typing.Union["GoogleIapSettingsAccessSettingsGcipSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        identity_sources: typing.Optional[typing.Sequence[builtins.str]] = None,
        oauth_settings: typing.Optional[typing.Union["GoogleIapSettingsAccessSettingsOauthSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        reauth_settings: typing.Optional[typing.Union["GoogleIapSettingsAccessSettingsReauthSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        workforce_identity_settings: typing.Optional[typing.Union["GoogleIapSettingsAccessSettingsWorkforceIdentitySettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allowed_domains_settings: allowed_domains_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#allowed_domains_settings GoogleIapSettings#allowed_domains_settings}
        :param cors_settings: cors_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#cors_settings GoogleIapSettings#cors_settings}
        :param gcip_settings: gcip_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#gcip_settings GoogleIapSettings#gcip_settings}
        :param identity_sources: Identity sources that IAP can use to authenticate the end user. Only one identity source can be configured. The possible values are: - 'WORKFORCE_IDENTITY_FEDERATION': Use external identities set up on Google Cloud Workforce Identity Federation. Possible values: ["WORKFORCE_IDENTITY_FEDERATION"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#identity_sources GoogleIapSettings#identity_sources}
        :param oauth_settings: oauth_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#oauth_settings GoogleIapSettings#oauth_settings}
        :param reauth_settings: reauth_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#reauth_settings GoogleIapSettings#reauth_settings}
        :param workforce_identity_settings: workforce_identity_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#workforce_identity_settings GoogleIapSettings#workforce_identity_settings}
        '''
        value = GoogleIapSettingsAccessSettings(
            allowed_domains_settings=allowed_domains_settings,
            cors_settings=cors_settings,
            gcip_settings=gcip_settings,
            identity_sources=identity_sources,
            oauth_settings=oauth_settings,
            reauth_settings=reauth_settings,
            workforce_identity_settings=workforce_identity_settings,
        )

        return typing.cast(None, jsii.invoke(self, "putAccessSettings", [value]))

    @jsii.member(jsii_name="putApplicationSettings")
    def put_application_settings(
        self,
        *,
        access_denied_page_settings: typing.Optional[typing.Union["GoogleIapSettingsApplicationSettingsAccessDeniedPageSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        attribute_propagation_settings: typing.Optional[typing.Union["GoogleIapSettingsApplicationSettingsAttributePropagationSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        cookie_domain: typing.Optional[builtins.str] = None,
        csm_settings: typing.Optional[typing.Union["GoogleIapSettingsApplicationSettingsCsmSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param access_denied_page_settings: access_denied_page_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#access_denied_page_settings GoogleIapSettings#access_denied_page_settings}
        :param attribute_propagation_settings: attribute_propagation_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#attribute_propagation_settings GoogleIapSettings#attribute_propagation_settings}
        :param cookie_domain: The Domain value to set for cookies generated by IAP. This value is not validated by the API, but will be ignored at runtime if invalid. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#cookie_domain GoogleIapSettings#cookie_domain}
        :param csm_settings: csm_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#csm_settings GoogleIapSettings#csm_settings}
        '''
        value = GoogleIapSettingsApplicationSettings(
            access_denied_page_settings=access_denied_page_settings,
            attribute_propagation_settings=attribute_propagation_settings,
            cookie_domain=cookie_domain,
            csm_settings=csm_settings,
        )

        return typing.cast(None, jsii.invoke(self, "putApplicationSettings", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#create GoogleIapSettings#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#delete GoogleIapSettings#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#update GoogleIapSettings#update}.
        '''
        value = GoogleIapSettingsTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAccessSettings")
    def reset_access_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessSettings", []))

    @jsii.member(jsii_name="resetApplicationSettings")
    def reset_application_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApplicationSettings", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

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
    @jsii.member(jsii_name="accessSettings")
    def access_settings(self) -> "GoogleIapSettingsAccessSettingsOutputReference":
        return typing.cast("GoogleIapSettingsAccessSettingsOutputReference", jsii.get(self, "accessSettings"))

    @builtins.property
    @jsii.member(jsii_name="applicationSettings")
    def application_settings(
        self,
    ) -> "GoogleIapSettingsApplicationSettingsOutputReference":
        return typing.cast("GoogleIapSettingsApplicationSettingsOutputReference", jsii.get(self, "applicationSettings"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleIapSettingsTimeoutsOutputReference":
        return typing.cast("GoogleIapSettingsTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="accessSettingsInput")
    def access_settings_input(
        self,
    ) -> typing.Optional["GoogleIapSettingsAccessSettings"]:
        return typing.cast(typing.Optional["GoogleIapSettingsAccessSettings"], jsii.get(self, "accessSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="applicationSettingsInput")
    def application_settings_input(
        self,
    ) -> typing.Optional["GoogleIapSettingsApplicationSettings"]:
        return typing.cast(typing.Optional["GoogleIapSettingsApplicationSettings"], jsii.get(self, "applicationSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleIapSettingsTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleIapSettingsTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__564c8f90bebce661230826b155a336d7399c3021d863fc6e3a0711fc75e1258d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44203fb5618bf44ba326eebe5d529ac42a4122b8d98592659f3bbcfe259fbdd7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIapSettings.GoogleIapSettingsAccessSettings",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_domains_settings": "allowedDomainsSettings",
        "cors_settings": "corsSettings",
        "gcip_settings": "gcipSettings",
        "identity_sources": "identitySources",
        "oauth_settings": "oauthSettings",
        "reauth_settings": "reauthSettings",
        "workforce_identity_settings": "workforceIdentitySettings",
    },
)
class GoogleIapSettingsAccessSettings:
    def __init__(
        self,
        *,
        allowed_domains_settings: typing.Optional[typing.Union["GoogleIapSettingsAccessSettingsAllowedDomainsSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        cors_settings: typing.Optional[typing.Union["GoogleIapSettingsAccessSettingsCorsSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        gcip_settings: typing.Optional[typing.Union["GoogleIapSettingsAccessSettingsGcipSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        identity_sources: typing.Optional[typing.Sequence[builtins.str]] = None,
        oauth_settings: typing.Optional[typing.Union["GoogleIapSettingsAccessSettingsOauthSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        reauth_settings: typing.Optional[typing.Union["GoogleIapSettingsAccessSettingsReauthSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        workforce_identity_settings: typing.Optional[typing.Union["GoogleIapSettingsAccessSettingsWorkforceIdentitySettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allowed_domains_settings: allowed_domains_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#allowed_domains_settings GoogleIapSettings#allowed_domains_settings}
        :param cors_settings: cors_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#cors_settings GoogleIapSettings#cors_settings}
        :param gcip_settings: gcip_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#gcip_settings GoogleIapSettings#gcip_settings}
        :param identity_sources: Identity sources that IAP can use to authenticate the end user. Only one identity source can be configured. The possible values are: - 'WORKFORCE_IDENTITY_FEDERATION': Use external identities set up on Google Cloud Workforce Identity Federation. Possible values: ["WORKFORCE_IDENTITY_FEDERATION"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#identity_sources GoogleIapSettings#identity_sources}
        :param oauth_settings: oauth_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#oauth_settings GoogleIapSettings#oauth_settings}
        :param reauth_settings: reauth_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#reauth_settings GoogleIapSettings#reauth_settings}
        :param workforce_identity_settings: workforce_identity_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#workforce_identity_settings GoogleIapSettings#workforce_identity_settings}
        '''
        if isinstance(allowed_domains_settings, dict):
            allowed_domains_settings = GoogleIapSettingsAccessSettingsAllowedDomainsSettings(**allowed_domains_settings)
        if isinstance(cors_settings, dict):
            cors_settings = GoogleIapSettingsAccessSettingsCorsSettings(**cors_settings)
        if isinstance(gcip_settings, dict):
            gcip_settings = GoogleIapSettingsAccessSettingsGcipSettings(**gcip_settings)
        if isinstance(oauth_settings, dict):
            oauth_settings = GoogleIapSettingsAccessSettingsOauthSettings(**oauth_settings)
        if isinstance(reauth_settings, dict):
            reauth_settings = GoogleIapSettingsAccessSettingsReauthSettings(**reauth_settings)
        if isinstance(workforce_identity_settings, dict):
            workforce_identity_settings = GoogleIapSettingsAccessSettingsWorkforceIdentitySettings(**workforce_identity_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a670cca7c8926e502a0d2bef9fd4d39f11d0305687913d60d0cc838793f08d7)
            check_type(argname="argument allowed_domains_settings", value=allowed_domains_settings, expected_type=type_hints["allowed_domains_settings"])
            check_type(argname="argument cors_settings", value=cors_settings, expected_type=type_hints["cors_settings"])
            check_type(argname="argument gcip_settings", value=gcip_settings, expected_type=type_hints["gcip_settings"])
            check_type(argname="argument identity_sources", value=identity_sources, expected_type=type_hints["identity_sources"])
            check_type(argname="argument oauth_settings", value=oauth_settings, expected_type=type_hints["oauth_settings"])
            check_type(argname="argument reauth_settings", value=reauth_settings, expected_type=type_hints["reauth_settings"])
            check_type(argname="argument workforce_identity_settings", value=workforce_identity_settings, expected_type=type_hints["workforce_identity_settings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allowed_domains_settings is not None:
            self._values["allowed_domains_settings"] = allowed_domains_settings
        if cors_settings is not None:
            self._values["cors_settings"] = cors_settings
        if gcip_settings is not None:
            self._values["gcip_settings"] = gcip_settings
        if identity_sources is not None:
            self._values["identity_sources"] = identity_sources
        if oauth_settings is not None:
            self._values["oauth_settings"] = oauth_settings
        if reauth_settings is not None:
            self._values["reauth_settings"] = reauth_settings
        if workforce_identity_settings is not None:
            self._values["workforce_identity_settings"] = workforce_identity_settings

    @builtins.property
    def allowed_domains_settings(
        self,
    ) -> typing.Optional["GoogleIapSettingsAccessSettingsAllowedDomainsSettings"]:
        '''allowed_domains_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#allowed_domains_settings GoogleIapSettings#allowed_domains_settings}
        '''
        result = self._values.get("allowed_domains_settings")
        return typing.cast(typing.Optional["GoogleIapSettingsAccessSettingsAllowedDomainsSettings"], result)

    @builtins.property
    def cors_settings(
        self,
    ) -> typing.Optional["GoogleIapSettingsAccessSettingsCorsSettings"]:
        '''cors_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#cors_settings GoogleIapSettings#cors_settings}
        '''
        result = self._values.get("cors_settings")
        return typing.cast(typing.Optional["GoogleIapSettingsAccessSettingsCorsSettings"], result)

    @builtins.property
    def gcip_settings(
        self,
    ) -> typing.Optional["GoogleIapSettingsAccessSettingsGcipSettings"]:
        '''gcip_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#gcip_settings GoogleIapSettings#gcip_settings}
        '''
        result = self._values.get("gcip_settings")
        return typing.cast(typing.Optional["GoogleIapSettingsAccessSettingsGcipSettings"], result)

    @builtins.property
    def identity_sources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Identity sources that IAP can use to authenticate the end user.

        Only one identity source
        can be configured. The possible values are:

        - 'WORKFORCE_IDENTITY_FEDERATION': Use external identities set up on Google Cloud Workforce
          Identity Federation. Possible values: ["WORKFORCE_IDENTITY_FEDERATION"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#identity_sources GoogleIapSettings#identity_sources}
        '''
        result = self._values.get("identity_sources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def oauth_settings(
        self,
    ) -> typing.Optional["GoogleIapSettingsAccessSettingsOauthSettings"]:
        '''oauth_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#oauth_settings GoogleIapSettings#oauth_settings}
        '''
        result = self._values.get("oauth_settings")
        return typing.cast(typing.Optional["GoogleIapSettingsAccessSettingsOauthSettings"], result)

    @builtins.property
    def reauth_settings(
        self,
    ) -> typing.Optional["GoogleIapSettingsAccessSettingsReauthSettings"]:
        '''reauth_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#reauth_settings GoogleIapSettings#reauth_settings}
        '''
        result = self._values.get("reauth_settings")
        return typing.cast(typing.Optional["GoogleIapSettingsAccessSettingsReauthSettings"], result)

    @builtins.property
    def workforce_identity_settings(
        self,
    ) -> typing.Optional["GoogleIapSettingsAccessSettingsWorkforceIdentitySettings"]:
        '''workforce_identity_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#workforce_identity_settings GoogleIapSettings#workforce_identity_settings}
        '''
        result = self._values.get("workforce_identity_settings")
        return typing.cast(typing.Optional["GoogleIapSettingsAccessSettingsWorkforceIdentitySettings"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIapSettingsAccessSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIapSettings.GoogleIapSettingsAccessSettingsAllowedDomainsSettings",
    jsii_struct_bases=[],
    name_mapping={"domains": "domains", "enable": "enable"},
)
class GoogleIapSettingsAccessSettingsAllowedDomainsSettings:
    def __init__(
        self,
        *,
        domains: typing.Optional[typing.Sequence[builtins.str]] = None,
        enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param domains: List of trusted domains. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#domains GoogleIapSettings#domains}
        :param enable: Configuration for customers to opt in for the feature. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#enable GoogleIapSettings#enable}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7e7088ae7945aca88670d308ce6a309fe53c7864d1159b928d23838db24b8c1)
            check_type(argname="argument domains", value=domains, expected_type=type_hints["domains"])
            check_type(argname="argument enable", value=enable, expected_type=type_hints["enable"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if domains is not None:
            self._values["domains"] = domains
        if enable is not None:
            self._values["enable"] = enable

    @builtins.property
    def domains(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of trusted domains.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#domains GoogleIapSettings#domains}
        '''
        result = self._values.get("domains")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def enable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Configuration for customers to opt in for the feature.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#enable GoogleIapSettings#enable}
        '''
        result = self._values.get("enable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIapSettingsAccessSettingsAllowedDomainsSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIapSettingsAccessSettingsAllowedDomainsSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIapSettings.GoogleIapSettingsAccessSettingsAllowedDomainsSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e513b92489c9cdcee230194230efedf641c4a87ae1d10b2ff165e34e4cb2b92)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDomains")
    def reset_domains(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDomains", []))

    @jsii.member(jsii_name="resetEnable")
    def reset_enable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnable", []))

    @builtins.property
    @jsii.member(jsii_name="domainsInput")
    def domains_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "domainsInput"))

    @builtins.property
    @jsii.member(jsii_name="enableInput")
    def enable_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableInput"))

    @builtins.property
    @jsii.member(jsii_name="domains")
    def domains(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "domains"))

    @domains.setter
    def domains(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7f5e19ab7acc537083492fd4754218986f344e7b41150093c7c2c3827823afc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domains", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enable")
    def enable(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enable"))

    @enable.setter
    def enable(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28c134c0d1fb8e35d05613a32f2735dee4353950fe92d5794c2b70f807e465c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIapSettingsAccessSettingsAllowedDomainsSettings]:
        return typing.cast(typing.Optional[GoogleIapSettingsAccessSettingsAllowedDomainsSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIapSettingsAccessSettingsAllowedDomainsSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00078765414d3ceba0a77372ee74e08c7b245d53e5a0299a6903bbd46e809360)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIapSettings.GoogleIapSettingsAccessSettingsCorsSettings",
    jsii_struct_bases=[],
    name_mapping={"allow_http_options": "allowHttpOptions"},
)
class GoogleIapSettingsAccessSettingsCorsSettings:
    def __init__(
        self,
        *,
        allow_http_options: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param allow_http_options: Configuration to allow HTTP OPTIONS calls to skip authorization. If undefined, IAP will not apply any special logic to OPTIONS requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#allow_http_options GoogleIapSettings#allow_http_options}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2d295485ff0968cfb3d40d22373aff7f1e81574192f578a4a9855385876fce8)
            check_type(argname="argument allow_http_options", value=allow_http_options, expected_type=type_hints["allow_http_options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allow_http_options is not None:
            self._values["allow_http_options"] = allow_http_options

    @builtins.property
    def allow_http_options(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Configuration to allow HTTP OPTIONS calls to skip authorization.

        If undefined, IAP will not apply any special logic to OPTIONS requests.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#allow_http_options GoogleIapSettings#allow_http_options}
        '''
        result = self._values.get("allow_http_options")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIapSettingsAccessSettingsCorsSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIapSettingsAccessSettingsCorsSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIapSettings.GoogleIapSettingsAccessSettingsCorsSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__302491b625d0d1b7128dfb8a1350bef58b89b67f6f9291a8db2c91a233ed2ccc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAllowHttpOptions")
    def reset_allow_http_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowHttpOptions", []))

    @builtins.property
    @jsii.member(jsii_name="allowHttpOptionsInput")
    def allow_http_options_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowHttpOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowHttpOptions")
    def allow_http_options(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowHttpOptions"))

    @allow_http_options.setter
    def allow_http_options(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a278b1b39fa8655185aadf33eea6147ac28fa99c746e0ad6abe020fc853ee3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowHttpOptions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIapSettingsAccessSettingsCorsSettings]:
        return typing.cast(typing.Optional[GoogleIapSettingsAccessSettingsCorsSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIapSettingsAccessSettingsCorsSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33094455e0d724a16002d834343b22c729d6fa30dfebc515738f9d4e47911060)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIapSettings.GoogleIapSettingsAccessSettingsGcipSettings",
    jsii_struct_bases=[],
    name_mapping={"login_page_uri": "loginPageUri", "tenant_ids": "tenantIds"},
)
class GoogleIapSettingsAccessSettingsGcipSettings:
    def __init__(
        self,
        *,
        login_page_uri: typing.Optional[builtins.str] = None,
        tenant_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param login_page_uri: Login page URI associated with the GCIP tenants. Typically, all resources within the same project share the same login page, though it could be overridden at the sub resource level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#login_page_uri GoogleIapSettings#login_page_uri}
        :param tenant_ids: GCIP tenant ids that are linked to the IAP resource. tenantIds could be a string beginning with a number character to indicate authenticating with GCIP tenant flow, or in the format of _ to indicate authenticating with GCIP agent flow. If agent flow is used, tenantIds should only contain one single element, while for tenant flow, tenantIds can contain multiple elements. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#tenant_ids GoogleIapSettings#tenant_ids}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03a85d1ecd8521fe5cd5bb2d81d209972a7102729d54409992ee69ca244b9e89)
            check_type(argname="argument login_page_uri", value=login_page_uri, expected_type=type_hints["login_page_uri"])
            check_type(argname="argument tenant_ids", value=tenant_ids, expected_type=type_hints["tenant_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if login_page_uri is not None:
            self._values["login_page_uri"] = login_page_uri
        if tenant_ids is not None:
            self._values["tenant_ids"] = tenant_ids

    @builtins.property
    def login_page_uri(self) -> typing.Optional[builtins.str]:
        '''Login page URI associated with the GCIP tenants.

        Typically, all resources within
        the same project share the same login page, though it could be overridden at the
        sub resource level.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#login_page_uri GoogleIapSettings#login_page_uri}
        '''
        result = self._values.get("login_page_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tenant_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''GCIP tenant ids that are linked to the IAP resource.

        tenantIds could be a string
        beginning with a number character to indicate authenticating with GCIP tenant flow,
        or in the format of _ to indicate authenticating with GCIP agent flow. If agent flow
        is used, tenantIds should only contain one single element, while for tenant flow,
        tenantIds can contain multiple elements.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#tenant_ids GoogleIapSettings#tenant_ids}
        '''
        result = self._values.get("tenant_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIapSettingsAccessSettingsGcipSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIapSettingsAccessSettingsGcipSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIapSettings.GoogleIapSettingsAccessSettingsGcipSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b1583f183225e0254fbfb22bab74ca91a7819b7fcc87919de275b50c70c9244)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetLoginPageUri")
    def reset_login_page_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoginPageUri", []))

    @jsii.member(jsii_name="resetTenantIds")
    def reset_tenant_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTenantIds", []))

    @builtins.property
    @jsii.member(jsii_name="loginPageUriInput")
    def login_page_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "loginPageUriInput"))

    @builtins.property
    @jsii.member(jsii_name="tenantIdsInput")
    def tenant_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tenantIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="loginPageUri")
    def login_page_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loginPageUri"))

    @login_page_uri.setter
    def login_page_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1795e1edae4e55857c8614a28c53c331c533c7fcb3299d0a9c68ba44950178c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loginPageUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tenantIds")
    def tenant_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tenantIds"))

    @tenant_ids.setter
    def tenant_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2487e40264b6e7b59301b8f480278fe2538f712554aa008c1efca5ff79a51c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tenantIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIapSettingsAccessSettingsGcipSettings]:
        return typing.cast(typing.Optional[GoogleIapSettingsAccessSettingsGcipSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIapSettingsAccessSettingsGcipSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1874dd4ccbcbe4fc12ce95d15dfe2cb21ae1b0a2b3d9eaca65e088b30786ce39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIapSettings.GoogleIapSettingsAccessSettingsOauthSettings",
    jsii_struct_bases=[],
    name_mapping={
        "login_hint": "loginHint",
        "programmatic_clients": "programmaticClients",
    },
)
class GoogleIapSettingsAccessSettingsOauthSettings:
    def __init__(
        self,
        *,
        login_hint: typing.Optional[builtins.str] = None,
        programmatic_clients: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param login_hint: Domain hint to send as hd=? parameter in OAuth request flow. Enables redirect to primary IDP by skipping Google's login screen. (https://developers.google.com/identity/protocols/OpenIDConnect#hd-param) Note: IAP does not verify that the id token's hd claim matches this value since access behavior is managed by IAM policies. - loginHint setting is not a replacement for access control. Always enforce an appropriate access policy if you want to restrict access to users outside your domain. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#login_hint GoogleIapSettings#login_hint}
        :param programmatic_clients: List of client ids allowed to use IAP programmatically. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#programmatic_clients GoogleIapSettings#programmatic_clients}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfe5f8423bc24863e77534deb9366029d8ee9169f4b7484120553710ae49ecde)
            check_type(argname="argument login_hint", value=login_hint, expected_type=type_hints["login_hint"])
            check_type(argname="argument programmatic_clients", value=programmatic_clients, expected_type=type_hints["programmatic_clients"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if login_hint is not None:
            self._values["login_hint"] = login_hint
        if programmatic_clients is not None:
            self._values["programmatic_clients"] = programmatic_clients

    @builtins.property
    def login_hint(self) -> typing.Optional[builtins.str]:
        '''Domain hint to send as hd=?

        parameter in OAuth request flow.
        Enables redirect to primary IDP by skipping Google's login screen.
        (https://developers.google.com/identity/protocols/OpenIDConnect#hd-param)
        Note: IAP does not verify that the id token's hd claim matches this value
        since access behavior is managed by IAM policies.

        - loginHint setting is not a replacement for access control. Always enforce an appropriate access policy if you want to restrict access to users outside your domain.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#login_hint GoogleIapSettings#login_hint}
        '''
        result = self._values.get("login_hint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def programmatic_clients(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of client ids allowed to use IAP programmatically.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#programmatic_clients GoogleIapSettings#programmatic_clients}
        '''
        result = self._values.get("programmatic_clients")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIapSettingsAccessSettingsOauthSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIapSettingsAccessSettingsOauthSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIapSettings.GoogleIapSettingsAccessSettingsOauthSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f7b24ddd7011a28366f060e7e1aea36fb53b8e27f6845c0d67f642b1ed031e0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetLoginHint")
    def reset_login_hint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoginHint", []))

    @jsii.member(jsii_name="resetProgrammaticClients")
    def reset_programmatic_clients(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProgrammaticClients", []))

    @builtins.property
    @jsii.member(jsii_name="loginHintInput")
    def login_hint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "loginHintInput"))

    @builtins.property
    @jsii.member(jsii_name="programmaticClientsInput")
    def programmatic_clients_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "programmaticClientsInput"))

    @builtins.property
    @jsii.member(jsii_name="loginHint")
    def login_hint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loginHint"))

    @login_hint.setter
    def login_hint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56424c00fcd8434a1c55ee75b519f32ae6c006d3fc1eb03c23c427c177c9717f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loginHint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="programmaticClients")
    def programmatic_clients(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "programmaticClients"))

    @programmatic_clients.setter
    def programmatic_clients(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b95b0e8ab9b934d436b3e0d93b1f840bc0c17b0466944bfb0d64fa03a84d45a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "programmaticClients", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIapSettingsAccessSettingsOauthSettings]:
        return typing.cast(typing.Optional[GoogleIapSettingsAccessSettingsOauthSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIapSettingsAccessSettingsOauthSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e6e8a1744d7b254b694a0cd9b5d7002e2b500c239a79e74840bb30ae2f5fdb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleIapSettingsAccessSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIapSettings.GoogleIapSettingsAccessSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d84f5288c2c0c496537d85d69a31a16419c5a40deb19f7c44cf03624a05a916)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAllowedDomainsSettings")
    def put_allowed_domains_settings(
        self,
        *,
        domains: typing.Optional[typing.Sequence[builtins.str]] = None,
        enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param domains: List of trusted domains. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#domains GoogleIapSettings#domains}
        :param enable: Configuration for customers to opt in for the feature. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#enable GoogleIapSettings#enable}
        '''
        value = GoogleIapSettingsAccessSettingsAllowedDomainsSettings(
            domains=domains, enable=enable
        )

        return typing.cast(None, jsii.invoke(self, "putAllowedDomainsSettings", [value]))

    @jsii.member(jsii_name="putCorsSettings")
    def put_cors_settings(
        self,
        *,
        allow_http_options: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param allow_http_options: Configuration to allow HTTP OPTIONS calls to skip authorization. If undefined, IAP will not apply any special logic to OPTIONS requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#allow_http_options GoogleIapSettings#allow_http_options}
        '''
        value = GoogleIapSettingsAccessSettingsCorsSettings(
            allow_http_options=allow_http_options
        )

        return typing.cast(None, jsii.invoke(self, "putCorsSettings", [value]))

    @jsii.member(jsii_name="putGcipSettings")
    def put_gcip_settings(
        self,
        *,
        login_page_uri: typing.Optional[builtins.str] = None,
        tenant_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param login_page_uri: Login page URI associated with the GCIP tenants. Typically, all resources within the same project share the same login page, though it could be overridden at the sub resource level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#login_page_uri GoogleIapSettings#login_page_uri}
        :param tenant_ids: GCIP tenant ids that are linked to the IAP resource. tenantIds could be a string beginning with a number character to indicate authenticating with GCIP tenant flow, or in the format of _ to indicate authenticating with GCIP agent flow. If agent flow is used, tenantIds should only contain one single element, while for tenant flow, tenantIds can contain multiple elements. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#tenant_ids GoogleIapSettings#tenant_ids}
        '''
        value = GoogleIapSettingsAccessSettingsGcipSettings(
            login_page_uri=login_page_uri, tenant_ids=tenant_ids
        )

        return typing.cast(None, jsii.invoke(self, "putGcipSettings", [value]))

    @jsii.member(jsii_name="putOauthSettings")
    def put_oauth_settings(
        self,
        *,
        login_hint: typing.Optional[builtins.str] = None,
        programmatic_clients: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param login_hint: Domain hint to send as hd=? parameter in OAuth request flow. Enables redirect to primary IDP by skipping Google's login screen. (https://developers.google.com/identity/protocols/OpenIDConnect#hd-param) Note: IAP does not verify that the id token's hd claim matches this value since access behavior is managed by IAM policies. - loginHint setting is not a replacement for access control. Always enforce an appropriate access policy if you want to restrict access to users outside your domain. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#login_hint GoogleIapSettings#login_hint}
        :param programmatic_clients: List of client ids allowed to use IAP programmatically. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#programmatic_clients GoogleIapSettings#programmatic_clients}
        '''
        value = GoogleIapSettingsAccessSettingsOauthSettings(
            login_hint=login_hint, programmatic_clients=programmatic_clients
        )

        return typing.cast(None, jsii.invoke(self, "putOauthSettings", [value]))

    @jsii.member(jsii_name="putReauthSettings")
    def put_reauth_settings(
        self,
        *,
        max_age: builtins.str,
        method: builtins.str,
        policy_type: builtins.str,
    ) -> None:
        '''
        :param max_age: Reauth session lifetime, how long before a user has to reauthenticate again. A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#max_age GoogleIapSettings#max_age}
        :param method: Reauth method requested. The possible values are:. - 'LOGIN': Prompts the user to log in again. - 'SECURE_KEY': User must use their secure key 2nd factor device. - 'ENROLLED_SECOND_FACTORS': User can use any enabled 2nd factor. Possible values: ["LOGIN", "SECURE_KEY", "ENROLLED_SECOND_FACTORS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#method GoogleIapSettings#method}
        :param policy_type: How IAP determines the effective policy in cases of hierarchical policies. Policies are merged from higher in the hierarchy to lower in the hierarchy. The possible values are: - 'MINIMUM': This policy acts as a minimum to other policies, lower in the hierarchy. Effective policy may only be the same or stricter. - 'DEFAULT': This policy acts as a default if no other reauth policy is set. Possible values: ["MINIMUM", "DEFAULT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#policy_type GoogleIapSettings#policy_type}
        '''
        value = GoogleIapSettingsAccessSettingsReauthSettings(
            max_age=max_age, method=method, policy_type=policy_type
        )

        return typing.cast(None, jsii.invoke(self, "putReauthSettings", [value]))

    @jsii.member(jsii_name="putWorkforceIdentitySettings")
    def put_workforce_identity_settings(
        self,
        *,
        oauth2: typing.Optional[typing.Union["GoogleIapSettingsAccessSettingsWorkforceIdentitySettingsOauth2", typing.Dict[builtins.str, typing.Any]]] = None,
        workforce_pools: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param oauth2: oauth2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#oauth2 GoogleIapSettings#oauth2}
        :param workforce_pools: The workforce pool resources. Only one workforce pool is accepted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#workforce_pools GoogleIapSettings#workforce_pools}
        '''
        value = GoogleIapSettingsAccessSettingsWorkforceIdentitySettings(
            oauth2=oauth2, workforce_pools=workforce_pools
        )

        return typing.cast(None, jsii.invoke(self, "putWorkforceIdentitySettings", [value]))

    @jsii.member(jsii_name="resetAllowedDomainsSettings")
    def reset_allowed_domains_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedDomainsSettings", []))

    @jsii.member(jsii_name="resetCorsSettings")
    def reset_cors_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCorsSettings", []))

    @jsii.member(jsii_name="resetGcipSettings")
    def reset_gcip_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGcipSettings", []))

    @jsii.member(jsii_name="resetIdentitySources")
    def reset_identity_sources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentitySources", []))

    @jsii.member(jsii_name="resetOauthSettings")
    def reset_oauth_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauthSettings", []))

    @jsii.member(jsii_name="resetReauthSettings")
    def reset_reauth_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReauthSettings", []))

    @jsii.member(jsii_name="resetWorkforceIdentitySettings")
    def reset_workforce_identity_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkforceIdentitySettings", []))

    @builtins.property
    @jsii.member(jsii_name="allowedDomainsSettings")
    def allowed_domains_settings(
        self,
    ) -> GoogleIapSettingsAccessSettingsAllowedDomainsSettingsOutputReference:
        return typing.cast(GoogleIapSettingsAccessSettingsAllowedDomainsSettingsOutputReference, jsii.get(self, "allowedDomainsSettings"))

    @builtins.property
    @jsii.member(jsii_name="corsSettings")
    def cors_settings(
        self,
    ) -> GoogleIapSettingsAccessSettingsCorsSettingsOutputReference:
        return typing.cast(GoogleIapSettingsAccessSettingsCorsSettingsOutputReference, jsii.get(self, "corsSettings"))

    @builtins.property
    @jsii.member(jsii_name="gcipSettings")
    def gcip_settings(
        self,
    ) -> GoogleIapSettingsAccessSettingsGcipSettingsOutputReference:
        return typing.cast(GoogleIapSettingsAccessSettingsGcipSettingsOutputReference, jsii.get(self, "gcipSettings"))

    @builtins.property
    @jsii.member(jsii_name="oauthSettings")
    def oauth_settings(
        self,
    ) -> GoogleIapSettingsAccessSettingsOauthSettingsOutputReference:
        return typing.cast(GoogleIapSettingsAccessSettingsOauthSettingsOutputReference, jsii.get(self, "oauthSettings"))

    @builtins.property
    @jsii.member(jsii_name="reauthSettings")
    def reauth_settings(
        self,
    ) -> "GoogleIapSettingsAccessSettingsReauthSettingsOutputReference":
        return typing.cast("GoogleIapSettingsAccessSettingsReauthSettingsOutputReference", jsii.get(self, "reauthSettings"))

    @builtins.property
    @jsii.member(jsii_name="workforceIdentitySettings")
    def workforce_identity_settings(
        self,
    ) -> "GoogleIapSettingsAccessSettingsWorkforceIdentitySettingsOutputReference":
        return typing.cast("GoogleIapSettingsAccessSettingsWorkforceIdentitySettingsOutputReference", jsii.get(self, "workforceIdentitySettings"))

    @builtins.property
    @jsii.member(jsii_name="allowedDomainsSettingsInput")
    def allowed_domains_settings_input(
        self,
    ) -> typing.Optional[GoogleIapSettingsAccessSettingsAllowedDomainsSettings]:
        return typing.cast(typing.Optional[GoogleIapSettingsAccessSettingsAllowedDomainsSettings], jsii.get(self, "allowedDomainsSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="corsSettingsInput")
    def cors_settings_input(
        self,
    ) -> typing.Optional[GoogleIapSettingsAccessSettingsCorsSettings]:
        return typing.cast(typing.Optional[GoogleIapSettingsAccessSettingsCorsSettings], jsii.get(self, "corsSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="gcipSettingsInput")
    def gcip_settings_input(
        self,
    ) -> typing.Optional[GoogleIapSettingsAccessSettingsGcipSettings]:
        return typing.cast(typing.Optional[GoogleIapSettingsAccessSettingsGcipSettings], jsii.get(self, "gcipSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="identitySourcesInput")
    def identity_sources_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "identitySourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="oauthSettingsInput")
    def oauth_settings_input(
        self,
    ) -> typing.Optional[GoogleIapSettingsAccessSettingsOauthSettings]:
        return typing.cast(typing.Optional[GoogleIapSettingsAccessSettingsOauthSettings], jsii.get(self, "oauthSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="reauthSettingsInput")
    def reauth_settings_input(
        self,
    ) -> typing.Optional["GoogleIapSettingsAccessSettingsReauthSettings"]:
        return typing.cast(typing.Optional["GoogleIapSettingsAccessSettingsReauthSettings"], jsii.get(self, "reauthSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="workforceIdentitySettingsInput")
    def workforce_identity_settings_input(
        self,
    ) -> typing.Optional["GoogleIapSettingsAccessSettingsWorkforceIdentitySettings"]:
        return typing.cast(typing.Optional["GoogleIapSettingsAccessSettingsWorkforceIdentitySettings"], jsii.get(self, "workforceIdentitySettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="identitySources")
    def identity_sources(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "identitySources"))

    @identity_sources.setter
    def identity_sources(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf7322491f135524d9b1c4ffb0567753b434badb9edd8c37e5cc8ebf8973a2c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identitySources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleIapSettingsAccessSettings]:
        return typing.cast(typing.Optional[GoogleIapSettingsAccessSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIapSettingsAccessSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b156cf3380bfb061573282fe3b5d6574ff0fc31b85c5a636ca981ed8380a1a25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIapSettings.GoogleIapSettingsAccessSettingsReauthSettings",
    jsii_struct_bases=[],
    name_mapping={
        "max_age": "maxAge",
        "method": "method",
        "policy_type": "policyType",
    },
)
class GoogleIapSettingsAccessSettingsReauthSettings:
    def __init__(
        self,
        *,
        max_age: builtins.str,
        method: builtins.str,
        policy_type: builtins.str,
    ) -> None:
        '''
        :param max_age: Reauth session lifetime, how long before a user has to reauthenticate again. A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#max_age GoogleIapSettings#max_age}
        :param method: Reauth method requested. The possible values are:. - 'LOGIN': Prompts the user to log in again. - 'SECURE_KEY': User must use their secure key 2nd factor device. - 'ENROLLED_SECOND_FACTORS': User can use any enabled 2nd factor. Possible values: ["LOGIN", "SECURE_KEY", "ENROLLED_SECOND_FACTORS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#method GoogleIapSettings#method}
        :param policy_type: How IAP determines the effective policy in cases of hierarchical policies. Policies are merged from higher in the hierarchy to lower in the hierarchy. The possible values are: - 'MINIMUM': This policy acts as a minimum to other policies, lower in the hierarchy. Effective policy may only be the same or stricter. - 'DEFAULT': This policy acts as a default if no other reauth policy is set. Possible values: ["MINIMUM", "DEFAULT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#policy_type GoogleIapSettings#policy_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5de0d32ab62a3da5b4a23faba5d0ce483ec43b53864835c31ed557a6be9f167)
            check_type(argname="argument max_age", value=max_age, expected_type=type_hints["max_age"])
            check_type(argname="argument method", value=method, expected_type=type_hints["method"])
            check_type(argname="argument policy_type", value=policy_type, expected_type=type_hints["policy_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "max_age": max_age,
            "method": method,
            "policy_type": policy_type,
        }

    @builtins.property
    def max_age(self) -> builtins.str:
        '''Reauth session lifetime, how long before a user has to reauthenticate again.

        A duration in seconds with up to nine fractional digits, ending with 's'.
        Example: "3.5s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#max_age GoogleIapSettings#max_age}
        '''
        result = self._values.get("max_age")
        assert result is not None, "Required property 'max_age' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def method(self) -> builtins.str:
        '''Reauth method requested. The possible values are:.

        - 'LOGIN': Prompts the user to log in again.
        - 'SECURE_KEY': User must use their secure key 2nd factor device.
        - 'ENROLLED_SECOND_FACTORS': User can use any enabled 2nd factor. Possible values: ["LOGIN", "SECURE_KEY", "ENROLLED_SECOND_FACTORS"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#method GoogleIapSettings#method}
        '''
        result = self._values.get("method")
        assert result is not None, "Required property 'method' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def policy_type(self) -> builtins.str:
        '''How IAP determines the effective policy in cases of hierarchical policies.

        Policies are merged from higher in the hierarchy to lower in the hierarchy.
        The possible values are:

        - 'MINIMUM': This policy acts as a minimum to other policies, lower in the hierarchy.
          Effective policy may only be the same or stricter.
        - 'DEFAULT': This policy acts as a default if no other reauth policy is set. Possible values: ["MINIMUM", "DEFAULT"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#policy_type GoogleIapSettings#policy_type}
        '''
        result = self._values.get("policy_type")
        assert result is not None, "Required property 'policy_type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIapSettingsAccessSettingsReauthSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIapSettingsAccessSettingsReauthSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIapSettings.GoogleIapSettingsAccessSettingsReauthSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__196e12aecab60ff8e4bf69322547daa39b157c3d563d398d85adef7593a0eda0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="maxAgeInput")
    def max_age_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maxAgeInput"))

    @builtins.property
    @jsii.member(jsii_name="methodInput")
    def method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "methodInput"))

    @builtins.property
    @jsii.member(jsii_name="policyTypeInput")
    def policy_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="maxAge")
    def max_age(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxAge"))

    @max_age.setter
    def max_age(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb9a2d16d87aca898db3571a27e72be5ca07cae43cd6c1a02d26812a1d4892f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxAge", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="method")
    def method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "method"))

    @method.setter
    def method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b08c78a345102909e3293fb7b52593a62ef8d9ff69541e3862dd694f20e9245d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "method", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="policyType")
    def policy_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyType"))

    @policy_type.setter
    def policy_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b820709825280ad032b00b905ff1fd05fda70c188fd2a8435402917bb6faf39c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIapSettingsAccessSettingsReauthSettings]:
        return typing.cast(typing.Optional[GoogleIapSettingsAccessSettingsReauthSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIapSettingsAccessSettingsReauthSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6af4fb26b228b49a3bf7d2138d2c6a4532a8980d88fcfa7192285ec913bbec8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIapSettings.GoogleIapSettingsAccessSettingsWorkforceIdentitySettings",
    jsii_struct_bases=[],
    name_mapping={"oauth2": "oauth2", "workforce_pools": "workforcePools"},
)
class GoogleIapSettingsAccessSettingsWorkforceIdentitySettings:
    def __init__(
        self,
        *,
        oauth2: typing.Optional[typing.Union["GoogleIapSettingsAccessSettingsWorkforceIdentitySettingsOauth2", typing.Dict[builtins.str, typing.Any]]] = None,
        workforce_pools: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param oauth2: oauth2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#oauth2 GoogleIapSettings#oauth2}
        :param workforce_pools: The workforce pool resources. Only one workforce pool is accepted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#workforce_pools GoogleIapSettings#workforce_pools}
        '''
        if isinstance(oauth2, dict):
            oauth2 = GoogleIapSettingsAccessSettingsWorkforceIdentitySettingsOauth2(**oauth2)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__841840908b6b84e10074b5fade5bf549c5652c2b1cb7cf926cab103c3b9d21e9)
            check_type(argname="argument oauth2", value=oauth2, expected_type=type_hints["oauth2"])
            check_type(argname="argument workforce_pools", value=workforce_pools, expected_type=type_hints["workforce_pools"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if oauth2 is not None:
            self._values["oauth2"] = oauth2
        if workforce_pools is not None:
            self._values["workforce_pools"] = workforce_pools

    @builtins.property
    def oauth2(
        self,
    ) -> typing.Optional["GoogleIapSettingsAccessSettingsWorkforceIdentitySettingsOauth2"]:
        '''oauth2 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#oauth2 GoogleIapSettings#oauth2}
        '''
        result = self._values.get("oauth2")
        return typing.cast(typing.Optional["GoogleIapSettingsAccessSettingsWorkforceIdentitySettingsOauth2"], result)

    @builtins.property
    def workforce_pools(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The workforce pool resources. Only one workforce pool is accepted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#workforce_pools GoogleIapSettings#workforce_pools}
        '''
        result = self._values.get("workforce_pools")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIapSettingsAccessSettingsWorkforceIdentitySettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIapSettings.GoogleIapSettingsAccessSettingsWorkforceIdentitySettingsOauth2",
    jsii_struct_bases=[],
    name_mapping={"client_id": "clientId", "client_secret": "clientSecret"},
)
class GoogleIapSettingsAccessSettingsWorkforceIdentitySettingsOauth2:
    def __init__(
        self,
        *,
        client_id: typing.Optional[builtins.str] = None,
        client_secret: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param client_id: The OAuth 2.0 client ID registered in the workforce identity federation OAuth 2.0 Server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#client_id GoogleIapSettings#client_id}
        :param client_secret: Input only. The OAuth 2.0 client secret created while registering the client ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#client_secret GoogleIapSettings#client_secret}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__081141a58518a4f67ef890f94e57453050c91c0fbb9b87fe20f54762e51401ba)
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if client_id is not None:
            self._values["client_id"] = client_id
        if client_secret is not None:
            self._values["client_secret"] = client_secret

    @builtins.property
    def client_id(self) -> typing.Optional[builtins.str]:
        '''The OAuth 2.0 client ID registered in the workforce identity federation OAuth 2.0 Server.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#client_id GoogleIapSettings#client_id}
        '''
        result = self._values.get("client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_secret(self) -> typing.Optional[builtins.str]:
        '''Input only. The OAuth 2.0 client secret created while registering the client ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#client_secret GoogleIapSettings#client_secret}
        '''
        result = self._values.get("client_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIapSettingsAccessSettingsWorkforceIdentitySettingsOauth2(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIapSettingsAccessSettingsWorkforceIdentitySettingsOauth2OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIapSettings.GoogleIapSettingsAccessSettingsWorkforceIdentitySettingsOauth2OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a8e82ae46dba2a8218c37280126ef81c9a5beda192c075151af6bdcd67bdfca6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetClientId")
    def reset_client_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientId", []))

    @jsii.member(jsii_name="resetClientSecret")
    def reset_client_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientSecret", []))

    @builtins.property
    @jsii.member(jsii_name="clientSecretSha256")
    def client_secret_sha256(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecretSha256"))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretInput")
    def client_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31818a528591d803b7ab720ca13d268db9c1795b1a8c2f4cd3345a42e6052379)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecret"))

    @client_secret.setter
    def client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9817cae648aa420ca24cc2a32ec558e3d79ece7f342af499e834bdf4faaae97f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIapSettingsAccessSettingsWorkforceIdentitySettingsOauth2]:
        return typing.cast(typing.Optional[GoogleIapSettingsAccessSettingsWorkforceIdentitySettingsOauth2], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIapSettingsAccessSettingsWorkforceIdentitySettingsOauth2],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__269a4fd08db90ddd85ee1214a8c0bd091c998add1a016df478d24c7dff1f4bcb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleIapSettingsAccessSettingsWorkforceIdentitySettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIapSettings.GoogleIapSettingsAccessSettingsWorkforceIdentitySettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__641efa2eb5ed848bde98b1a1bc40e8058282d8548143652847d66e2b44278b7e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOauth2")
    def put_oauth2(
        self,
        *,
        client_id: typing.Optional[builtins.str] = None,
        client_secret: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param client_id: The OAuth 2.0 client ID registered in the workforce identity federation OAuth 2.0 Server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#client_id GoogleIapSettings#client_id}
        :param client_secret: Input only. The OAuth 2.0 client secret created while registering the client ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#client_secret GoogleIapSettings#client_secret}
        '''
        value = GoogleIapSettingsAccessSettingsWorkforceIdentitySettingsOauth2(
            client_id=client_id, client_secret=client_secret
        )

        return typing.cast(None, jsii.invoke(self, "putOauth2", [value]))

    @jsii.member(jsii_name="resetOauth2")
    def reset_oauth2(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauth2", []))

    @jsii.member(jsii_name="resetWorkforcePools")
    def reset_workforce_pools(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkforcePools", []))

    @builtins.property
    @jsii.member(jsii_name="oauth2")
    def oauth2(
        self,
    ) -> GoogleIapSettingsAccessSettingsWorkforceIdentitySettingsOauth2OutputReference:
        return typing.cast(GoogleIapSettingsAccessSettingsWorkforceIdentitySettingsOauth2OutputReference, jsii.get(self, "oauth2"))

    @builtins.property
    @jsii.member(jsii_name="oauth2Input")
    def oauth2_input(
        self,
    ) -> typing.Optional[GoogleIapSettingsAccessSettingsWorkforceIdentitySettingsOauth2]:
        return typing.cast(typing.Optional[GoogleIapSettingsAccessSettingsWorkforceIdentitySettingsOauth2], jsii.get(self, "oauth2Input"))

    @builtins.property
    @jsii.member(jsii_name="workforcePoolsInput")
    def workforce_pools_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "workforcePoolsInput"))

    @builtins.property
    @jsii.member(jsii_name="workforcePools")
    def workforce_pools(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "workforcePools"))

    @workforce_pools.setter
    def workforce_pools(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c7a4c3f103daeb36138a5fb1bded67495dd4e58229f625bc63cd42cd9fa666a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workforcePools", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIapSettingsAccessSettingsWorkforceIdentitySettings]:
        return typing.cast(typing.Optional[GoogleIapSettingsAccessSettingsWorkforceIdentitySettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIapSettingsAccessSettingsWorkforceIdentitySettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17b6d7412cfe55f2ca546b5e4ba67758fee17f46668f68270f4005b357a75488)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIapSettings.GoogleIapSettingsApplicationSettings",
    jsii_struct_bases=[],
    name_mapping={
        "access_denied_page_settings": "accessDeniedPageSettings",
        "attribute_propagation_settings": "attributePropagationSettings",
        "cookie_domain": "cookieDomain",
        "csm_settings": "csmSettings",
    },
)
class GoogleIapSettingsApplicationSettings:
    def __init__(
        self,
        *,
        access_denied_page_settings: typing.Optional[typing.Union["GoogleIapSettingsApplicationSettingsAccessDeniedPageSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        attribute_propagation_settings: typing.Optional[typing.Union["GoogleIapSettingsApplicationSettingsAttributePropagationSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        cookie_domain: typing.Optional[builtins.str] = None,
        csm_settings: typing.Optional[typing.Union["GoogleIapSettingsApplicationSettingsCsmSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param access_denied_page_settings: access_denied_page_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#access_denied_page_settings GoogleIapSettings#access_denied_page_settings}
        :param attribute_propagation_settings: attribute_propagation_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#attribute_propagation_settings GoogleIapSettings#attribute_propagation_settings}
        :param cookie_domain: The Domain value to set for cookies generated by IAP. This value is not validated by the API, but will be ignored at runtime if invalid. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#cookie_domain GoogleIapSettings#cookie_domain}
        :param csm_settings: csm_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#csm_settings GoogleIapSettings#csm_settings}
        '''
        if isinstance(access_denied_page_settings, dict):
            access_denied_page_settings = GoogleIapSettingsApplicationSettingsAccessDeniedPageSettings(**access_denied_page_settings)
        if isinstance(attribute_propagation_settings, dict):
            attribute_propagation_settings = GoogleIapSettingsApplicationSettingsAttributePropagationSettings(**attribute_propagation_settings)
        if isinstance(csm_settings, dict):
            csm_settings = GoogleIapSettingsApplicationSettingsCsmSettings(**csm_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fbdbe140a7c0db5d42699cdf690481fed6523da1f5cfeb56c79694750b5ca90)
            check_type(argname="argument access_denied_page_settings", value=access_denied_page_settings, expected_type=type_hints["access_denied_page_settings"])
            check_type(argname="argument attribute_propagation_settings", value=attribute_propagation_settings, expected_type=type_hints["attribute_propagation_settings"])
            check_type(argname="argument cookie_domain", value=cookie_domain, expected_type=type_hints["cookie_domain"])
            check_type(argname="argument csm_settings", value=csm_settings, expected_type=type_hints["csm_settings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_denied_page_settings is not None:
            self._values["access_denied_page_settings"] = access_denied_page_settings
        if attribute_propagation_settings is not None:
            self._values["attribute_propagation_settings"] = attribute_propagation_settings
        if cookie_domain is not None:
            self._values["cookie_domain"] = cookie_domain
        if csm_settings is not None:
            self._values["csm_settings"] = csm_settings

    @builtins.property
    def access_denied_page_settings(
        self,
    ) -> typing.Optional["GoogleIapSettingsApplicationSettingsAccessDeniedPageSettings"]:
        '''access_denied_page_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#access_denied_page_settings GoogleIapSettings#access_denied_page_settings}
        '''
        result = self._values.get("access_denied_page_settings")
        return typing.cast(typing.Optional["GoogleIapSettingsApplicationSettingsAccessDeniedPageSettings"], result)

    @builtins.property
    def attribute_propagation_settings(
        self,
    ) -> typing.Optional["GoogleIapSettingsApplicationSettingsAttributePropagationSettings"]:
        '''attribute_propagation_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#attribute_propagation_settings GoogleIapSettings#attribute_propagation_settings}
        '''
        result = self._values.get("attribute_propagation_settings")
        return typing.cast(typing.Optional["GoogleIapSettingsApplicationSettingsAttributePropagationSettings"], result)

    @builtins.property
    def cookie_domain(self) -> typing.Optional[builtins.str]:
        '''The Domain value to set for cookies generated by IAP.

        This value is not validated by the API,
        but will be ignored at runtime if invalid.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#cookie_domain GoogleIapSettings#cookie_domain}
        '''
        result = self._values.get("cookie_domain")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def csm_settings(
        self,
    ) -> typing.Optional["GoogleIapSettingsApplicationSettingsCsmSettings"]:
        '''csm_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#csm_settings GoogleIapSettings#csm_settings}
        '''
        result = self._values.get("csm_settings")
        return typing.cast(typing.Optional["GoogleIapSettingsApplicationSettingsCsmSettings"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIapSettingsApplicationSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIapSettings.GoogleIapSettingsApplicationSettingsAccessDeniedPageSettings",
    jsii_struct_bases=[],
    name_mapping={
        "access_denied_page_uri": "accessDeniedPageUri",
        "generate_troubleshooting_uri": "generateTroubleshootingUri",
        "remediation_token_generation_enabled": "remediationTokenGenerationEnabled",
    },
)
class GoogleIapSettingsApplicationSettingsAccessDeniedPageSettings:
    def __init__(
        self,
        *,
        access_denied_page_uri: typing.Optional[builtins.str] = None,
        generate_troubleshooting_uri: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        remediation_token_generation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param access_denied_page_uri: The URI to be redirected to when access is denied. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#access_denied_page_uri GoogleIapSettings#access_denied_page_uri}
        :param generate_troubleshooting_uri: Whether to generate a troubleshooting URL on access denied events to this application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#generate_troubleshooting_uri GoogleIapSettings#generate_troubleshooting_uri}
        :param remediation_token_generation_enabled: Whether to generate remediation token on access denied events to this application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#remediation_token_generation_enabled GoogleIapSettings#remediation_token_generation_enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60f7348d751cc600d5e46a6a8067d5023cd54ea36b8412c5fe4e65cd7299759a)
            check_type(argname="argument access_denied_page_uri", value=access_denied_page_uri, expected_type=type_hints["access_denied_page_uri"])
            check_type(argname="argument generate_troubleshooting_uri", value=generate_troubleshooting_uri, expected_type=type_hints["generate_troubleshooting_uri"])
            check_type(argname="argument remediation_token_generation_enabled", value=remediation_token_generation_enabled, expected_type=type_hints["remediation_token_generation_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_denied_page_uri is not None:
            self._values["access_denied_page_uri"] = access_denied_page_uri
        if generate_troubleshooting_uri is not None:
            self._values["generate_troubleshooting_uri"] = generate_troubleshooting_uri
        if remediation_token_generation_enabled is not None:
            self._values["remediation_token_generation_enabled"] = remediation_token_generation_enabled

    @builtins.property
    def access_denied_page_uri(self) -> typing.Optional[builtins.str]:
        '''The URI to be redirected to when access is denied.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#access_denied_page_uri GoogleIapSettings#access_denied_page_uri}
        '''
        result = self._values.get("access_denied_page_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def generate_troubleshooting_uri(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to generate a troubleshooting URL on access denied events to this application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#generate_troubleshooting_uri GoogleIapSettings#generate_troubleshooting_uri}
        '''
        result = self._values.get("generate_troubleshooting_uri")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def remediation_token_generation_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to generate remediation token on access denied events to this application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#remediation_token_generation_enabled GoogleIapSettings#remediation_token_generation_enabled}
        '''
        result = self._values.get("remediation_token_generation_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIapSettingsApplicationSettingsAccessDeniedPageSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIapSettingsApplicationSettingsAccessDeniedPageSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIapSettings.GoogleIapSettingsApplicationSettingsAccessDeniedPageSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__01bf46b967859a43323b442e717f16d5f27be73a5bff7d0d6dfdbc238f019f93)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAccessDeniedPageUri")
    def reset_access_denied_page_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessDeniedPageUri", []))

    @jsii.member(jsii_name="resetGenerateTroubleshootingUri")
    def reset_generate_troubleshooting_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGenerateTroubleshootingUri", []))

    @jsii.member(jsii_name="resetRemediationTokenGenerationEnabled")
    def reset_remediation_token_generation_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRemediationTokenGenerationEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="accessDeniedPageUriInput")
    def access_denied_page_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessDeniedPageUriInput"))

    @builtins.property
    @jsii.member(jsii_name="generateTroubleshootingUriInput")
    def generate_troubleshooting_uri_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "generateTroubleshootingUriInput"))

    @builtins.property
    @jsii.member(jsii_name="remediationTokenGenerationEnabledInput")
    def remediation_token_generation_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "remediationTokenGenerationEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="accessDeniedPageUri")
    def access_denied_page_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessDeniedPageUri"))

    @access_denied_page_uri.setter
    def access_denied_page_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e495af7363da5bc834aa59cae6f1d74ce49050df2724c3ec86350e7849f77d30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessDeniedPageUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="generateTroubleshootingUri")
    def generate_troubleshooting_uri(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "generateTroubleshootingUri"))

    @generate_troubleshooting_uri.setter
    def generate_troubleshooting_uri(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98f144f855fe0ed163db53e11806fa843cd66ad9cf44440436f9e0e9170be08d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "generateTroubleshootingUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="remediationTokenGenerationEnabled")
    def remediation_token_generation_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "remediationTokenGenerationEnabled"))

    @remediation_token_generation_enabled.setter
    def remediation_token_generation_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbe2d4f2970fc6c95734b8a45cd8c506e99b19e12f2826feddefb9582094852b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "remediationTokenGenerationEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIapSettingsApplicationSettingsAccessDeniedPageSettings]:
        return typing.cast(typing.Optional[GoogleIapSettingsApplicationSettingsAccessDeniedPageSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIapSettingsApplicationSettingsAccessDeniedPageSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40c8a25bcb28acca0447a40a62e81f3f80ec4e4c2efe9e7d93f1754cbd04a8b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIapSettings.GoogleIapSettingsApplicationSettingsAttributePropagationSettings",
    jsii_struct_bases=[],
    name_mapping={
        "enable": "enable",
        "expression": "expression",
        "output_credentials": "outputCredentials",
    },
)
class GoogleIapSettingsApplicationSettingsAttributePropagationSettings:
    def __init__(
        self,
        *,
        enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        expression: typing.Optional[builtins.str] = None,
        output_credentials: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param enable: Whether the provided attribute propagation settings should be evaluated on user requests. If set to true, attributes returned from the expression will be propagated in the set output credentials. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#enable GoogleIapSettings#enable}
        :param expression: Raw string CEL expression. Must return a list of attributes. A maximum of 45 attributes can be selected. Expressions can select different attribute types from attributes: attributes.saml_attributes, attributes.iap_attributes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#expression GoogleIapSettings#expression}
        :param output_credentials: Which output credentials attributes selected by the CEL expression should be propagated in. All attributes will be fully duplicated in each selected output credential. Possible values are: - 'HEADER': Propagate attributes in the headers with "x-goog-iap-attr-" prefix. - 'JWT': Propagate attributes in the JWT of the form: "additional_claims": { "my_attribute": ["value1", "value2"] } - 'RCTOKEN': Propagate attributes in the RCToken of the form: " additional_claims": { "my_attribute": ["value1", "value2"] } Possible values: ["HEADER", "JWT", "RCTOKEN"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#output_credentials GoogleIapSettings#output_credentials}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7577c8258b59dd9f8ce427cfa7fc2adaf3474baa694265be93d4f36698ed741)
            check_type(argname="argument enable", value=enable, expected_type=type_hints["enable"])
            check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
            check_type(argname="argument output_credentials", value=output_credentials, expected_type=type_hints["output_credentials"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enable is not None:
            self._values["enable"] = enable
        if expression is not None:
            self._values["expression"] = expression
        if output_credentials is not None:
            self._values["output_credentials"] = output_credentials

    @builtins.property
    def enable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the provided attribute propagation settings should be evaluated on user requests.

        If set to true, attributes returned from the expression will be propagated in the set output credentials.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#enable GoogleIapSettings#enable}
        '''
        result = self._values.get("enable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def expression(self) -> typing.Optional[builtins.str]:
        '''Raw string CEL expression.

        Must return a list of attributes. A maximum of 45 attributes can
        be selected. Expressions can select different attribute types from attributes:
        attributes.saml_attributes, attributes.iap_attributes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#expression GoogleIapSettings#expression}
        '''
        result = self._values.get("expression")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def output_credentials(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Which output credentials attributes selected by the CEL expression should be propagated in.

        All attributes will be fully duplicated in each selected output credential.
        Possible values are:

        - 'HEADER': Propagate attributes in the headers with "x-goog-iap-attr-" prefix.
        - 'JWT': Propagate attributes in the JWT of the form:
          "additional_claims": { "my_attribute": ["value1", "value2"] }
        - 'RCTOKEN': Propagate attributes in the RCToken of the form: "
          additional_claims": { "my_attribute": ["value1", "value2"] } Possible values: ["HEADER", "JWT", "RCTOKEN"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#output_credentials GoogleIapSettings#output_credentials}
        '''
        result = self._values.get("output_credentials")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIapSettingsApplicationSettingsAttributePropagationSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIapSettingsApplicationSettingsAttributePropagationSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIapSettings.GoogleIapSettingsApplicationSettingsAttributePropagationSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3133e01b05c9510150407e312d69ca14ff3a20b4cb4ad7c77bf861abe6a8367b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnable")
    def reset_enable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnable", []))

    @jsii.member(jsii_name="resetExpression")
    def reset_expression(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpression", []))

    @jsii.member(jsii_name="resetOutputCredentials")
    def reset_output_credentials(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutputCredentials", []))

    @builtins.property
    @jsii.member(jsii_name="enableInput")
    def enable_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableInput"))

    @builtins.property
    @jsii.member(jsii_name="expressionInput")
    def expression_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expressionInput"))

    @builtins.property
    @jsii.member(jsii_name="outputCredentialsInput")
    def output_credentials_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "outputCredentialsInput"))

    @builtins.property
    @jsii.member(jsii_name="enable")
    def enable(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enable"))

    @enable.setter
    def enable(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59d91fbb034ab3887e838961e9338b1a9d548103c01d54620813a955f88afdcc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expression")
    def expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expression"))

    @expression.setter
    def expression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__897e201b577a626fcd3b38538781324a8b05f0f927dd96cb0af5e0b6b119ff93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="outputCredentials")
    def output_credentials(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "outputCredentials"))

    @output_credentials.setter
    def output_credentials(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2fd6c6e0bda6160ba6d8edf8a76d374f63a838c6779b0e04960b5420946e27c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outputCredentials", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIapSettingsApplicationSettingsAttributePropagationSettings]:
        return typing.cast(typing.Optional[GoogleIapSettingsApplicationSettingsAttributePropagationSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIapSettingsApplicationSettingsAttributePropagationSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b8d00decaf5e7ceacd8c51108f10b294ff81bab392b27297ffbeb642f7b8395)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIapSettings.GoogleIapSettingsApplicationSettingsCsmSettings",
    jsii_struct_bases=[],
    name_mapping={"rctoken_aud": "rctokenAud"},
)
class GoogleIapSettingsApplicationSettingsCsmSettings:
    def __init__(self, *, rctoken_aud: typing.Optional[builtins.str] = None) -> None:
        '''
        :param rctoken_aud: Audience claim set in the generated RCToken. This value is not validated by IAP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#rctoken_aud GoogleIapSettings#rctoken_aud}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15b55946571bc5e3cdfba973a983f558c58d54966b2529473a9cc7dd2cedf652)
            check_type(argname="argument rctoken_aud", value=rctoken_aud, expected_type=type_hints["rctoken_aud"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if rctoken_aud is not None:
            self._values["rctoken_aud"] = rctoken_aud

    @builtins.property
    def rctoken_aud(self) -> typing.Optional[builtins.str]:
        '''Audience claim set in the generated RCToken. This value is not validated by IAP.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#rctoken_aud GoogleIapSettings#rctoken_aud}
        '''
        result = self._values.get("rctoken_aud")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIapSettingsApplicationSettingsCsmSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIapSettingsApplicationSettingsCsmSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIapSettings.GoogleIapSettingsApplicationSettingsCsmSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__73949858843e06adaf685ab4eb61977a759b2943297f01b658f59ce070368fdb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetRctokenAud")
    def reset_rctoken_aud(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRctokenAud", []))

    @builtins.property
    @jsii.member(jsii_name="rctokenAudInput")
    def rctoken_aud_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rctokenAudInput"))

    @builtins.property
    @jsii.member(jsii_name="rctokenAud")
    def rctoken_aud(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rctokenAud"))

    @rctoken_aud.setter
    def rctoken_aud(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bd5b2b25301d298da685915c4ee48340abe1241e78b559c98ab22934573632b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rctokenAud", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIapSettingsApplicationSettingsCsmSettings]:
        return typing.cast(typing.Optional[GoogleIapSettingsApplicationSettingsCsmSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIapSettingsApplicationSettingsCsmSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c989a748f1141fe2ebd790396d674b3533c81f88ca16cad4f35fadfb0e829bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleIapSettingsApplicationSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIapSettings.GoogleIapSettingsApplicationSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a7aec5732d69f60acf45e3d5150613fc584cca4612386b1450be91abdfcf675)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAccessDeniedPageSettings")
    def put_access_denied_page_settings(
        self,
        *,
        access_denied_page_uri: typing.Optional[builtins.str] = None,
        generate_troubleshooting_uri: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        remediation_token_generation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param access_denied_page_uri: The URI to be redirected to when access is denied. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#access_denied_page_uri GoogleIapSettings#access_denied_page_uri}
        :param generate_troubleshooting_uri: Whether to generate a troubleshooting URL on access denied events to this application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#generate_troubleshooting_uri GoogleIapSettings#generate_troubleshooting_uri}
        :param remediation_token_generation_enabled: Whether to generate remediation token on access denied events to this application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#remediation_token_generation_enabled GoogleIapSettings#remediation_token_generation_enabled}
        '''
        value = GoogleIapSettingsApplicationSettingsAccessDeniedPageSettings(
            access_denied_page_uri=access_denied_page_uri,
            generate_troubleshooting_uri=generate_troubleshooting_uri,
            remediation_token_generation_enabled=remediation_token_generation_enabled,
        )

        return typing.cast(None, jsii.invoke(self, "putAccessDeniedPageSettings", [value]))

    @jsii.member(jsii_name="putAttributePropagationSettings")
    def put_attribute_propagation_settings(
        self,
        *,
        enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        expression: typing.Optional[builtins.str] = None,
        output_credentials: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param enable: Whether the provided attribute propagation settings should be evaluated on user requests. If set to true, attributes returned from the expression will be propagated in the set output credentials. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#enable GoogleIapSettings#enable}
        :param expression: Raw string CEL expression. Must return a list of attributes. A maximum of 45 attributes can be selected. Expressions can select different attribute types from attributes: attributes.saml_attributes, attributes.iap_attributes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#expression GoogleIapSettings#expression}
        :param output_credentials: Which output credentials attributes selected by the CEL expression should be propagated in. All attributes will be fully duplicated in each selected output credential. Possible values are: - 'HEADER': Propagate attributes in the headers with "x-goog-iap-attr-" prefix. - 'JWT': Propagate attributes in the JWT of the form: "additional_claims": { "my_attribute": ["value1", "value2"] } - 'RCTOKEN': Propagate attributes in the RCToken of the form: " additional_claims": { "my_attribute": ["value1", "value2"] } Possible values: ["HEADER", "JWT", "RCTOKEN"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#output_credentials GoogleIapSettings#output_credentials}
        '''
        value = GoogleIapSettingsApplicationSettingsAttributePropagationSettings(
            enable=enable, expression=expression, output_credentials=output_credentials
        )

        return typing.cast(None, jsii.invoke(self, "putAttributePropagationSettings", [value]))

    @jsii.member(jsii_name="putCsmSettings")
    def put_csm_settings(
        self,
        *,
        rctoken_aud: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param rctoken_aud: Audience claim set in the generated RCToken. This value is not validated by IAP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#rctoken_aud GoogleIapSettings#rctoken_aud}
        '''
        value = GoogleIapSettingsApplicationSettingsCsmSettings(
            rctoken_aud=rctoken_aud
        )

        return typing.cast(None, jsii.invoke(self, "putCsmSettings", [value]))

    @jsii.member(jsii_name="resetAccessDeniedPageSettings")
    def reset_access_denied_page_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessDeniedPageSettings", []))

    @jsii.member(jsii_name="resetAttributePropagationSettings")
    def reset_attribute_propagation_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAttributePropagationSettings", []))

    @jsii.member(jsii_name="resetCookieDomain")
    def reset_cookie_domain(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCookieDomain", []))

    @jsii.member(jsii_name="resetCsmSettings")
    def reset_csm_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCsmSettings", []))

    @builtins.property
    @jsii.member(jsii_name="accessDeniedPageSettings")
    def access_denied_page_settings(
        self,
    ) -> GoogleIapSettingsApplicationSettingsAccessDeniedPageSettingsOutputReference:
        return typing.cast(GoogleIapSettingsApplicationSettingsAccessDeniedPageSettingsOutputReference, jsii.get(self, "accessDeniedPageSettings"))

    @builtins.property
    @jsii.member(jsii_name="attributePropagationSettings")
    def attribute_propagation_settings(
        self,
    ) -> GoogleIapSettingsApplicationSettingsAttributePropagationSettingsOutputReference:
        return typing.cast(GoogleIapSettingsApplicationSettingsAttributePropagationSettingsOutputReference, jsii.get(self, "attributePropagationSettings"))

    @builtins.property
    @jsii.member(jsii_name="csmSettings")
    def csm_settings(
        self,
    ) -> GoogleIapSettingsApplicationSettingsCsmSettingsOutputReference:
        return typing.cast(GoogleIapSettingsApplicationSettingsCsmSettingsOutputReference, jsii.get(self, "csmSettings"))

    @builtins.property
    @jsii.member(jsii_name="accessDeniedPageSettingsInput")
    def access_denied_page_settings_input(
        self,
    ) -> typing.Optional[GoogleIapSettingsApplicationSettingsAccessDeniedPageSettings]:
        return typing.cast(typing.Optional[GoogleIapSettingsApplicationSettingsAccessDeniedPageSettings], jsii.get(self, "accessDeniedPageSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="attributePropagationSettingsInput")
    def attribute_propagation_settings_input(
        self,
    ) -> typing.Optional[GoogleIapSettingsApplicationSettingsAttributePropagationSettings]:
        return typing.cast(typing.Optional[GoogleIapSettingsApplicationSettingsAttributePropagationSettings], jsii.get(self, "attributePropagationSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="cookieDomainInput")
    def cookie_domain_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cookieDomainInput"))

    @builtins.property
    @jsii.member(jsii_name="csmSettingsInput")
    def csm_settings_input(
        self,
    ) -> typing.Optional[GoogleIapSettingsApplicationSettingsCsmSettings]:
        return typing.cast(typing.Optional[GoogleIapSettingsApplicationSettingsCsmSettings], jsii.get(self, "csmSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="cookieDomain")
    def cookie_domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cookieDomain"))

    @cookie_domain.setter
    def cookie_domain(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1031203a3e5a17eb9e04dd3f620d556be006ee113ce7231bd417cf713e41088a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cookieDomain", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleIapSettingsApplicationSettings]:
        return typing.cast(typing.Optional[GoogleIapSettingsApplicationSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIapSettingsApplicationSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07d49d6814dc3966cfe6b76cd5b674ab0d330482b5e76e6ee2dbe28dedd45500)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIapSettings.GoogleIapSettingsConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "name": "name",
        "access_settings": "accessSettings",
        "application_settings": "applicationSettings",
        "id": "id",
        "timeouts": "timeouts",
    },
)
class GoogleIapSettingsConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        name: builtins.str,
        access_settings: typing.Optional[typing.Union[GoogleIapSettingsAccessSettings, typing.Dict[builtins.str, typing.Any]]] = None,
        application_settings: typing.Optional[typing.Union[GoogleIapSettingsApplicationSettings, typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleIapSettingsTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: The resource name of the IAP protected resource. Name can have below resources: - organizations/{organization_id} - folders/{folder_id} - projects/{project_id} - projects/{project_id}/iap_web - projects/{project_id}/iap_web/compute - projects/{project_id}/iap_web/compute-{region} - projects/{project_id}/iap_web/compute/services/{service_id} - projects/{project_id}/iap_web/compute-{region}/services/{service_id} - projects/{project_id}/iap_web/appengine-{app_id} - projects/{project_id}/iap_web/appengine-{app_id}/services/{service_id} - projects/{project_id}/iap_web/appengine-{app_id}/services/{service_id}/version/{version_id} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#name GoogleIapSettings#name}
        :param access_settings: access_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#access_settings GoogleIapSettings#access_settings}
        :param application_settings: application_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#application_settings GoogleIapSettings#application_settings}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#id GoogleIapSettings#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#timeouts GoogleIapSettings#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(access_settings, dict):
            access_settings = GoogleIapSettingsAccessSettings(**access_settings)
        if isinstance(application_settings, dict):
            application_settings = GoogleIapSettingsApplicationSettings(**application_settings)
        if isinstance(timeouts, dict):
            timeouts = GoogleIapSettingsTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__968c1c6a2f418d43003a11a210d02e4a574ffba61458d59cc1d04479f6254a73)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument access_settings", value=access_settings, expected_type=type_hints["access_settings"])
            check_type(argname="argument application_settings", value=application_settings, expected_type=type_hints["application_settings"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
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
        if access_settings is not None:
            self._values["access_settings"] = access_settings
        if application_settings is not None:
            self._values["application_settings"] = application_settings
        if id is not None:
            self._values["id"] = id
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
    def name(self) -> builtins.str:
        '''The resource name of the IAP protected resource.

        Name can have below resources:

        - organizations/{organization_id}
        - folders/{folder_id}
        - projects/{project_id}
        - projects/{project_id}/iap_web
        - projects/{project_id}/iap_web/compute
        - projects/{project_id}/iap_web/compute-{region}
        - projects/{project_id}/iap_web/compute/services/{service_id}
        - projects/{project_id}/iap_web/compute-{region}/services/{service_id}
        - projects/{project_id}/iap_web/appengine-{app_id}
        - projects/{project_id}/iap_web/appengine-{app_id}/services/{service_id}
        - projects/{project_id}/iap_web/appengine-{app_id}/services/{service_id}/version/{version_id}

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#name GoogleIapSettings#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_settings(self) -> typing.Optional[GoogleIapSettingsAccessSettings]:
        '''access_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#access_settings GoogleIapSettings#access_settings}
        '''
        result = self._values.get("access_settings")
        return typing.cast(typing.Optional[GoogleIapSettingsAccessSettings], result)

    @builtins.property
    def application_settings(
        self,
    ) -> typing.Optional[GoogleIapSettingsApplicationSettings]:
        '''application_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#application_settings GoogleIapSettings#application_settings}
        '''
        result = self._values.get("application_settings")
        return typing.cast(typing.Optional[GoogleIapSettingsApplicationSettings], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#id GoogleIapSettings#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleIapSettingsTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#timeouts GoogleIapSettings#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleIapSettingsTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIapSettingsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIapSettings.GoogleIapSettingsTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleIapSettingsTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#create GoogleIapSettings#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#delete GoogleIapSettings#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#update GoogleIapSettings#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e54df8ed158994b43af7be7107f83122cfdf235842f1d9227f9985ff327606ab)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#create GoogleIapSettings#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#delete GoogleIapSettings#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_iap_settings#update GoogleIapSettings#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIapSettingsTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIapSettingsTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIapSettings.GoogleIapSettingsTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ba6eb5da011e379d337546c2b869aa3416ea3d8b2d6d9897c4442b9ea19c948b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c648a7d890b560aaa846afddaac4949d2b38afef51d578f34e73c6c7fd0fbbcf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03685e21b0a017ef3da59a4794f0a347e1236a3f6078ce9f5aa0fd326197ded3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21f6a5bf06500ab20ea5178c35dc05562b2616d20952f48c07b7ad0b585eadf3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIapSettingsTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIapSettingsTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIapSettingsTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__000c98cbfefcd36d8e9cc96f90c53616f293bbaded22efe8db9d95df2c23e4e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleIapSettings",
    "GoogleIapSettingsAccessSettings",
    "GoogleIapSettingsAccessSettingsAllowedDomainsSettings",
    "GoogleIapSettingsAccessSettingsAllowedDomainsSettingsOutputReference",
    "GoogleIapSettingsAccessSettingsCorsSettings",
    "GoogleIapSettingsAccessSettingsCorsSettingsOutputReference",
    "GoogleIapSettingsAccessSettingsGcipSettings",
    "GoogleIapSettingsAccessSettingsGcipSettingsOutputReference",
    "GoogleIapSettingsAccessSettingsOauthSettings",
    "GoogleIapSettingsAccessSettingsOauthSettingsOutputReference",
    "GoogleIapSettingsAccessSettingsOutputReference",
    "GoogleIapSettingsAccessSettingsReauthSettings",
    "GoogleIapSettingsAccessSettingsReauthSettingsOutputReference",
    "GoogleIapSettingsAccessSettingsWorkforceIdentitySettings",
    "GoogleIapSettingsAccessSettingsWorkforceIdentitySettingsOauth2",
    "GoogleIapSettingsAccessSettingsWorkforceIdentitySettingsOauth2OutputReference",
    "GoogleIapSettingsAccessSettingsWorkforceIdentitySettingsOutputReference",
    "GoogleIapSettingsApplicationSettings",
    "GoogleIapSettingsApplicationSettingsAccessDeniedPageSettings",
    "GoogleIapSettingsApplicationSettingsAccessDeniedPageSettingsOutputReference",
    "GoogleIapSettingsApplicationSettingsAttributePropagationSettings",
    "GoogleIapSettingsApplicationSettingsAttributePropagationSettingsOutputReference",
    "GoogleIapSettingsApplicationSettingsCsmSettings",
    "GoogleIapSettingsApplicationSettingsCsmSettingsOutputReference",
    "GoogleIapSettingsApplicationSettingsOutputReference",
    "GoogleIapSettingsConfig",
    "GoogleIapSettingsTimeouts",
    "GoogleIapSettingsTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__611cd777bb5dff5822d68548397ddcf57684e40e404c93e00b687e7301b7d106(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    access_settings: typing.Optional[typing.Union[GoogleIapSettingsAccessSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    application_settings: typing.Optional[typing.Union[GoogleIapSettingsApplicationSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleIapSettingsTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__cfe672fe20a7e58d70291b0219bdd098905301b6ff800b3a546733e3c33d8fbb(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__564c8f90bebce661230826b155a336d7399c3021d863fc6e3a0711fc75e1258d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44203fb5618bf44ba326eebe5d529ac42a4122b8d98592659f3bbcfe259fbdd7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a670cca7c8926e502a0d2bef9fd4d39f11d0305687913d60d0cc838793f08d7(
    *,
    allowed_domains_settings: typing.Optional[typing.Union[GoogleIapSettingsAccessSettingsAllowedDomainsSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    cors_settings: typing.Optional[typing.Union[GoogleIapSettingsAccessSettingsCorsSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    gcip_settings: typing.Optional[typing.Union[GoogleIapSettingsAccessSettingsGcipSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    identity_sources: typing.Optional[typing.Sequence[builtins.str]] = None,
    oauth_settings: typing.Optional[typing.Union[GoogleIapSettingsAccessSettingsOauthSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    reauth_settings: typing.Optional[typing.Union[GoogleIapSettingsAccessSettingsReauthSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    workforce_identity_settings: typing.Optional[typing.Union[GoogleIapSettingsAccessSettingsWorkforceIdentitySettings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7e7088ae7945aca88670d308ce6a309fe53c7864d1159b928d23838db24b8c1(
    *,
    domains: typing.Optional[typing.Sequence[builtins.str]] = None,
    enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e513b92489c9cdcee230194230efedf641c4a87ae1d10b2ff165e34e4cb2b92(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7f5e19ab7acc537083492fd4754218986f344e7b41150093c7c2c3827823afc(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28c134c0d1fb8e35d05613a32f2735dee4353950fe92d5794c2b70f807e465c2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00078765414d3ceba0a77372ee74e08c7b245d53e5a0299a6903bbd46e809360(
    value: typing.Optional[GoogleIapSettingsAccessSettingsAllowedDomainsSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2d295485ff0968cfb3d40d22373aff7f1e81574192f578a4a9855385876fce8(
    *,
    allow_http_options: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__302491b625d0d1b7128dfb8a1350bef58b89b67f6f9291a8db2c91a233ed2ccc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a278b1b39fa8655185aadf33eea6147ac28fa99c746e0ad6abe020fc853ee3e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33094455e0d724a16002d834343b22c729d6fa30dfebc515738f9d4e47911060(
    value: typing.Optional[GoogleIapSettingsAccessSettingsCorsSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03a85d1ecd8521fe5cd5bb2d81d209972a7102729d54409992ee69ca244b9e89(
    *,
    login_page_uri: typing.Optional[builtins.str] = None,
    tenant_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b1583f183225e0254fbfb22bab74ca91a7819b7fcc87919de275b50c70c9244(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1795e1edae4e55857c8614a28c53c331c533c7fcb3299d0a9c68ba44950178c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2487e40264b6e7b59301b8f480278fe2538f712554aa008c1efca5ff79a51c1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1874dd4ccbcbe4fc12ce95d15dfe2cb21ae1b0a2b3d9eaca65e088b30786ce39(
    value: typing.Optional[GoogleIapSettingsAccessSettingsGcipSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfe5f8423bc24863e77534deb9366029d8ee9169f4b7484120553710ae49ecde(
    *,
    login_hint: typing.Optional[builtins.str] = None,
    programmatic_clients: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f7b24ddd7011a28366f060e7e1aea36fb53b8e27f6845c0d67f642b1ed031e0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56424c00fcd8434a1c55ee75b519f32ae6c006d3fc1eb03c23c427c177c9717f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b95b0e8ab9b934d436b3e0d93b1f840bc0c17b0466944bfb0d64fa03a84d45a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e6e8a1744d7b254b694a0cd9b5d7002e2b500c239a79e74840bb30ae2f5fdb5(
    value: typing.Optional[GoogleIapSettingsAccessSettingsOauthSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d84f5288c2c0c496537d85d69a31a16419c5a40deb19f7c44cf03624a05a916(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf7322491f135524d9b1c4ffb0567753b434badb9edd8c37e5cc8ebf8973a2c5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b156cf3380bfb061573282fe3b5d6574ff0fc31b85c5a636ca981ed8380a1a25(
    value: typing.Optional[GoogleIapSettingsAccessSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5de0d32ab62a3da5b4a23faba5d0ce483ec43b53864835c31ed557a6be9f167(
    *,
    max_age: builtins.str,
    method: builtins.str,
    policy_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__196e12aecab60ff8e4bf69322547daa39b157c3d563d398d85adef7593a0eda0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb9a2d16d87aca898db3571a27e72be5ca07cae43cd6c1a02d26812a1d4892f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b08c78a345102909e3293fb7b52593a62ef8d9ff69541e3862dd694f20e9245d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b820709825280ad032b00b905ff1fd05fda70c188fd2a8435402917bb6faf39c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6af4fb26b228b49a3bf7d2138d2c6a4532a8980d88fcfa7192285ec913bbec8(
    value: typing.Optional[GoogleIapSettingsAccessSettingsReauthSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__841840908b6b84e10074b5fade5bf549c5652c2b1cb7cf926cab103c3b9d21e9(
    *,
    oauth2: typing.Optional[typing.Union[GoogleIapSettingsAccessSettingsWorkforceIdentitySettingsOauth2, typing.Dict[builtins.str, typing.Any]]] = None,
    workforce_pools: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__081141a58518a4f67ef890f94e57453050c91c0fbb9b87fe20f54762e51401ba(
    *,
    client_id: typing.Optional[builtins.str] = None,
    client_secret: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8e82ae46dba2a8218c37280126ef81c9a5beda192c075151af6bdcd67bdfca6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31818a528591d803b7ab720ca13d268db9c1795b1a8c2f4cd3345a42e6052379(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9817cae648aa420ca24cc2a32ec558e3d79ece7f342af499e834bdf4faaae97f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__269a4fd08db90ddd85ee1214a8c0bd091c998add1a016df478d24c7dff1f4bcb(
    value: typing.Optional[GoogleIapSettingsAccessSettingsWorkforceIdentitySettingsOauth2],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__641efa2eb5ed848bde98b1a1bc40e8058282d8548143652847d66e2b44278b7e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c7a4c3f103daeb36138a5fb1bded67495dd4e58229f625bc63cd42cd9fa666a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17b6d7412cfe55f2ca546b5e4ba67758fee17f46668f68270f4005b357a75488(
    value: typing.Optional[GoogleIapSettingsAccessSettingsWorkforceIdentitySettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fbdbe140a7c0db5d42699cdf690481fed6523da1f5cfeb56c79694750b5ca90(
    *,
    access_denied_page_settings: typing.Optional[typing.Union[GoogleIapSettingsApplicationSettingsAccessDeniedPageSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    attribute_propagation_settings: typing.Optional[typing.Union[GoogleIapSettingsApplicationSettingsAttributePropagationSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    cookie_domain: typing.Optional[builtins.str] = None,
    csm_settings: typing.Optional[typing.Union[GoogleIapSettingsApplicationSettingsCsmSettings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60f7348d751cc600d5e46a6a8067d5023cd54ea36b8412c5fe4e65cd7299759a(
    *,
    access_denied_page_uri: typing.Optional[builtins.str] = None,
    generate_troubleshooting_uri: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    remediation_token_generation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01bf46b967859a43323b442e717f16d5f27be73a5bff7d0d6dfdbc238f019f93(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e495af7363da5bc834aa59cae6f1d74ce49050df2724c3ec86350e7849f77d30(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98f144f855fe0ed163db53e11806fa843cd66ad9cf44440436f9e0e9170be08d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbe2d4f2970fc6c95734b8a45cd8c506e99b19e12f2826feddefb9582094852b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40c8a25bcb28acca0447a40a62e81f3f80ec4e4c2efe9e7d93f1754cbd04a8b7(
    value: typing.Optional[GoogleIapSettingsApplicationSettingsAccessDeniedPageSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7577c8258b59dd9f8ce427cfa7fc2adaf3474baa694265be93d4f36698ed741(
    *,
    enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    expression: typing.Optional[builtins.str] = None,
    output_credentials: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3133e01b05c9510150407e312d69ca14ff3a20b4cb4ad7c77bf861abe6a8367b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59d91fbb034ab3887e838961e9338b1a9d548103c01d54620813a955f88afdcc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__897e201b577a626fcd3b38538781324a8b05f0f927dd96cb0af5e0b6b119ff93(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2fd6c6e0bda6160ba6d8edf8a76d374f63a838c6779b0e04960b5420946e27c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b8d00decaf5e7ceacd8c51108f10b294ff81bab392b27297ffbeb642f7b8395(
    value: typing.Optional[GoogleIapSettingsApplicationSettingsAttributePropagationSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15b55946571bc5e3cdfba973a983f558c58d54966b2529473a9cc7dd2cedf652(
    *,
    rctoken_aud: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73949858843e06adaf685ab4eb61977a759b2943297f01b658f59ce070368fdb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bd5b2b25301d298da685915c4ee48340abe1241e78b559c98ab22934573632b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c989a748f1141fe2ebd790396d674b3533c81f88ca16cad4f35fadfb0e829bd(
    value: typing.Optional[GoogleIapSettingsApplicationSettingsCsmSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a7aec5732d69f60acf45e3d5150613fc584cca4612386b1450be91abdfcf675(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1031203a3e5a17eb9e04dd3f620d556be006ee113ce7231bd417cf713e41088a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07d49d6814dc3966cfe6b76cd5b674ab0d330482b5e76e6ee2dbe28dedd45500(
    value: typing.Optional[GoogleIapSettingsApplicationSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__968c1c6a2f418d43003a11a210d02e4a574ffba61458d59cc1d04479f6254a73(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    access_settings: typing.Optional[typing.Union[GoogleIapSettingsAccessSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    application_settings: typing.Optional[typing.Union[GoogleIapSettingsApplicationSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleIapSettingsTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e54df8ed158994b43af7be7107f83122cfdf235842f1d9227f9985ff327606ab(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba6eb5da011e379d337546c2b869aa3416ea3d8b2d6d9897c4442b9ea19c948b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c648a7d890b560aaa846afddaac4949d2b38afef51d578f34e73c6c7fd0fbbcf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03685e21b0a017ef3da59a4794f0a347e1236a3f6078ce9f5aa0fd326197ded3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21f6a5bf06500ab20ea5178c35dc05562b2616d20952f48c07b7ad0b585eadf3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__000c98cbfefcd36d8e9cc96f90c53616f293bbaded22efe8db9d95df2c23e4e2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIapSettingsTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
