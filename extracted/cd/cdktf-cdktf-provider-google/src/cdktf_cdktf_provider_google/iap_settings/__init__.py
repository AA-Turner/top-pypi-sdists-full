r'''
# `google_iap_settings`

Refer to the Terraform Registry for docs: [`google_iap_settings`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings).
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


class IapSettings(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.iapSettings.IapSettings",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings google_iap_settings}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        access_settings: typing.Optional[typing.Union["IapSettingsAccessSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        application_settings: typing.Optional[typing.Union["IapSettingsApplicationSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["IapSettingsTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings google_iap_settings} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: The resource name of the IAP protected resource. Name can have below resources: - organizations/{organization_id} - folders/{folder_id} - projects/{project_id} - projects/{project_id}/iap_web - projects/{project_id}/iap_web/compute - projects/{project_id}/iap_web/compute-{region} - projects/{project_id}/iap_web/compute/services/{service_id} - projects/{project_id}/iap_web/compute-{region}/services/{service_id} - projects/{project_id}/iap_web/appengine-{app_id} - projects/{project_id}/iap_web/appengine-{app_id}/services/{service_id} - projects/{project_id}/iap_web/appengine-{app_id}/services/{service_id}/version/{version_id} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#name IapSettings#name}
        :param access_settings: access_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#access_settings IapSettings#access_settings}
        :param application_settings: application_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#application_settings IapSettings#application_settings}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#id IapSettings#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#timeouts IapSettings#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c23f33d85adf356bbeb3cf098314168f3211655918e006e3c9012d234a33ba40)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = IapSettingsConfig(
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
        '''Generates CDKTF code for importing a IapSettings resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the IapSettings to import.
        :param import_from_id: The id of the existing IapSettings that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the IapSettings to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4837cfaadfc59c76849a1a7558387065ef74d50c64060a7a7878cc81dd1c5e2b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAccessSettings")
    def put_access_settings(
        self,
        *,
        allowed_domains_settings: typing.Optional[typing.Union["IapSettingsAccessSettingsAllowedDomainsSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        cors_settings: typing.Optional[typing.Union["IapSettingsAccessSettingsCorsSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        gcip_settings: typing.Optional[typing.Union["IapSettingsAccessSettingsGcipSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        identity_sources: typing.Optional[typing.Sequence[builtins.str]] = None,
        oauth_settings: typing.Optional[typing.Union["IapSettingsAccessSettingsOauthSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        reauth_settings: typing.Optional[typing.Union["IapSettingsAccessSettingsReauthSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        workforce_identity_settings: typing.Optional[typing.Union["IapSettingsAccessSettingsWorkforceIdentitySettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allowed_domains_settings: allowed_domains_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#allowed_domains_settings IapSettings#allowed_domains_settings}
        :param cors_settings: cors_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#cors_settings IapSettings#cors_settings}
        :param gcip_settings: gcip_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#gcip_settings IapSettings#gcip_settings}
        :param identity_sources: Identity sources that IAP can use to authenticate the end user. Only one identity source can be configured. The possible values are: - 'WORKFORCE_IDENTITY_FEDERATION': Use external identities set up on Google Cloud Workforce Identity Federation. Possible values: ["WORKFORCE_IDENTITY_FEDERATION"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#identity_sources IapSettings#identity_sources}
        :param oauth_settings: oauth_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#oauth_settings IapSettings#oauth_settings}
        :param reauth_settings: reauth_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#reauth_settings IapSettings#reauth_settings}
        :param workforce_identity_settings: workforce_identity_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#workforce_identity_settings IapSettings#workforce_identity_settings}
        '''
        value = IapSettingsAccessSettings(
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
        access_denied_page_settings: typing.Optional[typing.Union["IapSettingsApplicationSettingsAccessDeniedPageSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        attribute_propagation_settings: typing.Optional[typing.Union["IapSettingsApplicationSettingsAttributePropagationSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        cookie_domain: typing.Optional[builtins.str] = None,
        csm_settings: typing.Optional[typing.Union["IapSettingsApplicationSettingsCsmSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param access_denied_page_settings: access_denied_page_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#access_denied_page_settings IapSettings#access_denied_page_settings}
        :param attribute_propagation_settings: attribute_propagation_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#attribute_propagation_settings IapSettings#attribute_propagation_settings}
        :param cookie_domain: The Domain value to set for cookies generated by IAP. This value is not validated by the API, but will be ignored at runtime if invalid. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#cookie_domain IapSettings#cookie_domain}
        :param csm_settings: csm_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#csm_settings IapSettings#csm_settings}
        '''
        value = IapSettingsApplicationSettings(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#create IapSettings#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#delete IapSettings#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#update IapSettings#update}.
        '''
        value = IapSettingsTimeouts(create=create, delete=delete, update=update)

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
    def access_settings(self) -> "IapSettingsAccessSettingsOutputReference":
        return typing.cast("IapSettingsAccessSettingsOutputReference", jsii.get(self, "accessSettings"))

    @builtins.property
    @jsii.member(jsii_name="applicationSettings")
    def application_settings(self) -> "IapSettingsApplicationSettingsOutputReference":
        return typing.cast("IapSettingsApplicationSettingsOutputReference", jsii.get(self, "applicationSettings"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "IapSettingsTimeoutsOutputReference":
        return typing.cast("IapSettingsTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="accessSettingsInput")
    def access_settings_input(self) -> typing.Optional["IapSettingsAccessSettings"]:
        return typing.cast(typing.Optional["IapSettingsAccessSettings"], jsii.get(self, "accessSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="applicationSettingsInput")
    def application_settings_input(
        self,
    ) -> typing.Optional["IapSettingsApplicationSettings"]:
        return typing.cast(typing.Optional["IapSettingsApplicationSettings"], jsii.get(self, "applicationSettingsInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "IapSettingsTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "IapSettingsTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__174ffe31cca398cb44bd2142a7877a17255746831cb1edf2d3ad4b4aba49e0af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e798f2a1b76c51c9b0f81d83564869a2a3eac718cc3e5458d34450be2b8909c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.iapSettings.IapSettingsAccessSettings",
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
class IapSettingsAccessSettings:
    def __init__(
        self,
        *,
        allowed_domains_settings: typing.Optional[typing.Union["IapSettingsAccessSettingsAllowedDomainsSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        cors_settings: typing.Optional[typing.Union["IapSettingsAccessSettingsCorsSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        gcip_settings: typing.Optional[typing.Union["IapSettingsAccessSettingsGcipSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        identity_sources: typing.Optional[typing.Sequence[builtins.str]] = None,
        oauth_settings: typing.Optional[typing.Union["IapSettingsAccessSettingsOauthSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        reauth_settings: typing.Optional[typing.Union["IapSettingsAccessSettingsReauthSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        workforce_identity_settings: typing.Optional[typing.Union["IapSettingsAccessSettingsWorkforceIdentitySettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allowed_domains_settings: allowed_domains_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#allowed_domains_settings IapSettings#allowed_domains_settings}
        :param cors_settings: cors_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#cors_settings IapSettings#cors_settings}
        :param gcip_settings: gcip_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#gcip_settings IapSettings#gcip_settings}
        :param identity_sources: Identity sources that IAP can use to authenticate the end user. Only one identity source can be configured. The possible values are: - 'WORKFORCE_IDENTITY_FEDERATION': Use external identities set up on Google Cloud Workforce Identity Federation. Possible values: ["WORKFORCE_IDENTITY_FEDERATION"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#identity_sources IapSettings#identity_sources}
        :param oauth_settings: oauth_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#oauth_settings IapSettings#oauth_settings}
        :param reauth_settings: reauth_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#reauth_settings IapSettings#reauth_settings}
        :param workforce_identity_settings: workforce_identity_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#workforce_identity_settings IapSettings#workforce_identity_settings}
        '''
        if isinstance(allowed_domains_settings, dict):
            allowed_domains_settings = IapSettingsAccessSettingsAllowedDomainsSettings(**allowed_domains_settings)
        if isinstance(cors_settings, dict):
            cors_settings = IapSettingsAccessSettingsCorsSettings(**cors_settings)
        if isinstance(gcip_settings, dict):
            gcip_settings = IapSettingsAccessSettingsGcipSettings(**gcip_settings)
        if isinstance(oauth_settings, dict):
            oauth_settings = IapSettingsAccessSettingsOauthSettings(**oauth_settings)
        if isinstance(reauth_settings, dict):
            reauth_settings = IapSettingsAccessSettingsReauthSettings(**reauth_settings)
        if isinstance(workforce_identity_settings, dict):
            workforce_identity_settings = IapSettingsAccessSettingsWorkforceIdentitySettings(**workforce_identity_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d49dad08ba4f8080d05db405a9119c4de4eac8cd5a105defc8167c1d1f42eb0)
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
    ) -> typing.Optional["IapSettingsAccessSettingsAllowedDomainsSettings"]:
        '''allowed_domains_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#allowed_domains_settings IapSettings#allowed_domains_settings}
        '''
        result = self._values.get("allowed_domains_settings")
        return typing.cast(typing.Optional["IapSettingsAccessSettingsAllowedDomainsSettings"], result)

    @builtins.property
    def cors_settings(self) -> typing.Optional["IapSettingsAccessSettingsCorsSettings"]:
        '''cors_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#cors_settings IapSettings#cors_settings}
        '''
        result = self._values.get("cors_settings")
        return typing.cast(typing.Optional["IapSettingsAccessSettingsCorsSettings"], result)

    @builtins.property
    def gcip_settings(self) -> typing.Optional["IapSettingsAccessSettingsGcipSettings"]:
        '''gcip_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#gcip_settings IapSettings#gcip_settings}
        '''
        result = self._values.get("gcip_settings")
        return typing.cast(typing.Optional["IapSettingsAccessSettingsGcipSettings"], result)

    @builtins.property
    def identity_sources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Identity sources that IAP can use to authenticate the end user.

        Only one identity source
        can be configured. The possible values are:

        - 'WORKFORCE_IDENTITY_FEDERATION': Use external identities set up on Google Cloud Workforce
          Identity Federation. Possible values: ["WORKFORCE_IDENTITY_FEDERATION"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#identity_sources IapSettings#identity_sources}
        '''
        result = self._values.get("identity_sources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def oauth_settings(
        self,
    ) -> typing.Optional["IapSettingsAccessSettingsOauthSettings"]:
        '''oauth_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#oauth_settings IapSettings#oauth_settings}
        '''
        result = self._values.get("oauth_settings")
        return typing.cast(typing.Optional["IapSettingsAccessSettingsOauthSettings"], result)

    @builtins.property
    def reauth_settings(
        self,
    ) -> typing.Optional["IapSettingsAccessSettingsReauthSettings"]:
        '''reauth_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#reauth_settings IapSettings#reauth_settings}
        '''
        result = self._values.get("reauth_settings")
        return typing.cast(typing.Optional["IapSettingsAccessSettingsReauthSettings"], result)

    @builtins.property
    def workforce_identity_settings(
        self,
    ) -> typing.Optional["IapSettingsAccessSettingsWorkforceIdentitySettings"]:
        '''workforce_identity_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#workforce_identity_settings IapSettings#workforce_identity_settings}
        '''
        result = self._values.get("workforce_identity_settings")
        return typing.cast(typing.Optional["IapSettingsAccessSettingsWorkforceIdentitySettings"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IapSettingsAccessSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.iapSettings.IapSettingsAccessSettingsAllowedDomainsSettings",
    jsii_struct_bases=[],
    name_mapping={"domains": "domains", "enable": "enable"},
)
class IapSettingsAccessSettingsAllowedDomainsSettings:
    def __init__(
        self,
        *,
        domains: typing.Optional[typing.Sequence[builtins.str]] = None,
        enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param domains: List of trusted domains. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#domains IapSettings#domains}
        :param enable: Configuration for customers to opt in for the feature. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#enable IapSettings#enable}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4ee3283e85980fbb699c1affcf51afaf44cd50e7a2353317198ec46400d05bb)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#domains IapSettings#domains}
        '''
        result = self._values.get("domains")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def enable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Configuration for customers to opt in for the feature.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#enable IapSettings#enable}
        '''
        result = self._values.get("enable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IapSettingsAccessSettingsAllowedDomainsSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IapSettingsAccessSettingsAllowedDomainsSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.iapSettings.IapSettingsAccessSettingsAllowedDomainsSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__10337c37ad0f0a938658d3ba660b42ea3654c98c5dc649bd7974347c59755af3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d7e54d814973c67348024b05652850de3a9595283697ec0bb093d20a0b5956a9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2218a94feb3522e63fb2c516b67533ebb86da4b6fc32c9db364c16cb019a81e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IapSettingsAccessSettingsAllowedDomainsSettings]:
        return typing.cast(typing.Optional[IapSettingsAccessSettingsAllowedDomainsSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IapSettingsAccessSettingsAllowedDomainsSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__728bc3f35cccae539c1496540eb4781f9625ae897c2830160077290180e10c9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.iapSettings.IapSettingsAccessSettingsCorsSettings",
    jsii_struct_bases=[],
    name_mapping={"allow_http_options": "allowHttpOptions"},
)
class IapSettingsAccessSettingsCorsSettings:
    def __init__(
        self,
        *,
        allow_http_options: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param allow_http_options: Configuration to allow HTTP OPTIONS calls to skip authorization. If undefined, IAP will not apply any special logic to OPTIONS requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#allow_http_options IapSettings#allow_http_options}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d35232c21c2b225128eebc08a4ba535c2038273d6d0e5715bc70eb5dfd5c9b5c)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#allow_http_options IapSettings#allow_http_options}
        '''
        result = self._values.get("allow_http_options")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IapSettingsAccessSettingsCorsSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IapSettingsAccessSettingsCorsSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.iapSettings.IapSettingsAccessSettingsCorsSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b839a35137868a1b914bde9cb4a2577a08aa665b09adf39d1d9565fba619e2d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e5909647268ae68dd72f46e12e848193bcfd6f464283a504c7a72285d89bc850)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowHttpOptions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[IapSettingsAccessSettingsCorsSettings]:
        return typing.cast(typing.Optional[IapSettingsAccessSettingsCorsSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IapSettingsAccessSettingsCorsSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c452f0265ef5493f822094f9116c4f80de190d5803fb7139901e59fefb7258d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.iapSettings.IapSettingsAccessSettingsGcipSettings",
    jsii_struct_bases=[],
    name_mapping={"login_page_uri": "loginPageUri", "tenant_ids": "tenantIds"},
)
class IapSettingsAccessSettingsGcipSettings:
    def __init__(
        self,
        *,
        login_page_uri: typing.Optional[builtins.str] = None,
        tenant_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param login_page_uri: Login page URI associated with the GCIP tenants. Typically, all resources within the same project share the same login page, though it could be overridden at the sub resource level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#login_page_uri IapSettings#login_page_uri}
        :param tenant_ids: GCIP tenant ids that are linked to the IAP resource. tenantIds could be a string beginning with a number character to indicate authenticating with GCIP tenant flow, or in the format of _ to indicate authenticating with GCIP agent flow. If agent flow is used, tenantIds should only contain one single element, while for tenant flow, tenantIds can contain multiple elements. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#tenant_ids IapSettings#tenant_ids}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b87b25b9729ee9c43b3904fd3cfefe3e784170d035157f2648cb74d4b55e0f5)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#login_page_uri IapSettings#login_page_uri}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#tenant_ids IapSettings#tenant_ids}
        '''
        result = self._values.get("tenant_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IapSettingsAccessSettingsGcipSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IapSettingsAccessSettingsGcipSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.iapSettings.IapSettingsAccessSettingsGcipSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__26b6a105c1190da2e28fce6ae58e0fd61d43b8f2ca8d1281256d00fabae2a4a7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a8a787f78e988a3a375bd9ebeb4b12f4fe53e77b550b7082caf14ca2e5ad443)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loginPageUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tenantIds")
    def tenant_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tenantIds"))

    @tenant_ids.setter
    def tenant_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6187a7a759b715e6d9be1ae04cd31bed9ed1470a0a4869f9d3e67e92fd3aaab1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tenantIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[IapSettingsAccessSettingsGcipSettings]:
        return typing.cast(typing.Optional[IapSettingsAccessSettingsGcipSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IapSettingsAccessSettingsGcipSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9b1f9f9849ccc419380b30bdda5d8ff7f8d79ccac5b785c76da49d6a55ee1ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.iapSettings.IapSettingsAccessSettingsOauthSettings",
    jsii_struct_bases=[],
    name_mapping={
        "login_hint": "loginHint",
        "programmatic_clients": "programmaticClients",
    },
)
class IapSettingsAccessSettingsOauthSettings:
    def __init__(
        self,
        *,
        login_hint: typing.Optional[builtins.str] = None,
        programmatic_clients: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param login_hint: Domain hint to send as hd=? parameter in OAuth request flow. Enables redirect to primary IDP by skipping Google's login screen. (https://developers.google.com/identity/protocols/OpenIDConnect#hd-param) Note: IAP does not verify that the id token's hd claim matches this value since access behavior is managed by IAM policies. - loginHint setting is not a replacement for access control. Always enforce an appropriate access policy if you want to restrict access to users outside your domain. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#login_hint IapSettings#login_hint}
        :param programmatic_clients: List of client ids allowed to use IAP programmatically. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#programmatic_clients IapSettings#programmatic_clients}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__987d2655e902f556c5ac5416969e46869a8a5a35e78f630b5b055a5e01a45410)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#login_hint IapSettings#login_hint}
        '''
        result = self._values.get("login_hint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def programmatic_clients(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of client ids allowed to use IAP programmatically.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#programmatic_clients IapSettings#programmatic_clients}
        '''
        result = self._values.get("programmatic_clients")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IapSettingsAccessSettingsOauthSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IapSettingsAccessSettingsOauthSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.iapSettings.IapSettingsAccessSettingsOauthSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3fb9a567af2a8836defe95b3915080f1156466e23304405aed7ac2e54f4129e7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__91c76fff628b312b6475440289e4125e4f805b3cb8f2b93906634f061dcc7e7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loginHint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="programmaticClients")
    def programmatic_clients(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "programmaticClients"))

    @programmatic_clients.setter
    def programmatic_clients(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1506efc7cd4bbece9c7f833e6e201264bd6d7f033cdbea570aec92668891fc48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "programmaticClients", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[IapSettingsAccessSettingsOauthSettings]:
        return typing.cast(typing.Optional[IapSettingsAccessSettingsOauthSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IapSettingsAccessSettingsOauthSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e4671307c6eb522a6fb711206e7e505af5e6856813cb47227c961f6db4cb5c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IapSettingsAccessSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.iapSettings.IapSettingsAccessSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__641b5b546d6d13ebf361ade80a55c378472f8b4b5820737860abd29a9015a6db)
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
        :param domains: List of trusted domains. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#domains IapSettings#domains}
        :param enable: Configuration for customers to opt in for the feature. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#enable IapSettings#enable}
        '''
        value = IapSettingsAccessSettingsAllowedDomainsSettings(
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
        :param allow_http_options: Configuration to allow HTTP OPTIONS calls to skip authorization. If undefined, IAP will not apply any special logic to OPTIONS requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#allow_http_options IapSettings#allow_http_options}
        '''
        value = IapSettingsAccessSettingsCorsSettings(
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
        :param login_page_uri: Login page URI associated with the GCIP tenants. Typically, all resources within the same project share the same login page, though it could be overridden at the sub resource level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#login_page_uri IapSettings#login_page_uri}
        :param tenant_ids: GCIP tenant ids that are linked to the IAP resource. tenantIds could be a string beginning with a number character to indicate authenticating with GCIP tenant flow, or in the format of _ to indicate authenticating with GCIP agent flow. If agent flow is used, tenantIds should only contain one single element, while for tenant flow, tenantIds can contain multiple elements. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#tenant_ids IapSettings#tenant_ids}
        '''
        value = IapSettingsAccessSettingsGcipSettings(
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
        :param login_hint: Domain hint to send as hd=? parameter in OAuth request flow. Enables redirect to primary IDP by skipping Google's login screen. (https://developers.google.com/identity/protocols/OpenIDConnect#hd-param) Note: IAP does not verify that the id token's hd claim matches this value since access behavior is managed by IAM policies. - loginHint setting is not a replacement for access control. Always enforce an appropriate access policy if you want to restrict access to users outside your domain. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#login_hint IapSettings#login_hint}
        :param programmatic_clients: List of client ids allowed to use IAP programmatically. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#programmatic_clients IapSettings#programmatic_clients}
        '''
        value = IapSettingsAccessSettingsOauthSettings(
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
        :param max_age: Reauth session lifetime, how long before a user has to reauthenticate again. A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#max_age IapSettings#max_age}
        :param method: Reauth method requested. The possible values are:. - 'LOGIN': Prompts the user to log in again. - 'SECURE_KEY': User must use their secure key 2nd factor device. - 'ENROLLED_SECOND_FACTORS': User can use any enabled 2nd factor. Possible values: ["LOGIN", "SECURE_KEY", "ENROLLED_SECOND_FACTORS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#method IapSettings#method}
        :param policy_type: How IAP determines the effective policy in cases of hierarchical policies. Policies are merged from higher in the hierarchy to lower in the hierarchy. The possible values are: - 'MINIMUM': This policy acts as a minimum to other policies, lower in the hierarchy. Effective policy may only be the same or stricter. - 'DEFAULT': This policy acts as a default if no other reauth policy is set. Possible values: ["MINIMUM", "DEFAULT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#policy_type IapSettings#policy_type}
        '''
        value = IapSettingsAccessSettingsReauthSettings(
            max_age=max_age, method=method, policy_type=policy_type
        )

        return typing.cast(None, jsii.invoke(self, "putReauthSettings", [value]))

    @jsii.member(jsii_name="putWorkforceIdentitySettings")
    def put_workforce_identity_settings(
        self,
        *,
        oauth2: typing.Optional[typing.Union["IapSettingsAccessSettingsWorkforceIdentitySettingsOauth2", typing.Dict[builtins.str, typing.Any]]] = None,
        workforce_pools: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param oauth2: oauth2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#oauth2 IapSettings#oauth2}
        :param workforce_pools: The workforce pool resources. Only one workforce pool is accepted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#workforce_pools IapSettings#workforce_pools}
        '''
        value = IapSettingsAccessSettingsWorkforceIdentitySettings(
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
    ) -> IapSettingsAccessSettingsAllowedDomainsSettingsOutputReference:
        return typing.cast(IapSettingsAccessSettingsAllowedDomainsSettingsOutputReference, jsii.get(self, "allowedDomainsSettings"))

    @builtins.property
    @jsii.member(jsii_name="corsSettings")
    def cors_settings(self) -> IapSettingsAccessSettingsCorsSettingsOutputReference:
        return typing.cast(IapSettingsAccessSettingsCorsSettingsOutputReference, jsii.get(self, "corsSettings"))

    @builtins.property
    @jsii.member(jsii_name="gcipSettings")
    def gcip_settings(self) -> IapSettingsAccessSettingsGcipSettingsOutputReference:
        return typing.cast(IapSettingsAccessSettingsGcipSettingsOutputReference, jsii.get(self, "gcipSettings"))

    @builtins.property
    @jsii.member(jsii_name="oauthSettings")
    def oauth_settings(self) -> IapSettingsAccessSettingsOauthSettingsOutputReference:
        return typing.cast(IapSettingsAccessSettingsOauthSettingsOutputReference, jsii.get(self, "oauthSettings"))

    @builtins.property
    @jsii.member(jsii_name="reauthSettings")
    def reauth_settings(
        self,
    ) -> "IapSettingsAccessSettingsReauthSettingsOutputReference":
        return typing.cast("IapSettingsAccessSettingsReauthSettingsOutputReference", jsii.get(self, "reauthSettings"))

    @builtins.property
    @jsii.member(jsii_name="workforceIdentitySettings")
    def workforce_identity_settings(
        self,
    ) -> "IapSettingsAccessSettingsWorkforceIdentitySettingsOutputReference":
        return typing.cast("IapSettingsAccessSettingsWorkforceIdentitySettingsOutputReference", jsii.get(self, "workforceIdentitySettings"))

    @builtins.property
    @jsii.member(jsii_name="allowedDomainsSettingsInput")
    def allowed_domains_settings_input(
        self,
    ) -> typing.Optional[IapSettingsAccessSettingsAllowedDomainsSettings]:
        return typing.cast(typing.Optional[IapSettingsAccessSettingsAllowedDomainsSettings], jsii.get(self, "allowedDomainsSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="corsSettingsInput")
    def cors_settings_input(
        self,
    ) -> typing.Optional[IapSettingsAccessSettingsCorsSettings]:
        return typing.cast(typing.Optional[IapSettingsAccessSettingsCorsSettings], jsii.get(self, "corsSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="gcipSettingsInput")
    def gcip_settings_input(
        self,
    ) -> typing.Optional[IapSettingsAccessSettingsGcipSettings]:
        return typing.cast(typing.Optional[IapSettingsAccessSettingsGcipSettings], jsii.get(self, "gcipSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="identitySourcesInput")
    def identity_sources_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "identitySourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="oauthSettingsInput")
    def oauth_settings_input(
        self,
    ) -> typing.Optional[IapSettingsAccessSettingsOauthSettings]:
        return typing.cast(typing.Optional[IapSettingsAccessSettingsOauthSettings], jsii.get(self, "oauthSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="reauthSettingsInput")
    def reauth_settings_input(
        self,
    ) -> typing.Optional["IapSettingsAccessSettingsReauthSettings"]:
        return typing.cast(typing.Optional["IapSettingsAccessSettingsReauthSettings"], jsii.get(self, "reauthSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="workforceIdentitySettingsInput")
    def workforce_identity_settings_input(
        self,
    ) -> typing.Optional["IapSettingsAccessSettingsWorkforceIdentitySettings"]:
        return typing.cast(typing.Optional["IapSettingsAccessSettingsWorkforceIdentitySettings"], jsii.get(self, "workforceIdentitySettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="identitySources")
    def identity_sources(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "identitySources"))

    @identity_sources.setter
    def identity_sources(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a568e793ed67ee39a16e0e07b195a5b11cb823d6aa8e2c20aa1a577288ce9889)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identitySources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[IapSettingsAccessSettings]:
        return typing.cast(typing.Optional[IapSettingsAccessSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[IapSettingsAccessSettings]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7af1305179c9ffae1b1cc56d93592b50302c22435f3843505b97dafb313fd3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.iapSettings.IapSettingsAccessSettingsReauthSettings",
    jsii_struct_bases=[],
    name_mapping={
        "max_age": "maxAge",
        "method": "method",
        "policy_type": "policyType",
    },
)
class IapSettingsAccessSettingsReauthSettings:
    def __init__(
        self,
        *,
        max_age: builtins.str,
        method: builtins.str,
        policy_type: builtins.str,
    ) -> None:
        '''
        :param max_age: Reauth session lifetime, how long before a user has to reauthenticate again. A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#max_age IapSettings#max_age}
        :param method: Reauth method requested. The possible values are:. - 'LOGIN': Prompts the user to log in again. - 'SECURE_KEY': User must use their secure key 2nd factor device. - 'ENROLLED_SECOND_FACTORS': User can use any enabled 2nd factor. Possible values: ["LOGIN", "SECURE_KEY", "ENROLLED_SECOND_FACTORS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#method IapSettings#method}
        :param policy_type: How IAP determines the effective policy in cases of hierarchical policies. Policies are merged from higher in the hierarchy to lower in the hierarchy. The possible values are: - 'MINIMUM': This policy acts as a minimum to other policies, lower in the hierarchy. Effective policy may only be the same or stricter. - 'DEFAULT': This policy acts as a default if no other reauth policy is set. Possible values: ["MINIMUM", "DEFAULT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#policy_type IapSettings#policy_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df42e802f4eb62dc1317756d18f57fef32f37c42640e7a4fbbe8db5ac9e3f594)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#max_age IapSettings#max_age}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#method IapSettings#method}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#policy_type IapSettings#policy_type}
        '''
        result = self._values.get("policy_type")
        assert result is not None, "Required property 'policy_type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IapSettingsAccessSettingsReauthSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IapSettingsAccessSettingsReauthSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.iapSettings.IapSettingsAccessSettingsReauthSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b8549db8bf9fea67f8a5aa5a22c7921a154895dd97cff4d59907d99483e9adb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d7213e923cf990e0988b8cb0ee66c612883ff675281f36acdb74162323e942aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxAge", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="method")
    def method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "method"))

    @method.setter
    def method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec9b81f7d15968e49dec88f059832ef82ac38cc99c291862743a3b0e1ffd577f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "method", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="policyType")
    def policy_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyType"))

    @policy_type.setter
    def policy_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66ac2756a6b8e5096224cec8f147d168cd2d618bc67b066c734a59631c52e5c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IapSettingsAccessSettingsReauthSettings]:
        return typing.cast(typing.Optional[IapSettingsAccessSettingsReauthSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IapSettingsAccessSettingsReauthSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6102c3052763b4e60a86f98fdb3308acd7a7fc21deac5513a5b83552a94ca43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.iapSettings.IapSettingsAccessSettingsWorkforceIdentitySettings",
    jsii_struct_bases=[],
    name_mapping={"oauth2": "oauth2", "workforce_pools": "workforcePools"},
)
class IapSettingsAccessSettingsWorkforceIdentitySettings:
    def __init__(
        self,
        *,
        oauth2: typing.Optional[typing.Union["IapSettingsAccessSettingsWorkforceIdentitySettingsOauth2", typing.Dict[builtins.str, typing.Any]]] = None,
        workforce_pools: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param oauth2: oauth2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#oauth2 IapSettings#oauth2}
        :param workforce_pools: The workforce pool resources. Only one workforce pool is accepted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#workforce_pools IapSettings#workforce_pools}
        '''
        if isinstance(oauth2, dict):
            oauth2 = IapSettingsAccessSettingsWorkforceIdentitySettingsOauth2(**oauth2)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a4964af261e210759ab69feb7439e1297f4a3c41f392959a15840c55d9824dd)
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
    ) -> typing.Optional["IapSettingsAccessSettingsWorkforceIdentitySettingsOauth2"]:
        '''oauth2 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#oauth2 IapSettings#oauth2}
        '''
        result = self._values.get("oauth2")
        return typing.cast(typing.Optional["IapSettingsAccessSettingsWorkforceIdentitySettingsOauth2"], result)

    @builtins.property
    def workforce_pools(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The workforce pool resources. Only one workforce pool is accepted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#workforce_pools IapSettings#workforce_pools}
        '''
        result = self._values.get("workforce_pools")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IapSettingsAccessSettingsWorkforceIdentitySettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.iapSettings.IapSettingsAccessSettingsWorkforceIdentitySettingsOauth2",
    jsii_struct_bases=[],
    name_mapping={"client_id": "clientId", "client_secret": "clientSecret"},
)
class IapSettingsAccessSettingsWorkforceIdentitySettingsOauth2:
    def __init__(
        self,
        *,
        client_id: typing.Optional[builtins.str] = None,
        client_secret: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param client_id: The OAuth 2.0 client ID registered in the workforce identity federation OAuth 2.0 Server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#client_id IapSettings#client_id}
        :param client_secret: Input only. The OAuth 2.0 client secret created while registering the client ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#client_secret IapSettings#client_secret}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a3a57ce164d591eafd42efefdc6d7ca0ff8d9f73f50eb218e51a5044e913321)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#client_id IapSettings#client_id}
        '''
        result = self._values.get("client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_secret(self) -> typing.Optional[builtins.str]:
        '''Input only. The OAuth 2.0 client secret created while registering the client ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#client_secret IapSettings#client_secret}
        '''
        result = self._values.get("client_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IapSettingsAccessSettingsWorkforceIdentitySettingsOauth2(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IapSettingsAccessSettingsWorkforceIdentitySettingsOauth2OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.iapSettings.IapSettingsAccessSettingsWorkforceIdentitySettingsOauth2OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4fb84792e9b7109b77c3852192c81430328970a34d46e6f2be4eaf8f33e1edb8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f467596e1965bf79eebb4eca1d1d1acfd5c811664bac2f986f9bd76c51d6343)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecret"))

    @client_secret.setter
    def client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de83659c761a27df41835d65574bd6e5274c9d8316c7983f1e44e39a75c10893)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IapSettingsAccessSettingsWorkforceIdentitySettingsOauth2]:
        return typing.cast(typing.Optional[IapSettingsAccessSettingsWorkforceIdentitySettingsOauth2], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IapSettingsAccessSettingsWorkforceIdentitySettingsOauth2],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00f9bb4edce8ff736563d60298ecd6ff37cf67a4149fb26874737595bd90f7b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IapSettingsAccessSettingsWorkforceIdentitySettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.iapSettings.IapSettingsAccessSettingsWorkforceIdentitySettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__827c68c123c0d74f01857414f49f9277bc1075596bc3e33d8cf83feb82ee8576)
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
        :param client_id: The OAuth 2.0 client ID registered in the workforce identity federation OAuth 2.0 Server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#client_id IapSettings#client_id}
        :param client_secret: Input only. The OAuth 2.0 client secret created while registering the client ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#client_secret IapSettings#client_secret}
        '''
        value = IapSettingsAccessSettingsWorkforceIdentitySettingsOauth2(
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
    ) -> IapSettingsAccessSettingsWorkforceIdentitySettingsOauth2OutputReference:
        return typing.cast(IapSettingsAccessSettingsWorkforceIdentitySettingsOauth2OutputReference, jsii.get(self, "oauth2"))

    @builtins.property
    @jsii.member(jsii_name="oauth2Input")
    def oauth2_input(
        self,
    ) -> typing.Optional[IapSettingsAccessSettingsWorkforceIdentitySettingsOauth2]:
        return typing.cast(typing.Optional[IapSettingsAccessSettingsWorkforceIdentitySettingsOauth2], jsii.get(self, "oauth2Input"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__712593bff04e9b0d34d0abf98b31b2e2ca247c59fa515386549b1cefeaded0c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workforcePools", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IapSettingsAccessSettingsWorkforceIdentitySettings]:
        return typing.cast(typing.Optional[IapSettingsAccessSettingsWorkforceIdentitySettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IapSettingsAccessSettingsWorkforceIdentitySettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44bb4e243a037272e4d4eddb5ad7d0575f9526e8ec4c19afcb8a305999416460)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.iapSettings.IapSettingsApplicationSettings",
    jsii_struct_bases=[],
    name_mapping={
        "access_denied_page_settings": "accessDeniedPageSettings",
        "attribute_propagation_settings": "attributePropagationSettings",
        "cookie_domain": "cookieDomain",
        "csm_settings": "csmSettings",
    },
)
class IapSettingsApplicationSettings:
    def __init__(
        self,
        *,
        access_denied_page_settings: typing.Optional[typing.Union["IapSettingsApplicationSettingsAccessDeniedPageSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        attribute_propagation_settings: typing.Optional[typing.Union["IapSettingsApplicationSettingsAttributePropagationSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        cookie_domain: typing.Optional[builtins.str] = None,
        csm_settings: typing.Optional[typing.Union["IapSettingsApplicationSettingsCsmSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param access_denied_page_settings: access_denied_page_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#access_denied_page_settings IapSettings#access_denied_page_settings}
        :param attribute_propagation_settings: attribute_propagation_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#attribute_propagation_settings IapSettings#attribute_propagation_settings}
        :param cookie_domain: The Domain value to set for cookies generated by IAP. This value is not validated by the API, but will be ignored at runtime if invalid. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#cookie_domain IapSettings#cookie_domain}
        :param csm_settings: csm_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#csm_settings IapSettings#csm_settings}
        '''
        if isinstance(access_denied_page_settings, dict):
            access_denied_page_settings = IapSettingsApplicationSettingsAccessDeniedPageSettings(**access_denied_page_settings)
        if isinstance(attribute_propagation_settings, dict):
            attribute_propagation_settings = IapSettingsApplicationSettingsAttributePropagationSettings(**attribute_propagation_settings)
        if isinstance(csm_settings, dict):
            csm_settings = IapSettingsApplicationSettingsCsmSettings(**csm_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76e3855c4c6789e9bd9bbca981b3002f403f723d9d38ac2794b2c66b825575fa)
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
    ) -> typing.Optional["IapSettingsApplicationSettingsAccessDeniedPageSettings"]:
        '''access_denied_page_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#access_denied_page_settings IapSettings#access_denied_page_settings}
        '''
        result = self._values.get("access_denied_page_settings")
        return typing.cast(typing.Optional["IapSettingsApplicationSettingsAccessDeniedPageSettings"], result)

    @builtins.property
    def attribute_propagation_settings(
        self,
    ) -> typing.Optional["IapSettingsApplicationSettingsAttributePropagationSettings"]:
        '''attribute_propagation_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#attribute_propagation_settings IapSettings#attribute_propagation_settings}
        '''
        result = self._values.get("attribute_propagation_settings")
        return typing.cast(typing.Optional["IapSettingsApplicationSettingsAttributePropagationSettings"], result)

    @builtins.property
    def cookie_domain(self) -> typing.Optional[builtins.str]:
        '''The Domain value to set for cookies generated by IAP.

        This value is not validated by the API,
        but will be ignored at runtime if invalid.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#cookie_domain IapSettings#cookie_domain}
        '''
        result = self._values.get("cookie_domain")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def csm_settings(
        self,
    ) -> typing.Optional["IapSettingsApplicationSettingsCsmSettings"]:
        '''csm_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#csm_settings IapSettings#csm_settings}
        '''
        result = self._values.get("csm_settings")
        return typing.cast(typing.Optional["IapSettingsApplicationSettingsCsmSettings"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IapSettingsApplicationSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.iapSettings.IapSettingsApplicationSettingsAccessDeniedPageSettings",
    jsii_struct_bases=[],
    name_mapping={
        "access_denied_page_uri": "accessDeniedPageUri",
        "generate_troubleshooting_uri": "generateTroubleshootingUri",
        "remediation_token_generation_enabled": "remediationTokenGenerationEnabled",
    },
)
class IapSettingsApplicationSettingsAccessDeniedPageSettings:
    def __init__(
        self,
        *,
        access_denied_page_uri: typing.Optional[builtins.str] = None,
        generate_troubleshooting_uri: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        remediation_token_generation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param access_denied_page_uri: The URI to be redirected to when access is denied. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#access_denied_page_uri IapSettings#access_denied_page_uri}
        :param generate_troubleshooting_uri: Whether to generate a troubleshooting URL on access denied events to this application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#generate_troubleshooting_uri IapSettings#generate_troubleshooting_uri}
        :param remediation_token_generation_enabled: Whether to generate remediation token on access denied events to this application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#remediation_token_generation_enabled IapSettings#remediation_token_generation_enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f20cb873caac8df14e4bf6517f87569976bb16f027d2bdcdc425bc6ab7ad8f0d)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#access_denied_page_uri IapSettings#access_denied_page_uri}
        '''
        result = self._values.get("access_denied_page_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def generate_troubleshooting_uri(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to generate a troubleshooting URL on access denied events to this application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#generate_troubleshooting_uri IapSettings#generate_troubleshooting_uri}
        '''
        result = self._values.get("generate_troubleshooting_uri")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def remediation_token_generation_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to generate remediation token on access denied events to this application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#remediation_token_generation_enabled IapSettings#remediation_token_generation_enabled}
        '''
        result = self._values.get("remediation_token_generation_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IapSettingsApplicationSettingsAccessDeniedPageSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IapSettingsApplicationSettingsAccessDeniedPageSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.iapSettings.IapSettingsApplicationSettingsAccessDeniedPageSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f1738d8f5f6bd2f906c253bd20c509bf51570b265a8d84160758c3a601b8f34e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__31c7d1f0dbeaa8497e57a3fb7ca0fb5736e4eb95b27cfa1f5079253f343cda29)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b1221948d251df15f41c7b0dd2ad8f024cc03bd84b2b8dcccb487d8414d13520)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1958348e24c1d9fde7b40701f3f6d1eacf56d36639a43cd991765f582941ed99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "remediationTokenGenerationEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IapSettingsApplicationSettingsAccessDeniedPageSettings]:
        return typing.cast(typing.Optional[IapSettingsApplicationSettingsAccessDeniedPageSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IapSettingsApplicationSettingsAccessDeniedPageSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3991f685744079a86dba8d5207f0777e6de508d50cf5d1de7ad3d8775052bdf2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.iapSettings.IapSettingsApplicationSettingsAttributePropagationSettings",
    jsii_struct_bases=[],
    name_mapping={
        "enable": "enable",
        "expression": "expression",
        "output_credentials": "outputCredentials",
    },
)
class IapSettingsApplicationSettingsAttributePropagationSettings:
    def __init__(
        self,
        *,
        enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        expression: typing.Optional[builtins.str] = None,
        output_credentials: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param enable: Whether the provided attribute propagation settings should be evaluated on user requests. If set to true, attributes returned from the expression will be propagated in the set output credentials. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#enable IapSettings#enable}
        :param expression: Raw string CEL expression. Must return a list of attributes. A maximum of 45 attributes can be selected. Expressions can select different attribute types from attributes: attributes.saml_attributes, attributes.iap_attributes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#expression IapSettings#expression}
        :param output_credentials: Which output credentials attributes selected by the CEL expression should be propagated in. All attributes will be fully duplicated in each selected output credential. Possible values are: - 'HEADER': Propagate attributes in the headers with "x-goog-iap-attr-" prefix. - 'JWT': Propagate attributes in the JWT of the form: "additional_claims": { "my_attribute": ["value1", "value2"] } - 'RCTOKEN': Propagate attributes in the RCToken of the form: " additional_claims": { "my_attribute": ["value1", "value2"] } Possible values: ["HEADER", "JWT", "RCTOKEN"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#output_credentials IapSettings#output_credentials}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd18ed1de0e7953e4b963cd3ad91d4f7f9b290339987c4e238034c94b4109910)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#enable IapSettings#enable}
        '''
        result = self._values.get("enable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def expression(self) -> typing.Optional[builtins.str]:
        '''Raw string CEL expression.

        Must return a list of attributes. A maximum of 45 attributes can
        be selected. Expressions can select different attribute types from attributes:
        attributes.saml_attributes, attributes.iap_attributes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#expression IapSettings#expression}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#output_credentials IapSettings#output_credentials}
        '''
        result = self._values.get("output_credentials")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IapSettingsApplicationSettingsAttributePropagationSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IapSettingsApplicationSettingsAttributePropagationSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.iapSettings.IapSettingsApplicationSettingsAttributePropagationSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6cf9ccc4ba43570455f6daa9798233bbb5d560b94dd4bcd6a21ac9739a7a7712)
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
            type_hints = typing.get_type_hints(_typecheckingstub__55f3e7ae0668b7e635a12812d5bebad716c1fceca3274281413a555adc5bd8bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expression")
    def expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expression"))

    @expression.setter
    def expression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbfeb96d7e4e7bad2691c8b6f7dfe5a778e6023fc2f643632253192625293aed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="outputCredentials")
    def output_credentials(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "outputCredentials"))

    @output_credentials.setter
    def output_credentials(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df23061cfa27caac747d5629faa4b40e0e7656ba56009bee6dffd949148d6ac9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outputCredentials", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IapSettingsApplicationSettingsAttributePropagationSettings]:
        return typing.cast(typing.Optional[IapSettingsApplicationSettingsAttributePropagationSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IapSettingsApplicationSettingsAttributePropagationSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c70df3cf1949cd7d100f266fb4915b261c09f8fcd21b1c33fcdb2fea5d5e4c1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.iapSettings.IapSettingsApplicationSettingsCsmSettings",
    jsii_struct_bases=[],
    name_mapping={"rctoken_aud": "rctokenAud"},
)
class IapSettingsApplicationSettingsCsmSettings:
    def __init__(self, *, rctoken_aud: typing.Optional[builtins.str] = None) -> None:
        '''
        :param rctoken_aud: Audience claim set in the generated RCToken. This value is not validated by IAP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#rctoken_aud IapSettings#rctoken_aud}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__101fffd3952f523d4fd2632b750b9bf05045fa81733cd2f90592be900aae860a)
            check_type(argname="argument rctoken_aud", value=rctoken_aud, expected_type=type_hints["rctoken_aud"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if rctoken_aud is not None:
            self._values["rctoken_aud"] = rctoken_aud

    @builtins.property
    def rctoken_aud(self) -> typing.Optional[builtins.str]:
        '''Audience claim set in the generated RCToken. This value is not validated by IAP.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#rctoken_aud IapSettings#rctoken_aud}
        '''
        result = self._values.get("rctoken_aud")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IapSettingsApplicationSettingsCsmSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IapSettingsApplicationSettingsCsmSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.iapSettings.IapSettingsApplicationSettingsCsmSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b5897995a052ad5cbb754247fc8cff96c53e1e4b3393b2bdc3e5fab554708715)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4818bd8043b94d55d71396568c48bd2948bde9467c870cb7baaf3f01b01bf7fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rctokenAud", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IapSettingsApplicationSettingsCsmSettings]:
        return typing.cast(typing.Optional[IapSettingsApplicationSettingsCsmSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IapSettingsApplicationSettingsCsmSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16e3aecd69c3670aabaccd7bf159b1047734c6159b951a640b7aff0a6ae3991a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IapSettingsApplicationSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.iapSettings.IapSettingsApplicationSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f0af419bdc7502b64c3f562a66d68a1da6742ccdd2fb366a51ed6099b8507d01)
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
        :param access_denied_page_uri: The URI to be redirected to when access is denied. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#access_denied_page_uri IapSettings#access_denied_page_uri}
        :param generate_troubleshooting_uri: Whether to generate a troubleshooting URL on access denied events to this application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#generate_troubleshooting_uri IapSettings#generate_troubleshooting_uri}
        :param remediation_token_generation_enabled: Whether to generate remediation token on access denied events to this application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#remediation_token_generation_enabled IapSettings#remediation_token_generation_enabled}
        '''
        value = IapSettingsApplicationSettingsAccessDeniedPageSettings(
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
        :param enable: Whether the provided attribute propagation settings should be evaluated on user requests. If set to true, attributes returned from the expression will be propagated in the set output credentials. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#enable IapSettings#enable}
        :param expression: Raw string CEL expression. Must return a list of attributes. A maximum of 45 attributes can be selected. Expressions can select different attribute types from attributes: attributes.saml_attributes, attributes.iap_attributes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#expression IapSettings#expression}
        :param output_credentials: Which output credentials attributes selected by the CEL expression should be propagated in. All attributes will be fully duplicated in each selected output credential. Possible values are: - 'HEADER': Propagate attributes in the headers with "x-goog-iap-attr-" prefix. - 'JWT': Propagate attributes in the JWT of the form: "additional_claims": { "my_attribute": ["value1", "value2"] } - 'RCTOKEN': Propagate attributes in the RCToken of the form: " additional_claims": { "my_attribute": ["value1", "value2"] } Possible values: ["HEADER", "JWT", "RCTOKEN"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#output_credentials IapSettings#output_credentials}
        '''
        value = IapSettingsApplicationSettingsAttributePropagationSettings(
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
        :param rctoken_aud: Audience claim set in the generated RCToken. This value is not validated by IAP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#rctoken_aud IapSettings#rctoken_aud}
        '''
        value = IapSettingsApplicationSettingsCsmSettings(rctoken_aud=rctoken_aud)

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
    ) -> IapSettingsApplicationSettingsAccessDeniedPageSettingsOutputReference:
        return typing.cast(IapSettingsApplicationSettingsAccessDeniedPageSettingsOutputReference, jsii.get(self, "accessDeniedPageSettings"))

    @builtins.property
    @jsii.member(jsii_name="attributePropagationSettings")
    def attribute_propagation_settings(
        self,
    ) -> IapSettingsApplicationSettingsAttributePropagationSettingsOutputReference:
        return typing.cast(IapSettingsApplicationSettingsAttributePropagationSettingsOutputReference, jsii.get(self, "attributePropagationSettings"))

    @builtins.property
    @jsii.member(jsii_name="csmSettings")
    def csm_settings(self) -> IapSettingsApplicationSettingsCsmSettingsOutputReference:
        return typing.cast(IapSettingsApplicationSettingsCsmSettingsOutputReference, jsii.get(self, "csmSettings"))

    @builtins.property
    @jsii.member(jsii_name="accessDeniedPageSettingsInput")
    def access_denied_page_settings_input(
        self,
    ) -> typing.Optional[IapSettingsApplicationSettingsAccessDeniedPageSettings]:
        return typing.cast(typing.Optional[IapSettingsApplicationSettingsAccessDeniedPageSettings], jsii.get(self, "accessDeniedPageSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="attributePropagationSettingsInput")
    def attribute_propagation_settings_input(
        self,
    ) -> typing.Optional[IapSettingsApplicationSettingsAttributePropagationSettings]:
        return typing.cast(typing.Optional[IapSettingsApplicationSettingsAttributePropagationSettings], jsii.get(self, "attributePropagationSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="cookieDomainInput")
    def cookie_domain_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cookieDomainInput"))

    @builtins.property
    @jsii.member(jsii_name="csmSettingsInput")
    def csm_settings_input(
        self,
    ) -> typing.Optional[IapSettingsApplicationSettingsCsmSettings]:
        return typing.cast(typing.Optional[IapSettingsApplicationSettingsCsmSettings], jsii.get(self, "csmSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="cookieDomain")
    def cookie_domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cookieDomain"))

    @cookie_domain.setter
    def cookie_domain(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4591f190364db2d77921861fcbbe1b47e1965f45f6d048fc2602faf7087586b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cookieDomain", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[IapSettingsApplicationSettings]:
        return typing.cast(typing.Optional[IapSettingsApplicationSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IapSettingsApplicationSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__647b5f22282a1b3f89ce3fc253a13d107b43618e79bd75ebc835fa64dceb4f3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.iapSettings.IapSettingsConfig",
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
class IapSettingsConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        access_settings: typing.Optional[typing.Union[IapSettingsAccessSettings, typing.Dict[builtins.str, typing.Any]]] = None,
        application_settings: typing.Optional[typing.Union[IapSettingsApplicationSettings, typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["IapSettingsTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: The resource name of the IAP protected resource. Name can have below resources: - organizations/{organization_id} - folders/{folder_id} - projects/{project_id} - projects/{project_id}/iap_web - projects/{project_id}/iap_web/compute - projects/{project_id}/iap_web/compute-{region} - projects/{project_id}/iap_web/compute/services/{service_id} - projects/{project_id}/iap_web/compute-{region}/services/{service_id} - projects/{project_id}/iap_web/appengine-{app_id} - projects/{project_id}/iap_web/appengine-{app_id}/services/{service_id} - projects/{project_id}/iap_web/appengine-{app_id}/services/{service_id}/version/{version_id} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#name IapSettings#name}
        :param access_settings: access_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#access_settings IapSettings#access_settings}
        :param application_settings: application_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#application_settings IapSettings#application_settings}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#id IapSettings#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#timeouts IapSettings#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(access_settings, dict):
            access_settings = IapSettingsAccessSettings(**access_settings)
        if isinstance(application_settings, dict):
            application_settings = IapSettingsApplicationSettings(**application_settings)
        if isinstance(timeouts, dict):
            timeouts = IapSettingsTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fdfc1702b9d6901975383d43eeee7c63dddbe9a88599cfa7334ee4925d880be)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#name IapSettings#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_settings(self) -> typing.Optional[IapSettingsAccessSettings]:
        '''access_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#access_settings IapSettings#access_settings}
        '''
        result = self._values.get("access_settings")
        return typing.cast(typing.Optional[IapSettingsAccessSettings], result)

    @builtins.property
    def application_settings(self) -> typing.Optional[IapSettingsApplicationSettings]:
        '''application_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#application_settings IapSettings#application_settings}
        '''
        result = self._values.get("application_settings")
        return typing.cast(typing.Optional[IapSettingsApplicationSettings], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#id IapSettings#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["IapSettingsTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#timeouts IapSettings#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["IapSettingsTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IapSettingsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.iapSettings.IapSettingsTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class IapSettingsTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#create IapSettings#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#delete IapSettings#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#update IapSettings#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08fd959703b62a99480bd93e1e5226d41a2fc64c037f6bb8283b09c46182138e)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#create IapSettings#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#delete IapSettings#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iap_settings#update IapSettings#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IapSettingsTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IapSettingsTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.iapSettings.IapSettingsTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__21c7f44dd246dd4463c2e3f6ea84fb907a3f8a48a2ad6467cc53eb9f24b2e6c9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eefc4bb84f05070433b7873caff491dea76c489dcdb7a252ce0c9e04a76af031)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3e8b996231d03e71a9dc5cacff6a5b43e8f3fd44d1ca4df362a0e884bfdebda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c321db70801975e0e05dd2d28f3f73ba08aa20347e2141181b533067876562f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IapSettingsTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IapSettingsTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IapSettingsTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f510cef1a14d3204e01361926fdfa8d14480b30824fe99744d0ab04b7f57d7c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "IapSettings",
    "IapSettingsAccessSettings",
    "IapSettingsAccessSettingsAllowedDomainsSettings",
    "IapSettingsAccessSettingsAllowedDomainsSettingsOutputReference",
    "IapSettingsAccessSettingsCorsSettings",
    "IapSettingsAccessSettingsCorsSettingsOutputReference",
    "IapSettingsAccessSettingsGcipSettings",
    "IapSettingsAccessSettingsGcipSettingsOutputReference",
    "IapSettingsAccessSettingsOauthSettings",
    "IapSettingsAccessSettingsOauthSettingsOutputReference",
    "IapSettingsAccessSettingsOutputReference",
    "IapSettingsAccessSettingsReauthSettings",
    "IapSettingsAccessSettingsReauthSettingsOutputReference",
    "IapSettingsAccessSettingsWorkforceIdentitySettings",
    "IapSettingsAccessSettingsWorkforceIdentitySettingsOauth2",
    "IapSettingsAccessSettingsWorkforceIdentitySettingsOauth2OutputReference",
    "IapSettingsAccessSettingsWorkforceIdentitySettingsOutputReference",
    "IapSettingsApplicationSettings",
    "IapSettingsApplicationSettingsAccessDeniedPageSettings",
    "IapSettingsApplicationSettingsAccessDeniedPageSettingsOutputReference",
    "IapSettingsApplicationSettingsAttributePropagationSettings",
    "IapSettingsApplicationSettingsAttributePropagationSettingsOutputReference",
    "IapSettingsApplicationSettingsCsmSettings",
    "IapSettingsApplicationSettingsCsmSettingsOutputReference",
    "IapSettingsApplicationSettingsOutputReference",
    "IapSettingsConfig",
    "IapSettingsTimeouts",
    "IapSettingsTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__c23f33d85adf356bbeb3cf098314168f3211655918e006e3c9012d234a33ba40(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    access_settings: typing.Optional[typing.Union[IapSettingsAccessSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    application_settings: typing.Optional[typing.Union[IapSettingsApplicationSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[IapSettingsTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__4837cfaadfc59c76849a1a7558387065ef74d50c64060a7a7878cc81dd1c5e2b(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__174ffe31cca398cb44bd2142a7877a17255746831cb1edf2d3ad4b4aba49e0af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e798f2a1b76c51c9b0f81d83564869a2a3eac718cc3e5458d34450be2b8909c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d49dad08ba4f8080d05db405a9119c4de4eac8cd5a105defc8167c1d1f42eb0(
    *,
    allowed_domains_settings: typing.Optional[typing.Union[IapSettingsAccessSettingsAllowedDomainsSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    cors_settings: typing.Optional[typing.Union[IapSettingsAccessSettingsCorsSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    gcip_settings: typing.Optional[typing.Union[IapSettingsAccessSettingsGcipSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    identity_sources: typing.Optional[typing.Sequence[builtins.str]] = None,
    oauth_settings: typing.Optional[typing.Union[IapSettingsAccessSettingsOauthSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    reauth_settings: typing.Optional[typing.Union[IapSettingsAccessSettingsReauthSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    workforce_identity_settings: typing.Optional[typing.Union[IapSettingsAccessSettingsWorkforceIdentitySettings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4ee3283e85980fbb699c1affcf51afaf44cd50e7a2353317198ec46400d05bb(
    *,
    domains: typing.Optional[typing.Sequence[builtins.str]] = None,
    enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10337c37ad0f0a938658d3ba660b42ea3654c98c5dc649bd7974347c59755af3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7e54d814973c67348024b05652850de3a9595283697ec0bb093d20a0b5956a9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2218a94feb3522e63fb2c516b67533ebb86da4b6fc32c9db364c16cb019a81e6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__728bc3f35cccae539c1496540eb4781f9625ae897c2830160077290180e10c9d(
    value: typing.Optional[IapSettingsAccessSettingsAllowedDomainsSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d35232c21c2b225128eebc08a4ba535c2038273d6d0e5715bc70eb5dfd5c9b5c(
    *,
    allow_http_options: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b839a35137868a1b914bde9cb4a2577a08aa665b09adf39d1d9565fba619e2d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5909647268ae68dd72f46e12e848193bcfd6f464283a504c7a72285d89bc850(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c452f0265ef5493f822094f9116c4f80de190d5803fb7139901e59fefb7258d5(
    value: typing.Optional[IapSettingsAccessSettingsCorsSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b87b25b9729ee9c43b3904fd3cfefe3e784170d035157f2648cb74d4b55e0f5(
    *,
    login_page_uri: typing.Optional[builtins.str] = None,
    tenant_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26b6a105c1190da2e28fce6ae58e0fd61d43b8f2ca8d1281256d00fabae2a4a7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a8a787f78e988a3a375bd9ebeb4b12f4fe53e77b550b7082caf14ca2e5ad443(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6187a7a759b715e6d9be1ae04cd31bed9ed1470a0a4869f9d3e67e92fd3aaab1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9b1f9f9849ccc419380b30bdda5d8ff7f8d79ccac5b785c76da49d6a55ee1ae(
    value: typing.Optional[IapSettingsAccessSettingsGcipSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__987d2655e902f556c5ac5416969e46869a8a5a35e78f630b5b055a5e01a45410(
    *,
    login_hint: typing.Optional[builtins.str] = None,
    programmatic_clients: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fb9a567af2a8836defe95b3915080f1156466e23304405aed7ac2e54f4129e7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91c76fff628b312b6475440289e4125e4f805b3cb8f2b93906634f061dcc7e7c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1506efc7cd4bbece9c7f833e6e201264bd6d7f033cdbea570aec92668891fc48(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e4671307c6eb522a6fb711206e7e505af5e6856813cb47227c961f6db4cb5c8(
    value: typing.Optional[IapSettingsAccessSettingsOauthSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__641b5b546d6d13ebf361ade80a55c378472f8b4b5820737860abd29a9015a6db(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a568e793ed67ee39a16e0e07b195a5b11cb823d6aa8e2c20aa1a577288ce9889(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7af1305179c9ffae1b1cc56d93592b50302c22435f3843505b97dafb313fd3f(
    value: typing.Optional[IapSettingsAccessSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df42e802f4eb62dc1317756d18f57fef32f37c42640e7a4fbbe8db5ac9e3f594(
    *,
    max_age: builtins.str,
    method: builtins.str,
    policy_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b8549db8bf9fea67f8a5aa5a22c7921a154895dd97cff4d59907d99483e9adb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7213e923cf990e0988b8cb0ee66c612883ff675281f36acdb74162323e942aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec9b81f7d15968e49dec88f059832ef82ac38cc99c291862743a3b0e1ffd577f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66ac2756a6b8e5096224cec8f147d168cd2d618bc67b066c734a59631c52e5c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6102c3052763b4e60a86f98fdb3308acd7a7fc21deac5513a5b83552a94ca43(
    value: typing.Optional[IapSettingsAccessSettingsReauthSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a4964af261e210759ab69feb7439e1297f4a3c41f392959a15840c55d9824dd(
    *,
    oauth2: typing.Optional[typing.Union[IapSettingsAccessSettingsWorkforceIdentitySettingsOauth2, typing.Dict[builtins.str, typing.Any]]] = None,
    workforce_pools: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a3a57ce164d591eafd42efefdc6d7ca0ff8d9f73f50eb218e51a5044e913321(
    *,
    client_id: typing.Optional[builtins.str] = None,
    client_secret: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fb84792e9b7109b77c3852192c81430328970a34d46e6f2be4eaf8f33e1edb8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f467596e1965bf79eebb4eca1d1d1acfd5c811664bac2f986f9bd76c51d6343(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de83659c761a27df41835d65574bd6e5274c9d8316c7983f1e44e39a75c10893(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00f9bb4edce8ff736563d60298ecd6ff37cf67a4149fb26874737595bd90f7b6(
    value: typing.Optional[IapSettingsAccessSettingsWorkforceIdentitySettingsOauth2],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__827c68c123c0d74f01857414f49f9277bc1075596bc3e33d8cf83feb82ee8576(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__712593bff04e9b0d34d0abf98b31b2e2ca247c59fa515386549b1cefeaded0c0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44bb4e243a037272e4d4eddb5ad7d0575f9526e8ec4c19afcb8a305999416460(
    value: typing.Optional[IapSettingsAccessSettingsWorkforceIdentitySettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76e3855c4c6789e9bd9bbca981b3002f403f723d9d38ac2794b2c66b825575fa(
    *,
    access_denied_page_settings: typing.Optional[typing.Union[IapSettingsApplicationSettingsAccessDeniedPageSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    attribute_propagation_settings: typing.Optional[typing.Union[IapSettingsApplicationSettingsAttributePropagationSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    cookie_domain: typing.Optional[builtins.str] = None,
    csm_settings: typing.Optional[typing.Union[IapSettingsApplicationSettingsCsmSettings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f20cb873caac8df14e4bf6517f87569976bb16f027d2bdcdc425bc6ab7ad8f0d(
    *,
    access_denied_page_uri: typing.Optional[builtins.str] = None,
    generate_troubleshooting_uri: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    remediation_token_generation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1738d8f5f6bd2f906c253bd20c509bf51570b265a8d84160758c3a601b8f34e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31c7d1f0dbeaa8497e57a3fb7ca0fb5736e4eb95b27cfa1f5079253f343cda29(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1221948d251df15f41c7b0dd2ad8f024cc03bd84b2b8dcccb487d8414d13520(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1958348e24c1d9fde7b40701f3f6d1eacf56d36639a43cd991765f582941ed99(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3991f685744079a86dba8d5207f0777e6de508d50cf5d1de7ad3d8775052bdf2(
    value: typing.Optional[IapSettingsApplicationSettingsAccessDeniedPageSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd18ed1de0e7953e4b963cd3ad91d4f7f9b290339987c4e238034c94b4109910(
    *,
    enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    expression: typing.Optional[builtins.str] = None,
    output_credentials: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cf9ccc4ba43570455f6daa9798233bbb5d560b94dd4bcd6a21ac9739a7a7712(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55f3e7ae0668b7e635a12812d5bebad716c1fceca3274281413a555adc5bd8bc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbfeb96d7e4e7bad2691c8b6f7dfe5a778e6023fc2f643632253192625293aed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df23061cfa27caac747d5629faa4b40e0e7656ba56009bee6dffd949148d6ac9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c70df3cf1949cd7d100f266fb4915b261c09f8fcd21b1c33fcdb2fea5d5e4c1b(
    value: typing.Optional[IapSettingsApplicationSettingsAttributePropagationSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__101fffd3952f523d4fd2632b750b9bf05045fa81733cd2f90592be900aae860a(
    *,
    rctoken_aud: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5897995a052ad5cbb754247fc8cff96c53e1e4b3393b2bdc3e5fab554708715(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4818bd8043b94d55d71396568c48bd2948bde9467c870cb7baaf3f01b01bf7fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16e3aecd69c3670aabaccd7bf159b1047734c6159b951a640b7aff0a6ae3991a(
    value: typing.Optional[IapSettingsApplicationSettingsCsmSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0af419bdc7502b64c3f562a66d68a1da6742ccdd2fb366a51ed6099b8507d01(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4591f190364db2d77921861fcbbe1b47e1965f45f6d048fc2602faf7087586b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__647b5f22282a1b3f89ce3fc253a13d107b43618e79bd75ebc835fa64dceb4f3a(
    value: typing.Optional[IapSettingsApplicationSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fdfc1702b9d6901975383d43eeee7c63dddbe9a88599cfa7334ee4925d880be(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    access_settings: typing.Optional[typing.Union[IapSettingsAccessSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    application_settings: typing.Optional[typing.Union[IapSettingsApplicationSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[IapSettingsTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08fd959703b62a99480bd93e1e5226d41a2fc64c037f6bb8283b09c46182138e(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21c7f44dd246dd4463c2e3f6ea84fb907a3f8a48a2ad6467cc53eb9f24b2e6c9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eefc4bb84f05070433b7873caff491dea76c489dcdb7a252ce0c9e04a76af031(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3e8b996231d03e71a9dc5cacff6a5b43e8f3fd44d1ca4df362a0e884bfdebda(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c321db70801975e0e05dd2d28f3f73ba08aa20347e2141181b533067876562f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f510cef1a14d3204e01361926fdfa8d14480b30824fe99744d0ab04b7f57d7c8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IapSettingsTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
