r'''
# `google_app_engine_application`

Refer to the Terraform Registry for docs: [`google_app_engine_application`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_application).
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


class AppEngineApplication(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.appEngineApplication.AppEngineApplication",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_application google_app_engine_application}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location_id: builtins.str,
        auth_domain: typing.Optional[builtins.str] = None,
        database_type: typing.Optional[builtins.str] = None,
        feature_settings: typing.Optional[typing.Union["AppEngineApplicationFeatureSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        iap: typing.Optional[typing.Union["AppEngineApplicationIap", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        serving_status: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["AppEngineApplicationTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_application google_app_engine_application} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location_id: The location to serve the app from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_application#location_id AppEngineApplication#location_id}
        :param auth_domain: The domain to authenticate users with when using App Engine's User API. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_application#auth_domain AppEngineApplication#auth_domain}
        :param database_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_application#database_type AppEngineApplication#database_type}.
        :param feature_settings: feature_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_application#feature_settings AppEngineApplication#feature_settings}
        :param iap: iap block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_application#iap AppEngineApplication#iap}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_application#id AppEngineApplication#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: The project ID to create the application under. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_application#project AppEngineApplication#project}
        :param serving_status: The serving status of the app. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_application#serving_status AppEngineApplication#serving_status}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_application#timeouts AppEngineApplication#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c19ffb4d4126e9b9ee2e6657cfac62b7fb7d732ff7ef42ab6ce5bedabee1d7d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = AppEngineApplicationConfig(
            location_id=location_id,
            auth_domain=auth_domain,
            database_type=database_type,
            feature_settings=feature_settings,
            iap=iap,
            id=id,
            project=project,
            serving_status=serving_status,
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
        '''Generates CDKTF code for importing a AppEngineApplication resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the AppEngineApplication to import.
        :param import_from_id: The id of the existing AppEngineApplication that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_application#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the AppEngineApplication to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__843efcd4ff98d4921be2e9e8b79cee451852ea6ad75d40c76acab950293d7fca)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putFeatureSettings")
    def put_feature_settings(
        self,
        *,
        split_health_checks: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param split_health_checks: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_application#split_health_checks AppEngineApplication#split_health_checks}.
        '''
        value = AppEngineApplicationFeatureSettings(
            split_health_checks=split_health_checks
        )

        return typing.cast(None, jsii.invoke(self, "putFeatureSettings", [value]))

    @jsii.member(jsii_name="putIap")
    def put_iap(
        self,
        *,
        oauth2_client_id: builtins.str,
        oauth2_client_secret: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param oauth2_client_id: OAuth2 client ID to use for the authentication flow. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_application#oauth2_client_id AppEngineApplication#oauth2_client_id}
        :param oauth2_client_secret: OAuth2 client secret to use for the authentication flow. The SHA-256 hash of the value is returned in the oauth2ClientSecretSha256 field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_application#oauth2_client_secret AppEngineApplication#oauth2_client_secret}
        :param enabled: Adapted for use with the app. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_application#enabled AppEngineApplication#enabled}
        '''
        value = AppEngineApplicationIap(
            oauth2_client_id=oauth2_client_id,
            oauth2_client_secret=oauth2_client_secret,
            enabled=enabled,
        )

        return typing.cast(None, jsii.invoke(self, "putIap", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_application#create AppEngineApplication#create}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_application#update AppEngineApplication#update}.
        '''
        value = AppEngineApplicationTimeouts(create=create, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAuthDomain")
    def reset_auth_domain(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthDomain", []))

    @jsii.member(jsii_name="resetDatabaseType")
    def reset_database_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatabaseType", []))

    @jsii.member(jsii_name="resetFeatureSettings")
    def reset_feature_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFeatureSettings", []))

    @jsii.member(jsii_name="resetIap")
    def reset_iap(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIap", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetServingStatus")
    def reset_serving_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServingStatus", []))

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
    @jsii.member(jsii_name="appId")
    def app_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appId"))

    @builtins.property
    @jsii.member(jsii_name="codeBucket")
    def code_bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "codeBucket"))

    @builtins.property
    @jsii.member(jsii_name="defaultBucket")
    def default_bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultBucket"))

    @builtins.property
    @jsii.member(jsii_name="defaultHostname")
    def default_hostname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultHostname"))

    @builtins.property
    @jsii.member(jsii_name="featureSettings")
    def feature_settings(self) -> "AppEngineApplicationFeatureSettingsOutputReference":
        return typing.cast("AppEngineApplicationFeatureSettingsOutputReference", jsii.get(self, "featureSettings"))

    @builtins.property
    @jsii.member(jsii_name="gcrDomain")
    def gcr_domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gcrDomain"))

    @builtins.property
    @jsii.member(jsii_name="iap")
    def iap(self) -> "AppEngineApplicationIapOutputReference":
        return typing.cast("AppEngineApplicationIapOutputReference", jsii.get(self, "iap"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "AppEngineApplicationTimeoutsOutputReference":
        return typing.cast("AppEngineApplicationTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="urlDispatchRule")
    def url_dispatch_rule(self) -> "AppEngineApplicationUrlDispatchRuleList":
        return typing.cast("AppEngineApplicationUrlDispatchRuleList", jsii.get(self, "urlDispatchRule"))

    @builtins.property
    @jsii.member(jsii_name="authDomainInput")
    def auth_domain_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authDomainInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseTypeInput")
    def database_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="featureSettingsInput")
    def feature_settings_input(
        self,
    ) -> typing.Optional["AppEngineApplicationFeatureSettings"]:
        return typing.cast(typing.Optional["AppEngineApplicationFeatureSettings"], jsii.get(self, "featureSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="iapInput")
    def iap_input(self) -> typing.Optional["AppEngineApplicationIap"]:
        return typing.cast(typing.Optional["AppEngineApplicationIap"], jsii.get(self, "iapInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationIdInput")
    def location_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationIdInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="servingStatusInput")
    def serving_status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "servingStatusInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "AppEngineApplicationTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "AppEngineApplicationTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="authDomain")
    def auth_domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authDomain"))

    @auth_domain.setter
    def auth_domain(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3fe2ef6144d28ee3124009db96746f4e404575a49ea965de123027c431fbd7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authDomain", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="databaseType")
    def database_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseType"))

    @database_type.setter
    def database_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a343c9abc2cf6378bd9d5250cbb0d75a27f8f5e52934355cabf5bcdad260c303)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9423c59c82c8f897c8eca97805330d852e53f2352027e03500073d8e46031e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="locationId")
    def location_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "locationId"))

    @location_id.setter
    def location_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbaa934ede317c736faaa5b45e7144c2a27641110c8f2df31c87a9953c6b3bce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "locationId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60bd49a37b534c73189d8c8f36cbed8a00a217683385b142f0b60af588209b38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="servingStatus")
    def serving_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "servingStatus"))

    @serving_status.setter
    def serving_status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a26157a01f99bf1d3d90004cca2f023acc71f671915481b0d8fb475b2d087432)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "servingStatus", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.appEngineApplication.AppEngineApplicationConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "location_id": "locationId",
        "auth_domain": "authDomain",
        "database_type": "databaseType",
        "feature_settings": "featureSettings",
        "iap": "iap",
        "id": "id",
        "project": "project",
        "serving_status": "servingStatus",
        "timeouts": "timeouts",
    },
)
class AppEngineApplicationConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        location_id: builtins.str,
        auth_domain: typing.Optional[builtins.str] = None,
        database_type: typing.Optional[builtins.str] = None,
        feature_settings: typing.Optional[typing.Union["AppEngineApplicationFeatureSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        iap: typing.Optional[typing.Union["AppEngineApplicationIap", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        serving_status: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["AppEngineApplicationTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location_id: The location to serve the app from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_application#location_id AppEngineApplication#location_id}
        :param auth_domain: The domain to authenticate users with when using App Engine's User API. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_application#auth_domain AppEngineApplication#auth_domain}
        :param database_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_application#database_type AppEngineApplication#database_type}.
        :param feature_settings: feature_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_application#feature_settings AppEngineApplication#feature_settings}
        :param iap: iap block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_application#iap AppEngineApplication#iap}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_application#id AppEngineApplication#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: The project ID to create the application under. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_application#project AppEngineApplication#project}
        :param serving_status: The serving status of the app. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_application#serving_status AppEngineApplication#serving_status}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_application#timeouts AppEngineApplication#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(feature_settings, dict):
            feature_settings = AppEngineApplicationFeatureSettings(**feature_settings)
        if isinstance(iap, dict):
            iap = AppEngineApplicationIap(**iap)
        if isinstance(timeouts, dict):
            timeouts = AppEngineApplicationTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__315d7538893bf5a1392a31f47fa1ca4cb279334a79a8bf3056a758bbad3d6d2a)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location_id", value=location_id, expected_type=type_hints["location_id"])
            check_type(argname="argument auth_domain", value=auth_domain, expected_type=type_hints["auth_domain"])
            check_type(argname="argument database_type", value=database_type, expected_type=type_hints["database_type"])
            check_type(argname="argument feature_settings", value=feature_settings, expected_type=type_hints["feature_settings"])
            check_type(argname="argument iap", value=iap, expected_type=type_hints["iap"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument serving_status", value=serving_status, expected_type=type_hints["serving_status"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location_id": location_id,
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
        if auth_domain is not None:
            self._values["auth_domain"] = auth_domain
        if database_type is not None:
            self._values["database_type"] = database_type
        if feature_settings is not None:
            self._values["feature_settings"] = feature_settings
        if iap is not None:
            self._values["iap"] = iap
        if id is not None:
            self._values["id"] = id
        if project is not None:
            self._values["project"] = project
        if serving_status is not None:
            self._values["serving_status"] = serving_status
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
    def location_id(self) -> builtins.str:
        '''The location to serve the app from.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_application#location_id AppEngineApplication#location_id}
        '''
        result = self._values.get("location_id")
        assert result is not None, "Required property 'location_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auth_domain(self) -> typing.Optional[builtins.str]:
        '''The domain to authenticate users with when using App Engine's User API.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_application#auth_domain AppEngineApplication#auth_domain}
        '''
        result = self._values.get("auth_domain")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def database_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_application#database_type AppEngineApplication#database_type}.'''
        result = self._values.get("database_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def feature_settings(
        self,
    ) -> typing.Optional["AppEngineApplicationFeatureSettings"]:
        '''feature_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_application#feature_settings AppEngineApplication#feature_settings}
        '''
        result = self._values.get("feature_settings")
        return typing.cast(typing.Optional["AppEngineApplicationFeatureSettings"], result)

    @builtins.property
    def iap(self) -> typing.Optional["AppEngineApplicationIap"]:
        '''iap block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_application#iap AppEngineApplication#iap}
        '''
        result = self._values.get("iap")
        return typing.cast(typing.Optional["AppEngineApplicationIap"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_application#id AppEngineApplication#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''The project ID to create the application under.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_application#project AppEngineApplication#project}
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def serving_status(self) -> typing.Optional[builtins.str]:
        '''The serving status of the app.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_application#serving_status AppEngineApplication#serving_status}
        '''
        result = self._values.get("serving_status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["AppEngineApplicationTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_application#timeouts AppEngineApplication#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["AppEngineApplicationTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppEngineApplicationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.appEngineApplication.AppEngineApplicationFeatureSettings",
    jsii_struct_bases=[],
    name_mapping={"split_health_checks": "splitHealthChecks"},
)
class AppEngineApplicationFeatureSettings:
    def __init__(
        self,
        *,
        split_health_checks: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param split_health_checks: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_application#split_health_checks AppEngineApplication#split_health_checks}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed59b5812b806520bf636beeb88e94c47a7a76f59d1192de8b280e4a4cda44f1)
            check_type(argname="argument split_health_checks", value=split_health_checks, expected_type=type_hints["split_health_checks"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "split_health_checks": split_health_checks,
        }

    @builtins.property
    def split_health_checks(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_application#split_health_checks AppEngineApplication#split_health_checks}.'''
        result = self._values.get("split_health_checks")
        assert result is not None, "Required property 'split_health_checks' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppEngineApplicationFeatureSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppEngineApplicationFeatureSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.appEngineApplication.AppEngineApplicationFeatureSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__42434851dd33bd1bad2427bd57699e0a6f4082760788aa63029084daacf06205)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="splitHealthChecksInput")
    def split_health_checks_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "splitHealthChecksInput"))

    @builtins.property
    @jsii.member(jsii_name="splitHealthChecks")
    def split_health_checks(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "splitHealthChecks"))

    @split_health_checks.setter
    def split_health_checks(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edd40754fdc5167f4b86c787f791dd39734fbed0958b99dc29e203e3964799f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "splitHealthChecks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppEngineApplicationFeatureSettings]:
        return typing.cast(typing.Optional[AppEngineApplicationFeatureSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppEngineApplicationFeatureSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65c183cd429cfa01aecd4a28602afa665e5da80185cebda1370b55a43f5c3ba2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.appEngineApplication.AppEngineApplicationIap",
    jsii_struct_bases=[],
    name_mapping={
        "oauth2_client_id": "oauth2ClientId",
        "oauth2_client_secret": "oauth2ClientSecret",
        "enabled": "enabled",
    },
)
class AppEngineApplicationIap:
    def __init__(
        self,
        *,
        oauth2_client_id: builtins.str,
        oauth2_client_secret: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param oauth2_client_id: OAuth2 client ID to use for the authentication flow. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_application#oauth2_client_id AppEngineApplication#oauth2_client_id}
        :param oauth2_client_secret: OAuth2 client secret to use for the authentication flow. The SHA-256 hash of the value is returned in the oauth2ClientSecretSha256 field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_application#oauth2_client_secret AppEngineApplication#oauth2_client_secret}
        :param enabled: Adapted for use with the app. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_application#enabled AppEngineApplication#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e421507e5df849c1ba4ca7815b98a7e704bef568f5a190101e9a0a17925d4588)
            check_type(argname="argument oauth2_client_id", value=oauth2_client_id, expected_type=type_hints["oauth2_client_id"])
            check_type(argname="argument oauth2_client_secret", value=oauth2_client_secret, expected_type=type_hints["oauth2_client_secret"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "oauth2_client_id": oauth2_client_id,
            "oauth2_client_secret": oauth2_client_secret,
        }
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def oauth2_client_id(self) -> builtins.str:
        '''OAuth2 client ID to use for the authentication flow.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_application#oauth2_client_id AppEngineApplication#oauth2_client_id}
        '''
        result = self._values.get("oauth2_client_id")
        assert result is not None, "Required property 'oauth2_client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def oauth2_client_secret(self) -> builtins.str:
        '''OAuth2 client secret to use for the authentication flow.

        The SHA-256 hash of the value is returned in the oauth2ClientSecretSha256 field.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_application#oauth2_client_secret AppEngineApplication#oauth2_client_secret}
        '''
        result = self._values.get("oauth2_client_secret")
        assert result is not None, "Required property 'oauth2_client_secret' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Adapted for use with the app.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_application#enabled AppEngineApplication#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppEngineApplicationIap(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppEngineApplicationIapOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.appEngineApplication.AppEngineApplicationIapOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5fe12809670bab5dabb2de47c1f02900105bd50ee7d031fcd10de5f3a6c73b70)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="oauth2ClientSecretSha256")
    def oauth2_client_secret_sha256(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "oauth2ClientSecretSha256"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="oauth2ClientIdInput")
    def oauth2_client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "oauth2ClientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="oauth2ClientSecretInput")
    def oauth2_client_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "oauth2ClientSecretInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__5245a24c9db0b4e29e3418c5a4f265777f0de853de150d1d53365f2c4f3ba27e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oauth2ClientId")
    def oauth2_client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "oauth2ClientId"))

    @oauth2_client_id.setter
    def oauth2_client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfdec0e8590112b2f1861686b537e5e738beb73c10a9d95d12e871c58eb3c470)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauth2ClientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oauth2ClientSecret")
    def oauth2_client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "oauth2ClientSecret"))

    @oauth2_client_secret.setter
    def oauth2_client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84139896410fa53e9c8728b062c4932d0a6b586bbb46b8e951cdaa2c1b4819bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauth2ClientSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppEngineApplicationIap]:
        return typing.cast(typing.Optional[AppEngineApplicationIap], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[AppEngineApplicationIap]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3007fd8c250dd4fc05b4f89e821ed588d53cc39b3082c74e11ced1b0398da5f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.appEngineApplication.AppEngineApplicationTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "update": "update"},
)
class AppEngineApplicationTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_application#create AppEngineApplication#create}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_application#update AppEngineApplication#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d9ab535d3003417f2887b24634ffd08f200c56a99e2a5005bd2ffee6d6bf350)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_application#create AppEngineApplication#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/app_engine_application#update AppEngineApplication#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppEngineApplicationTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppEngineApplicationTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.appEngineApplication.AppEngineApplicationTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8baaab26f52583c596cd4ca6af71ec9f12af4a1b0a3e9cf3d47b3090be5d73cb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetUpdate")
    def reset_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdate", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__24e5ea0e44d460c3355fa43508ffe9c72e5cb553802b238eedf13e1d63290998)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce8c49e8ca3ebc8cbf2f30b2e2e51ee617bbfb6f3c3e9aa08b51d7bedaa0f7df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppEngineApplicationTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppEngineApplicationTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppEngineApplicationTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47ee097aae610bcc3ba668ef38d6738c82f2a01439da4430482f56d1cdd96188)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.appEngineApplication.AppEngineApplicationUrlDispatchRule",
    jsii_struct_bases=[],
    name_mapping={},
)
class AppEngineApplicationUrlDispatchRule:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppEngineApplicationUrlDispatchRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppEngineApplicationUrlDispatchRuleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.appEngineApplication.AppEngineApplicationUrlDispatchRuleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__540c17e8abfcbb93985dad9d119660cf0fc3bfa8c2ec70a18f6ac74bb1155cb4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AppEngineApplicationUrlDispatchRuleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffe82cdc084ece959377aca26704cd9ddd11ec0a98bad8784a8c01e360216243)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AppEngineApplicationUrlDispatchRuleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1be32c34c4032d1d66721dda6e616ec075ed32214cc5d9ff6486ad95196bf8aa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cde872b5324aeb943c417f0ef83ce487c7275c20964a8b62ccf79ddf535d197a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca237e30278b6952cebe65308bcab219d2113015cc9febf793a84e298ac124a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class AppEngineApplicationUrlDispatchRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.appEngineApplication.AppEngineApplicationUrlDispatchRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5eb9eb4eef617d4d37401e27960fc16f6ec6c437d06ba5c44ce7d552ac49002a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="domain")
    def domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domain"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "service"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppEngineApplicationUrlDispatchRule]:
        return typing.cast(typing.Optional[AppEngineApplicationUrlDispatchRule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppEngineApplicationUrlDispatchRule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6464989ec1ac4fe2a3b2561519e858c2a428e6afe484be6d6edc825c277201f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "AppEngineApplication",
    "AppEngineApplicationConfig",
    "AppEngineApplicationFeatureSettings",
    "AppEngineApplicationFeatureSettingsOutputReference",
    "AppEngineApplicationIap",
    "AppEngineApplicationIapOutputReference",
    "AppEngineApplicationTimeouts",
    "AppEngineApplicationTimeoutsOutputReference",
    "AppEngineApplicationUrlDispatchRule",
    "AppEngineApplicationUrlDispatchRuleList",
    "AppEngineApplicationUrlDispatchRuleOutputReference",
]

publication.publish()

def _typecheckingstub__6c19ffb4d4126e9b9ee2e6657cfac62b7fb7d732ff7ef42ab6ce5bedabee1d7d(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location_id: builtins.str,
    auth_domain: typing.Optional[builtins.str] = None,
    database_type: typing.Optional[builtins.str] = None,
    feature_settings: typing.Optional[typing.Union[AppEngineApplicationFeatureSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    iap: typing.Optional[typing.Union[AppEngineApplicationIap, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    serving_status: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[AppEngineApplicationTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__843efcd4ff98d4921be2e9e8b79cee451852ea6ad75d40c76acab950293d7fca(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3fe2ef6144d28ee3124009db96746f4e404575a49ea965de123027c431fbd7a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a343c9abc2cf6378bd9d5250cbb0d75a27f8f5e52934355cabf5bcdad260c303(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9423c59c82c8f897c8eca97805330d852e53f2352027e03500073d8e46031e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbaa934ede317c736faaa5b45e7144c2a27641110c8f2df31c87a9953c6b3bce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60bd49a37b534c73189d8c8f36cbed8a00a217683385b142f0b60af588209b38(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a26157a01f99bf1d3d90004cca2f023acc71f671915481b0d8fb475b2d087432(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__315d7538893bf5a1392a31f47fa1ca4cb279334a79a8bf3056a758bbad3d6d2a(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location_id: builtins.str,
    auth_domain: typing.Optional[builtins.str] = None,
    database_type: typing.Optional[builtins.str] = None,
    feature_settings: typing.Optional[typing.Union[AppEngineApplicationFeatureSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    iap: typing.Optional[typing.Union[AppEngineApplicationIap, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    serving_status: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[AppEngineApplicationTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed59b5812b806520bf636beeb88e94c47a7a76f59d1192de8b280e4a4cda44f1(
    *,
    split_health_checks: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42434851dd33bd1bad2427bd57699e0a6f4082760788aa63029084daacf06205(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edd40754fdc5167f4b86c787f791dd39734fbed0958b99dc29e203e3964799f0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65c183cd429cfa01aecd4a28602afa665e5da80185cebda1370b55a43f5c3ba2(
    value: typing.Optional[AppEngineApplicationFeatureSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e421507e5df849c1ba4ca7815b98a7e704bef568f5a190101e9a0a17925d4588(
    *,
    oauth2_client_id: builtins.str,
    oauth2_client_secret: builtins.str,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fe12809670bab5dabb2de47c1f02900105bd50ee7d031fcd10de5f3a6c73b70(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5245a24c9db0b4e29e3418c5a4f265777f0de853de150d1d53365f2c4f3ba27e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfdec0e8590112b2f1861686b537e5e738beb73c10a9d95d12e871c58eb3c470(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84139896410fa53e9c8728b062c4932d0a6b586bbb46b8e951cdaa2c1b4819bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3007fd8c250dd4fc05b4f89e821ed588d53cc39b3082c74e11ced1b0398da5f8(
    value: typing.Optional[AppEngineApplicationIap],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d9ab535d3003417f2887b24634ffd08f200c56a99e2a5005bd2ffee6d6bf350(
    *,
    create: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8baaab26f52583c596cd4ca6af71ec9f12af4a1b0a3e9cf3d47b3090be5d73cb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24e5ea0e44d460c3355fa43508ffe9c72e5cb553802b238eedf13e1d63290998(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce8c49e8ca3ebc8cbf2f30b2e2e51ee617bbfb6f3c3e9aa08b51d7bedaa0f7df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47ee097aae610bcc3ba668ef38d6738c82f2a01439da4430482f56d1cdd96188(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppEngineApplicationTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__540c17e8abfcbb93985dad9d119660cf0fc3bfa8c2ec70a18f6ac74bb1155cb4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffe82cdc084ece959377aca26704cd9ddd11ec0a98bad8784a8c01e360216243(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1be32c34c4032d1d66721dda6e616ec075ed32214cc5d9ff6486ad95196bf8aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cde872b5324aeb943c417f0ef83ce487c7275c20964a8b62ccf79ddf535d197a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca237e30278b6952cebe65308bcab219d2113015cc9febf793a84e298ac124a5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5eb9eb4eef617d4d37401e27960fc16f6ec6c437d06ba5c44ce7d552ac49002a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6464989ec1ac4fe2a3b2561519e858c2a428e6afe484be6d6edc825c277201f(
    value: typing.Optional[AppEngineApplicationUrlDispatchRule],
) -> None:
    """Type checking stubs"""
    pass
