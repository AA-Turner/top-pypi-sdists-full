r'''
# `google_vmwareengine_network_peering`

Refer to the Terraform Registry for docs: [`google_vmwareengine_network_peering`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_network_peering).
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


class VmwareengineNetworkPeering(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vmwareengineNetworkPeering.VmwareengineNetworkPeering",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_network_peering google_vmwareengine_network_peering}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        peer_network: builtins.str,
        peer_network_type: builtins.str,
        vmware_engine_network: builtins.str,
        description: typing.Optional[builtins.str] = None,
        export_custom_routes: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        export_custom_routes_with_public_ip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        import_custom_routes: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        import_custom_routes_with_public_ip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["VmwareengineNetworkPeeringTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_network_peering google_vmwareengine_network_peering} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: The ID of the Network Peering. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_network_peering#name VmwareengineNetworkPeering#name}
        :param peer_network: The relative resource name of the network to peer with a standard VMware Engine network. The provided network can be a consumer VPC network or another standard VMware Engine network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_network_peering#peer_network VmwareengineNetworkPeering#peer_network}
        :param peer_network_type: The type of the network to peer with the VMware Engine network. Possible values: ["STANDARD", "VMWARE_ENGINE_NETWORK", "PRIVATE_SERVICES_ACCESS", "NETAPP_CLOUD_VOLUMES", "THIRD_PARTY_SERVICE", "DELL_POWERSCALE", "GOOGLE_CLOUD_NETAPP_VOLUMES"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_network_peering#peer_network_type VmwareengineNetworkPeering#peer_network_type}
        :param vmware_engine_network: The relative resource name of the VMware Engine network. Specify the name in the following form: projects/{project}/locations/{location}/vmwareEngineNetworks/{vmwareEngineNetworkId} where {project} can either be a project number or a project ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_network_peering#vmware_engine_network VmwareengineNetworkPeering#vmware_engine_network}
        :param description: User-provided description for this network peering. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_network_peering#description VmwareengineNetworkPeering#description}
        :param export_custom_routes: True if custom routes are exported to the peered network; false otherwise. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_network_peering#export_custom_routes VmwareengineNetworkPeering#export_custom_routes}
        :param export_custom_routes_with_public_ip: True if all subnet routes with a public IP address range are exported; false otherwise. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_network_peering#export_custom_routes_with_public_ip VmwareengineNetworkPeering#export_custom_routes_with_public_ip}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_network_peering#id VmwareengineNetworkPeering#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param import_custom_routes: True if custom routes are imported from the peered network; false otherwise. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_network_peering#import_custom_routes VmwareengineNetworkPeering#import_custom_routes}
        :param import_custom_routes_with_public_ip: True if custom routes are imported from the peered network; false otherwise. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_network_peering#import_custom_routes_with_public_ip VmwareengineNetworkPeering#import_custom_routes_with_public_ip}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_network_peering#project VmwareengineNetworkPeering#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_network_peering#timeouts VmwareengineNetworkPeering#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46f6084d842375fd84078d98e2bffd3fa04bd430970fda36cbee7ae3abfdcaab)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = VmwareengineNetworkPeeringConfig(
            name=name,
            peer_network=peer_network,
            peer_network_type=peer_network_type,
            vmware_engine_network=vmware_engine_network,
            description=description,
            export_custom_routes=export_custom_routes,
            export_custom_routes_with_public_ip=export_custom_routes_with_public_ip,
            id=id,
            import_custom_routes=import_custom_routes,
            import_custom_routes_with_public_ip=import_custom_routes_with_public_ip,
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
        '''Generates CDKTF code for importing a VmwareengineNetworkPeering resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the VmwareengineNetworkPeering to import.
        :param import_from_id: The id of the existing VmwareengineNetworkPeering that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_network_peering#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the VmwareengineNetworkPeering to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6456cf2aa20fa9d7af6ba8ca9b1d489f19a7adeb132b3a8985af10674e9067b8)
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_network_peering#create VmwareengineNetworkPeering#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_network_peering#delete VmwareengineNetworkPeering#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_network_peering#update VmwareengineNetworkPeering#update}.
        '''
        value = VmwareengineNetworkPeeringTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetExportCustomRoutes")
    def reset_export_custom_routes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExportCustomRoutes", []))

    @jsii.member(jsii_name="resetExportCustomRoutesWithPublicIp")
    def reset_export_custom_routes_with_public_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExportCustomRoutesWithPublicIp", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetImportCustomRoutes")
    def reset_import_custom_routes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImportCustomRoutes", []))

    @jsii.member(jsii_name="resetImportCustomRoutesWithPublicIp")
    def reset_import_custom_routes_with_public_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImportCustomRoutesWithPublicIp", []))

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
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="stateDetails")
    def state_details(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stateDetails"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "VmwareengineNetworkPeeringTimeoutsOutputReference":
        return typing.cast("VmwareengineNetworkPeeringTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="uid")
    def uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uid"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="vmwareEngineNetworkCanonical")
    def vmware_engine_network_canonical(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vmwareEngineNetworkCanonical"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="exportCustomRoutesInput")
    def export_custom_routes_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "exportCustomRoutesInput"))

    @builtins.property
    @jsii.member(jsii_name="exportCustomRoutesWithPublicIpInput")
    def export_custom_routes_with_public_ip_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "exportCustomRoutesWithPublicIpInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="importCustomRoutesInput")
    def import_custom_routes_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "importCustomRoutesInput"))

    @builtins.property
    @jsii.member(jsii_name="importCustomRoutesWithPublicIpInput")
    def import_custom_routes_with_public_ip_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "importCustomRoutesWithPublicIpInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="peerNetworkInput")
    def peer_network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "peerNetworkInput"))

    @builtins.property
    @jsii.member(jsii_name="peerNetworkTypeInput")
    def peer_network_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "peerNetworkTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VmwareengineNetworkPeeringTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VmwareengineNetworkPeeringTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="vmwareEngineNetworkInput")
    def vmware_engine_network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vmwareEngineNetworkInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__769ab36cf1845057756bd1b1573b02ea9e1f2911efed01fb489eb3048f8e6839)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exportCustomRoutes")
    def export_custom_routes(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "exportCustomRoutes"))

    @export_custom_routes.setter
    def export_custom_routes(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e2320f571be92279d5be522fafd2bdfa3342c7a6e70de849a8a54c1a50990b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exportCustomRoutes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exportCustomRoutesWithPublicIp")
    def export_custom_routes_with_public_ip(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "exportCustomRoutesWithPublicIp"))

    @export_custom_routes_with_public_ip.setter
    def export_custom_routes_with_public_ip(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87e324a0022caa19b440d6e8a3015985aa844fdd062d94f90841f16b34be65b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exportCustomRoutesWithPublicIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87437b72096933b1c72d783d1869bcdf4634a736678a2acb6dc4a0a6369ea9b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="importCustomRoutes")
    def import_custom_routes(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "importCustomRoutes"))

    @import_custom_routes.setter
    def import_custom_routes(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c9a638ad3cf120dfa48a4de53e9f97e563f052d6564b8c9b4658556e43c4a76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "importCustomRoutes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="importCustomRoutesWithPublicIp")
    def import_custom_routes_with_public_ip(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "importCustomRoutesWithPublicIp"))

    @import_custom_routes_with_public_ip.setter
    def import_custom_routes_with_public_ip(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ee2ce643b7f0b9e58d4598708dd0f779ce56f7c94d557576679b30dd47876ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "importCustomRoutesWithPublicIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fd12ce2222d67f2fe8ba4a0fc2dc6638d2a411e95fc048d03303a1502eacaf3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="peerNetwork")
    def peer_network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "peerNetwork"))

    @peer_network.setter
    def peer_network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a5674019b535c1178237274ec8bcccc2adae564be5c33de4f1800b56654c036)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "peerNetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="peerNetworkType")
    def peer_network_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "peerNetworkType"))

    @peer_network_type.setter
    def peer_network_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37a5ede724aacc39323595212a32bc3088f5d549bfe00fba039a7a65b2394df0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "peerNetworkType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fad2d03c5398983229c0d2b06c849a5366514ee007d372108f540ec6a220dfdb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vmwareEngineNetwork")
    def vmware_engine_network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vmwareEngineNetwork"))

    @vmware_engine_network.setter
    def vmware_engine_network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b83c5921c971c4c3adc71315dc8679dc628b19d259486037a3c9e89ea11b6a67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vmwareEngineNetwork", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vmwareengineNetworkPeering.VmwareengineNetworkPeeringConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "name": "name",
        "peer_network": "peerNetwork",
        "peer_network_type": "peerNetworkType",
        "vmware_engine_network": "vmwareEngineNetwork",
        "description": "description",
        "export_custom_routes": "exportCustomRoutes",
        "export_custom_routes_with_public_ip": "exportCustomRoutesWithPublicIp",
        "id": "id",
        "import_custom_routes": "importCustomRoutes",
        "import_custom_routes_with_public_ip": "importCustomRoutesWithPublicIp",
        "project": "project",
        "timeouts": "timeouts",
    },
)
class VmwareengineNetworkPeeringConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        name: builtins.str,
        peer_network: builtins.str,
        peer_network_type: builtins.str,
        vmware_engine_network: builtins.str,
        description: typing.Optional[builtins.str] = None,
        export_custom_routes: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        export_custom_routes_with_public_ip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        import_custom_routes: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        import_custom_routes_with_public_ip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["VmwareengineNetworkPeeringTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: The ID of the Network Peering. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_network_peering#name VmwareengineNetworkPeering#name}
        :param peer_network: The relative resource name of the network to peer with a standard VMware Engine network. The provided network can be a consumer VPC network or another standard VMware Engine network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_network_peering#peer_network VmwareengineNetworkPeering#peer_network}
        :param peer_network_type: The type of the network to peer with the VMware Engine network. Possible values: ["STANDARD", "VMWARE_ENGINE_NETWORK", "PRIVATE_SERVICES_ACCESS", "NETAPP_CLOUD_VOLUMES", "THIRD_PARTY_SERVICE", "DELL_POWERSCALE", "GOOGLE_CLOUD_NETAPP_VOLUMES"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_network_peering#peer_network_type VmwareengineNetworkPeering#peer_network_type}
        :param vmware_engine_network: The relative resource name of the VMware Engine network. Specify the name in the following form: projects/{project}/locations/{location}/vmwareEngineNetworks/{vmwareEngineNetworkId} where {project} can either be a project number or a project ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_network_peering#vmware_engine_network VmwareengineNetworkPeering#vmware_engine_network}
        :param description: User-provided description for this network peering. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_network_peering#description VmwareengineNetworkPeering#description}
        :param export_custom_routes: True if custom routes are exported to the peered network; false otherwise. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_network_peering#export_custom_routes VmwareengineNetworkPeering#export_custom_routes}
        :param export_custom_routes_with_public_ip: True if all subnet routes with a public IP address range are exported; false otherwise. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_network_peering#export_custom_routes_with_public_ip VmwareengineNetworkPeering#export_custom_routes_with_public_ip}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_network_peering#id VmwareengineNetworkPeering#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param import_custom_routes: True if custom routes are imported from the peered network; false otherwise. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_network_peering#import_custom_routes VmwareengineNetworkPeering#import_custom_routes}
        :param import_custom_routes_with_public_ip: True if custom routes are imported from the peered network; false otherwise. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_network_peering#import_custom_routes_with_public_ip VmwareengineNetworkPeering#import_custom_routes_with_public_ip}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_network_peering#project VmwareengineNetworkPeering#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_network_peering#timeouts VmwareengineNetworkPeering#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = VmwareengineNetworkPeeringTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b1cfefd082d915e128b7099b685fb31a1de0234547d66bb65ffd6d4cd595fc7)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument peer_network", value=peer_network, expected_type=type_hints["peer_network"])
            check_type(argname="argument peer_network_type", value=peer_network_type, expected_type=type_hints["peer_network_type"])
            check_type(argname="argument vmware_engine_network", value=vmware_engine_network, expected_type=type_hints["vmware_engine_network"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument export_custom_routes", value=export_custom_routes, expected_type=type_hints["export_custom_routes"])
            check_type(argname="argument export_custom_routes_with_public_ip", value=export_custom_routes_with_public_ip, expected_type=type_hints["export_custom_routes_with_public_ip"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument import_custom_routes", value=import_custom_routes, expected_type=type_hints["import_custom_routes"])
            check_type(argname="argument import_custom_routes_with_public_ip", value=import_custom_routes_with_public_ip, expected_type=type_hints["import_custom_routes_with_public_ip"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "peer_network": peer_network,
            "peer_network_type": peer_network_type,
            "vmware_engine_network": vmware_engine_network,
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
        if export_custom_routes is not None:
            self._values["export_custom_routes"] = export_custom_routes
        if export_custom_routes_with_public_ip is not None:
            self._values["export_custom_routes_with_public_ip"] = export_custom_routes_with_public_ip
        if id is not None:
            self._values["id"] = id
        if import_custom_routes is not None:
            self._values["import_custom_routes"] = import_custom_routes
        if import_custom_routes_with_public_ip is not None:
            self._values["import_custom_routes_with_public_ip"] = import_custom_routes_with_public_ip
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
    def name(self) -> builtins.str:
        '''The ID of the Network Peering.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_network_peering#name VmwareengineNetworkPeering#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def peer_network(self) -> builtins.str:
        '''The relative resource name of the network to peer with a standard VMware Engine network.

        The provided network can be a consumer VPC network or another standard VMware Engine network.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_network_peering#peer_network VmwareengineNetworkPeering#peer_network}
        '''
        result = self._values.get("peer_network")
        assert result is not None, "Required property 'peer_network' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def peer_network_type(self) -> builtins.str:
        '''The type of the network to peer with the VMware Engine network.

        Possible values: ["STANDARD", "VMWARE_ENGINE_NETWORK", "PRIVATE_SERVICES_ACCESS", "NETAPP_CLOUD_VOLUMES", "THIRD_PARTY_SERVICE", "DELL_POWERSCALE", "GOOGLE_CLOUD_NETAPP_VOLUMES"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_network_peering#peer_network_type VmwareengineNetworkPeering#peer_network_type}
        '''
        result = self._values.get("peer_network_type")
        assert result is not None, "Required property 'peer_network_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vmware_engine_network(self) -> builtins.str:
        '''The relative resource name of the VMware Engine network.

        Specify the name in the following form:
        projects/{project}/locations/{location}/vmwareEngineNetworks/{vmwareEngineNetworkId} where {project}
        can either be a project number or a project ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_network_peering#vmware_engine_network VmwareengineNetworkPeering#vmware_engine_network}
        '''
        result = self._values.get("vmware_engine_network")
        assert result is not None, "Required property 'vmware_engine_network' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''User-provided description for this network peering.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_network_peering#description VmwareengineNetworkPeering#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def export_custom_routes(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''True if custom routes are exported to the peered network; false otherwise.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_network_peering#export_custom_routes VmwareengineNetworkPeering#export_custom_routes}
        '''
        result = self._values.get("export_custom_routes")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def export_custom_routes_with_public_ip(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''True if all subnet routes with a public IP address range are exported; false otherwise.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_network_peering#export_custom_routes_with_public_ip VmwareengineNetworkPeering#export_custom_routes_with_public_ip}
        '''
        result = self._values.get("export_custom_routes_with_public_ip")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_network_peering#id VmwareengineNetworkPeering#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def import_custom_routes(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''True if custom routes are imported from the peered network; false otherwise.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_network_peering#import_custom_routes VmwareengineNetworkPeering#import_custom_routes}
        '''
        result = self._values.get("import_custom_routes")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def import_custom_routes_with_public_ip(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''True if custom routes are imported from the peered network; false otherwise.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_network_peering#import_custom_routes_with_public_ip VmwareengineNetworkPeering#import_custom_routes_with_public_ip}
        '''
        result = self._values.get("import_custom_routes_with_public_ip")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_network_peering#project VmwareengineNetworkPeering#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["VmwareengineNetworkPeeringTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_network_peering#timeouts VmwareengineNetworkPeering#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["VmwareengineNetworkPeeringTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VmwareengineNetworkPeeringConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vmwareengineNetworkPeering.VmwareengineNetworkPeeringTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class VmwareengineNetworkPeeringTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_network_peering#create VmwareengineNetworkPeering#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_network_peering#delete VmwareengineNetworkPeering#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_network_peering#update VmwareengineNetworkPeering#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d995639385ae39d3dc080f0857cf895819c581fbcfdaded7d3ad5e2913c060e5)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_network_peering#create VmwareengineNetworkPeering#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_network_peering#delete VmwareengineNetworkPeering#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_network_peering#update VmwareengineNetworkPeering#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VmwareengineNetworkPeeringTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VmwareengineNetworkPeeringTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vmwareengineNetworkPeering.VmwareengineNetworkPeeringTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf11371b533d6c160b5b3b2a00dfa48920bfcb3de3d1116339d6a5a32070e51a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5fc05bbc5d55a1f660f6eee2c02c2a257c2ebd76418c37534b9297afdbafe055)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cafefcf189cee9a89e5d5d7e15e6b04bba07e331430bd416735fab73d34b3535)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4aaefca0193ae88738d358da0c42dfa81f75762327e5a4f82ccaf0bc0f12d806)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VmwareengineNetworkPeeringTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VmwareengineNetworkPeeringTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VmwareengineNetworkPeeringTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__021b09acd59cba2b425bcf23b3cbd1610da83cd47e3a73ce1248048df39f7690)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "VmwareengineNetworkPeering",
    "VmwareengineNetworkPeeringConfig",
    "VmwareengineNetworkPeeringTimeouts",
    "VmwareengineNetworkPeeringTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__46f6084d842375fd84078d98e2bffd3fa04bd430970fda36cbee7ae3abfdcaab(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    peer_network: builtins.str,
    peer_network_type: builtins.str,
    vmware_engine_network: builtins.str,
    description: typing.Optional[builtins.str] = None,
    export_custom_routes: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    export_custom_routes_with_public_ip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    import_custom_routes: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    import_custom_routes_with_public_ip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[VmwareengineNetworkPeeringTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__6456cf2aa20fa9d7af6ba8ca9b1d489f19a7adeb132b3a8985af10674e9067b8(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__769ab36cf1845057756bd1b1573b02ea9e1f2911efed01fb489eb3048f8e6839(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e2320f571be92279d5be522fafd2bdfa3342c7a6e70de849a8a54c1a50990b2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87e324a0022caa19b440d6e8a3015985aa844fdd062d94f90841f16b34be65b3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87437b72096933b1c72d783d1869bcdf4634a736678a2acb6dc4a0a6369ea9b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c9a638ad3cf120dfa48a4de53e9f97e563f052d6564b8c9b4658556e43c4a76(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ee2ce643b7f0b9e58d4598708dd0f779ce56f7c94d557576679b30dd47876ee(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fd12ce2222d67f2fe8ba4a0fc2dc6638d2a411e95fc048d03303a1502eacaf3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a5674019b535c1178237274ec8bcccc2adae564be5c33de4f1800b56654c036(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37a5ede724aacc39323595212a32bc3088f5d549bfe00fba039a7a65b2394df0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fad2d03c5398983229c0d2b06c849a5366514ee007d372108f540ec6a220dfdb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b83c5921c971c4c3adc71315dc8679dc628b19d259486037a3c9e89ea11b6a67(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b1cfefd082d915e128b7099b685fb31a1de0234547d66bb65ffd6d4cd595fc7(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    peer_network: builtins.str,
    peer_network_type: builtins.str,
    vmware_engine_network: builtins.str,
    description: typing.Optional[builtins.str] = None,
    export_custom_routes: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    export_custom_routes_with_public_ip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    import_custom_routes: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    import_custom_routes_with_public_ip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[VmwareengineNetworkPeeringTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d995639385ae39d3dc080f0857cf895819c581fbcfdaded7d3ad5e2913c060e5(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf11371b533d6c160b5b3b2a00dfa48920bfcb3de3d1116339d6a5a32070e51a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fc05bbc5d55a1f660f6eee2c02c2a257c2ebd76418c37534b9297afdbafe055(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cafefcf189cee9a89e5d5d7e15e6b04bba07e331430bd416735fab73d34b3535(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4aaefca0193ae88738d358da0c42dfa81f75762327e5a4f82ccaf0bc0f12d806(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__021b09acd59cba2b425bcf23b3cbd1610da83cd47e3a73ce1248048df39f7690(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VmwareengineNetworkPeeringTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
