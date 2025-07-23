r'''
# `google_network_connectivity_policy_based_route`

Refer to the Terraform Registry for docs: [`google_network_connectivity_policy_based_route`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_policy_based_route).
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


class NetworkConnectivityPolicyBasedRoute(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkConnectivityPolicyBasedRoute.NetworkConnectivityPolicyBasedRoute",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_policy_based_route google_network_connectivity_policy_based_route}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        filter: typing.Union["NetworkConnectivityPolicyBasedRouteFilter", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        network: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        interconnect_attachment: typing.Optional[typing.Union["NetworkConnectivityPolicyBasedRouteInterconnectAttachment", typing.Dict[builtins.str, typing.Any]]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        next_hop_ilb_ip: typing.Optional[builtins.str] = None,
        next_hop_other_routes: typing.Optional[builtins.str] = None,
        priority: typing.Optional[jsii.Number] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["NetworkConnectivityPolicyBasedRouteTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        virtual_machine: typing.Optional[typing.Union["NetworkConnectivityPolicyBasedRouteVirtualMachine", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_policy_based_route google_network_connectivity_policy_based_route} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param filter: filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_policy_based_route#filter NetworkConnectivityPolicyBasedRoute#filter}
        :param name: The name of the policy based route. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_policy_based_route#name NetworkConnectivityPolicyBasedRoute#name}
        :param network: Fully-qualified URL of the network that this route applies to, for example: projects/my-project/global/networks/my-network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_policy_based_route#network NetworkConnectivityPolicyBasedRoute#network}
        :param description: An optional description of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_policy_based_route#description NetworkConnectivityPolicyBasedRoute#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_policy_based_route#id NetworkConnectivityPolicyBasedRoute#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param interconnect_attachment: interconnect_attachment block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_policy_based_route#interconnect_attachment NetworkConnectivityPolicyBasedRoute#interconnect_attachment}
        :param labels: User-defined labels. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_policy_based_route#labels NetworkConnectivityPolicyBasedRoute#labels}
        :param next_hop_ilb_ip: The IP address of a global-access-enabled L4 ILB that is the next hop for matching packets. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_policy_based_route#next_hop_ilb_ip NetworkConnectivityPolicyBasedRoute#next_hop_ilb_ip}
        :param next_hop_other_routes: Other routes that will be referenced to determine the next hop of the packet. Possible values: ["DEFAULT_ROUTING"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_policy_based_route#next_hop_other_routes NetworkConnectivityPolicyBasedRoute#next_hop_other_routes}
        :param priority: The priority of this policy-based route. Priority is used to break ties in cases where there are more than one matching policy-based routes found. In cases where multiple policy-based routes are matched, the one with the lowest-numbered priority value wins. The default value is 1000. The priority value must be from 1 to 65535, inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_policy_based_route#priority NetworkConnectivityPolicyBasedRoute#priority}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_policy_based_route#project NetworkConnectivityPolicyBasedRoute#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_policy_based_route#timeouts NetworkConnectivityPolicyBasedRoute#timeouts}
        :param virtual_machine: virtual_machine block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_policy_based_route#virtual_machine NetworkConnectivityPolicyBasedRoute#virtual_machine}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b208f6b69aefa19871d69586ff5ada47d85b98e157591430c68fee885feb83b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = NetworkConnectivityPolicyBasedRouteConfig(
            filter=filter,
            name=name,
            network=network,
            description=description,
            id=id,
            interconnect_attachment=interconnect_attachment,
            labels=labels,
            next_hop_ilb_ip=next_hop_ilb_ip,
            next_hop_other_routes=next_hop_other_routes,
            priority=priority,
            project=project,
            timeouts=timeouts,
            virtual_machine=virtual_machine,
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
        '''Generates CDKTF code for importing a NetworkConnectivityPolicyBasedRoute resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the NetworkConnectivityPolicyBasedRoute to import.
        :param import_from_id: The id of the existing NetworkConnectivityPolicyBasedRoute that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_policy_based_route#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the NetworkConnectivityPolicyBasedRoute to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b0a45995e900ca623bd73600be052dc59347803837ed4b545e5c85caa402e41)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putFilter")
    def put_filter(
        self,
        *,
        protocol_version: builtins.str,
        dest_range: typing.Optional[builtins.str] = None,
        ip_protocol: typing.Optional[builtins.str] = None,
        src_range: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param protocol_version: Internet protocol versions this policy-based route applies to. Possible values: ["IPV4", "IPV6"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_policy_based_route#protocol_version NetworkConnectivityPolicyBasedRoute#protocol_version}
        :param dest_range: The destination IP range of outgoing packets that this policy-based route applies to. Default is "0.0.0.0/0". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_policy_based_route#dest_range NetworkConnectivityPolicyBasedRoute#dest_range}
        :param ip_protocol: The IP protocol that this policy-based route applies to. Valid values are 'TCP', 'UDP', and 'ALL'. Default is 'ALL'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_policy_based_route#ip_protocol NetworkConnectivityPolicyBasedRoute#ip_protocol}
        :param src_range: The source IP range of outgoing packets that this policy-based route applies to. Default is "0.0.0.0/0". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_policy_based_route#src_range NetworkConnectivityPolicyBasedRoute#src_range}
        '''
        value = NetworkConnectivityPolicyBasedRouteFilter(
            protocol_version=protocol_version,
            dest_range=dest_range,
            ip_protocol=ip_protocol,
            src_range=src_range,
        )

        return typing.cast(None, jsii.invoke(self, "putFilter", [value]))

    @jsii.member(jsii_name="putInterconnectAttachment")
    def put_interconnect_attachment(self, *, region: builtins.str) -> None:
        '''
        :param region: Cloud region to install this policy-based route on for Interconnect attachments. Use 'all' to install it on all Interconnect attachments. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_policy_based_route#region NetworkConnectivityPolicyBasedRoute#region}
        '''
        value = NetworkConnectivityPolicyBasedRouteInterconnectAttachment(
            region=region
        )

        return typing.cast(None, jsii.invoke(self, "putInterconnectAttachment", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_policy_based_route#create NetworkConnectivityPolicyBasedRoute#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_policy_based_route#delete NetworkConnectivityPolicyBasedRoute#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_policy_based_route#update NetworkConnectivityPolicyBasedRoute#update}.
        '''
        value = NetworkConnectivityPolicyBasedRouteTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putVirtualMachine")
    def put_virtual_machine(self, *, tags: typing.Sequence[builtins.str]) -> None:
        '''
        :param tags: A list of VM instance tags that this policy-based route applies to. VM instances that have ANY of tags specified here will install this PBR. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_policy_based_route#tags NetworkConnectivityPolicyBasedRoute#tags}
        '''
        value = NetworkConnectivityPolicyBasedRouteVirtualMachine(tags=tags)

        return typing.cast(None, jsii.invoke(self, "putVirtualMachine", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInterconnectAttachment")
    def reset_interconnect_attachment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInterconnectAttachment", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetNextHopIlbIp")
    def reset_next_hop_ilb_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNextHopIlbIp", []))

    @jsii.member(jsii_name="resetNextHopOtherRoutes")
    def reset_next_hop_other_routes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNextHopOtherRoutes", []))

    @jsii.member(jsii_name="resetPriority")
    def reset_priority(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPriority", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetVirtualMachine")
    def reset_virtual_machine(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVirtualMachine", []))

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
    @jsii.member(jsii_name="filter")
    def filter(self) -> "NetworkConnectivityPolicyBasedRouteFilterOutputReference":
        return typing.cast("NetworkConnectivityPolicyBasedRouteFilterOutputReference", jsii.get(self, "filter"))

    @builtins.property
    @jsii.member(jsii_name="interconnectAttachment")
    def interconnect_attachment(
        self,
    ) -> "NetworkConnectivityPolicyBasedRouteInterconnectAttachmentOutputReference":
        return typing.cast("NetworkConnectivityPolicyBasedRouteInterconnectAttachmentOutputReference", jsii.get(self, "interconnectAttachment"))

    @builtins.property
    @jsii.member(jsii_name="kind")
    def kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kind"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "NetworkConnectivityPolicyBasedRouteTimeoutsOutputReference":
        return typing.cast("NetworkConnectivityPolicyBasedRouteTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="virtualMachine")
    def virtual_machine(
        self,
    ) -> "NetworkConnectivityPolicyBasedRouteVirtualMachineOutputReference":
        return typing.cast("NetworkConnectivityPolicyBasedRouteVirtualMachineOutputReference", jsii.get(self, "virtualMachine"))

    @builtins.property
    @jsii.member(jsii_name="warnings")
    def warnings(self) -> "NetworkConnectivityPolicyBasedRouteWarningsList":
        return typing.cast("NetworkConnectivityPolicyBasedRouteWarningsList", jsii.get(self, "warnings"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="filterInput")
    def filter_input(
        self,
    ) -> typing.Optional["NetworkConnectivityPolicyBasedRouteFilter"]:
        return typing.cast(typing.Optional["NetworkConnectivityPolicyBasedRouteFilter"], jsii.get(self, "filterInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="interconnectAttachmentInput")
    def interconnect_attachment_input(
        self,
    ) -> typing.Optional["NetworkConnectivityPolicyBasedRouteInterconnectAttachment"]:
        return typing.cast(typing.Optional["NetworkConnectivityPolicyBasedRouteInterconnectAttachment"], jsii.get(self, "interconnectAttachmentInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkInput")
    def network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkInput"))

    @builtins.property
    @jsii.member(jsii_name="nextHopIlbIpInput")
    def next_hop_ilb_ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nextHopIlbIpInput"))

    @builtins.property
    @jsii.member(jsii_name="nextHopOtherRoutesInput")
    def next_hop_other_routes_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nextHopOtherRoutesInput"))

    @builtins.property
    @jsii.member(jsii_name="priorityInput")
    def priority_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "priorityInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "NetworkConnectivityPolicyBasedRouteTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "NetworkConnectivityPolicyBasedRouteTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualMachineInput")
    def virtual_machine_input(
        self,
    ) -> typing.Optional["NetworkConnectivityPolicyBasedRouteVirtualMachine"]:
        return typing.cast(typing.Optional["NetworkConnectivityPolicyBasedRouteVirtualMachine"], jsii.get(self, "virtualMachineInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e30aad89e69f2825664a23d5b0cbb31268e23a051f67de51cc6df7865076e3c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b331175473822a3d8ecdb561f79552a7c86b1a63a892a6d0efd3cc7688ecbce8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b17e4b6f4433d86408b981a59156b460354a1d72ea6de3110553afad8df531e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee822153149bf813d1e724a8cde7e7af2f317e8e4d160089133f8158924ad89e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__447a737d15edf18c640dc6491561597bd9b1bbf2632049465eab5a8f5bd521a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nextHopIlbIp")
    def next_hop_ilb_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nextHopIlbIp"))

    @next_hop_ilb_ip.setter
    def next_hop_ilb_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c2e53cfcb9d584f05b39d004d44ee5fa5b64463f918dcc6fc3c76fc41053539)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nextHopIlbIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nextHopOtherRoutes")
    def next_hop_other_routes(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nextHopOtherRoutes"))

    @next_hop_other_routes.setter
    def next_hop_other_routes(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__362bb97bc203eb2000874e72cc5dc64825a8ec16cd0cb27b63f36991a718a552)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nextHopOtherRoutes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c29c3bcbb20aa13b14a2dd347878574d00e19ad54f8fc104e0bc62bafc86d48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6db248f56ac3533ff4692b08b8d71cdeaff172bcb4eab553fc43b3eaf6a4cb34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkConnectivityPolicyBasedRoute.NetworkConnectivityPolicyBasedRouteConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "filter": "filter",
        "name": "name",
        "network": "network",
        "description": "description",
        "id": "id",
        "interconnect_attachment": "interconnectAttachment",
        "labels": "labels",
        "next_hop_ilb_ip": "nextHopIlbIp",
        "next_hop_other_routes": "nextHopOtherRoutes",
        "priority": "priority",
        "project": "project",
        "timeouts": "timeouts",
        "virtual_machine": "virtualMachine",
    },
)
class NetworkConnectivityPolicyBasedRouteConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        filter: typing.Union["NetworkConnectivityPolicyBasedRouteFilter", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        network: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        interconnect_attachment: typing.Optional[typing.Union["NetworkConnectivityPolicyBasedRouteInterconnectAttachment", typing.Dict[builtins.str, typing.Any]]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        next_hop_ilb_ip: typing.Optional[builtins.str] = None,
        next_hop_other_routes: typing.Optional[builtins.str] = None,
        priority: typing.Optional[jsii.Number] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["NetworkConnectivityPolicyBasedRouteTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        virtual_machine: typing.Optional[typing.Union["NetworkConnectivityPolicyBasedRouteVirtualMachine", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param filter: filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_policy_based_route#filter NetworkConnectivityPolicyBasedRoute#filter}
        :param name: The name of the policy based route. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_policy_based_route#name NetworkConnectivityPolicyBasedRoute#name}
        :param network: Fully-qualified URL of the network that this route applies to, for example: projects/my-project/global/networks/my-network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_policy_based_route#network NetworkConnectivityPolicyBasedRoute#network}
        :param description: An optional description of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_policy_based_route#description NetworkConnectivityPolicyBasedRoute#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_policy_based_route#id NetworkConnectivityPolicyBasedRoute#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param interconnect_attachment: interconnect_attachment block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_policy_based_route#interconnect_attachment NetworkConnectivityPolicyBasedRoute#interconnect_attachment}
        :param labels: User-defined labels. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_policy_based_route#labels NetworkConnectivityPolicyBasedRoute#labels}
        :param next_hop_ilb_ip: The IP address of a global-access-enabled L4 ILB that is the next hop for matching packets. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_policy_based_route#next_hop_ilb_ip NetworkConnectivityPolicyBasedRoute#next_hop_ilb_ip}
        :param next_hop_other_routes: Other routes that will be referenced to determine the next hop of the packet. Possible values: ["DEFAULT_ROUTING"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_policy_based_route#next_hop_other_routes NetworkConnectivityPolicyBasedRoute#next_hop_other_routes}
        :param priority: The priority of this policy-based route. Priority is used to break ties in cases where there are more than one matching policy-based routes found. In cases where multiple policy-based routes are matched, the one with the lowest-numbered priority value wins. The default value is 1000. The priority value must be from 1 to 65535, inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_policy_based_route#priority NetworkConnectivityPolicyBasedRoute#priority}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_policy_based_route#project NetworkConnectivityPolicyBasedRoute#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_policy_based_route#timeouts NetworkConnectivityPolicyBasedRoute#timeouts}
        :param virtual_machine: virtual_machine block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_policy_based_route#virtual_machine NetworkConnectivityPolicyBasedRoute#virtual_machine}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(filter, dict):
            filter = NetworkConnectivityPolicyBasedRouteFilter(**filter)
        if isinstance(interconnect_attachment, dict):
            interconnect_attachment = NetworkConnectivityPolicyBasedRouteInterconnectAttachment(**interconnect_attachment)
        if isinstance(timeouts, dict):
            timeouts = NetworkConnectivityPolicyBasedRouteTimeouts(**timeouts)
        if isinstance(virtual_machine, dict):
            virtual_machine = NetworkConnectivityPolicyBasedRouteVirtualMachine(**virtual_machine)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db634a31cf482c143b02fc3dd610cc2908af7232109b31e9aacd4f89efacf732)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument interconnect_attachment", value=interconnect_attachment, expected_type=type_hints["interconnect_attachment"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument next_hop_ilb_ip", value=next_hop_ilb_ip, expected_type=type_hints["next_hop_ilb_ip"])
            check_type(argname="argument next_hop_other_routes", value=next_hop_other_routes, expected_type=type_hints["next_hop_other_routes"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument virtual_machine", value=virtual_machine, expected_type=type_hints["virtual_machine"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "filter": filter,
            "name": name,
            "network": network,
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
        if id is not None:
            self._values["id"] = id
        if interconnect_attachment is not None:
            self._values["interconnect_attachment"] = interconnect_attachment
        if labels is not None:
            self._values["labels"] = labels
        if next_hop_ilb_ip is not None:
            self._values["next_hop_ilb_ip"] = next_hop_ilb_ip
        if next_hop_other_routes is not None:
            self._values["next_hop_other_routes"] = next_hop_other_routes
        if priority is not None:
            self._values["priority"] = priority
        if project is not None:
            self._values["project"] = project
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if virtual_machine is not None:
            self._values["virtual_machine"] = virtual_machine

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
    def filter(self) -> "NetworkConnectivityPolicyBasedRouteFilter":
        '''filter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_policy_based_route#filter NetworkConnectivityPolicyBasedRoute#filter}
        '''
        result = self._values.get("filter")
        assert result is not None, "Required property 'filter' is missing"
        return typing.cast("NetworkConnectivityPolicyBasedRouteFilter", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the policy based route.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_policy_based_route#name NetworkConnectivityPolicyBasedRoute#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def network(self) -> builtins.str:
        '''Fully-qualified URL of the network that this route applies to, for example: projects/my-project/global/networks/my-network.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_policy_based_route#network NetworkConnectivityPolicyBasedRoute#network}
        '''
        result = self._values.get("network")
        assert result is not None, "Required property 'network' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_policy_based_route#description NetworkConnectivityPolicyBasedRoute#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_policy_based_route#id NetworkConnectivityPolicyBasedRoute#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def interconnect_attachment(
        self,
    ) -> typing.Optional["NetworkConnectivityPolicyBasedRouteInterconnectAttachment"]:
        '''interconnect_attachment block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_policy_based_route#interconnect_attachment NetworkConnectivityPolicyBasedRoute#interconnect_attachment}
        '''
        result = self._values.get("interconnect_attachment")
        return typing.cast(typing.Optional["NetworkConnectivityPolicyBasedRouteInterconnectAttachment"], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''User-defined labels.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_policy_based_route#labels NetworkConnectivityPolicyBasedRoute#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def next_hop_ilb_ip(self) -> typing.Optional[builtins.str]:
        '''The IP address of a global-access-enabled L4 ILB that is the next hop for matching packets.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_policy_based_route#next_hop_ilb_ip NetworkConnectivityPolicyBasedRoute#next_hop_ilb_ip}
        '''
        result = self._values.get("next_hop_ilb_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def next_hop_other_routes(self) -> typing.Optional[builtins.str]:
        '''Other routes that will be referenced to determine the next hop of the packet. Possible values: ["DEFAULT_ROUTING"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_policy_based_route#next_hop_other_routes NetworkConnectivityPolicyBasedRoute#next_hop_other_routes}
        '''
        result = self._values.get("next_hop_other_routes")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        '''The priority of this policy-based route.

        Priority is used to break ties in cases where there are more than one matching policy-based routes found. In cases where multiple policy-based routes are matched, the one with the lowest-numbered priority value wins. The default value is 1000. The priority value must be from 1 to 65535, inclusive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_policy_based_route#priority NetworkConnectivityPolicyBasedRoute#priority}
        '''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_policy_based_route#project NetworkConnectivityPolicyBasedRoute#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["NetworkConnectivityPolicyBasedRouteTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_policy_based_route#timeouts NetworkConnectivityPolicyBasedRoute#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["NetworkConnectivityPolicyBasedRouteTimeouts"], result)

    @builtins.property
    def virtual_machine(
        self,
    ) -> typing.Optional["NetworkConnectivityPolicyBasedRouteVirtualMachine"]:
        '''virtual_machine block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_policy_based_route#virtual_machine NetworkConnectivityPolicyBasedRoute#virtual_machine}
        '''
        result = self._values.get("virtual_machine")
        return typing.cast(typing.Optional["NetworkConnectivityPolicyBasedRouteVirtualMachine"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkConnectivityPolicyBasedRouteConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkConnectivityPolicyBasedRoute.NetworkConnectivityPolicyBasedRouteFilter",
    jsii_struct_bases=[],
    name_mapping={
        "protocol_version": "protocolVersion",
        "dest_range": "destRange",
        "ip_protocol": "ipProtocol",
        "src_range": "srcRange",
    },
)
class NetworkConnectivityPolicyBasedRouteFilter:
    def __init__(
        self,
        *,
        protocol_version: builtins.str,
        dest_range: typing.Optional[builtins.str] = None,
        ip_protocol: typing.Optional[builtins.str] = None,
        src_range: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param protocol_version: Internet protocol versions this policy-based route applies to. Possible values: ["IPV4", "IPV6"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_policy_based_route#protocol_version NetworkConnectivityPolicyBasedRoute#protocol_version}
        :param dest_range: The destination IP range of outgoing packets that this policy-based route applies to. Default is "0.0.0.0/0". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_policy_based_route#dest_range NetworkConnectivityPolicyBasedRoute#dest_range}
        :param ip_protocol: The IP protocol that this policy-based route applies to. Valid values are 'TCP', 'UDP', and 'ALL'. Default is 'ALL'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_policy_based_route#ip_protocol NetworkConnectivityPolicyBasedRoute#ip_protocol}
        :param src_range: The source IP range of outgoing packets that this policy-based route applies to. Default is "0.0.0.0/0". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_policy_based_route#src_range NetworkConnectivityPolicyBasedRoute#src_range}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7f3113e985a4de9c9da66c15ecc3f6f8d56f006bf77f97ed91e51ac30377eac)
            check_type(argname="argument protocol_version", value=protocol_version, expected_type=type_hints["protocol_version"])
            check_type(argname="argument dest_range", value=dest_range, expected_type=type_hints["dest_range"])
            check_type(argname="argument ip_protocol", value=ip_protocol, expected_type=type_hints["ip_protocol"])
            check_type(argname="argument src_range", value=src_range, expected_type=type_hints["src_range"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "protocol_version": protocol_version,
        }
        if dest_range is not None:
            self._values["dest_range"] = dest_range
        if ip_protocol is not None:
            self._values["ip_protocol"] = ip_protocol
        if src_range is not None:
            self._values["src_range"] = src_range

    @builtins.property
    def protocol_version(self) -> builtins.str:
        '''Internet protocol versions this policy-based route applies to. Possible values: ["IPV4", "IPV6"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_policy_based_route#protocol_version NetworkConnectivityPolicyBasedRoute#protocol_version}
        '''
        result = self._values.get("protocol_version")
        assert result is not None, "Required property 'protocol_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dest_range(self) -> typing.Optional[builtins.str]:
        '''The destination IP range of outgoing packets that this policy-based route applies to. Default is "0.0.0.0/0".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_policy_based_route#dest_range NetworkConnectivityPolicyBasedRoute#dest_range}
        '''
        result = self._values.get("dest_range")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_protocol(self) -> typing.Optional[builtins.str]:
        '''The IP protocol that this policy-based route applies to. Valid values are 'TCP', 'UDP', and 'ALL'. Default is 'ALL'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_policy_based_route#ip_protocol NetworkConnectivityPolicyBasedRoute#ip_protocol}
        '''
        result = self._values.get("ip_protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def src_range(self) -> typing.Optional[builtins.str]:
        '''The source IP range of outgoing packets that this policy-based route applies to. Default is "0.0.0.0/0".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_policy_based_route#src_range NetworkConnectivityPolicyBasedRoute#src_range}
        '''
        result = self._values.get("src_range")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkConnectivityPolicyBasedRouteFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkConnectivityPolicyBasedRouteFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkConnectivityPolicyBasedRoute.NetworkConnectivityPolicyBasedRouteFilterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0587634fda2e6aa067e9024c2469224e9d3aae4430a5886d3f7938b41e8f0382)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDestRange")
    def reset_dest_range(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestRange", []))

    @jsii.member(jsii_name="resetIpProtocol")
    def reset_ip_protocol(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpProtocol", []))

    @jsii.member(jsii_name="resetSrcRange")
    def reset_src_range(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSrcRange", []))

    @builtins.property
    @jsii.member(jsii_name="destRangeInput")
    def dest_range_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="ipProtocolInput")
    def ip_protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipProtocolInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolVersionInput")
    def protocol_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protocolVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="srcRangeInput")
    def src_range_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "srcRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="destRange")
    def dest_range(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destRange"))

    @dest_range.setter
    def dest_range(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7551588ab2c1788a7d8d51ddc0b05c59fcac8c3f01b74bef59d77a551f8e2af4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destRange", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipProtocol")
    def ip_protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipProtocol"))

    @ip_protocol.setter
    def ip_protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a99507d8dd04b8ee635743392dc7944ac2bc51665d8bc69805ab0f4cc208f417)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipProtocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocolVersion")
    def protocol_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocolVersion"))

    @protocol_version.setter
    def protocol_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__867bbba1082f2699d16622c53df3629ee032c99d73a931c5fcad4e6f9879d44f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocolVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="srcRange")
    def src_range(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "srcRange"))

    @src_range.setter
    def src_range(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__701634e327a8665ccef7075e714332214fc91ab2976a15d990a3488474b8cdec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "srcRange", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkConnectivityPolicyBasedRouteFilter]:
        return typing.cast(typing.Optional[NetworkConnectivityPolicyBasedRouteFilter], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkConnectivityPolicyBasedRouteFilter],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd56b8f88ef5afa3c925bd129ee4cb2d653c7beb5ba8d42c261d21b39e6c57ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkConnectivityPolicyBasedRoute.NetworkConnectivityPolicyBasedRouteInterconnectAttachment",
    jsii_struct_bases=[],
    name_mapping={"region": "region"},
)
class NetworkConnectivityPolicyBasedRouteInterconnectAttachment:
    def __init__(self, *, region: builtins.str) -> None:
        '''
        :param region: Cloud region to install this policy-based route on for Interconnect attachments. Use 'all' to install it on all Interconnect attachments. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_policy_based_route#region NetworkConnectivityPolicyBasedRoute#region}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4455b54ca0f7d7b2da79703ab3133824e684d3506e801bfad0d1cd2040b1854)
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "region": region,
        }

    @builtins.property
    def region(self) -> builtins.str:
        '''Cloud region to install this policy-based route on for Interconnect attachments.

        Use 'all' to install it on all Interconnect attachments.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_policy_based_route#region NetworkConnectivityPolicyBasedRoute#region}
        '''
        result = self._values.get("region")
        assert result is not None, "Required property 'region' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkConnectivityPolicyBasedRouteInterconnectAttachment(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkConnectivityPolicyBasedRouteInterconnectAttachmentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkConnectivityPolicyBasedRoute.NetworkConnectivityPolicyBasedRouteInterconnectAttachmentOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__95761cc2462b6b25f0023d45fa347a735fb350d14dcd7e8d7d23fd6f8d6016a1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f334f1b084b1a996de6bbfeb5e6948b9ba3a7112196703958d7a796450b71600)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkConnectivityPolicyBasedRouteInterconnectAttachment]:
        return typing.cast(typing.Optional[NetworkConnectivityPolicyBasedRouteInterconnectAttachment], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkConnectivityPolicyBasedRouteInterconnectAttachment],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57a606fa8f1177344ea0cb527bbb7a8dd20bc1ec7aef4f67e7a78b46cdf7be3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkConnectivityPolicyBasedRoute.NetworkConnectivityPolicyBasedRouteTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class NetworkConnectivityPolicyBasedRouteTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_policy_based_route#create NetworkConnectivityPolicyBasedRoute#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_policy_based_route#delete NetworkConnectivityPolicyBasedRoute#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_policy_based_route#update NetworkConnectivityPolicyBasedRoute#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27c4d5d398736ba10be54fa462700e1a7c3837a656e3232c405f360e0e28dab1)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_policy_based_route#create NetworkConnectivityPolicyBasedRoute#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_policy_based_route#delete NetworkConnectivityPolicyBasedRoute#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_policy_based_route#update NetworkConnectivityPolicyBasedRoute#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkConnectivityPolicyBasedRouteTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkConnectivityPolicyBasedRouteTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkConnectivityPolicyBasedRoute.NetworkConnectivityPolicyBasedRouteTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a9b46352c82c97c308717b1dc5775fd2d208428e21270948ae0238d06be0d4d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__240431ba950217b3e14c5531e27c682ed881f8eedc3d20fae96813d4a0911f97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f1c49ae424f59358612eba5d1be2a2e9f25565015508eee3d1c94863fd24093)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0295473ad38bdc93866c2ba3637a321fc56db3f6f74661db8f853e374463adf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkConnectivityPolicyBasedRouteTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkConnectivityPolicyBasedRouteTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkConnectivityPolicyBasedRouteTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9b89765468686fec152cf5ea3bda4bdf5f7e88a7f051c32e1385841034a3ecf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkConnectivityPolicyBasedRoute.NetworkConnectivityPolicyBasedRouteVirtualMachine",
    jsii_struct_bases=[],
    name_mapping={"tags": "tags"},
)
class NetworkConnectivityPolicyBasedRouteVirtualMachine:
    def __init__(self, *, tags: typing.Sequence[builtins.str]) -> None:
        '''
        :param tags: A list of VM instance tags that this policy-based route applies to. VM instances that have ANY of tags specified here will install this PBR. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_policy_based_route#tags NetworkConnectivityPolicyBasedRoute#tags}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__544878104bfe0b263de59f1d1bfead0fa56e04ed63a003c22d42681d70045243)
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "tags": tags,
        }

    @builtins.property
    def tags(self) -> typing.List[builtins.str]:
        '''A list of VM instance tags that this policy-based route applies to.

        VM instances that have ANY of tags specified here will install this PBR.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_policy_based_route#tags NetworkConnectivityPolicyBasedRoute#tags}
        '''
        result = self._values.get("tags")
        assert result is not None, "Required property 'tags' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkConnectivityPolicyBasedRouteVirtualMachine(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkConnectivityPolicyBasedRouteVirtualMachineOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkConnectivityPolicyBasedRoute.NetworkConnectivityPolicyBasedRouteVirtualMachineOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__46ef8df1c01bab60d78561dd78fadd5b0740c2789ee70ed40019451a7a9b0f58)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e559b77d3ca2179a4dbd8af2a3ccfd8ac04c5d9b1241b60a9f3b37384c2fe66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkConnectivityPolicyBasedRouteVirtualMachine]:
        return typing.cast(typing.Optional[NetworkConnectivityPolicyBasedRouteVirtualMachine], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkConnectivityPolicyBasedRouteVirtualMachine],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__caf1e35999ff80e8306653ddb2b0e32cc3c5a50665204b7a0dcea2253444d809)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkConnectivityPolicyBasedRoute.NetworkConnectivityPolicyBasedRouteWarnings",
    jsii_struct_bases=[],
    name_mapping={},
)
class NetworkConnectivityPolicyBasedRouteWarnings:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkConnectivityPolicyBasedRouteWarnings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkConnectivityPolicyBasedRouteWarningsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkConnectivityPolicyBasedRoute.NetworkConnectivityPolicyBasedRouteWarningsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c6f48e63d676ed3aa6c864284cb94fea58aeaa052c60f3375e8383d522fa1401)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NetworkConnectivityPolicyBasedRouteWarningsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9187629c3cfa6835e8498b6a46b973efcf7428a5279336daf5eff0d67716e450)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkConnectivityPolicyBasedRouteWarningsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0f476d037e329ff51b6393089bf9577475b31244a1c2e09c28a679c443f9aeb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6243ee69b5ec72f801ba7fddc4a738427bef728074c2201a2e3e0dae65b169d2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a58ab8b5da432ddeb03d89568035aaa34460a10289aafcca073dff4e1056d523)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class NetworkConnectivityPolicyBasedRouteWarningsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkConnectivityPolicyBasedRoute.NetworkConnectivityPolicyBasedRouteWarningsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b09b63f229a1a35ae5995b90d3dd9e5a3e7a483d8b3603d19552ad4a4e8b241d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="code")
    def code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "code"))

    @builtins.property
    @jsii.member(jsii_name="data")
    def data(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "data"))

    @builtins.property
    @jsii.member(jsii_name="warningMessage")
    def warning_message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "warningMessage"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkConnectivityPolicyBasedRouteWarnings]:
        return typing.cast(typing.Optional[NetworkConnectivityPolicyBasedRouteWarnings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkConnectivityPolicyBasedRouteWarnings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cdafa03bc0e547567d025cfe41d9628a9658b1470c8ef58cc1d7de32ee20164)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "NetworkConnectivityPolicyBasedRoute",
    "NetworkConnectivityPolicyBasedRouteConfig",
    "NetworkConnectivityPolicyBasedRouteFilter",
    "NetworkConnectivityPolicyBasedRouteFilterOutputReference",
    "NetworkConnectivityPolicyBasedRouteInterconnectAttachment",
    "NetworkConnectivityPolicyBasedRouteInterconnectAttachmentOutputReference",
    "NetworkConnectivityPolicyBasedRouteTimeouts",
    "NetworkConnectivityPolicyBasedRouteTimeoutsOutputReference",
    "NetworkConnectivityPolicyBasedRouteVirtualMachine",
    "NetworkConnectivityPolicyBasedRouteVirtualMachineOutputReference",
    "NetworkConnectivityPolicyBasedRouteWarnings",
    "NetworkConnectivityPolicyBasedRouteWarningsList",
    "NetworkConnectivityPolicyBasedRouteWarningsOutputReference",
]

publication.publish()

def _typecheckingstub__8b208f6b69aefa19871d69586ff5ada47d85b98e157591430c68fee885feb83b(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    filter: typing.Union[NetworkConnectivityPolicyBasedRouteFilter, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    network: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    interconnect_attachment: typing.Optional[typing.Union[NetworkConnectivityPolicyBasedRouteInterconnectAttachment, typing.Dict[builtins.str, typing.Any]]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    next_hop_ilb_ip: typing.Optional[builtins.str] = None,
    next_hop_other_routes: typing.Optional[builtins.str] = None,
    priority: typing.Optional[jsii.Number] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[NetworkConnectivityPolicyBasedRouteTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    virtual_machine: typing.Optional[typing.Union[NetworkConnectivityPolicyBasedRouteVirtualMachine, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__6b0a45995e900ca623bd73600be052dc59347803837ed4b545e5c85caa402e41(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e30aad89e69f2825664a23d5b0cbb31268e23a051f67de51cc6df7865076e3c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b331175473822a3d8ecdb561f79552a7c86b1a63a892a6d0efd3cc7688ecbce8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b17e4b6f4433d86408b981a59156b460354a1d72ea6de3110553afad8df531e7(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee822153149bf813d1e724a8cde7e7af2f317e8e4d160089133f8158924ad89e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__447a737d15edf18c640dc6491561597bd9b1bbf2632049465eab5a8f5bd521a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c2e53cfcb9d584f05b39d004d44ee5fa5b64463f918dcc6fc3c76fc41053539(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__362bb97bc203eb2000874e72cc5dc64825a8ec16cd0cb27b63f36991a718a552(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c29c3bcbb20aa13b14a2dd347878574d00e19ad54f8fc104e0bc62bafc86d48(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6db248f56ac3533ff4692b08b8d71cdeaff172bcb4eab553fc43b3eaf6a4cb34(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db634a31cf482c143b02fc3dd610cc2908af7232109b31e9aacd4f89efacf732(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    filter: typing.Union[NetworkConnectivityPolicyBasedRouteFilter, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    network: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    interconnect_attachment: typing.Optional[typing.Union[NetworkConnectivityPolicyBasedRouteInterconnectAttachment, typing.Dict[builtins.str, typing.Any]]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    next_hop_ilb_ip: typing.Optional[builtins.str] = None,
    next_hop_other_routes: typing.Optional[builtins.str] = None,
    priority: typing.Optional[jsii.Number] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[NetworkConnectivityPolicyBasedRouteTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    virtual_machine: typing.Optional[typing.Union[NetworkConnectivityPolicyBasedRouteVirtualMachine, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7f3113e985a4de9c9da66c15ecc3f6f8d56f006bf77f97ed91e51ac30377eac(
    *,
    protocol_version: builtins.str,
    dest_range: typing.Optional[builtins.str] = None,
    ip_protocol: typing.Optional[builtins.str] = None,
    src_range: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0587634fda2e6aa067e9024c2469224e9d3aae4430a5886d3f7938b41e8f0382(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7551588ab2c1788a7d8d51ddc0b05c59fcac8c3f01b74bef59d77a551f8e2af4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a99507d8dd04b8ee635743392dc7944ac2bc51665d8bc69805ab0f4cc208f417(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__867bbba1082f2699d16622c53df3629ee032c99d73a931c5fcad4e6f9879d44f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__701634e327a8665ccef7075e714332214fc91ab2976a15d990a3488474b8cdec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd56b8f88ef5afa3c925bd129ee4cb2d653c7beb5ba8d42c261d21b39e6c57ff(
    value: typing.Optional[NetworkConnectivityPolicyBasedRouteFilter],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4455b54ca0f7d7b2da79703ab3133824e684d3506e801bfad0d1cd2040b1854(
    *,
    region: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95761cc2462b6b25f0023d45fa347a735fb350d14dcd7e8d7d23fd6f8d6016a1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f334f1b084b1a996de6bbfeb5e6948b9ba3a7112196703958d7a796450b71600(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57a606fa8f1177344ea0cb527bbb7a8dd20bc1ec7aef4f67e7a78b46cdf7be3c(
    value: typing.Optional[NetworkConnectivityPolicyBasedRouteInterconnectAttachment],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27c4d5d398736ba10be54fa462700e1a7c3837a656e3232c405f360e0e28dab1(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a9b46352c82c97c308717b1dc5775fd2d208428e21270948ae0238d06be0d4d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__240431ba950217b3e14c5531e27c682ed881f8eedc3d20fae96813d4a0911f97(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f1c49ae424f59358612eba5d1be2a2e9f25565015508eee3d1c94863fd24093(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0295473ad38bdc93866c2ba3637a321fc56db3f6f74661db8f853e374463adf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9b89765468686fec152cf5ea3bda4bdf5f7e88a7f051c32e1385841034a3ecf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkConnectivityPolicyBasedRouteTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__544878104bfe0b263de59f1d1bfead0fa56e04ed63a003c22d42681d70045243(
    *,
    tags: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46ef8df1c01bab60d78561dd78fadd5b0740c2789ee70ed40019451a7a9b0f58(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e559b77d3ca2179a4dbd8af2a3ccfd8ac04c5d9b1241b60a9f3b37384c2fe66(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__caf1e35999ff80e8306653ddb2b0e32cc3c5a50665204b7a0dcea2253444d809(
    value: typing.Optional[NetworkConnectivityPolicyBasedRouteVirtualMachine],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6f48e63d676ed3aa6c864284cb94fea58aeaa052c60f3375e8383d522fa1401(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9187629c3cfa6835e8498b6a46b973efcf7428a5279336daf5eff0d67716e450(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0f476d037e329ff51b6393089bf9577475b31244a1c2e09c28a679c443f9aeb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6243ee69b5ec72f801ba7fddc4a738427bef728074c2201a2e3e0dae65b169d2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a58ab8b5da432ddeb03d89568035aaa34460a10289aafcca073dff4e1056d523(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b09b63f229a1a35ae5995b90d3dd9e5a3e7a483d8b3603d19552ad4a4e8b241d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cdafa03bc0e547567d025cfe41d9628a9658b1470c8ef58cc1d7de32ee20164(
    value: typing.Optional[NetworkConnectivityPolicyBasedRouteWarnings],
) -> None:
    """Type checking stubs"""
    pass
