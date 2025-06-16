r'''
# `google_network_connectivity_policy_based_route`

Refer to the Terraform Registry for docs: [`google_network_connectivity_policy_based_route`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_connectivity_policy_based_route).
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


class GoogleNetworkConnectivityPolicyBasedRoute(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkConnectivityPolicyBasedRoute.GoogleNetworkConnectivityPolicyBasedRoute",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_connectivity_policy_based_route google_network_connectivity_policy_based_route}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        filter: typing.Union["GoogleNetworkConnectivityPolicyBasedRouteFilter", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        network: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        interconnect_attachment: typing.Optional[typing.Union["GoogleNetworkConnectivityPolicyBasedRouteInterconnectAttachment", typing.Dict[builtins.str, typing.Any]]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        next_hop_ilb_ip: typing.Optional[builtins.str] = None,
        next_hop_other_routes: typing.Optional[builtins.str] = None,
        priority: typing.Optional[jsii.Number] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleNetworkConnectivityPolicyBasedRouteTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        virtual_machine: typing.Optional[typing.Union["GoogleNetworkConnectivityPolicyBasedRouteVirtualMachine", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_connectivity_policy_based_route google_network_connectivity_policy_based_route} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param filter: filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_connectivity_policy_based_route#filter GoogleNetworkConnectivityPolicyBasedRoute#filter}
        :param name: The name of the policy based route. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_connectivity_policy_based_route#name GoogleNetworkConnectivityPolicyBasedRoute#name}
        :param network: Fully-qualified URL of the network that this route applies to, for example: projects/my-project/global/networks/my-network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_connectivity_policy_based_route#network GoogleNetworkConnectivityPolicyBasedRoute#network}
        :param description: An optional description of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_connectivity_policy_based_route#description GoogleNetworkConnectivityPolicyBasedRoute#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_connectivity_policy_based_route#id GoogleNetworkConnectivityPolicyBasedRoute#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param interconnect_attachment: interconnect_attachment block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_connectivity_policy_based_route#interconnect_attachment GoogleNetworkConnectivityPolicyBasedRoute#interconnect_attachment}
        :param labels: User-defined labels. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_connectivity_policy_based_route#labels GoogleNetworkConnectivityPolicyBasedRoute#labels}
        :param next_hop_ilb_ip: The IP address of a global-access-enabled L4 ILB that is the next hop for matching packets. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_connectivity_policy_based_route#next_hop_ilb_ip GoogleNetworkConnectivityPolicyBasedRoute#next_hop_ilb_ip}
        :param next_hop_other_routes: Other routes that will be referenced to determine the next hop of the packet. Possible values: ["DEFAULT_ROUTING"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_connectivity_policy_based_route#next_hop_other_routes GoogleNetworkConnectivityPolicyBasedRoute#next_hop_other_routes}
        :param priority: The priority of this policy-based route. Priority is used to break ties in cases where there are more than one matching policy-based routes found. In cases where multiple policy-based routes are matched, the one with the lowest-numbered priority value wins. The default value is 1000. The priority value must be from 1 to 65535, inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_connectivity_policy_based_route#priority GoogleNetworkConnectivityPolicyBasedRoute#priority}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_connectivity_policy_based_route#project GoogleNetworkConnectivityPolicyBasedRoute#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_connectivity_policy_based_route#timeouts GoogleNetworkConnectivityPolicyBasedRoute#timeouts}
        :param virtual_machine: virtual_machine block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_connectivity_policy_based_route#virtual_machine GoogleNetworkConnectivityPolicyBasedRoute#virtual_machine}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33cf0104908f6e9d0f266a61589e452f35c9762fe5764f48d9130d10d1070074)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleNetworkConnectivityPolicyBasedRouteConfig(
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
        '''Generates CDKTF code for importing a GoogleNetworkConnectivityPolicyBasedRoute resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleNetworkConnectivityPolicyBasedRoute to import.
        :param import_from_id: The id of the existing GoogleNetworkConnectivityPolicyBasedRoute that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_connectivity_policy_based_route#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleNetworkConnectivityPolicyBasedRoute to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c3ee8e116746fee046d9a04bbb63647d1beb3a415258294ec7826474fd272bd)
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
        :param protocol_version: Internet protocol versions this policy-based route applies to. Possible values: ["IPV4", "IPV6"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_connectivity_policy_based_route#protocol_version GoogleNetworkConnectivityPolicyBasedRoute#protocol_version}
        :param dest_range: The destination IP range of outgoing packets that this policy-based route applies to. Default is "0.0.0.0/0". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_connectivity_policy_based_route#dest_range GoogleNetworkConnectivityPolicyBasedRoute#dest_range}
        :param ip_protocol: The IP protocol that this policy-based route applies to. Valid values are 'TCP', 'UDP', and 'ALL'. Default is 'ALL'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_connectivity_policy_based_route#ip_protocol GoogleNetworkConnectivityPolicyBasedRoute#ip_protocol}
        :param src_range: The source IP range of outgoing packets that this policy-based route applies to. Default is "0.0.0.0/0". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_connectivity_policy_based_route#src_range GoogleNetworkConnectivityPolicyBasedRoute#src_range}
        '''
        value = GoogleNetworkConnectivityPolicyBasedRouteFilter(
            protocol_version=protocol_version,
            dest_range=dest_range,
            ip_protocol=ip_protocol,
            src_range=src_range,
        )

        return typing.cast(None, jsii.invoke(self, "putFilter", [value]))

    @jsii.member(jsii_name="putInterconnectAttachment")
    def put_interconnect_attachment(self, *, region: builtins.str) -> None:
        '''
        :param region: Cloud region to install this policy-based route on for Interconnect attachments. Use 'all' to install it on all Interconnect attachments. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_connectivity_policy_based_route#region GoogleNetworkConnectivityPolicyBasedRoute#region}
        '''
        value = GoogleNetworkConnectivityPolicyBasedRouteInterconnectAttachment(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_connectivity_policy_based_route#create GoogleNetworkConnectivityPolicyBasedRoute#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_connectivity_policy_based_route#delete GoogleNetworkConnectivityPolicyBasedRoute#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_connectivity_policy_based_route#update GoogleNetworkConnectivityPolicyBasedRoute#update}.
        '''
        value = GoogleNetworkConnectivityPolicyBasedRouteTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putVirtualMachine")
    def put_virtual_machine(self, *, tags: typing.Sequence[builtins.str]) -> None:
        '''
        :param tags: A list of VM instance tags that this policy-based route applies to. VM instances that have ANY of tags specified here will install this PBR. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_connectivity_policy_based_route#tags GoogleNetworkConnectivityPolicyBasedRoute#tags}
        '''
        value = GoogleNetworkConnectivityPolicyBasedRouteVirtualMachine(tags=tags)

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
    def filter(
        self,
    ) -> "GoogleNetworkConnectivityPolicyBasedRouteFilterOutputReference":
        return typing.cast("GoogleNetworkConnectivityPolicyBasedRouteFilterOutputReference", jsii.get(self, "filter"))

    @builtins.property
    @jsii.member(jsii_name="interconnectAttachment")
    def interconnect_attachment(
        self,
    ) -> "GoogleNetworkConnectivityPolicyBasedRouteInterconnectAttachmentOutputReference":
        return typing.cast("GoogleNetworkConnectivityPolicyBasedRouteInterconnectAttachmentOutputReference", jsii.get(self, "interconnectAttachment"))

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
    def timeouts(
        self,
    ) -> "GoogleNetworkConnectivityPolicyBasedRouteTimeoutsOutputReference":
        return typing.cast("GoogleNetworkConnectivityPolicyBasedRouteTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="virtualMachine")
    def virtual_machine(
        self,
    ) -> "GoogleNetworkConnectivityPolicyBasedRouteVirtualMachineOutputReference":
        return typing.cast("GoogleNetworkConnectivityPolicyBasedRouteVirtualMachineOutputReference", jsii.get(self, "virtualMachine"))

    @builtins.property
    @jsii.member(jsii_name="warnings")
    def warnings(self) -> "GoogleNetworkConnectivityPolicyBasedRouteWarningsList":
        return typing.cast("GoogleNetworkConnectivityPolicyBasedRouteWarningsList", jsii.get(self, "warnings"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="filterInput")
    def filter_input(
        self,
    ) -> typing.Optional["GoogleNetworkConnectivityPolicyBasedRouteFilter"]:
        return typing.cast(typing.Optional["GoogleNetworkConnectivityPolicyBasedRouteFilter"], jsii.get(self, "filterInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="interconnectAttachmentInput")
    def interconnect_attachment_input(
        self,
    ) -> typing.Optional["GoogleNetworkConnectivityPolicyBasedRouteInterconnectAttachment"]:
        return typing.cast(typing.Optional["GoogleNetworkConnectivityPolicyBasedRouteInterconnectAttachment"], jsii.get(self, "interconnectAttachmentInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleNetworkConnectivityPolicyBasedRouteTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleNetworkConnectivityPolicyBasedRouteTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualMachineInput")
    def virtual_machine_input(
        self,
    ) -> typing.Optional["GoogleNetworkConnectivityPolicyBasedRouteVirtualMachine"]:
        return typing.cast(typing.Optional["GoogleNetworkConnectivityPolicyBasedRouteVirtualMachine"], jsii.get(self, "virtualMachineInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbeccc649bd6ae59a7970407d1917e768199a2ff111a059c2be34324cadf9e61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec40f5cef4bbdf62dc8ec752595e030784a1ad5c2d6232867afe4634093a43d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dfd831855cb5fb1ef466b2542ae93efe69f1b18b360c64f254704b3a6f2b799)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e5a1a5e561ecc16088cd5619abad42f7b2482a473fba3b60dd199667da49313)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0c15d67bb84797e874ed88ff6d39f980c03ca4d3c3c38c0e39fd683bbdafee0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nextHopIlbIp")
    def next_hop_ilb_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nextHopIlbIp"))

    @next_hop_ilb_ip.setter
    def next_hop_ilb_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6787940ef0cbdba9d80b35257cb1b0f65981e21b5851675d55962462ef363033)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nextHopIlbIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nextHopOtherRoutes")
    def next_hop_other_routes(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nextHopOtherRoutes"))

    @next_hop_other_routes.setter
    def next_hop_other_routes(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84285c3455856886f4cc5c85cd8481061e9ab1ae7cc6fe9bb82f46b5d97c9281)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nextHopOtherRoutes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__972d5f862bf65500a5ba9e4b529f9fe86a851ee37d50317162f365c1c46654cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76a80f8014527b6b70a1db74ce353a8f384cfacc76c87225e283f7426216bd23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkConnectivityPolicyBasedRoute.GoogleNetworkConnectivityPolicyBasedRouteConfig",
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
class GoogleNetworkConnectivityPolicyBasedRouteConfig(
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
        filter: typing.Union["GoogleNetworkConnectivityPolicyBasedRouteFilter", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        network: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        interconnect_attachment: typing.Optional[typing.Union["GoogleNetworkConnectivityPolicyBasedRouteInterconnectAttachment", typing.Dict[builtins.str, typing.Any]]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        next_hop_ilb_ip: typing.Optional[builtins.str] = None,
        next_hop_other_routes: typing.Optional[builtins.str] = None,
        priority: typing.Optional[jsii.Number] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleNetworkConnectivityPolicyBasedRouteTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        virtual_machine: typing.Optional[typing.Union["GoogleNetworkConnectivityPolicyBasedRouteVirtualMachine", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param filter: filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_connectivity_policy_based_route#filter GoogleNetworkConnectivityPolicyBasedRoute#filter}
        :param name: The name of the policy based route. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_connectivity_policy_based_route#name GoogleNetworkConnectivityPolicyBasedRoute#name}
        :param network: Fully-qualified URL of the network that this route applies to, for example: projects/my-project/global/networks/my-network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_connectivity_policy_based_route#network GoogleNetworkConnectivityPolicyBasedRoute#network}
        :param description: An optional description of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_connectivity_policy_based_route#description GoogleNetworkConnectivityPolicyBasedRoute#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_connectivity_policy_based_route#id GoogleNetworkConnectivityPolicyBasedRoute#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param interconnect_attachment: interconnect_attachment block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_connectivity_policy_based_route#interconnect_attachment GoogleNetworkConnectivityPolicyBasedRoute#interconnect_attachment}
        :param labels: User-defined labels. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_connectivity_policy_based_route#labels GoogleNetworkConnectivityPolicyBasedRoute#labels}
        :param next_hop_ilb_ip: The IP address of a global-access-enabled L4 ILB that is the next hop for matching packets. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_connectivity_policy_based_route#next_hop_ilb_ip GoogleNetworkConnectivityPolicyBasedRoute#next_hop_ilb_ip}
        :param next_hop_other_routes: Other routes that will be referenced to determine the next hop of the packet. Possible values: ["DEFAULT_ROUTING"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_connectivity_policy_based_route#next_hop_other_routes GoogleNetworkConnectivityPolicyBasedRoute#next_hop_other_routes}
        :param priority: The priority of this policy-based route. Priority is used to break ties in cases where there are more than one matching policy-based routes found. In cases where multiple policy-based routes are matched, the one with the lowest-numbered priority value wins. The default value is 1000. The priority value must be from 1 to 65535, inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_connectivity_policy_based_route#priority GoogleNetworkConnectivityPolicyBasedRoute#priority}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_connectivity_policy_based_route#project GoogleNetworkConnectivityPolicyBasedRoute#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_connectivity_policy_based_route#timeouts GoogleNetworkConnectivityPolicyBasedRoute#timeouts}
        :param virtual_machine: virtual_machine block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_connectivity_policy_based_route#virtual_machine GoogleNetworkConnectivityPolicyBasedRoute#virtual_machine}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(filter, dict):
            filter = GoogleNetworkConnectivityPolicyBasedRouteFilter(**filter)
        if isinstance(interconnect_attachment, dict):
            interconnect_attachment = GoogleNetworkConnectivityPolicyBasedRouteInterconnectAttachment(**interconnect_attachment)
        if isinstance(timeouts, dict):
            timeouts = GoogleNetworkConnectivityPolicyBasedRouteTimeouts(**timeouts)
        if isinstance(virtual_machine, dict):
            virtual_machine = GoogleNetworkConnectivityPolicyBasedRouteVirtualMachine(**virtual_machine)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a6aba40a2779459c11444a7771dd5be47e2ed78a332a71ee1bd32a0cde38e0c)
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
    def filter(self) -> "GoogleNetworkConnectivityPolicyBasedRouteFilter":
        '''filter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_connectivity_policy_based_route#filter GoogleNetworkConnectivityPolicyBasedRoute#filter}
        '''
        result = self._values.get("filter")
        assert result is not None, "Required property 'filter' is missing"
        return typing.cast("GoogleNetworkConnectivityPolicyBasedRouteFilter", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the policy based route.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_connectivity_policy_based_route#name GoogleNetworkConnectivityPolicyBasedRoute#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def network(self) -> builtins.str:
        '''Fully-qualified URL of the network that this route applies to, for example: projects/my-project/global/networks/my-network.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_connectivity_policy_based_route#network GoogleNetworkConnectivityPolicyBasedRoute#network}
        '''
        result = self._values.get("network")
        assert result is not None, "Required property 'network' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_connectivity_policy_based_route#description GoogleNetworkConnectivityPolicyBasedRoute#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_connectivity_policy_based_route#id GoogleNetworkConnectivityPolicyBasedRoute#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def interconnect_attachment(
        self,
    ) -> typing.Optional["GoogleNetworkConnectivityPolicyBasedRouteInterconnectAttachment"]:
        '''interconnect_attachment block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_connectivity_policy_based_route#interconnect_attachment GoogleNetworkConnectivityPolicyBasedRoute#interconnect_attachment}
        '''
        result = self._values.get("interconnect_attachment")
        return typing.cast(typing.Optional["GoogleNetworkConnectivityPolicyBasedRouteInterconnectAttachment"], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''User-defined labels.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_connectivity_policy_based_route#labels GoogleNetworkConnectivityPolicyBasedRoute#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def next_hop_ilb_ip(self) -> typing.Optional[builtins.str]:
        '''The IP address of a global-access-enabled L4 ILB that is the next hop for matching packets.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_connectivity_policy_based_route#next_hop_ilb_ip GoogleNetworkConnectivityPolicyBasedRoute#next_hop_ilb_ip}
        '''
        result = self._values.get("next_hop_ilb_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def next_hop_other_routes(self) -> typing.Optional[builtins.str]:
        '''Other routes that will be referenced to determine the next hop of the packet. Possible values: ["DEFAULT_ROUTING"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_connectivity_policy_based_route#next_hop_other_routes GoogleNetworkConnectivityPolicyBasedRoute#next_hop_other_routes}
        '''
        result = self._values.get("next_hop_other_routes")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        '''The priority of this policy-based route.

        Priority is used to break ties in cases where there are more than one matching policy-based routes found. In cases where multiple policy-based routes are matched, the one with the lowest-numbered priority value wins. The default value is 1000. The priority value must be from 1 to 65535, inclusive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_connectivity_policy_based_route#priority GoogleNetworkConnectivityPolicyBasedRoute#priority}
        '''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_connectivity_policy_based_route#project GoogleNetworkConnectivityPolicyBasedRoute#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["GoogleNetworkConnectivityPolicyBasedRouteTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_connectivity_policy_based_route#timeouts GoogleNetworkConnectivityPolicyBasedRoute#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleNetworkConnectivityPolicyBasedRouteTimeouts"], result)

    @builtins.property
    def virtual_machine(
        self,
    ) -> typing.Optional["GoogleNetworkConnectivityPolicyBasedRouteVirtualMachine"]:
        '''virtual_machine block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_connectivity_policy_based_route#virtual_machine GoogleNetworkConnectivityPolicyBasedRoute#virtual_machine}
        '''
        result = self._values.get("virtual_machine")
        return typing.cast(typing.Optional["GoogleNetworkConnectivityPolicyBasedRouteVirtualMachine"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkConnectivityPolicyBasedRouteConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkConnectivityPolicyBasedRoute.GoogleNetworkConnectivityPolicyBasedRouteFilter",
    jsii_struct_bases=[],
    name_mapping={
        "protocol_version": "protocolVersion",
        "dest_range": "destRange",
        "ip_protocol": "ipProtocol",
        "src_range": "srcRange",
    },
)
class GoogleNetworkConnectivityPolicyBasedRouteFilter:
    def __init__(
        self,
        *,
        protocol_version: builtins.str,
        dest_range: typing.Optional[builtins.str] = None,
        ip_protocol: typing.Optional[builtins.str] = None,
        src_range: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param protocol_version: Internet protocol versions this policy-based route applies to. Possible values: ["IPV4", "IPV6"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_connectivity_policy_based_route#protocol_version GoogleNetworkConnectivityPolicyBasedRoute#protocol_version}
        :param dest_range: The destination IP range of outgoing packets that this policy-based route applies to. Default is "0.0.0.0/0". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_connectivity_policy_based_route#dest_range GoogleNetworkConnectivityPolicyBasedRoute#dest_range}
        :param ip_protocol: The IP protocol that this policy-based route applies to. Valid values are 'TCP', 'UDP', and 'ALL'. Default is 'ALL'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_connectivity_policy_based_route#ip_protocol GoogleNetworkConnectivityPolicyBasedRoute#ip_protocol}
        :param src_range: The source IP range of outgoing packets that this policy-based route applies to. Default is "0.0.0.0/0". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_connectivity_policy_based_route#src_range GoogleNetworkConnectivityPolicyBasedRoute#src_range}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2308e4b8e65de1ac51fc1d00ca4acafc423f221b3d721b47f335ec91733c71e5)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_connectivity_policy_based_route#protocol_version GoogleNetworkConnectivityPolicyBasedRoute#protocol_version}
        '''
        result = self._values.get("protocol_version")
        assert result is not None, "Required property 'protocol_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dest_range(self) -> typing.Optional[builtins.str]:
        '''The destination IP range of outgoing packets that this policy-based route applies to. Default is "0.0.0.0/0".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_connectivity_policy_based_route#dest_range GoogleNetworkConnectivityPolicyBasedRoute#dest_range}
        '''
        result = self._values.get("dest_range")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_protocol(self) -> typing.Optional[builtins.str]:
        '''The IP protocol that this policy-based route applies to. Valid values are 'TCP', 'UDP', and 'ALL'. Default is 'ALL'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_connectivity_policy_based_route#ip_protocol GoogleNetworkConnectivityPolicyBasedRoute#ip_protocol}
        '''
        result = self._values.get("ip_protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def src_range(self) -> typing.Optional[builtins.str]:
        '''The source IP range of outgoing packets that this policy-based route applies to. Default is "0.0.0.0/0".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_connectivity_policy_based_route#src_range GoogleNetworkConnectivityPolicyBasedRoute#src_range}
        '''
        result = self._values.get("src_range")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkConnectivityPolicyBasedRouteFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkConnectivityPolicyBasedRouteFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkConnectivityPolicyBasedRoute.GoogleNetworkConnectivityPolicyBasedRouteFilterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__124546a94df3574bafc8ec5de2eb9d0abb6f1268fbd69b39a8cf56092bcfcd0b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f09a6608b9164fcc6a9bc9c16ce5e613309fcb8d0e70aefe6de6f2ed37a0ca1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destRange", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipProtocol")
    def ip_protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipProtocol"))

    @ip_protocol.setter
    def ip_protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e79535aee1823b28a44b2bf78133c9606cfc28de648d866d352a416c5321b2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipProtocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocolVersion")
    def protocol_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocolVersion"))

    @protocol_version.setter
    def protocol_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__155df5399b807fd6e5ab6b9ff1e2b62e93798fecda19d96768c6f62d2089ccd6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocolVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="srcRange")
    def src_range(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "srcRange"))

    @src_range.setter
    def src_range(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3ab2841b312cf7e00b6e6ef12797be706827332e0a7e31f5c3af94e2bb62948)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "srcRange", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetworkConnectivityPolicyBasedRouteFilter]:
        return typing.cast(typing.Optional[GoogleNetworkConnectivityPolicyBasedRouteFilter], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetworkConnectivityPolicyBasedRouteFilter],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__060d0bdea78e99e12a7cb7607fffd0226feb880ea0774b29ba24c3e7242c325e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkConnectivityPolicyBasedRoute.GoogleNetworkConnectivityPolicyBasedRouteInterconnectAttachment",
    jsii_struct_bases=[],
    name_mapping={"region": "region"},
)
class GoogleNetworkConnectivityPolicyBasedRouteInterconnectAttachment:
    def __init__(self, *, region: builtins.str) -> None:
        '''
        :param region: Cloud region to install this policy-based route on for Interconnect attachments. Use 'all' to install it on all Interconnect attachments. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_connectivity_policy_based_route#region GoogleNetworkConnectivityPolicyBasedRoute#region}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3114f82a7f45ec4b7fb8718ddedbc95f94623b265c389eb69036c7148a5fd4ed)
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "region": region,
        }

    @builtins.property
    def region(self) -> builtins.str:
        '''Cloud region to install this policy-based route on for Interconnect attachments.

        Use 'all' to install it on all Interconnect attachments.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_connectivity_policy_based_route#region GoogleNetworkConnectivityPolicyBasedRoute#region}
        '''
        result = self._values.get("region")
        assert result is not None, "Required property 'region' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkConnectivityPolicyBasedRouteInterconnectAttachment(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkConnectivityPolicyBasedRouteInterconnectAttachmentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkConnectivityPolicyBasedRoute.GoogleNetworkConnectivityPolicyBasedRouteInterconnectAttachmentOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d0381ea57a2be31c1d3398976bf1fcb29df6563dc47d9b82da864c8ed8824763)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a559cd787360eda55d5073961193722e8b2cbbc116ed068981d39d087cb04431)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetworkConnectivityPolicyBasedRouteInterconnectAttachment]:
        return typing.cast(typing.Optional[GoogleNetworkConnectivityPolicyBasedRouteInterconnectAttachment], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetworkConnectivityPolicyBasedRouteInterconnectAttachment],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__503c5af32cd52a918464f84ba65e53881e40dd794938c7c472450767e28b713d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkConnectivityPolicyBasedRoute.GoogleNetworkConnectivityPolicyBasedRouteTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleNetworkConnectivityPolicyBasedRouteTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_connectivity_policy_based_route#create GoogleNetworkConnectivityPolicyBasedRoute#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_connectivity_policy_based_route#delete GoogleNetworkConnectivityPolicyBasedRoute#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_connectivity_policy_based_route#update GoogleNetworkConnectivityPolicyBasedRoute#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b00d3d5eefc16e10a18617eb615e11cfe7bd1a294bcfc4e1c5880e1b2816040)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_connectivity_policy_based_route#create GoogleNetworkConnectivityPolicyBasedRoute#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_connectivity_policy_based_route#delete GoogleNetworkConnectivityPolicyBasedRoute#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_connectivity_policy_based_route#update GoogleNetworkConnectivityPolicyBasedRoute#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkConnectivityPolicyBasedRouteTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkConnectivityPolicyBasedRouteTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkConnectivityPolicyBasedRoute.GoogleNetworkConnectivityPolicyBasedRouteTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__51e2259eb734f3ae5974f18bf4014a160aa13bacc0f5798e421e179d9fad38b4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2905ae276111fbfd23b5701ea1eebb48574b324e9f1beaa064a098f293255a84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b277c6dc47442db48dcb26d8c2f2df538d149f21b8109c6132e82c8353abafda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f0eb7980afbed6171c3d1a7688743a3ccfd686f6f9e8eb3ede819683095263c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkConnectivityPolicyBasedRouteTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkConnectivityPolicyBasedRouteTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkConnectivityPolicyBasedRouteTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__702f7619ff26ebd270ceaced94400300e814901a6f6cce2623bd4eb22a3b3eca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkConnectivityPolicyBasedRoute.GoogleNetworkConnectivityPolicyBasedRouteVirtualMachine",
    jsii_struct_bases=[],
    name_mapping={"tags": "tags"},
)
class GoogleNetworkConnectivityPolicyBasedRouteVirtualMachine:
    def __init__(self, *, tags: typing.Sequence[builtins.str]) -> None:
        '''
        :param tags: A list of VM instance tags that this policy-based route applies to. VM instances that have ANY of tags specified here will install this PBR. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_connectivity_policy_based_route#tags GoogleNetworkConnectivityPolicyBasedRoute#tags}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed7ea882a84ffa18cc6d3c95e31bdcbaa028795b2ce095cd39ffe526ffd53964)
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "tags": tags,
        }

    @builtins.property
    def tags(self) -> typing.List[builtins.str]:
        '''A list of VM instance tags that this policy-based route applies to.

        VM instances that have ANY of tags specified here will install this PBR.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_connectivity_policy_based_route#tags GoogleNetworkConnectivityPolicyBasedRoute#tags}
        '''
        result = self._values.get("tags")
        assert result is not None, "Required property 'tags' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkConnectivityPolicyBasedRouteVirtualMachine(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkConnectivityPolicyBasedRouteVirtualMachineOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkConnectivityPolicyBasedRoute.GoogleNetworkConnectivityPolicyBasedRouteVirtualMachineOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ddce80a1f1d118b51e7f67b843b77dc0b701d15707341a5f29eb1528e50b5ea4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ea191c007a1130eb79b8c57ab431046bf9c4ece99a9670aa73e91d11ff4daff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetworkConnectivityPolicyBasedRouteVirtualMachine]:
        return typing.cast(typing.Optional[GoogleNetworkConnectivityPolicyBasedRouteVirtualMachine], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetworkConnectivityPolicyBasedRouteVirtualMachine],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eff47ffb81ab0f503a5731ece6af5702bbd3c93385df8d1b18cc80493452b507)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkConnectivityPolicyBasedRoute.GoogleNetworkConnectivityPolicyBasedRouteWarnings",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleNetworkConnectivityPolicyBasedRouteWarnings:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkConnectivityPolicyBasedRouteWarnings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkConnectivityPolicyBasedRouteWarningsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkConnectivityPolicyBasedRoute.GoogleNetworkConnectivityPolicyBasedRouteWarningsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c0c8308a8c0ea1d926ea56bda60112cb6c216e51a6150cc94757aa52f3e3041e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleNetworkConnectivityPolicyBasedRouteWarningsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8d423f1dd2e5322729bcd71303128158be95eb8e7b3c0007bba144123dea154)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleNetworkConnectivityPolicyBasedRouteWarningsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4531b1b151891456e5f1cf54ef24f78ee68676fcbf4aa2168dc89ba59242623e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c3ae7574b3bd5ba0b20ef3473e978a59e03d1945186e10e9e87e239900f8809b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__34164592745487dbb365adf6e9d13f2f0b81e1a3eea3366170045c51fbf2664d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleNetworkConnectivityPolicyBasedRouteWarningsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkConnectivityPolicyBasedRoute.GoogleNetworkConnectivityPolicyBasedRouteWarningsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f63729dbc65f33e83019a3ac8a8c58eeec8601aa6a2df47223a4e22cc7035245)
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
    ) -> typing.Optional[GoogleNetworkConnectivityPolicyBasedRouteWarnings]:
        return typing.cast(typing.Optional[GoogleNetworkConnectivityPolicyBasedRouteWarnings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetworkConnectivityPolicyBasedRouteWarnings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cd757c88ee6d3a48bfe5dd66bf62d2b64866fc91cd29de59b947ff4f9d8eb08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleNetworkConnectivityPolicyBasedRoute",
    "GoogleNetworkConnectivityPolicyBasedRouteConfig",
    "GoogleNetworkConnectivityPolicyBasedRouteFilter",
    "GoogleNetworkConnectivityPolicyBasedRouteFilterOutputReference",
    "GoogleNetworkConnectivityPolicyBasedRouteInterconnectAttachment",
    "GoogleNetworkConnectivityPolicyBasedRouteInterconnectAttachmentOutputReference",
    "GoogleNetworkConnectivityPolicyBasedRouteTimeouts",
    "GoogleNetworkConnectivityPolicyBasedRouteTimeoutsOutputReference",
    "GoogleNetworkConnectivityPolicyBasedRouteVirtualMachine",
    "GoogleNetworkConnectivityPolicyBasedRouteVirtualMachineOutputReference",
    "GoogleNetworkConnectivityPolicyBasedRouteWarnings",
    "GoogleNetworkConnectivityPolicyBasedRouteWarningsList",
    "GoogleNetworkConnectivityPolicyBasedRouteWarningsOutputReference",
]

publication.publish()

def _typecheckingstub__33cf0104908f6e9d0f266a61589e452f35c9762fe5764f48d9130d10d1070074(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    filter: typing.Union[GoogleNetworkConnectivityPolicyBasedRouteFilter, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    network: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    interconnect_attachment: typing.Optional[typing.Union[GoogleNetworkConnectivityPolicyBasedRouteInterconnectAttachment, typing.Dict[builtins.str, typing.Any]]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    next_hop_ilb_ip: typing.Optional[builtins.str] = None,
    next_hop_other_routes: typing.Optional[builtins.str] = None,
    priority: typing.Optional[jsii.Number] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleNetworkConnectivityPolicyBasedRouteTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    virtual_machine: typing.Optional[typing.Union[GoogleNetworkConnectivityPolicyBasedRouteVirtualMachine, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__5c3ee8e116746fee046d9a04bbb63647d1beb3a415258294ec7826474fd272bd(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbeccc649bd6ae59a7970407d1917e768199a2ff111a059c2be34324cadf9e61(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec40f5cef4bbdf62dc8ec752595e030784a1ad5c2d6232867afe4634093a43d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dfd831855cb5fb1ef466b2542ae93efe69f1b18b360c64f254704b3a6f2b799(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e5a1a5e561ecc16088cd5619abad42f7b2482a473fba3b60dd199667da49313(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0c15d67bb84797e874ed88ff6d39f980c03ca4d3c3c38c0e39fd683bbdafee0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6787940ef0cbdba9d80b35257cb1b0f65981e21b5851675d55962462ef363033(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84285c3455856886f4cc5c85cd8481061e9ab1ae7cc6fe9bb82f46b5d97c9281(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__972d5f862bf65500a5ba9e4b529f9fe86a851ee37d50317162f365c1c46654cc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76a80f8014527b6b70a1db74ce353a8f384cfacc76c87225e283f7426216bd23(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a6aba40a2779459c11444a7771dd5be47e2ed78a332a71ee1bd32a0cde38e0c(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    filter: typing.Union[GoogleNetworkConnectivityPolicyBasedRouteFilter, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    network: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    interconnect_attachment: typing.Optional[typing.Union[GoogleNetworkConnectivityPolicyBasedRouteInterconnectAttachment, typing.Dict[builtins.str, typing.Any]]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    next_hop_ilb_ip: typing.Optional[builtins.str] = None,
    next_hop_other_routes: typing.Optional[builtins.str] = None,
    priority: typing.Optional[jsii.Number] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleNetworkConnectivityPolicyBasedRouteTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    virtual_machine: typing.Optional[typing.Union[GoogleNetworkConnectivityPolicyBasedRouteVirtualMachine, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2308e4b8e65de1ac51fc1d00ca4acafc423f221b3d721b47f335ec91733c71e5(
    *,
    protocol_version: builtins.str,
    dest_range: typing.Optional[builtins.str] = None,
    ip_protocol: typing.Optional[builtins.str] = None,
    src_range: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__124546a94df3574bafc8ec5de2eb9d0abb6f1268fbd69b39a8cf56092bcfcd0b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f09a6608b9164fcc6a9bc9c16ce5e613309fcb8d0e70aefe6de6f2ed37a0ca1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e79535aee1823b28a44b2bf78133c9606cfc28de648d866d352a416c5321b2a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__155df5399b807fd6e5ab6b9ff1e2b62e93798fecda19d96768c6f62d2089ccd6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3ab2841b312cf7e00b6e6ef12797be706827332e0a7e31f5c3af94e2bb62948(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__060d0bdea78e99e12a7cb7607fffd0226feb880ea0774b29ba24c3e7242c325e(
    value: typing.Optional[GoogleNetworkConnectivityPolicyBasedRouteFilter],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3114f82a7f45ec4b7fb8718ddedbc95f94623b265c389eb69036c7148a5fd4ed(
    *,
    region: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0381ea57a2be31c1d3398976bf1fcb29df6563dc47d9b82da864c8ed8824763(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a559cd787360eda55d5073961193722e8b2cbbc116ed068981d39d087cb04431(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__503c5af32cd52a918464f84ba65e53881e40dd794938c7c472450767e28b713d(
    value: typing.Optional[GoogleNetworkConnectivityPolicyBasedRouteInterconnectAttachment],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b00d3d5eefc16e10a18617eb615e11cfe7bd1a294bcfc4e1c5880e1b2816040(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51e2259eb734f3ae5974f18bf4014a160aa13bacc0f5798e421e179d9fad38b4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2905ae276111fbfd23b5701ea1eebb48574b324e9f1beaa064a098f293255a84(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b277c6dc47442db48dcb26d8c2f2df538d149f21b8109c6132e82c8353abafda(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f0eb7980afbed6171c3d1a7688743a3ccfd686f6f9e8eb3ede819683095263c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__702f7619ff26ebd270ceaced94400300e814901a6f6cce2623bd4eb22a3b3eca(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkConnectivityPolicyBasedRouteTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed7ea882a84ffa18cc6d3c95e31bdcbaa028795b2ce095cd39ffe526ffd53964(
    *,
    tags: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddce80a1f1d118b51e7f67b843b77dc0b701d15707341a5f29eb1528e50b5ea4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ea191c007a1130eb79b8c57ab431046bf9c4ece99a9670aa73e91d11ff4daff(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eff47ffb81ab0f503a5731ece6af5702bbd3c93385df8d1b18cc80493452b507(
    value: typing.Optional[GoogleNetworkConnectivityPolicyBasedRouteVirtualMachine],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0c8308a8c0ea1d926ea56bda60112cb6c216e51a6150cc94757aa52f3e3041e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8d423f1dd2e5322729bcd71303128158be95eb8e7b3c0007bba144123dea154(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4531b1b151891456e5f1cf54ef24f78ee68676fcbf4aa2168dc89ba59242623e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3ae7574b3bd5ba0b20ef3473e978a59e03d1945186e10e9e87e239900f8809b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34164592745487dbb365adf6e9d13f2f0b81e1a3eea3366170045c51fbf2664d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f63729dbc65f33e83019a3ac8a8c58eeec8601aa6a2df47223a4e22cc7035245(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cd757c88ee6d3a48bfe5dd66bf62d2b64866fc91cd29de59b947ff4f9d8eb08(
    value: typing.Optional[GoogleNetworkConnectivityPolicyBasedRouteWarnings],
) -> None:
    """Type checking stubs"""
    pass
