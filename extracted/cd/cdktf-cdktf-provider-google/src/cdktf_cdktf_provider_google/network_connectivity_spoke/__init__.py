r'''
# `google_network_connectivity_spoke`

Refer to the Terraform Registry for docs: [`google_network_connectivity_spoke`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke).
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


class NetworkConnectivitySpoke(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkConnectivitySpoke.NetworkConnectivitySpoke",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke google_network_connectivity_spoke}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        hub: builtins.str,
        location: builtins.str,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        group: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        linked_interconnect_attachments: typing.Optional[typing.Union["NetworkConnectivitySpokeLinkedInterconnectAttachments", typing.Dict[builtins.str, typing.Any]]] = None,
        linked_producer_vpc_network: typing.Optional[typing.Union["NetworkConnectivitySpokeLinkedProducerVpcNetwork", typing.Dict[builtins.str, typing.Any]]] = None,
        linked_router_appliance_instances: typing.Optional[typing.Union["NetworkConnectivitySpokeLinkedRouterApplianceInstances", typing.Dict[builtins.str, typing.Any]]] = None,
        linked_vpc_network: typing.Optional[typing.Union["NetworkConnectivitySpokeLinkedVpcNetwork", typing.Dict[builtins.str, typing.Any]]] = None,
        linked_vpn_tunnels: typing.Optional[typing.Union["NetworkConnectivitySpokeLinkedVpnTunnels", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["NetworkConnectivitySpokeTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke google_network_connectivity_spoke} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param hub: Immutable. The URI of the hub that this spoke is attached to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#hub NetworkConnectivitySpoke#hub}
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#location NetworkConnectivitySpoke#location}
        :param name: Immutable. The name of the spoke. Spoke names must be unique. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#name NetworkConnectivitySpoke#name}
        :param description: An optional description of the spoke. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#description NetworkConnectivitySpoke#description}
        :param group: The name of the group that this spoke is associated with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#group NetworkConnectivitySpoke#group}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#id NetworkConnectivitySpoke#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Optional labels in key:value format. For more information about labels, see `Requirements for labels <https://cloud.google.com/resource-manager/docs/creating-managing-labels#requirements>`_. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#labels NetworkConnectivitySpoke#labels}
        :param linked_interconnect_attachments: linked_interconnect_attachments block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#linked_interconnect_attachments NetworkConnectivitySpoke#linked_interconnect_attachments}
        :param linked_producer_vpc_network: linked_producer_vpc_network block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#linked_producer_vpc_network NetworkConnectivitySpoke#linked_producer_vpc_network}
        :param linked_router_appliance_instances: linked_router_appliance_instances block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#linked_router_appliance_instances NetworkConnectivitySpoke#linked_router_appliance_instances}
        :param linked_vpc_network: linked_vpc_network block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#linked_vpc_network NetworkConnectivitySpoke#linked_vpc_network}
        :param linked_vpn_tunnels: linked_vpn_tunnels block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#linked_vpn_tunnels NetworkConnectivitySpoke#linked_vpn_tunnels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#project NetworkConnectivitySpoke#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#timeouts NetworkConnectivitySpoke#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc96b7abfa74c4d2bf6743ee906865f83afb04ac79c7f09610526aed7a234e7d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = NetworkConnectivitySpokeConfig(
            hub=hub,
            location=location,
            name=name,
            description=description,
            group=group,
            id=id,
            labels=labels,
            linked_interconnect_attachments=linked_interconnect_attachments,
            linked_producer_vpc_network=linked_producer_vpc_network,
            linked_router_appliance_instances=linked_router_appliance_instances,
            linked_vpc_network=linked_vpc_network,
            linked_vpn_tunnels=linked_vpn_tunnels,
            project=project,
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
        '''Generates CDKTF code for importing a NetworkConnectivitySpoke resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the NetworkConnectivitySpoke to import.
        :param import_from_id: The id of the existing NetworkConnectivitySpoke that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the NetworkConnectivitySpoke to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e56dc8ea8103c57c426edf05be5efa293ac83feaf5b3b9bb1a46bf843eacbdd0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putLinkedInterconnectAttachments")
    def put_linked_interconnect_attachments(
        self,
        *,
        site_to_site_data_transfer: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        uris: typing.Sequence[builtins.str],
        include_import_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param site_to_site_data_transfer: A value that controls whether site-to-site data transfer is enabled for these resources. Note that data transfer is available only in supported locations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#site_to_site_data_transfer NetworkConnectivitySpoke#site_to_site_data_transfer}
        :param uris: The URIs of linked interconnect attachment resources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#uris NetworkConnectivitySpoke#uris}
        :param include_import_ranges: IP ranges allowed to be included during import from hub (does not control transit connectivity). The only allowed value for now is "ALL_IPV4_RANGES". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#include_import_ranges NetworkConnectivitySpoke#include_import_ranges}
        '''
        value = NetworkConnectivitySpokeLinkedInterconnectAttachments(
            site_to_site_data_transfer=site_to_site_data_transfer,
            uris=uris,
            include_import_ranges=include_import_ranges,
        )

        return typing.cast(None, jsii.invoke(self, "putLinkedInterconnectAttachments", [value]))

    @jsii.member(jsii_name="putLinkedProducerVpcNetwork")
    def put_linked_producer_vpc_network(
        self,
        *,
        network: builtins.str,
        peering: builtins.str,
        exclude_export_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        include_export_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param network: The URI of the Service Consumer VPC that the Producer VPC is peered with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#network NetworkConnectivitySpoke#network}
        :param peering: The name of the VPC peering between the Service Consumer VPC and the Producer VPC (defined in the Tenant project) which is added to the NCC hub. This peering must be in ACTIVE state. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#peering NetworkConnectivitySpoke#peering}
        :param exclude_export_ranges: IP ranges encompassing the subnets to be excluded from peering. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#exclude_export_ranges NetworkConnectivitySpoke#exclude_export_ranges}
        :param include_export_ranges: IP ranges allowed to be included from peering. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#include_export_ranges NetworkConnectivitySpoke#include_export_ranges}
        '''
        value = NetworkConnectivitySpokeLinkedProducerVpcNetwork(
            network=network,
            peering=peering,
            exclude_export_ranges=exclude_export_ranges,
            include_export_ranges=include_export_ranges,
        )

        return typing.cast(None, jsii.invoke(self, "putLinkedProducerVpcNetwork", [value]))

    @jsii.member(jsii_name="putLinkedRouterApplianceInstances")
    def put_linked_router_appliance_instances(
        self,
        *,
        instances: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkConnectivitySpokeLinkedRouterApplianceInstancesInstances", typing.Dict[builtins.str, typing.Any]]]],
        site_to_site_data_transfer: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        include_import_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param instances: instances block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#instances NetworkConnectivitySpoke#instances}
        :param site_to_site_data_transfer: A value that controls whether site-to-site data transfer is enabled for these resources. Note that data transfer is available only in supported locations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#site_to_site_data_transfer NetworkConnectivitySpoke#site_to_site_data_transfer}
        :param include_import_ranges: IP ranges allowed to be included during import from hub (does not control transit connectivity). The only allowed value for now is "ALL_IPV4_RANGES". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#include_import_ranges NetworkConnectivitySpoke#include_import_ranges}
        '''
        value = NetworkConnectivitySpokeLinkedRouterApplianceInstances(
            instances=instances,
            site_to_site_data_transfer=site_to_site_data_transfer,
            include_import_ranges=include_import_ranges,
        )

        return typing.cast(None, jsii.invoke(self, "putLinkedRouterApplianceInstances", [value]))

    @jsii.member(jsii_name="putLinkedVpcNetwork")
    def put_linked_vpc_network(
        self,
        *,
        uri: builtins.str,
        exclude_export_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        include_export_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param uri: The URI of the VPC network resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#uri NetworkConnectivitySpoke#uri}
        :param exclude_export_ranges: IP ranges encompassing the subnets to be excluded from peering. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#exclude_export_ranges NetworkConnectivitySpoke#exclude_export_ranges}
        :param include_export_ranges: IP ranges allowed to be included from peering. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#include_export_ranges NetworkConnectivitySpoke#include_export_ranges}
        '''
        value = NetworkConnectivitySpokeLinkedVpcNetwork(
            uri=uri,
            exclude_export_ranges=exclude_export_ranges,
            include_export_ranges=include_export_ranges,
        )

        return typing.cast(None, jsii.invoke(self, "putLinkedVpcNetwork", [value]))

    @jsii.member(jsii_name="putLinkedVpnTunnels")
    def put_linked_vpn_tunnels(
        self,
        *,
        site_to_site_data_transfer: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        uris: typing.Sequence[builtins.str],
        include_import_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param site_to_site_data_transfer: A value that controls whether site-to-site data transfer is enabled for these resources. Note that data transfer is available only in supported locations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#site_to_site_data_transfer NetworkConnectivitySpoke#site_to_site_data_transfer}
        :param uris: The URIs of linked VPN tunnel resources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#uris NetworkConnectivitySpoke#uris}
        :param include_import_ranges: IP ranges allowed to be included during import from hub (does not control transit connectivity). The only allowed value for now is "ALL_IPV4_RANGES". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#include_import_ranges NetworkConnectivitySpoke#include_import_ranges}
        '''
        value = NetworkConnectivitySpokeLinkedVpnTunnels(
            site_to_site_data_transfer=site_to_site_data_transfer,
            uris=uris,
            include_import_ranges=include_import_ranges,
        )

        return typing.cast(None, jsii.invoke(self, "putLinkedVpnTunnels", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#create NetworkConnectivitySpoke#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#delete NetworkConnectivitySpoke#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#update NetworkConnectivitySpoke#update}.
        '''
        value = NetworkConnectivitySpokeTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetGroup")
    def reset_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroup", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetLinkedInterconnectAttachments")
    def reset_linked_interconnect_attachments(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLinkedInterconnectAttachments", []))

    @jsii.member(jsii_name="resetLinkedProducerVpcNetwork")
    def reset_linked_producer_vpc_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLinkedProducerVpcNetwork", []))

    @jsii.member(jsii_name="resetLinkedRouterApplianceInstances")
    def reset_linked_router_appliance_instances(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLinkedRouterApplianceInstances", []))

    @jsii.member(jsii_name="resetLinkedVpcNetwork")
    def reset_linked_vpc_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLinkedVpcNetwork", []))

    @jsii.member(jsii_name="resetLinkedVpnTunnels")
    def reset_linked_vpn_tunnels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLinkedVpnTunnels", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

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
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="linkedInterconnectAttachments")
    def linked_interconnect_attachments(
        self,
    ) -> "NetworkConnectivitySpokeLinkedInterconnectAttachmentsOutputReference":
        return typing.cast("NetworkConnectivitySpokeLinkedInterconnectAttachmentsOutputReference", jsii.get(self, "linkedInterconnectAttachments"))

    @builtins.property
    @jsii.member(jsii_name="linkedProducerVpcNetwork")
    def linked_producer_vpc_network(
        self,
    ) -> "NetworkConnectivitySpokeLinkedProducerVpcNetworkOutputReference":
        return typing.cast("NetworkConnectivitySpokeLinkedProducerVpcNetworkOutputReference", jsii.get(self, "linkedProducerVpcNetwork"))

    @builtins.property
    @jsii.member(jsii_name="linkedRouterApplianceInstances")
    def linked_router_appliance_instances(
        self,
    ) -> "NetworkConnectivitySpokeLinkedRouterApplianceInstancesOutputReference":
        return typing.cast("NetworkConnectivitySpokeLinkedRouterApplianceInstancesOutputReference", jsii.get(self, "linkedRouterApplianceInstances"))

    @builtins.property
    @jsii.member(jsii_name="linkedVpcNetwork")
    def linked_vpc_network(
        self,
    ) -> "NetworkConnectivitySpokeLinkedVpcNetworkOutputReference":
        return typing.cast("NetworkConnectivitySpokeLinkedVpcNetworkOutputReference", jsii.get(self, "linkedVpcNetwork"))

    @builtins.property
    @jsii.member(jsii_name="linkedVpnTunnels")
    def linked_vpn_tunnels(
        self,
    ) -> "NetworkConnectivitySpokeLinkedVpnTunnelsOutputReference":
        return typing.cast("NetworkConnectivitySpokeLinkedVpnTunnelsOutputReference", jsii.get(self, "linkedVpnTunnels"))

    @builtins.property
    @jsii.member(jsii_name="reasons")
    def reasons(self) -> "NetworkConnectivitySpokeReasonsList":
        return typing.cast("NetworkConnectivitySpokeReasonsList", jsii.get(self, "reasons"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "NetworkConnectivitySpokeTimeoutsOutputReference":
        return typing.cast("NetworkConnectivitySpokeTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="uniqueId")
    def unique_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uniqueId"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="groupInput")
    def group_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "groupInput"))

    @builtins.property
    @jsii.member(jsii_name="hubInput")
    def hub_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hubInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="linkedInterconnectAttachmentsInput")
    def linked_interconnect_attachments_input(
        self,
    ) -> typing.Optional["NetworkConnectivitySpokeLinkedInterconnectAttachments"]:
        return typing.cast(typing.Optional["NetworkConnectivitySpokeLinkedInterconnectAttachments"], jsii.get(self, "linkedInterconnectAttachmentsInput"))

    @builtins.property
    @jsii.member(jsii_name="linkedProducerVpcNetworkInput")
    def linked_producer_vpc_network_input(
        self,
    ) -> typing.Optional["NetworkConnectivitySpokeLinkedProducerVpcNetwork"]:
        return typing.cast(typing.Optional["NetworkConnectivitySpokeLinkedProducerVpcNetwork"], jsii.get(self, "linkedProducerVpcNetworkInput"))

    @builtins.property
    @jsii.member(jsii_name="linkedRouterApplianceInstancesInput")
    def linked_router_appliance_instances_input(
        self,
    ) -> typing.Optional["NetworkConnectivitySpokeLinkedRouterApplianceInstances"]:
        return typing.cast(typing.Optional["NetworkConnectivitySpokeLinkedRouterApplianceInstances"], jsii.get(self, "linkedRouterApplianceInstancesInput"))

    @builtins.property
    @jsii.member(jsii_name="linkedVpcNetworkInput")
    def linked_vpc_network_input(
        self,
    ) -> typing.Optional["NetworkConnectivitySpokeLinkedVpcNetwork"]:
        return typing.cast(typing.Optional["NetworkConnectivitySpokeLinkedVpcNetwork"], jsii.get(self, "linkedVpcNetworkInput"))

    @builtins.property
    @jsii.member(jsii_name="linkedVpnTunnelsInput")
    def linked_vpn_tunnels_input(
        self,
    ) -> typing.Optional["NetworkConnectivitySpokeLinkedVpnTunnels"]:
        return typing.cast(typing.Optional["NetworkConnectivitySpokeLinkedVpnTunnels"], jsii.get(self, "linkedVpnTunnelsInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "NetworkConnectivitySpokeTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "NetworkConnectivitySpokeTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55c4a8c8db5163262cc9638e3b1d2cd6dfa4eb126e098f17609e524438b120e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="group")
    def group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "group"))

    @group.setter
    def group(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b410faa8e5b93a59d6d1909e1145038abc3614e4c386009701f1189087d0d8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "group", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hub")
    def hub(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hub"))

    @hub.setter
    def hub(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f34005a672d0e7ef49937dc1190732151a15e964dd58ae54f768f1bb836d0ebe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hub", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9a7697b03fdc161fb3c6bb99421186a6ce1a2f96f7794c3c657bfe954ebac79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d46639bf04ec13fc76ecb42dbdb6fd7a158485e07369dbdafd6d3880f3f36e37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25812cc2d34c49536982206b65ceb554ecccbbe9bbd0aeffa3f9204fbaeac47c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8ccebf2480b171eb9e979f52157670d32ae95d58775d721d33d46d5c7d3aab5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e381a433570885220448327a2126f6d4a47432ca9006c02e5af4b2dbe41188f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkConnectivitySpoke.NetworkConnectivitySpokeConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "hub": "hub",
        "location": "location",
        "name": "name",
        "description": "description",
        "group": "group",
        "id": "id",
        "labels": "labels",
        "linked_interconnect_attachments": "linkedInterconnectAttachments",
        "linked_producer_vpc_network": "linkedProducerVpcNetwork",
        "linked_router_appliance_instances": "linkedRouterApplianceInstances",
        "linked_vpc_network": "linkedVpcNetwork",
        "linked_vpn_tunnels": "linkedVpnTunnels",
        "project": "project",
        "timeouts": "timeouts",
    },
)
class NetworkConnectivitySpokeConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        hub: builtins.str,
        location: builtins.str,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        group: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        linked_interconnect_attachments: typing.Optional[typing.Union["NetworkConnectivitySpokeLinkedInterconnectAttachments", typing.Dict[builtins.str, typing.Any]]] = None,
        linked_producer_vpc_network: typing.Optional[typing.Union["NetworkConnectivitySpokeLinkedProducerVpcNetwork", typing.Dict[builtins.str, typing.Any]]] = None,
        linked_router_appliance_instances: typing.Optional[typing.Union["NetworkConnectivitySpokeLinkedRouterApplianceInstances", typing.Dict[builtins.str, typing.Any]]] = None,
        linked_vpc_network: typing.Optional[typing.Union["NetworkConnectivitySpokeLinkedVpcNetwork", typing.Dict[builtins.str, typing.Any]]] = None,
        linked_vpn_tunnels: typing.Optional[typing.Union["NetworkConnectivitySpokeLinkedVpnTunnels", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["NetworkConnectivitySpokeTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param hub: Immutable. The URI of the hub that this spoke is attached to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#hub NetworkConnectivitySpoke#hub}
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#location NetworkConnectivitySpoke#location}
        :param name: Immutable. The name of the spoke. Spoke names must be unique. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#name NetworkConnectivitySpoke#name}
        :param description: An optional description of the spoke. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#description NetworkConnectivitySpoke#description}
        :param group: The name of the group that this spoke is associated with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#group NetworkConnectivitySpoke#group}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#id NetworkConnectivitySpoke#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Optional labels in key:value format. For more information about labels, see `Requirements for labels <https://cloud.google.com/resource-manager/docs/creating-managing-labels#requirements>`_. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#labels NetworkConnectivitySpoke#labels}
        :param linked_interconnect_attachments: linked_interconnect_attachments block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#linked_interconnect_attachments NetworkConnectivitySpoke#linked_interconnect_attachments}
        :param linked_producer_vpc_network: linked_producer_vpc_network block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#linked_producer_vpc_network NetworkConnectivitySpoke#linked_producer_vpc_network}
        :param linked_router_appliance_instances: linked_router_appliance_instances block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#linked_router_appliance_instances NetworkConnectivitySpoke#linked_router_appliance_instances}
        :param linked_vpc_network: linked_vpc_network block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#linked_vpc_network NetworkConnectivitySpoke#linked_vpc_network}
        :param linked_vpn_tunnels: linked_vpn_tunnels block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#linked_vpn_tunnels NetworkConnectivitySpoke#linked_vpn_tunnels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#project NetworkConnectivitySpoke#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#timeouts NetworkConnectivitySpoke#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(linked_interconnect_attachments, dict):
            linked_interconnect_attachments = NetworkConnectivitySpokeLinkedInterconnectAttachments(**linked_interconnect_attachments)
        if isinstance(linked_producer_vpc_network, dict):
            linked_producer_vpc_network = NetworkConnectivitySpokeLinkedProducerVpcNetwork(**linked_producer_vpc_network)
        if isinstance(linked_router_appliance_instances, dict):
            linked_router_appliance_instances = NetworkConnectivitySpokeLinkedRouterApplianceInstances(**linked_router_appliance_instances)
        if isinstance(linked_vpc_network, dict):
            linked_vpc_network = NetworkConnectivitySpokeLinkedVpcNetwork(**linked_vpc_network)
        if isinstance(linked_vpn_tunnels, dict):
            linked_vpn_tunnels = NetworkConnectivitySpokeLinkedVpnTunnels(**linked_vpn_tunnels)
        if isinstance(timeouts, dict):
            timeouts = NetworkConnectivitySpokeTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93134a2b405500b5500e47a1c7f44dd201f4b3b1e7fb8d27b71529ba8aaa9048)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument hub", value=hub, expected_type=type_hints["hub"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument group", value=group, expected_type=type_hints["group"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument linked_interconnect_attachments", value=linked_interconnect_attachments, expected_type=type_hints["linked_interconnect_attachments"])
            check_type(argname="argument linked_producer_vpc_network", value=linked_producer_vpc_network, expected_type=type_hints["linked_producer_vpc_network"])
            check_type(argname="argument linked_router_appliance_instances", value=linked_router_appliance_instances, expected_type=type_hints["linked_router_appliance_instances"])
            check_type(argname="argument linked_vpc_network", value=linked_vpc_network, expected_type=type_hints["linked_vpc_network"])
            check_type(argname="argument linked_vpn_tunnels", value=linked_vpn_tunnels, expected_type=type_hints["linked_vpn_tunnels"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "hub": hub,
            "location": location,
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
        if description is not None:
            self._values["description"] = description
        if group is not None:
            self._values["group"] = group
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if linked_interconnect_attachments is not None:
            self._values["linked_interconnect_attachments"] = linked_interconnect_attachments
        if linked_producer_vpc_network is not None:
            self._values["linked_producer_vpc_network"] = linked_producer_vpc_network
        if linked_router_appliance_instances is not None:
            self._values["linked_router_appliance_instances"] = linked_router_appliance_instances
        if linked_vpc_network is not None:
            self._values["linked_vpc_network"] = linked_vpc_network
        if linked_vpn_tunnels is not None:
            self._values["linked_vpn_tunnels"] = linked_vpn_tunnels
        if project is not None:
            self._values["project"] = project
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
    def hub(self) -> builtins.str:
        '''Immutable. The URI of the hub that this spoke is attached to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#hub NetworkConnectivitySpoke#hub}
        '''
        result = self._values.get("hub")
        assert result is not None, "Required property 'hub' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location for the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#location NetworkConnectivitySpoke#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Immutable. The name of the spoke. Spoke names must be unique.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#name NetworkConnectivitySpoke#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of the spoke.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#description NetworkConnectivitySpoke#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def group(self) -> typing.Optional[builtins.str]:
        '''The name of the group that this spoke is associated with.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#group NetworkConnectivitySpoke#group}
        '''
        result = self._values.get("group")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#id NetworkConnectivitySpoke#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional labels in key:value format. For more information about labels, see `Requirements for labels <https://cloud.google.com/resource-manager/docs/creating-managing-labels#requirements>`_.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#labels NetworkConnectivitySpoke#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def linked_interconnect_attachments(
        self,
    ) -> typing.Optional["NetworkConnectivitySpokeLinkedInterconnectAttachments"]:
        '''linked_interconnect_attachments block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#linked_interconnect_attachments NetworkConnectivitySpoke#linked_interconnect_attachments}
        '''
        result = self._values.get("linked_interconnect_attachments")
        return typing.cast(typing.Optional["NetworkConnectivitySpokeLinkedInterconnectAttachments"], result)

    @builtins.property
    def linked_producer_vpc_network(
        self,
    ) -> typing.Optional["NetworkConnectivitySpokeLinkedProducerVpcNetwork"]:
        '''linked_producer_vpc_network block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#linked_producer_vpc_network NetworkConnectivitySpoke#linked_producer_vpc_network}
        '''
        result = self._values.get("linked_producer_vpc_network")
        return typing.cast(typing.Optional["NetworkConnectivitySpokeLinkedProducerVpcNetwork"], result)

    @builtins.property
    def linked_router_appliance_instances(
        self,
    ) -> typing.Optional["NetworkConnectivitySpokeLinkedRouterApplianceInstances"]:
        '''linked_router_appliance_instances block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#linked_router_appliance_instances NetworkConnectivitySpoke#linked_router_appliance_instances}
        '''
        result = self._values.get("linked_router_appliance_instances")
        return typing.cast(typing.Optional["NetworkConnectivitySpokeLinkedRouterApplianceInstances"], result)

    @builtins.property
    def linked_vpc_network(
        self,
    ) -> typing.Optional["NetworkConnectivitySpokeLinkedVpcNetwork"]:
        '''linked_vpc_network block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#linked_vpc_network NetworkConnectivitySpoke#linked_vpc_network}
        '''
        result = self._values.get("linked_vpc_network")
        return typing.cast(typing.Optional["NetworkConnectivitySpokeLinkedVpcNetwork"], result)

    @builtins.property
    def linked_vpn_tunnels(
        self,
    ) -> typing.Optional["NetworkConnectivitySpokeLinkedVpnTunnels"]:
        '''linked_vpn_tunnels block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#linked_vpn_tunnels NetworkConnectivitySpoke#linked_vpn_tunnels}
        '''
        result = self._values.get("linked_vpn_tunnels")
        return typing.cast(typing.Optional["NetworkConnectivitySpokeLinkedVpnTunnels"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#project NetworkConnectivitySpoke#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["NetworkConnectivitySpokeTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#timeouts NetworkConnectivitySpoke#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["NetworkConnectivitySpokeTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkConnectivitySpokeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkConnectivitySpoke.NetworkConnectivitySpokeLinkedInterconnectAttachments",
    jsii_struct_bases=[],
    name_mapping={
        "site_to_site_data_transfer": "siteToSiteDataTransfer",
        "uris": "uris",
        "include_import_ranges": "includeImportRanges",
    },
)
class NetworkConnectivitySpokeLinkedInterconnectAttachments:
    def __init__(
        self,
        *,
        site_to_site_data_transfer: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        uris: typing.Sequence[builtins.str],
        include_import_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param site_to_site_data_transfer: A value that controls whether site-to-site data transfer is enabled for these resources. Note that data transfer is available only in supported locations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#site_to_site_data_transfer NetworkConnectivitySpoke#site_to_site_data_transfer}
        :param uris: The URIs of linked interconnect attachment resources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#uris NetworkConnectivitySpoke#uris}
        :param include_import_ranges: IP ranges allowed to be included during import from hub (does not control transit connectivity). The only allowed value for now is "ALL_IPV4_RANGES". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#include_import_ranges NetworkConnectivitySpoke#include_import_ranges}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__128f78c240308f3898f4dabc5cad80c5c6b285c76989654bd5c256c31558141c)
            check_type(argname="argument site_to_site_data_transfer", value=site_to_site_data_transfer, expected_type=type_hints["site_to_site_data_transfer"])
            check_type(argname="argument uris", value=uris, expected_type=type_hints["uris"])
            check_type(argname="argument include_import_ranges", value=include_import_ranges, expected_type=type_hints["include_import_ranges"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "site_to_site_data_transfer": site_to_site_data_transfer,
            "uris": uris,
        }
        if include_import_ranges is not None:
            self._values["include_import_ranges"] = include_import_ranges

    @builtins.property
    def site_to_site_data_transfer(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''A value that controls whether site-to-site data transfer is enabled for these resources.

        Note that data transfer is available only in supported locations.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#site_to_site_data_transfer NetworkConnectivitySpoke#site_to_site_data_transfer}
        '''
        result = self._values.get("site_to_site_data_transfer")
        assert result is not None, "Required property 'site_to_site_data_transfer' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def uris(self) -> typing.List[builtins.str]:
        '''The URIs of linked interconnect attachment resources.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#uris NetworkConnectivitySpoke#uris}
        '''
        result = self._values.get("uris")
        assert result is not None, "Required property 'uris' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def include_import_ranges(self) -> typing.Optional[typing.List[builtins.str]]:
        '''IP ranges allowed to be included during import from hub (does not control transit connectivity).

        The only allowed value for now is "ALL_IPV4_RANGES".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#include_import_ranges NetworkConnectivitySpoke#include_import_ranges}
        '''
        result = self._values.get("include_import_ranges")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkConnectivitySpokeLinkedInterconnectAttachments(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkConnectivitySpokeLinkedInterconnectAttachmentsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkConnectivitySpoke.NetworkConnectivitySpokeLinkedInterconnectAttachmentsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__908440db75c0e8f586a5613eddfcfac0b8ce278871e8cd11fdec892e4f3a4c9d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIncludeImportRanges")
    def reset_include_import_ranges(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeImportRanges", []))

    @builtins.property
    @jsii.member(jsii_name="includeImportRangesInput")
    def include_import_ranges_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "includeImportRangesInput"))

    @builtins.property
    @jsii.member(jsii_name="siteToSiteDataTransferInput")
    def site_to_site_data_transfer_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "siteToSiteDataTransferInput"))

    @builtins.property
    @jsii.member(jsii_name="urisInput")
    def uris_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "urisInput"))

    @builtins.property
    @jsii.member(jsii_name="includeImportRanges")
    def include_import_ranges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "includeImportRanges"))

    @include_import_ranges.setter
    def include_import_ranges(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca2abdd3f4af237d97fa0a5558c0465777bd3979d0f0e907a95e3e6c78fd0e9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeImportRanges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="siteToSiteDataTransfer")
    def site_to_site_data_transfer(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "siteToSiteDataTransfer"))

    @site_to_site_data_transfer.setter
    def site_to_site_data_transfer(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__561f14d7f252e5d6e181f19a7355b7b98855c6c80cfb38a557d67f6a900aba12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "siteToSiteDataTransfer", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uris")
    def uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "uris"))

    @uris.setter
    def uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f279c0ab1acc0cd834e32fecfe441d60c271b992ed061692960a50d6f1618e01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkConnectivitySpokeLinkedInterconnectAttachments]:
        return typing.cast(typing.Optional[NetworkConnectivitySpokeLinkedInterconnectAttachments], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkConnectivitySpokeLinkedInterconnectAttachments],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bd3b1dbf08095e36797aedc096f3f86b965cc798e05e51dac2207b5fadc09ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkConnectivitySpoke.NetworkConnectivitySpokeLinkedProducerVpcNetwork",
    jsii_struct_bases=[],
    name_mapping={
        "network": "network",
        "peering": "peering",
        "exclude_export_ranges": "excludeExportRanges",
        "include_export_ranges": "includeExportRanges",
    },
)
class NetworkConnectivitySpokeLinkedProducerVpcNetwork:
    def __init__(
        self,
        *,
        network: builtins.str,
        peering: builtins.str,
        exclude_export_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        include_export_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param network: The URI of the Service Consumer VPC that the Producer VPC is peered with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#network NetworkConnectivitySpoke#network}
        :param peering: The name of the VPC peering between the Service Consumer VPC and the Producer VPC (defined in the Tenant project) which is added to the NCC hub. This peering must be in ACTIVE state. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#peering NetworkConnectivitySpoke#peering}
        :param exclude_export_ranges: IP ranges encompassing the subnets to be excluded from peering. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#exclude_export_ranges NetworkConnectivitySpoke#exclude_export_ranges}
        :param include_export_ranges: IP ranges allowed to be included from peering. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#include_export_ranges NetworkConnectivitySpoke#include_export_ranges}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4aceff239059719303534e5a67c862929619684bbd9f5df9c0eebe64a1aad41)
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
            check_type(argname="argument peering", value=peering, expected_type=type_hints["peering"])
            check_type(argname="argument exclude_export_ranges", value=exclude_export_ranges, expected_type=type_hints["exclude_export_ranges"])
            check_type(argname="argument include_export_ranges", value=include_export_ranges, expected_type=type_hints["include_export_ranges"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "network": network,
            "peering": peering,
        }
        if exclude_export_ranges is not None:
            self._values["exclude_export_ranges"] = exclude_export_ranges
        if include_export_ranges is not None:
            self._values["include_export_ranges"] = include_export_ranges

    @builtins.property
    def network(self) -> builtins.str:
        '''The URI of the Service Consumer VPC that the Producer VPC is peered with.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#network NetworkConnectivitySpoke#network}
        '''
        result = self._values.get("network")
        assert result is not None, "Required property 'network' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def peering(self) -> builtins.str:
        '''The name of the VPC peering between the Service Consumer VPC and the Producer VPC (defined in the Tenant project) which is added to the NCC hub.

        This peering must be in ACTIVE state.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#peering NetworkConnectivitySpoke#peering}
        '''
        result = self._values.get("peering")
        assert result is not None, "Required property 'peering' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def exclude_export_ranges(self) -> typing.Optional[typing.List[builtins.str]]:
        '''IP ranges encompassing the subnets to be excluded from peering.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#exclude_export_ranges NetworkConnectivitySpoke#exclude_export_ranges}
        '''
        result = self._values.get("exclude_export_ranges")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def include_export_ranges(self) -> typing.Optional[typing.List[builtins.str]]:
        '''IP ranges allowed to be included from peering.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#include_export_ranges NetworkConnectivitySpoke#include_export_ranges}
        '''
        result = self._values.get("include_export_ranges")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkConnectivitySpokeLinkedProducerVpcNetwork(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkConnectivitySpokeLinkedProducerVpcNetworkOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkConnectivitySpoke.NetworkConnectivitySpokeLinkedProducerVpcNetworkOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b44da61ec2eb936df2d320d15c4ccc74c2e5ab7eeefd9d69addc3ca9e5c9aabf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetExcludeExportRanges")
    def reset_exclude_export_ranges(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludeExportRanges", []))

    @jsii.member(jsii_name="resetIncludeExportRanges")
    def reset_include_export_ranges(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeExportRanges", []))

    @builtins.property
    @jsii.member(jsii_name="producerNetwork")
    def producer_network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "producerNetwork"))

    @builtins.property
    @jsii.member(jsii_name="excludeExportRangesInput")
    def exclude_export_ranges_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "excludeExportRangesInput"))

    @builtins.property
    @jsii.member(jsii_name="includeExportRangesInput")
    def include_export_ranges_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "includeExportRangesInput"))

    @builtins.property
    @jsii.member(jsii_name="networkInput")
    def network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkInput"))

    @builtins.property
    @jsii.member(jsii_name="peeringInput")
    def peering_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "peeringInput"))

    @builtins.property
    @jsii.member(jsii_name="excludeExportRanges")
    def exclude_export_ranges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludeExportRanges"))

    @exclude_export_ranges.setter
    def exclude_export_ranges(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be9d85078105b803784a219039e806a8354e6d6371dc29ae1acc6b289fa887dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludeExportRanges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeExportRanges")
    def include_export_ranges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "includeExportRanges"))

    @include_export_ranges.setter
    def include_export_ranges(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__861abbefcf7fe19cdff9c5bfe158b33f8cfeacc2a0093155f49cef9bfbde1b0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeExportRanges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__493486460e2f2c190b6b54283dee9a525b13b786f2753151239eb6b8f9e20c94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="peering")
    def peering(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "peering"))

    @peering.setter
    def peering(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da366dd676a206df57e98402f001dbe757cd6cfe8c36b0250ed8aa28fb834978)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "peering", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkConnectivitySpokeLinkedProducerVpcNetwork]:
        return typing.cast(typing.Optional[NetworkConnectivitySpokeLinkedProducerVpcNetwork], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkConnectivitySpokeLinkedProducerVpcNetwork],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dafb1ef14428025a5cb2c4e0774c8706bcc4b4d814ac3c1c82b4c714be08ab93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkConnectivitySpoke.NetworkConnectivitySpokeLinkedRouterApplianceInstances",
    jsii_struct_bases=[],
    name_mapping={
        "instances": "instances",
        "site_to_site_data_transfer": "siteToSiteDataTransfer",
        "include_import_ranges": "includeImportRanges",
    },
)
class NetworkConnectivitySpokeLinkedRouterApplianceInstances:
    def __init__(
        self,
        *,
        instances: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkConnectivitySpokeLinkedRouterApplianceInstancesInstances", typing.Dict[builtins.str, typing.Any]]]],
        site_to_site_data_transfer: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        include_import_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param instances: instances block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#instances NetworkConnectivitySpoke#instances}
        :param site_to_site_data_transfer: A value that controls whether site-to-site data transfer is enabled for these resources. Note that data transfer is available only in supported locations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#site_to_site_data_transfer NetworkConnectivitySpoke#site_to_site_data_transfer}
        :param include_import_ranges: IP ranges allowed to be included during import from hub (does not control transit connectivity). The only allowed value for now is "ALL_IPV4_RANGES". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#include_import_ranges NetworkConnectivitySpoke#include_import_ranges}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c212b999dec8c9fe95472245ccef2b098df36c971c60212937edc0424eef8945)
            check_type(argname="argument instances", value=instances, expected_type=type_hints["instances"])
            check_type(argname="argument site_to_site_data_transfer", value=site_to_site_data_transfer, expected_type=type_hints["site_to_site_data_transfer"])
            check_type(argname="argument include_import_ranges", value=include_import_ranges, expected_type=type_hints["include_import_ranges"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instances": instances,
            "site_to_site_data_transfer": site_to_site_data_transfer,
        }
        if include_import_ranges is not None:
            self._values["include_import_ranges"] = include_import_ranges

    @builtins.property
    def instances(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkConnectivitySpokeLinkedRouterApplianceInstancesInstances"]]:
        '''instances block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#instances NetworkConnectivitySpoke#instances}
        '''
        result = self._values.get("instances")
        assert result is not None, "Required property 'instances' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkConnectivitySpokeLinkedRouterApplianceInstancesInstances"]], result)

    @builtins.property
    def site_to_site_data_transfer(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''A value that controls whether site-to-site data transfer is enabled for these resources.

        Note that data transfer is available only in supported locations.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#site_to_site_data_transfer NetworkConnectivitySpoke#site_to_site_data_transfer}
        '''
        result = self._values.get("site_to_site_data_transfer")
        assert result is not None, "Required property 'site_to_site_data_transfer' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def include_import_ranges(self) -> typing.Optional[typing.List[builtins.str]]:
        '''IP ranges allowed to be included during import from hub (does not control transit connectivity).

        The only allowed value for now is "ALL_IPV4_RANGES".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#include_import_ranges NetworkConnectivitySpoke#include_import_ranges}
        '''
        result = self._values.get("include_import_ranges")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkConnectivitySpokeLinkedRouterApplianceInstances(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkConnectivitySpoke.NetworkConnectivitySpokeLinkedRouterApplianceInstancesInstances",
    jsii_struct_bases=[],
    name_mapping={"ip_address": "ipAddress", "virtual_machine": "virtualMachine"},
)
class NetworkConnectivitySpokeLinkedRouterApplianceInstancesInstances:
    def __init__(
        self,
        *,
        ip_address: builtins.str,
        virtual_machine: builtins.str,
    ) -> None:
        '''
        :param ip_address: The IP address on the VM to use for peering. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#ip_address NetworkConnectivitySpoke#ip_address}
        :param virtual_machine: The URI of the virtual machine resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#virtual_machine NetworkConnectivitySpoke#virtual_machine}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bc102060677a5280344ee09c0c0a775b2f410d51d21f4f2f6d1a3811c65ebdb)
            check_type(argname="argument ip_address", value=ip_address, expected_type=type_hints["ip_address"])
            check_type(argname="argument virtual_machine", value=virtual_machine, expected_type=type_hints["virtual_machine"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ip_address": ip_address,
            "virtual_machine": virtual_machine,
        }

    @builtins.property
    def ip_address(self) -> builtins.str:
        '''The IP address on the VM to use for peering.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#ip_address NetworkConnectivitySpoke#ip_address}
        '''
        result = self._values.get("ip_address")
        assert result is not None, "Required property 'ip_address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def virtual_machine(self) -> builtins.str:
        '''The URI of the virtual machine resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#virtual_machine NetworkConnectivitySpoke#virtual_machine}
        '''
        result = self._values.get("virtual_machine")
        assert result is not None, "Required property 'virtual_machine' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkConnectivitySpokeLinkedRouterApplianceInstancesInstances(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkConnectivitySpokeLinkedRouterApplianceInstancesInstancesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkConnectivitySpoke.NetworkConnectivitySpokeLinkedRouterApplianceInstancesInstancesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c4d2b2e9a1b4c989fc00cf83015116464a4d260d6b4d73a17edbe0c4e5b8798a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NetworkConnectivitySpokeLinkedRouterApplianceInstancesInstancesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0986d4c663a8b61a545140661ea68fb8a13a5cc014e0b41a5ba54a2061d6cec7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkConnectivitySpokeLinkedRouterApplianceInstancesInstancesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1dc075695e69fce7859750f15dab3d50d1aeb74f2f9b7fe935766b5f966d3e0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__38d1d700702f77771cd1e5f349113321f711cb15246537cba22422267c337902)
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
            type_hints = typing.get_type_hints(_typecheckingstub__45b595e45a142b93fe0e754f41d0c9c2a85c089a7b1666bfc3a98d6ca0fd3f8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkConnectivitySpokeLinkedRouterApplianceInstancesInstances]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkConnectivitySpokeLinkedRouterApplianceInstancesInstances]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkConnectivitySpokeLinkedRouterApplianceInstancesInstances]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffc62d66f7f9247117debbd164618915a15f5430c3b17fc4f963f77d017e3cc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkConnectivitySpokeLinkedRouterApplianceInstancesInstancesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkConnectivitySpoke.NetworkConnectivitySpokeLinkedRouterApplianceInstancesInstancesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__09883fa5db70381e79036283f2ec694bce22a49fe579c7b0cf142c044ad9c5c0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="ipAddressInput")
    def ip_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualMachineInput")
    def virtual_machine_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "virtualMachineInput"))

    @builtins.property
    @jsii.member(jsii_name="ipAddress")
    def ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAddress"))

    @ip_address.setter
    def ip_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cdf49615dbfda7376f821c3b86e8e2de9633635e8385b93455afd78ccf2408d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="virtualMachine")
    def virtual_machine(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualMachine"))

    @virtual_machine.setter
    def virtual_machine(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f98f69f0f54ac8f2e056077783bfea68a5d23bd9371bb445cd840dd33601a27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualMachine", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkConnectivitySpokeLinkedRouterApplianceInstancesInstances]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkConnectivitySpokeLinkedRouterApplianceInstancesInstances]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkConnectivitySpokeLinkedRouterApplianceInstancesInstances]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8eed65a13fbffb4ec5d1b763909da53471ed96836b2f6e51a33b868469729ca1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkConnectivitySpokeLinkedRouterApplianceInstancesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkConnectivitySpoke.NetworkConnectivitySpokeLinkedRouterApplianceInstancesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__087a03a528955f57e3eb5127f6ec737419c8cc24614659be9d2f6280d75c1fe7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putInstances")
    def put_instances(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkConnectivitySpokeLinkedRouterApplianceInstancesInstances, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b451f74f0549526f283e42f4cfafc600d18b0832ceab12954df07e2a65818f29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInstances", [value]))

    @jsii.member(jsii_name="resetIncludeImportRanges")
    def reset_include_import_ranges(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeImportRanges", []))

    @builtins.property
    @jsii.member(jsii_name="instances")
    def instances(
        self,
    ) -> NetworkConnectivitySpokeLinkedRouterApplianceInstancesInstancesList:
        return typing.cast(NetworkConnectivitySpokeLinkedRouterApplianceInstancesInstancesList, jsii.get(self, "instances"))

    @builtins.property
    @jsii.member(jsii_name="includeImportRangesInput")
    def include_import_ranges_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "includeImportRangesInput"))

    @builtins.property
    @jsii.member(jsii_name="instancesInput")
    def instances_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkConnectivitySpokeLinkedRouterApplianceInstancesInstances]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkConnectivitySpokeLinkedRouterApplianceInstancesInstances]]], jsii.get(self, "instancesInput"))

    @builtins.property
    @jsii.member(jsii_name="siteToSiteDataTransferInput")
    def site_to_site_data_transfer_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "siteToSiteDataTransferInput"))

    @builtins.property
    @jsii.member(jsii_name="includeImportRanges")
    def include_import_ranges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "includeImportRanges"))

    @include_import_ranges.setter
    def include_import_ranges(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__910554719b31b606ef7599495672a2c5f1f7af4007cf49b2e78c36ba4f94b63c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeImportRanges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="siteToSiteDataTransfer")
    def site_to_site_data_transfer(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "siteToSiteDataTransfer"))

    @site_to_site_data_transfer.setter
    def site_to_site_data_transfer(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__376c7bf84728ccb9a18a06845ed02744f9fd5246612d58669729182326e27107)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "siteToSiteDataTransfer", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkConnectivitySpokeLinkedRouterApplianceInstances]:
        return typing.cast(typing.Optional[NetworkConnectivitySpokeLinkedRouterApplianceInstances], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkConnectivitySpokeLinkedRouterApplianceInstances],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a485d2d5f2c6b37d22b8d30a6dfd288050d4d0d95a69c302bb62073a8d97617)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkConnectivitySpoke.NetworkConnectivitySpokeLinkedVpcNetwork",
    jsii_struct_bases=[],
    name_mapping={
        "uri": "uri",
        "exclude_export_ranges": "excludeExportRanges",
        "include_export_ranges": "includeExportRanges",
    },
)
class NetworkConnectivitySpokeLinkedVpcNetwork:
    def __init__(
        self,
        *,
        uri: builtins.str,
        exclude_export_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        include_export_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param uri: The URI of the VPC network resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#uri NetworkConnectivitySpoke#uri}
        :param exclude_export_ranges: IP ranges encompassing the subnets to be excluded from peering. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#exclude_export_ranges NetworkConnectivitySpoke#exclude_export_ranges}
        :param include_export_ranges: IP ranges allowed to be included from peering. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#include_export_ranges NetworkConnectivitySpoke#include_export_ranges}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c27e4c0f67f0765dc585de4fb61c4cfc194d1bf0441f527a55506b49669cc827)
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
            check_type(argname="argument exclude_export_ranges", value=exclude_export_ranges, expected_type=type_hints["exclude_export_ranges"])
            check_type(argname="argument include_export_ranges", value=include_export_ranges, expected_type=type_hints["include_export_ranges"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "uri": uri,
        }
        if exclude_export_ranges is not None:
            self._values["exclude_export_ranges"] = exclude_export_ranges
        if include_export_ranges is not None:
            self._values["include_export_ranges"] = include_export_ranges

    @builtins.property
    def uri(self) -> builtins.str:
        '''The URI of the VPC network resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#uri NetworkConnectivitySpoke#uri}
        '''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def exclude_export_ranges(self) -> typing.Optional[typing.List[builtins.str]]:
        '''IP ranges encompassing the subnets to be excluded from peering.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#exclude_export_ranges NetworkConnectivitySpoke#exclude_export_ranges}
        '''
        result = self._values.get("exclude_export_ranges")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def include_export_ranges(self) -> typing.Optional[typing.List[builtins.str]]:
        '''IP ranges allowed to be included from peering.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#include_export_ranges NetworkConnectivitySpoke#include_export_ranges}
        '''
        result = self._values.get("include_export_ranges")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkConnectivitySpokeLinkedVpcNetwork(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkConnectivitySpokeLinkedVpcNetworkOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkConnectivitySpoke.NetworkConnectivitySpokeLinkedVpcNetworkOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__54fb8140af514f8ae3d71d62a4d86643a833cef4b3ac88b4650c88f8bedecba2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetExcludeExportRanges")
    def reset_exclude_export_ranges(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludeExportRanges", []))

    @jsii.member(jsii_name="resetIncludeExportRanges")
    def reset_include_export_ranges(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeExportRanges", []))

    @builtins.property
    @jsii.member(jsii_name="excludeExportRangesInput")
    def exclude_export_ranges_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "excludeExportRangesInput"))

    @builtins.property
    @jsii.member(jsii_name="includeExportRangesInput")
    def include_export_ranges_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "includeExportRangesInput"))

    @builtins.property
    @jsii.member(jsii_name="uriInput")
    def uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uriInput"))

    @builtins.property
    @jsii.member(jsii_name="excludeExportRanges")
    def exclude_export_ranges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludeExportRanges"))

    @exclude_export_ranges.setter
    def exclude_export_ranges(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d22e17360e5e8b622f6ca8a46eb837976de5a4b8a2ac4aa961762e63143b43f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludeExportRanges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeExportRanges")
    def include_export_ranges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "includeExportRanges"))

    @include_export_ranges.setter
    def include_export_ranges(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96500d297fe42023284addda024aac2173e387a8e16df198bb7de90d6dcdb0f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeExportRanges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff98e629a0f6f02bd06ddd8eb5c3550cf8a84347360d2e742511f1a8a2a41caf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkConnectivitySpokeLinkedVpcNetwork]:
        return typing.cast(typing.Optional[NetworkConnectivitySpokeLinkedVpcNetwork], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkConnectivitySpokeLinkedVpcNetwork],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ce5256ce7ecbda9e477471bf694aa459ba6f1fa5049dd852383b1db4a32fafe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkConnectivitySpoke.NetworkConnectivitySpokeLinkedVpnTunnels",
    jsii_struct_bases=[],
    name_mapping={
        "site_to_site_data_transfer": "siteToSiteDataTransfer",
        "uris": "uris",
        "include_import_ranges": "includeImportRanges",
    },
)
class NetworkConnectivitySpokeLinkedVpnTunnels:
    def __init__(
        self,
        *,
        site_to_site_data_transfer: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        uris: typing.Sequence[builtins.str],
        include_import_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param site_to_site_data_transfer: A value that controls whether site-to-site data transfer is enabled for these resources. Note that data transfer is available only in supported locations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#site_to_site_data_transfer NetworkConnectivitySpoke#site_to_site_data_transfer}
        :param uris: The URIs of linked VPN tunnel resources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#uris NetworkConnectivitySpoke#uris}
        :param include_import_ranges: IP ranges allowed to be included during import from hub (does not control transit connectivity). The only allowed value for now is "ALL_IPV4_RANGES". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#include_import_ranges NetworkConnectivitySpoke#include_import_ranges}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25a36120ab4da3ae306f488b0bd4107a1dea5133588c4f19866697307ff44f66)
            check_type(argname="argument site_to_site_data_transfer", value=site_to_site_data_transfer, expected_type=type_hints["site_to_site_data_transfer"])
            check_type(argname="argument uris", value=uris, expected_type=type_hints["uris"])
            check_type(argname="argument include_import_ranges", value=include_import_ranges, expected_type=type_hints["include_import_ranges"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "site_to_site_data_transfer": site_to_site_data_transfer,
            "uris": uris,
        }
        if include_import_ranges is not None:
            self._values["include_import_ranges"] = include_import_ranges

    @builtins.property
    def site_to_site_data_transfer(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''A value that controls whether site-to-site data transfer is enabled for these resources.

        Note that data transfer is available only in supported locations.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#site_to_site_data_transfer NetworkConnectivitySpoke#site_to_site_data_transfer}
        '''
        result = self._values.get("site_to_site_data_transfer")
        assert result is not None, "Required property 'site_to_site_data_transfer' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def uris(self) -> typing.List[builtins.str]:
        '''The URIs of linked VPN tunnel resources.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#uris NetworkConnectivitySpoke#uris}
        '''
        result = self._values.get("uris")
        assert result is not None, "Required property 'uris' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def include_import_ranges(self) -> typing.Optional[typing.List[builtins.str]]:
        '''IP ranges allowed to be included during import from hub (does not control transit connectivity).

        The only allowed value for now is "ALL_IPV4_RANGES".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#include_import_ranges NetworkConnectivitySpoke#include_import_ranges}
        '''
        result = self._values.get("include_import_ranges")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkConnectivitySpokeLinkedVpnTunnels(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkConnectivitySpokeLinkedVpnTunnelsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkConnectivitySpoke.NetworkConnectivitySpokeLinkedVpnTunnelsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f02f2ae8e71da1a125be399d85f9654fb7b9b4ef5c77d8167e5e54b16650007b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIncludeImportRanges")
    def reset_include_import_ranges(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeImportRanges", []))

    @builtins.property
    @jsii.member(jsii_name="includeImportRangesInput")
    def include_import_ranges_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "includeImportRangesInput"))

    @builtins.property
    @jsii.member(jsii_name="siteToSiteDataTransferInput")
    def site_to_site_data_transfer_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "siteToSiteDataTransferInput"))

    @builtins.property
    @jsii.member(jsii_name="urisInput")
    def uris_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "urisInput"))

    @builtins.property
    @jsii.member(jsii_name="includeImportRanges")
    def include_import_ranges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "includeImportRanges"))

    @include_import_ranges.setter
    def include_import_ranges(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcd9338bff2f2001176ccfcbec131e4a1fd6da2addc47688eca5abe1c4693afe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeImportRanges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="siteToSiteDataTransfer")
    def site_to_site_data_transfer(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "siteToSiteDataTransfer"))

    @site_to_site_data_transfer.setter
    def site_to_site_data_transfer(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d5861a02d6f2309fb52ea778aa78c93847c47eb856b7f46eb1eba2ab6c5a7c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "siteToSiteDataTransfer", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uris")
    def uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "uris"))

    @uris.setter
    def uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2b6980f4eb0f02a141a64c9b1950588452f5327f9c8e2164b958e58fb416bcd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkConnectivitySpokeLinkedVpnTunnels]:
        return typing.cast(typing.Optional[NetworkConnectivitySpokeLinkedVpnTunnels], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkConnectivitySpokeLinkedVpnTunnels],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6f2d4fa2c62f0157946f7c149be2cc54f1dc4c3c7086e84e8dc66a8b3f9d1f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkConnectivitySpoke.NetworkConnectivitySpokeReasons",
    jsii_struct_bases=[],
    name_mapping={},
)
class NetworkConnectivitySpokeReasons:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkConnectivitySpokeReasons(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkConnectivitySpokeReasonsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkConnectivitySpoke.NetworkConnectivitySpokeReasonsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__002bce4508ceb185b276bfcae592163820393b37d1117eae5441e5b7ed9e20b8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NetworkConnectivitySpokeReasonsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1d1c74979a65c511e3131c6dce994f4f60f71c895b25e0c02b99523f7e038f1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkConnectivitySpokeReasonsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a73fa291ed36f3103fc905cf3777b32328da383c97938bd6f579b4ede19e9c0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9557afc634cfa74d569320d5486c71521b2c9dd91f081ef758c67aff43bcb567)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e6172e10accfadc3a1db0513a15ea0a6b03194ab271422c7dfd6b6e4a0503d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class NetworkConnectivitySpokeReasonsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkConnectivitySpoke.NetworkConnectivitySpokeReasonsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__687ac24c8fd51ef1ebc867868d35991a6c1ef95d84f20e99d90ff29d364df524)
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
    @jsii.member(jsii_name="message")
    def message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "message"))

    @builtins.property
    @jsii.member(jsii_name="userDetails")
    def user_details(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userDetails"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[NetworkConnectivitySpokeReasons]:
        return typing.cast(typing.Optional[NetworkConnectivitySpokeReasons], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkConnectivitySpokeReasons],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4ae7833890191d97bf8c141550ba1271e2630eaae9aece5a18a71b78ab0f625)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkConnectivitySpoke.NetworkConnectivitySpokeTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class NetworkConnectivitySpokeTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#create NetworkConnectivitySpoke#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#delete NetworkConnectivitySpoke#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#update NetworkConnectivitySpoke#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03f29328ca4b9b78224bc008a7ccd8474d81d1117cb7a99c90051778f19c7930)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#create NetworkConnectivitySpoke#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#delete NetworkConnectivitySpoke#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_spoke#update NetworkConnectivitySpoke#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkConnectivitySpokeTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkConnectivitySpokeTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkConnectivitySpoke.NetworkConnectivitySpokeTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a43dfa0993541cd313ecc92516989b8f38d51d5db19de65ba43463a86ac3250)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c3530fd304cb339fc6a3b7f814f7c2ff9fc948ccddda7f2318a9d8fcec6bfe0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6505f2735a599fe581b221506fad21d66aeaab6f2f7f1a125eaf59d09cb9ba30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5ee7c12d7e3eae9cd440820429f507a3fa8ad643e95386c3de7d4220681057b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkConnectivitySpokeTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkConnectivitySpokeTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkConnectivitySpokeTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a14b7041032494b622c7eca2534649552015517c5d0d940c357449820bdca4cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "NetworkConnectivitySpoke",
    "NetworkConnectivitySpokeConfig",
    "NetworkConnectivitySpokeLinkedInterconnectAttachments",
    "NetworkConnectivitySpokeLinkedInterconnectAttachmentsOutputReference",
    "NetworkConnectivitySpokeLinkedProducerVpcNetwork",
    "NetworkConnectivitySpokeLinkedProducerVpcNetworkOutputReference",
    "NetworkConnectivitySpokeLinkedRouterApplianceInstances",
    "NetworkConnectivitySpokeLinkedRouterApplianceInstancesInstances",
    "NetworkConnectivitySpokeLinkedRouterApplianceInstancesInstancesList",
    "NetworkConnectivitySpokeLinkedRouterApplianceInstancesInstancesOutputReference",
    "NetworkConnectivitySpokeLinkedRouterApplianceInstancesOutputReference",
    "NetworkConnectivitySpokeLinkedVpcNetwork",
    "NetworkConnectivitySpokeLinkedVpcNetworkOutputReference",
    "NetworkConnectivitySpokeLinkedVpnTunnels",
    "NetworkConnectivitySpokeLinkedVpnTunnelsOutputReference",
    "NetworkConnectivitySpokeReasons",
    "NetworkConnectivitySpokeReasonsList",
    "NetworkConnectivitySpokeReasonsOutputReference",
    "NetworkConnectivitySpokeTimeouts",
    "NetworkConnectivitySpokeTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__bc96b7abfa74c4d2bf6743ee906865f83afb04ac79c7f09610526aed7a234e7d(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    hub: builtins.str,
    location: builtins.str,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    group: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    linked_interconnect_attachments: typing.Optional[typing.Union[NetworkConnectivitySpokeLinkedInterconnectAttachments, typing.Dict[builtins.str, typing.Any]]] = None,
    linked_producer_vpc_network: typing.Optional[typing.Union[NetworkConnectivitySpokeLinkedProducerVpcNetwork, typing.Dict[builtins.str, typing.Any]]] = None,
    linked_router_appliance_instances: typing.Optional[typing.Union[NetworkConnectivitySpokeLinkedRouterApplianceInstances, typing.Dict[builtins.str, typing.Any]]] = None,
    linked_vpc_network: typing.Optional[typing.Union[NetworkConnectivitySpokeLinkedVpcNetwork, typing.Dict[builtins.str, typing.Any]]] = None,
    linked_vpn_tunnels: typing.Optional[typing.Union[NetworkConnectivitySpokeLinkedVpnTunnels, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[NetworkConnectivitySpokeTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__e56dc8ea8103c57c426edf05be5efa293ac83feaf5b3b9bb1a46bf843eacbdd0(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55c4a8c8db5163262cc9638e3b1d2cd6dfa4eb126e098f17609e524438b120e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b410faa8e5b93a59d6d1909e1145038abc3614e4c386009701f1189087d0d8b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f34005a672d0e7ef49937dc1190732151a15e964dd58ae54f768f1bb836d0ebe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9a7697b03fdc161fb3c6bb99421186a6ce1a2f96f7794c3c657bfe954ebac79(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d46639bf04ec13fc76ecb42dbdb6fd7a158485e07369dbdafd6d3880f3f36e37(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25812cc2d34c49536982206b65ceb554ecccbbe9bbd0aeffa3f9204fbaeac47c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8ccebf2480b171eb9e979f52157670d32ae95d58775d721d33d46d5c7d3aab5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e381a433570885220448327a2126f6d4a47432ca9006c02e5af4b2dbe41188f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93134a2b405500b5500e47a1c7f44dd201f4b3b1e7fb8d27b71529ba8aaa9048(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    hub: builtins.str,
    location: builtins.str,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    group: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    linked_interconnect_attachments: typing.Optional[typing.Union[NetworkConnectivitySpokeLinkedInterconnectAttachments, typing.Dict[builtins.str, typing.Any]]] = None,
    linked_producer_vpc_network: typing.Optional[typing.Union[NetworkConnectivitySpokeLinkedProducerVpcNetwork, typing.Dict[builtins.str, typing.Any]]] = None,
    linked_router_appliance_instances: typing.Optional[typing.Union[NetworkConnectivitySpokeLinkedRouterApplianceInstances, typing.Dict[builtins.str, typing.Any]]] = None,
    linked_vpc_network: typing.Optional[typing.Union[NetworkConnectivitySpokeLinkedVpcNetwork, typing.Dict[builtins.str, typing.Any]]] = None,
    linked_vpn_tunnels: typing.Optional[typing.Union[NetworkConnectivitySpokeLinkedVpnTunnels, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[NetworkConnectivitySpokeTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__128f78c240308f3898f4dabc5cad80c5c6b285c76989654bd5c256c31558141c(
    *,
    site_to_site_data_transfer: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    uris: typing.Sequence[builtins.str],
    include_import_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__908440db75c0e8f586a5613eddfcfac0b8ce278871e8cd11fdec892e4f3a4c9d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca2abdd3f4af237d97fa0a5558c0465777bd3979d0f0e907a95e3e6c78fd0e9b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__561f14d7f252e5d6e181f19a7355b7b98855c6c80cfb38a557d67f6a900aba12(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f279c0ab1acc0cd834e32fecfe441d60c271b992ed061692960a50d6f1618e01(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bd3b1dbf08095e36797aedc096f3f86b965cc798e05e51dac2207b5fadc09ee(
    value: typing.Optional[NetworkConnectivitySpokeLinkedInterconnectAttachments],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4aceff239059719303534e5a67c862929619684bbd9f5df9c0eebe64a1aad41(
    *,
    network: builtins.str,
    peering: builtins.str,
    exclude_export_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    include_export_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b44da61ec2eb936df2d320d15c4ccc74c2e5ab7eeefd9d69addc3ca9e5c9aabf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be9d85078105b803784a219039e806a8354e6d6371dc29ae1acc6b289fa887dc(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__861abbefcf7fe19cdff9c5bfe158b33f8cfeacc2a0093155f49cef9bfbde1b0a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__493486460e2f2c190b6b54283dee9a525b13b786f2753151239eb6b8f9e20c94(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da366dd676a206df57e98402f001dbe757cd6cfe8c36b0250ed8aa28fb834978(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dafb1ef14428025a5cb2c4e0774c8706bcc4b4d814ac3c1c82b4c714be08ab93(
    value: typing.Optional[NetworkConnectivitySpokeLinkedProducerVpcNetwork],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c212b999dec8c9fe95472245ccef2b098df36c971c60212937edc0424eef8945(
    *,
    instances: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkConnectivitySpokeLinkedRouterApplianceInstancesInstances, typing.Dict[builtins.str, typing.Any]]]],
    site_to_site_data_transfer: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    include_import_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bc102060677a5280344ee09c0c0a775b2f410d51d21f4f2f6d1a3811c65ebdb(
    *,
    ip_address: builtins.str,
    virtual_machine: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4d2b2e9a1b4c989fc00cf83015116464a4d260d6b4d73a17edbe0c4e5b8798a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0986d4c663a8b61a545140661ea68fb8a13a5cc014e0b41a5ba54a2061d6cec7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1dc075695e69fce7859750f15dab3d50d1aeb74f2f9b7fe935766b5f966d3e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38d1d700702f77771cd1e5f349113321f711cb15246537cba22422267c337902(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45b595e45a142b93fe0e754f41d0c9c2a85c089a7b1666bfc3a98d6ca0fd3f8e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffc62d66f7f9247117debbd164618915a15f5430c3b17fc4f963f77d017e3cc9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkConnectivitySpokeLinkedRouterApplianceInstancesInstances]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09883fa5db70381e79036283f2ec694bce22a49fe579c7b0cf142c044ad9c5c0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cdf49615dbfda7376f821c3b86e8e2de9633635e8385b93455afd78ccf2408d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f98f69f0f54ac8f2e056077783bfea68a5d23bd9371bb445cd840dd33601a27(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8eed65a13fbffb4ec5d1b763909da53471ed96836b2f6e51a33b868469729ca1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkConnectivitySpokeLinkedRouterApplianceInstancesInstances]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__087a03a528955f57e3eb5127f6ec737419c8cc24614659be9d2f6280d75c1fe7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b451f74f0549526f283e42f4cfafc600d18b0832ceab12954df07e2a65818f29(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkConnectivitySpokeLinkedRouterApplianceInstancesInstances, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__910554719b31b606ef7599495672a2c5f1f7af4007cf49b2e78c36ba4f94b63c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__376c7bf84728ccb9a18a06845ed02744f9fd5246612d58669729182326e27107(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a485d2d5f2c6b37d22b8d30a6dfd288050d4d0d95a69c302bb62073a8d97617(
    value: typing.Optional[NetworkConnectivitySpokeLinkedRouterApplianceInstances],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c27e4c0f67f0765dc585de4fb61c4cfc194d1bf0441f527a55506b49669cc827(
    *,
    uri: builtins.str,
    exclude_export_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    include_export_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54fb8140af514f8ae3d71d62a4d86643a833cef4b3ac88b4650c88f8bedecba2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d22e17360e5e8b622f6ca8a46eb837976de5a4b8a2ac4aa961762e63143b43f3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96500d297fe42023284addda024aac2173e387a8e16df198bb7de90d6dcdb0f0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff98e629a0f6f02bd06ddd8eb5c3550cf8a84347360d2e742511f1a8a2a41caf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ce5256ce7ecbda9e477471bf694aa459ba6f1fa5049dd852383b1db4a32fafe(
    value: typing.Optional[NetworkConnectivitySpokeLinkedVpcNetwork],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25a36120ab4da3ae306f488b0bd4107a1dea5133588c4f19866697307ff44f66(
    *,
    site_to_site_data_transfer: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    uris: typing.Sequence[builtins.str],
    include_import_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f02f2ae8e71da1a125be399d85f9654fb7b9b4ef5c77d8167e5e54b16650007b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcd9338bff2f2001176ccfcbec131e4a1fd6da2addc47688eca5abe1c4693afe(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d5861a02d6f2309fb52ea778aa78c93847c47eb856b7f46eb1eba2ab6c5a7c2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2b6980f4eb0f02a141a64c9b1950588452f5327f9c8e2164b958e58fb416bcd(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6f2d4fa2c62f0157946f7c149be2cc54f1dc4c3c7086e84e8dc66a8b3f9d1f4(
    value: typing.Optional[NetworkConnectivitySpokeLinkedVpnTunnels],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__002bce4508ceb185b276bfcae592163820393b37d1117eae5441e5b7ed9e20b8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1d1c74979a65c511e3131c6dce994f4f60f71c895b25e0c02b99523f7e038f1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a73fa291ed36f3103fc905cf3777b32328da383c97938bd6f579b4ede19e9c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9557afc634cfa74d569320d5486c71521b2c9dd91f081ef758c67aff43bcb567(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e6172e10accfadc3a1db0513a15ea0a6b03194ab271422c7dfd6b6e4a0503d7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__687ac24c8fd51ef1ebc867868d35991a6c1ef95d84f20e99d90ff29d364df524(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4ae7833890191d97bf8c141550ba1271e2630eaae9aece5a18a71b78ab0f625(
    value: typing.Optional[NetworkConnectivitySpokeReasons],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03f29328ca4b9b78224bc008a7ccd8474d81d1117cb7a99c90051778f19c7930(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a43dfa0993541cd313ecc92516989b8f38d51d5db19de65ba43463a86ac3250(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c3530fd304cb339fc6a3b7f814f7c2ff9fc948ccddda7f2318a9d8fcec6bfe0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6505f2735a599fe581b221506fad21d66aeaab6f2f7f1a125eaf59d09cb9ba30(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5ee7c12d7e3eae9cd440820429f507a3fa8ad643e95386c3de7d4220681057b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a14b7041032494b622c7eca2534649552015517c5d0d940c357449820bdca4cd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkConnectivitySpokeTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
