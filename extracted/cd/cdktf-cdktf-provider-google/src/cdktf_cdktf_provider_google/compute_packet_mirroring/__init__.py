r'''
# `google_compute_packet_mirroring`

Refer to the Terraform Registry for docs: [`google_compute_packet_mirroring`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring).
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


class ComputePacketMirroring(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computePacketMirroring.ComputePacketMirroring",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring google_compute_packet_mirroring}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        collector_ilb: typing.Union["ComputePacketMirroringCollectorIlb", typing.Dict[builtins.str, typing.Any]],
        mirrored_resources: typing.Union["ComputePacketMirroringMirroredResources", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        network: typing.Union["ComputePacketMirroringNetwork", typing.Dict[builtins.str, typing.Any]],
        description: typing.Optional[builtins.str] = None,
        filter: typing.Optional[typing.Union["ComputePacketMirroringFilter", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        priority: typing.Optional[jsii.Number] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ComputePacketMirroringTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring google_compute_packet_mirroring} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param collector_ilb: collector_ilb block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring#collector_ilb ComputePacketMirroring#collector_ilb}
        :param mirrored_resources: mirrored_resources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring#mirrored_resources ComputePacketMirroring#mirrored_resources}
        :param name: The name of the packet mirroring rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring#name ComputePacketMirroring#name}
        :param network: network block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring#network ComputePacketMirroring#network}
        :param description: A human-readable description of the rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring#description ComputePacketMirroring#description}
        :param filter: filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring#filter ComputePacketMirroring#filter}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring#id ComputePacketMirroring#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param priority: Since only one rule can be active at a time, priority is used to break ties in the case of two rules that apply to the same instances. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring#priority ComputePacketMirroring#priority}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring#project ComputePacketMirroring#project}.
        :param region: The Region in which the created address should reside. If it is not provided, the provider region is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring#region ComputePacketMirroring#region}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring#timeouts ComputePacketMirroring#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bee84ae7eb595967427e41c6132e50fbb1efe9ae3f0387164071fe13918aeec6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ComputePacketMirroringConfig(
            collector_ilb=collector_ilb,
            mirrored_resources=mirrored_resources,
            name=name,
            network=network,
            description=description,
            filter=filter,
            id=id,
            priority=priority,
            project=project,
            region=region,
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
        '''Generates CDKTF code for importing a ComputePacketMirroring resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ComputePacketMirroring to import.
        :param import_from_id: The id of the existing ComputePacketMirroring that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ComputePacketMirroring to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e1989c73951c6061c1bd9d051f92d2a502386dedb5f3173d8ba0851b2323723)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCollectorIlb")
    def put_collector_ilb(self, *, url: builtins.str) -> None:
        '''
        :param url: The URL of the forwarding rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring#url ComputePacketMirroring#url}
        '''
        value = ComputePacketMirroringCollectorIlb(url=url)

        return typing.cast(None, jsii.invoke(self, "putCollectorIlb", [value]))

    @jsii.member(jsii_name="putFilter")
    def put_filter(
        self,
        *,
        cidr_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        direction: typing.Optional[builtins.str] = None,
        ip_protocols: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param cidr_ranges: IP CIDR ranges that apply as a filter on the source (ingress) or destination (egress) IP in the IP header. Only IPv4 is supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring#cidr_ranges ComputePacketMirroring#cidr_ranges}
        :param direction: Direction of traffic to mirror. Default value: "BOTH" Possible values: ["INGRESS", "EGRESS", "BOTH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring#direction ComputePacketMirroring#direction}
        :param ip_protocols: Possible IP protocols including tcp, udp, icmp and esp. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring#ip_protocols ComputePacketMirroring#ip_protocols}
        '''
        value = ComputePacketMirroringFilter(
            cidr_ranges=cidr_ranges, direction=direction, ip_protocols=ip_protocols
        )

        return typing.cast(None, jsii.invoke(self, "putFilter", [value]))

    @jsii.member(jsii_name="putMirroredResources")
    def put_mirrored_resources(
        self,
        *,
        instances: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputePacketMirroringMirroredResourcesInstances", typing.Dict[builtins.str, typing.Any]]]]] = None,
        subnetworks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputePacketMirroringMirroredResourcesSubnetworks", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param instances: instances block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring#instances ComputePacketMirroring#instances}
        :param subnetworks: subnetworks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring#subnetworks ComputePacketMirroring#subnetworks}
        :param tags: All instances with these tags will be mirrored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring#tags ComputePacketMirroring#tags}
        '''
        value = ComputePacketMirroringMirroredResources(
            instances=instances, subnetworks=subnetworks, tags=tags
        )

        return typing.cast(None, jsii.invoke(self, "putMirroredResources", [value]))

    @jsii.member(jsii_name="putNetwork")
    def put_network(self, *, url: builtins.str) -> None:
        '''
        :param url: The full self_link URL of the network where this rule is active. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring#url ComputePacketMirroring#url}
        '''
        value = ComputePacketMirroringNetwork(url=url)

        return typing.cast(None, jsii.invoke(self, "putNetwork", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring#create ComputePacketMirroring#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring#delete ComputePacketMirroring#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring#update ComputePacketMirroring#update}.
        '''
        value = ComputePacketMirroringTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetFilter")
    def reset_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilter", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetPriority")
    def reset_priority(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPriority", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

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
    @jsii.member(jsii_name="collectorIlb")
    def collector_ilb(self) -> "ComputePacketMirroringCollectorIlbOutputReference":
        return typing.cast("ComputePacketMirroringCollectorIlbOutputReference", jsii.get(self, "collectorIlb"))

    @builtins.property
    @jsii.member(jsii_name="filter")
    def filter(self) -> "ComputePacketMirroringFilterOutputReference":
        return typing.cast("ComputePacketMirroringFilterOutputReference", jsii.get(self, "filter"))

    @builtins.property
    @jsii.member(jsii_name="mirroredResources")
    def mirrored_resources(
        self,
    ) -> "ComputePacketMirroringMirroredResourcesOutputReference":
        return typing.cast("ComputePacketMirroringMirroredResourcesOutputReference", jsii.get(self, "mirroredResources"))

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> "ComputePacketMirroringNetworkOutputReference":
        return typing.cast("ComputePacketMirroringNetworkOutputReference", jsii.get(self, "network"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ComputePacketMirroringTimeoutsOutputReference":
        return typing.cast("ComputePacketMirroringTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="collectorIlbInput")
    def collector_ilb_input(
        self,
    ) -> typing.Optional["ComputePacketMirroringCollectorIlb"]:
        return typing.cast(typing.Optional["ComputePacketMirroringCollectorIlb"], jsii.get(self, "collectorIlbInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="filterInput")
    def filter_input(self) -> typing.Optional["ComputePacketMirroringFilter"]:
        return typing.cast(typing.Optional["ComputePacketMirroringFilter"], jsii.get(self, "filterInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="mirroredResourcesInput")
    def mirrored_resources_input(
        self,
    ) -> typing.Optional["ComputePacketMirroringMirroredResources"]:
        return typing.cast(typing.Optional["ComputePacketMirroringMirroredResources"], jsii.get(self, "mirroredResourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkInput")
    def network_input(self) -> typing.Optional["ComputePacketMirroringNetwork"]:
        return typing.cast(typing.Optional["ComputePacketMirroringNetwork"], jsii.get(self, "networkInput"))

    @builtins.property
    @jsii.member(jsii_name="priorityInput")
    def priority_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "priorityInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputePacketMirroringTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputePacketMirroringTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c13ab63c5081ffc4d48ce946dc61b55cc26933483b7d82cf304eabb69bb988c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a69f5ca866d9f92061eebab5a90e88f9ea1bc01d7e650865ed9b01c9a28311ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d19a3be81da7f8bd92880d777b47e655cee807c7b8813cb32550d3a158a2f7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a8181d82a381c3ff25b13f8195c03d05d45f9c03a356f81d6adc52199db5765)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4061d9da77ed923ad0cb5870151eb74aba27fa7a5fd90c85b80fa91a5051839)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a99133abae81ac4824dcccb1425e74712f117804b6f32d386a8ebc1377e6d23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computePacketMirroring.ComputePacketMirroringCollectorIlb",
    jsii_struct_bases=[],
    name_mapping={"url": "url"},
)
class ComputePacketMirroringCollectorIlb:
    def __init__(self, *, url: builtins.str) -> None:
        '''
        :param url: The URL of the forwarding rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring#url ComputePacketMirroring#url}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d0d969db7a37ab8faa85588b141797aa969aa1e2cc3397021f02f6d2f6e8b1e)
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "url": url,
        }

    @builtins.property
    def url(self) -> builtins.str:
        '''The URL of the forwarding rule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring#url ComputePacketMirroring#url}
        '''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputePacketMirroringCollectorIlb(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputePacketMirroringCollectorIlbOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computePacketMirroring.ComputePacketMirroringCollectorIlbOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cf6f7cd8683db643713ada3794b76595adaac91f7243e4d6e8b812579d36fe85)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="urlInput")
    def url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlInput"))

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88b85c64aa18f62e0c1b84b0cc36f817d94361f540d19d85ef2e22a277201860)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputePacketMirroringCollectorIlb]:
        return typing.cast(typing.Optional[ComputePacketMirroringCollectorIlb], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputePacketMirroringCollectorIlb],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6de04d234ad389f2a84a62f160a24942648b559ff2b4a5b738c1f793ca7416e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computePacketMirroring.ComputePacketMirroringConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "collector_ilb": "collectorIlb",
        "mirrored_resources": "mirroredResources",
        "name": "name",
        "network": "network",
        "description": "description",
        "filter": "filter",
        "id": "id",
        "priority": "priority",
        "project": "project",
        "region": "region",
        "timeouts": "timeouts",
    },
)
class ComputePacketMirroringConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        collector_ilb: typing.Union[ComputePacketMirroringCollectorIlb, typing.Dict[builtins.str, typing.Any]],
        mirrored_resources: typing.Union["ComputePacketMirroringMirroredResources", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        network: typing.Union["ComputePacketMirroringNetwork", typing.Dict[builtins.str, typing.Any]],
        description: typing.Optional[builtins.str] = None,
        filter: typing.Optional[typing.Union["ComputePacketMirroringFilter", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        priority: typing.Optional[jsii.Number] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ComputePacketMirroringTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param collector_ilb: collector_ilb block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring#collector_ilb ComputePacketMirroring#collector_ilb}
        :param mirrored_resources: mirrored_resources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring#mirrored_resources ComputePacketMirroring#mirrored_resources}
        :param name: The name of the packet mirroring rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring#name ComputePacketMirroring#name}
        :param network: network block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring#network ComputePacketMirroring#network}
        :param description: A human-readable description of the rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring#description ComputePacketMirroring#description}
        :param filter: filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring#filter ComputePacketMirroring#filter}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring#id ComputePacketMirroring#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param priority: Since only one rule can be active at a time, priority is used to break ties in the case of two rules that apply to the same instances. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring#priority ComputePacketMirroring#priority}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring#project ComputePacketMirroring#project}.
        :param region: The Region in which the created address should reside. If it is not provided, the provider region is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring#region ComputePacketMirroring#region}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring#timeouts ComputePacketMirroring#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(collector_ilb, dict):
            collector_ilb = ComputePacketMirroringCollectorIlb(**collector_ilb)
        if isinstance(mirrored_resources, dict):
            mirrored_resources = ComputePacketMirroringMirroredResources(**mirrored_resources)
        if isinstance(network, dict):
            network = ComputePacketMirroringNetwork(**network)
        if isinstance(filter, dict):
            filter = ComputePacketMirroringFilter(**filter)
        if isinstance(timeouts, dict):
            timeouts = ComputePacketMirroringTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15f0e2abf12ad55cfebe35e0d238e987d26d83a4e87c8196c668e33552800c03)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument collector_ilb", value=collector_ilb, expected_type=type_hints["collector_ilb"])
            check_type(argname="argument mirrored_resources", value=mirrored_resources, expected_type=type_hints["mirrored_resources"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "collector_ilb": collector_ilb,
            "mirrored_resources": mirrored_resources,
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
        if filter is not None:
            self._values["filter"] = filter
        if id is not None:
            self._values["id"] = id
        if priority is not None:
            self._values["priority"] = priority
        if project is not None:
            self._values["project"] = project
        if region is not None:
            self._values["region"] = region
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
    def collector_ilb(self) -> ComputePacketMirroringCollectorIlb:
        '''collector_ilb block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring#collector_ilb ComputePacketMirroring#collector_ilb}
        '''
        result = self._values.get("collector_ilb")
        assert result is not None, "Required property 'collector_ilb' is missing"
        return typing.cast(ComputePacketMirroringCollectorIlb, result)

    @builtins.property
    def mirrored_resources(self) -> "ComputePacketMirroringMirroredResources":
        '''mirrored_resources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring#mirrored_resources ComputePacketMirroring#mirrored_resources}
        '''
        result = self._values.get("mirrored_resources")
        assert result is not None, "Required property 'mirrored_resources' is missing"
        return typing.cast("ComputePacketMirroringMirroredResources", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the packet mirroring rule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring#name ComputePacketMirroring#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def network(self) -> "ComputePacketMirroringNetwork":
        '''network block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring#network ComputePacketMirroring#network}
        '''
        result = self._values.get("network")
        assert result is not None, "Required property 'network' is missing"
        return typing.cast("ComputePacketMirroringNetwork", result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A human-readable description of the rule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring#description ComputePacketMirroring#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def filter(self) -> typing.Optional["ComputePacketMirroringFilter"]:
        '''filter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring#filter ComputePacketMirroring#filter}
        '''
        result = self._values.get("filter")
        return typing.cast(typing.Optional["ComputePacketMirroringFilter"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring#id ComputePacketMirroring#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        '''Since only one rule can be active at a time, priority is used to break ties in the case of two rules that apply to the same instances.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring#priority ComputePacketMirroring#priority}
        '''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring#project ComputePacketMirroring#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The Region in which the created address should reside. If it is not provided, the provider region is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring#region ComputePacketMirroring#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ComputePacketMirroringTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring#timeouts ComputePacketMirroring#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ComputePacketMirroringTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputePacketMirroringConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computePacketMirroring.ComputePacketMirroringFilter",
    jsii_struct_bases=[],
    name_mapping={
        "cidr_ranges": "cidrRanges",
        "direction": "direction",
        "ip_protocols": "ipProtocols",
    },
)
class ComputePacketMirroringFilter:
    def __init__(
        self,
        *,
        cidr_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        direction: typing.Optional[builtins.str] = None,
        ip_protocols: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param cidr_ranges: IP CIDR ranges that apply as a filter on the source (ingress) or destination (egress) IP in the IP header. Only IPv4 is supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring#cidr_ranges ComputePacketMirroring#cidr_ranges}
        :param direction: Direction of traffic to mirror. Default value: "BOTH" Possible values: ["INGRESS", "EGRESS", "BOTH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring#direction ComputePacketMirroring#direction}
        :param ip_protocols: Possible IP protocols including tcp, udp, icmp and esp. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring#ip_protocols ComputePacketMirroring#ip_protocols}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__703a20cebe6b5063588eba36d2b95dec420bada96e8f87f1067fefb6f7f088b7)
            check_type(argname="argument cidr_ranges", value=cidr_ranges, expected_type=type_hints["cidr_ranges"])
            check_type(argname="argument direction", value=direction, expected_type=type_hints["direction"])
            check_type(argname="argument ip_protocols", value=ip_protocols, expected_type=type_hints["ip_protocols"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cidr_ranges is not None:
            self._values["cidr_ranges"] = cidr_ranges
        if direction is not None:
            self._values["direction"] = direction
        if ip_protocols is not None:
            self._values["ip_protocols"] = ip_protocols

    @builtins.property
    def cidr_ranges(self) -> typing.Optional[typing.List[builtins.str]]:
        '''IP CIDR ranges that apply as a filter on the source (ingress) or destination (egress) IP in the IP header.

        Only IPv4 is supported.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring#cidr_ranges ComputePacketMirroring#cidr_ranges}
        '''
        result = self._values.get("cidr_ranges")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def direction(self) -> typing.Optional[builtins.str]:
        '''Direction of traffic to mirror. Default value: "BOTH" Possible values: ["INGRESS", "EGRESS", "BOTH"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring#direction ComputePacketMirroring#direction}
        '''
        result = self._values.get("direction")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_protocols(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Possible IP protocols including tcp, udp, icmp and esp.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring#ip_protocols ComputePacketMirroring#ip_protocols}
        '''
        result = self._values.get("ip_protocols")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputePacketMirroringFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputePacketMirroringFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computePacketMirroring.ComputePacketMirroringFilterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__24afbdccd204a9b6c2aea19127916e1e84ea55367038c9485b999a0836f34656)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCidrRanges")
    def reset_cidr_ranges(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCidrRanges", []))

    @jsii.member(jsii_name="resetDirection")
    def reset_direction(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDirection", []))

    @jsii.member(jsii_name="resetIpProtocols")
    def reset_ip_protocols(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpProtocols", []))

    @builtins.property
    @jsii.member(jsii_name="cidrRangesInput")
    def cidr_ranges_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "cidrRangesInput"))

    @builtins.property
    @jsii.member(jsii_name="directionInput")
    def direction_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "directionInput"))

    @builtins.property
    @jsii.member(jsii_name="ipProtocolsInput")
    def ip_protocols_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "ipProtocolsInput"))

    @builtins.property
    @jsii.member(jsii_name="cidrRanges")
    def cidr_ranges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "cidrRanges"))

    @cidr_ranges.setter
    def cidr_ranges(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0ce447a9b648eb200c0f813c855a7e3690848772bb1b2575c034de2ec206222)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cidrRanges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="direction")
    def direction(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "direction"))

    @direction.setter
    def direction(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f60d7fb2c91fcd1a222a8b2f6ece3f68d7e534470acbe4e31fd7de92c64e0cc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "direction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipProtocols")
    def ip_protocols(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ipProtocols"))

    @ip_protocols.setter
    def ip_protocols(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d21aab39a07600e29dcbe3b9d58a112f65dd9cc59e17a2eec5069a591ee1d2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipProtocols", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputePacketMirroringFilter]:
        return typing.cast(typing.Optional[ComputePacketMirroringFilter], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputePacketMirroringFilter],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50d712eb7d1b76162159c49e2b6c6b8f2896cf56ad0a9c375dc72a7c95984306)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computePacketMirroring.ComputePacketMirroringMirroredResources",
    jsii_struct_bases=[],
    name_mapping={
        "instances": "instances",
        "subnetworks": "subnetworks",
        "tags": "tags",
    },
)
class ComputePacketMirroringMirroredResources:
    def __init__(
        self,
        *,
        instances: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputePacketMirroringMirroredResourcesInstances", typing.Dict[builtins.str, typing.Any]]]]] = None,
        subnetworks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputePacketMirroringMirroredResourcesSubnetworks", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param instances: instances block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring#instances ComputePacketMirroring#instances}
        :param subnetworks: subnetworks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring#subnetworks ComputePacketMirroring#subnetworks}
        :param tags: All instances with these tags will be mirrored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring#tags ComputePacketMirroring#tags}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e9422a5b8eebf0943880e6f9706184eec695016b1460acf81be677be335cd44)
            check_type(argname="argument instances", value=instances, expected_type=type_hints["instances"])
            check_type(argname="argument subnetworks", value=subnetworks, expected_type=type_hints["subnetworks"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if instances is not None:
            self._values["instances"] = instances
        if subnetworks is not None:
            self._values["subnetworks"] = subnetworks
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def instances(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputePacketMirroringMirroredResourcesInstances"]]]:
        '''instances block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring#instances ComputePacketMirroring#instances}
        '''
        result = self._values.get("instances")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputePacketMirroringMirroredResourcesInstances"]]], result)

    @builtins.property
    def subnetworks(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputePacketMirroringMirroredResourcesSubnetworks"]]]:
        '''subnetworks block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring#subnetworks ComputePacketMirroring#subnetworks}
        '''
        result = self._values.get("subnetworks")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputePacketMirroringMirroredResourcesSubnetworks"]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''All instances with these tags will be mirrored.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring#tags ComputePacketMirroring#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputePacketMirroringMirroredResources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computePacketMirroring.ComputePacketMirroringMirroredResourcesInstances",
    jsii_struct_bases=[],
    name_mapping={"url": "url"},
)
class ComputePacketMirroringMirroredResourcesInstances:
    def __init__(self, *, url: builtins.str) -> None:
        '''
        :param url: The URL of the instances where this rule should be active. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring#url ComputePacketMirroring#url}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b506983317a9cdcaee49cfec92b1f6d5cc6e50e5f031b62506b2d81d5c1206aa)
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "url": url,
        }

    @builtins.property
    def url(self) -> builtins.str:
        '''The URL of the instances where this rule should be active.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring#url ComputePacketMirroring#url}
        '''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputePacketMirroringMirroredResourcesInstances(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputePacketMirroringMirroredResourcesInstancesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computePacketMirroring.ComputePacketMirroringMirroredResourcesInstancesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb3c70b8be18a5b2660eebd685bd2b24990c45112f3c05df17ca7f3866190435)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputePacketMirroringMirroredResourcesInstancesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47319773c699bef92d9a0369d42a8a27869171f00f8ec562fd8d849b929c05e3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputePacketMirroringMirroredResourcesInstancesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbb931d45fde62ab66be54f635babb80e24ed1a1729b0e9cde69d278955c3454)
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
            type_hints = typing.get_type_hints(_typecheckingstub__95c69f5c6327e1ea27ae60805cd7730e9e4fef98f924248e4cecd2d5dd19bb50)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf0907db3179641d3dc2cee4b0e14ad619e2a48d19fe96725ffa6d23ef247a66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputePacketMirroringMirroredResourcesInstances]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputePacketMirroringMirroredResourcesInstances]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputePacketMirroringMirroredResourcesInstances]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99589624a9e2c44de6a77cb92ea1a6a98b8a03b07be42dd7f3b7260425fe327e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputePacketMirroringMirroredResourcesInstancesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computePacketMirroring.ComputePacketMirroringMirroredResourcesInstancesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a21b2d0d3f1c29cb124f097db54b9a1596ee3c2f5c71c6c72fceed152e43f87c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="urlInput")
    def url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlInput"))

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76b73b948173114fcc029d25de6b55f62efc980bd2622f0ef49348c152b32b53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputePacketMirroringMirroredResourcesInstances]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputePacketMirroringMirroredResourcesInstances]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputePacketMirroringMirroredResourcesInstances]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26465c599ae06ef81cf749681cf405b28bab86f7459bdf0d0501857784f4ab15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputePacketMirroringMirroredResourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computePacketMirroring.ComputePacketMirroringMirroredResourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e13000156eda51ac11b2b5de6e7df6d582188b06b605bd4baf0116f5ada99615)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putInstances")
    def put_instances(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputePacketMirroringMirroredResourcesInstances, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2c81a426f852962552f6260a45df7688242417263ec8c228e731d387ef7eb54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInstances", [value]))

    @jsii.member(jsii_name="putSubnetworks")
    def put_subnetworks(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputePacketMirroringMirroredResourcesSubnetworks", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df7a13fcc5dfa7b0b69c67173c6dfaefc1545384f5536427b42810eb948e555d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSubnetworks", [value]))

    @jsii.member(jsii_name="resetInstances")
    def reset_instances(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstances", []))

    @jsii.member(jsii_name="resetSubnetworks")
    def reset_subnetworks(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnetworks", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @builtins.property
    @jsii.member(jsii_name="instances")
    def instances(self) -> ComputePacketMirroringMirroredResourcesInstancesList:
        return typing.cast(ComputePacketMirroringMirroredResourcesInstancesList, jsii.get(self, "instances"))

    @builtins.property
    @jsii.member(jsii_name="subnetworks")
    def subnetworks(self) -> "ComputePacketMirroringMirroredResourcesSubnetworksList":
        return typing.cast("ComputePacketMirroringMirroredResourcesSubnetworksList", jsii.get(self, "subnetworks"))

    @builtins.property
    @jsii.member(jsii_name="instancesInput")
    def instances_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputePacketMirroringMirroredResourcesInstances]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputePacketMirroringMirroredResourcesInstances]]], jsii.get(self, "instancesInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetworksInput")
    def subnetworks_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputePacketMirroringMirroredResourcesSubnetworks"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputePacketMirroringMirroredResourcesSubnetworks"]]], jsii.get(self, "subnetworksInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__6759eccb7ea4652d59de0d182697344a1bbc1481cd2f77e5e72f6d5a8dd0f8a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputePacketMirroringMirroredResources]:
        return typing.cast(typing.Optional[ComputePacketMirroringMirroredResources], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputePacketMirroringMirroredResources],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b132cf18aba361b751ee7a818420a251bed166ea5db7b9a48feb41a91669c15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computePacketMirroring.ComputePacketMirroringMirroredResourcesSubnetworks",
    jsii_struct_bases=[],
    name_mapping={"url": "url"},
)
class ComputePacketMirroringMirroredResourcesSubnetworks:
    def __init__(self, *, url: builtins.str) -> None:
        '''
        :param url: The URL of the subnetwork where this rule should be active. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring#url ComputePacketMirroring#url}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7560f6c8dd83394f4a2bb35e7e34c7ecb378179ce5fa9a4c5a9ed21f22321da)
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "url": url,
        }

    @builtins.property
    def url(self) -> builtins.str:
        '''The URL of the subnetwork where this rule should be active.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring#url ComputePacketMirroring#url}
        '''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputePacketMirroringMirroredResourcesSubnetworks(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputePacketMirroringMirroredResourcesSubnetworksList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computePacketMirroring.ComputePacketMirroringMirroredResourcesSubnetworksList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b9212deaf115f5aaf1813533fd9377940747c84540bd8265e14f144235210b92)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputePacketMirroringMirroredResourcesSubnetworksOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0f692675cb326af769dedf83bda19f4b4e68a4b5e566b0a30a55752c3e5e1c5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputePacketMirroringMirroredResourcesSubnetworksOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44eea7fd06253ead8ded7d5aab2a7e090675870cd520eccbe354ba446563ee6b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a422a03d74e89ea45abce81010a49b79899d229b5ca9786d5779b17a4bac086)
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
            type_hints = typing.get_type_hints(_typecheckingstub__35a0ebf80a738aaea97fd776cc887dd4e883e18555c544a40fe90be17c4147d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputePacketMirroringMirroredResourcesSubnetworks]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputePacketMirroringMirroredResourcesSubnetworks]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputePacketMirroringMirroredResourcesSubnetworks]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcf52f7d59d2609bac00441340e565731066d26f3d847248df5e65bffb0b5bda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputePacketMirroringMirroredResourcesSubnetworksOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computePacketMirroring.ComputePacketMirroringMirroredResourcesSubnetworksOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a7ba7c41293037172ea3199939bd1b9e69cc4a3de8dfbd1792982ffecd2639e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="urlInput")
    def url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlInput"))

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a65e6956e6a116bd4cd960df070d37e4776e6562ef81f24b5b348d867cb0b0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputePacketMirroringMirroredResourcesSubnetworks]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputePacketMirroringMirroredResourcesSubnetworks]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputePacketMirroringMirroredResourcesSubnetworks]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c2520acaa35efcbd6aa56709bf4c3c28d9922e776361308f91f134d0acc5bb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computePacketMirroring.ComputePacketMirroringNetwork",
    jsii_struct_bases=[],
    name_mapping={"url": "url"},
)
class ComputePacketMirroringNetwork:
    def __init__(self, *, url: builtins.str) -> None:
        '''
        :param url: The full self_link URL of the network where this rule is active. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring#url ComputePacketMirroring#url}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e986550cf796e35fb31524eaa4edefb5bfc78c2d5b5d39533df350931c75c84b)
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "url": url,
        }

    @builtins.property
    def url(self) -> builtins.str:
        '''The full self_link URL of the network where this rule is active.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring#url ComputePacketMirroring#url}
        '''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputePacketMirroringNetwork(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputePacketMirroringNetworkOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computePacketMirroring.ComputePacketMirroringNetworkOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e0b7e938b9ef8dd0965520d66e45ed22ffe011d84bedcc50f61385d219f9d41a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="urlInput")
    def url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlInput"))

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c4328c445a74695db79bbb1416570cd00d5afde73b889ce48fffc66cc572e67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputePacketMirroringNetwork]:
        return typing.cast(typing.Optional[ComputePacketMirroringNetwork], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputePacketMirroringNetwork],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__847e6a37dee9b155a8394c62507ed1fe610b2be4bb9b6f3a816174f631d616d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computePacketMirroring.ComputePacketMirroringTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ComputePacketMirroringTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring#create ComputePacketMirroring#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring#delete ComputePacketMirroring#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring#update ComputePacketMirroring#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f721745301338c43d18408a7b07c09d8e00e3348ebce8105f16333e65718d301)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring#create ComputePacketMirroring#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring#delete ComputePacketMirroring#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_packet_mirroring#update ComputePacketMirroring#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputePacketMirroringTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputePacketMirroringTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computePacketMirroring.ComputePacketMirroringTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__407df953f508d59a80feea8df7595fae250f3f7741f5767baed1bbfb50dcf388)
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
            type_hints = typing.get_type_hints(_typecheckingstub__886b17b2ec6d8f7d68747e9a6dc3b7a65ec0ec21b6049e102d5404ba4c206879)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75e950589f61647a11992617ce48ba02f72061459369b27fdc2eb968a136334f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e749f96cd5351631f72660a6d4e6241e1f17f7a3882327469d160294c36b519d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputePacketMirroringTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputePacketMirroringTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputePacketMirroringTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cdebc9195c81eff00e05f66a416211aab0d3bf414e907c31158952c597701ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ComputePacketMirroring",
    "ComputePacketMirroringCollectorIlb",
    "ComputePacketMirroringCollectorIlbOutputReference",
    "ComputePacketMirroringConfig",
    "ComputePacketMirroringFilter",
    "ComputePacketMirroringFilterOutputReference",
    "ComputePacketMirroringMirroredResources",
    "ComputePacketMirroringMirroredResourcesInstances",
    "ComputePacketMirroringMirroredResourcesInstancesList",
    "ComputePacketMirroringMirroredResourcesInstancesOutputReference",
    "ComputePacketMirroringMirroredResourcesOutputReference",
    "ComputePacketMirroringMirroredResourcesSubnetworks",
    "ComputePacketMirroringMirroredResourcesSubnetworksList",
    "ComputePacketMirroringMirroredResourcesSubnetworksOutputReference",
    "ComputePacketMirroringNetwork",
    "ComputePacketMirroringNetworkOutputReference",
    "ComputePacketMirroringTimeouts",
    "ComputePacketMirroringTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__bee84ae7eb595967427e41c6132e50fbb1efe9ae3f0387164071fe13918aeec6(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    collector_ilb: typing.Union[ComputePacketMirroringCollectorIlb, typing.Dict[builtins.str, typing.Any]],
    mirrored_resources: typing.Union[ComputePacketMirroringMirroredResources, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    network: typing.Union[ComputePacketMirroringNetwork, typing.Dict[builtins.str, typing.Any]],
    description: typing.Optional[builtins.str] = None,
    filter: typing.Optional[typing.Union[ComputePacketMirroringFilter, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    priority: typing.Optional[jsii.Number] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ComputePacketMirroringTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__8e1989c73951c6061c1bd9d051f92d2a502386dedb5f3173d8ba0851b2323723(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c13ab63c5081ffc4d48ce946dc61b55cc26933483b7d82cf304eabb69bb988c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a69f5ca866d9f92061eebab5a90e88f9ea1bc01d7e650865ed9b01c9a28311ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d19a3be81da7f8bd92880d777b47e655cee807c7b8813cb32550d3a158a2f7e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a8181d82a381c3ff25b13f8195c03d05d45f9c03a356f81d6adc52199db5765(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4061d9da77ed923ad0cb5870151eb74aba27fa7a5fd90c85b80fa91a5051839(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a99133abae81ac4824dcccb1425e74712f117804b6f32d386a8ebc1377e6d23(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d0d969db7a37ab8faa85588b141797aa969aa1e2cc3397021f02f6d2f6e8b1e(
    *,
    url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf6f7cd8683db643713ada3794b76595adaac91f7243e4d6e8b812579d36fe85(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88b85c64aa18f62e0c1b84b0cc36f817d94361f540d19d85ef2e22a277201860(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6de04d234ad389f2a84a62f160a24942648b559ff2b4a5b738c1f793ca7416e9(
    value: typing.Optional[ComputePacketMirroringCollectorIlb],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15f0e2abf12ad55cfebe35e0d238e987d26d83a4e87c8196c668e33552800c03(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    collector_ilb: typing.Union[ComputePacketMirroringCollectorIlb, typing.Dict[builtins.str, typing.Any]],
    mirrored_resources: typing.Union[ComputePacketMirroringMirroredResources, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    network: typing.Union[ComputePacketMirroringNetwork, typing.Dict[builtins.str, typing.Any]],
    description: typing.Optional[builtins.str] = None,
    filter: typing.Optional[typing.Union[ComputePacketMirroringFilter, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    priority: typing.Optional[jsii.Number] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ComputePacketMirroringTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__703a20cebe6b5063588eba36d2b95dec420bada96e8f87f1067fefb6f7f088b7(
    *,
    cidr_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    direction: typing.Optional[builtins.str] = None,
    ip_protocols: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24afbdccd204a9b6c2aea19127916e1e84ea55367038c9485b999a0836f34656(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0ce447a9b648eb200c0f813c855a7e3690848772bb1b2575c034de2ec206222(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f60d7fb2c91fcd1a222a8b2f6ece3f68d7e534470acbe4e31fd7de92c64e0cc2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d21aab39a07600e29dcbe3b9d58a112f65dd9cc59e17a2eec5069a591ee1d2c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50d712eb7d1b76162159c49e2b6c6b8f2896cf56ad0a9c375dc72a7c95984306(
    value: typing.Optional[ComputePacketMirroringFilter],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e9422a5b8eebf0943880e6f9706184eec695016b1460acf81be677be335cd44(
    *,
    instances: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputePacketMirroringMirroredResourcesInstances, typing.Dict[builtins.str, typing.Any]]]]] = None,
    subnetworks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputePacketMirroringMirroredResourcesSubnetworks, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b506983317a9cdcaee49cfec92b1f6d5cc6e50e5f031b62506b2d81d5c1206aa(
    *,
    url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb3c70b8be18a5b2660eebd685bd2b24990c45112f3c05df17ca7f3866190435(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47319773c699bef92d9a0369d42a8a27869171f00f8ec562fd8d849b929c05e3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbb931d45fde62ab66be54f635babb80e24ed1a1729b0e9cde69d278955c3454(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95c69f5c6327e1ea27ae60805cd7730e9e4fef98f924248e4cecd2d5dd19bb50(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf0907db3179641d3dc2cee4b0e14ad619e2a48d19fe96725ffa6d23ef247a66(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99589624a9e2c44de6a77cb92ea1a6a98b8a03b07be42dd7f3b7260425fe327e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputePacketMirroringMirroredResourcesInstances]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a21b2d0d3f1c29cb124f097db54b9a1596ee3c2f5c71c6c72fceed152e43f87c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76b73b948173114fcc029d25de6b55f62efc980bd2622f0ef49348c152b32b53(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26465c599ae06ef81cf749681cf405b28bab86f7459bdf0d0501857784f4ab15(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputePacketMirroringMirroredResourcesInstances]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e13000156eda51ac11b2b5de6e7df6d582188b06b605bd4baf0116f5ada99615(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2c81a426f852962552f6260a45df7688242417263ec8c228e731d387ef7eb54(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputePacketMirroringMirroredResourcesInstances, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df7a13fcc5dfa7b0b69c67173c6dfaefc1545384f5536427b42810eb948e555d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputePacketMirroringMirroredResourcesSubnetworks, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6759eccb7ea4652d59de0d182697344a1bbc1481cd2f77e5e72f6d5a8dd0f8a4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b132cf18aba361b751ee7a818420a251bed166ea5db7b9a48feb41a91669c15(
    value: typing.Optional[ComputePacketMirroringMirroredResources],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7560f6c8dd83394f4a2bb35e7e34c7ecb378179ce5fa9a4c5a9ed21f22321da(
    *,
    url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9212deaf115f5aaf1813533fd9377940747c84540bd8265e14f144235210b92(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0f692675cb326af769dedf83bda19f4b4e68a4b5e566b0a30a55752c3e5e1c5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44eea7fd06253ead8ded7d5aab2a7e090675870cd520eccbe354ba446563ee6b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a422a03d74e89ea45abce81010a49b79899d229b5ca9786d5779b17a4bac086(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35a0ebf80a738aaea97fd776cc887dd4e883e18555c544a40fe90be17c4147d0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcf52f7d59d2609bac00441340e565731066d26f3d847248df5e65bffb0b5bda(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputePacketMirroringMirroredResourcesSubnetworks]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a7ba7c41293037172ea3199939bd1b9e69cc4a3de8dfbd1792982ffecd2639e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a65e6956e6a116bd4cd960df070d37e4776e6562ef81f24b5b348d867cb0b0d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c2520acaa35efcbd6aa56709bf4c3c28d9922e776361308f91f134d0acc5bb5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputePacketMirroringMirroredResourcesSubnetworks]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e986550cf796e35fb31524eaa4edefb5bfc78c2d5b5d39533df350931c75c84b(
    *,
    url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0b7e938b9ef8dd0965520d66e45ed22ffe011d84bedcc50f61385d219f9d41a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c4328c445a74695db79bbb1416570cd00d5afde73b889ce48fffc66cc572e67(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__847e6a37dee9b155a8394c62507ed1fe610b2be4bb9b6f3a816174f631d616d7(
    value: typing.Optional[ComputePacketMirroringNetwork],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f721745301338c43d18408a7b07c09d8e00e3348ebce8105f16333e65718d301(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__407df953f508d59a80feea8df7595fae250f3f7741f5767baed1bbfb50dcf388(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__886b17b2ec6d8f7d68747e9a6dc3b7a65ec0ec21b6049e102d5404ba4c206879(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75e950589f61647a11992617ce48ba02f72061459369b27fdc2eb968a136334f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e749f96cd5351631f72660a6d4e6241e1f17f7a3882327469d160294c36b519d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cdebc9195c81eff00e05f66a416211aab0d3bf414e907c31158952c597701ca(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputePacketMirroringTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
