r'''
# `google_bigquery_analytics_hub_data_exchange`

Refer to the Terraform Registry for docs: [`google_bigquery_analytics_hub_data_exchange`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_data_exchange).
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


class GoogleBigqueryAnalyticsHubDataExchange(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBigqueryAnalyticsHubDataExchange.GoogleBigqueryAnalyticsHubDataExchange",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_data_exchange google_bigquery_analytics_hub_data_exchange}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        data_exchange_id: builtins.str,
        display_name: builtins.str,
        location: builtins.str,
        description: typing.Optional[builtins.str] = None,
        documentation: typing.Optional[builtins.str] = None,
        icon: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        primary_contact: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        sharing_environment_config: typing.Optional[typing.Union["GoogleBigqueryAnalyticsHubDataExchangeSharingEnvironmentConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleBigqueryAnalyticsHubDataExchangeTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_data_exchange google_bigquery_analytics_hub_data_exchange} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param data_exchange_id: The ID of the data exchange. Must contain only Unicode letters, numbers (0-9), underscores (_). Should not use characters that require URL-escaping, or characters outside of ASCII, spaces. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_data_exchange#data_exchange_id GoogleBigqueryAnalyticsHubDataExchange#data_exchange_id}
        :param display_name: Human-readable display name of the data exchange. The display name must contain only Unicode letters, numbers (0-9), underscores (_), dashes (-), spaces ( ), and must not start or end with spaces. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_data_exchange#display_name GoogleBigqueryAnalyticsHubDataExchange#display_name}
        :param location: The name of the location this data exchange. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_data_exchange#location GoogleBigqueryAnalyticsHubDataExchange#location}
        :param description: Description of the data exchange. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_data_exchange#description GoogleBigqueryAnalyticsHubDataExchange#description}
        :param documentation: Documentation describing the data exchange. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_data_exchange#documentation GoogleBigqueryAnalyticsHubDataExchange#documentation}
        :param icon: Base64 encoded image representing the data exchange. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_data_exchange#icon GoogleBigqueryAnalyticsHubDataExchange#icon}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_data_exchange#id GoogleBigqueryAnalyticsHubDataExchange#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param primary_contact: Email or URL of the primary point of contact of the data exchange. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_data_exchange#primary_contact GoogleBigqueryAnalyticsHubDataExchange#primary_contact}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_data_exchange#project GoogleBigqueryAnalyticsHubDataExchange#project}.
        :param sharing_environment_config: sharing_environment_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_data_exchange#sharing_environment_config GoogleBigqueryAnalyticsHubDataExchange#sharing_environment_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_data_exchange#timeouts GoogleBigqueryAnalyticsHubDataExchange#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0593d4e51a56186b384356646e1c350c70954f6e99471d5edd271220d4cc265)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleBigqueryAnalyticsHubDataExchangeConfig(
            data_exchange_id=data_exchange_id,
            display_name=display_name,
            location=location,
            description=description,
            documentation=documentation,
            icon=icon,
            id=id,
            primary_contact=primary_contact,
            project=project,
            sharing_environment_config=sharing_environment_config,
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
        '''Generates CDKTF code for importing a GoogleBigqueryAnalyticsHubDataExchange resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleBigqueryAnalyticsHubDataExchange to import.
        :param import_from_id: The id of the existing GoogleBigqueryAnalyticsHubDataExchange that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_data_exchange#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleBigqueryAnalyticsHubDataExchange to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef3af2493e3c2cc37ec6362cdbcfa2e06d5edd1b2132e3064b1bc22d27db93ac)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putSharingEnvironmentConfig")
    def put_sharing_environment_config(
        self,
        *,
        dcr_exchange_config: typing.Optional[typing.Union["GoogleBigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDcrExchangeConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        default_exchange_config: typing.Optional[typing.Union["GoogleBigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDefaultExchangeConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param dcr_exchange_config: dcr_exchange_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_data_exchange#dcr_exchange_config GoogleBigqueryAnalyticsHubDataExchange#dcr_exchange_config}
        :param default_exchange_config: default_exchange_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_data_exchange#default_exchange_config GoogleBigqueryAnalyticsHubDataExchange#default_exchange_config}
        '''
        value = GoogleBigqueryAnalyticsHubDataExchangeSharingEnvironmentConfig(
            dcr_exchange_config=dcr_exchange_config,
            default_exchange_config=default_exchange_config,
        )

        return typing.cast(None, jsii.invoke(self, "putSharingEnvironmentConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_data_exchange#create GoogleBigqueryAnalyticsHubDataExchange#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_data_exchange#delete GoogleBigqueryAnalyticsHubDataExchange#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_data_exchange#update GoogleBigqueryAnalyticsHubDataExchange#update}.
        '''
        value = GoogleBigqueryAnalyticsHubDataExchangeTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDocumentation")
    def reset_documentation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDocumentation", []))

    @jsii.member(jsii_name="resetIcon")
    def reset_icon(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIcon", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetPrimaryContact")
    def reset_primary_contact(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrimaryContact", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetSharingEnvironmentConfig")
    def reset_sharing_environment_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSharingEnvironmentConfig", []))

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
    @jsii.member(jsii_name="listingCount")
    def listing_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "listingCount"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="sharingEnvironmentConfig")
    def sharing_environment_config(
        self,
    ) -> "GoogleBigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigOutputReference":
        return typing.cast("GoogleBigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigOutputReference", jsii.get(self, "sharingEnvironmentConfig"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "GoogleBigqueryAnalyticsHubDataExchangeTimeoutsOutputReference":
        return typing.cast("GoogleBigqueryAnalyticsHubDataExchangeTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="dataExchangeIdInput")
    def data_exchange_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataExchangeIdInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="documentationInput")
    def documentation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "documentationInput"))

    @builtins.property
    @jsii.member(jsii_name="iconInput")
    def icon_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "iconInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="primaryContactInput")
    def primary_contact_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "primaryContactInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="sharingEnvironmentConfigInput")
    def sharing_environment_config_input(
        self,
    ) -> typing.Optional["GoogleBigqueryAnalyticsHubDataExchangeSharingEnvironmentConfig"]:
        return typing.cast(typing.Optional["GoogleBigqueryAnalyticsHubDataExchangeSharingEnvironmentConfig"], jsii.get(self, "sharingEnvironmentConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleBigqueryAnalyticsHubDataExchangeTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleBigqueryAnalyticsHubDataExchangeTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="dataExchangeId")
    def data_exchange_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataExchangeId"))

    @data_exchange_id.setter
    def data_exchange_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a576f667ee7a16776d9345f69a9884771050a1765f8aac7ce6cfe70d88cba330)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataExchangeId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5d4a170e55b657b55192f7edac69b2ba3a6a9de311a5aaa3b8b0b1440b36a35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2939140585001593a3805a059755158624598c95d66978138b3a763ef11465cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="documentation")
    def documentation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "documentation"))

    @documentation.setter
    def documentation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d45faf50f6b93f7f60453417897d9019bd339b7f4ba6d205130fd6ab2c4ebff0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "documentation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="icon")
    def icon(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "icon"))

    @icon.setter
    def icon(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__740e4374064f65220feb48f42ececed231f37493eff8b2cfcd1f5367b4c9d19f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "icon", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4a1e4f462678b5d9b8203dda15942f00c8b455cc46cac746768ce1775b7685d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6afb13fb48ae12d16b2ee637bba4f9862bfba94103baac33121cb1dd9de7ca40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="primaryContact")
    def primary_contact(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryContact"))

    @primary_contact.setter
    def primary_contact(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31653d75bda1e67648da809c475666b4662690eac069f72c216967665025acfb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "primaryContact", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fbd62953a7feb8649095e0e924d3a8a64834cc4b9401c65a72be320bd381015)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBigqueryAnalyticsHubDataExchange.GoogleBigqueryAnalyticsHubDataExchangeConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "data_exchange_id": "dataExchangeId",
        "display_name": "displayName",
        "location": "location",
        "description": "description",
        "documentation": "documentation",
        "icon": "icon",
        "id": "id",
        "primary_contact": "primaryContact",
        "project": "project",
        "sharing_environment_config": "sharingEnvironmentConfig",
        "timeouts": "timeouts",
    },
)
class GoogleBigqueryAnalyticsHubDataExchangeConfig(
    _cdktf_9a9027ec.TerraformMetaArguments,
):
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
        data_exchange_id: builtins.str,
        display_name: builtins.str,
        location: builtins.str,
        description: typing.Optional[builtins.str] = None,
        documentation: typing.Optional[builtins.str] = None,
        icon: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        primary_contact: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        sharing_environment_config: typing.Optional[typing.Union["GoogleBigqueryAnalyticsHubDataExchangeSharingEnvironmentConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleBigqueryAnalyticsHubDataExchangeTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param data_exchange_id: The ID of the data exchange. Must contain only Unicode letters, numbers (0-9), underscores (_). Should not use characters that require URL-escaping, or characters outside of ASCII, spaces. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_data_exchange#data_exchange_id GoogleBigqueryAnalyticsHubDataExchange#data_exchange_id}
        :param display_name: Human-readable display name of the data exchange. The display name must contain only Unicode letters, numbers (0-9), underscores (_), dashes (-), spaces ( ), and must not start or end with spaces. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_data_exchange#display_name GoogleBigqueryAnalyticsHubDataExchange#display_name}
        :param location: The name of the location this data exchange. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_data_exchange#location GoogleBigqueryAnalyticsHubDataExchange#location}
        :param description: Description of the data exchange. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_data_exchange#description GoogleBigqueryAnalyticsHubDataExchange#description}
        :param documentation: Documentation describing the data exchange. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_data_exchange#documentation GoogleBigqueryAnalyticsHubDataExchange#documentation}
        :param icon: Base64 encoded image representing the data exchange. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_data_exchange#icon GoogleBigqueryAnalyticsHubDataExchange#icon}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_data_exchange#id GoogleBigqueryAnalyticsHubDataExchange#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param primary_contact: Email or URL of the primary point of contact of the data exchange. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_data_exchange#primary_contact GoogleBigqueryAnalyticsHubDataExchange#primary_contact}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_data_exchange#project GoogleBigqueryAnalyticsHubDataExchange#project}.
        :param sharing_environment_config: sharing_environment_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_data_exchange#sharing_environment_config GoogleBigqueryAnalyticsHubDataExchange#sharing_environment_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_data_exchange#timeouts GoogleBigqueryAnalyticsHubDataExchange#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(sharing_environment_config, dict):
            sharing_environment_config = GoogleBigqueryAnalyticsHubDataExchangeSharingEnvironmentConfig(**sharing_environment_config)
        if isinstance(timeouts, dict):
            timeouts = GoogleBigqueryAnalyticsHubDataExchangeTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ac017e8e1f23e9c6b921919ab9f7437c3456a05eb1f82d2e2d83fcb902faf38)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument data_exchange_id", value=data_exchange_id, expected_type=type_hints["data_exchange_id"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument documentation", value=documentation, expected_type=type_hints["documentation"])
            check_type(argname="argument icon", value=icon, expected_type=type_hints["icon"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument primary_contact", value=primary_contact, expected_type=type_hints["primary_contact"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument sharing_environment_config", value=sharing_environment_config, expected_type=type_hints["sharing_environment_config"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data_exchange_id": data_exchange_id,
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
        if description is not None:
            self._values["description"] = description
        if documentation is not None:
            self._values["documentation"] = documentation
        if icon is not None:
            self._values["icon"] = icon
        if id is not None:
            self._values["id"] = id
        if primary_contact is not None:
            self._values["primary_contact"] = primary_contact
        if project is not None:
            self._values["project"] = project
        if sharing_environment_config is not None:
            self._values["sharing_environment_config"] = sharing_environment_config
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
    def data_exchange_id(self) -> builtins.str:
        '''The ID of the data exchange.

        Must contain only Unicode letters, numbers (0-9), underscores (_). Should not use characters that require URL-escaping, or characters outside of ASCII, spaces.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_data_exchange#data_exchange_id GoogleBigqueryAnalyticsHubDataExchange#data_exchange_id}
        '''
        result = self._values.get("data_exchange_id")
        assert result is not None, "Required property 'data_exchange_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_name(self) -> builtins.str:
        '''Human-readable display name of the data exchange.

        The display name must contain only Unicode letters, numbers (0-9), underscores (_), dashes (-), spaces ( ), and must not start or end with spaces.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_data_exchange#display_name GoogleBigqueryAnalyticsHubDataExchange#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The name of the location this data exchange.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_data_exchange#location GoogleBigqueryAnalyticsHubDataExchange#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the data exchange.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_data_exchange#description GoogleBigqueryAnalyticsHubDataExchange#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def documentation(self) -> typing.Optional[builtins.str]:
        '''Documentation describing the data exchange.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_data_exchange#documentation GoogleBigqueryAnalyticsHubDataExchange#documentation}
        '''
        result = self._values.get("documentation")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def icon(self) -> typing.Optional[builtins.str]:
        '''Base64 encoded image representing the data exchange.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_data_exchange#icon GoogleBigqueryAnalyticsHubDataExchange#icon}
        '''
        result = self._values.get("icon")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_data_exchange#id GoogleBigqueryAnalyticsHubDataExchange#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def primary_contact(self) -> typing.Optional[builtins.str]:
        '''Email or URL of the primary point of contact of the data exchange.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_data_exchange#primary_contact GoogleBigqueryAnalyticsHubDataExchange#primary_contact}
        '''
        result = self._values.get("primary_contact")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_data_exchange#project GoogleBigqueryAnalyticsHubDataExchange#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sharing_environment_config(
        self,
    ) -> typing.Optional["GoogleBigqueryAnalyticsHubDataExchangeSharingEnvironmentConfig"]:
        '''sharing_environment_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_data_exchange#sharing_environment_config GoogleBigqueryAnalyticsHubDataExchange#sharing_environment_config}
        '''
        result = self._values.get("sharing_environment_config")
        return typing.cast(typing.Optional["GoogleBigqueryAnalyticsHubDataExchangeSharingEnvironmentConfig"], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["GoogleBigqueryAnalyticsHubDataExchangeTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_data_exchange#timeouts GoogleBigqueryAnalyticsHubDataExchange#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleBigqueryAnalyticsHubDataExchangeTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBigqueryAnalyticsHubDataExchangeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBigqueryAnalyticsHubDataExchange.GoogleBigqueryAnalyticsHubDataExchangeSharingEnvironmentConfig",
    jsii_struct_bases=[],
    name_mapping={
        "dcr_exchange_config": "dcrExchangeConfig",
        "default_exchange_config": "defaultExchangeConfig",
    },
)
class GoogleBigqueryAnalyticsHubDataExchangeSharingEnvironmentConfig:
    def __init__(
        self,
        *,
        dcr_exchange_config: typing.Optional[typing.Union["GoogleBigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDcrExchangeConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        default_exchange_config: typing.Optional[typing.Union["GoogleBigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDefaultExchangeConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param dcr_exchange_config: dcr_exchange_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_data_exchange#dcr_exchange_config GoogleBigqueryAnalyticsHubDataExchange#dcr_exchange_config}
        :param default_exchange_config: default_exchange_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_data_exchange#default_exchange_config GoogleBigqueryAnalyticsHubDataExchange#default_exchange_config}
        '''
        if isinstance(dcr_exchange_config, dict):
            dcr_exchange_config = GoogleBigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDcrExchangeConfig(**dcr_exchange_config)
        if isinstance(default_exchange_config, dict):
            default_exchange_config = GoogleBigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDefaultExchangeConfig(**default_exchange_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f970623f9fb96ef44281b1a0773d6f10a9c33c469f82a6386ae850c58dfe336)
            check_type(argname="argument dcr_exchange_config", value=dcr_exchange_config, expected_type=type_hints["dcr_exchange_config"])
            check_type(argname="argument default_exchange_config", value=default_exchange_config, expected_type=type_hints["default_exchange_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dcr_exchange_config is not None:
            self._values["dcr_exchange_config"] = dcr_exchange_config
        if default_exchange_config is not None:
            self._values["default_exchange_config"] = default_exchange_config

    @builtins.property
    def dcr_exchange_config(
        self,
    ) -> typing.Optional["GoogleBigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDcrExchangeConfig"]:
        '''dcr_exchange_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_data_exchange#dcr_exchange_config GoogleBigqueryAnalyticsHubDataExchange#dcr_exchange_config}
        '''
        result = self._values.get("dcr_exchange_config")
        return typing.cast(typing.Optional["GoogleBigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDcrExchangeConfig"], result)

    @builtins.property
    def default_exchange_config(
        self,
    ) -> typing.Optional["GoogleBigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDefaultExchangeConfig"]:
        '''default_exchange_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_data_exchange#default_exchange_config GoogleBigqueryAnalyticsHubDataExchange#default_exchange_config}
        '''
        result = self._values.get("default_exchange_config")
        return typing.cast(typing.Optional["GoogleBigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDefaultExchangeConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBigqueryAnalyticsHubDataExchangeSharingEnvironmentConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBigqueryAnalyticsHubDataExchange.GoogleBigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDcrExchangeConfig",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleBigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDcrExchangeConfig:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDcrExchangeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleBigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDcrExchangeConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBigqueryAnalyticsHubDataExchange.GoogleBigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDcrExchangeConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b69c9052e8821bb7a732ceb50bd5f2591f744e12ab3a2f8d90bca2b77ad9eb3c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleBigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDcrExchangeConfig]:
        return typing.cast(typing.Optional[GoogleBigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDcrExchangeConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleBigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDcrExchangeConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e276cc3a34453763a0608ae16d271c523193c8dd38b15e7b81f2e22d33691bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBigqueryAnalyticsHubDataExchange.GoogleBigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDefaultExchangeConfig",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleBigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDefaultExchangeConfig:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDefaultExchangeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleBigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDefaultExchangeConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBigqueryAnalyticsHubDataExchange.GoogleBigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDefaultExchangeConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2f9814cb9330606a618087fd6fd1d6bcf62286c992be4eef7fdd2a1436a8f733)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleBigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDefaultExchangeConfig]:
        return typing.cast(typing.Optional[GoogleBigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDefaultExchangeConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleBigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDefaultExchangeConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5226585d1a50145ffc8ec926f8cfec82d41ad60c776280ca800eb5fb9ef21322)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleBigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBigqueryAnalyticsHubDataExchange.GoogleBigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b51d8824cd9742fab168f0f16b34f9d591fb2f9cf37fa0ba20b2eab936a53ed)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDcrExchangeConfig")
    def put_dcr_exchange_config(self) -> None:
        value = GoogleBigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDcrExchangeConfig()

        return typing.cast(None, jsii.invoke(self, "putDcrExchangeConfig", [value]))

    @jsii.member(jsii_name="putDefaultExchangeConfig")
    def put_default_exchange_config(self) -> None:
        value = GoogleBigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDefaultExchangeConfig()

        return typing.cast(None, jsii.invoke(self, "putDefaultExchangeConfig", [value]))

    @jsii.member(jsii_name="resetDcrExchangeConfig")
    def reset_dcr_exchange_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDcrExchangeConfig", []))

    @jsii.member(jsii_name="resetDefaultExchangeConfig")
    def reset_default_exchange_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultExchangeConfig", []))

    @builtins.property
    @jsii.member(jsii_name="dcrExchangeConfig")
    def dcr_exchange_config(
        self,
    ) -> GoogleBigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDcrExchangeConfigOutputReference:
        return typing.cast(GoogleBigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDcrExchangeConfigOutputReference, jsii.get(self, "dcrExchangeConfig"))

    @builtins.property
    @jsii.member(jsii_name="defaultExchangeConfig")
    def default_exchange_config(
        self,
    ) -> GoogleBigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDefaultExchangeConfigOutputReference:
        return typing.cast(GoogleBigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDefaultExchangeConfigOutputReference, jsii.get(self, "defaultExchangeConfig"))

    @builtins.property
    @jsii.member(jsii_name="dcrExchangeConfigInput")
    def dcr_exchange_config_input(
        self,
    ) -> typing.Optional[GoogleBigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDcrExchangeConfig]:
        return typing.cast(typing.Optional[GoogleBigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDcrExchangeConfig], jsii.get(self, "dcrExchangeConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultExchangeConfigInput")
    def default_exchange_config_input(
        self,
    ) -> typing.Optional[GoogleBigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDefaultExchangeConfig]:
        return typing.cast(typing.Optional[GoogleBigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDefaultExchangeConfig], jsii.get(self, "defaultExchangeConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleBigqueryAnalyticsHubDataExchangeSharingEnvironmentConfig]:
        return typing.cast(typing.Optional[GoogleBigqueryAnalyticsHubDataExchangeSharingEnvironmentConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleBigqueryAnalyticsHubDataExchangeSharingEnvironmentConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3471890bb66c08bd05f73479ba53ae5003727d59ae1b414b6ff4cea9e5364979)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBigqueryAnalyticsHubDataExchange.GoogleBigqueryAnalyticsHubDataExchangeTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleBigqueryAnalyticsHubDataExchangeTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_data_exchange#create GoogleBigqueryAnalyticsHubDataExchange#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_data_exchange#delete GoogleBigqueryAnalyticsHubDataExchange#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_data_exchange#update GoogleBigqueryAnalyticsHubDataExchange#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__572e6a9240353476dd275b25a312d6cc182f47d52a5c45d23846daf41bd1cefb)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_data_exchange#create GoogleBigqueryAnalyticsHubDataExchange#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_data_exchange#delete GoogleBigqueryAnalyticsHubDataExchange#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_analytics_hub_data_exchange#update GoogleBigqueryAnalyticsHubDataExchange#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBigqueryAnalyticsHubDataExchangeTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleBigqueryAnalyticsHubDataExchangeTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBigqueryAnalyticsHubDataExchange.GoogleBigqueryAnalyticsHubDataExchangeTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4e0c694b9fef2befeea34cf119deefadb843ac0aa5f98b38492f199ff24bb24e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f352ecfd69b92e37461b040ceddadcdcdf3235db564f30abc2259fa1b3553f5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__334a28c884bfb363effaecda06466d0dca61eb73d8152ab602b8c807179f39bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa9c713e6e668a712c4e83742cd9928ec4a18569cd3dcffc97109c4e3d725088)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBigqueryAnalyticsHubDataExchangeTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBigqueryAnalyticsHubDataExchangeTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBigqueryAnalyticsHubDataExchangeTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b932188a07d364bf2cd6e57f7d0c7d95b3ec28f6436f8c49e65aa420ec8477d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleBigqueryAnalyticsHubDataExchange",
    "GoogleBigqueryAnalyticsHubDataExchangeConfig",
    "GoogleBigqueryAnalyticsHubDataExchangeSharingEnvironmentConfig",
    "GoogleBigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDcrExchangeConfig",
    "GoogleBigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDcrExchangeConfigOutputReference",
    "GoogleBigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDefaultExchangeConfig",
    "GoogleBigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDefaultExchangeConfigOutputReference",
    "GoogleBigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigOutputReference",
    "GoogleBigqueryAnalyticsHubDataExchangeTimeouts",
    "GoogleBigqueryAnalyticsHubDataExchangeTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__b0593d4e51a56186b384356646e1c350c70954f6e99471d5edd271220d4cc265(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    data_exchange_id: builtins.str,
    display_name: builtins.str,
    location: builtins.str,
    description: typing.Optional[builtins.str] = None,
    documentation: typing.Optional[builtins.str] = None,
    icon: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    primary_contact: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    sharing_environment_config: typing.Optional[typing.Union[GoogleBigqueryAnalyticsHubDataExchangeSharingEnvironmentConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleBigqueryAnalyticsHubDataExchangeTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__ef3af2493e3c2cc37ec6362cdbcfa2e06d5edd1b2132e3064b1bc22d27db93ac(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a576f667ee7a16776d9345f69a9884771050a1765f8aac7ce6cfe70d88cba330(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5d4a170e55b657b55192f7edac69b2ba3a6a9de311a5aaa3b8b0b1440b36a35(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2939140585001593a3805a059755158624598c95d66978138b3a763ef11465cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d45faf50f6b93f7f60453417897d9019bd339b7f4ba6d205130fd6ab2c4ebff0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__740e4374064f65220feb48f42ececed231f37493eff8b2cfcd1f5367b4c9d19f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4a1e4f462678b5d9b8203dda15942f00c8b455cc46cac746768ce1775b7685d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6afb13fb48ae12d16b2ee637bba4f9862bfba94103baac33121cb1dd9de7ca40(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31653d75bda1e67648da809c475666b4662690eac069f72c216967665025acfb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fbd62953a7feb8649095e0e924d3a8a64834cc4b9401c65a72be320bd381015(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ac017e8e1f23e9c6b921919ab9f7437c3456a05eb1f82d2e2d83fcb902faf38(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    data_exchange_id: builtins.str,
    display_name: builtins.str,
    location: builtins.str,
    description: typing.Optional[builtins.str] = None,
    documentation: typing.Optional[builtins.str] = None,
    icon: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    primary_contact: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    sharing_environment_config: typing.Optional[typing.Union[GoogleBigqueryAnalyticsHubDataExchangeSharingEnvironmentConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleBigqueryAnalyticsHubDataExchangeTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f970623f9fb96ef44281b1a0773d6f10a9c33c469f82a6386ae850c58dfe336(
    *,
    dcr_exchange_config: typing.Optional[typing.Union[GoogleBigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDcrExchangeConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    default_exchange_config: typing.Optional[typing.Union[GoogleBigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDefaultExchangeConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b69c9052e8821bb7a732ceb50bd5f2591f744e12ab3a2f8d90bca2b77ad9eb3c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e276cc3a34453763a0608ae16d271c523193c8dd38b15e7b81f2e22d33691bb(
    value: typing.Optional[GoogleBigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDcrExchangeConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f9814cb9330606a618087fd6fd1d6bcf62286c992be4eef7fdd2a1436a8f733(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5226585d1a50145ffc8ec926f8cfec82d41ad60c776280ca800eb5fb9ef21322(
    value: typing.Optional[GoogleBigqueryAnalyticsHubDataExchangeSharingEnvironmentConfigDefaultExchangeConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b51d8824cd9742fab168f0f16b34f9d591fb2f9cf37fa0ba20b2eab936a53ed(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3471890bb66c08bd05f73479ba53ae5003727d59ae1b414b6ff4cea9e5364979(
    value: typing.Optional[GoogleBigqueryAnalyticsHubDataExchangeSharingEnvironmentConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__572e6a9240353476dd275b25a312d6cc182f47d52a5c45d23846daf41bd1cefb(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e0c694b9fef2befeea34cf119deefadb843ac0aa5f98b38492f199ff24bb24e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f352ecfd69b92e37461b040ceddadcdcdf3235db564f30abc2259fa1b3553f5c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__334a28c884bfb363effaecda06466d0dca61eb73d8152ab602b8c807179f39bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa9c713e6e668a712c4e83742cd9928ec4a18569cd3dcffc97109c4e3d725088(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b932188a07d364bf2cd6e57f7d0c7d95b3ec28f6436f8c49e65aa420ec8477d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBigqueryAnalyticsHubDataExchangeTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
