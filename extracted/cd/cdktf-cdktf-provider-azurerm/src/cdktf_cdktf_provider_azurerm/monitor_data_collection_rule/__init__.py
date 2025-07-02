r'''
# `azurerm_monitor_data_collection_rule`

Refer to the Terraform Registry for docs: [`azurerm_monitor_data_collection_rule`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule).
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


class MonitorDataCollectionRule(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRule",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule azurerm_monitor_data_collection_rule}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        data_flow: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorDataCollectionRuleDataFlow", typing.Dict[builtins.str, typing.Any]]]],
        destinations: typing.Union["MonitorDataCollectionRuleDestinations", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        data_collection_endpoint_id: typing.Optional[builtins.str] = None,
        data_sources: typing.Optional[typing.Union["MonitorDataCollectionRuleDataSources", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        identity: typing.Optional[typing.Union["MonitorDataCollectionRuleIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        kind: typing.Optional[builtins.str] = None,
        stream_declaration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorDataCollectionRuleStreamDeclaration", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["MonitorDataCollectionRuleTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule azurerm_monitor_data_collection_rule} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param data_flow: data_flow block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#data_flow MonitorDataCollectionRule#data_flow}
        :param destinations: destinations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#destinations MonitorDataCollectionRule#destinations}
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#location MonitorDataCollectionRule#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#name MonitorDataCollectionRule#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#resource_group_name MonitorDataCollectionRule#resource_group_name}.
        :param data_collection_endpoint_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#data_collection_endpoint_id MonitorDataCollectionRule#data_collection_endpoint_id}.
        :param data_sources: data_sources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#data_sources MonitorDataCollectionRule#data_sources}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#description MonitorDataCollectionRule#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#id MonitorDataCollectionRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity: identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#identity MonitorDataCollectionRule#identity}
        :param kind: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#kind MonitorDataCollectionRule#kind}.
        :param stream_declaration: stream_declaration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#stream_declaration MonitorDataCollectionRule#stream_declaration}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#tags MonitorDataCollectionRule#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#timeouts MonitorDataCollectionRule#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7453666e1a553395226393741cd1fa7f278ea729f9b208c8d82957365dd73fe)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = MonitorDataCollectionRuleConfig(
            data_flow=data_flow,
            destinations=destinations,
            location=location,
            name=name,
            resource_group_name=resource_group_name,
            data_collection_endpoint_id=data_collection_endpoint_id,
            data_sources=data_sources,
            description=description,
            id=id,
            identity=identity,
            kind=kind,
            stream_declaration=stream_declaration,
            tags=tags,
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
        '''Generates CDKTF code for importing a MonitorDataCollectionRule resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the MonitorDataCollectionRule to import.
        :param import_from_id: The id of the existing MonitorDataCollectionRule that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the MonitorDataCollectionRule to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dba47b1b6c42de36e6ae9966095eb212675ea24a244b1496da0d3b486acc7891)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDataFlow")
    def put_data_flow(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorDataCollectionRuleDataFlow", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e11e8053e4d4689ad66e11c5b3b4857dd939bf1bc46f7fd9a24c4a7ce5e81a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDataFlow", [value]))

    @jsii.member(jsii_name="putDataSources")
    def put_data_sources(
        self,
        *,
        data_import: typing.Optional[typing.Union["MonitorDataCollectionRuleDataSourcesDataImport", typing.Dict[builtins.str, typing.Any]]] = None,
        extension: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorDataCollectionRuleDataSourcesExtension", typing.Dict[builtins.str, typing.Any]]]]] = None,
        iis_log: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorDataCollectionRuleDataSourcesIisLog", typing.Dict[builtins.str, typing.Any]]]]] = None,
        log_file: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorDataCollectionRuleDataSourcesLogFile", typing.Dict[builtins.str, typing.Any]]]]] = None,
        performance_counter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorDataCollectionRuleDataSourcesPerformanceCounter", typing.Dict[builtins.str, typing.Any]]]]] = None,
        platform_telemetry: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorDataCollectionRuleDataSourcesPlatformTelemetry", typing.Dict[builtins.str, typing.Any]]]]] = None,
        prometheus_forwarder: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorDataCollectionRuleDataSourcesPrometheusForwarder", typing.Dict[builtins.str, typing.Any]]]]] = None,
        syslog: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorDataCollectionRuleDataSourcesSyslog", typing.Dict[builtins.str, typing.Any]]]]] = None,
        windows_event_log: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorDataCollectionRuleDataSourcesWindowsEventLog", typing.Dict[builtins.str, typing.Any]]]]] = None,
        windows_firewall_log: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorDataCollectionRuleDataSourcesWindowsFirewallLog", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param data_import: data_import block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#data_import MonitorDataCollectionRule#data_import}
        :param extension: extension block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#extension MonitorDataCollectionRule#extension}
        :param iis_log: iis_log block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#iis_log MonitorDataCollectionRule#iis_log}
        :param log_file: log_file block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#log_file MonitorDataCollectionRule#log_file}
        :param performance_counter: performance_counter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#performance_counter MonitorDataCollectionRule#performance_counter}
        :param platform_telemetry: platform_telemetry block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#platform_telemetry MonitorDataCollectionRule#platform_telemetry}
        :param prometheus_forwarder: prometheus_forwarder block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#prometheus_forwarder MonitorDataCollectionRule#prometheus_forwarder}
        :param syslog: syslog block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#syslog MonitorDataCollectionRule#syslog}
        :param windows_event_log: windows_event_log block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#windows_event_log MonitorDataCollectionRule#windows_event_log}
        :param windows_firewall_log: windows_firewall_log block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#windows_firewall_log MonitorDataCollectionRule#windows_firewall_log}
        '''
        value = MonitorDataCollectionRuleDataSources(
            data_import=data_import,
            extension=extension,
            iis_log=iis_log,
            log_file=log_file,
            performance_counter=performance_counter,
            platform_telemetry=platform_telemetry,
            prometheus_forwarder=prometheus_forwarder,
            syslog=syslog,
            windows_event_log=windows_event_log,
            windows_firewall_log=windows_firewall_log,
        )

        return typing.cast(None, jsii.invoke(self, "putDataSources", [value]))

    @jsii.member(jsii_name="putDestinations")
    def put_destinations(
        self,
        *,
        azure_monitor_metrics: typing.Optional[typing.Union["MonitorDataCollectionRuleDestinationsAzureMonitorMetrics", typing.Dict[builtins.str, typing.Any]]] = None,
        event_hub: typing.Optional[typing.Union["MonitorDataCollectionRuleDestinationsEventHub", typing.Dict[builtins.str, typing.Any]]] = None,
        event_hub_direct: typing.Optional[typing.Union["MonitorDataCollectionRuleDestinationsEventHubDirect", typing.Dict[builtins.str, typing.Any]]] = None,
        log_analytics: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorDataCollectionRuleDestinationsLogAnalytics", typing.Dict[builtins.str, typing.Any]]]]] = None,
        monitor_account: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorDataCollectionRuleDestinationsMonitorAccount", typing.Dict[builtins.str, typing.Any]]]]] = None,
        storage_blob: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorDataCollectionRuleDestinationsStorageBlob", typing.Dict[builtins.str, typing.Any]]]]] = None,
        storage_blob_direct: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorDataCollectionRuleDestinationsStorageBlobDirect", typing.Dict[builtins.str, typing.Any]]]]] = None,
        storage_table_direct: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorDataCollectionRuleDestinationsStorageTableDirect", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param azure_monitor_metrics: azure_monitor_metrics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#azure_monitor_metrics MonitorDataCollectionRule#azure_monitor_metrics}
        :param event_hub: event_hub block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#event_hub MonitorDataCollectionRule#event_hub}
        :param event_hub_direct: event_hub_direct block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#event_hub_direct MonitorDataCollectionRule#event_hub_direct}
        :param log_analytics: log_analytics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#log_analytics MonitorDataCollectionRule#log_analytics}
        :param monitor_account: monitor_account block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#monitor_account MonitorDataCollectionRule#monitor_account}
        :param storage_blob: storage_blob block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#storage_blob MonitorDataCollectionRule#storage_blob}
        :param storage_blob_direct: storage_blob_direct block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#storage_blob_direct MonitorDataCollectionRule#storage_blob_direct}
        :param storage_table_direct: storage_table_direct block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#storage_table_direct MonitorDataCollectionRule#storage_table_direct}
        '''
        value = MonitorDataCollectionRuleDestinations(
            azure_monitor_metrics=azure_monitor_metrics,
            event_hub=event_hub,
            event_hub_direct=event_hub_direct,
            log_analytics=log_analytics,
            monitor_account=monitor_account,
            storage_blob=storage_blob,
            storage_blob_direct=storage_blob_direct,
            storage_table_direct=storage_table_direct,
        )

        return typing.cast(None, jsii.invoke(self, "putDestinations", [value]))

    @jsii.member(jsii_name="putIdentity")
    def put_identity(
        self,
        *,
        type: builtins.str,
        identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#type MonitorDataCollectionRule#type}.
        :param identity_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#identity_ids MonitorDataCollectionRule#identity_ids}.
        '''
        value = MonitorDataCollectionRuleIdentity(type=type, identity_ids=identity_ids)

        return typing.cast(None, jsii.invoke(self, "putIdentity", [value]))

    @jsii.member(jsii_name="putStreamDeclaration")
    def put_stream_declaration(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorDataCollectionRuleStreamDeclaration", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54f340e62d907c8b0daf07fe2fba7d441325e33f8ab4032cf24dfadad6e3c4df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putStreamDeclaration", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#create MonitorDataCollectionRule#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#delete MonitorDataCollectionRule#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#read MonitorDataCollectionRule#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#update MonitorDataCollectionRule#update}.
        '''
        value = MonitorDataCollectionRuleTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDataCollectionEndpointId")
    def reset_data_collection_endpoint_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataCollectionEndpointId", []))

    @jsii.member(jsii_name="resetDataSources")
    def reset_data_sources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataSources", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIdentity")
    def reset_identity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentity", []))

    @jsii.member(jsii_name="resetKind")
    def reset_kind(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKind", []))

    @jsii.member(jsii_name="resetStreamDeclaration")
    def reset_stream_declaration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStreamDeclaration", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

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
    @jsii.member(jsii_name="dataFlow")
    def data_flow(self) -> "MonitorDataCollectionRuleDataFlowList":
        return typing.cast("MonitorDataCollectionRuleDataFlowList", jsii.get(self, "dataFlow"))

    @builtins.property
    @jsii.member(jsii_name="dataSources")
    def data_sources(self) -> "MonitorDataCollectionRuleDataSourcesOutputReference":
        return typing.cast("MonitorDataCollectionRuleDataSourcesOutputReference", jsii.get(self, "dataSources"))

    @builtins.property
    @jsii.member(jsii_name="destinations")
    def destinations(self) -> "MonitorDataCollectionRuleDestinationsOutputReference":
        return typing.cast("MonitorDataCollectionRuleDestinationsOutputReference", jsii.get(self, "destinations"))

    @builtins.property
    @jsii.member(jsii_name="identity")
    def identity(self) -> "MonitorDataCollectionRuleIdentityOutputReference":
        return typing.cast("MonitorDataCollectionRuleIdentityOutputReference", jsii.get(self, "identity"))

    @builtins.property
    @jsii.member(jsii_name="immutableId")
    def immutable_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "immutableId"))

    @builtins.property
    @jsii.member(jsii_name="streamDeclaration")
    def stream_declaration(self) -> "MonitorDataCollectionRuleStreamDeclarationList":
        return typing.cast("MonitorDataCollectionRuleStreamDeclarationList", jsii.get(self, "streamDeclaration"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "MonitorDataCollectionRuleTimeoutsOutputReference":
        return typing.cast("MonitorDataCollectionRuleTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="dataCollectionEndpointIdInput")
    def data_collection_endpoint_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataCollectionEndpointIdInput"))

    @builtins.property
    @jsii.member(jsii_name="dataFlowInput")
    def data_flow_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDataFlow"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDataFlow"]]], jsii.get(self, "dataFlowInput"))

    @builtins.property
    @jsii.member(jsii_name="dataSourcesInput")
    def data_sources_input(
        self,
    ) -> typing.Optional["MonitorDataCollectionRuleDataSources"]:
        return typing.cast(typing.Optional["MonitorDataCollectionRuleDataSources"], jsii.get(self, "dataSourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationsInput")
    def destinations_input(
        self,
    ) -> typing.Optional["MonitorDataCollectionRuleDestinations"]:
        return typing.cast(typing.Optional["MonitorDataCollectionRuleDestinations"], jsii.get(self, "destinationsInput"))

    @builtins.property
    @jsii.member(jsii_name="identityInput")
    def identity_input(self) -> typing.Optional["MonitorDataCollectionRuleIdentity"]:
        return typing.cast(typing.Optional["MonitorDataCollectionRuleIdentity"], jsii.get(self, "identityInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="kindInput")
    def kind_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kindInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="streamDeclarationInput")
    def stream_declaration_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleStreamDeclaration"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleStreamDeclaration"]]], jsii.get(self, "streamDeclarationInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "MonitorDataCollectionRuleTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "MonitorDataCollectionRuleTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="dataCollectionEndpointId")
    def data_collection_endpoint_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataCollectionEndpointId"))

    @data_collection_endpoint_id.setter
    def data_collection_endpoint_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d30877cff5173239a7b0c8c7ef63144c135a702f3454101cd8bbc9bde00aeaef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataCollectionEndpointId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0a394bb8b6e37d91805fa59e4acaf2d079e0d607c424ce7ee9c94e1d8b7eef5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd1a633d39cc0d112f1c664f1c447859aab147a85e4c0b444cf173e02a713773)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kind")
    def kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kind"))

    @kind.setter
    def kind(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__275a728f2a5ab4f192ac57947b946bd499a44adaa22a59fed67db05e8add50df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kind", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b2ebce16a93e815816f1d44e9db356f927eeee9cbe385ce08fe43cd9deccb68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d38fb73cf03f998dbc2489f0dda204889060e754510687c2747824cfd3dbb408)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc5f01dbf2f883c2a932ccfd3de2a8ac4ae393089c4ea1d2dc518f89a95f885f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a015c242f541883e7d693f89c1e1d38d3a9ab49dd92619dbb1ce3d833530265b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "data_flow": "dataFlow",
        "destinations": "destinations",
        "location": "location",
        "name": "name",
        "resource_group_name": "resourceGroupName",
        "data_collection_endpoint_id": "dataCollectionEndpointId",
        "data_sources": "dataSources",
        "description": "description",
        "id": "id",
        "identity": "identity",
        "kind": "kind",
        "stream_declaration": "streamDeclaration",
        "tags": "tags",
        "timeouts": "timeouts",
    },
)
class MonitorDataCollectionRuleConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        data_flow: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorDataCollectionRuleDataFlow", typing.Dict[builtins.str, typing.Any]]]],
        destinations: typing.Union["MonitorDataCollectionRuleDestinations", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        data_collection_endpoint_id: typing.Optional[builtins.str] = None,
        data_sources: typing.Optional[typing.Union["MonitorDataCollectionRuleDataSources", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        identity: typing.Optional[typing.Union["MonitorDataCollectionRuleIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        kind: typing.Optional[builtins.str] = None,
        stream_declaration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorDataCollectionRuleStreamDeclaration", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["MonitorDataCollectionRuleTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param data_flow: data_flow block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#data_flow MonitorDataCollectionRule#data_flow}
        :param destinations: destinations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#destinations MonitorDataCollectionRule#destinations}
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#location MonitorDataCollectionRule#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#name MonitorDataCollectionRule#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#resource_group_name MonitorDataCollectionRule#resource_group_name}.
        :param data_collection_endpoint_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#data_collection_endpoint_id MonitorDataCollectionRule#data_collection_endpoint_id}.
        :param data_sources: data_sources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#data_sources MonitorDataCollectionRule#data_sources}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#description MonitorDataCollectionRule#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#id MonitorDataCollectionRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity: identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#identity MonitorDataCollectionRule#identity}
        :param kind: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#kind MonitorDataCollectionRule#kind}.
        :param stream_declaration: stream_declaration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#stream_declaration MonitorDataCollectionRule#stream_declaration}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#tags MonitorDataCollectionRule#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#timeouts MonitorDataCollectionRule#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(destinations, dict):
            destinations = MonitorDataCollectionRuleDestinations(**destinations)
        if isinstance(data_sources, dict):
            data_sources = MonitorDataCollectionRuleDataSources(**data_sources)
        if isinstance(identity, dict):
            identity = MonitorDataCollectionRuleIdentity(**identity)
        if isinstance(timeouts, dict):
            timeouts = MonitorDataCollectionRuleTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fa2466c780fe932563ee1fdec3e948f3932866f264f4758aa6e61dfaf01b721)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument data_flow", value=data_flow, expected_type=type_hints["data_flow"])
            check_type(argname="argument destinations", value=destinations, expected_type=type_hints["destinations"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument data_collection_endpoint_id", value=data_collection_endpoint_id, expected_type=type_hints["data_collection_endpoint_id"])
            check_type(argname="argument data_sources", value=data_sources, expected_type=type_hints["data_sources"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
            check_type(argname="argument kind", value=kind, expected_type=type_hints["kind"])
            check_type(argname="argument stream_declaration", value=stream_declaration, expected_type=type_hints["stream_declaration"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data_flow": data_flow,
            "destinations": destinations,
            "location": location,
            "name": name,
            "resource_group_name": resource_group_name,
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
        if data_collection_endpoint_id is not None:
            self._values["data_collection_endpoint_id"] = data_collection_endpoint_id
        if data_sources is not None:
            self._values["data_sources"] = data_sources
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if identity is not None:
            self._values["identity"] = identity
        if kind is not None:
            self._values["kind"] = kind
        if stream_declaration is not None:
            self._values["stream_declaration"] = stream_declaration
        if tags is not None:
            self._values["tags"] = tags
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
    def data_flow(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDataFlow"]]:
        '''data_flow block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#data_flow MonitorDataCollectionRule#data_flow}
        '''
        result = self._values.get("data_flow")
        assert result is not None, "Required property 'data_flow' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDataFlow"]], result)

    @builtins.property
    def destinations(self) -> "MonitorDataCollectionRuleDestinations":
        '''destinations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#destinations MonitorDataCollectionRule#destinations}
        '''
        result = self._values.get("destinations")
        assert result is not None, "Required property 'destinations' is missing"
        return typing.cast("MonitorDataCollectionRuleDestinations", result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#location MonitorDataCollectionRule#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#name MonitorDataCollectionRule#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#resource_group_name MonitorDataCollectionRule#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def data_collection_endpoint_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#data_collection_endpoint_id MonitorDataCollectionRule#data_collection_endpoint_id}.'''
        result = self._values.get("data_collection_endpoint_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_sources(self) -> typing.Optional["MonitorDataCollectionRuleDataSources"]:
        '''data_sources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#data_sources MonitorDataCollectionRule#data_sources}
        '''
        result = self._values.get("data_sources")
        return typing.cast(typing.Optional["MonitorDataCollectionRuleDataSources"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#description MonitorDataCollectionRule#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#id MonitorDataCollectionRule#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity(self) -> typing.Optional["MonitorDataCollectionRuleIdentity"]:
        '''identity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#identity MonitorDataCollectionRule#identity}
        '''
        result = self._values.get("identity")
        return typing.cast(typing.Optional["MonitorDataCollectionRuleIdentity"], result)

    @builtins.property
    def kind(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#kind MonitorDataCollectionRule#kind}.'''
        result = self._values.get("kind")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stream_declaration(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleStreamDeclaration"]]]:
        '''stream_declaration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#stream_declaration MonitorDataCollectionRule#stream_declaration}
        '''
        result = self._values.get("stream_declaration")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleStreamDeclaration"]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#tags MonitorDataCollectionRule#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["MonitorDataCollectionRuleTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#timeouts MonitorDataCollectionRule#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["MonitorDataCollectionRuleTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorDataCollectionRuleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDataFlow",
    jsii_struct_bases=[],
    name_mapping={
        "destinations": "destinations",
        "streams": "streams",
        "built_in_transform": "builtInTransform",
        "output_stream": "outputStream",
        "transform_kql": "transformKql",
    },
)
class MonitorDataCollectionRuleDataFlow:
    def __init__(
        self,
        *,
        destinations: typing.Sequence[builtins.str],
        streams: typing.Sequence[builtins.str],
        built_in_transform: typing.Optional[builtins.str] = None,
        output_stream: typing.Optional[builtins.str] = None,
        transform_kql: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param destinations: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#destinations MonitorDataCollectionRule#destinations}.
        :param streams: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#streams MonitorDataCollectionRule#streams}.
        :param built_in_transform: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#built_in_transform MonitorDataCollectionRule#built_in_transform}.
        :param output_stream: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#output_stream MonitorDataCollectionRule#output_stream}.
        :param transform_kql: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#transform_kql MonitorDataCollectionRule#transform_kql}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31534c94d7dd3dad441dc0a88e1e01b345b0d2771935ed98ae8cfa810007c1b8)
            check_type(argname="argument destinations", value=destinations, expected_type=type_hints["destinations"])
            check_type(argname="argument streams", value=streams, expected_type=type_hints["streams"])
            check_type(argname="argument built_in_transform", value=built_in_transform, expected_type=type_hints["built_in_transform"])
            check_type(argname="argument output_stream", value=output_stream, expected_type=type_hints["output_stream"])
            check_type(argname="argument transform_kql", value=transform_kql, expected_type=type_hints["transform_kql"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destinations": destinations,
            "streams": streams,
        }
        if built_in_transform is not None:
            self._values["built_in_transform"] = built_in_transform
        if output_stream is not None:
            self._values["output_stream"] = output_stream
        if transform_kql is not None:
            self._values["transform_kql"] = transform_kql

    @builtins.property
    def destinations(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#destinations MonitorDataCollectionRule#destinations}.'''
        result = self._values.get("destinations")
        assert result is not None, "Required property 'destinations' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def streams(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#streams MonitorDataCollectionRule#streams}.'''
        result = self._values.get("streams")
        assert result is not None, "Required property 'streams' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def built_in_transform(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#built_in_transform MonitorDataCollectionRule#built_in_transform}.'''
        result = self._values.get("built_in_transform")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def output_stream(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#output_stream MonitorDataCollectionRule#output_stream}.'''
        result = self._values.get("output_stream")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def transform_kql(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#transform_kql MonitorDataCollectionRule#transform_kql}.'''
        result = self._values.get("transform_kql")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorDataCollectionRuleDataFlow(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorDataCollectionRuleDataFlowList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDataFlowList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d3b7467ac66c79abb788f4f177613cc038be6bd3bef457292cad4d50c9d2ac4a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MonitorDataCollectionRuleDataFlowOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e28001bae8dde55b09ebc93d72573d086b3471678ab9376fb58397279361854)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MonitorDataCollectionRuleDataFlowOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f3fe99a37a74266ffbc7c65e477f17d6b2ae1c0d94b6fe073fc14a8ac979493)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e37357f493fd96feb93ab04c9ba3ffd21760d46f8a20df9eea4700415bccd5ff)
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
            type_hints = typing.get_type_hints(_typecheckingstub__16f8b837a7f0ac2ccc598e8656dc844340d6afc00202328badf53b48cf1d29ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataFlow]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataFlow]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataFlow]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19211c8f99e693e17a52ce672f2aaafaa796160841818044805dec48626ccd3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitorDataCollectionRuleDataFlowOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDataFlowOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4c3d0559b2a7af7e3c93c11f6ce5dd64fc74b4cce670ea17392f5d6adc9f9777)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetBuiltInTransform")
    def reset_built_in_transform(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBuiltInTransform", []))

    @jsii.member(jsii_name="resetOutputStream")
    def reset_output_stream(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutputStream", []))

    @jsii.member(jsii_name="resetTransformKql")
    def reset_transform_kql(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTransformKql", []))

    @builtins.property
    @jsii.member(jsii_name="builtInTransformInput")
    def built_in_transform_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "builtInTransformInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationsInput")
    def destinations_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "destinationsInput"))

    @builtins.property
    @jsii.member(jsii_name="outputStreamInput")
    def output_stream_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "outputStreamInput"))

    @builtins.property
    @jsii.member(jsii_name="streamsInput")
    def streams_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "streamsInput"))

    @builtins.property
    @jsii.member(jsii_name="transformKqlInput")
    def transform_kql_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "transformKqlInput"))

    @builtins.property
    @jsii.member(jsii_name="builtInTransform")
    def built_in_transform(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "builtInTransform"))

    @built_in_transform.setter
    def built_in_transform(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d03e553b251524d586568c78b3442226119c632c5a22c4ada73be4320aa4382a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "builtInTransform", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="destinations")
    def destinations(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "destinations"))

    @destinations.setter
    def destinations(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1c3ab541bab6e813a141e98046559a185a3117aac7618ac05955f43018ca51f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="outputStream")
    def output_stream(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outputStream"))

    @output_stream.setter
    def output_stream(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82747043612d572183f743126834600111dbe1cbe0beb9b34e2c6bff289b6aee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outputStream", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="streams")
    def streams(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "streams"))

    @streams.setter
    def streams(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5d5cdf55d1808ceeb0ade162c05658ac355c00259c0977a978a8ed2acb2942c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "streams", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="transformKql")
    def transform_kql(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "transformKql"))

    @transform_kql.setter
    def transform_kql(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e185123c0ff9f2683216d5da44c60b17b01ffb8d0565bb3d2ee8dfd1b364e1bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transformKql", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleDataFlow]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleDataFlow]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleDataFlow]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ae601d4a96b61b1e90db264045b452e77a95599c2b7b7c10185d848b2b2a32e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDataSources",
    jsii_struct_bases=[],
    name_mapping={
        "data_import": "dataImport",
        "extension": "extension",
        "iis_log": "iisLog",
        "log_file": "logFile",
        "performance_counter": "performanceCounter",
        "platform_telemetry": "platformTelemetry",
        "prometheus_forwarder": "prometheusForwarder",
        "syslog": "syslog",
        "windows_event_log": "windowsEventLog",
        "windows_firewall_log": "windowsFirewallLog",
    },
)
class MonitorDataCollectionRuleDataSources:
    def __init__(
        self,
        *,
        data_import: typing.Optional[typing.Union["MonitorDataCollectionRuleDataSourcesDataImport", typing.Dict[builtins.str, typing.Any]]] = None,
        extension: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorDataCollectionRuleDataSourcesExtension", typing.Dict[builtins.str, typing.Any]]]]] = None,
        iis_log: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorDataCollectionRuleDataSourcesIisLog", typing.Dict[builtins.str, typing.Any]]]]] = None,
        log_file: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorDataCollectionRuleDataSourcesLogFile", typing.Dict[builtins.str, typing.Any]]]]] = None,
        performance_counter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorDataCollectionRuleDataSourcesPerformanceCounter", typing.Dict[builtins.str, typing.Any]]]]] = None,
        platform_telemetry: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorDataCollectionRuleDataSourcesPlatformTelemetry", typing.Dict[builtins.str, typing.Any]]]]] = None,
        prometheus_forwarder: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorDataCollectionRuleDataSourcesPrometheusForwarder", typing.Dict[builtins.str, typing.Any]]]]] = None,
        syslog: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorDataCollectionRuleDataSourcesSyslog", typing.Dict[builtins.str, typing.Any]]]]] = None,
        windows_event_log: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorDataCollectionRuleDataSourcesWindowsEventLog", typing.Dict[builtins.str, typing.Any]]]]] = None,
        windows_firewall_log: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorDataCollectionRuleDataSourcesWindowsFirewallLog", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param data_import: data_import block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#data_import MonitorDataCollectionRule#data_import}
        :param extension: extension block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#extension MonitorDataCollectionRule#extension}
        :param iis_log: iis_log block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#iis_log MonitorDataCollectionRule#iis_log}
        :param log_file: log_file block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#log_file MonitorDataCollectionRule#log_file}
        :param performance_counter: performance_counter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#performance_counter MonitorDataCollectionRule#performance_counter}
        :param platform_telemetry: platform_telemetry block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#platform_telemetry MonitorDataCollectionRule#platform_telemetry}
        :param prometheus_forwarder: prometheus_forwarder block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#prometheus_forwarder MonitorDataCollectionRule#prometheus_forwarder}
        :param syslog: syslog block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#syslog MonitorDataCollectionRule#syslog}
        :param windows_event_log: windows_event_log block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#windows_event_log MonitorDataCollectionRule#windows_event_log}
        :param windows_firewall_log: windows_firewall_log block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#windows_firewall_log MonitorDataCollectionRule#windows_firewall_log}
        '''
        if isinstance(data_import, dict):
            data_import = MonitorDataCollectionRuleDataSourcesDataImport(**data_import)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50c3daef060c1ba14b60de26ea3644ccaf37e883eede9cf3152594ac4b91630e)
            check_type(argname="argument data_import", value=data_import, expected_type=type_hints["data_import"])
            check_type(argname="argument extension", value=extension, expected_type=type_hints["extension"])
            check_type(argname="argument iis_log", value=iis_log, expected_type=type_hints["iis_log"])
            check_type(argname="argument log_file", value=log_file, expected_type=type_hints["log_file"])
            check_type(argname="argument performance_counter", value=performance_counter, expected_type=type_hints["performance_counter"])
            check_type(argname="argument platform_telemetry", value=platform_telemetry, expected_type=type_hints["platform_telemetry"])
            check_type(argname="argument prometheus_forwarder", value=prometheus_forwarder, expected_type=type_hints["prometheus_forwarder"])
            check_type(argname="argument syslog", value=syslog, expected_type=type_hints["syslog"])
            check_type(argname="argument windows_event_log", value=windows_event_log, expected_type=type_hints["windows_event_log"])
            check_type(argname="argument windows_firewall_log", value=windows_firewall_log, expected_type=type_hints["windows_firewall_log"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if data_import is not None:
            self._values["data_import"] = data_import
        if extension is not None:
            self._values["extension"] = extension
        if iis_log is not None:
            self._values["iis_log"] = iis_log
        if log_file is not None:
            self._values["log_file"] = log_file
        if performance_counter is not None:
            self._values["performance_counter"] = performance_counter
        if platform_telemetry is not None:
            self._values["platform_telemetry"] = platform_telemetry
        if prometheus_forwarder is not None:
            self._values["prometheus_forwarder"] = prometheus_forwarder
        if syslog is not None:
            self._values["syslog"] = syslog
        if windows_event_log is not None:
            self._values["windows_event_log"] = windows_event_log
        if windows_firewall_log is not None:
            self._values["windows_firewall_log"] = windows_firewall_log

    @builtins.property
    def data_import(
        self,
    ) -> typing.Optional["MonitorDataCollectionRuleDataSourcesDataImport"]:
        '''data_import block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#data_import MonitorDataCollectionRule#data_import}
        '''
        result = self._values.get("data_import")
        return typing.cast(typing.Optional["MonitorDataCollectionRuleDataSourcesDataImport"], result)

    @builtins.property
    def extension(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDataSourcesExtension"]]]:
        '''extension block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#extension MonitorDataCollectionRule#extension}
        '''
        result = self._values.get("extension")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDataSourcesExtension"]]], result)

    @builtins.property
    def iis_log(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDataSourcesIisLog"]]]:
        '''iis_log block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#iis_log MonitorDataCollectionRule#iis_log}
        '''
        result = self._values.get("iis_log")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDataSourcesIisLog"]]], result)

    @builtins.property
    def log_file(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDataSourcesLogFile"]]]:
        '''log_file block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#log_file MonitorDataCollectionRule#log_file}
        '''
        result = self._values.get("log_file")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDataSourcesLogFile"]]], result)

    @builtins.property
    def performance_counter(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDataSourcesPerformanceCounter"]]]:
        '''performance_counter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#performance_counter MonitorDataCollectionRule#performance_counter}
        '''
        result = self._values.get("performance_counter")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDataSourcesPerformanceCounter"]]], result)

    @builtins.property
    def platform_telemetry(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDataSourcesPlatformTelemetry"]]]:
        '''platform_telemetry block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#platform_telemetry MonitorDataCollectionRule#platform_telemetry}
        '''
        result = self._values.get("platform_telemetry")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDataSourcesPlatformTelemetry"]]], result)

    @builtins.property
    def prometheus_forwarder(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDataSourcesPrometheusForwarder"]]]:
        '''prometheus_forwarder block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#prometheus_forwarder MonitorDataCollectionRule#prometheus_forwarder}
        '''
        result = self._values.get("prometheus_forwarder")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDataSourcesPrometheusForwarder"]]], result)

    @builtins.property
    def syslog(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDataSourcesSyslog"]]]:
        '''syslog block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#syslog MonitorDataCollectionRule#syslog}
        '''
        result = self._values.get("syslog")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDataSourcesSyslog"]]], result)

    @builtins.property
    def windows_event_log(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDataSourcesWindowsEventLog"]]]:
        '''windows_event_log block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#windows_event_log MonitorDataCollectionRule#windows_event_log}
        '''
        result = self._values.get("windows_event_log")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDataSourcesWindowsEventLog"]]], result)

    @builtins.property
    def windows_firewall_log(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDataSourcesWindowsFirewallLog"]]]:
        '''windows_firewall_log block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#windows_firewall_log MonitorDataCollectionRule#windows_firewall_log}
        '''
        result = self._values.get("windows_firewall_log")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDataSourcesWindowsFirewallLog"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorDataCollectionRuleDataSources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDataSourcesDataImport",
    jsii_struct_bases=[],
    name_mapping={"event_hub_data_source": "eventHubDataSource"},
)
class MonitorDataCollectionRuleDataSourcesDataImport:
    def __init__(
        self,
        *,
        event_hub_data_source: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorDataCollectionRuleDataSourcesDataImportEventHubDataSource", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param event_hub_data_source: event_hub_data_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#event_hub_data_source MonitorDataCollectionRule#event_hub_data_source}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3262b7e4fba65b85ae0a8271ed3df0413aef70895f9bb24c6fc6610da49d2bae)
            check_type(argname="argument event_hub_data_source", value=event_hub_data_source, expected_type=type_hints["event_hub_data_source"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "event_hub_data_source": event_hub_data_source,
        }

    @builtins.property
    def event_hub_data_source(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDataSourcesDataImportEventHubDataSource"]]:
        '''event_hub_data_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#event_hub_data_source MonitorDataCollectionRule#event_hub_data_source}
        '''
        result = self._values.get("event_hub_data_source")
        assert result is not None, "Required property 'event_hub_data_source' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDataSourcesDataImportEventHubDataSource"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorDataCollectionRuleDataSourcesDataImport(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDataSourcesDataImportEventHubDataSource",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "stream": "stream",
        "consumer_group": "consumerGroup",
    },
)
class MonitorDataCollectionRuleDataSourcesDataImportEventHubDataSource:
    def __init__(
        self,
        *,
        name: builtins.str,
        stream: builtins.str,
        consumer_group: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#name MonitorDataCollectionRule#name}.
        :param stream: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#stream MonitorDataCollectionRule#stream}.
        :param consumer_group: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#consumer_group MonitorDataCollectionRule#consumer_group}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f2f3b342185c9de637d137d175678eff77f778fda571cc847a8c5b4828c5323)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument stream", value=stream, expected_type=type_hints["stream"])
            check_type(argname="argument consumer_group", value=consumer_group, expected_type=type_hints["consumer_group"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "stream": stream,
        }
        if consumer_group is not None:
            self._values["consumer_group"] = consumer_group

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#name MonitorDataCollectionRule#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def stream(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#stream MonitorDataCollectionRule#stream}.'''
        result = self._values.get("stream")
        assert result is not None, "Required property 'stream' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def consumer_group(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#consumer_group MonitorDataCollectionRule#consumer_group}.'''
        result = self._values.get("consumer_group")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorDataCollectionRuleDataSourcesDataImportEventHubDataSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorDataCollectionRuleDataSourcesDataImportEventHubDataSourceList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDataSourcesDataImportEventHubDataSourceList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__29590b283d356a0f90c9cc3128b67b845ce4cdeda8beed13ea38940ed7686a04)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MonitorDataCollectionRuleDataSourcesDataImportEventHubDataSourceOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ae9a7f6721561df6fc9c14806670eb54fecf35de55fc3af72cc6b8f22cf3ab7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MonitorDataCollectionRuleDataSourcesDataImportEventHubDataSourceOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfea3867418562ef8851fc1c89ecdcbf975b9228da27dd1055f27fa5c79d3171)
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
            type_hints = typing.get_type_hints(_typecheckingstub__529ccb764c8e7b468e996ee0d8873e53255fc39ed89eb95a0b016a82094f3622)
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
            type_hints = typing.get_type_hints(_typecheckingstub__55ed47aff4f3af3bab2d243d4e933beeb4651a3391057e700f2da7550403ed90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataSourcesDataImportEventHubDataSource]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataSourcesDataImportEventHubDataSource]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataSourcesDataImportEventHubDataSource]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cd03ac7c0bd7e474ba5b8207bc5fca2a97c2c54d78936e1e05ddc5971c3b3b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitorDataCollectionRuleDataSourcesDataImportEventHubDataSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDataSourcesDataImportEventHubDataSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f44bfe2c2089926bf7a525290cc575d620b333d029b0d2c142e954ec0d51f067)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetConsumerGroup")
    def reset_consumer_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConsumerGroup", []))

    @builtins.property
    @jsii.member(jsii_name="consumerGroupInput")
    def consumer_group_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "consumerGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="streamInput")
    def stream_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "streamInput"))

    @builtins.property
    @jsii.member(jsii_name="consumerGroup")
    def consumer_group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consumerGroup"))

    @consumer_group.setter
    def consumer_group(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74b562cd9ffdacde0d9ea28b274d6bb47fd9cc594824bab0d3c244b3a3196e54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consumerGroup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7869bab659488254e97b166fa162eddb98cac3ed4c25e9e509c6b23078d25634)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stream")
    def stream(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stream"))

    @stream.setter
    def stream(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__397ec18f5435583edd09a2ad3299ecbdf0e8e1b6d6ef49d1a96c27e2152bab25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stream", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleDataSourcesDataImportEventHubDataSource]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleDataSourcesDataImportEventHubDataSource]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleDataSourcesDataImportEventHubDataSource]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6ae81a81f9c633214caab5ae0efdcfe44a86ea39382d403ca1f0263526d700a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitorDataCollectionRuleDataSourcesDataImportOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDataSourcesDataImportOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cbf3731504544b30a8c9651015413a3a45b069b395baa58e796e79266b9d1998)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putEventHubDataSource")
    def put_event_hub_data_source(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorDataCollectionRuleDataSourcesDataImportEventHubDataSource, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d130638f8d2f6ba7debf434f56af56fad1f853a9089fbce7f1476f11c185b36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEventHubDataSource", [value]))

    @builtins.property
    @jsii.member(jsii_name="eventHubDataSource")
    def event_hub_data_source(
        self,
    ) -> MonitorDataCollectionRuleDataSourcesDataImportEventHubDataSourceList:
        return typing.cast(MonitorDataCollectionRuleDataSourcesDataImportEventHubDataSourceList, jsii.get(self, "eventHubDataSource"))

    @builtins.property
    @jsii.member(jsii_name="eventHubDataSourceInput")
    def event_hub_data_source_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataSourcesDataImportEventHubDataSource]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataSourcesDataImportEventHubDataSource]]], jsii.get(self, "eventHubDataSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitorDataCollectionRuleDataSourcesDataImport]:
        return typing.cast(typing.Optional[MonitorDataCollectionRuleDataSourcesDataImport], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorDataCollectionRuleDataSourcesDataImport],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c61704b586a19652403e830efc3ecffd3b09188fab704fa525b992f1dc06480)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDataSourcesExtension",
    jsii_struct_bases=[],
    name_mapping={
        "extension_name": "extensionName",
        "name": "name",
        "streams": "streams",
        "extension_json": "extensionJson",
        "input_data_sources": "inputDataSources",
    },
)
class MonitorDataCollectionRuleDataSourcesExtension:
    def __init__(
        self,
        *,
        extension_name: builtins.str,
        name: builtins.str,
        streams: typing.Sequence[builtins.str],
        extension_json: typing.Optional[builtins.str] = None,
        input_data_sources: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param extension_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#extension_name MonitorDataCollectionRule#extension_name}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#name MonitorDataCollectionRule#name}.
        :param streams: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#streams MonitorDataCollectionRule#streams}.
        :param extension_json: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#extension_json MonitorDataCollectionRule#extension_json}.
        :param input_data_sources: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#input_data_sources MonitorDataCollectionRule#input_data_sources}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__880b7ad1e3b0bd0ba7e0151d7e7567c5d08b9cbdfc6d38d39417b12702a3368f)
            check_type(argname="argument extension_name", value=extension_name, expected_type=type_hints["extension_name"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument streams", value=streams, expected_type=type_hints["streams"])
            check_type(argname="argument extension_json", value=extension_json, expected_type=type_hints["extension_json"])
            check_type(argname="argument input_data_sources", value=input_data_sources, expected_type=type_hints["input_data_sources"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "extension_name": extension_name,
            "name": name,
            "streams": streams,
        }
        if extension_json is not None:
            self._values["extension_json"] = extension_json
        if input_data_sources is not None:
            self._values["input_data_sources"] = input_data_sources

    @builtins.property
    def extension_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#extension_name MonitorDataCollectionRule#extension_name}.'''
        result = self._values.get("extension_name")
        assert result is not None, "Required property 'extension_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#name MonitorDataCollectionRule#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def streams(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#streams MonitorDataCollectionRule#streams}.'''
        result = self._values.get("streams")
        assert result is not None, "Required property 'streams' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def extension_json(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#extension_json MonitorDataCollectionRule#extension_json}.'''
        result = self._values.get("extension_json")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def input_data_sources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#input_data_sources MonitorDataCollectionRule#input_data_sources}.'''
        result = self._values.get("input_data_sources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorDataCollectionRuleDataSourcesExtension(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorDataCollectionRuleDataSourcesExtensionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDataSourcesExtensionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__183fae162e87e634b2a1f5afe600ebc7173826d68e760e51ee37419023830866)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MonitorDataCollectionRuleDataSourcesExtensionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcbd9f8ba2db26388671009239773467b9df840eb192aafbb15e32fbe6db5486)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MonitorDataCollectionRuleDataSourcesExtensionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7a9b8afdc59c99c73eafd4d2819580128b0f70cb88281820ff12e4121c0895d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9fa733b18a6e5102f40d47e6d9254aff9099cc2b95d7877810da5756c5f56b9f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__185756c2250710bef82bf9ac7c9bb9b2cc4e16b791ea9d93bac1f29419126d06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataSourcesExtension]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataSourcesExtension]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataSourcesExtension]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d0cd819b7de080bf03920306efacdd1aefc760d5024ea31242786ee123aa0f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitorDataCollectionRuleDataSourcesExtensionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDataSourcesExtensionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d52a47c60ab98c9c983f79ffe99470d98b01f78d2b3c72d7de6fdff9efd14a6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetExtensionJson")
    def reset_extension_json(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExtensionJson", []))

    @jsii.member(jsii_name="resetInputDataSources")
    def reset_input_data_sources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInputDataSources", []))

    @builtins.property
    @jsii.member(jsii_name="extensionJsonInput")
    def extension_json_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "extensionJsonInput"))

    @builtins.property
    @jsii.member(jsii_name="extensionNameInput")
    def extension_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "extensionNameInput"))

    @builtins.property
    @jsii.member(jsii_name="inputDataSourcesInput")
    def input_data_sources_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "inputDataSourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="streamsInput")
    def streams_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "streamsInput"))

    @builtins.property
    @jsii.member(jsii_name="extensionJson")
    def extension_json(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "extensionJson"))

    @extension_json.setter
    def extension_json(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae6e2ea2650bca6797764421dc9064fed839bc8a152f80c6c282e07160d96b1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "extensionJson", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="extensionName")
    def extension_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "extensionName"))

    @extension_name.setter
    def extension_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b90ad2b40420efecf2dd706280bf4eec18f806932690a7cee0d59f7995555fa6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "extensionName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="inputDataSources")
    def input_data_sources(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "inputDataSources"))

    @input_data_sources.setter
    def input_data_sources(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d043607978efb77412109d01c1589c0f4a02ce12d95b0d4be2879dc7ab7d6d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inputDataSources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35680830854aa39deac9d18cbfa14a1eb36b0479ff3535f70a2040634b7feac2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="streams")
    def streams(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "streams"))

    @streams.setter
    def streams(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d00efb2fbf8068731a29e8ab7f73f72aecd0787c4401f1cae08f2ee5e2c1e50d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "streams", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleDataSourcesExtension]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleDataSourcesExtension]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleDataSourcesExtension]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67c7afc49a4e77c572bcb5390bd01ce235841f959207e50382bcb1962e0b8e04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDataSourcesIisLog",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "streams": "streams",
        "log_directories": "logDirectories",
    },
)
class MonitorDataCollectionRuleDataSourcesIisLog:
    def __init__(
        self,
        *,
        name: builtins.str,
        streams: typing.Sequence[builtins.str],
        log_directories: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#name MonitorDataCollectionRule#name}.
        :param streams: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#streams MonitorDataCollectionRule#streams}.
        :param log_directories: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#log_directories MonitorDataCollectionRule#log_directories}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ef8c9fca9c8b9b79002539a94df023be6df964f6f39c0d558c3a4777c90ccd3)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument streams", value=streams, expected_type=type_hints["streams"])
            check_type(argname="argument log_directories", value=log_directories, expected_type=type_hints["log_directories"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "streams": streams,
        }
        if log_directories is not None:
            self._values["log_directories"] = log_directories

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#name MonitorDataCollectionRule#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def streams(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#streams MonitorDataCollectionRule#streams}.'''
        result = self._values.get("streams")
        assert result is not None, "Required property 'streams' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def log_directories(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#log_directories MonitorDataCollectionRule#log_directories}.'''
        result = self._values.get("log_directories")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorDataCollectionRuleDataSourcesIisLog(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorDataCollectionRuleDataSourcesIisLogList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDataSourcesIisLogList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__06b3a67e2c30d18451d24fb3cf65a1636d46c5468602d45254cae2513ae8a595)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MonitorDataCollectionRuleDataSourcesIisLogOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ceb44a30fc035f9e53bcc72d6a21ae2404ed42c790558ae375399abf84bf576)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MonitorDataCollectionRuleDataSourcesIisLogOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__752acecd7c19c1cb258e4b1a2317dab77fa17dee046a0430f5d2f0557d7fb703)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4cf7e719bef4c809a5a420826ce55f4db3efc0de9f49827d0a64a049363438b4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__954312fad0afa4158e1064b1f4fbf1147bebc4447552b060565ccb9ae234c882)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataSourcesIisLog]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataSourcesIisLog]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataSourcesIisLog]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63b258eab377dfdb70dc0b6c7c9ae85ab87df9549b9bfbfea17ef93cb4ef0d79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitorDataCollectionRuleDataSourcesIisLogOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDataSourcesIisLogOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c618e00db752173dedb3c55c3f7198f2bda0afc2a7279d388b871fed33c8f125)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetLogDirectories")
    def reset_log_directories(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogDirectories", []))

    @builtins.property
    @jsii.member(jsii_name="logDirectoriesInput")
    def log_directories_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "logDirectoriesInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="streamsInput")
    def streams_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "streamsInput"))

    @builtins.property
    @jsii.member(jsii_name="logDirectories")
    def log_directories(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "logDirectories"))

    @log_directories.setter
    def log_directories(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac77ff797f08d8baeebc79d65bf0e69663aeda19b3415dead23bda985483bf1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logDirectories", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f369b767deef3361ed020489d6f1191a77d2eaf098a23b9171513af6a67e776)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="streams")
    def streams(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "streams"))

    @streams.setter
    def streams(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7535688f3775d46b49526d26e308f0b6d5b25867b5f97804bad20dd8c71267ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "streams", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleDataSourcesIisLog]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleDataSourcesIisLog]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleDataSourcesIisLog]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a506c53057206010880750cbb88d05dc756409723ba562dee2b5afa5abd63e6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDataSourcesLogFile",
    jsii_struct_bases=[],
    name_mapping={
        "file_patterns": "filePatterns",
        "format": "format",
        "name": "name",
        "streams": "streams",
        "settings": "settings",
    },
)
class MonitorDataCollectionRuleDataSourcesLogFile:
    def __init__(
        self,
        *,
        file_patterns: typing.Sequence[builtins.str],
        format: builtins.str,
        name: builtins.str,
        streams: typing.Sequence[builtins.str],
        settings: typing.Optional[typing.Union["MonitorDataCollectionRuleDataSourcesLogFileSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param file_patterns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#file_patterns MonitorDataCollectionRule#file_patterns}.
        :param format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#format MonitorDataCollectionRule#format}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#name MonitorDataCollectionRule#name}.
        :param streams: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#streams MonitorDataCollectionRule#streams}.
        :param settings: settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#settings MonitorDataCollectionRule#settings}
        '''
        if isinstance(settings, dict):
            settings = MonitorDataCollectionRuleDataSourcesLogFileSettings(**settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce6bf92be26f173593b7b8f50b510aaa03756cc509333fdb39e9ac87d3776cd8)
            check_type(argname="argument file_patterns", value=file_patterns, expected_type=type_hints["file_patterns"])
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument streams", value=streams, expected_type=type_hints["streams"])
            check_type(argname="argument settings", value=settings, expected_type=type_hints["settings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "file_patterns": file_patterns,
            "format": format,
            "name": name,
            "streams": streams,
        }
        if settings is not None:
            self._values["settings"] = settings

    @builtins.property
    def file_patterns(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#file_patterns MonitorDataCollectionRule#file_patterns}.'''
        result = self._values.get("file_patterns")
        assert result is not None, "Required property 'file_patterns' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def format(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#format MonitorDataCollectionRule#format}.'''
        result = self._values.get("format")
        assert result is not None, "Required property 'format' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#name MonitorDataCollectionRule#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def streams(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#streams MonitorDataCollectionRule#streams}.'''
        result = self._values.get("streams")
        assert result is not None, "Required property 'streams' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def settings(
        self,
    ) -> typing.Optional["MonitorDataCollectionRuleDataSourcesLogFileSettings"]:
        '''settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#settings MonitorDataCollectionRule#settings}
        '''
        result = self._values.get("settings")
        return typing.cast(typing.Optional["MonitorDataCollectionRuleDataSourcesLogFileSettings"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorDataCollectionRuleDataSourcesLogFile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorDataCollectionRuleDataSourcesLogFileList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDataSourcesLogFileList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__727135006aedeb8ae5ce3fa6cef49e607828971f07d6d32e647023f7487bb7f1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MonitorDataCollectionRuleDataSourcesLogFileOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18daa58e609b8a8874b4d6abb918f3653c290f91d97452e6b3008a2afb9d7bfa)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MonitorDataCollectionRuleDataSourcesLogFileOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__686e4534090feaf1ee8efbc4e2b3ea209dfb5eb27aa22d02c2debc3bac6470d9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f642acceeb4ca4caadc25df35494e5f438044570134e607a27d4383dcc0449bc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d71fbcf47ceb6aa01f8cc4bd7fcffe3f4c26df7c5d1b40f99f0e0ed98186440b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataSourcesLogFile]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataSourcesLogFile]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataSourcesLogFile]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42c55079e690c1c4f9d4e94dc2aae91a29fa878b3a573c15438d39e72641a548)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitorDataCollectionRuleDataSourcesLogFileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDataSourcesLogFileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__92bea6f0cb202c919836612c29ee2784808e7bb1598645092e715d95eef46a64)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putSettings")
    def put_settings(
        self,
        *,
        text: typing.Union["MonitorDataCollectionRuleDataSourcesLogFileSettingsText", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param text: text block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#text MonitorDataCollectionRule#text}
        '''
        value = MonitorDataCollectionRuleDataSourcesLogFileSettings(text=text)

        return typing.cast(None, jsii.invoke(self, "putSettings", [value]))

    @jsii.member(jsii_name="resetSettings")
    def reset_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSettings", []))

    @builtins.property
    @jsii.member(jsii_name="settings")
    def settings(
        self,
    ) -> "MonitorDataCollectionRuleDataSourcesLogFileSettingsOutputReference":
        return typing.cast("MonitorDataCollectionRuleDataSourcesLogFileSettingsOutputReference", jsii.get(self, "settings"))

    @builtins.property
    @jsii.member(jsii_name="filePatternsInput")
    def file_patterns_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "filePatternsInput"))

    @builtins.property
    @jsii.member(jsii_name="formatInput")
    def format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "formatInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="settingsInput")
    def settings_input(
        self,
    ) -> typing.Optional["MonitorDataCollectionRuleDataSourcesLogFileSettings"]:
        return typing.cast(typing.Optional["MonitorDataCollectionRuleDataSourcesLogFileSettings"], jsii.get(self, "settingsInput"))

    @builtins.property
    @jsii.member(jsii_name="streamsInput")
    def streams_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "streamsInput"))

    @builtins.property
    @jsii.member(jsii_name="filePatterns")
    def file_patterns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "filePatterns"))

    @file_patterns.setter
    def file_patterns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e9d5cab40adfc1b6fb3b04a6ee823caabd50af330c9cdc2fd206fe9acabfc4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filePatterns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="format")
    def format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "format"))

    @format.setter
    def format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3861ce8f7db6e132b46d0cd7589274e19436415d22189db5abddb31b30382b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "format", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d694afa9393a29374778337827ed1e372af586609b98063939930b1919f48e8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="streams")
    def streams(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "streams"))

    @streams.setter
    def streams(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c151260505352414307da7588cb600525382ed38e04f8e69c0f5a01c3f47a4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "streams", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleDataSourcesLogFile]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleDataSourcesLogFile]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleDataSourcesLogFile]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebffeec8e64047386c02e4a1b41c2cdb189a883936bd11dac86af50d3261d2ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDataSourcesLogFileSettings",
    jsii_struct_bases=[],
    name_mapping={"text": "text"},
)
class MonitorDataCollectionRuleDataSourcesLogFileSettings:
    def __init__(
        self,
        *,
        text: typing.Union["MonitorDataCollectionRuleDataSourcesLogFileSettingsText", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param text: text block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#text MonitorDataCollectionRule#text}
        '''
        if isinstance(text, dict):
            text = MonitorDataCollectionRuleDataSourcesLogFileSettingsText(**text)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95b234245330a8d0fc8eacc51541d51a7c89e09f6bb857f8bb16c20454ecb08c)
            check_type(argname="argument text", value=text, expected_type=type_hints["text"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "text": text,
        }

    @builtins.property
    def text(self) -> "MonitorDataCollectionRuleDataSourcesLogFileSettingsText":
        '''text block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#text MonitorDataCollectionRule#text}
        '''
        result = self._values.get("text")
        assert result is not None, "Required property 'text' is missing"
        return typing.cast("MonitorDataCollectionRuleDataSourcesLogFileSettingsText", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorDataCollectionRuleDataSourcesLogFileSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorDataCollectionRuleDataSourcesLogFileSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDataSourcesLogFileSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc06b4ab28a44d9250550e345d6e992cc5a255db20b244e7a35d7d30543d17bb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putText")
    def put_text(self, *, record_start_timestamp_format: builtins.str) -> None:
        '''
        :param record_start_timestamp_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#record_start_timestamp_format MonitorDataCollectionRule#record_start_timestamp_format}.
        '''
        value = MonitorDataCollectionRuleDataSourcesLogFileSettingsText(
            record_start_timestamp_format=record_start_timestamp_format
        )

        return typing.cast(None, jsii.invoke(self, "putText", [value]))

    @builtins.property
    @jsii.member(jsii_name="text")
    def text(
        self,
    ) -> "MonitorDataCollectionRuleDataSourcesLogFileSettingsTextOutputReference":
        return typing.cast("MonitorDataCollectionRuleDataSourcesLogFileSettingsTextOutputReference", jsii.get(self, "text"))

    @builtins.property
    @jsii.member(jsii_name="textInput")
    def text_input(
        self,
    ) -> typing.Optional["MonitorDataCollectionRuleDataSourcesLogFileSettingsText"]:
        return typing.cast(typing.Optional["MonitorDataCollectionRuleDataSourcesLogFileSettingsText"], jsii.get(self, "textInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitorDataCollectionRuleDataSourcesLogFileSettings]:
        return typing.cast(typing.Optional[MonitorDataCollectionRuleDataSourcesLogFileSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorDataCollectionRuleDataSourcesLogFileSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f677a00e585184c248d95092d1a1a237593fa4b56a313377ab0448b9c263f5a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDataSourcesLogFileSettingsText",
    jsii_struct_bases=[],
    name_mapping={"record_start_timestamp_format": "recordStartTimestampFormat"},
)
class MonitorDataCollectionRuleDataSourcesLogFileSettingsText:
    def __init__(self, *, record_start_timestamp_format: builtins.str) -> None:
        '''
        :param record_start_timestamp_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#record_start_timestamp_format MonitorDataCollectionRule#record_start_timestamp_format}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95255289c5e4137d42b09cc7a318a73acb6d1dc2303b37ef18d657e89efe34b7)
            check_type(argname="argument record_start_timestamp_format", value=record_start_timestamp_format, expected_type=type_hints["record_start_timestamp_format"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "record_start_timestamp_format": record_start_timestamp_format,
        }

    @builtins.property
    def record_start_timestamp_format(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#record_start_timestamp_format MonitorDataCollectionRule#record_start_timestamp_format}.'''
        result = self._values.get("record_start_timestamp_format")
        assert result is not None, "Required property 'record_start_timestamp_format' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorDataCollectionRuleDataSourcesLogFileSettingsText(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorDataCollectionRuleDataSourcesLogFileSettingsTextOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDataSourcesLogFileSettingsTextOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4732828277e824f249dd704e72000b2b5609f4a48028f2b14884f04c4c59c619)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="recordStartTimestampFormatInput")
    def record_start_timestamp_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recordStartTimestampFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="recordStartTimestampFormat")
    def record_start_timestamp_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recordStartTimestampFormat"))

    @record_start_timestamp_format.setter
    def record_start_timestamp_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f9c8c490846ca7ba7f9c1d43328a58c8908dd0192b65923431deae7f2d1bdca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recordStartTimestampFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitorDataCollectionRuleDataSourcesLogFileSettingsText]:
        return typing.cast(typing.Optional[MonitorDataCollectionRuleDataSourcesLogFileSettingsText], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorDataCollectionRuleDataSourcesLogFileSettingsText],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8a9db2bf08bee988ffe81d2ac84f12288f91c711f54cdd54659d8b60bc493c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitorDataCollectionRuleDataSourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDataSourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2effe2f8c570d9473506ca26fa08538e9686d88823968e25280314ce036abb49)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDataImport")
    def put_data_import(
        self,
        *,
        event_hub_data_source: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorDataCollectionRuleDataSourcesDataImportEventHubDataSource, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param event_hub_data_source: event_hub_data_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#event_hub_data_source MonitorDataCollectionRule#event_hub_data_source}
        '''
        value = MonitorDataCollectionRuleDataSourcesDataImport(
            event_hub_data_source=event_hub_data_source
        )

        return typing.cast(None, jsii.invoke(self, "putDataImport", [value]))

    @jsii.member(jsii_name="putExtension")
    def put_extension(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorDataCollectionRuleDataSourcesExtension, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c0a89278e0341b256e9f9cc8e1d9d492bc0e448d8018ca9d7cb9088b0251dd6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putExtension", [value]))

    @jsii.member(jsii_name="putIisLog")
    def put_iis_log(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorDataCollectionRuleDataSourcesIisLog, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__479e5fb7f6b3bd77369d320a95d5dda73a25207f9e6afde8d1b7f5697cc7c3ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIisLog", [value]))

    @jsii.member(jsii_name="putLogFile")
    def put_log_file(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorDataCollectionRuleDataSourcesLogFile, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f84c621f1373a4e36867e0e7a44cd5fcc625a0c01046e9742eb4c00a631f5991)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLogFile", [value]))

    @jsii.member(jsii_name="putPerformanceCounter")
    def put_performance_counter(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorDataCollectionRuleDataSourcesPerformanceCounter", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b0b23419be8886df574a3538f0029ecb4dc28798e8cf2988355ce62ea204452)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPerformanceCounter", [value]))

    @jsii.member(jsii_name="putPlatformTelemetry")
    def put_platform_telemetry(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorDataCollectionRuleDataSourcesPlatformTelemetry", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89117c9722f1d47111ae53313de1e42c5bffa808939d9e009e266f36cd54c68c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPlatformTelemetry", [value]))

    @jsii.member(jsii_name="putPrometheusForwarder")
    def put_prometheus_forwarder(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorDataCollectionRuleDataSourcesPrometheusForwarder", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__446f8dba2d704141f0974d30fb46b96460d04c072f7a06bfa65ae0acba3688a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPrometheusForwarder", [value]))

    @jsii.member(jsii_name="putSyslog")
    def put_syslog(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorDataCollectionRuleDataSourcesSyslog", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24b4fc0a3e1e4514bdc017ec8e53c7c1d6b3f0d0fd2a867d9635198eeb9a9979)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSyslog", [value]))

    @jsii.member(jsii_name="putWindowsEventLog")
    def put_windows_event_log(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorDataCollectionRuleDataSourcesWindowsEventLog", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__678e2a6c50a509255b32cdb494db7c92fc40cca514d78b7b7865700b097015e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putWindowsEventLog", [value]))

    @jsii.member(jsii_name="putWindowsFirewallLog")
    def put_windows_firewall_log(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorDataCollectionRuleDataSourcesWindowsFirewallLog", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67b556c47dc3f879401f4125b0b86b6b58e4ea460632d4fd37138fd836339706)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putWindowsFirewallLog", [value]))

    @jsii.member(jsii_name="resetDataImport")
    def reset_data_import(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataImport", []))

    @jsii.member(jsii_name="resetExtension")
    def reset_extension(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExtension", []))

    @jsii.member(jsii_name="resetIisLog")
    def reset_iis_log(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIisLog", []))

    @jsii.member(jsii_name="resetLogFile")
    def reset_log_file(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogFile", []))

    @jsii.member(jsii_name="resetPerformanceCounter")
    def reset_performance_counter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPerformanceCounter", []))

    @jsii.member(jsii_name="resetPlatformTelemetry")
    def reset_platform_telemetry(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPlatformTelemetry", []))

    @jsii.member(jsii_name="resetPrometheusForwarder")
    def reset_prometheus_forwarder(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrometheusForwarder", []))

    @jsii.member(jsii_name="resetSyslog")
    def reset_syslog(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSyslog", []))

    @jsii.member(jsii_name="resetWindowsEventLog")
    def reset_windows_event_log(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWindowsEventLog", []))

    @jsii.member(jsii_name="resetWindowsFirewallLog")
    def reset_windows_firewall_log(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWindowsFirewallLog", []))

    @builtins.property
    @jsii.member(jsii_name="dataImport")
    def data_import(
        self,
    ) -> MonitorDataCollectionRuleDataSourcesDataImportOutputReference:
        return typing.cast(MonitorDataCollectionRuleDataSourcesDataImportOutputReference, jsii.get(self, "dataImport"))

    @builtins.property
    @jsii.member(jsii_name="extension")
    def extension(self) -> MonitorDataCollectionRuleDataSourcesExtensionList:
        return typing.cast(MonitorDataCollectionRuleDataSourcesExtensionList, jsii.get(self, "extension"))

    @builtins.property
    @jsii.member(jsii_name="iisLog")
    def iis_log(self) -> MonitorDataCollectionRuleDataSourcesIisLogList:
        return typing.cast(MonitorDataCollectionRuleDataSourcesIisLogList, jsii.get(self, "iisLog"))

    @builtins.property
    @jsii.member(jsii_name="logFile")
    def log_file(self) -> MonitorDataCollectionRuleDataSourcesLogFileList:
        return typing.cast(MonitorDataCollectionRuleDataSourcesLogFileList, jsii.get(self, "logFile"))

    @builtins.property
    @jsii.member(jsii_name="performanceCounter")
    def performance_counter(
        self,
    ) -> "MonitorDataCollectionRuleDataSourcesPerformanceCounterList":
        return typing.cast("MonitorDataCollectionRuleDataSourcesPerformanceCounterList", jsii.get(self, "performanceCounter"))

    @builtins.property
    @jsii.member(jsii_name="platformTelemetry")
    def platform_telemetry(
        self,
    ) -> "MonitorDataCollectionRuleDataSourcesPlatformTelemetryList":
        return typing.cast("MonitorDataCollectionRuleDataSourcesPlatformTelemetryList", jsii.get(self, "platformTelemetry"))

    @builtins.property
    @jsii.member(jsii_name="prometheusForwarder")
    def prometheus_forwarder(
        self,
    ) -> "MonitorDataCollectionRuleDataSourcesPrometheusForwarderList":
        return typing.cast("MonitorDataCollectionRuleDataSourcesPrometheusForwarderList", jsii.get(self, "prometheusForwarder"))

    @builtins.property
    @jsii.member(jsii_name="syslog")
    def syslog(self) -> "MonitorDataCollectionRuleDataSourcesSyslogList":
        return typing.cast("MonitorDataCollectionRuleDataSourcesSyslogList", jsii.get(self, "syslog"))

    @builtins.property
    @jsii.member(jsii_name="windowsEventLog")
    def windows_event_log(
        self,
    ) -> "MonitorDataCollectionRuleDataSourcesWindowsEventLogList":
        return typing.cast("MonitorDataCollectionRuleDataSourcesWindowsEventLogList", jsii.get(self, "windowsEventLog"))

    @builtins.property
    @jsii.member(jsii_name="windowsFirewallLog")
    def windows_firewall_log(
        self,
    ) -> "MonitorDataCollectionRuleDataSourcesWindowsFirewallLogList":
        return typing.cast("MonitorDataCollectionRuleDataSourcesWindowsFirewallLogList", jsii.get(self, "windowsFirewallLog"))

    @builtins.property
    @jsii.member(jsii_name="dataImportInput")
    def data_import_input(
        self,
    ) -> typing.Optional[MonitorDataCollectionRuleDataSourcesDataImport]:
        return typing.cast(typing.Optional[MonitorDataCollectionRuleDataSourcesDataImport], jsii.get(self, "dataImportInput"))

    @builtins.property
    @jsii.member(jsii_name="extensionInput")
    def extension_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataSourcesExtension]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataSourcesExtension]]], jsii.get(self, "extensionInput"))

    @builtins.property
    @jsii.member(jsii_name="iisLogInput")
    def iis_log_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataSourcesIisLog]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataSourcesIisLog]]], jsii.get(self, "iisLogInput"))

    @builtins.property
    @jsii.member(jsii_name="logFileInput")
    def log_file_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataSourcesLogFile]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataSourcesLogFile]]], jsii.get(self, "logFileInput"))

    @builtins.property
    @jsii.member(jsii_name="performanceCounterInput")
    def performance_counter_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDataSourcesPerformanceCounter"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDataSourcesPerformanceCounter"]]], jsii.get(self, "performanceCounterInput"))

    @builtins.property
    @jsii.member(jsii_name="platformTelemetryInput")
    def platform_telemetry_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDataSourcesPlatformTelemetry"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDataSourcesPlatformTelemetry"]]], jsii.get(self, "platformTelemetryInput"))

    @builtins.property
    @jsii.member(jsii_name="prometheusForwarderInput")
    def prometheus_forwarder_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDataSourcesPrometheusForwarder"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDataSourcesPrometheusForwarder"]]], jsii.get(self, "prometheusForwarderInput"))

    @builtins.property
    @jsii.member(jsii_name="syslogInput")
    def syslog_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDataSourcesSyslog"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDataSourcesSyslog"]]], jsii.get(self, "syslogInput"))

    @builtins.property
    @jsii.member(jsii_name="windowsEventLogInput")
    def windows_event_log_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDataSourcesWindowsEventLog"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDataSourcesWindowsEventLog"]]], jsii.get(self, "windowsEventLogInput"))

    @builtins.property
    @jsii.member(jsii_name="windowsFirewallLogInput")
    def windows_firewall_log_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDataSourcesWindowsFirewallLog"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDataSourcesWindowsFirewallLog"]]], jsii.get(self, "windowsFirewallLogInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MonitorDataCollectionRuleDataSources]:
        return typing.cast(typing.Optional[MonitorDataCollectionRuleDataSources], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorDataCollectionRuleDataSources],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de9fcfd914b9be386362f91e5d399a648425be687b5559c9d4e9dbf6d3ca17c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDataSourcesPerformanceCounter",
    jsii_struct_bases=[],
    name_mapping={
        "counter_specifiers": "counterSpecifiers",
        "name": "name",
        "sampling_frequency_in_seconds": "samplingFrequencyInSeconds",
        "streams": "streams",
    },
)
class MonitorDataCollectionRuleDataSourcesPerformanceCounter:
    def __init__(
        self,
        *,
        counter_specifiers: typing.Sequence[builtins.str],
        name: builtins.str,
        sampling_frequency_in_seconds: jsii.Number,
        streams: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param counter_specifiers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#counter_specifiers MonitorDataCollectionRule#counter_specifiers}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#name MonitorDataCollectionRule#name}.
        :param sampling_frequency_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#sampling_frequency_in_seconds MonitorDataCollectionRule#sampling_frequency_in_seconds}.
        :param streams: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#streams MonitorDataCollectionRule#streams}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78ba1f5d9613309985657fe5930e78b29ab6382c52d1effa76c6bbec356ed669)
            check_type(argname="argument counter_specifiers", value=counter_specifiers, expected_type=type_hints["counter_specifiers"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument sampling_frequency_in_seconds", value=sampling_frequency_in_seconds, expected_type=type_hints["sampling_frequency_in_seconds"])
            check_type(argname="argument streams", value=streams, expected_type=type_hints["streams"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "counter_specifiers": counter_specifiers,
            "name": name,
            "sampling_frequency_in_seconds": sampling_frequency_in_seconds,
            "streams": streams,
        }

    @builtins.property
    def counter_specifiers(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#counter_specifiers MonitorDataCollectionRule#counter_specifiers}.'''
        result = self._values.get("counter_specifiers")
        assert result is not None, "Required property 'counter_specifiers' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#name MonitorDataCollectionRule#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sampling_frequency_in_seconds(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#sampling_frequency_in_seconds MonitorDataCollectionRule#sampling_frequency_in_seconds}.'''
        result = self._values.get("sampling_frequency_in_seconds")
        assert result is not None, "Required property 'sampling_frequency_in_seconds' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def streams(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#streams MonitorDataCollectionRule#streams}.'''
        result = self._values.get("streams")
        assert result is not None, "Required property 'streams' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorDataCollectionRuleDataSourcesPerformanceCounter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorDataCollectionRuleDataSourcesPerformanceCounterList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDataSourcesPerformanceCounterList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e176ba6c348b43592700cf73b905e40b6e43c0ec8716e5c3463fc730347ae7a1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MonitorDataCollectionRuleDataSourcesPerformanceCounterOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3df5f8db59d7a70d216f8b9d09242dea4d008534d6c676b32f5c9082c4a5e52)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MonitorDataCollectionRuleDataSourcesPerformanceCounterOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a46ef8e935b7375dc66288bcbfa68000ba20431c33565aa6ab0db1ac11d5247b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a50725eb29f40423111863c87f0fd76d5a138203d80f1f44cd8b71d14aaa5010)
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
            type_hints = typing.get_type_hints(_typecheckingstub__afd547505ac563cc2877a062839063bffca99801d395a2c457198379b0a157e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataSourcesPerformanceCounter]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataSourcesPerformanceCounter]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataSourcesPerformanceCounter]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da162700eecd9b67119ff4ba6574311c9cbf7617dde1c9306c4a761f93a5d923)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitorDataCollectionRuleDataSourcesPerformanceCounterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDataSourcesPerformanceCounterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eba48b3032f1fbdbec9520c26c08f837f3499f3787aad32081ac6bf7d9c0a1bf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="counterSpecifiersInput")
    def counter_specifiers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "counterSpecifiersInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="samplingFrequencyInSecondsInput")
    def sampling_frequency_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "samplingFrequencyInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="streamsInput")
    def streams_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "streamsInput"))

    @builtins.property
    @jsii.member(jsii_name="counterSpecifiers")
    def counter_specifiers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "counterSpecifiers"))

    @counter_specifiers.setter
    def counter_specifiers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__019fc55d291fdf6ed53eabcdfe5a735e7cfe4e23b2bc2205f2076a530231696c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "counterSpecifiers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44685a243f0dd09810e08799a3cb881340919bfdab2f5963000a5fefa414a0de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="samplingFrequencyInSeconds")
    def sampling_frequency_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "samplingFrequencyInSeconds"))

    @sampling_frequency_in_seconds.setter
    def sampling_frequency_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55e296f08e7386d1e845462f452383c1b5701615f2293becda6436199586af13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "samplingFrequencyInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="streams")
    def streams(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "streams"))

    @streams.setter
    def streams(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0a02f98829b60720def8c2570ddc43664284f7ec78b53b572f0f27c587664c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "streams", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleDataSourcesPerformanceCounter]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleDataSourcesPerformanceCounter]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleDataSourcesPerformanceCounter]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b102ff800cdee7e14415df5d29642221721ec2b922472f59e0ae5a26a074e62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDataSourcesPlatformTelemetry",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "streams": "streams"},
)
class MonitorDataCollectionRuleDataSourcesPlatformTelemetry:
    def __init__(
        self,
        *,
        name: builtins.str,
        streams: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#name MonitorDataCollectionRule#name}.
        :param streams: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#streams MonitorDataCollectionRule#streams}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__893b7642dc4492cb01e1fc646c94a91668454a46f91008a4605d9b08fe53b0f7)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument streams", value=streams, expected_type=type_hints["streams"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "streams": streams,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#name MonitorDataCollectionRule#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def streams(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#streams MonitorDataCollectionRule#streams}.'''
        result = self._values.get("streams")
        assert result is not None, "Required property 'streams' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorDataCollectionRuleDataSourcesPlatformTelemetry(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorDataCollectionRuleDataSourcesPlatformTelemetryList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDataSourcesPlatformTelemetryList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__40b8ffd17e076f7ce35660925126a7d27653b7b891169cdb5dad3462520557d4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MonitorDataCollectionRuleDataSourcesPlatformTelemetryOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecb14f862f326f28c802aed5d368d3f8bdbbf88ac91778583294dad151299fbe)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MonitorDataCollectionRuleDataSourcesPlatformTelemetryOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71e6b77e81de88cf838253f01612e4950ceeb9fe4b49d712e8d7873b4cc505ae)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0338a47c8935435c408cb764cc97ed35d60160a5ba4f501c4317ee3662ab73ac)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f33b81a6bb8842c742d3165482ffcd32e6e91230c49be8ef7c974aab6a9f0526)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataSourcesPlatformTelemetry]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataSourcesPlatformTelemetry]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataSourcesPlatformTelemetry]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1419b396805706fce6f8d5a6d8badde0e7ecf405f0ac0098881d13d718f53661)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitorDataCollectionRuleDataSourcesPlatformTelemetryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDataSourcesPlatformTelemetryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__72b053ce11de80de9743885e7c9b439986c3382d770f0c040ab97bc0f748a484)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="streamsInput")
    def streams_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "streamsInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__166ce3b31b2eb654cd710d257e20968d0e41132c8e61feda632062d5e183b048)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="streams")
    def streams(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "streams"))

    @streams.setter
    def streams(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed326a49ab99ecdf7aa42121c0cb3b8eae5fd045fc70361e56a2186a81ae119a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "streams", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleDataSourcesPlatformTelemetry]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleDataSourcesPlatformTelemetry]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleDataSourcesPlatformTelemetry]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d3315c2cfaab6618515c86287781d06b3f1f3daf34c9d94027784c67fd68f0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDataSourcesPrometheusForwarder",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "streams": "streams",
        "label_include_filter": "labelIncludeFilter",
    },
)
class MonitorDataCollectionRuleDataSourcesPrometheusForwarder:
    def __init__(
        self,
        *,
        name: builtins.str,
        streams: typing.Sequence[builtins.str],
        label_include_filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorDataCollectionRuleDataSourcesPrometheusForwarderLabelIncludeFilter", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#name MonitorDataCollectionRule#name}.
        :param streams: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#streams MonitorDataCollectionRule#streams}.
        :param label_include_filter: label_include_filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#label_include_filter MonitorDataCollectionRule#label_include_filter}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__748a48c639c5c6d46cac71e2d1bbc17ab59f3d95e1ffab7a424dc9b5f78e6297)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument streams", value=streams, expected_type=type_hints["streams"])
            check_type(argname="argument label_include_filter", value=label_include_filter, expected_type=type_hints["label_include_filter"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "streams": streams,
        }
        if label_include_filter is not None:
            self._values["label_include_filter"] = label_include_filter

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#name MonitorDataCollectionRule#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def streams(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#streams MonitorDataCollectionRule#streams}.'''
        result = self._values.get("streams")
        assert result is not None, "Required property 'streams' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def label_include_filter(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDataSourcesPrometheusForwarderLabelIncludeFilter"]]]:
        '''label_include_filter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#label_include_filter MonitorDataCollectionRule#label_include_filter}
        '''
        result = self._values.get("label_include_filter")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDataSourcesPrometheusForwarderLabelIncludeFilter"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorDataCollectionRuleDataSourcesPrometheusForwarder(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDataSourcesPrometheusForwarderLabelIncludeFilter",
    jsii_struct_bases=[],
    name_mapping={"label": "label", "value": "value"},
)
class MonitorDataCollectionRuleDataSourcesPrometheusForwarderLabelIncludeFilter:
    def __init__(self, *, label: builtins.str, value: builtins.str) -> None:
        '''
        :param label: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#label MonitorDataCollectionRule#label}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#value MonitorDataCollectionRule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7819ef7b9f42ab08f81f81aff0b853cf3db67b21f7054c7e036d5c7010b7941)
            check_type(argname="argument label", value=label, expected_type=type_hints["label"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "label": label,
            "value": value,
        }

    @builtins.property
    def label(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#label MonitorDataCollectionRule#label}.'''
        result = self._values.get("label")
        assert result is not None, "Required property 'label' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#value MonitorDataCollectionRule#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorDataCollectionRuleDataSourcesPrometheusForwarderLabelIncludeFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorDataCollectionRuleDataSourcesPrometheusForwarderLabelIncludeFilterList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDataSourcesPrometheusForwarderLabelIncludeFilterList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dde0866ef111a4158a013d6a97cce28736a3d65f1bffa01461148886731799c1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MonitorDataCollectionRuleDataSourcesPrometheusForwarderLabelIncludeFilterOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2df643227f769dcfc10f96e9b375fa3070a745f6cf25f6934f214f5fff068227)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MonitorDataCollectionRuleDataSourcesPrometheusForwarderLabelIncludeFilterOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa8cddf8bef9870024c205d956ef793f82c7bebd12e4af96a8987220628debd9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c274bb9584ee04f296539ee7142e838cfa7b15a5fa742a408b84a4e20c538a6a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab61b8e9711b1f55ef363b6b31f6f4a4af77b963fc349f5c3961557904af3e3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataSourcesPrometheusForwarderLabelIncludeFilter]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataSourcesPrometheusForwarderLabelIncludeFilter]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataSourcesPrometheusForwarderLabelIncludeFilter]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4c3589dfe654e9aa703f50de18eceb8b70bea8f99e4a7ba209e24ab50fd2f3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitorDataCollectionRuleDataSourcesPrometheusForwarderLabelIncludeFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDataSourcesPrometheusForwarderLabelIncludeFilterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab3e82b5634f904979adbdf991549be00bf8fe88f4583c97f5737b1ed6a8c35b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="labelInput")
    def label_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "labelInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="label")
    def label(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "label"))

    @label.setter
    def label(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a7ab249ce09b53f9f01c9151fd9f4f494b57cdaaacf94510b1cdf986e7425af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "label", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ac72bdac82b947a6a8f66e06085918c0031dcc03bf1879493aec32985dfc766)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleDataSourcesPrometheusForwarderLabelIncludeFilter]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleDataSourcesPrometheusForwarderLabelIncludeFilter]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleDataSourcesPrometheusForwarderLabelIncludeFilter]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a49ca3311e1a4a725d5eaa6af0b3cbfb1214f1bc6302f194676a3a9e1343a98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitorDataCollectionRuleDataSourcesPrometheusForwarderList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDataSourcesPrometheusForwarderList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__17b730ccb790ef3acafd2a5efc047bf288696d01fc22937ba669fa73c0363c5e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MonitorDataCollectionRuleDataSourcesPrometheusForwarderOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16e6e7f1ac10a26dc3dd99ddacf08e0a3c7d34fa31c371d297f8016bdc25c577)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MonitorDataCollectionRuleDataSourcesPrometheusForwarderOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c96b6423087db06a4c50fdfefb2a973ad90791e90612a33f16cdd65a5dec3f1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6dad2ba06b3ebb6259ffc9a6f1e388d5b91feb5f669b47e47b608dff692fe19b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__db1e4da8e54017aeb4105205d13f8f243ad056386d5926e4f4a118a2d5a07f5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataSourcesPrometheusForwarder]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataSourcesPrometheusForwarder]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataSourcesPrometheusForwarder]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd29ce9a04bc3da9f4cdc044ab4f84ea3c5c9293e7a66164f18e519ff472de2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitorDataCollectionRuleDataSourcesPrometheusForwarderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDataSourcesPrometheusForwarderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__74f944e46d0e8360e8d42d38f908006a4c6d9572e9cea4eed6a63e7f37f1bf52)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putLabelIncludeFilter")
    def put_label_include_filter(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorDataCollectionRuleDataSourcesPrometheusForwarderLabelIncludeFilter, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70b4d8667a809599de311da20fd4a3b58a317e9ba59aed6d3610fb76bd505f1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLabelIncludeFilter", [value]))

    @jsii.member(jsii_name="resetLabelIncludeFilter")
    def reset_label_include_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabelIncludeFilter", []))

    @builtins.property
    @jsii.member(jsii_name="labelIncludeFilter")
    def label_include_filter(
        self,
    ) -> MonitorDataCollectionRuleDataSourcesPrometheusForwarderLabelIncludeFilterList:
        return typing.cast(MonitorDataCollectionRuleDataSourcesPrometheusForwarderLabelIncludeFilterList, jsii.get(self, "labelIncludeFilter"))

    @builtins.property
    @jsii.member(jsii_name="labelIncludeFilterInput")
    def label_include_filter_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataSourcesPrometheusForwarderLabelIncludeFilter]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataSourcesPrometheusForwarderLabelIncludeFilter]]], jsii.get(self, "labelIncludeFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="streamsInput")
    def streams_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "streamsInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1422ea479ac5d9d4fd0dbd69a1a44c1a983fec6f10c66be730e81f1243bb78ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="streams")
    def streams(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "streams"))

    @streams.setter
    def streams(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__303875eb0d02e0550ce37a4015f792c57cc25fc32629705a1c77b38a1d882c42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "streams", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleDataSourcesPrometheusForwarder]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleDataSourcesPrometheusForwarder]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleDataSourcesPrometheusForwarder]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3177152f4b640aa9072f6d04d09e80e9a68d84fefbbab44ec637b8ac09aeaa53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDataSourcesSyslog",
    jsii_struct_bases=[],
    name_mapping={
        "facility_names": "facilityNames",
        "log_levels": "logLevels",
        "name": "name",
        "streams": "streams",
    },
)
class MonitorDataCollectionRuleDataSourcesSyslog:
    def __init__(
        self,
        *,
        facility_names: typing.Sequence[builtins.str],
        log_levels: typing.Sequence[builtins.str],
        name: builtins.str,
        streams: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param facility_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#facility_names MonitorDataCollectionRule#facility_names}.
        :param log_levels: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#log_levels MonitorDataCollectionRule#log_levels}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#name MonitorDataCollectionRule#name}.
        :param streams: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#streams MonitorDataCollectionRule#streams}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a9883e1ae6a4738a241f2d58c530f77392ebf28f4f8bcff16cbb35b180a87dd)
            check_type(argname="argument facility_names", value=facility_names, expected_type=type_hints["facility_names"])
            check_type(argname="argument log_levels", value=log_levels, expected_type=type_hints["log_levels"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument streams", value=streams, expected_type=type_hints["streams"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "facility_names": facility_names,
            "log_levels": log_levels,
            "name": name,
            "streams": streams,
        }

    @builtins.property
    def facility_names(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#facility_names MonitorDataCollectionRule#facility_names}.'''
        result = self._values.get("facility_names")
        assert result is not None, "Required property 'facility_names' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def log_levels(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#log_levels MonitorDataCollectionRule#log_levels}.'''
        result = self._values.get("log_levels")
        assert result is not None, "Required property 'log_levels' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#name MonitorDataCollectionRule#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def streams(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#streams MonitorDataCollectionRule#streams}.'''
        result = self._values.get("streams")
        assert result is not None, "Required property 'streams' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorDataCollectionRuleDataSourcesSyslog(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorDataCollectionRuleDataSourcesSyslogList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDataSourcesSyslogList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a8e065d90d2fec3a359cfa493fc108b40bb648980f2a7a10d7c41adcb8e342a2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MonitorDataCollectionRuleDataSourcesSyslogOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__775dd5444548e5ad93924f6b6bdb06546a96458eac1dff78ce4ffef60980db18)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MonitorDataCollectionRuleDataSourcesSyslogOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3b2257aad83009eff725de5a48a53bb4b36eb3f0fd2d008e6341c5caa217967)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b22a5544aea02741f55941d849ef70b86928957d176407217cf1c05e2b4ad316)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ac12af89411ebf126eaa86d93b12437625c0c61c2ef2ed78715fa965e45867a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataSourcesSyslog]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataSourcesSyslog]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataSourcesSyslog]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bf58e26d2249e71249170f53fc2737e098ad5207f6a76257b72d373a24f8862)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitorDataCollectionRuleDataSourcesSyslogOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDataSourcesSyslogOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9395de1dc772496048a16e5720bf172b0429024a22a8780da6d5625c4edffa3e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="facilityNamesInput")
    def facility_names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "facilityNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="logLevelsInput")
    def log_levels_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "logLevelsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="streamsInput")
    def streams_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "streamsInput"))

    @builtins.property
    @jsii.member(jsii_name="facilityNames")
    def facility_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "facilityNames"))

    @facility_names.setter
    def facility_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a710f9efe877b8c08037c0a7688d0c185fa2ad66c1420e68d86ebf9afee7e9f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "facilityNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logLevels")
    def log_levels(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "logLevels"))

    @log_levels.setter
    def log_levels(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b95687c2eec80398767496ad3cfa55696d9ea87e6425d0ed7691355e0ed6bc47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logLevels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__500fe805d28c61fcaacebf17058d8f615e949ced6a6cc55dfd9917bc41b9f381)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="streams")
    def streams(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "streams"))

    @streams.setter
    def streams(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c1cb242acfb5b9e07424d7ab71d87206676b08fd6ca1cc668c9daec918a93b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "streams", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleDataSourcesSyslog]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleDataSourcesSyslog]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleDataSourcesSyslog]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca36002b57f3acbd64630f68149f68bcde0363e4baa21d3592020407ece77b90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDataSourcesWindowsEventLog",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "streams": "streams",
        "x_path_queries": "xPathQueries",
    },
)
class MonitorDataCollectionRuleDataSourcesWindowsEventLog:
    def __init__(
        self,
        *,
        name: builtins.str,
        streams: typing.Sequence[builtins.str],
        x_path_queries: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#name MonitorDataCollectionRule#name}.
        :param streams: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#streams MonitorDataCollectionRule#streams}.
        :param x_path_queries: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#x_path_queries MonitorDataCollectionRule#x_path_queries}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b557f77d1831e36056c552a32db43c0d6da5fda2d3231c835178e51abd7925a)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument streams", value=streams, expected_type=type_hints["streams"])
            check_type(argname="argument x_path_queries", value=x_path_queries, expected_type=type_hints["x_path_queries"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "streams": streams,
            "x_path_queries": x_path_queries,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#name MonitorDataCollectionRule#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def streams(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#streams MonitorDataCollectionRule#streams}.'''
        result = self._values.get("streams")
        assert result is not None, "Required property 'streams' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def x_path_queries(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#x_path_queries MonitorDataCollectionRule#x_path_queries}.'''
        result = self._values.get("x_path_queries")
        assert result is not None, "Required property 'x_path_queries' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorDataCollectionRuleDataSourcesWindowsEventLog(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorDataCollectionRuleDataSourcesWindowsEventLogList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDataSourcesWindowsEventLogList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ec9a50ff2a5020e44702ba3ecf596a9339a8dc48b6fc4695018929d907f21f9f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MonitorDataCollectionRuleDataSourcesWindowsEventLogOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a625a4a1a6a1cf68036a2cbbc33e3af075a67ab10696572e1d5fa4cc84c1052)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MonitorDataCollectionRuleDataSourcesWindowsEventLogOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f9fa611d7edce38fd55b9b978596d636a49acd5037a6e226b599532c8e369b4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b27f75a278932276e72a3aefedcb4483e91634cebdcafff23762203e82469f8d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__84602f9219b96030b27dc26be68b3a66a004f24f7d1062ee5316a73753202e8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataSourcesWindowsEventLog]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataSourcesWindowsEventLog]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataSourcesWindowsEventLog]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8313d3809cc603a18a5c92cfb56366a1df14d027b50ea1a55acc65608409efe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitorDataCollectionRuleDataSourcesWindowsEventLogOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDataSourcesWindowsEventLogOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f0fb0e4b94355c0f9c3eb1acbc8271d1cffec0637dbbdc4546a4b2cf757e007)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="streamsInput")
    def streams_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "streamsInput"))

    @builtins.property
    @jsii.member(jsii_name="xPathQueriesInput")
    def x_path_queries_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "xPathQueriesInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e59ed61ddbff58dc840808382b8ddf1c2892676c422e0c949d21370e3de0a920)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="streams")
    def streams(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "streams"))

    @streams.setter
    def streams(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4e3a8eae68c25d444877c414cc6abda9d2d5cf268f00cc01e386619a37507e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "streams", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="xPathQueries")
    def x_path_queries(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "xPathQueries"))

    @x_path_queries.setter
    def x_path_queries(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f23cebcc2b2a793c46d90f5a53dbe34f3c4549cbee36bab023a947623238222)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "xPathQueries", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleDataSourcesWindowsEventLog]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleDataSourcesWindowsEventLog]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleDataSourcesWindowsEventLog]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41b0f67435549f47faad1238a8cd36c0a9404a47a886965b566e4967ba1a389c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDataSourcesWindowsFirewallLog",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "streams": "streams"},
)
class MonitorDataCollectionRuleDataSourcesWindowsFirewallLog:
    def __init__(
        self,
        *,
        name: builtins.str,
        streams: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#name MonitorDataCollectionRule#name}.
        :param streams: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#streams MonitorDataCollectionRule#streams}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1a1bd09b1a147bd26074ba3591ac31ffcf67a492a6f3dae379ae3e5a71d754e)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument streams", value=streams, expected_type=type_hints["streams"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "streams": streams,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#name MonitorDataCollectionRule#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def streams(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#streams MonitorDataCollectionRule#streams}.'''
        result = self._values.get("streams")
        assert result is not None, "Required property 'streams' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorDataCollectionRuleDataSourcesWindowsFirewallLog(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorDataCollectionRuleDataSourcesWindowsFirewallLogList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDataSourcesWindowsFirewallLogList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__613de7631942b3295fe2cd82a34fc560a6f5687f37f6ec4ec4089fa6c76bd9f7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MonitorDataCollectionRuleDataSourcesWindowsFirewallLogOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82e28b8cdd352ddeaf52c739818f620daf3eb1b82544609efe2c98e7da156a53)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MonitorDataCollectionRuleDataSourcesWindowsFirewallLogOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14cf0dcff3b1eea3b96519ade30dadc323a3bb398e94903c19c6a5fd244a0df3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eda2dbf53aaec196c5b45d6ef402760b30a33cdddd8f8a39cea80b0858fae0b1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef57cd82c9a2b0f14ddd2df1a7850c264e73921e9ccf131c2a95dba976e97143)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataSourcesWindowsFirewallLog]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataSourcesWindowsFirewallLog]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataSourcesWindowsFirewallLog]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0500c3d5b61211b1c71b49dfa0845a527ffe0d0bd3720df12148d8795ca525e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitorDataCollectionRuleDataSourcesWindowsFirewallLogOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDataSourcesWindowsFirewallLogOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b37a7787c1610e053182d4bd5ed868b58a83515b45edc30bd3cc451dbebca2b0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="streamsInput")
    def streams_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "streamsInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1707e9fdd31fd12f9de1730a95c4720b9e182585fb4ba56f34663b3383ce6bcc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="streams")
    def streams(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "streams"))

    @streams.setter
    def streams(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32690042f3ea13ccb446b4392a304bee6af6dba1ba46652e1e3c9b10102ee94f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "streams", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleDataSourcesWindowsFirewallLog]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleDataSourcesWindowsFirewallLog]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleDataSourcesWindowsFirewallLog]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7aaeb5e424b3ee0ee12a4597ffc004d1f138611e369216cfc8e6e58a690d2463)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDestinations",
    jsii_struct_bases=[],
    name_mapping={
        "azure_monitor_metrics": "azureMonitorMetrics",
        "event_hub": "eventHub",
        "event_hub_direct": "eventHubDirect",
        "log_analytics": "logAnalytics",
        "monitor_account": "monitorAccount",
        "storage_blob": "storageBlob",
        "storage_blob_direct": "storageBlobDirect",
        "storage_table_direct": "storageTableDirect",
    },
)
class MonitorDataCollectionRuleDestinations:
    def __init__(
        self,
        *,
        azure_monitor_metrics: typing.Optional[typing.Union["MonitorDataCollectionRuleDestinationsAzureMonitorMetrics", typing.Dict[builtins.str, typing.Any]]] = None,
        event_hub: typing.Optional[typing.Union["MonitorDataCollectionRuleDestinationsEventHub", typing.Dict[builtins.str, typing.Any]]] = None,
        event_hub_direct: typing.Optional[typing.Union["MonitorDataCollectionRuleDestinationsEventHubDirect", typing.Dict[builtins.str, typing.Any]]] = None,
        log_analytics: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorDataCollectionRuleDestinationsLogAnalytics", typing.Dict[builtins.str, typing.Any]]]]] = None,
        monitor_account: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorDataCollectionRuleDestinationsMonitorAccount", typing.Dict[builtins.str, typing.Any]]]]] = None,
        storage_blob: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorDataCollectionRuleDestinationsStorageBlob", typing.Dict[builtins.str, typing.Any]]]]] = None,
        storage_blob_direct: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorDataCollectionRuleDestinationsStorageBlobDirect", typing.Dict[builtins.str, typing.Any]]]]] = None,
        storage_table_direct: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorDataCollectionRuleDestinationsStorageTableDirect", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param azure_monitor_metrics: azure_monitor_metrics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#azure_monitor_metrics MonitorDataCollectionRule#azure_monitor_metrics}
        :param event_hub: event_hub block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#event_hub MonitorDataCollectionRule#event_hub}
        :param event_hub_direct: event_hub_direct block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#event_hub_direct MonitorDataCollectionRule#event_hub_direct}
        :param log_analytics: log_analytics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#log_analytics MonitorDataCollectionRule#log_analytics}
        :param monitor_account: monitor_account block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#monitor_account MonitorDataCollectionRule#monitor_account}
        :param storage_blob: storage_blob block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#storage_blob MonitorDataCollectionRule#storage_blob}
        :param storage_blob_direct: storage_blob_direct block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#storage_blob_direct MonitorDataCollectionRule#storage_blob_direct}
        :param storage_table_direct: storage_table_direct block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#storage_table_direct MonitorDataCollectionRule#storage_table_direct}
        '''
        if isinstance(azure_monitor_metrics, dict):
            azure_monitor_metrics = MonitorDataCollectionRuleDestinationsAzureMonitorMetrics(**azure_monitor_metrics)
        if isinstance(event_hub, dict):
            event_hub = MonitorDataCollectionRuleDestinationsEventHub(**event_hub)
        if isinstance(event_hub_direct, dict):
            event_hub_direct = MonitorDataCollectionRuleDestinationsEventHubDirect(**event_hub_direct)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91129a3b8459f9f9277e633acd1c0cba03afca8b282196aba60a2ffea57b91a8)
            check_type(argname="argument azure_monitor_metrics", value=azure_monitor_metrics, expected_type=type_hints["azure_monitor_metrics"])
            check_type(argname="argument event_hub", value=event_hub, expected_type=type_hints["event_hub"])
            check_type(argname="argument event_hub_direct", value=event_hub_direct, expected_type=type_hints["event_hub_direct"])
            check_type(argname="argument log_analytics", value=log_analytics, expected_type=type_hints["log_analytics"])
            check_type(argname="argument monitor_account", value=monitor_account, expected_type=type_hints["monitor_account"])
            check_type(argname="argument storage_blob", value=storage_blob, expected_type=type_hints["storage_blob"])
            check_type(argname="argument storage_blob_direct", value=storage_blob_direct, expected_type=type_hints["storage_blob_direct"])
            check_type(argname="argument storage_table_direct", value=storage_table_direct, expected_type=type_hints["storage_table_direct"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if azure_monitor_metrics is not None:
            self._values["azure_monitor_metrics"] = azure_monitor_metrics
        if event_hub is not None:
            self._values["event_hub"] = event_hub
        if event_hub_direct is not None:
            self._values["event_hub_direct"] = event_hub_direct
        if log_analytics is not None:
            self._values["log_analytics"] = log_analytics
        if monitor_account is not None:
            self._values["monitor_account"] = monitor_account
        if storage_blob is not None:
            self._values["storage_blob"] = storage_blob
        if storage_blob_direct is not None:
            self._values["storage_blob_direct"] = storage_blob_direct
        if storage_table_direct is not None:
            self._values["storage_table_direct"] = storage_table_direct

    @builtins.property
    def azure_monitor_metrics(
        self,
    ) -> typing.Optional["MonitorDataCollectionRuleDestinationsAzureMonitorMetrics"]:
        '''azure_monitor_metrics block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#azure_monitor_metrics MonitorDataCollectionRule#azure_monitor_metrics}
        '''
        result = self._values.get("azure_monitor_metrics")
        return typing.cast(typing.Optional["MonitorDataCollectionRuleDestinationsAzureMonitorMetrics"], result)

    @builtins.property
    def event_hub(
        self,
    ) -> typing.Optional["MonitorDataCollectionRuleDestinationsEventHub"]:
        '''event_hub block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#event_hub MonitorDataCollectionRule#event_hub}
        '''
        result = self._values.get("event_hub")
        return typing.cast(typing.Optional["MonitorDataCollectionRuleDestinationsEventHub"], result)

    @builtins.property
    def event_hub_direct(
        self,
    ) -> typing.Optional["MonitorDataCollectionRuleDestinationsEventHubDirect"]:
        '''event_hub_direct block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#event_hub_direct MonitorDataCollectionRule#event_hub_direct}
        '''
        result = self._values.get("event_hub_direct")
        return typing.cast(typing.Optional["MonitorDataCollectionRuleDestinationsEventHubDirect"], result)

    @builtins.property
    def log_analytics(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDestinationsLogAnalytics"]]]:
        '''log_analytics block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#log_analytics MonitorDataCollectionRule#log_analytics}
        '''
        result = self._values.get("log_analytics")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDestinationsLogAnalytics"]]], result)

    @builtins.property
    def monitor_account(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDestinationsMonitorAccount"]]]:
        '''monitor_account block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#monitor_account MonitorDataCollectionRule#monitor_account}
        '''
        result = self._values.get("monitor_account")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDestinationsMonitorAccount"]]], result)

    @builtins.property
    def storage_blob(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDestinationsStorageBlob"]]]:
        '''storage_blob block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#storage_blob MonitorDataCollectionRule#storage_blob}
        '''
        result = self._values.get("storage_blob")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDestinationsStorageBlob"]]], result)

    @builtins.property
    def storage_blob_direct(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDestinationsStorageBlobDirect"]]]:
        '''storage_blob_direct block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#storage_blob_direct MonitorDataCollectionRule#storage_blob_direct}
        '''
        result = self._values.get("storage_blob_direct")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDestinationsStorageBlobDirect"]]], result)

    @builtins.property
    def storage_table_direct(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDestinationsStorageTableDirect"]]]:
        '''storage_table_direct block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#storage_table_direct MonitorDataCollectionRule#storage_table_direct}
        '''
        result = self._values.get("storage_table_direct")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDestinationsStorageTableDirect"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorDataCollectionRuleDestinations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDestinationsAzureMonitorMetrics",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class MonitorDataCollectionRuleDestinationsAzureMonitorMetrics:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#name MonitorDataCollectionRule#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34ecd0556ab897ecc2bca1b5401b8dbd4d672f663daadc537150dba8b8f4fb70)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#name MonitorDataCollectionRule#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorDataCollectionRuleDestinationsAzureMonitorMetrics(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorDataCollectionRuleDestinationsAzureMonitorMetricsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDestinationsAzureMonitorMetricsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9057f9db833800d87a63b1df8170af107ad8c20affb98d66be4da94182eb044a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4a0a0ceb07c7ec885a3ac5d79b0833b8caa3d739dd8be4eecf59962a9c29a10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitorDataCollectionRuleDestinationsAzureMonitorMetrics]:
        return typing.cast(typing.Optional[MonitorDataCollectionRuleDestinationsAzureMonitorMetrics], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorDataCollectionRuleDestinationsAzureMonitorMetrics],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd026bc0ea172c4e759b319b66699e7648ed57e390d431db5a417465a0b767a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDestinationsEventHub",
    jsii_struct_bases=[],
    name_mapping={"event_hub_id": "eventHubId", "name": "name"},
)
class MonitorDataCollectionRuleDestinationsEventHub:
    def __init__(self, *, event_hub_id: builtins.str, name: builtins.str) -> None:
        '''
        :param event_hub_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#event_hub_id MonitorDataCollectionRule#event_hub_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#name MonitorDataCollectionRule#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__160d234c5efb98e7d7aaf8fff166cf2501f5f0da4e0369fa0331cb69400f804b)
            check_type(argname="argument event_hub_id", value=event_hub_id, expected_type=type_hints["event_hub_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "event_hub_id": event_hub_id,
            "name": name,
        }

    @builtins.property
    def event_hub_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#event_hub_id MonitorDataCollectionRule#event_hub_id}.'''
        result = self._values.get("event_hub_id")
        assert result is not None, "Required property 'event_hub_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#name MonitorDataCollectionRule#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorDataCollectionRuleDestinationsEventHub(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDestinationsEventHubDirect",
    jsii_struct_bases=[],
    name_mapping={"event_hub_id": "eventHubId", "name": "name"},
)
class MonitorDataCollectionRuleDestinationsEventHubDirect:
    def __init__(self, *, event_hub_id: builtins.str, name: builtins.str) -> None:
        '''
        :param event_hub_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#event_hub_id MonitorDataCollectionRule#event_hub_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#name MonitorDataCollectionRule#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c230c5f49687b4cccd1f72d1306f6771230a133b3d8fedbf9b3091cbf8e020d)
            check_type(argname="argument event_hub_id", value=event_hub_id, expected_type=type_hints["event_hub_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "event_hub_id": event_hub_id,
            "name": name,
        }

    @builtins.property
    def event_hub_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#event_hub_id MonitorDataCollectionRule#event_hub_id}.'''
        result = self._values.get("event_hub_id")
        assert result is not None, "Required property 'event_hub_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#name MonitorDataCollectionRule#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorDataCollectionRuleDestinationsEventHubDirect(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorDataCollectionRuleDestinationsEventHubDirectOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDestinationsEventHubDirectOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__26533ecd7410f95ecddf5b352a8f5795bb40af2d387718041f5bbaf431bac56b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="eventHubIdInput")
    def event_hub_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventHubIdInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="eventHubId")
    def event_hub_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventHubId"))

    @event_hub_id.setter
    def event_hub_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd583406bbb530e86aaa46cbf72ce344b0ed8753b6815f83b5b2b5c780368d88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventHubId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d68c4b0157dbf2a9e8349a16acd59779316296814282f580b387912424bed271)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitorDataCollectionRuleDestinationsEventHubDirect]:
        return typing.cast(typing.Optional[MonitorDataCollectionRuleDestinationsEventHubDirect], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorDataCollectionRuleDestinationsEventHubDirect],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9853d165c79cedb400075b022dd67011c74bf6314681cfbcfadbf3c444934a37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitorDataCollectionRuleDestinationsEventHubOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDestinationsEventHubOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c9cfb57eddc8c11ae96b69b9e1ef5e27251765f4f6f390828c7f7e168ff3b04)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="eventHubIdInput")
    def event_hub_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventHubIdInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="eventHubId")
    def event_hub_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventHubId"))

    @event_hub_id.setter
    def event_hub_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffd209adc5f4d36db698e02874baa297726524bf45773526b85a36c7eb8fe3b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventHubId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fa7b2ad4fd2a505c27c86dba2e107d9698b55030205f9737a63cb9618831458)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitorDataCollectionRuleDestinationsEventHub]:
        return typing.cast(typing.Optional[MonitorDataCollectionRuleDestinationsEventHub], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorDataCollectionRuleDestinationsEventHub],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0347098749d1808cf452d8b76755b08a11bd47d27cec485c36488b977acfcaa2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDestinationsLogAnalytics",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "workspace_resource_id": "workspaceResourceId"},
)
class MonitorDataCollectionRuleDestinationsLogAnalytics:
    def __init__(
        self,
        *,
        name: builtins.str,
        workspace_resource_id: builtins.str,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#name MonitorDataCollectionRule#name}.
        :param workspace_resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#workspace_resource_id MonitorDataCollectionRule#workspace_resource_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__251443bc66028e9ec47bb10d9c703e7b79fd9cb49a3de69a82c29a7adf08508d)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument workspace_resource_id", value=workspace_resource_id, expected_type=type_hints["workspace_resource_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "workspace_resource_id": workspace_resource_id,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#name MonitorDataCollectionRule#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def workspace_resource_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#workspace_resource_id MonitorDataCollectionRule#workspace_resource_id}.'''
        result = self._values.get("workspace_resource_id")
        assert result is not None, "Required property 'workspace_resource_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorDataCollectionRuleDestinationsLogAnalytics(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorDataCollectionRuleDestinationsLogAnalyticsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDestinationsLogAnalyticsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b910654ddfca9e344e8141acb1abb600e90077de18e9650337a717855d8d624)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MonitorDataCollectionRuleDestinationsLogAnalyticsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63e8cb24e7b3a3be4c78abe3061cb2287e98ba7aa0554fcc0bc3e3ad43b25a50)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MonitorDataCollectionRuleDestinationsLogAnalyticsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__731f1b46222b14adf5de13fc4bd639cb53277f8c38ae139bf3c633796136e89a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3a9bd5eb5e4e75e12f759e050b6048ec228cbdb3328abf91ef53311f1ce2c44)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f959ef7c4c4d4bd72b60c4d4bd883b10c7bb28a6131fe871b7626b4963e14b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDestinationsLogAnalytics]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDestinationsLogAnalytics]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDestinationsLogAnalytics]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__616fd31921bf88f0d3165cee51b4f976c64c556905fe55727a70ccf6ad9a45bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitorDataCollectionRuleDestinationsLogAnalyticsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDestinationsLogAnalyticsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d98f91803fead56e4f1ba854b066930a45e6c7e6e91b8502163107c55ac6e11)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="workspaceResourceIdInput")
    def workspace_resource_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workspaceResourceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc1ccb4def4da1177ca948eefc1199d7f4cd2ea3886594f89878527bc679f01f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workspaceResourceId")
    def workspace_resource_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workspaceResourceId"))

    @workspace_resource_id.setter
    def workspace_resource_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dea27ca99d63e43e6b0aa930b3ebbf5767b9ec3af80e50e6ea7f25059c0014b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workspaceResourceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleDestinationsLogAnalytics]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleDestinationsLogAnalytics]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleDestinationsLogAnalytics]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__818948068c75dcae789dd04d74629d38a8c8c7d00b4382e6015b7fd035227055)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDestinationsMonitorAccount",
    jsii_struct_bases=[],
    name_mapping={"monitor_account_id": "monitorAccountId", "name": "name"},
)
class MonitorDataCollectionRuleDestinationsMonitorAccount:
    def __init__(self, *, monitor_account_id: builtins.str, name: builtins.str) -> None:
        '''
        :param monitor_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#monitor_account_id MonitorDataCollectionRule#monitor_account_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#name MonitorDataCollectionRule#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5b78cb44e678c95f8c57a8899b455f3f9c8bf41c58a6075812fd133343a3925)
            check_type(argname="argument monitor_account_id", value=monitor_account_id, expected_type=type_hints["monitor_account_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "monitor_account_id": monitor_account_id,
            "name": name,
        }

    @builtins.property
    def monitor_account_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#monitor_account_id MonitorDataCollectionRule#monitor_account_id}.'''
        result = self._values.get("monitor_account_id")
        assert result is not None, "Required property 'monitor_account_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#name MonitorDataCollectionRule#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorDataCollectionRuleDestinationsMonitorAccount(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorDataCollectionRuleDestinationsMonitorAccountList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDestinationsMonitorAccountList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f175c3b6717c542a224787b5b2cf8c565cc037df0838fb3806bccaff5df40bf4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MonitorDataCollectionRuleDestinationsMonitorAccountOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eed958ab0f9a61e88839ec16c6aa0d47f02c45f039858a89c4c665d5c2c58f01)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MonitorDataCollectionRuleDestinationsMonitorAccountOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61c65298fa12f0d2264b24757a2e9fb6cb2c426a824b87316a990a1b00619d80)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2034dce92e800f4802cd76f29670ef36023f5fb25bffd0ca2c0d2bcffc2fa7e8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c1ccd450e69cd0267425454375e567c1e0a3b10ad65fd71823ec51a4ddcb92c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDestinationsMonitorAccount]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDestinationsMonitorAccount]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDestinationsMonitorAccount]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0e560068e9761ad15cd30ddaf3b8f3824bfb6cc2a1367a6b2ede026d813ade1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitorDataCollectionRuleDestinationsMonitorAccountOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDestinationsMonitorAccountOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9bfa1609570e37c05da2cc1e4b2d7f32d5438e334c3fb54049bc0d938517dba1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="monitorAccountIdInput")
    def monitor_account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "monitorAccountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="monitorAccountId")
    def monitor_account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "monitorAccountId"))

    @monitor_account_id.setter
    def monitor_account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f19fd9d9353226cadd39167ce025a6e6c6b0be1d9f0af80f4eeff22e82b7e9ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "monitorAccountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12b1a388d0f71574bd5181bfbc4b72121818bdf4840ff3ac497f00ca11123200)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleDestinationsMonitorAccount]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleDestinationsMonitorAccount]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleDestinationsMonitorAccount]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6fcdf9f53f6c6a19cec0de7b063182ce437c3cbb639c4b6b9c4ae5149996ead)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitorDataCollectionRuleDestinationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDestinationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__02c782f684d157afde64540324f5f82e0b0f863ad3b1dc23c61fd2fcc72643d4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAzureMonitorMetrics")
    def put_azure_monitor_metrics(self, *, name: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#name MonitorDataCollectionRule#name}.
        '''
        value = MonitorDataCollectionRuleDestinationsAzureMonitorMetrics(name=name)

        return typing.cast(None, jsii.invoke(self, "putAzureMonitorMetrics", [value]))

    @jsii.member(jsii_name="putEventHub")
    def put_event_hub(self, *, event_hub_id: builtins.str, name: builtins.str) -> None:
        '''
        :param event_hub_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#event_hub_id MonitorDataCollectionRule#event_hub_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#name MonitorDataCollectionRule#name}.
        '''
        value = MonitorDataCollectionRuleDestinationsEventHub(
            event_hub_id=event_hub_id, name=name
        )

        return typing.cast(None, jsii.invoke(self, "putEventHub", [value]))

    @jsii.member(jsii_name="putEventHubDirect")
    def put_event_hub_direct(
        self,
        *,
        event_hub_id: builtins.str,
        name: builtins.str,
    ) -> None:
        '''
        :param event_hub_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#event_hub_id MonitorDataCollectionRule#event_hub_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#name MonitorDataCollectionRule#name}.
        '''
        value = MonitorDataCollectionRuleDestinationsEventHubDirect(
            event_hub_id=event_hub_id, name=name
        )

        return typing.cast(None, jsii.invoke(self, "putEventHubDirect", [value]))

    @jsii.member(jsii_name="putLogAnalytics")
    def put_log_analytics(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorDataCollectionRuleDestinationsLogAnalytics, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b415fe73dab62431fb7a05f0e71fec2d04de47a0db07fa94d8980ccc2497326e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLogAnalytics", [value]))

    @jsii.member(jsii_name="putMonitorAccount")
    def put_monitor_account(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorDataCollectionRuleDestinationsMonitorAccount, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f921b93ba934429c76fd4a832a05d7fac685b14ef4be389ca07cafcd49ab37cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMonitorAccount", [value]))

    @jsii.member(jsii_name="putStorageBlob")
    def put_storage_blob(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorDataCollectionRuleDestinationsStorageBlob", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67efb94f39d4bb0542b9586e38b4c1758a6083c3f68b4e1a6f3addd77b0bd7f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putStorageBlob", [value]))

    @jsii.member(jsii_name="putStorageBlobDirect")
    def put_storage_blob_direct(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorDataCollectionRuleDestinationsStorageBlobDirect", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__075eeef1eebd0b23821cbf78acc145806a0a7bf4f064270a59d5e50b3f820dbf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putStorageBlobDirect", [value]))

    @jsii.member(jsii_name="putStorageTableDirect")
    def put_storage_table_direct(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorDataCollectionRuleDestinationsStorageTableDirect", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3294acaa45b376647b138d9274c746c9a2746fe54246b661ed4da9c57476258d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putStorageTableDirect", [value]))

    @jsii.member(jsii_name="resetAzureMonitorMetrics")
    def reset_azure_monitor_metrics(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAzureMonitorMetrics", []))

    @jsii.member(jsii_name="resetEventHub")
    def reset_event_hub(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventHub", []))

    @jsii.member(jsii_name="resetEventHubDirect")
    def reset_event_hub_direct(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventHubDirect", []))

    @jsii.member(jsii_name="resetLogAnalytics")
    def reset_log_analytics(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogAnalytics", []))

    @jsii.member(jsii_name="resetMonitorAccount")
    def reset_monitor_account(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonitorAccount", []))

    @jsii.member(jsii_name="resetStorageBlob")
    def reset_storage_blob(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageBlob", []))

    @jsii.member(jsii_name="resetStorageBlobDirect")
    def reset_storage_blob_direct(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageBlobDirect", []))

    @jsii.member(jsii_name="resetStorageTableDirect")
    def reset_storage_table_direct(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageTableDirect", []))

    @builtins.property
    @jsii.member(jsii_name="azureMonitorMetrics")
    def azure_monitor_metrics(
        self,
    ) -> MonitorDataCollectionRuleDestinationsAzureMonitorMetricsOutputReference:
        return typing.cast(MonitorDataCollectionRuleDestinationsAzureMonitorMetricsOutputReference, jsii.get(self, "azureMonitorMetrics"))

    @builtins.property
    @jsii.member(jsii_name="eventHub")
    def event_hub(self) -> MonitorDataCollectionRuleDestinationsEventHubOutputReference:
        return typing.cast(MonitorDataCollectionRuleDestinationsEventHubOutputReference, jsii.get(self, "eventHub"))

    @builtins.property
    @jsii.member(jsii_name="eventHubDirect")
    def event_hub_direct(
        self,
    ) -> MonitorDataCollectionRuleDestinationsEventHubDirectOutputReference:
        return typing.cast(MonitorDataCollectionRuleDestinationsEventHubDirectOutputReference, jsii.get(self, "eventHubDirect"))

    @builtins.property
    @jsii.member(jsii_name="logAnalytics")
    def log_analytics(self) -> MonitorDataCollectionRuleDestinationsLogAnalyticsList:
        return typing.cast(MonitorDataCollectionRuleDestinationsLogAnalyticsList, jsii.get(self, "logAnalytics"))

    @builtins.property
    @jsii.member(jsii_name="monitorAccount")
    def monitor_account(
        self,
    ) -> MonitorDataCollectionRuleDestinationsMonitorAccountList:
        return typing.cast(MonitorDataCollectionRuleDestinationsMonitorAccountList, jsii.get(self, "monitorAccount"))

    @builtins.property
    @jsii.member(jsii_name="storageBlob")
    def storage_blob(self) -> "MonitorDataCollectionRuleDestinationsStorageBlobList":
        return typing.cast("MonitorDataCollectionRuleDestinationsStorageBlobList", jsii.get(self, "storageBlob"))

    @builtins.property
    @jsii.member(jsii_name="storageBlobDirect")
    def storage_blob_direct(
        self,
    ) -> "MonitorDataCollectionRuleDestinationsStorageBlobDirectList":
        return typing.cast("MonitorDataCollectionRuleDestinationsStorageBlobDirectList", jsii.get(self, "storageBlobDirect"))

    @builtins.property
    @jsii.member(jsii_name="storageTableDirect")
    def storage_table_direct(
        self,
    ) -> "MonitorDataCollectionRuleDestinationsStorageTableDirectList":
        return typing.cast("MonitorDataCollectionRuleDestinationsStorageTableDirectList", jsii.get(self, "storageTableDirect"))

    @builtins.property
    @jsii.member(jsii_name="azureMonitorMetricsInput")
    def azure_monitor_metrics_input(
        self,
    ) -> typing.Optional[MonitorDataCollectionRuleDestinationsAzureMonitorMetrics]:
        return typing.cast(typing.Optional[MonitorDataCollectionRuleDestinationsAzureMonitorMetrics], jsii.get(self, "azureMonitorMetricsInput"))

    @builtins.property
    @jsii.member(jsii_name="eventHubDirectInput")
    def event_hub_direct_input(
        self,
    ) -> typing.Optional[MonitorDataCollectionRuleDestinationsEventHubDirect]:
        return typing.cast(typing.Optional[MonitorDataCollectionRuleDestinationsEventHubDirect], jsii.get(self, "eventHubDirectInput"))

    @builtins.property
    @jsii.member(jsii_name="eventHubInput")
    def event_hub_input(
        self,
    ) -> typing.Optional[MonitorDataCollectionRuleDestinationsEventHub]:
        return typing.cast(typing.Optional[MonitorDataCollectionRuleDestinationsEventHub], jsii.get(self, "eventHubInput"))

    @builtins.property
    @jsii.member(jsii_name="logAnalyticsInput")
    def log_analytics_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDestinationsLogAnalytics]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDestinationsLogAnalytics]]], jsii.get(self, "logAnalyticsInput"))

    @builtins.property
    @jsii.member(jsii_name="monitorAccountInput")
    def monitor_account_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDestinationsMonitorAccount]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDestinationsMonitorAccount]]], jsii.get(self, "monitorAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="storageBlobDirectInput")
    def storage_blob_direct_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDestinationsStorageBlobDirect"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDestinationsStorageBlobDirect"]]], jsii.get(self, "storageBlobDirectInput"))

    @builtins.property
    @jsii.member(jsii_name="storageBlobInput")
    def storage_blob_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDestinationsStorageBlob"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDestinationsStorageBlob"]]], jsii.get(self, "storageBlobInput"))

    @builtins.property
    @jsii.member(jsii_name="storageTableDirectInput")
    def storage_table_direct_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDestinationsStorageTableDirect"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDestinationsStorageTableDirect"]]], jsii.get(self, "storageTableDirectInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MonitorDataCollectionRuleDestinations]:
        return typing.cast(typing.Optional[MonitorDataCollectionRuleDestinations], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorDataCollectionRuleDestinations],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e09f04e010ada32c12dc4384179d3061aaa449ccbbbf9e0972c668346135b13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDestinationsStorageBlob",
    jsii_struct_bases=[],
    name_mapping={
        "container_name": "containerName",
        "name": "name",
        "storage_account_id": "storageAccountId",
    },
)
class MonitorDataCollectionRuleDestinationsStorageBlob:
    def __init__(
        self,
        *,
        container_name: builtins.str,
        name: builtins.str,
        storage_account_id: builtins.str,
    ) -> None:
        '''
        :param container_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#container_name MonitorDataCollectionRule#container_name}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#name MonitorDataCollectionRule#name}.
        :param storage_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#storage_account_id MonitorDataCollectionRule#storage_account_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0a5cd93e054aaea4539bb66d675d50c1803bf406ca6a6f7a07181f782b37295)
            check_type(argname="argument container_name", value=container_name, expected_type=type_hints["container_name"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument storage_account_id", value=storage_account_id, expected_type=type_hints["storage_account_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "container_name": container_name,
            "name": name,
            "storage_account_id": storage_account_id,
        }

    @builtins.property
    def container_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#container_name MonitorDataCollectionRule#container_name}.'''
        result = self._values.get("container_name")
        assert result is not None, "Required property 'container_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#name MonitorDataCollectionRule#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_account_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#storage_account_id MonitorDataCollectionRule#storage_account_id}.'''
        result = self._values.get("storage_account_id")
        assert result is not None, "Required property 'storage_account_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorDataCollectionRuleDestinationsStorageBlob(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDestinationsStorageBlobDirect",
    jsii_struct_bases=[],
    name_mapping={
        "container_name": "containerName",
        "name": "name",
        "storage_account_id": "storageAccountId",
    },
)
class MonitorDataCollectionRuleDestinationsStorageBlobDirect:
    def __init__(
        self,
        *,
        container_name: builtins.str,
        name: builtins.str,
        storage_account_id: builtins.str,
    ) -> None:
        '''
        :param container_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#container_name MonitorDataCollectionRule#container_name}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#name MonitorDataCollectionRule#name}.
        :param storage_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#storage_account_id MonitorDataCollectionRule#storage_account_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ea149d212a8d21c3ff325f26906453d1f8660d65ce442c890906f81651658a7)
            check_type(argname="argument container_name", value=container_name, expected_type=type_hints["container_name"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument storage_account_id", value=storage_account_id, expected_type=type_hints["storage_account_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "container_name": container_name,
            "name": name,
            "storage_account_id": storage_account_id,
        }

    @builtins.property
    def container_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#container_name MonitorDataCollectionRule#container_name}.'''
        result = self._values.get("container_name")
        assert result is not None, "Required property 'container_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#name MonitorDataCollectionRule#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_account_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#storage_account_id MonitorDataCollectionRule#storage_account_id}.'''
        result = self._values.get("storage_account_id")
        assert result is not None, "Required property 'storage_account_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorDataCollectionRuleDestinationsStorageBlobDirect(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorDataCollectionRuleDestinationsStorageBlobDirectList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDestinationsStorageBlobDirectList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8021273c42b466f9f3b97486baf27f9585bf6c4de0a6baac46e1bae6140165bd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MonitorDataCollectionRuleDestinationsStorageBlobDirectOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__256a548052790ed4f3ba2333f964f1786b08cb5d2ea755a26be30cac970b1e00)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MonitorDataCollectionRuleDestinationsStorageBlobDirectOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d370873594fde043fdc531fccf13ce4ce14656a60bb4e3a51a33b70fca1db53a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__df8161d495d10aef9ad291757083cd8408558cfae0fca6ad95755c04648afe74)
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
            type_hints = typing.get_type_hints(_typecheckingstub__59d4ceb5911760df7d6ba2a6c028422e5fbe9422313763e64777558c2cd6f35f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDestinationsStorageBlobDirect]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDestinationsStorageBlobDirect]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDestinationsStorageBlobDirect]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1daf7485596c215fcb5147b894da0d38632c13b8bc56029c227e22edbad3227f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitorDataCollectionRuleDestinationsStorageBlobDirectOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDestinationsStorageBlobDirectOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f082bcc46470e3378cf2165764ae72f1e36c0aa362d89b9c6f82543a0c73684d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="containerNameInput")
    def container_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "containerNameInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="storageAccountIdInput")
    def storage_account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageAccountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="containerName")
    def container_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "containerName"))

    @container_name.setter
    def container_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__662518c759cc7ad79cbad2ef8ef4708d4dd14b74cec2480af699d3308db490c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0434e1b4afc017abde4df13076b1c3e12969bb7e2ab85471b7d28b626b304cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageAccountId")
    def storage_account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageAccountId"))

    @storage_account_id.setter
    def storage_account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f28668130b226b67833a2889a291936ec0ad9ebc39d25b0f1299a346b0e69b0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageAccountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleDestinationsStorageBlobDirect]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleDestinationsStorageBlobDirect]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleDestinationsStorageBlobDirect]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a185a22b5e1efeed207b2ebca2dfe8d331a067038826058bb6b10dc885f5a24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitorDataCollectionRuleDestinationsStorageBlobList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDestinationsStorageBlobList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__68fe61b60734786501aaa0c3117c25108924ae24a2d2895c2ba83a58f39a524e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MonitorDataCollectionRuleDestinationsStorageBlobOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1136790942ae95df619a710fe1f41d3f8762ab48b6b539ddac0f0780fe88eb49)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MonitorDataCollectionRuleDestinationsStorageBlobOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ca283d159ffce95ea2dbd901c8028d4c83aa9d3e0b32a7c7dea1259a884b7a0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__259aeb9002ac21aa419f5e0afae8b376b39171a8b189138821aee99b7bbe2903)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf3485fa18f0fe3814dd6640dfe811abbf51845cd6d10f729e035dfede36ca38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDestinationsStorageBlob]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDestinationsStorageBlob]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDestinationsStorageBlob]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02560b930034fec2c8feece69505ece6abaca0e826e1ea678ca2361429355e4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitorDataCollectionRuleDestinationsStorageBlobOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDestinationsStorageBlobOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__850765f4ae3f14d5edef7dfff2c7d71d31285328ef9bd89049198b3e85173cfe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="containerNameInput")
    def container_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "containerNameInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="storageAccountIdInput")
    def storage_account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageAccountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="containerName")
    def container_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "containerName"))

    @container_name.setter
    def container_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3258d9bf93fd56f5b401b320354ab9f7b2afcabf71680ba3a47093c9c81aa73a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2480828729c567fc8f6611a9675db3d625035a46ba281af51d649dde7fcbf900)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageAccountId")
    def storage_account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageAccountId"))

    @storage_account_id.setter
    def storage_account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__475c5218e654a18a322219c2104ec972b9f9165c793d2aa9dd570578d5e2a786)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageAccountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleDestinationsStorageBlob]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleDestinationsStorageBlob]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleDestinationsStorageBlob]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0bfeb3d337ff74cb52689e3176ac77cbf2695bf8fa4499e1ed94912ae844d2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDestinationsStorageTableDirect",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "storage_account_id": "storageAccountId",
        "table_name": "tableName",
    },
)
class MonitorDataCollectionRuleDestinationsStorageTableDirect:
    def __init__(
        self,
        *,
        name: builtins.str,
        storage_account_id: builtins.str,
        table_name: builtins.str,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#name MonitorDataCollectionRule#name}.
        :param storage_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#storage_account_id MonitorDataCollectionRule#storage_account_id}.
        :param table_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#table_name MonitorDataCollectionRule#table_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3b1e4f45317733b74c17366e09ec07f8540e18690d0f7d878c8db7017f1ea6d)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument storage_account_id", value=storage_account_id, expected_type=type_hints["storage_account_id"])
            check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "storage_account_id": storage_account_id,
            "table_name": table_name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#name MonitorDataCollectionRule#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_account_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#storage_account_id MonitorDataCollectionRule#storage_account_id}.'''
        result = self._values.get("storage_account_id")
        assert result is not None, "Required property 'storage_account_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def table_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#table_name MonitorDataCollectionRule#table_name}.'''
        result = self._values.get("table_name")
        assert result is not None, "Required property 'table_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorDataCollectionRuleDestinationsStorageTableDirect(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorDataCollectionRuleDestinationsStorageTableDirectList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDestinationsStorageTableDirectList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f8690fe76bc211d9fc83f28783bc83135a377c4c505dc634d3b06b793af6e91)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MonitorDataCollectionRuleDestinationsStorageTableDirectOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef5c3d6d0eb8f5dd4234823dfb0324d487606f4ae2c92f9a0d52ee19f6a97ef9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MonitorDataCollectionRuleDestinationsStorageTableDirectOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36d3047a81c34b65bedf1bfba7469161cf31e68274b667c4882eb27351fec4ef)
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
            type_hints = typing.get_type_hints(_typecheckingstub__65ac47afb175997fe3c17c507ea5cc2b3d71abfa593866c9a6a5cc9736400911)
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
            type_hints = typing.get_type_hints(_typecheckingstub__37c63be88b5cb5cbf1d953d2a826e19965087b6934fb9602337e1e09a53eaf50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDestinationsStorageTableDirect]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDestinationsStorageTableDirect]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDestinationsStorageTableDirect]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__443e4388d566cf2100e2e2a612d3a75d9596c88dd08ea2ba2e33b47791fec601)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitorDataCollectionRuleDestinationsStorageTableDirectOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDestinationsStorageTableDirectOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5545279f07c7facd5e3d8f06af970a93d16a0d698b612858fbba584a6fc867b0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="storageAccountIdInput")
    def storage_account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageAccountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="tableNameInput")
    def table_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableNameInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66e48dd877d1d09bf673596d01ff6502326ac957dfa945d6631bcbaffe59e15e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageAccountId")
    def storage_account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageAccountId"))

    @storage_account_id.setter
    def storage_account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcc0e35739403f0d9c9b8de299cd7fd76f6282b76e6f4129a6f467595ecfe5a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageAccountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tableName")
    def table_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tableName"))

    @table_name.setter
    def table_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5b674a36d32ce7138e260f5b5a9df5a5765812a9dbb9c4e0b58803dba4af617)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tableName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleDestinationsStorageTableDirect]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleDestinationsStorageTableDirect]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleDestinationsStorageTableDirect]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed6f9b13b7b399f0439eb206144030f2592a59988408888ce51d2a31cf4fcc13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleIdentity",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "identity_ids": "identityIds"},
)
class MonitorDataCollectionRuleIdentity:
    def __init__(
        self,
        *,
        type: builtins.str,
        identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#type MonitorDataCollectionRule#type}.
        :param identity_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#identity_ids MonitorDataCollectionRule#identity_ids}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f650c265237317561bc2dfa71cf72f7201660e1f4242f9607a25f5788d6c02d)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument identity_ids", value=identity_ids, expected_type=type_hints["identity_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if identity_ids is not None:
            self._values["identity_ids"] = identity_ids

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#type MonitorDataCollectionRule#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def identity_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#identity_ids MonitorDataCollectionRule#identity_ids}.'''
        result = self._values.get("identity_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorDataCollectionRuleIdentity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorDataCollectionRuleIdentityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleIdentityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b3da5b97412e8737e5243674a917c40fda8601f51e0e7648c14cb25687c0f3c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIdentityIds")
    def reset_identity_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentityIds", []))

    @builtins.property
    @jsii.member(jsii_name="principalId")
    def principal_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "principalId"))

    @builtins.property
    @jsii.member(jsii_name="tenantId")
    def tenant_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tenantId"))

    @builtins.property
    @jsii.member(jsii_name="identityIdsInput")
    def identity_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "identityIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="identityIds")
    def identity_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "identityIds"))

    @identity_ids.setter
    def identity_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3853531074b63b3f75574c3b5e12635a5bd67ea0343cac7402fb87ac8675dc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fc45c3025797d8bf5347222063c2f63a1e057866b80b3eb7d0bb0f8e79b9435)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MonitorDataCollectionRuleIdentity]:
        return typing.cast(typing.Optional[MonitorDataCollectionRuleIdentity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorDataCollectionRuleIdentity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82792bb2f9b81393dc25a536b8cfd81c8c58dc64040c4316d8a59ab1923ae764)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleStreamDeclaration",
    jsii_struct_bases=[],
    name_mapping={"column": "column", "stream_name": "streamName"},
)
class MonitorDataCollectionRuleStreamDeclaration:
    def __init__(
        self,
        *,
        column: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorDataCollectionRuleStreamDeclarationColumn", typing.Dict[builtins.str, typing.Any]]]],
        stream_name: builtins.str,
    ) -> None:
        '''
        :param column: column block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#column MonitorDataCollectionRule#column}
        :param stream_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#stream_name MonitorDataCollectionRule#stream_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4937c7273ee18bf0afd4efd6156584107b2e8dabda3e2c4b92f75e52942618eb)
            check_type(argname="argument column", value=column, expected_type=type_hints["column"])
            check_type(argname="argument stream_name", value=stream_name, expected_type=type_hints["stream_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "column": column,
            "stream_name": stream_name,
        }

    @builtins.property
    def column(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleStreamDeclarationColumn"]]:
        '''column block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#column MonitorDataCollectionRule#column}
        '''
        result = self._values.get("column")
        assert result is not None, "Required property 'column' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleStreamDeclarationColumn"]], result)

    @builtins.property
    def stream_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#stream_name MonitorDataCollectionRule#stream_name}.'''
        result = self._values.get("stream_name")
        assert result is not None, "Required property 'stream_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorDataCollectionRuleStreamDeclaration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleStreamDeclarationColumn",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "type": "type"},
)
class MonitorDataCollectionRuleStreamDeclarationColumn:
    def __init__(self, *, name: builtins.str, type: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#name MonitorDataCollectionRule#name}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#type MonitorDataCollectionRule#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66fec215009ed2ba77089c862d175dbd4183192a14ff4c2595f13ace96eae357)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "type": type,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#name MonitorDataCollectionRule#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#type MonitorDataCollectionRule#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorDataCollectionRuleStreamDeclarationColumn(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorDataCollectionRuleStreamDeclarationColumnList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleStreamDeclarationColumnList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__58867fe18fe48c7cd7a7bdce907732a72947f2ee9fe27d3e5eaae3087fd159b7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MonitorDataCollectionRuleStreamDeclarationColumnOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__737f37b7baa90d66f5b4017371a14b24d11d0db14e15b9ea763ced3b94475e62)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MonitorDataCollectionRuleStreamDeclarationColumnOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bd672935853ed7684ec14a9d2846e8d90a47711ae1672d127c07fa50a85f5f2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c2b9f8bfa03a826ad0ad0778127f7c39758246cd0aaebb52442eb5d6367f512)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6dac1468c5c654bcad8d1ad576a91c4277414e351ffe68885e13ac8720e35ff0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleStreamDeclarationColumn]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleStreamDeclarationColumn]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleStreamDeclarationColumn]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__631c4f4b007a17e89688605541745b46d9dacb3afb03f8239bd3627422926a26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitorDataCollectionRuleStreamDeclarationColumnOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleStreamDeclarationColumnOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__15d899d3099b04a3c429977a56e93f878c6aa476499af826dfeb31e1427a3ecf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a8adb342a2e480d53c51603cdc4639fd267aa3a0bd2e23a401a96ff59fd6835)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49d512db6d3b1ffc684d416879df83dc5653ae72bb42efd35a26725caf1d4dcf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleStreamDeclarationColumn]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleStreamDeclarationColumn]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleStreamDeclarationColumn]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5e66888da9da15f6f89739276a36e94c22f279f30fd375ccf712ee9a039ae95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitorDataCollectionRuleStreamDeclarationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleStreamDeclarationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c400332498a5f74e125dc0ff665323d4fb05ed567586d0d0c3bb927043268f81)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MonitorDataCollectionRuleStreamDeclarationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80a36eeee45ef156a9c7e3ed2d7927f36c7634875fe3a5530cef2f422a925531)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MonitorDataCollectionRuleStreamDeclarationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00bd38b5a0ef91213a035c24ae7c922c212052b84b4ea10d8ad432e06aa282c3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b41d6ccad592225e855f3c0342c9b401117f5c1865982fe0c5737ccccf4ad3a5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a17459a17bec5a83ffc8624d119eab8ded4d390acaed70a8b85cf7ee346fd924)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleStreamDeclaration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleStreamDeclaration]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleStreamDeclaration]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec1b9ba16f5445bb2d002a51f11adfce97a43b9d7b4ae2b73457cee8ddd2f1ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitorDataCollectionRuleStreamDeclarationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleStreamDeclarationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e33be8e1d18f694ba4677058f160d1838599bc2807b8b52f0b67f8fd9705dff6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putColumn")
    def put_column(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorDataCollectionRuleStreamDeclarationColumn, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff37e31aead6dbdcafbf2dc25806cc88a0516f99dd770bb49f37e32a6afc4254)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putColumn", [value]))

    @builtins.property
    @jsii.member(jsii_name="column")
    def column(self) -> MonitorDataCollectionRuleStreamDeclarationColumnList:
        return typing.cast(MonitorDataCollectionRuleStreamDeclarationColumnList, jsii.get(self, "column"))

    @builtins.property
    @jsii.member(jsii_name="columnInput")
    def column_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleStreamDeclarationColumn]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleStreamDeclarationColumn]]], jsii.get(self, "columnInput"))

    @builtins.property
    @jsii.member(jsii_name="streamNameInput")
    def stream_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "streamNameInput"))

    @builtins.property
    @jsii.member(jsii_name="streamName")
    def stream_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "streamName"))

    @stream_name.setter
    def stream_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00fe327948ece6e337e8b4f1c8e0a681cfb20f111f2e46efd766314fb52618e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "streamName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleStreamDeclaration]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleStreamDeclaration]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleStreamDeclaration]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__476e90edd85e53884b8cb43534e783166bec4f4bd4920110de22b9c028311056)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class MonitorDataCollectionRuleTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#create MonitorDataCollectionRule#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#delete MonitorDataCollectionRule#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#read MonitorDataCollectionRule#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#update MonitorDataCollectionRule#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f613481b34a9e84eaf7bdfe27afa2f209b9c0450d6f6da0e76bf9978064eb832)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if read is not None:
            self._values["read"] = read
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#create MonitorDataCollectionRule#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#delete MonitorDataCollectionRule#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#read MonitorDataCollectionRule#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_data_collection_rule#update MonitorDataCollectionRule#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorDataCollectionRuleTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorDataCollectionRuleTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__748230ce1aa460add2b88e74b7b34e8e75cfb571cddd317414f030d656e633be)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetRead")
    def reset_read(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRead", []))

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
    @jsii.member(jsii_name="readInput")
    def read_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "readInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__623c9190f2692ff5b8c50f4dc7846c8ae43654b019829ffe7ce7255adebbe281)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__944eaa692cd5bc0f47db9e7de9ee30c53758ecdb4de0dbb2324c765bc500ed3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b21271d37530314d8a2a14fd460cbcf4ce1910df9dd7a122aa1902c42e21872)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74dc6e72b4d4da7518e8afb87a7b1a96223dfeaf3705c734a9179cba1db15e4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff96d5437c456f564ff126f6b28b77cc57c6bb67a074dd8c94acac244b1d4bde)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "MonitorDataCollectionRule",
    "MonitorDataCollectionRuleConfig",
    "MonitorDataCollectionRuleDataFlow",
    "MonitorDataCollectionRuleDataFlowList",
    "MonitorDataCollectionRuleDataFlowOutputReference",
    "MonitorDataCollectionRuleDataSources",
    "MonitorDataCollectionRuleDataSourcesDataImport",
    "MonitorDataCollectionRuleDataSourcesDataImportEventHubDataSource",
    "MonitorDataCollectionRuleDataSourcesDataImportEventHubDataSourceList",
    "MonitorDataCollectionRuleDataSourcesDataImportEventHubDataSourceOutputReference",
    "MonitorDataCollectionRuleDataSourcesDataImportOutputReference",
    "MonitorDataCollectionRuleDataSourcesExtension",
    "MonitorDataCollectionRuleDataSourcesExtensionList",
    "MonitorDataCollectionRuleDataSourcesExtensionOutputReference",
    "MonitorDataCollectionRuleDataSourcesIisLog",
    "MonitorDataCollectionRuleDataSourcesIisLogList",
    "MonitorDataCollectionRuleDataSourcesIisLogOutputReference",
    "MonitorDataCollectionRuleDataSourcesLogFile",
    "MonitorDataCollectionRuleDataSourcesLogFileList",
    "MonitorDataCollectionRuleDataSourcesLogFileOutputReference",
    "MonitorDataCollectionRuleDataSourcesLogFileSettings",
    "MonitorDataCollectionRuleDataSourcesLogFileSettingsOutputReference",
    "MonitorDataCollectionRuleDataSourcesLogFileSettingsText",
    "MonitorDataCollectionRuleDataSourcesLogFileSettingsTextOutputReference",
    "MonitorDataCollectionRuleDataSourcesOutputReference",
    "MonitorDataCollectionRuleDataSourcesPerformanceCounter",
    "MonitorDataCollectionRuleDataSourcesPerformanceCounterList",
    "MonitorDataCollectionRuleDataSourcesPerformanceCounterOutputReference",
    "MonitorDataCollectionRuleDataSourcesPlatformTelemetry",
    "MonitorDataCollectionRuleDataSourcesPlatformTelemetryList",
    "MonitorDataCollectionRuleDataSourcesPlatformTelemetryOutputReference",
    "MonitorDataCollectionRuleDataSourcesPrometheusForwarder",
    "MonitorDataCollectionRuleDataSourcesPrometheusForwarderLabelIncludeFilter",
    "MonitorDataCollectionRuleDataSourcesPrometheusForwarderLabelIncludeFilterList",
    "MonitorDataCollectionRuleDataSourcesPrometheusForwarderLabelIncludeFilterOutputReference",
    "MonitorDataCollectionRuleDataSourcesPrometheusForwarderList",
    "MonitorDataCollectionRuleDataSourcesPrometheusForwarderOutputReference",
    "MonitorDataCollectionRuleDataSourcesSyslog",
    "MonitorDataCollectionRuleDataSourcesSyslogList",
    "MonitorDataCollectionRuleDataSourcesSyslogOutputReference",
    "MonitorDataCollectionRuleDataSourcesWindowsEventLog",
    "MonitorDataCollectionRuleDataSourcesWindowsEventLogList",
    "MonitorDataCollectionRuleDataSourcesWindowsEventLogOutputReference",
    "MonitorDataCollectionRuleDataSourcesWindowsFirewallLog",
    "MonitorDataCollectionRuleDataSourcesWindowsFirewallLogList",
    "MonitorDataCollectionRuleDataSourcesWindowsFirewallLogOutputReference",
    "MonitorDataCollectionRuleDestinations",
    "MonitorDataCollectionRuleDestinationsAzureMonitorMetrics",
    "MonitorDataCollectionRuleDestinationsAzureMonitorMetricsOutputReference",
    "MonitorDataCollectionRuleDestinationsEventHub",
    "MonitorDataCollectionRuleDestinationsEventHubDirect",
    "MonitorDataCollectionRuleDestinationsEventHubDirectOutputReference",
    "MonitorDataCollectionRuleDestinationsEventHubOutputReference",
    "MonitorDataCollectionRuleDestinationsLogAnalytics",
    "MonitorDataCollectionRuleDestinationsLogAnalyticsList",
    "MonitorDataCollectionRuleDestinationsLogAnalyticsOutputReference",
    "MonitorDataCollectionRuleDestinationsMonitorAccount",
    "MonitorDataCollectionRuleDestinationsMonitorAccountList",
    "MonitorDataCollectionRuleDestinationsMonitorAccountOutputReference",
    "MonitorDataCollectionRuleDestinationsOutputReference",
    "MonitorDataCollectionRuleDestinationsStorageBlob",
    "MonitorDataCollectionRuleDestinationsStorageBlobDirect",
    "MonitorDataCollectionRuleDestinationsStorageBlobDirectList",
    "MonitorDataCollectionRuleDestinationsStorageBlobDirectOutputReference",
    "MonitorDataCollectionRuleDestinationsStorageBlobList",
    "MonitorDataCollectionRuleDestinationsStorageBlobOutputReference",
    "MonitorDataCollectionRuleDestinationsStorageTableDirect",
    "MonitorDataCollectionRuleDestinationsStorageTableDirectList",
    "MonitorDataCollectionRuleDestinationsStorageTableDirectOutputReference",
    "MonitorDataCollectionRuleIdentity",
    "MonitorDataCollectionRuleIdentityOutputReference",
    "MonitorDataCollectionRuleStreamDeclaration",
    "MonitorDataCollectionRuleStreamDeclarationColumn",
    "MonitorDataCollectionRuleStreamDeclarationColumnList",
    "MonitorDataCollectionRuleStreamDeclarationColumnOutputReference",
    "MonitorDataCollectionRuleStreamDeclarationList",
    "MonitorDataCollectionRuleStreamDeclarationOutputReference",
    "MonitorDataCollectionRuleTimeouts",
    "MonitorDataCollectionRuleTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__c7453666e1a553395226393741cd1fa7f278ea729f9b208c8d82957365dd73fe(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    data_flow: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorDataCollectionRuleDataFlow, typing.Dict[builtins.str, typing.Any]]]],
    destinations: typing.Union[MonitorDataCollectionRuleDestinations, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    data_collection_endpoint_id: typing.Optional[builtins.str] = None,
    data_sources: typing.Optional[typing.Union[MonitorDataCollectionRuleDataSources, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    identity: typing.Optional[typing.Union[MonitorDataCollectionRuleIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    kind: typing.Optional[builtins.str] = None,
    stream_declaration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorDataCollectionRuleStreamDeclaration, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[MonitorDataCollectionRuleTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__dba47b1b6c42de36e6ae9966095eb212675ea24a244b1496da0d3b486acc7891(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e11e8053e4d4689ad66e11c5b3b4857dd939bf1bc46f7fd9a24c4a7ce5e81a3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorDataCollectionRuleDataFlow, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54f340e62d907c8b0daf07fe2fba7d441325e33f8ab4032cf24dfadad6e3c4df(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorDataCollectionRuleStreamDeclaration, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d30877cff5173239a7b0c8c7ef63144c135a702f3454101cd8bbc9bde00aeaef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0a394bb8b6e37d91805fa59e4acaf2d079e0d607c424ce7ee9c94e1d8b7eef5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd1a633d39cc0d112f1c664f1c447859aab147a85e4c0b444cf173e02a713773(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__275a728f2a5ab4f192ac57947b946bd499a44adaa22a59fed67db05e8add50df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b2ebce16a93e815816f1d44e9db356f927eeee9cbe385ce08fe43cd9deccb68(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d38fb73cf03f998dbc2489f0dda204889060e754510687c2747824cfd3dbb408(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc5f01dbf2f883c2a932ccfd3de2a8ac4ae393089c4ea1d2dc518f89a95f885f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a015c242f541883e7d693f89c1e1d38d3a9ab49dd92619dbb1ce3d833530265b(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fa2466c780fe932563ee1fdec3e948f3932866f264f4758aa6e61dfaf01b721(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    data_flow: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorDataCollectionRuleDataFlow, typing.Dict[builtins.str, typing.Any]]]],
    destinations: typing.Union[MonitorDataCollectionRuleDestinations, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    data_collection_endpoint_id: typing.Optional[builtins.str] = None,
    data_sources: typing.Optional[typing.Union[MonitorDataCollectionRuleDataSources, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    identity: typing.Optional[typing.Union[MonitorDataCollectionRuleIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    kind: typing.Optional[builtins.str] = None,
    stream_declaration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorDataCollectionRuleStreamDeclaration, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[MonitorDataCollectionRuleTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31534c94d7dd3dad441dc0a88e1e01b345b0d2771935ed98ae8cfa810007c1b8(
    *,
    destinations: typing.Sequence[builtins.str],
    streams: typing.Sequence[builtins.str],
    built_in_transform: typing.Optional[builtins.str] = None,
    output_stream: typing.Optional[builtins.str] = None,
    transform_kql: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3b7467ac66c79abb788f4f177613cc038be6bd3bef457292cad4d50c9d2ac4a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e28001bae8dde55b09ebc93d72573d086b3471678ab9376fb58397279361854(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f3fe99a37a74266ffbc7c65e477f17d6b2ae1c0d94b6fe073fc14a8ac979493(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e37357f493fd96feb93ab04c9ba3ffd21760d46f8a20df9eea4700415bccd5ff(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16f8b837a7f0ac2ccc598e8656dc844340d6afc00202328badf53b48cf1d29ea(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19211c8f99e693e17a52ce672f2aaafaa796160841818044805dec48626ccd3a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataFlow]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c3d0559b2a7af7e3c93c11f6ce5dd64fc74b4cce670ea17392f5d6adc9f9777(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d03e553b251524d586568c78b3442226119c632c5a22c4ada73be4320aa4382a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1c3ab541bab6e813a141e98046559a185a3117aac7618ac05955f43018ca51f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82747043612d572183f743126834600111dbe1cbe0beb9b34e2c6bff289b6aee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5d5cdf55d1808ceeb0ade162c05658ac355c00259c0977a978a8ed2acb2942c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e185123c0ff9f2683216d5da44c60b17b01ffb8d0565bb3d2ee8dfd1b364e1bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ae601d4a96b61b1e90db264045b452e77a95599c2b7b7c10185d848b2b2a32e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleDataFlow]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50c3daef060c1ba14b60de26ea3644ccaf37e883eede9cf3152594ac4b91630e(
    *,
    data_import: typing.Optional[typing.Union[MonitorDataCollectionRuleDataSourcesDataImport, typing.Dict[builtins.str, typing.Any]]] = None,
    extension: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorDataCollectionRuleDataSourcesExtension, typing.Dict[builtins.str, typing.Any]]]]] = None,
    iis_log: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorDataCollectionRuleDataSourcesIisLog, typing.Dict[builtins.str, typing.Any]]]]] = None,
    log_file: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorDataCollectionRuleDataSourcesLogFile, typing.Dict[builtins.str, typing.Any]]]]] = None,
    performance_counter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorDataCollectionRuleDataSourcesPerformanceCounter, typing.Dict[builtins.str, typing.Any]]]]] = None,
    platform_telemetry: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorDataCollectionRuleDataSourcesPlatformTelemetry, typing.Dict[builtins.str, typing.Any]]]]] = None,
    prometheus_forwarder: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorDataCollectionRuleDataSourcesPrometheusForwarder, typing.Dict[builtins.str, typing.Any]]]]] = None,
    syslog: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorDataCollectionRuleDataSourcesSyslog, typing.Dict[builtins.str, typing.Any]]]]] = None,
    windows_event_log: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorDataCollectionRuleDataSourcesWindowsEventLog, typing.Dict[builtins.str, typing.Any]]]]] = None,
    windows_firewall_log: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorDataCollectionRuleDataSourcesWindowsFirewallLog, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3262b7e4fba65b85ae0a8271ed3df0413aef70895f9bb24c6fc6610da49d2bae(
    *,
    event_hub_data_source: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorDataCollectionRuleDataSourcesDataImportEventHubDataSource, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f2f3b342185c9de637d137d175678eff77f778fda571cc847a8c5b4828c5323(
    *,
    name: builtins.str,
    stream: builtins.str,
    consumer_group: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29590b283d356a0f90c9cc3128b67b845ce4cdeda8beed13ea38940ed7686a04(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ae9a7f6721561df6fc9c14806670eb54fecf35de55fc3af72cc6b8f22cf3ab7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfea3867418562ef8851fc1c89ecdcbf975b9228da27dd1055f27fa5c79d3171(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__529ccb764c8e7b468e996ee0d8873e53255fc39ed89eb95a0b016a82094f3622(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55ed47aff4f3af3bab2d243d4e933beeb4651a3391057e700f2da7550403ed90(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cd03ac7c0bd7e474ba5b8207bc5fca2a97c2c54d78936e1e05ddc5971c3b3b8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataSourcesDataImportEventHubDataSource]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f44bfe2c2089926bf7a525290cc575d620b333d029b0d2c142e954ec0d51f067(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74b562cd9ffdacde0d9ea28b274d6bb47fd9cc594824bab0d3c244b3a3196e54(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7869bab659488254e97b166fa162eddb98cac3ed4c25e9e509c6b23078d25634(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__397ec18f5435583edd09a2ad3299ecbdf0e8e1b6d6ef49d1a96c27e2152bab25(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6ae81a81f9c633214caab5ae0efdcfe44a86ea39382d403ca1f0263526d700a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleDataSourcesDataImportEventHubDataSource]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbf3731504544b30a8c9651015413a3a45b069b395baa58e796e79266b9d1998(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d130638f8d2f6ba7debf434f56af56fad1f853a9089fbce7f1476f11c185b36(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorDataCollectionRuleDataSourcesDataImportEventHubDataSource, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c61704b586a19652403e830efc3ecffd3b09188fab704fa525b992f1dc06480(
    value: typing.Optional[MonitorDataCollectionRuleDataSourcesDataImport],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__880b7ad1e3b0bd0ba7e0151d7e7567c5d08b9cbdfc6d38d39417b12702a3368f(
    *,
    extension_name: builtins.str,
    name: builtins.str,
    streams: typing.Sequence[builtins.str],
    extension_json: typing.Optional[builtins.str] = None,
    input_data_sources: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__183fae162e87e634b2a1f5afe600ebc7173826d68e760e51ee37419023830866(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcbd9f8ba2db26388671009239773467b9df840eb192aafbb15e32fbe6db5486(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7a9b8afdc59c99c73eafd4d2819580128b0f70cb88281820ff12e4121c0895d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fa733b18a6e5102f40d47e6d9254aff9099cc2b95d7877810da5756c5f56b9f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__185756c2250710bef82bf9ac7c9bb9b2cc4e16b791ea9d93bac1f29419126d06(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d0cd819b7de080bf03920306efacdd1aefc760d5024ea31242786ee123aa0f8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataSourcesExtension]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d52a47c60ab98c9c983f79ffe99470d98b01f78d2b3c72d7de6fdff9efd14a6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae6e2ea2650bca6797764421dc9064fed839bc8a152f80c6c282e07160d96b1b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b90ad2b40420efecf2dd706280bf4eec18f806932690a7cee0d59f7995555fa6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d043607978efb77412109d01c1589c0f4a02ce12d95b0d4be2879dc7ab7d6d0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35680830854aa39deac9d18cbfa14a1eb36b0479ff3535f70a2040634b7feac2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d00efb2fbf8068731a29e8ab7f73f72aecd0787c4401f1cae08f2ee5e2c1e50d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67c7afc49a4e77c572bcb5390bd01ce235841f959207e50382bcb1962e0b8e04(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleDataSourcesExtension]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ef8c9fca9c8b9b79002539a94df023be6df964f6f39c0d558c3a4777c90ccd3(
    *,
    name: builtins.str,
    streams: typing.Sequence[builtins.str],
    log_directories: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06b3a67e2c30d18451d24fb3cf65a1636d46c5468602d45254cae2513ae8a595(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ceb44a30fc035f9e53bcc72d6a21ae2404ed42c790558ae375399abf84bf576(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__752acecd7c19c1cb258e4b1a2317dab77fa17dee046a0430f5d2f0557d7fb703(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cf7e719bef4c809a5a420826ce55f4db3efc0de9f49827d0a64a049363438b4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__954312fad0afa4158e1064b1f4fbf1147bebc4447552b060565ccb9ae234c882(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63b258eab377dfdb70dc0b6c7c9ae85ab87df9549b9bfbfea17ef93cb4ef0d79(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataSourcesIisLog]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c618e00db752173dedb3c55c3f7198f2bda0afc2a7279d388b871fed33c8f125(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac77ff797f08d8baeebc79d65bf0e69663aeda19b3415dead23bda985483bf1f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f369b767deef3361ed020489d6f1191a77d2eaf098a23b9171513af6a67e776(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7535688f3775d46b49526d26e308f0b6d5b25867b5f97804bad20dd8c71267ea(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a506c53057206010880750cbb88d05dc756409723ba562dee2b5afa5abd63e6e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleDataSourcesIisLog]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce6bf92be26f173593b7b8f50b510aaa03756cc509333fdb39e9ac87d3776cd8(
    *,
    file_patterns: typing.Sequence[builtins.str],
    format: builtins.str,
    name: builtins.str,
    streams: typing.Sequence[builtins.str],
    settings: typing.Optional[typing.Union[MonitorDataCollectionRuleDataSourcesLogFileSettings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__727135006aedeb8ae5ce3fa6cef49e607828971f07d6d32e647023f7487bb7f1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18daa58e609b8a8874b4d6abb918f3653c290f91d97452e6b3008a2afb9d7bfa(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__686e4534090feaf1ee8efbc4e2b3ea209dfb5eb27aa22d02c2debc3bac6470d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f642acceeb4ca4caadc25df35494e5f438044570134e607a27d4383dcc0449bc(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d71fbcf47ceb6aa01f8cc4bd7fcffe3f4c26df7c5d1b40f99f0e0ed98186440b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42c55079e690c1c4f9d4e94dc2aae91a29fa878b3a573c15438d39e72641a548(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataSourcesLogFile]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92bea6f0cb202c919836612c29ee2784808e7bb1598645092e715d95eef46a64(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e9d5cab40adfc1b6fb3b04a6ee823caabd50af330c9cdc2fd206fe9acabfc4f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3861ce8f7db6e132b46d0cd7589274e19436415d22189db5abddb31b30382b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d694afa9393a29374778337827ed1e372af586609b98063939930b1919f48e8a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c151260505352414307da7588cb600525382ed38e04f8e69c0f5a01c3f47a4c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebffeec8e64047386c02e4a1b41c2cdb189a883936bd11dac86af50d3261d2ed(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleDataSourcesLogFile]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95b234245330a8d0fc8eacc51541d51a7c89e09f6bb857f8bb16c20454ecb08c(
    *,
    text: typing.Union[MonitorDataCollectionRuleDataSourcesLogFileSettingsText, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc06b4ab28a44d9250550e345d6e992cc5a255db20b244e7a35d7d30543d17bb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f677a00e585184c248d95092d1a1a237593fa4b56a313377ab0448b9c263f5a1(
    value: typing.Optional[MonitorDataCollectionRuleDataSourcesLogFileSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95255289c5e4137d42b09cc7a318a73acb6d1dc2303b37ef18d657e89efe34b7(
    *,
    record_start_timestamp_format: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4732828277e824f249dd704e72000b2b5609f4a48028f2b14884f04c4c59c619(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f9c8c490846ca7ba7f9c1d43328a58c8908dd0192b65923431deae7f2d1bdca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8a9db2bf08bee988ffe81d2ac84f12288f91c711f54cdd54659d8b60bc493c1(
    value: typing.Optional[MonitorDataCollectionRuleDataSourcesLogFileSettingsText],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2effe2f8c570d9473506ca26fa08538e9686d88823968e25280314ce036abb49(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c0a89278e0341b256e9f9cc8e1d9d492bc0e448d8018ca9d7cb9088b0251dd6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorDataCollectionRuleDataSourcesExtension, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__479e5fb7f6b3bd77369d320a95d5dda73a25207f9e6afde8d1b7f5697cc7c3ae(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorDataCollectionRuleDataSourcesIisLog, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f84c621f1373a4e36867e0e7a44cd5fcc625a0c01046e9742eb4c00a631f5991(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorDataCollectionRuleDataSourcesLogFile, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b0b23419be8886df574a3538f0029ecb4dc28798e8cf2988355ce62ea204452(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorDataCollectionRuleDataSourcesPerformanceCounter, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89117c9722f1d47111ae53313de1e42c5bffa808939d9e009e266f36cd54c68c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorDataCollectionRuleDataSourcesPlatformTelemetry, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__446f8dba2d704141f0974d30fb46b96460d04c072f7a06bfa65ae0acba3688a9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorDataCollectionRuleDataSourcesPrometheusForwarder, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24b4fc0a3e1e4514bdc017ec8e53c7c1d6b3f0d0fd2a867d9635198eeb9a9979(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorDataCollectionRuleDataSourcesSyslog, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__678e2a6c50a509255b32cdb494db7c92fc40cca514d78b7b7865700b097015e9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorDataCollectionRuleDataSourcesWindowsEventLog, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67b556c47dc3f879401f4125b0b86b6b58e4ea460632d4fd37138fd836339706(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorDataCollectionRuleDataSourcesWindowsFirewallLog, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de9fcfd914b9be386362f91e5d399a648425be687b5559c9d4e9dbf6d3ca17c9(
    value: typing.Optional[MonitorDataCollectionRuleDataSources],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78ba1f5d9613309985657fe5930e78b29ab6382c52d1effa76c6bbec356ed669(
    *,
    counter_specifiers: typing.Sequence[builtins.str],
    name: builtins.str,
    sampling_frequency_in_seconds: jsii.Number,
    streams: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e176ba6c348b43592700cf73b905e40b6e43c0ec8716e5c3463fc730347ae7a1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3df5f8db59d7a70d216f8b9d09242dea4d008534d6c676b32f5c9082c4a5e52(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a46ef8e935b7375dc66288bcbfa68000ba20431c33565aa6ab0db1ac11d5247b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a50725eb29f40423111863c87f0fd76d5a138203d80f1f44cd8b71d14aaa5010(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afd547505ac563cc2877a062839063bffca99801d395a2c457198379b0a157e7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da162700eecd9b67119ff4ba6574311c9cbf7617dde1c9306c4a761f93a5d923(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataSourcesPerformanceCounter]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eba48b3032f1fbdbec9520c26c08f837f3499f3787aad32081ac6bf7d9c0a1bf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__019fc55d291fdf6ed53eabcdfe5a735e7cfe4e23b2bc2205f2076a530231696c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44685a243f0dd09810e08799a3cb881340919bfdab2f5963000a5fefa414a0de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55e296f08e7386d1e845462f452383c1b5701615f2293becda6436199586af13(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0a02f98829b60720def8c2570ddc43664284f7ec78b53b572f0f27c587664c0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b102ff800cdee7e14415df5d29642221721ec2b922472f59e0ae5a26a074e62(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleDataSourcesPerformanceCounter]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__893b7642dc4492cb01e1fc646c94a91668454a46f91008a4605d9b08fe53b0f7(
    *,
    name: builtins.str,
    streams: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40b8ffd17e076f7ce35660925126a7d27653b7b891169cdb5dad3462520557d4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecb14f862f326f28c802aed5d368d3f8bdbbf88ac91778583294dad151299fbe(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71e6b77e81de88cf838253f01612e4950ceeb9fe4b49d712e8d7873b4cc505ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0338a47c8935435c408cb764cc97ed35d60160a5ba4f501c4317ee3662ab73ac(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f33b81a6bb8842c742d3165482ffcd32e6e91230c49be8ef7c974aab6a9f0526(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1419b396805706fce6f8d5a6d8badde0e7ecf405f0ac0098881d13d718f53661(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataSourcesPlatformTelemetry]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72b053ce11de80de9743885e7c9b439986c3382d770f0c040ab97bc0f748a484(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__166ce3b31b2eb654cd710d257e20968d0e41132c8e61feda632062d5e183b048(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed326a49ab99ecdf7aa42121c0cb3b8eae5fd045fc70361e56a2186a81ae119a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d3315c2cfaab6618515c86287781d06b3f1f3daf34c9d94027784c67fd68f0f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleDataSourcesPlatformTelemetry]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__748a48c639c5c6d46cac71e2d1bbc17ab59f3d95e1ffab7a424dc9b5f78e6297(
    *,
    name: builtins.str,
    streams: typing.Sequence[builtins.str],
    label_include_filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorDataCollectionRuleDataSourcesPrometheusForwarderLabelIncludeFilter, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7819ef7b9f42ab08f81f81aff0b853cf3db67b21f7054c7e036d5c7010b7941(
    *,
    label: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dde0866ef111a4158a013d6a97cce28736a3d65f1bffa01461148886731799c1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2df643227f769dcfc10f96e9b375fa3070a745f6cf25f6934f214f5fff068227(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa8cddf8bef9870024c205d956ef793f82c7bebd12e4af96a8987220628debd9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c274bb9584ee04f296539ee7142e838cfa7b15a5fa742a408b84a4e20c538a6a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab61b8e9711b1f55ef363b6b31f6f4a4af77b963fc349f5c3961557904af3e3d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4c3589dfe654e9aa703f50de18eceb8b70bea8f99e4a7ba209e24ab50fd2f3d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataSourcesPrometheusForwarderLabelIncludeFilter]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab3e82b5634f904979adbdf991549be00bf8fe88f4583c97f5737b1ed6a8c35b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a7ab249ce09b53f9f01c9151fd9f4f494b57cdaaacf94510b1cdf986e7425af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ac72bdac82b947a6a8f66e06085918c0031dcc03bf1879493aec32985dfc766(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a49ca3311e1a4a725d5eaa6af0b3cbfb1214f1bc6302f194676a3a9e1343a98(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleDataSourcesPrometheusForwarderLabelIncludeFilter]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17b730ccb790ef3acafd2a5efc047bf288696d01fc22937ba669fa73c0363c5e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16e6e7f1ac10a26dc3dd99ddacf08e0a3c7d34fa31c371d297f8016bdc25c577(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c96b6423087db06a4c50fdfefb2a973ad90791e90612a33f16cdd65a5dec3f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dad2ba06b3ebb6259ffc9a6f1e388d5b91feb5f669b47e47b608dff692fe19b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db1e4da8e54017aeb4105205d13f8f243ad056386d5926e4f4a118a2d5a07f5b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd29ce9a04bc3da9f4cdc044ab4f84ea3c5c9293e7a66164f18e519ff472de2d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataSourcesPrometheusForwarder]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74f944e46d0e8360e8d42d38f908006a4c6d9572e9cea4eed6a63e7f37f1bf52(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70b4d8667a809599de311da20fd4a3b58a317e9ba59aed6d3610fb76bd505f1b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorDataCollectionRuleDataSourcesPrometheusForwarderLabelIncludeFilter, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1422ea479ac5d9d4fd0dbd69a1a44c1a983fec6f10c66be730e81f1243bb78ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__303875eb0d02e0550ce37a4015f792c57cc25fc32629705a1c77b38a1d882c42(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3177152f4b640aa9072f6d04d09e80e9a68d84fefbbab44ec637b8ac09aeaa53(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleDataSourcesPrometheusForwarder]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a9883e1ae6a4738a241f2d58c530f77392ebf28f4f8bcff16cbb35b180a87dd(
    *,
    facility_names: typing.Sequence[builtins.str],
    log_levels: typing.Sequence[builtins.str],
    name: builtins.str,
    streams: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8e065d90d2fec3a359cfa493fc108b40bb648980f2a7a10d7c41adcb8e342a2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__775dd5444548e5ad93924f6b6bdb06546a96458eac1dff78ce4ffef60980db18(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3b2257aad83009eff725de5a48a53bb4b36eb3f0fd2d008e6341c5caa217967(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b22a5544aea02741f55941d849ef70b86928957d176407217cf1c05e2b4ad316(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ac12af89411ebf126eaa86d93b12437625c0c61c2ef2ed78715fa965e45867a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bf58e26d2249e71249170f53fc2737e098ad5207f6a76257b72d373a24f8862(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataSourcesSyslog]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9395de1dc772496048a16e5720bf172b0429024a22a8780da6d5625c4edffa3e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a710f9efe877b8c08037c0a7688d0c185fa2ad66c1420e68d86ebf9afee7e9f6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b95687c2eec80398767496ad3cfa55696d9ea87e6425d0ed7691355e0ed6bc47(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__500fe805d28c61fcaacebf17058d8f615e949ced6a6cc55dfd9917bc41b9f381(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c1cb242acfb5b9e07424d7ab71d87206676b08fd6ca1cc668c9daec918a93b7(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca36002b57f3acbd64630f68149f68bcde0363e4baa21d3592020407ece77b90(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleDataSourcesSyslog]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b557f77d1831e36056c552a32db43c0d6da5fda2d3231c835178e51abd7925a(
    *,
    name: builtins.str,
    streams: typing.Sequence[builtins.str],
    x_path_queries: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec9a50ff2a5020e44702ba3ecf596a9339a8dc48b6fc4695018929d907f21f9f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a625a4a1a6a1cf68036a2cbbc33e3af075a67ab10696572e1d5fa4cc84c1052(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f9fa611d7edce38fd55b9b978596d636a49acd5037a6e226b599532c8e369b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b27f75a278932276e72a3aefedcb4483e91634cebdcafff23762203e82469f8d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84602f9219b96030b27dc26be68b3a66a004f24f7d1062ee5316a73753202e8c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8313d3809cc603a18a5c92cfb56366a1df14d027b50ea1a55acc65608409efe(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataSourcesWindowsEventLog]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f0fb0e4b94355c0f9c3eb1acbc8271d1cffec0637dbbdc4546a4b2cf757e007(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e59ed61ddbff58dc840808382b8ddf1c2892676c422e0c949d21370e3de0a920(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4e3a8eae68c25d444877c414cc6abda9d2d5cf268f00cc01e386619a37507e6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f23cebcc2b2a793c46d90f5a53dbe34f3c4549cbee36bab023a947623238222(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41b0f67435549f47faad1238a8cd36c0a9404a47a886965b566e4967ba1a389c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleDataSourcesWindowsEventLog]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1a1bd09b1a147bd26074ba3591ac31ffcf67a492a6f3dae379ae3e5a71d754e(
    *,
    name: builtins.str,
    streams: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__613de7631942b3295fe2cd82a34fc560a6f5687f37f6ec4ec4089fa6c76bd9f7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82e28b8cdd352ddeaf52c739818f620daf3eb1b82544609efe2c98e7da156a53(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14cf0dcff3b1eea3b96519ade30dadc323a3bb398e94903c19c6a5fd244a0df3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eda2dbf53aaec196c5b45d6ef402760b30a33cdddd8f8a39cea80b0858fae0b1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef57cd82c9a2b0f14ddd2df1a7850c264e73921e9ccf131c2a95dba976e97143(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0500c3d5b61211b1c71b49dfa0845a527ffe0d0bd3720df12148d8795ca525e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataSourcesWindowsFirewallLog]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b37a7787c1610e053182d4bd5ed868b58a83515b45edc30bd3cc451dbebca2b0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1707e9fdd31fd12f9de1730a95c4720b9e182585fb4ba56f34663b3383ce6bcc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32690042f3ea13ccb446b4392a304bee6af6dba1ba46652e1e3c9b10102ee94f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7aaeb5e424b3ee0ee12a4597ffc004d1f138611e369216cfc8e6e58a690d2463(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleDataSourcesWindowsFirewallLog]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91129a3b8459f9f9277e633acd1c0cba03afca8b282196aba60a2ffea57b91a8(
    *,
    azure_monitor_metrics: typing.Optional[typing.Union[MonitorDataCollectionRuleDestinationsAzureMonitorMetrics, typing.Dict[builtins.str, typing.Any]]] = None,
    event_hub: typing.Optional[typing.Union[MonitorDataCollectionRuleDestinationsEventHub, typing.Dict[builtins.str, typing.Any]]] = None,
    event_hub_direct: typing.Optional[typing.Union[MonitorDataCollectionRuleDestinationsEventHubDirect, typing.Dict[builtins.str, typing.Any]]] = None,
    log_analytics: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorDataCollectionRuleDestinationsLogAnalytics, typing.Dict[builtins.str, typing.Any]]]]] = None,
    monitor_account: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorDataCollectionRuleDestinationsMonitorAccount, typing.Dict[builtins.str, typing.Any]]]]] = None,
    storage_blob: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorDataCollectionRuleDestinationsStorageBlob, typing.Dict[builtins.str, typing.Any]]]]] = None,
    storage_blob_direct: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorDataCollectionRuleDestinationsStorageBlobDirect, typing.Dict[builtins.str, typing.Any]]]]] = None,
    storage_table_direct: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorDataCollectionRuleDestinationsStorageTableDirect, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34ecd0556ab897ecc2bca1b5401b8dbd4d672f663daadc537150dba8b8f4fb70(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9057f9db833800d87a63b1df8170af107ad8c20affb98d66be4da94182eb044a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4a0a0ceb07c7ec885a3ac5d79b0833b8caa3d739dd8be4eecf59962a9c29a10(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd026bc0ea172c4e759b319b66699e7648ed57e390d431db5a417465a0b767a1(
    value: typing.Optional[MonitorDataCollectionRuleDestinationsAzureMonitorMetrics],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__160d234c5efb98e7d7aaf8fff166cf2501f5f0da4e0369fa0331cb69400f804b(
    *,
    event_hub_id: builtins.str,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c230c5f49687b4cccd1f72d1306f6771230a133b3d8fedbf9b3091cbf8e020d(
    *,
    event_hub_id: builtins.str,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26533ecd7410f95ecddf5b352a8f5795bb40af2d387718041f5bbaf431bac56b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd583406bbb530e86aaa46cbf72ce344b0ed8753b6815f83b5b2b5c780368d88(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d68c4b0157dbf2a9e8349a16acd59779316296814282f580b387912424bed271(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9853d165c79cedb400075b022dd67011c74bf6314681cfbcfadbf3c444934a37(
    value: typing.Optional[MonitorDataCollectionRuleDestinationsEventHubDirect],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c9cfb57eddc8c11ae96b69b9e1ef5e27251765f4f6f390828c7f7e168ff3b04(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffd209adc5f4d36db698e02874baa297726524bf45773526b85a36c7eb8fe3b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fa7b2ad4fd2a505c27c86dba2e107d9698b55030205f9737a63cb9618831458(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0347098749d1808cf452d8b76755b08a11bd47d27cec485c36488b977acfcaa2(
    value: typing.Optional[MonitorDataCollectionRuleDestinationsEventHub],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__251443bc66028e9ec47bb10d9c703e7b79fd9cb49a3de69a82c29a7adf08508d(
    *,
    name: builtins.str,
    workspace_resource_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b910654ddfca9e344e8141acb1abb600e90077de18e9650337a717855d8d624(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63e8cb24e7b3a3be4c78abe3061cb2287e98ba7aa0554fcc0bc3e3ad43b25a50(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__731f1b46222b14adf5de13fc4bd639cb53277f8c38ae139bf3c633796136e89a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3a9bd5eb5e4e75e12f759e050b6048ec228cbdb3328abf91ef53311f1ce2c44(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f959ef7c4c4d4bd72b60c4d4bd883b10c7bb28a6131fe871b7626b4963e14b0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__616fd31921bf88f0d3165cee51b4f976c64c556905fe55727a70ccf6ad9a45bc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDestinationsLogAnalytics]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d98f91803fead56e4f1ba854b066930a45e6c7e6e91b8502163107c55ac6e11(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc1ccb4def4da1177ca948eefc1199d7f4cd2ea3886594f89878527bc679f01f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dea27ca99d63e43e6b0aa930b3ebbf5767b9ec3af80e50e6ea7f25059c0014b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__818948068c75dcae789dd04d74629d38a8c8c7d00b4382e6015b7fd035227055(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleDestinationsLogAnalytics]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5b78cb44e678c95f8c57a8899b455f3f9c8bf41c58a6075812fd133343a3925(
    *,
    monitor_account_id: builtins.str,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f175c3b6717c542a224787b5b2cf8c565cc037df0838fb3806bccaff5df40bf4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eed958ab0f9a61e88839ec16c6aa0d47f02c45f039858a89c4c665d5c2c58f01(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61c65298fa12f0d2264b24757a2e9fb6cb2c426a824b87316a990a1b00619d80(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2034dce92e800f4802cd76f29670ef36023f5fb25bffd0ca2c0d2bcffc2fa7e8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1ccd450e69cd0267425454375e567c1e0a3b10ad65fd71823ec51a4ddcb92c4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0e560068e9761ad15cd30ddaf3b8f3824bfb6cc2a1367a6b2ede026d813ade1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDestinationsMonitorAccount]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bfa1609570e37c05da2cc1e4b2d7f32d5438e334c3fb54049bc0d938517dba1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f19fd9d9353226cadd39167ce025a6e6c6b0be1d9f0af80f4eeff22e82b7e9ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12b1a388d0f71574bd5181bfbc4b72121818bdf4840ff3ac497f00ca11123200(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6fcdf9f53f6c6a19cec0de7b063182ce437c3cbb639c4b6b9c4ae5149996ead(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleDestinationsMonitorAccount]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02c782f684d157afde64540324f5f82e0b0f863ad3b1dc23c61fd2fcc72643d4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b415fe73dab62431fb7a05f0e71fec2d04de47a0db07fa94d8980ccc2497326e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorDataCollectionRuleDestinationsLogAnalytics, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f921b93ba934429c76fd4a832a05d7fac685b14ef4be389ca07cafcd49ab37cc(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorDataCollectionRuleDestinationsMonitorAccount, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67efb94f39d4bb0542b9586e38b4c1758a6083c3f68b4e1a6f3addd77b0bd7f7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorDataCollectionRuleDestinationsStorageBlob, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__075eeef1eebd0b23821cbf78acc145806a0a7bf4f064270a59d5e50b3f820dbf(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorDataCollectionRuleDestinationsStorageBlobDirect, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3294acaa45b376647b138d9274c746c9a2746fe54246b661ed4da9c57476258d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorDataCollectionRuleDestinationsStorageTableDirect, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e09f04e010ada32c12dc4384179d3061aaa449ccbbbf9e0972c668346135b13(
    value: typing.Optional[MonitorDataCollectionRuleDestinations],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0a5cd93e054aaea4539bb66d675d50c1803bf406ca6a6f7a07181f782b37295(
    *,
    container_name: builtins.str,
    name: builtins.str,
    storage_account_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ea149d212a8d21c3ff325f26906453d1f8660d65ce442c890906f81651658a7(
    *,
    container_name: builtins.str,
    name: builtins.str,
    storage_account_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8021273c42b466f9f3b97486baf27f9585bf6c4de0a6baac46e1bae6140165bd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__256a548052790ed4f3ba2333f964f1786b08cb5d2ea755a26be30cac970b1e00(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d370873594fde043fdc531fccf13ce4ce14656a60bb4e3a51a33b70fca1db53a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df8161d495d10aef9ad291757083cd8408558cfae0fca6ad95755c04648afe74(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59d4ceb5911760df7d6ba2a6c028422e5fbe9422313763e64777558c2cd6f35f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1daf7485596c215fcb5147b894da0d38632c13b8bc56029c227e22edbad3227f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDestinationsStorageBlobDirect]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f082bcc46470e3378cf2165764ae72f1e36c0aa362d89b9c6f82543a0c73684d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__662518c759cc7ad79cbad2ef8ef4708d4dd14b74cec2480af699d3308db490c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0434e1b4afc017abde4df13076b1c3e12969bb7e2ab85471b7d28b626b304cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f28668130b226b67833a2889a291936ec0ad9ebc39d25b0f1299a346b0e69b0b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a185a22b5e1efeed207b2ebca2dfe8d331a067038826058bb6b10dc885f5a24(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleDestinationsStorageBlobDirect]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68fe61b60734786501aaa0c3117c25108924ae24a2d2895c2ba83a58f39a524e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1136790942ae95df619a710fe1f41d3f8762ab48b6b539ddac0f0780fe88eb49(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ca283d159ffce95ea2dbd901c8028d4c83aa9d3e0b32a7c7dea1259a884b7a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__259aeb9002ac21aa419f5e0afae8b376b39171a8b189138821aee99b7bbe2903(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf3485fa18f0fe3814dd6640dfe811abbf51845cd6d10f729e035dfede36ca38(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02560b930034fec2c8feece69505ece6abaca0e826e1ea678ca2361429355e4e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDestinationsStorageBlob]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__850765f4ae3f14d5edef7dfff2c7d71d31285328ef9bd89049198b3e85173cfe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3258d9bf93fd56f5b401b320354ab9f7b2afcabf71680ba3a47093c9c81aa73a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2480828729c567fc8f6611a9675db3d625035a46ba281af51d649dde7fcbf900(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__475c5218e654a18a322219c2104ec972b9f9165c793d2aa9dd570578d5e2a786(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0bfeb3d337ff74cb52689e3176ac77cbf2695bf8fa4499e1ed94912ae844d2d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleDestinationsStorageBlob]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3b1e4f45317733b74c17366e09ec07f8540e18690d0f7d878c8db7017f1ea6d(
    *,
    name: builtins.str,
    storage_account_id: builtins.str,
    table_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f8690fe76bc211d9fc83f28783bc83135a377c4c505dc634d3b06b793af6e91(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef5c3d6d0eb8f5dd4234823dfb0324d487606f4ae2c92f9a0d52ee19f6a97ef9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36d3047a81c34b65bedf1bfba7469161cf31e68274b667c4882eb27351fec4ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65ac47afb175997fe3c17c507ea5cc2b3d71abfa593866c9a6a5cc9736400911(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37c63be88b5cb5cbf1d953d2a826e19965087b6934fb9602337e1e09a53eaf50(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__443e4388d566cf2100e2e2a612d3a75d9596c88dd08ea2ba2e33b47791fec601(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDestinationsStorageTableDirect]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5545279f07c7facd5e3d8f06af970a93d16a0d698b612858fbba584a6fc867b0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66e48dd877d1d09bf673596d01ff6502326ac957dfa945d6631bcbaffe59e15e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcc0e35739403f0d9c9b8de299cd7fd76f6282b76e6f4129a6f467595ecfe5a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5b674a36d32ce7138e260f5b5a9df5a5765812a9dbb9c4e0b58803dba4af617(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed6f9b13b7b399f0439eb206144030f2592a59988408888ce51d2a31cf4fcc13(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleDestinationsStorageTableDirect]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f650c265237317561bc2dfa71cf72f7201660e1f4242f9607a25f5788d6c02d(
    *,
    type: builtins.str,
    identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b3da5b97412e8737e5243674a917c40fda8601f51e0e7648c14cb25687c0f3c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3853531074b63b3f75574c3b5e12635a5bd67ea0343cac7402fb87ac8675dc4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fc45c3025797d8bf5347222063c2f63a1e057866b80b3eb7d0bb0f8e79b9435(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82792bb2f9b81393dc25a536b8cfd81c8c58dc64040c4316d8a59ab1923ae764(
    value: typing.Optional[MonitorDataCollectionRuleIdentity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4937c7273ee18bf0afd4efd6156584107b2e8dabda3e2c4b92f75e52942618eb(
    *,
    column: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorDataCollectionRuleStreamDeclarationColumn, typing.Dict[builtins.str, typing.Any]]]],
    stream_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66fec215009ed2ba77089c862d175dbd4183192a14ff4c2595f13ace96eae357(
    *,
    name: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58867fe18fe48c7cd7a7bdce907732a72947f2ee9fe27d3e5eaae3087fd159b7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__737f37b7baa90d66f5b4017371a14b24d11d0db14e15b9ea763ced3b94475e62(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bd672935853ed7684ec14a9d2846e8d90a47711ae1672d127c07fa50a85f5f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c2b9f8bfa03a826ad0ad0778127f7c39758246cd0aaebb52442eb5d6367f512(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dac1468c5c654bcad8d1ad576a91c4277414e351ffe68885e13ac8720e35ff0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__631c4f4b007a17e89688605541745b46d9dacb3afb03f8239bd3627422926a26(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleStreamDeclarationColumn]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15d899d3099b04a3c429977a56e93f878c6aa476499af826dfeb31e1427a3ecf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a8adb342a2e480d53c51603cdc4639fd267aa3a0bd2e23a401a96ff59fd6835(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49d512db6d3b1ffc684d416879df83dc5653ae72bb42efd35a26725caf1d4dcf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5e66888da9da15f6f89739276a36e94c22f279f30fd375ccf712ee9a039ae95(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleStreamDeclarationColumn]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c400332498a5f74e125dc0ff665323d4fb05ed567586d0d0c3bb927043268f81(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80a36eeee45ef156a9c7e3ed2d7927f36c7634875fe3a5530cef2f422a925531(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00bd38b5a0ef91213a035c24ae7c922c212052b84b4ea10d8ad432e06aa282c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b41d6ccad592225e855f3c0342c9b401117f5c1865982fe0c5737ccccf4ad3a5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a17459a17bec5a83ffc8624d119eab8ded4d390acaed70a8b85cf7ee346fd924(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec1b9ba16f5445bb2d002a51f11adfce97a43b9d7b4ae2b73457cee8ddd2f1ea(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleStreamDeclaration]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e33be8e1d18f694ba4677058f160d1838599bc2807b8b52f0b67f8fd9705dff6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff37e31aead6dbdcafbf2dc25806cc88a0516f99dd770bb49f37e32a6afc4254(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorDataCollectionRuleStreamDeclarationColumn, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00fe327948ece6e337e8b4f1c8e0a681cfb20f111f2e46efd766314fb52618e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__476e90edd85e53884b8cb43534e783166bec4f4bd4920110de22b9c028311056(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleStreamDeclaration]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f613481b34a9e84eaf7bdfe27afa2f209b9c0450d6f6da0e76bf9978064eb832(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__748230ce1aa460add2b88e74b7b34e8e75cfb571cddd317414f030d656e633be(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__623c9190f2692ff5b8c50f4dc7846c8ae43654b019829ffe7ce7255adebbe281(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__944eaa692cd5bc0f47db9e7de9ee30c53758ecdb4de0dbb2324c765bc500ed3c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b21271d37530314d8a2a14fd460cbcf4ce1910df9dd7a122aa1902c42e21872(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74dc6e72b4d4da7518e8afb87a7b1a96223dfeaf3705c734a9179cba1db15e4d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff96d5437c456f564ff126f6b28b77cc57c6bb67a074dd8c94acac244b1d4bde(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorDataCollectionRuleTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
