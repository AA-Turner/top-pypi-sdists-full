r'''
# `google_network_management_vpc_flow_logs_config`

Refer to the Terraform Registry for docs: [`google_network_management_vpc_flow_logs_config`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_management_vpc_flow_logs_config).
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


class NetworkManagementVpcFlowLogsConfig(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkManagementVpcFlowLogsConfig.NetworkManagementVpcFlowLogsConfig",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_management_vpc_flow_logs_config google_network_management_vpc_flow_logs_config}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        vpc_flow_logs_config_id: builtins.str,
        aggregation_interval: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        filter_expr: typing.Optional[builtins.str] = None,
        flow_sampling: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        interconnect_attachment: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        metadata: typing.Optional[builtins.str] = None,
        metadata_fields: typing.Optional[typing.Sequence[builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["NetworkManagementVpcFlowLogsConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        vpn_tunnel: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_management_vpc_flow_logs_config google_network_management_vpc_flow_logs_config} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: Resource ID segment making up resource 'name'. It identifies the resource within its parent collection as described in https://google.aip.dev/122. See documentation for resource type 'networkmanagement.googleapis.com/VpcFlowLogsConfig'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_management_vpc_flow_logs_config#location NetworkManagementVpcFlowLogsConfig#location}
        :param vpc_flow_logs_config_id: Required. ID of the 'VpcFlowLogsConfig'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_management_vpc_flow_logs_config#vpc_flow_logs_config_id NetworkManagementVpcFlowLogsConfig#vpc_flow_logs_config_id}
        :param aggregation_interval: Optional. The aggregation interval for the logs. Default value is INTERVAL_5_SEC. Possible values: AGGREGATION_INTERVAL_UNSPECIFIED INTERVAL_5_SEC INTERVAL_30_SEC INTERVAL_1_MIN INTERVAL_5_MIN INTERVAL_10_MIN INTERVAL_15_MIN" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_management_vpc_flow_logs_config#aggregation_interval NetworkManagementVpcFlowLogsConfig#aggregation_interval}
        :param description: Optional. The user-supplied description of the VPC Flow Logs configuration. Maximum of 512 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_management_vpc_flow_logs_config#description NetworkManagementVpcFlowLogsConfig#description}
        :param filter_expr: Optional. Export filter used to define which VPC Flow Logs should be logged. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_management_vpc_flow_logs_config#filter_expr NetworkManagementVpcFlowLogsConfig#filter_expr}
        :param flow_sampling: Optional. The value of the field must be in (0, 1]. The sampling rate of VPC Flow Logs where 1.0 means all collected logs are reported. Setting the sampling rate to 0.0 is not allowed. If you want to disable VPC Flow Logs, use the state field instead. Default value is 1.0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_management_vpc_flow_logs_config#flow_sampling NetworkManagementVpcFlowLogsConfig#flow_sampling}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_management_vpc_flow_logs_config#id NetworkManagementVpcFlowLogsConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param interconnect_attachment: Traffic will be logged from the Interconnect Attachment. Format: projects/{project_id}/regions/{region}/interconnectAttachments/{name}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_management_vpc_flow_logs_config#interconnect_attachment NetworkManagementVpcFlowLogsConfig#interconnect_attachment}
        :param labels: Optional. Resource labels to represent user-provided metadata. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_management_vpc_flow_logs_config#labels NetworkManagementVpcFlowLogsConfig#labels}
        :param metadata: Optional. Configures whether all, none or a subset of metadata fields should be added to the reported VPC flow logs. Default value is INCLUDE_ALL_METADATA. Possible values: METADATA_UNSPECIFIED INCLUDE_ALL_METADATA EXCLUDE_ALL_METADATA CUSTOM_METADATA Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_management_vpc_flow_logs_config#metadata NetworkManagementVpcFlowLogsConfig#metadata}
        :param metadata_fields: Optional. Custom metadata fields to include in the reported VPC flow logs. Can only be specified if "metadata" was set to CUSTOM_METADATA. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_management_vpc_flow_logs_config#metadata_fields NetworkManagementVpcFlowLogsConfig#metadata_fields}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_management_vpc_flow_logs_config#project NetworkManagementVpcFlowLogsConfig#project}.
        :param state: Optional. The state of the VPC Flow Log configuration. Default value is ENABLED. When creating a new configuration, it must be enabled. Possible Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_management_vpc_flow_logs_config#state NetworkManagementVpcFlowLogsConfig#state}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_management_vpc_flow_logs_config#timeouts NetworkManagementVpcFlowLogsConfig#timeouts}
        :param vpn_tunnel: Traffic will be logged from the VPN Tunnel. Format: projects/{project_id}/regions/{region}/vpnTunnels/{name}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_management_vpc_flow_logs_config#vpn_tunnel NetworkManagementVpcFlowLogsConfig#vpn_tunnel}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4fa3034b321ba0038474e845c5e38927053b32956a24f9abe98b65fc207643c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = NetworkManagementVpcFlowLogsConfigConfig(
            location=location,
            vpc_flow_logs_config_id=vpc_flow_logs_config_id,
            aggregation_interval=aggregation_interval,
            description=description,
            filter_expr=filter_expr,
            flow_sampling=flow_sampling,
            id=id,
            interconnect_attachment=interconnect_attachment,
            labels=labels,
            metadata=metadata,
            metadata_fields=metadata_fields,
            project=project,
            state=state,
            timeouts=timeouts,
            vpn_tunnel=vpn_tunnel,
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
        '''Generates CDKTF code for importing a NetworkManagementVpcFlowLogsConfig resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the NetworkManagementVpcFlowLogsConfig to import.
        :param import_from_id: The id of the existing NetworkManagementVpcFlowLogsConfig that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_management_vpc_flow_logs_config#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the NetworkManagementVpcFlowLogsConfig to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ab7cdf3888a279e5d7a20fcaeab0c0d388e4f983cf6808058470008a5c4fbdd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_management_vpc_flow_logs_config#create NetworkManagementVpcFlowLogsConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_management_vpc_flow_logs_config#delete NetworkManagementVpcFlowLogsConfig#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_management_vpc_flow_logs_config#update NetworkManagementVpcFlowLogsConfig#update}.
        '''
        value = NetworkManagementVpcFlowLogsConfigTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAggregationInterval")
    def reset_aggregation_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAggregationInterval", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetFilterExpr")
    def reset_filter_expr(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilterExpr", []))

    @jsii.member(jsii_name="resetFlowSampling")
    def reset_flow_sampling(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFlowSampling", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInterconnectAttachment")
    def reset_interconnect_attachment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInterconnectAttachment", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetMetadata")
    def reset_metadata(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetadata", []))

    @jsii.member(jsii_name="resetMetadataFields")
    def reset_metadata_fields(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetadataFields", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetState")
    def reset_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetState", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetVpnTunnel")
    def reset_vpn_tunnel(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVpnTunnel", []))

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
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "NetworkManagementVpcFlowLogsConfigTimeoutsOutputReference":
        return typing.cast("NetworkManagementVpcFlowLogsConfigTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="aggregationIntervalInput")
    def aggregation_interval_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aggregationIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="filterExprInput")
    def filter_expr_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filterExprInput"))

    @builtins.property
    @jsii.member(jsii_name="flowSamplingInput")
    def flow_sampling_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "flowSamplingInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="interconnectAttachmentInput")
    def interconnect_attachment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "interconnectAttachmentInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataFieldsInput")
    def metadata_fields_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "metadataFieldsInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataInput")
    def metadata_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metadataInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="stateInput")
    def state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stateInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "NetworkManagementVpcFlowLogsConfigTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "NetworkManagementVpcFlowLogsConfigTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcFlowLogsConfigIdInput")
    def vpc_flow_logs_config_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcFlowLogsConfigIdInput"))

    @builtins.property
    @jsii.member(jsii_name="vpnTunnelInput")
    def vpn_tunnel_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpnTunnelInput"))

    @builtins.property
    @jsii.member(jsii_name="aggregationInterval")
    def aggregation_interval(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "aggregationInterval"))

    @aggregation_interval.setter
    def aggregation_interval(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97f062a928abdbb4bd75b0ad3dd81cd7563b88113fdd07c03572cc80b7394314)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "aggregationInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36da1a02b7a4481ff9bdb94edce5a325f8be86ea9356721730c8a41cfc71ae7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="filterExpr")
    def filter_expr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filterExpr"))

    @filter_expr.setter
    def filter_expr(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5247c528a2ab1a258fd729a584eab7671f48b4aa6d0e922e35a98a9eda4fea5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filterExpr", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="flowSampling")
    def flow_sampling(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "flowSampling"))

    @flow_sampling.setter
    def flow_sampling(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78c9c388624711429f37f5bfb661e4e9c43a18df0e690ea58d8628935c6f4c41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "flowSampling", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c8df138ff4ee8bdae44f7c9f8ead4a40daf54aeefb84aba27edee3ef13b4002)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="interconnectAttachment")
    def interconnect_attachment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "interconnectAttachment"))

    @interconnect_attachment.setter
    def interconnect_attachment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__017370a13a244123af496ff53e7f00504a0c101620f7c11df87064f13d4eddeb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interconnectAttachment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee1d6b8f4fb6638aa27d514a9c21b1e8f1c9cb1c94351bbc8aab1d9017c5ef79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6896a940eabf0f6049cfd6dc4155e8b18d55cb39bc2fc1b3bb7064c5fc6af0d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metadata"))

    @metadata.setter
    def metadata(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15e9d10330ca296bb0d60195e6ef7fe5cf4c5fdbb6a67356e7136690d3d92e6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadata", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metadataFields")
    def metadata_fields(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "metadataFields"))

    @metadata_fields.setter
    def metadata_fields(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7c74483b3394ec8a2142b11baa813bf9e711d85ec6655bf663205438327ce83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadataFields", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91858bf6ba97ce4c8fb41d711732ca9eebbc77876e6f4b27615325fa717bf04b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @state.setter
    def state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f1c46ab96081bc744e164c87118efed072d5a8dacb3a8131c34e4f49e443928)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpcFlowLogsConfigId")
    def vpc_flow_logs_config_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcFlowLogsConfigId"))

    @vpc_flow_logs_config_id.setter
    def vpc_flow_logs_config_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2580ada309b7e51a92786961d774ca778a45c4f7c0e9bee3bb410f8a8010c89a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcFlowLogsConfigId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpnTunnel")
    def vpn_tunnel(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpnTunnel"))

    @vpn_tunnel.setter
    def vpn_tunnel(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e3ba2fc317a0787a2238436be612dc9e8fab7865a6a2fb4d1b739a1cc81ccbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpnTunnel", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkManagementVpcFlowLogsConfig.NetworkManagementVpcFlowLogsConfigConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "location": "location",
        "vpc_flow_logs_config_id": "vpcFlowLogsConfigId",
        "aggregation_interval": "aggregationInterval",
        "description": "description",
        "filter_expr": "filterExpr",
        "flow_sampling": "flowSampling",
        "id": "id",
        "interconnect_attachment": "interconnectAttachment",
        "labels": "labels",
        "metadata": "metadata",
        "metadata_fields": "metadataFields",
        "project": "project",
        "state": "state",
        "timeouts": "timeouts",
        "vpn_tunnel": "vpnTunnel",
    },
)
class NetworkManagementVpcFlowLogsConfigConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        location: builtins.str,
        vpc_flow_logs_config_id: builtins.str,
        aggregation_interval: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        filter_expr: typing.Optional[builtins.str] = None,
        flow_sampling: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        interconnect_attachment: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        metadata: typing.Optional[builtins.str] = None,
        metadata_fields: typing.Optional[typing.Sequence[builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["NetworkManagementVpcFlowLogsConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        vpn_tunnel: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: Resource ID segment making up resource 'name'. It identifies the resource within its parent collection as described in https://google.aip.dev/122. See documentation for resource type 'networkmanagement.googleapis.com/VpcFlowLogsConfig'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_management_vpc_flow_logs_config#location NetworkManagementVpcFlowLogsConfig#location}
        :param vpc_flow_logs_config_id: Required. ID of the 'VpcFlowLogsConfig'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_management_vpc_flow_logs_config#vpc_flow_logs_config_id NetworkManagementVpcFlowLogsConfig#vpc_flow_logs_config_id}
        :param aggregation_interval: Optional. The aggregation interval for the logs. Default value is INTERVAL_5_SEC. Possible values: AGGREGATION_INTERVAL_UNSPECIFIED INTERVAL_5_SEC INTERVAL_30_SEC INTERVAL_1_MIN INTERVAL_5_MIN INTERVAL_10_MIN INTERVAL_15_MIN" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_management_vpc_flow_logs_config#aggregation_interval NetworkManagementVpcFlowLogsConfig#aggregation_interval}
        :param description: Optional. The user-supplied description of the VPC Flow Logs configuration. Maximum of 512 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_management_vpc_flow_logs_config#description NetworkManagementVpcFlowLogsConfig#description}
        :param filter_expr: Optional. Export filter used to define which VPC Flow Logs should be logged. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_management_vpc_flow_logs_config#filter_expr NetworkManagementVpcFlowLogsConfig#filter_expr}
        :param flow_sampling: Optional. The value of the field must be in (0, 1]. The sampling rate of VPC Flow Logs where 1.0 means all collected logs are reported. Setting the sampling rate to 0.0 is not allowed. If you want to disable VPC Flow Logs, use the state field instead. Default value is 1.0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_management_vpc_flow_logs_config#flow_sampling NetworkManagementVpcFlowLogsConfig#flow_sampling}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_management_vpc_flow_logs_config#id NetworkManagementVpcFlowLogsConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param interconnect_attachment: Traffic will be logged from the Interconnect Attachment. Format: projects/{project_id}/regions/{region}/interconnectAttachments/{name}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_management_vpc_flow_logs_config#interconnect_attachment NetworkManagementVpcFlowLogsConfig#interconnect_attachment}
        :param labels: Optional. Resource labels to represent user-provided metadata. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_management_vpc_flow_logs_config#labels NetworkManagementVpcFlowLogsConfig#labels}
        :param metadata: Optional. Configures whether all, none or a subset of metadata fields should be added to the reported VPC flow logs. Default value is INCLUDE_ALL_METADATA. Possible values: METADATA_UNSPECIFIED INCLUDE_ALL_METADATA EXCLUDE_ALL_METADATA CUSTOM_METADATA Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_management_vpc_flow_logs_config#metadata NetworkManagementVpcFlowLogsConfig#metadata}
        :param metadata_fields: Optional. Custom metadata fields to include in the reported VPC flow logs. Can only be specified if "metadata" was set to CUSTOM_METADATA. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_management_vpc_flow_logs_config#metadata_fields NetworkManagementVpcFlowLogsConfig#metadata_fields}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_management_vpc_flow_logs_config#project NetworkManagementVpcFlowLogsConfig#project}.
        :param state: Optional. The state of the VPC Flow Log configuration. Default value is ENABLED. When creating a new configuration, it must be enabled. Possible Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_management_vpc_flow_logs_config#state NetworkManagementVpcFlowLogsConfig#state}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_management_vpc_flow_logs_config#timeouts NetworkManagementVpcFlowLogsConfig#timeouts}
        :param vpn_tunnel: Traffic will be logged from the VPN Tunnel. Format: projects/{project_id}/regions/{region}/vpnTunnels/{name}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_management_vpc_flow_logs_config#vpn_tunnel NetworkManagementVpcFlowLogsConfig#vpn_tunnel}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = NetworkManagementVpcFlowLogsConfigTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bb438a75614f67b05a7844f03064b5c977c09f268d4f3fec811a0588e6d1ff7)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument vpc_flow_logs_config_id", value=vpc_flow_logs_config_id, expected_type=type_hints["vpc_flow_logs_config_id"])
            check_type(argname="argument aggregation_interval", value=aggregation_interval, expected_type=type_hints["aggregation_interval"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument filter_expr", value=filter_expr, expected_type=type_hints["filter_expr"])
            check_type(argname="argument flow_sampling", value=flow_sampling, expected_type=type_hints["flow_sampling"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument interconnect_attachment", value=interconnect_attachment, expected_type=type_hints["interconnect_attachment"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument metadata_fields", value=metadata_fields, expected_type=type_hints["metadata_fields"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument vpn_tunnel", value=vpn_tunnel, expected_type=type_hints["vpn_tunnel"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
            "vpc_flow_logs_config_id": vpc_flow_logs_config_id,
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
        if aggregation_interval is not None:
            self._values["aggregation_interval"] = aggregation_interval
        if description is not None:
            self._values["description"] = description
        if filter_expr is not None:
            self._values["filter_expr"] = filter_expr
        if flow_sampling is not None:
            self._values["flow_sampling"] = flow_sampling
        if id is not None:
            self._values["id"] = id
        if interconnect_attachment is not None:
            self._values["interconnect_attachment"] = interconnect_attachment
        if labels is not None:
            self._values["labels"] = labels
        if metadata is not None:
            self._values["metadata"] = metadata
        if metadata_fields is not None:
            self._values["metadata_fields"] = metadata_fields
        if project is not None:
            self._values["project"] = project
        if state is not None:
            self._values["state"] = state
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if vpn_tunnel is not None:
            self._values["vpn_tunnel"] = vpn_tunnel

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
    def location(self) -> builtins.str:
        '''Resource ID segment making up resource 'name'.

        It identifies the resource
        within its parent collection as described in https://google.aip.dev/122. See documentation
        for resource type 'networkmanagement.googleapis.com/VpcFlowLogsConfig'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_management_vpc_flow_logs_config#location NetworkManagementVpcFlowLogsConfig#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vpc_flow_logs_config_id(self) -> builtins.str:
        '''Required. ID of the 'VpcFlowLogsConfig'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_management_vpc_flow_logs_config#vpc_flow_logs_config_id NetworkManagementVpcFlowLogsConfig#vpc_flow_logs_config_id}
        '''
        result = self._values.get("vpc_flow_logs_config_id")
        assert result is not None, "Required property 'vpc_flow_logs_config_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def aggregation_interval(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The aggregation interval for the logs. Default value is
        INTERVAL_5_SEC.   Possible values:  AGGREGATION_INTERVAL_UNSPECIFIED INTERVAL_5_SEC INTERVAL_30_SEC INTERVAL_1_MIN INTERVAL_5_MIN INTERVAL_10_MIN INTERVAL_15_MIN"

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_management_vpc_flow_logs_config#aggregation_interval NetworkManagementVpcFlowLogsConfig#aggregation_interval}
        '''
        result = self._values.get("aggregation_interval")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Optional. The user-supplied description of the VPC Flow Logs configuration. Maximum of 512 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_management_vpc_flow_logs_config#description NetworkManagementVpcFlowLogsConfig#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def filter_expr(self) -> typing.Optional[builtins.str]:
        '''Optional. Export filter used to define which VPC Flow Logs should be logged.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_management_vpc_flow_logs_config#filter_expr NetworkManagementVpcFlowLogsConfig#filter_expr}
        '''
        result = self._values.get("filter_expr")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def flow_sampling(self) -> typing.Optional[jsii.Number]:
        '''Optional.

        The value of the field must be in (0, 1]. The sampling rate
        of VPC Flow Logs where 1.0 means all collected logs are reported. Setting the
        sampling rate to 0.0 is not allowed. If you want to disable VPC Flow Logs, use
        the state field instead. Default value is 1.0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_management_vpc_flow_logs_config#flow_sampling NetworkManagementVpcFlowLogsConfig#flow_sampling}
        '''
        result = self._values.get("flow_sampling")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_management_vpc_flow_logs_config#id NetworkManagementVpcFlowLogsConfig#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def interconnect_attachment(self) -> typing.Optional[builtins.str]:
        '''Traffic will be logged from the Interconnect Attachment. Format: projects/{project_id}/regions/{region}/interconnectAttachments/{name}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_management_vpc_flow_logs_config#interconnect_attachment NetworkManagementVpcFlowLogsConfig#interconnect_attachment}
        '''
        result = self._values.get("interconnect_attachment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional. Resource labels to represent user-provided metadata.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_management_vpc_flow_logs_config#labels NetworkManagementVpcFlowLogsConfig#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def metadata(self) -> typing.Optional[builtins.str]:
        '''Optional.

        Configures whether all, none or a subset of metadata fields
        should be added to the reported VPC flow logs. Default value is INCLUDE_ALL_METADATA.
        Possible values:  METADATA_UNSPECIFIED INCLUDE_ALL_METADATA EXCLUDE_ALL_METADATA CUSTOM_METADATA

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_management_vpc_flow_logs_config#metadata NetworkManagementVpcFlowLogsConfig#metadata}
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metadata_fields(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional.

        Custom metadata fields to include in the reported VPC flow
        logs. Can only be specified if "metadata" was set to CUSTOM_METADATA.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_management_vpc_flow_logs_config#metadata_fields NetworkManagementVpcFlowLogsConfig#metadata_fields}
        '''
        result = self._values.get("metadata_fields")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_management_vpc_flow_logs_config#project NetworkManagementVpcFlowLogsConfig#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def state(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The state of the VPC Flow Log configuration. Default value
        is ENABLED. When creating a new configuration, it must be enabled.   Possible

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_management_vpc_flow_logs_config#state NetworkManagementVpcFlowLogsConfig#state}
        '''
        result = self._values.get("state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["NetworkManagementVpcFlowLogsConfigTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_management_vpc_flow_logs_config#timeouts NetworkManagementVpcFlowLogsConfig#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["NetworkManagementVpcFlowLogsConfigTimeouts"], result)

    @builtins.property
    def vpn_tunnel(self) -> typing.Optional[builtins.str]:
        '''Traffic will be logged from the VPN Tunnel. Format: projects/{project_id}/regions/{region}/vpnTunnels/{name}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_management_vpc_flow_logs_config#vpn_tunnel NetworkManagementVpcFlowLogsConfig#vpn_tunnel}
        '''
        result = self._values.get("vpn_tunnel")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkManagementVpcFlowLogsConfigConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkManagementVpcFlowLogsConfig.NetworkManagementVpcFlowLogsConfigTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class NetworkManagementVpcFlowLogsConfigTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_management_vpc_flow_logs_config#create NetworkManagementVpcFlowLogsConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_management_vpc_flow_logs_config#delete NetworkManagementVpcFlowLogsConfig#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_management_vpc_flow_logs_config#update NetworkManagementVpcFlowLogsConfig#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95850767ea7862ab877a7b48fcfe738a60b5b3a2dd3683dc956ba22c73846731)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_management_vpc_flow_logs_config#create NetworkManagementVpcFlowLogsConfig#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_management_vpc_flow_logs_config#delete NetworkManagementVpcFlowLogsConfig#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_management_vpc_flow_logs_config#update NetworkManagementVpcFlowLogsConfig#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkManagementVpcFlowLogsConfigTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkManagementVpcFlowLogsConfigTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkManagementVpcFlowLogsConfig.NetworkManagementVpcFlowLogsConfigTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e458fe459bc8b3636b0881ae47fe573cb4274b68ba205d7e918ba5ae3717869a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c8ca32f84c8285477c7ec2eda27c9ec4a1a223dd48e9250f2e1e1278b6937d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4faea996e5e1b841e32d9b00dd58a7622cd30b5b6929a32ce10e9d162f1c74f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0a5ac3a2b1dcdd4d14e08106a64e8f81c7283437ac39a4b08beb998062e33ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkManagementVpcFlowLogsConfigTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkManagementVpcFlowLogsConfigTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkManagementVpcFlowLogsConfigTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fa7e729fb0b2f8ff0071affe9dd78614b93d9cd3d13745d98acaabb76ccd17c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "NetworkManagementVpcFlowLogsConfig",
    "NetworkManagementVpcFlowLogsConfigConfig",
    "NetworkManagementVpcFlowLogsConfigTimeouts",
    "NetworkManagementVpcFlowLogsConfigTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__d4fa3034b321ba0038474e845c5e38927053b32956a24f9abe98b65fc207643c(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    vpc_flow_logs_config_id: builtins.str,
    aggregation_interval: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    filter_expr: typing.Optional[builtins.str] = None,
    flow_sampling: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    interconnect_attachment: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    metadata: typing.Optional[builtins.str] = None,
    metadata_fields: typing.Optional[typing.Sequence[builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[NetworkManagementVpcFlowLogsConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    vpn_tunnel: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__4ab7cdf3888a279e5d7a20fcaeab0c0d388e4f983cf6808058470008a5c4fbdd(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97f062a928abdbb4bd75b0ad3dd81cd7563b88113fdd07c03572cc80b7394314(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36da1a02b7a4481ff9bdb94edce5a325f8be86ea9356721730c8a41cfc71ae7c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5247c528a2ab1a258fd729a584eab7671f48b4aa6d0e922e35a98a9eda4fea5d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78c9c388624711429f37f5bfb661e4e9c43a18df0e690ea58d8628935c6f4c41(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c8df138ff4ee8bdae44f7c9f8ead4a40daf54aeefb84aba27edee3ef13b4002(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__017370a13a244123af496ff53e7f00504a0c101620f7c11df87064f13d4eddeb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee1d6b8f4fb6638aa27d514a9c21b1e8f1c9cb1c94351bbc8aab1d9017c5ef79(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6896a940eabf0f6049cfd6dc4155e8b18d55cb39bc2fc1b3bb7064c5fc6af0d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15e9d10330ca296bb0d60195e6ef7fe5cf4c5fdbb6a67356e7136690d3d92e6a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7c74483b3394ec8a2142b11baa813bf9e711d85ec6655bf663205438327ce83(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91858bf6ba97ce4c8fb41d711732ca9eebbc77876e6f4b27615325fa717bf04b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f1c46ab96081bc744e164c87118efed072d5a8dacb3a8131c34e4f49e443928(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2580ada309b7e51a92786961d774ca778a45c4f7c0e9bee3bb410f8a8010c89a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e3ba2fc317a0787a2238436be612dc9e8fab7865a6a2fb4d1b739a1cc81ccbd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bb438a75614f67b05a7844f03064b5c977c09f268d4f3fec811a0588e6d1ff7(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location: builtins.str,
    vpc_flow_logs_config_id: builtins.str,
    aggregation_interval: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    filter_expr: typing.Optional[builtins.str] = None,
    flow_sampling: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    interconnect_attachment: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    metadata: typing.Optional[builtins.str] = None,
    metadata_fields: typing.Optional[typing.Sequence[builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[NetworkManagementVpcFlowLogsConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    vpn_tunnel: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95850767ea7862ab877a7b48fcfe738a60b5b3a2dd3683dc956ba22c73846731(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e458fe459bc8b3636b0881ae47fe573cb4274b68ba205d7e918ba5ae3717869a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c8ca32f84c8285477c7ec2eda27c9ec4a1a223dd48e9250f2e1e1278b6937d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4faea996e5e1b841e32d9b00dd58a7622cd30b5b6929a32ce10e9d162f1c74f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0a5ac3a2b1dcdd4d14e08106a64e8f81c7283437ac39a4b08beb998062e33ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fa7e729fb0b2f8ff0071affe9dd78614b93d9cd3d13745d98acaabb76ccd17c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkManagementVpcFlowLogsConfigTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
