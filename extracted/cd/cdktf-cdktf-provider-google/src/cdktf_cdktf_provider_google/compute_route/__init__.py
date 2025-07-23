r'''
# `google_compute_route`

Refer to the Terraform Registry for docs: [`google_compute_route`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_route).
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


class ComputeRoute(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRoute.ComputeRoute",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_route google_compute_route}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        dest_range: builtins.str,
        name: builtins.str,
        network: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        next_hop_gateway: typing.Optional[builtins.str] = None,
        next_hop_ilb: typing.Optional[builtins.str] = None,
        next_hop_instance: typing.Optional[builtins.str] = None,
        next_hop_instance_zone: typing.Optional[builtins.str] = None,
        next_hop_ip: typing.Optional[builtins.str] = None,
        next_hop_vpn_tunnel: typing.Optional[builtins.str] = None,
        params: typing.Optional[typing.Union["ComputeRouteParams", typing.Dict[builtins.str, typing.Any]]] = None,
        priority: typing.Optional[jsii.Number] = None,
        project: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["ComputeRouteTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_route google_compute_route} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param dest_range: The destination range of outgoing packets that this route applies to. Only IPv4 is supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_route#dest_range ComputeRoute#dest_range}
        :param name: Name of the resource. Provided by the client when the resource is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_route#name ComputeRoute#name}
        :param network: The network that this route applies to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_route#network ComputeRoute#network}
        :param description: An optional description of this resource. Provide this property when you create the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_route#description ComputeRoute#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_route#id ComputeRoute#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param next_hop_gateway: URL to a gateway that should handle matching packets. Currently, you can only specify the internet gateway, using a full or partial valid URL: - 'https://www.googleapis.com/compute/v1/projects/project/global/gateways/default-internet-gateway' - 'projects/project/global/gateways/default-internet-gateway' - 'global/gateways/default-internet-gateway' - The string 'default-internet-gateway'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_route#next_hop_gateway ComputeRoute#next_hop_gateway}
        :param next_hop_ilb: The IP address or URL to a forwarding rule of type loadBalancingScheme=INTERNAL that should handle matching packets. With the GA provider you can only specify the forwarding rule as a partial or full URL. For example, the following are all valid values: - 10.128.0.56 - https://www.googleapis.com/compute/v1/projects/project/regions/region/forwardingRules/forwardingRule - regions/region/forwardingRules/forwardingRule When the beta provider, you can also specify the IP address of a forwarding rule from the same VPC or any peered VPC. Note that this can only be used when the destinationRange is a public (non-RFC 1918) IP CIDR range. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_route#next_hop_ilb ComputeRoute#next_hop_ilb}
        :param next_hop_instance: URL to an instance that should handle matching packets. You can specify this as a full or partial URL. For example: - 'https://www.googleapis.com/compute/v1/projects/project/zones/zone/instances/instance' - 'projects/project/zones/zone/instances/instance' - 'zones/zone/instances/instance' - Just the instance name, with the zone in 'next_hop_instance_zone'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_route#next_hop_instance ComputeRoute#next_hop_instance}
        :param next_hop_instance_zone: The zone of the instance specified in next_hop_instance. Omit if next_hop_instance is specified as a URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_route#next_hop_instance_zone ComputeRoute#next_hop_instance_zone}
        :param next_hop_ip: Network IP address of an instance that should handle matching packets. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_route#next_hop_ip ComputeRoute#next_hop_ip}
        :param next_hop_vpn_tunnel: URL to a VpnTunnel that should handle matching packets. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_route#next_hop_vpn_tunnel ComputeRoute#next_hop_vpn_tunnel}
        :param params: params block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_route#params ComputeRoute#params}
        :param priority: The priority of this route. Priority is used to break ties in cases where there is more than one matching route of equal prefix length. In the case of two routes with equal prefix length, the one with the lowest-numbered priority value wins. Default value is 1000. Valid range is 0 through 65535. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_route#priority ComputeRoute#priority}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_route#project ComputeRoute#project}.
        :param tags: A list of instance tags to which this route applies. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_route#tags ComputeRoute#tags}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_route#timeouts ComputeRoute#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d70ce4466236ea531b210d9fbae9bdf5ca6ba4fa583156f91300a068309cc35f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ComputeRouteConfig(
            dest_range=dest_range,
            name=name,
            network=network,
            description=description,
            id=id,
            next_hop_gateway=next_hop_gateway,
            next_hop_ilb=next_hop_ilb,
            next_hop_instance=next_hop_instance,
            next_hop_instance_zone=next_hop_instance_zone,
            next_hop_ip=next_hop_ip,
            next_hop_vpn_tunnel=next_hop_vpn_tunnel,
            params=params,
            priority=priority,
            project=project,
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
        '''Generates CDKTF code for importing a ComputeRoute resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ComputeRoute to import.
        :param import_from_id: The id of the existing ComputeRoute that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_route#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ComputeRoute to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b1abb39e0723b976b0d0bb5023ffec66a1b1f663cfffb6b3fdd863bfce4943e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putParams")
    def put_params(
        self,
        *,
        resource_manager_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param resource_manager_tags: Resource manager tags to be bound to the route. Tag keys and values have the same definition as resource manager tags. Keys must be in the format tagKeys/{tag_key_id}, and values are in the format tagValues/456. The field is ignored when empty. The field is immutable and causes resource replacement when mutated. This field is only set at create time and modifying this field after creation will trigger recreation. To apply tags to an existing resource, see the google_tags_tag_binding resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_route#resource_manager_tags ComputeRoute#resource_manager_tags}
        '''
        value = ComputeRouteParams(resource_manager_tags=resource_manager_tags)

        return typing.cast(None, jsii.invoke(self, "putParams", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_route#create ComputeRoute#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_route#delete ComputeRoute#delete}.
        '''
        value = ComputeRouteTimeouts(create=create, delete=delete)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetNextHopGateway")
    def reset_next_hop_gateway(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNextHopGateway", []))

    @jsii.member(jsii_name="resetNextHopIlb")
    def reset_next_hop_ilb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNextHopIlb", []))

    @jsii.member(jsii_name="resetNextHopInstance")
    def reset_next_hop_instance(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNextHopInstance", []))

    @jsii.member(jsii_name="resetNextHopInstanceZone")
    def reset_next_hop_instance_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNextHopInstanceZone", []))

    @jsii.member(jsii_name="resetNextHopIp")
    def reset_next_hop_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNextHopIp", []))

    @jsii.member(jsii_name="resetNextHopVpnTunnel")
    def reset_next_hop_vpn_tunnel(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNextHopVpnTunnel", []))

    @jsii.member(jsii_name="resetParams")
    def reset_params(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParams", []))

    @jsii.member(jsii_name="resetPriority")
    def reset_priority(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPriority", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

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
    @jsii.member(jsii_name="asPaths")
    def as_paths(self) -> "ComputeRouteAsPathsList":
        return typing.cast("ComputeRouteAsPathsList", jsii.get(self, "asPaths"))

    @builtins.property
    @jsii.member(jsii_name="creationTimestamp")
    def creation_timestamp(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "creationTimestamp"))

    @builtins.property
    @jsii.member(jsii_name="nextHopHub")
    def next_hop_hub(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nextHopHub"))

    @builtins.property
    @jsii.member(jsii_name="nextHopInterRegionCost")
    def next_hop_inter_region_cost(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nextHopInterRegionCost"))

    @builtins.property
    @jsii.member(jsii_name="nextHopMed")
    def next_hop_med(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nextHopMed"))

    @builtins.property
    @jsii.member(jsii_name="nextHopNetwork")
    def next_hop_network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nextHopNetwork"))

    @builtins.property
    @jsii.member(jsii_name="nextHopOrigin")
    def next_hop_origin(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nextHopOrigin"))

    @builtins.property
    @jsii.member(jsii_name="nextHopPeering")
    def next_hop_peering(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nextHopPeering"))

    @builtins.property
    @jsii.member(jsii_name="params")
    def params(self) -> "ComputeRouteParamsOutputReference":
        return typing.cast("ComputeRouteParamsOutputReference", jsii.get(self, "params"))

    @builtins.property
    @jsii.member(jsii_name="routeStatus")
    def route_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "routeStatus"))

    @builtins.property
    @jsii.member(jsii_name="routeType")
    def route_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "routeType"))

    @builtins.property
    @jsii.member(jsii_name="selfLink")
    def self_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selfLink"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ComputeRouteTimeoutsOutputReference":
        return typing.cast("ComputeRouteTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="warnings")
    def warnings(self) -> "ComputeRouteWarningsList":
        return typing.cast("ComputeRouteWarningsList", jsii.get(self, "warnings"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="destRangeInput")
    def dest_range_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkInput")
    def network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkInput"))

    @builtins.property
    @jsii.member(jsii_name="nextHopGatewayInput")
    def next_hop_gateway_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nextHopGatewayInput"))

    @builtins.property
    @jsii.member(jsii_name="nextHopIlbInput")
    def next_hop_ilb_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nextHopIlbInput"))

    @builtins.property
    @jsii.member(jsii_name="nextHopInstanceInput")
    def next_hop_instance_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nextHopInstanceInput"))

    @builtins.property
    @jsii.member(jsii_name="nextHopInstanceZoneInput")
    def next_hop_instance_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nextHopInstanceZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="nextHopIpInput")
    def next_hop_ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nextHopIpInput"))

    @builtins.property
    @jsii.member(jsii_name="nextHopVpnTunnelInput")
    def next_hop_vpn_tunnel_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nextHopVpnTunnelInput"))

    @builtins.property
    @jsii.member(jsii_name="paramsInput")
    def params_input(self) -> typing.Optional["ComputeRouteParams"]:
        return typing.cast(typing.Optional["ComputeRouteParams"], jsii.get(self, "paramsInput"))

    @builtins.property
    @jsii.member(jsii_name="priorityInput")
    def priority_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "priorityInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeRouteTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeRouteTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6837fe40842871b443fb87059556c1d36aeed924cab8b8595d67c2188aa9690)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="destRange")
    def dest_range(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destRange"))

    @dest_range.setter
    def dest_range(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d43a1a9f83a1921cf2105ed77c5e63d628c962e3dddf5052fe32941915673603)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destRange", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3488ecafafecb58ba668d6f5aa6f525a7e8be2c5bb171c1b0af7f5dd9270112)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a877cdd5140ccbf8b6c7fb755c19daf5b871ef8aae4376da05ed4b75c74b34e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cf9f4fe83fff01ca92b637ada2e38e80796f340c331735abaedfe75679c608f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nextHopGateway")
    def next_hop_gateway(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nextHopGateway"))

    @next_hop_gateway.setter
    def next_hop_gateway(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9873e1e7d67c4f5ee9b8d2a4eef17cd97d872a0bf4cf4c21267b6801d8005382)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nextHopGateway", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nextHopIlb")
    def next_hop_ilb(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nextHopIlb"))

    @next_hop_ilb.setter
    def next_hop_ilb(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c632ac62c877e604d987512d9d5db3d73543980835d41313963b5f522c335fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nextHopIlb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nextHopInstance")
    def next_hop_instance(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nextHopInstance"))

    @next_hop_instance.setter
    def next_hop_instance(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0abbd00ac28a115cbc3a2f4496e081d15c260e889e7bd5b1c229bb3c8bda4b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nextHopInstance", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nextHopInstanceZone")
    def next_hop_instance_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nextHopInstanceZone"))

    @next_hop_instance_zone.setter
    def next_hop_instance_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ca6d24e9c55d9065aa8da982bd93d095789bae5c2bdc92429bbba0e10802c59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nextHopInstanceZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nextHopIp")
    def next_hop_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nextHopIp"))

    @next_hop_ip.setter
    def next_hop_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c562766a9b94881813c85884dff24d308497c9d6c1153035018405c6741d0a6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nextHopIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nextHopVpnTunnel")
    def next_hop_vpn_tunnel(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nextHopVpnTunnel"))

    @next_hop_vpn_tunnel.setter
    def next_hop_vpn_tunnel(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88728484394e4f7e9646b636a0dc472a46cf23def2ab8de3f8de8e9bf85fff41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nextHopVpnTunnel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__749ddcf793e6280e42c47be5cf2f54c1f4ba2f02ff3bef0928a8761a99377a49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c2a7eb2590353373d54d362f2cf0817057eb1a10492c2f2e2ca784dc3cb1c62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d55639ff75f806efb0ef6876428f5978b471b437440760b94152da7b5cbfe715)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRoute.ComputeRouteAsPaths",
    jsii_struct_bases=[],
    name_mapping={},
)
class ComputeRouteAsPaths:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRouteAsPaths(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRouteAsPathsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRoute.ComputeRouteAsPathsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4109404b0219033a571c712d4eaaf44e25fa1559cacaee9d93f8326ffa4519e5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ComputeRouteAsPathsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9eee5101902d7c32f57afaa5277a09339153b45e64267d601401ae5307eebcf1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeRouteAsPathsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8936ceb6621cf4ac58aed991ac161af34bbe944dbef32b659072d80928230028)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae024fbf059b7a6f6849fcc065b986c33588ef527caf9009afc4bb5ea857772f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__30046e42867b30e31482726ffb524fa2e3e006cf5f4464d08ede4759c3cebafc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ComputeRouteAsPathsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRoute.ComputeRouteAsPathsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d5d2648c81789a243ec766182d093036ddaddb03aa144b7c7375daaac23053f8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="asLists")
    def as_lists(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "asLists"))

    @builtins.property
    @jsii.member(jsii_name="pathSegmentType")
    def path_segment_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pathSegmentType"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeRouteAsPaths]:
        return typing.cast(typing.Optional[ComputeRouteAsPaths], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ComputeRouteAsPaths]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa41c530125772d48411a8978b9dad6e269376c0c5374315559bd9c177cca9fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRoute.ComputeRouteConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "dest_range": "destRange",
        "name": "name",
        "network": "network",
        "description": "description",
        "id": "id",
        "next_hop_gateway": "nextHopGateway",
        "next_hop_ilb": "nextHopIlb",
        "next_hop_instance": "nextHopInstance",
        "next_hop_instance_zone": "nextHopInstanceZone",
        "next_hop_ip": "nextHopIp",
        "next_hop_vpn_tunnel": "nextHopVpnTunnel",
        "params": "params",
        "priority": "priority",
        "project": "project",
        "tags": "tags",
        "timeouts": "timeouts",
    },
)
class ComputeRouteConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        dest_range: builtins.str,
        name: builtins.str,
        network: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        next_hop_gateway: typing.Optional[builtins.str] = None,
        next_hop_ilb: typing.Optional[builtins.str] = None,
        next_hop_instance: typing.Optional[builtins.str] = None,
        next_hop_instance_zone: typing.Optional[builtins.str] = None,
        next_hop_ip: typing.Optional[builtins.str] = None,
        next_hop_vpn_tunnel: typing.Optional[builtins.str] = None,
        params: typing.Optional[typing.Union["ComputeRouteParams", typing.Dict[builtins.str, typing.Any]]] = None,
        priority: typing.Optional[jsii.Number] = None,
        project: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["ComputeRouteTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param dest_range: The destination range of outgoing packets that this route applies to. Only IPv4 is supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_route#dest_range ComputeRoute#dest_range}
        :param name: Name of the resource. Provided by the client when the resource is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_route#name ComputeRoute#name}
        :param network: The network that this route applies to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_route#network ComputeRoute#network}
        :param description: An optional description of this resource. Provide this property when you create the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_route#description ComputeRoute#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_route#id ComputeRoute#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param next_hop_gateway: URL to a gateway that should handle matching packets. Currently, you can only specify the internet gateway, using a full or partial valid URL: - 'https://www.googleapis.com/compute/v1/projects/project/global/gateways/default-internet-gateway' - 'projects/project/global/gateways/default-internet-gateway' - 'global/gateways/default-internet-gateway' - The string 'default-internet-gateway'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_route#next_hop_gateway ComputeRoute#next_hop_gateway}
        :param next_hop_ilb: The IP address or URL to a forwarding rule of type loadBalancingScheme=INTERNAL that should handle matching packets. With the GA provider you can only specify the forwarding rule as a partial or full URL. For example, the following are all valid values: - 10.128.0.56 - https://www.googleapis.com/compute/v1/projects/project/regions/region/forwardingRules/forwardingRule - regions/region/forwardingRules/forwardingRule When the beta provider, you can also specify the IP address of a forwarding rule from the same VPC or any peered VPC. Note that this can only be used when the destinationRange is a public (non-RFC 1918) IP CIDR range. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_route#next_hop_ilb ComputeRoute#next_hop_ilb}
        :param next_hop_instance: URL to an instance that should handle matching packets. You can specify this as a full or partial URL. For example: - 'https://www.googleapis.com/compute/v1/projects/project/zones/zone/instances/instance' - 'projects/project/zones/zone/instances/instance' - 'zones/zone/instances/instance' - Just the instance name, with the zone in 'next_hop_instance_zone'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_route#next_hop_instance ComputeRoute#next_hop_instance}
        :param next_hop_instance_zone: The zone of the instance specified in next_hop_instance. Omit if next_hop_instance is specified as a URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_route#next_hop_instance_zone ComputeRoute#next_hop_instance_zone}
        :param next_hop_ip: Network IP address of an instance that should handle matching packets. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_route#next_hop_ip ComputeRoute#next_hop_ip}
        :param next_hop_vpn_tunnel: URL to a VpnTunnel that should handle matching packets. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_route#next_hop_vpn_tunnel ComputeRoute#next_hop_vpn_tunnel}
        :param params: params block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_route#params ComputeRoute#params}
        :param priority: The priority of this route. Priority is used to break ties in cases where there is more than one matching route of equal prefix length. In the case of two routes with equal prefix length, the one with the lowest-numbered priority value wins. Default value is 1000. Valid range is 0 through 65535. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_route#priority ComputeRoute#priority}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_route#project ComputeRoute#project}.
        :param tags: A list of instance tags to which this route applies. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_route#tags ComputeRoute#tags}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_route#timeouts ComputeRoute#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(params, dict):
            params = ComputeRouteParams(**params)
        if isinstance(timeouts, dict):
            timeouts = ComputeRouteTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c3c57fee472ebb086ebdde73d8ada8fb0ffc8a75300049e97745bc0d046402e)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument dest_range", value=dest_range, expected_type=type_hints["dest_range"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument next_hop_gateway", value=next_hop_gateway, expected_type=type_hints["next_hop_gateway"])
            check_type(argname="argument next_hop_ilb", value=next_hop_ilb, expected_type=type_hints["next_hop_ilb"])
            check_type(argname="argument next_hop_instance", value=next_hop_instance, expected_type=type_hints["next_hop_instance"])
            check_type(argname="argument next_hop_instance_zone", value=next_hop_instance_zone, expected_type=type_hints["next_hop_instance_zone"])
            check_type(argname="argument next_hop_ip", value=next_hop_ip, expected_type=type_hints["next_hop_ip"])
            check_type(argname="argument next_hop_vpn_tunnel", value=next_hop_vpn_tunnel, expected_type=type_hints["next_hop_vpn_tunnel"])
            check_type(argname="argument params", value=params, expected_type=type_hints["params"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dest_range": dest_range,
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
        if next_hop_gateway is not None:
            self._values["next_hop_gateway"] = next_hop_gateway
        if next_hop_ilb is not None:
            self._values["next_hop_ilb"] = next_hop_ilb
        if next_hop_instance is not None:
            self._values["next_hop_instance"] = next_hop_instance
        if next_hop_instance_zone is not None:
            self._values["next_hop_instance_zone"] = next_hop_instance_zone
        if next_hop_ip is not None:
            self._values["next_hop_ip"] = next_hop_ip
        if next_hop_vpn_tunnel is not None:
            self._values["next_hop_vpn_tunnel"] = next_hop_vpn_tunnel
        if params is not None:
            self._values["params"] = params
        if priority is not None:
            self._values["priority"] = priority
        if project is not None:
            self._values["project"] = project
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
    def dest_range(self) -> builtins.str:
        '''The destination range of outgoing packets that this route applies to. Only IPv4 is supported.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_route#dest_range ComputeRoute#dest_range}
        '''
        result = self._values.get("dest_range")
        assert result is not None, "Required property 'dest_range' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the resource.

        Provided by the client when the resource is
        created. The name must be 1-63 characters long, and comply with
        RFC1035.  Specifically, the name must be 1-63 characters long and
        match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means
        the first character must be a lowercase letter, and all following
        characters must be a dash, lowercase letter, or digit, except the
        last character, which cannot be a dash.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_route#name ComputeRoute#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def network(self) -> builtins.str:
        '''The network that this route applies to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_route#network ComputeRoute#network}
        '''
        result = self._values.get("network")
        assert result is not None, "Required property 'network' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of this resource. Provide this property when you create the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_route#description ComputeRoute#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_route#id ComputeRoute#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def next_hop_gateway(self) -> typing.Optional[builtins.str]:
        '''URL to a gateway that should handle matching packets.

        Currently, you can only specify the internet gateway, using a full or
        partial valid URL:

        - 'https://www.googleapis.com/compute/v1/projects/project/global/gateways/default-internet-gateway'
        - 'projects/project/global/gateways/default-internet-gateway'
        - 'global/gateways/default-internet-gateway'
        - The string 'default-internet-gateway'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_route#next_hop_gateway ComputeRoute#next_hop_gateway}
        '''
        result = self._values.get("next_hop_gateway")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def next_hop_ilb(self) -> typing.Optional[builtins.str]:
        '''The IP address or URL to a forwarding rule of type loadBalancingScheme=INTERNAL that should handle matching packets.

        With the GA provider you can only specify the forwarding
        rule as a partial or full URL. For example, the following
        are all valid values:

        - 10.128.0.56
        - https://www.googleapis.com/compute/v1/projects/project/regions/region/forwardingRules/forwardingRule
        - regions/region/forwardingRules/forwardingRule

        When the beta provider, you can also specify the IP address
        of a forwarding rule from the same VPC or any peered VPC.

        Note that this can only be used when the destinationRange is
        a public (non-RFC 1918) IP CIDR range.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_route#next_hop_ilb ComputeRoute#next_hop_ilb}
        '''
        result = self._values.get("next_hop_ilb")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def next_hop_instance(self) -> typing.Optional[builtins.str]:
        '''URL to an instance that should handle matching packets.

        You can specify this as a full or partial URL. For example:

        - 'https://www.googleapis.com/compute/v1/projects/project/zones/zone/instances/instance'
        - 'projects/project/zones/zone/instances/instance'
        - 'zones/zone/instances/instance'
        - Just the instance name, with the zone in 'next_hop_instance_zone'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_route#next_hop_instance ComputeRoute#next_hop_instance}
        '''
        result = self._values.get("next_hop_instance")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def next_hop_instance_zone(self) -> typing.Optional[builtins.str]:
        '''The zone of the instance specified in next_hop_instance. Omit if next_hop_instance is specified as a URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_route#next_hop_instance_zone ComputeRoute#next_hop_instance_zone}
        '''
        result = self._values.get("next_hop_instance_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def next_hop_ip(self) -> typing.Optional[builtins.str]:
        '''Network IP address of an instance that should handle matching packets.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_route#next_hop_ip ComputeRoute#next_hop_ip}
        '''
        result = self._values.get("next_hop_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def next_hop_vpn_tunnel(self) -> typing.Optional[builtins.str]:
        '''URL to a VpnTunnel that should handle matching packets.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_route#next_hop_vpn_tunnel ComputeRoute#next_hop_vpn_tunnel}
        '''
        result = self._values.get("next_hop_vpn_tunnel")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def params(self) -> typing.Optional["ComputeRouteParams"]:
        '''params block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_route#params ComputeRoute#params}
        '''
        result = self._values.get("params")
        return typing.cast(typing.Optional["ComputeRouteParams"], result)

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        '''The priority of this route.

        Priority is used to break ties in cases
        where there is more than one matching route of equal prefix length.

        In the case of two routes with equal prefix length, the one with the
        lowest-numbered priority value wins.

        Default value is 1000. Valid range is 0 through 65535.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_route#priority ComputeRoute#priority}
        '''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_route#project ComputeRoute#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of instance tags to which this route applies.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_route#tags ComputeRoute#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ComputeRouteTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_route#timeouts ComputeRoute#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ComputeRouteTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRouteConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRoute.ComputeRouteParams",
    jsii_struct_bases=[],
    name_mapping={"resource_manager_tags": "resourceManagerTags"},
)
class ComputeRouteParams:
    def __init__(
        self,
        *,
        resource_manager_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param resource_manager_tags: Resource manager tags to be bound to the route. Tag keys and values have the same definition as resource manager tags. Keys must be in the format tagKeys/{tag_key_id}, and values are in the format tagValues/456. The field is ignored when empty. The field is immutable and causes resource replacement when mutated. This field is only set at create time and modifying this field after creation will trigger recreation. To apply tags to an existing resource, see the google_tags_tag_binding resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_route#resource_manager_tags ComputeRoute#resource_manager_tags}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53affe493553174220d96a2c1a90ca9a3e566f93cccfd402a025b43e4f86409d)
            check_type(argname="argument resource_manager_tags", value=resource_manager_tags, expected_type=type_hints["resource_manager_tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if resource_manager_tags is not None:
            self._values["resource_manager_tags"] = resource_manager_tags

    @builtins.property
    def resource_manager_tags(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Resource manager tags to be bound to the route.

        Tag keys and values have the
        same definition as resource manager tags. Keys must be in the format tagKeys/{tag_key_id},
        and values are in the format tagValues/456. The field is ignored when empty.
        The field is immutable and causes resource replacement when mutated. This field is only
        set at create time and modifying this field after creation will trigger recreation.
        To apply tags to an existing resource, see the google_tags_tag_binding resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_route#resource_manager_tags ComputeRoute#resource_manager_tags}
        '''
        result = self._values.get("resource_manager_tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRouteParams(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRouteParamsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRoute.ComputeRouteParamsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8bffc960225ecf18a5ca9e1f8757154720730fa2a943d978dfb6ab631264b36)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetResourceManagerTags")
    def reset_resource_manager_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceManagerTags", []))

    @builtins.property
    @jsii.member(jsii_name="resourceManagerTagsInput")
    def resource_manager_tags_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "resourceManagerTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceManagerTags")
    def resource_manager_tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "resourceManagerTags"))

    @resource_manager_tags.setter
    def resource_manager_tags(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8db4495b8b0589e932c71d2888e0444762837ccd00477953bd66d163868ff48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceManagerTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeRouteParams]:
        return typing.cast(typing.Optional[ComputeRouteParams], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ComputeRouteParams]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42e1150cffb7609f716c20d8e7ba980ecbd6b9a8a38902a98f0c42dc054640b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRoute.ComputeRouteTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class ComputeRouteTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_route#create ComputeRoute#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_route#delete ComputeRoute#delete}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe5e2cc6ca4bf3428478bb06283f3376901f1ba5448c5555b6d8cf9c50715872)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_route#create ComputeRoute#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_route#delete ComputeRoute#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRouteTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRouteTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRoute.ComputeRouteTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ff1d75c64468f8d558877570bd3c41c717966cd26719af28de622e0be088b64)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31d466185da8b3896c1d70340f84e7d7074f7cfd7e4872de3b69ee61dbdcd87c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__483b13403f4402140d7e8cd3b05da992b14949827cb431a2b71f17dd1b27d69a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRouteTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRouteTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRouteTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a581599a475a1198325034cfbbd07547bb10002e3eec7bb73e034fd46f984718)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRoute.ComputeRouteWarnings",
    jsii_struct_bases=[],
    name_mapping={},
)
class ComputeRouteWarnings:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRouteWarnings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRoute.ComputeRouteWarningsData",
    jsii_struct_bases=[],
    name_mapping={},
)
class ComputeRouteWarningsData:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRouteWarningsData(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRouteWarningsDataList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRoute.ComputeRouteWarningsDataList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8102b422587ed1dea7ac9cf0873f35eb69404f0305bf73c889547a627936e35f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ComputeRouteWarningsDataOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d76caf5ddbf4ca1a3ed0672026a9f1f61e035c0028fd6e49799af2b4a96a840c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeRouteWarningsDataOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f51a512d82f4c282e97e86c9c096516e11b8f7339f6a960502e1b78815982c73)
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
            type_hints = typing.get_type_hints(_typecheckingstub__19cba390851a9d14b053cd31e81fa33ac4b30d560d217fc63d829410dc3d3a31)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c75c251ac27a65f0e4d56feeca8a6ed11cdfd6619b1ff2fd6a24144e6cb089e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ComputeRouteWarningsDataOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRoute.ComputeRouteWarningsDataOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e5ba9dce3836f0f8d9e770a0bd27e91053d54f502c780bbdd4edd0a23a6a7241)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeRouteWarningsData]:
        return typing.cast(typing.Optional[ComputeRouteWarningsData], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ComputeRouteWarningsData]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2e0775f0105283eda8ee1bb4dc01337a8bdc5a9dbb80b1b8f079a13d8cbce1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRouteWarningsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRoute.ComputeRouteWarningsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc4a054e87bcad915b9a70b9580348812dcdca6536ba2dd37de178ee49713d1c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ComputeRouteWarningsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69541d0a94d90b6c2460e4c893f9fcb0e61e15c399428bbab64b09f5be579ace)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeRouteWarningsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09463e7c546e0a3b43f02a7f2738ae810b4d4d70423b950935a7346be3f4ba75)
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
            type_hints = typing.get_type_hints(_typecheckingstub__67cb9faf778035199a6dbda16c43a1fc31a8506156a89fa0a5b7f696b2255733)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ba509df036b3c94a9af2057edb670c8ecd067e0ea4bfc3e6535dd3012a23a841)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ComputeRouteWarningsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRoute.ComputeRouteWarningsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc8c52b1c4a3240c886884fa1fd34333d86b51d60ccf42ca9820dcff210abd01)
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
    def data(self) -> ComputeRouteWarningsDataList:
        return typing.cast(ComputeRouteWarningsDataList, jsii.get(self, "data"))

    @builtins.property
    @jsii.member(jsii_name="message")
    def message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "message"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeRouteWarnings]:
        return typing.cast(typing.Optional[ComputeRouteWarnings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ComputeRouteWarnings]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8e355580b8d1bad3d00ddef49a4f9b8ae3803d021a771d4bfa048b74eab2ddb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ComputeRoute",
    "ComputeRouteAsPaths",
    "ComputeRouteAsPathsList",
    "ComputeRouteAsPathsOutputReference",
    "ComputeRouteConfig",
    "ComputeRouteParams",
    "ComputeRouteParamsOutputReference",
    "ComputeRouteTimeouts",
    "ComputeRouteTimeoutsOutputReference",
    "ComputeRouteWarnings",
    "ComputeRouteWarningsData",
    "ComputeRouteWarningsDataList",
    "ComputeRouteWarningsDataOutputReference",
    "ComputeRouteWarningsList",
    "ComputeRouteWarningsOutputReference",
]

publication.publish()

def _typecheckingstub__d70ce4466236ea531b210d9fbae9bdf5ca6ba4fa583156f91300a068309cc35f(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    dest_range: builtins.str,
    name: builtins.str,
    network: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    next_hop_gateway: typing.Optional[builtins.str] = None,
    next_hop_ilb: typing.Optional[builtins.str] = None,
    next_hop_instance: typing.Optional[builtins.str] = None,
    next_hop_instance_zone: typing.Optional[builtins.str] = None,
    next_hop_ip: typing.Optional[builtins.str] = None,
    next_hop_vpn_tunnel: typing.Optional[builtins.str] = None,
    params: typing.Optional[typing.Union[ComputeRouteParams, typing.Dict[builtins.str, typing.Any]]] = None,
    priority: typing.Optional[jsii.Number] = None,
    project: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[ComputeRouteTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__1b1abb39e0723b976b0d0bb5023ffec66a1b1f663cfffb6b3fdd863bfce4943e(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6837fe40842871b443fb87059556c1d36aeed924cab8b8595d67c2188aa9690(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d43a1a9f83a1921cf2105ed77c5e63d628c962e3dddf5052fe32941915673603(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3488ecafafecb58ba668d6f5aa6f525a7e8be2c5bb171c1b0af7f5dd9270112(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a877cdd5140ccbf8b6c7fb755c19daf5b871ef8aae4376da05ed4b75c74b34e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cf9f4fe83fff01ca92b637ada2e38e80796f340c331735abaedfe75679c608f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9873e1e7d67c4f5ee9b8d2a4eef17cd97d872a0bf4cf4c21267b6801d8005382(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c632ac62c877e604d987512d9d5db3d73543980835d41313963b5f522c335fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0abbd00ac28a115cbc3a2f4496e081d15c260e889e7bd5b1c229bb3c8bda4b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ca6d24e9c55d9065aa8da982bd93d095789bae5c2bdc92429bbba0e10802c59(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c562766a9b94881813c85884dff24d308497c9d6c1153035018405c6741d0a6b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88728484394e4f7e9646b636a0dc472a46cf23def2ab8de3f8de8e9bf85fff41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__749ddcf793e6280e42c47be5cf2f54c1f4ba2f02ff3bef0928a8761a99377a49(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c2a7eb2590353373d54d362f2cf0817057eb1a10492c2f2e2ca784dc3cb1c62(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d55639ff75f806efb0ef6876428f5978b471b437440760b94152da7b5cbfe715(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4109404b0219033a571c712d4eaaf44e25fa1559cacaee9d93f8326ffa4519e5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9eee5101902d7c32f57afaa5277a09339153b45e64267d601401ae5307eebcf1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8936ceb6621cf4ac58aed991ac161af34bbe944dbef32b659072d80928230028(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae024fbf059b7a6f6849fcc065b986c33588ef527caf9009afc4bb5ea857772f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30046e42867b30e31482726ffb524fa2e3e006cf5f4464d08ede4759c3cebafc(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5d2648c81789a243ec766182d093036ddaddb03aa144b7c7375daaac23053f8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa41c530125772d48411a8978b9dad6e269376c0c5374315559bd9c177cca9fc(
    value: typing.Optional[ComputeRouteAsPaths],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c3c57fee472ebb086ebdde73d8ada8fb0ffc8a75300049e97745bc0d046402e(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    dest_range: builtins.str,
    name: builtins.str,
    network: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    next_hop_gateway: typing.Optional[builtins.str] = None,
    next_hop_ilb: typing.Optional[builtins.str] = None,
    next_hop_instance: typing.Optional[builtins.str] = None,
    next_hop_instance_zone: typing.Optional[builtins.str] = None,
    next_hop_ip: typing.Optional[builtins.str] = None,
    next_hop_vpn_tunnel: typing.Optional[builtins.str] = None,
    params: typing.Optional[typing.Union[ComputeRouteParams, typing.Dict[builtins.str, typing.Any]]] = None,
    priority: typing.Optional[jsii.Number] = None,
    project: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[ComputeRouteTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53affe493553174220d96a2c1a90ca9a3e566f93cccfd402a025b43e4f86409d(
    *,
    resource_manager_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8bffc960225ecf18a5ca9e1f8757154720730fa2a943d978dfb6ab631264b36(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8db4495b8b0589e932c71d2888e0444762837ccd00477953bd66d163868ff48(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42e1150cffb7609f716c20d8e7ba980ecbd6b9a8a38902a98f0c42dc054640b8(
    value: typing.Optional[ComputeRouteParams],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe5e2cc6ca4bf3428478bb06283f3376901f1ba5448c5555b6d8cf9c50715872(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ff1d75c64468f8d558877570bd3c41c717966cd26719af28de622e0be088b64(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31d466185da8b3896c1d70340f84e7d7074f7cfd7e4872de3b69ee61dbdcd87c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__483b13403f4402140d7e8cd3b05da992b14949827cb431a2b71f17dd1b27d69a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a581599a475a1198325034cfbbd07547bb10002e3eec7bb73e034fd46f984718(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRouteTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8102b422587ed1dea7ac9cf0873f35eb69404f0305bf73c889547a627936e35f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d76caf5ddbf4ca1a3ed0672026a9f1f61e035c0028fd6e49799af2b4a96a840c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f51a512d82f4c282e97e86c9c096516e11b8f7339f6a960502e1b78815982c73(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19cba390851a9d14b053cd31e81fa33ac4b30d560d217fc63d829410dc3d3a31(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c75c251ac27a65f0e4d56feeca8a6ed11cdfd6619b1ff2fd6a24144e6cb089e4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5ba9dce3836f0f8d9e770a0bd27e91053d54f502c780bbdd4edd0a23a6a7241(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2e0775f0105283eda8ee1bb4dc01337a8bdc5a9dbb80b1b8f079a13d8cbce1a(
    value: typing.Optional[ComputeRouteWarningsData],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc4a054e87bcad915b9a70b9580348812dcdca6536ba2dd37de178ee49713d1c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69541d0a94d90b6c2460e4c893f9fcb0e61e15c399428bbab64b09f5be579ace(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09463e7c546e0a3b43f02a7f2738ae810b4d4d70423b950935a7346be3f4ba75(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67cb9faf778035199a6dbda16c43a1fc31a8506156a89fa0a5b7f696b2255733(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba509df036b3c94a9af2057edb670c8ecd067e0ea4bfc3e6535dd3012a23a841(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc8c52b1c4a3240c886884fa1fd34333d86b51d60ccf42ca9820dcff210abd01(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8e355580b8d1bad3d00ddef49a4f9b8ae3803d021a771d4bfa048b74eab2ddb(
    value: typing.Optional[ComputeRouteWarnings],
) -> None:
    """Type checking stubs"""
    pass
