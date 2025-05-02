r'''
# `aws_rum_app_monitor`

Refer to the Terraform Registry for docs: [`aws_rum_app_monitor`](https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rum_app_monitor).
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


class RumAppMonitor(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.rumAppMonitor.RumAppMonitor",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rum_app_monitor aws_rum_app_monitor}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        domain: builtins.str,
        name: builtins.str,
        app_monitor_configuration: typing.Optional[typing.Union["RumAppMonitorAppMonitorConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        custom_events: typing.Optional[typing.Union["RumAppMonitorCustomEvents", typing.Dict[builtins.str, typing.Any]]] = None,
        cw_log_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rum_app_monitor aws_rum_app_monitor} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param domain: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rum_app_monitor#domain RumAppMonitor#domain}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rum_app_monitor#name RumAppMonitor#name}.
        :param app_monitor_configuration: app_monitor_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rum_app_monitor#app_monitor_configuration RumAppMonitor#app_monitor_configuration}
        :param custom_events: custom_events block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rum_app_monitor#custom_events RumAppMonitor#custom_events}
        :param cw_log_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rum_app_monitor#cw_log_enabled RumAppMonitor#cw_log_enabled}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rum_app_monitor#id RumAppMonitor#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rum_app_monitor#tags RumAppMonitor#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rum_app_monitor#tags_all RumAppMonitor#tags_all}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d59c2e452c215acfbbe069715a91006795dcc379d9af92f837b51874cf097f09)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = RumAppMonitorConfig(
            domain=domain,
            name=name,
            app_monitor_configuration=app_monitor_configuration,
            custom_events=custom_events,
            cw_log_enabled=cw_log_enabled,
            id=id,
            tags=tags,
            tags_all=tags_all,
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
        '''Generates CDKTF code for importing a RumAppMonitor resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the RumAppMonitor to import.
        :param import_from_id: The id of the existing RumAppMonitor that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rum_app_monitor#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the RumAppMonitor to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33f2de8091faaace377edd17c46c89fb86369fb96cdc0ea6d2c322c40a1c7836)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAppMonitorConfiguration")
    def put_app_monitor_configuration(
        self,
        *,
        allow_cookies: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_xray: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        excluded_pages: typing.Optional[typing.Sequence[builtins.str]] = None,
        favorite_pages: typing.Optional[typing.Sequence[builtins.str]] = None,
        guest_role_arn: typing.Optional[builtins.str] = None,
        identity_pool_id: typing.Optional[builtins.str] = None,
        included_pages: typing.Optional[typing.Sequence[builtins.str]] = None,
        session_sample_rate: typing.Optional[jsii.Number] = None,
        telemetries: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param allow_cookies: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rum_app_monitor#allow_cookies RumAppMonitor#allow_cookies}.
        :param enable_xray: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rum_app_monitor#enable_xray RumAppMonitor#enable_xray}.
        :param excluded_pages: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rum_app_monitor#excluded_pages RumAppMonitor#excluded_pages}.
        :param favorite_pages: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rum_app_monitor#favorite_pages RumAppMonitor#favorite_pages}.
        :param guest_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rum_app_monitor#guest_role_arn RumAppMonitor#guest_role_arn}.
        :param identity_pool_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rum_app_monitor#identity_pool_id RumAppMonitor#identity_pool_id}.
        :param included_pages: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rum_app_monitor#included_pages RumAppMonitor#included_pages}.
        :param session_sample_rate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rum_app_monitor#session_sample_rate RumAppMonitor#session_sample_rate}.
        :param telemetries: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rum_app_monitor#telemetries RumAppMonitor#telemetries}.
        '''
        value = RumAppMonitorAppMonitorConfiguration(
            allow_cookies=allow_cookies,
            enable_xray=enable_xray,
            excluded_pages=excluded_pages,
            favorite_pages=favorite_pages,
            guest_role_arn=guest_role_arn,
            identity_pool_id=identity_pool_id,
            included_pages=included_pages,
            session_sample_rate=session_sample_rate,
            telemetries=telemetries,
        )

        return typing.cast(None, jsii.invoke(self, "putAppMonitorConfiguration", [value]))

    @jsii.member(jsii_name="putCustomEvents")
    def put_custom_events(
        self,
        *,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rum_app_monitor#status RumAppMonitor#status}.
        '''
        value = RumAppMonitorCustomEvents(status=status)

        return typing.cast(None, jsii.invoke(self, "putCustomEvents", [value]))

    @jsii.member(jsii_name="resetAppMonitorConfiguration")
    def reset_app_monitor_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppMonitorConfiguration", []))

    @jsii.member(jsii_name="resetCustomEvents")
    def reset_custom_events(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomEvents", []))

    @jsii.member(jsii_name="resetCwLogEnabled")
    def reset_cw_log_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCwLogEnabled", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

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
    @jsii.member(jsii_name="appMonitorConfiguration")
    def app_monitor_configuration(
        self,
    ) -> "RumAppMonitorAppMonitorConfigurationOutputReference":
        return typing.cast("RumAppMonitorAppMonitorConfigurationOutputReference", jsii.get(self, "appMonitorConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="appMonitorId")
    def app_monitor_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appMonitorId"))

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="customEvents")
    def custom_events(self) -> "RumAppMonitorCustomEventsOutputReference":
        return typing.cast("RumAppMonitorCustomEventsOutputReference", jsii.get(self, "customEvents"))

    @builtins.property
    @jsii.member(jsii_name="cwLogGroup")
    def cw_log_group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cwLogGroup"))

    @builtins.property
    @jsii.member(jsii_name="appMonitorConfigurationInput")
    def app_monitor_configuration_input(
        self,
    ) -> typing.Optional["RumAppMonitorAppMonitorConfiguration"]:
        return typing.cast(typing.Optional["RumAppMonitorAppMonitorConfiguration"], jsii.get(self, "appMonitorConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="customEventsInput")
    def custom_events_input(self) -> typing.Optional["RumAppMonitorCustomEvents"]:
        return typing.cast(typing.Optional["RumAppMonitorCustomEvents"], jsii.get(self, "customEventsInput"))

    @builtins.property
    @jsii.member(jsii_name="cwLogEnabledInput")
    def cw_log_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "cwLogEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="domainInput")
    def domain_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsAllInput")
    def tags_all_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsAllInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="cwLogEnabled")
    def cw_log_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "cwLogEnabled"))

    @cw_log_enabled.setter
    def cw_log_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec51281684b3716485266e414d737f410d52bdfaae4c8199977ff9da475db0f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cwLogEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="domain")
    def domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domain"))

    @domain.setter
    def domain(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92a60fad111a2479f59ee764a8e96593f6d39ea1b187c6a931e31475fada0bac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domain", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85fdb582b33f3852008f584dd9ba692c810e2827512173d0a619047da4dc1970)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66733ac4bddbb5f292dff16288dd0ae28fa09ce255731be54ffcb1bdbc870d62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a286c315c66167309deaf36a66fd8bf1977f86c2b254fc48be23516a04e859d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7570cc6a005af6d8a16bc9b4644966e38888c7a572251b1509155d1eb5293ec6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.rumAppMonitor.RumAppMonitorAppMonitorConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "allow_cookies": "allowCookies",
        "enable_xray": "enableXray",
        "excluded_pages": "excludedPages",
        "favorite_pages": "favoritePages",
        "guest_role_arn": "guestRoleArn",
        "identity_pool_id": "identityPoolId",
        "included_pages": "includedPages",
        "session_sample_rate": "sessionSampleRate",
        "telemetries": "telemetries",
    },
)
class RumAppMonitorAppMonitorConfiguration:
    def __init__(
        self,
        *,
        allow_cookies: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_xray: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        excluded_pages: typing.Optional[typing.Sequence[builtins.str]] = None,
        favorite_pages: typing.Optional[typing.Sequence[builtins.str]] = None,
        guest_role_arn: typing.Optional[builtins.str] = None,
        identity_pool_id: typing.Optional[builtins.str] = None,
        included_pages: typing.Optional[typing.Sequence[builtins.str]] = None,
        session_sample_rate: typing.Optional[jsii.Number] = None,
        telemetries: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param allow_cookies: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rum_app_monitor#allow_cookies RumAppMonitor#allow_cookies}.
        :param enable_xray: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rum_app_monitor#enable_xray RumAppMonitor#enable_xray}.
        :param excluded_pages: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rum_app_monitor#excluded_pages RumAppMonitor#excluded_pages}.
        :param favorite_pages: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rum_app_monitor#favorite_pages RumAppMonitor#favorite_pages}.
        :param guest_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rum_app_monitor#guest_role_arn RumAppMonitor#guest_role_arn}.
        :param identity_pool_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rum_app_monitor#identity_pool_id RumAppMonitor#identity_pool_id}.
        :param included_pages: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rum_app_monitor#included_pages RumAppMonitor#included_pages}.
        :param session_sample_rate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rum_app_monitor#session_sample_rate RumAppMonitor#session_sample_rate}.
        :param telemetries: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rum_app_monitor#telemetries RumAppMonitor#telemetries}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e27f690b60cdc243637713cadde49b3a99799b34e3dd870142d2c19f36cf7101)
            check_type(argname="argument allow_cookies", value=allow_cookies, expected_type=type_hints["allow_cookies"])
            check_type(argname="argument enable_xray", value=enable_xray, expected_type=type_hints["enable_xray"])
            check_type(argname="argument excluded_pages", value=excluded_pages, expected_type=type_hints["excluded_pages"])
            check_type(argname="argument favorite_pages", value=favorite_pages, expected_type=type_hints["favorite_pages"])
            check_type(argname="argument guest_role_arn", value=guest_role_arn, expected_type=type_hints["guest_role_arn"])
            check_type(argname="argument identity_pool_id", value=identity_pool_id, expected_type=type_hints["identity_pool_id"])
            check_type(argname="argument included_pages", value=included_pages, expected_type=type_hints["included_pages"])
            check_type(argname="argument session_sample_rate", value=session_sample_rate, expected_type=type_hints["session_sample_rate"])
            check_type(argname="argument telemetries", value=telemetries, expected_type=type_hints["telemetries"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allow_cookies is not None:
            self._values["allow_cookies"] = allow_cookies
        if enable_xray is not None:
            self._values["enable_xray"] = enable_xray
        if excluded_pages is not None:
            self._values["excluded_pages"] = excluded_pages
        if favorite_pages is not None:
            self._values["favorite_pages"] = favorite_pages
        if guest_role_arn is not None:
            self._values["guest_role_arn"] = guest_role_arn
        if identity_pool_id is not None:
            self._values["identity_pool_id"] = identity_pool_id
        if included_pages is not None:
            self._values["included_pages"] = included_pages
        if session_sample_rate is not None:
            self._values["session_sample_rate"] = session_sample_rate
        if telemetries is not None:
            self._values["telemetries"] = telemetries

    @builtins.property
    def allow_cookies(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rum_app_monitor#allow_cookies RumAppMonitor#allow_cookies}.'''
        result = self._values.get("allow_cookies")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_xray(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rum_app_monitor#enable_xray RumAppMonitor#enable_xray}.'''
        result = self._values.get("enable_xray")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def excluded_pages(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rum_app_monitor#excluded_pages RumAppMonitor#excluded_pages}.'''
        result = self._values.get("excluded_pages")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def favorite_pages(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rum_app_monitor#favorite_pages RumAppMonitor#favorite_pages}.'''
        result = self._values.get("favorite_pages")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def guest_role_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rum_app_monitor#guest_role_arn RumAppMonitor#guest_role_arn}.'''
        result = self._values.get("guest_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity_pool_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rum_app_monitor#identity_pool_id RumAppMonitor#identity_pool_id}.'''
        result = self._values.get("identity_pool_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def included_pages(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rum_app_monitor#included_pages RumAppMonitor#included_pages}.'''
        result = self._values.get("included_pages")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def session_sample_rate(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rum_app_monitor#session_sample_rate RumAppMonitor#session_sample_rate}.'''
        result = self._values.get("session_sample_rate")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def telemetries(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rum_app_monitor#telemetries RumAppMonitor#telemetries}.'''
        result = self._values.get("telemetries")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RumAppMonitorAppMonitorConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RumAppMonitorAppMonitorConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.rumAppMonitor.RumAppMonitorAppMonitorConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb0deef4ead698ed59cc11d60f8731a95dd39d9f5a0c2bd08ed506adbdb62694)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAllowCookies")
    def reset_allow_cookies(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowCookies", []))

    @jsii.member(jsii_name="resetEnableXray")
    def reset_enable_xray(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableXray", []))

    @jsii.member(jsii_name="resetExcludedPages")
    def reset_excluded_pages(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludedPages", []))

    @jsii.member(jsii_name="resetFavoritePages")
    def reset_favorite_pages(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFavoritePages", []))

    @jsii.member(jsii_name="resetGuestRoleArn")
    def reset_guest_role_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGuestRoleArn", []))

    @jsii.member(jsii_name="resetIdentityPoolId")
    def reset_identity_pool_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentityPoolId", []))

    @jsii.member(jsii_name="resetIncludedPages")
    def reset_included_pages(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludedPages", []))

    @jsii.member(jsii_name="resetSessionSampleRate")
    def reset_session_sample_rate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSessionSampleRate", []))

    @jsii.member(jsii_name="resetTelemetries")
    def reset_telemetries(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTelemetries", []))

    @builtins.property
    @jsii.member(jsii_name="allowCookiesInput")
    def allow_cookies_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowCookiesInput"))

    @builtins.property
    @jsii.member(jsii_name="enableXrayInput")
    def enable_xray_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableXrayInput"))

    @builtins.property
    @jsii.member(jsii_name="excludedPagesInput")
    def excluded_pages_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "excludedPagesInput"))

    @builtins.property
    @jsii.member(jsii_name="favoritePagesInput")
    def favorite_pages_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "favoritePagesInput"))

    @builtins.property
    @jsii.member(jsii_name="guestRoleArnInput")
    def guest_role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "guestRoleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="identityPoolIdInput")
    def identity_pool_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "identityPoolIdInput"))

    @builtins.property
    @jsii.member(jsii_name="includedPagesInput")
    def included_pages_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "includedPagesInput"))

    @builtins.property
    @jsii.member(jsii_name="sessionSampleRateInput")
    def session_sample_rate_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sessionSampleRateInput"))

    @builtins.property
    @jsii.member(jsii_name="telemetriesInput")
    def telemetries_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "telemetriesInput"))

    @builtins.property
    @jsii.member(jsii_name="allowCookies")
    def allow_cookies(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowCookies"))

    @allow_cookies.setter
    def allow_cookies(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3867ccb793592c097fc6aed768ba8435663e9f5f5021ba7bfb77c4f3b75c6768)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowCookies", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableXray")
    def enable_xray(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableXray"))

    @enable_xray.setter
    def enable_xray(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac8a8c6bde1641c2a9d516bbec3985f58024d2d395da7f221c864dc4f0ecbc86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableXray", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="excludedPages")
    def excluded_pages(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludedPages"))

    @excluded_pages.setter
    def excluded_pages(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a2261cf0a690938a9701d3765577df8a0728ed3037cbfedb5f1f6dc9694cd5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludedPages", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="favoritePages")
    def favorite_pages(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "favoritePages"))

    @favorite_pages.setter
    def favorite_pages(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__800ce2cb0c800b491c2942fb0da2c7f71e55ae52ff5313f00672635a7a8e96ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "favoritePages", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="guestRoleArn")
    def guest_role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "guestRoleArn"))

    @guest_role_arn.setter
    def guest_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe1c416f0018240dca1875ae43bbfbbce0ee7d406a4a5fb10ba8a05ffc730cbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "guestRoleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="identityPoolId")
    def identity_pool_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identityPoolId"))

    @identity_pool_id.setter
    def identity_pool_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1e5e18e3a66e9ecded0128257f398d40aa301891d1dce932614c3221c5ef1d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityPoolId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includedPages")
    def included_pages(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "includedPages"))

    @included_pages.setter
    def included_pages(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a0053cbdb92c0f6042ac536cb0710172031038436a15eb2a20fabedd2181cc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includedPages", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sessionSampleRate")
    def session_sample_rate(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sessionSampleRate"))

    @session_sample_rate.setter
    def session_sample_rate(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39e1e0b8f6e848fcfe8e12ff5a62a3e3d17556a3ad55194ab517da1a1ce44b82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sessionSampleRate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="telemetries")
    def telemetries(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "telemetries"))

    @telemetries.setter
    def telemetries(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dc625fcfa0f305c801c725c5c82e73a273b2846d21895018de63d441b81a545)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "telemetries", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RumAppMonitorAppMonitorConfiguration]:
        return typing.cast(typing.Optional[RumAppMonitorAppMonitorConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RumAppMonitorAppMonitorConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f51c68ae67a12cdd9cd887896ac707f723a0845f52550bf631279adc0e47519d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.rumAppMonitor.RumAppMonitorConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "domain": "domain",
        "name": "name",
        "app_monitor_configuration": "appMonitorConfiguration",
        "custom_events": "customEvents",
        "cw_log_enabled": "cwLogEnabled",
        "id": "id",
        "tags": "tags",
        "tags_all": "tagsAll",
    },
)
class RumAppMonitorConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        domain: builtins.str,
        name: builtins.str,
        app_monitor_configuration: typing.Optional[typing.Union[RumAppMonitorAppMonitorConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
        custom_events: typing.Optional[typing.Union["RumAppMonitorCustomEvents", typing.Dict[builtins.str, typing.Any]]] = None,
        cw_log_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param domain: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rum_app_monitor#domain RumAppMonitor#domain}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rum_app_monitor#name RumAppMonitor#name}.
        :param app_monitor_configuration: app_monitor_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rum_app_monitor#app_monitor_configuration RumAppMonitor#app_monitor_configuration}
        :param custom_events: custom_events block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rum_app_monitor#custom_events RumAppMonitor#custom_events}
        :param cw_log_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rum_app_monitor#cw_log_enabled RumAppMonitor#cw_log_enabled}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rum_app_monitor#id RumAppMonitor#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rum_app_monitor#tags RumAppMonitor#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rum_app_monitor#tags_all RumAppMonitor#tags_all}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(app_monitor_configuration, dict):
            app_monitor_configuration = RumAppMonitorAppMonitorConfiguration(**app_monitor_configuration)
        if isinstance(custom_events, dict):
            custom_events = RumAppMonitorCustomEvents(**custom_events)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__291d869b291c352aa78ad785d26ab344df75e4dc66c4e32c29411d4ad3c5fd2d)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument app_monitor_configuration", value=app_monitor_configuration, expected_type=type_hints["app_monitor_configuration"])
            check_type(argname="argument custom_events", value=custom_events, expected_type=type_hints["custom_events"])
            check_type(argname="argument cw_log_enabled", value=cw_log_enabled, expected_type=type_hints["cw_log_enabled"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "domain": domain,
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
        if app_monitor_configuration is not None:
            self._values["app_monitor_configuration"] = app_monitor_configuration
        if custom_events is not None:
            self._values["custom_events"] = custom_events
        if cw_log_enabled is not None:
            self._values["cw_log_enabled"] = cw_log_enabled
        if id is not None:
            self._values["id"] = id
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all

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
    def domain(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rum_app_monitor#domain RumAppMonitor#domain}.'''
        result = self._values.get("domain")
        assert result is not None, "Required property 'domain' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rum_app_monitor#name RumAppMonitor#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def app_monitor_configuration(
        self,
    ) -> typing.Optional[RumAppMonitorAppMonitorConfiguration]:
        '''app_monitor_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rum_app_monitor#app_monitor_configuration RumAppMonitor#app_monitor_configuration}
        '''
        result = self._values.get("app_monitor_configuration")
        return typing.cast(typing.Optional[RumAppMonitorAppMonitorConfiguration], result)

    @builtins.property
    def custom_events(self) -> typing.Optional["RumAppMonitorCustomEvents"]:
        '''custom_events block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rum_app_monitor#custom_events RumAppMonitor#custom_events}
        '''
        result = self._values.get("custom_events")
        return typing.cast(typing.Optional["RumAppMonitorCustomEvents"], result)

    @builtins.property
    def cw_log_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rum_app_monitor#cw_log_enabled RumAppMonitor#cw_log_enabled}.'''
        result = self._values.get("cw_log_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rum_app_monitor#id RumAppMonitor#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rum_app_monitor#tags RumAppMonitor#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rum_app_monitor#tags_all RumAppMonitor#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RumAppMonitorConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.rumAppMonitor.RumAppMonitorCustomEvents",
    jsii_struct_bases=[],
    name_mapping={"status": "status"},
)
class RumAppMonitorCustomEvents:
    def __init__(self, *, status: typing.Optional[builtins.str] = None) -> None:
        '''
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rum_app_monitor#status RumAppMonitor#status}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1e68cf65233c06ed8b734422ee703c9f939d05dad2b412ae4dbbf6c1cda7514)
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if status is not None:
            self._values["status"] = status

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rum_app_monitor#status RumAppMonitor#status}.'''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RumAppMonitorCustomEvents(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RumAppMonitorCustomEventsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.rumAppMonitor.RumAppMonitorCustomEventsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d3f326c71d735f0daca26fe957041bbfc2ac9c85332cef75818beb5d1d15322)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetStatus")
    def reset_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatus", []))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9b90e4a0d136381704b6a12df1685dca525d9596023b21d10d442a4e48b7d3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RumAppMonitorCustomEvents]:
        return typing.cast(typing.Optional[RumAppMonitorCustomEvents], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[RumAppMonitorCustomEvents]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20df5237bc634e34e521e81d9ab6f00124d6ded2b410dcf1975b92234571b6d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "RumAppMonitor",
    "RumAppMonitorAppMonitorConfiguration",
    "RumAppMonitorAppMonitorConfigurationOutputReference",
    "RumAppMonitorConfig",
    "RumAppMonitorCustomEvents",
    "RumAppMonitorCustomEventsOutputReference",
]

publication.publish()

def _typecheckingstub__d59c2e452c215acfbbe069715a91006795dcc379d9af92f837b51874cf097f09(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    domain: builtins.str,
    name: builtins.str,
    app_monitor_configuration: typing.Optional[typing.Union[RumAppMonitorAppMonitorConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    custom_events: typing.Optional[typing.Union[RumAppMonitorCustomEvents, typing.Dict[builtins.str, typing.Any]]] = None,
    cw_log_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
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

def _typecheckingstub__33f2de8091faaace377edd17c46c89fb86369fb96cdc0ea6d2c322c40a1c7836(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec51281684b3716485266e414d737f410d52bdfaae4c8199977ff9da475db0f8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92a60fad111a2479f59ee764a8e96593f6d39ea1b187c6a931e31475fada0bac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85fdb582b33f3852008f584dd9ba692c810e2827512173d0a619047da4dc1970(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66733ac4bddbb5f292dff16288dd0ae28fa09ce255731be54ffcb1bdbc870d62(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a286c315c66167309deaf36a66fd8bf1977f86c2b254fc48be23516a04e859d7(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7570cc6a005af6d8a16bc9b4644966e38888c7a572251b1509155d1eb5293ec6(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e27f690b60cdc243637713cadde49b3a99799b34e3dd870142d2c19f36cf7101(
    *,
    allow_cookies: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_xray: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    excluded_pages: typing.Optional[typing.Sequence[builtins.str]] = None,
    favorite_pages: typing.Optional[typing.Sequence[builtins.str]] = None,
    guest_role_arn: typing.Optional[builtins.str] = None,
    identity_pool_id: typing.Optional[builtins.str] = None,
    included_pages: typing.Optional[typing.Sequence[builtins.str]] = None,
    session_sample_rate: typing.Optional[jsii.Number] = None,
    telemetries: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb0deef4ead698ed59cc11d60f8731a95dd39d9f5a0c2bd08ed506adbdb62694(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3867ccb793592c097fc6aed768ba8435663e9f5f5021ba7bfb77c4f3b75c6768(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac8a8c6bde1641c2a9d516bbec3985f58024d2d395da7f221c864dc4f0ecbc86(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a2261cf0a690938a9701d3765577df8a0728ed3037cbfedb5f1f6dc9694cd5d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__800ce2cb0c800b491c2942fb0da2c7f71e55ae52ff5313f00672635a7a8e96ce(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe1c416f0018240dca1875ae43bbfbbce0ee7d406a4a5fb10ba8a05ffc730cbc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1e5e18e3a66e9ecded0128257f398d40aa301891d1dce932614c3221c5ef1d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a0053cbdb92c0f6042ac536cb0710172031038436a15eb2a20fabedd2181cc0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39e1e0b8f6e848fcfe8e12ff5a62a3e3d17556a3ad55194ab517da1a1ce44b82(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dc625fcfa0f305c801c725c5c82e73a273b2846d21895018de63d441b81a545(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f51c68ae67a12cdd9cd887896ac707f723a0845f52550bf631279adc0e47519d(
    value: typing.Optional[RumAppMonitorAppMonitorConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__291d869b291c352aa78ad785d26ab344df75e4dc66c4e32c29411d4ad3c5fd2d(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    domain: builtins.str,
    name: builtins.str,
    app_monitor_configuration: typing.Optional[typing.Union[RumAppMonitorAppMonitorConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    custom_events: typing.Optional[typing.Union[RumAppMonitorCustomEvents, typing.Dict[builtins.str, typing.Any]]] = None,
    cw_log_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1e68cf65233c06ed8b734422ee703c9f939d05dad2b412ae4dbbf6c1cda7514(
    *,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d3f326c71d735f0daca26fe957041bbfc2ac9c85332cef75818beb5d1d15322(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9b90e4a0d136381704b6a12df1685dca525d9596023b21d10d442a4e48b7d3c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20df5237bc634e34e521e81d9ab6f00124d6ded2b410dcf1975b92234571b6d8(
    value: typing.Optional[RumAppMonitorCustomEvents],
) -> None:
    """Type checking stubs"""
    pass
