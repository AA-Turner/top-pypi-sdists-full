r'''
# `azurerm_network_manager_verifier_workspace_reachability_analysis_intent`

Refer to the Terraform Registry for docs: [`azurerm_network_manager_verifier_workspace_reachability_analysis_intent`](https://registry.terraform.io/providers/hashicorp/azurerm/4.42.0/docs/resources/network_manager_verifier_workspace_reachability_analysis_intent).
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


class NetworkManagerVerifierWorkspaceReachabilityAnalysisIntent(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.networkManagerVerifierWorkspaceReachabilityAnalysisIntent.NetworkManagerVerifierWorkspaceReachabilityAnalysisIntent",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.42.0/docs/resources/network_manager_verifier_workspace_reachability_analysis_intent azurerm_network_manager_verifier_workspace_reachability_analysis_intent}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        destination_resource_id: builtins.str,
        ip_traffic: typing.Union["NetworkManagerVerifierWorkspaceReachabilityAnalysisIntentIpTraffic", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        source_resource_id: builtins.str,
        verifier_workspace_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["NetworkManagerVerifierWorkspaceReachabilityAnalysisIntentTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.42.0/docs/resources/network_manager_verifier_workspace_reachability_analysis_intent azurerm_network_manager_verifier_workspace_reachability_analysis_intent} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param destination_resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.42.0/docs/resources/network_manager_verifier_workspace_reachability_analysis_intent#destination_resource_id NetworkManagerVerifierWorkspaceReachabilityAnalysisIntent#destination_resource_id}.
        :param ip_traffic: ip_traffic block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.42.0/docs/resources/network_manager_verifier_workspace_reachability_analysis_intent#ip_traffic NetworkManagerVerifierWorkspaceReachabilityAnalysisIntent#ip_traffic}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.42.0/docs/resources/network_manager_verifier_workspace_reachability_analysis_intent#name NetworkManagerVerifierWorkspaceReachabilityAnalysisIntent#name}.
        :param source_resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.42.0/docs/resources/network_manager_verifier_workspace_reachability_analysis_intent#source_resource_id NetworkManagerVerifierWorkspaceReachabilityAnalysisIntent#source_resource_id}.
        :param verifier_workspace_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.42.0/docs/resources/network_manager_verifier_workspace_reachability_analysis_intent#verifier_workspace_id NetworkManagerVerifierWorkspaceReachabilityAnalysisIntent#verifier_workspace_id}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.42.0/docs/resources/network_manager_verifier_workspace_reachability_analysis_intent#description NetworkManagerVerifierWorkspaceReachabilityAnalysisIntent#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.42.0/docs/resources/network_manager_verifier_workspace_reachability_analysis_intent#id NetworkManagerVerifierWorkspaceReachabilityAnalysisIntent#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.42.0/docs/resources/network_manager_verifier_workspace_reachability_analysis_intent#timeouts NetworkManagerVerifierWorkspaceReachabilityAnalysisIntent#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67cea01c91b96e687666ab513281f4cf337cc897a7e25ddd19151e325fed8f39)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = NetworkManagerVerifierWorkspaceReachabilityAnalysisIntentConfig(
            destination_resource_id=destination_resource_id,
            ip_traffic=ip_traffic,
            name=name,
            source_resource_id=source_resource_id,
            verifier_workspace_id=verifier_workspace_id,
            description=description,
            id=id,
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
        '''Generates CDKTF code for importing a NetworkManagerVerifierWorkspaceReachabilityAnalysisIntent resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the NetworkManagerVerifierWorkspaceReachabilityAnalysisIntent to import.
        :param import_from_id: The id of the existing NetworkManagerVerifierWorkspaceReachabilityAnalysisIntent that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.42.0/docs/resources/network_manager_verifier_workspace_reachability_analysis_intent#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the NetworkManagerVerifierWorkspaceReachabilityAnalysisIntent to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f75f046dc83c54ac2c27c2086a4605397d0a83568ae352ab9e0819211dbb69fa)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putIpTraffic")
    def put_ip_traffic(
        self,
        *,
        destination_ips: typing.Sequence[builtins.str],
        destination_ports: typing.Sequence[builtins.str],
        protocols: typing.Sequence[builtins.str],
        source_ips: typing.Sequence[builtins.str],
        source_ports: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param destination_ips: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.42.0/docs/resources/network_manager_verifier_workspace_reachability_analysis_intent#destination_ips NetworkManagerVerifierWorkspaceReachabilityAnalysisIntent#destination_ips}.
        :param destination_ports: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.42.0/docs/resources/network_manager_verifier_workspace_reachability_analysis_intent#destination_ports NetworkManagerVerifierWorkspaceReachabilityAnalysisIntent#destination_ports}.
        :param protocols: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.42.0/docs/resources/network_manager_verifier_workspace_reachability_analysis_intent#protocols NetworkManagerVerifierWorkspaceReachabilityAnalysisIntent#protocols}.
        :param source_ips: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.42.0/docs/resources/network_manager_verifier_workspace_reachability_analysis_intent#source_ips NetworkManagerVerifierWorkspaceReachabilityAnalysisIntent#source_ips}.
        :param source_ports: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.42.0/docs/resources/network_manager_verifier_workspace_reachability_analysis_intent#source_ports NetworkManagerVerifierWorkspaceReachabilityAnalysisIntent#source_ports}.
        '''
        value = NetworkManagerVerifierWorkspaceReachabilityAnalysisIntentIpTraffic(
            destination_ips=destination_ips,
            destination_ports=destination_ports,
            protocols=protocols,
            source_ips=source_ips,
            source_ports=source_ports,
        )

        return typing.cast(None, jsii.invoke(self, "putIpTraffic", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.42.0/docs/resources/network_manager_verifier_workspace_reachability_analysis_intent#create NetworkManagerVerifierWorkspaceReachabilityAnalysisIntent#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.42.0/docs/resources/network_manager_verifier_workspace_reachability_analysis_intent#delete NetworkManagerVerifierWorkspaceReachabilityAnalysisIntent#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.42.0/docs/resources/network_manager_verifier_workspace_reachability_analysis_intent#read NetworkManagerVerifierWorkspaceReachabilityAnalysisIntent#read}.
        '''
        value = NetworkManagerVerifierWorkspaceReachabilityAnalysisIntentTimeouts(
            create=create, delete=delete, read=read
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

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
    @jsii.member(jsii_name="ipTraffic")
    def ip_traffic(
        self,
    ) -> "NetworkManagerVerifierWorkspaceReachabilityAnalysisIntentIpTrafficOutputReference":
        return typing.cast("NetworkManagerVerifierWorkspaceReachabilityAnalysisIntentIpTrafficOutputReference", jsii.get(self, "ipTraffic"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "NetworkManagerVerifierWorkspaceReachabilityAnalysisIntentTimeoutsOutputReference":
        return typing.cast("NetworkManagerVerifierWorkspaceReachabilityAnalysisIntentTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationResourceIdInput")
    def destination_resource_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationResourceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ipTrafficInput")
    def ip_traffic_input(
        self,
    ) -> typing.Optional["NetworkManagerVerifierWorkspaceReachabilityAnalysisIntentIpTraffic"]:
        return typing.cast(typing.Optional["NetworkManagerVerifierWorkspaceReachabilityAnalysisIntentIpTraffic"], jsii.get(self, "ipTrafficInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceResourceIdInput")
    def source_resource_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceResourceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "NetworkManagerVerifierWorkspaceReachabilityAnalysisIntentTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "NetworkManagerVerifierWorkspaceReachabilityAnalysisIntentTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="verifierWorkspaceIdInput")
    def verifier_workspace_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "verifierWorkspaceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3a5114ceb19fa91d154505c4eeccd120a6a283dcea42bed98af48b1cb524854)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="destinationResourceId")
    def destination_resource_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destinationResourceId"))

    @destination_resource_id.setter
    def destination_resource_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c19aa4f0a0bd19f603219a9632d12bfec34a6f8ce825c001cd67e99d6bbd57d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationResourceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f4fcffd447459fb94e14bad88b2df818bbf1fca2d84220c4db8d1e6022959a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afaf0ca5d5d6d26b44645a2b7552b8c4c0902d96e0994590c577bb231f8828de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceResourceId")
    def source_resource_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceResourceId"))

    @source_resource_id.setter
    def source_resource_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56e5a7017ae3c2211d3e6cedebbf71da6cd51854152d3968043378e0a5a8f650)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceResourceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="verifierWorkspaceId")
    def verifier_workspace_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "verifierWorkspaceId"))

    @verifier_workspace_id.setter
    def verifier_workspace_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa200bfb487c1a62c82971c909bf585646416dca1c1c92aa2be2b2a0d6394844)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "verifierWorkspaceId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.networkManagerVerifierWorkspaceReachabilityAnalysisIntent.NetworkManagerVerifierWorkspaceReachabilityAnalysisIntentConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "destination_resource_id": "destinationResourceId",
        "ip_traffic": "ipTraffic",
        "name": "name",
        "source_resource_id": "sourceResourceId",
        "verifier_workspace_id": "verifierWorkspaceId",
        "description": "description",
        "id": "id",
        "timeouts": "timeouts",
    },
)
class NetworkManagerVerifierWorkspaceReachabilityAnalysisIntentConfig(
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
        destination_resource_id: builtins.str,
        ip_traffic: typing.Union["NetworkManagerVerifierWorkspaceReachabilityAnalysisIntentIpTraffic", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        source_resource_id: builtins.str,
        verifier_workspace_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["NetworkManagerVerifierWorkspaceReachabilityAnalysisIntentTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param destination_resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.42.0/docs/resources/network_manager_verifier_workspace_reachability_analysis_intent#destination_resource_id NetworkManagerVerifierWorkspaceReachabilityAnalysisIntent#destination_resource_id}.
        :param ip_traffic: ip_traffic block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.42.0/docs/resources/network_manager_verifier_workspace_reachability_analysis_intent#ip_traffic NetworkManagerVerifierWorkspaceReachabilityAnalysisIntent#ip_traffic}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.42.0/docs/resources/network_manager_verifier_workspace_reachability_analysis_intent#name NetworkManagerVerifierWorkspaceReachabilityAnalysisIntent#name}.
        :param source_resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.42.0/docs/resources/network_manager_verifier_workspace_reachability_analysis_intent#source_resource_id NetworkManagerVerifierWorkspaceReachabilityAnalysisIntent#source_resource_id}.
        :param verifier_workspace_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.42.0/docs/resources/network_manager_verifier_workspace_reachability_analysis_intent#verifier_workspace_id NetworkManagerVerifierWorkspaceReachabilityAnalysisIntent#verifier_workspace_id}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.42.0/docs/resources/network_manager_verifier_workspace_reachability_analysis_intent#description NetworkManagerVerifierWorkspaceReachabilityAnalysisIntent#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.42.0/docs/resources/network_manager_verifier_workspace_reachability_analysis_intent#id NetworkManagerVerifierWorkspaceReachabilityAnalysisIntent#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.42.0/docs/resources/network_manager_verifier_workspace_reachability_analysis_intent#timeouts NetworkManagerVerifierWorkspaceReachabilityAnalysisIntent#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(ip_traffic, dict):
            ip_traffic = NetworkManagerVerifierWorkspaceReachabilityAnalysisIntentIpTraffic(**ip_traffic)
        if isinstance(timeouts, dict):
            timeouts = NetworkManagerVerifierWorkspaceReachabilityAnalysisIntentTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29a8d10f50837b05b765fc58a12e4226586d39dd52b26e70acfefd7b72728193)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument destination_resource_id", value=destination_resource_id, expected_type=type_hints["destination_resource_id"])
            check_type(argname="argument ip_traffic", value=ip_traffic, expected_type=type_hints["ip_traffic"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument source_resource_id", value=source_resource_id, expected_type=type_hints["source_resource_id"])
            check_type(argname="argument verifier_workspace_id", value=verifier_workspace_id, expected_type=type_hints["verifier_workspace_id"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination_resource_id": destination_resource_id,
            "ip_traffic": ip_traffic,
            "name": name,
            "source_resource_id": source_resource_id,
            "verifier_workspace_id": verifier_workspace_id,
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
    def destination_resource_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.42.0/docs/resources/network_manager_verifier_workspace_reachability_analysis_intent#destination_resource_id NetworkManagerVerifierWorkspaceReachabilityAnalysisIntent#destination_resource_id}.'''
        result = self._values.get("destination_resource_id")
        assert result is not None, "Required property 'destination_resource_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ip_traffic(
        self,
    ) -> "NetworkManagerVerifierWorkspaceReachabilityAnalysisIntentIpTraffic":
        '''ip_traffic block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.42.0/docs/resources/network_manager_verifier_workspace_reachability_analysis_intent#ip_traffic NetworkManagerVerifierWorkspaceReachabilityAnalysisIntent#ip_traffic}
        '''
        result = self._values.get("ip_traffic")
        assert result is not None, "Required property 'ip_traffic' is missing"
        return typing.cast("NetworkManagerVerifierWorkspaceReachabilityAnalysisIntentIpTraffic", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.42.0/docs/resources/network_manager_verifier_workspace_reachability_analysis_intent#name NetworkManagerVerifierWorkspaceReachabilityAnalysisIntent#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_resource_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.42.0/docs/resources/network_manager_verifier_workspace_reachability_analysis_intent#source_resource_id NetworkManagerVerifierWorkspaceReachabilityAnalysisIntent#source_resource_id}.'''
        result = self._values.get("source_resource_id")
        assert result is not None, "Required property 'source_resource_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def verifier_workspace_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.42.0/docs/resources/network_manager_verifier_workspace_reachability_analysis_intent#verifier_workspace_id NetworkManagerVerifierWorkspaceReachabilityAnalysisIntent#verifier_workspace_id}.'''
        result = self._values.get("verifier_workspace_id")
        assert result is not None, "Required property 'verifier_workspace_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.42.0/docs/resources/network_manager_verifier_workspace_reachability_analysis_intent#description NetworkManagerVerifierWorkspaceReachabilityAnalysisIntent#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.42.0/docs/resources/network_manager_verifier_workspace_reachability_analysis_intent#id NetworkManagerVerifierWorkspaceReachabilityAnalysisIntent#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["NetworkManagerVerifierWorkspaceReachabilityAnalysisIntentTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.42.0/docs/resources/network_manager_verifier_workspace_reachability_analysis_intent#timeouts NetworkManagerVerifierWorkspaceReachabilityAnalysisIntent#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["NetworkManagerVerifierWorkspaceReachabilityAnalysisIntentTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkManagerVerifierWorkspaceReachabilityAnalysisIntentConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.networkManagerVerifierWorkspaceReachabilityAnalysisIntent.NetworkManagerVerifierWorkspaceReachabilityAnalysisIntentIpTraffic",
    jsii_struct_bases=[],
    name_mapping={
        "destination_ips": "destinationIps",
        "destination_ports": "destinationPorts",
        "protocols": "protocols",
        "source_ips": "sourceIps",
        "source_ports": "sourcePorts",
    },
)
class NetworkManagerVerifierWorkspaceReachabilityAnalysisIntentIpTraffic:
    def __init__(
        self,
        *,
        destination_ips: typing.Sequence[builtins.str],
        destination_ports: typing.Sequence[builtins.str],
        protocols: typing.Sequence[builtins.str],
        source_ips: typing.Sequence[builtins.str],
        source_ports: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param destination_ips: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.42.0/docs/resources/network_manager_verifier_workspace_reachability_analysis_intent#destination_ips NetworkManagerVerifierWorkspaceReachabilityAnalysisIntent#destination_ips}.
        :param destination_ports: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.42.0/docs/resources/network_manager_verifier_workspace_reachability_analysis_intent#destination_ports NetworkManagerVerifierWorkspaceReachabilityAnalysisIntent#destination_ports}.
        :param protocols: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.42.0/docs/resources/network_manager_verifier_workspace_reachability_analysis_intent#protocols NetworkManagerVerifierWorkspaceReachabilityAnalysisIntent#protocols}.
        :param source_ips: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.42.0/docs/resources/network_manager_verifier_workspace_reachability_analysis_intent#source_ips NetworkManagerVerifierWorkspaceReachabilityAnalysisIntent#source_ips}.
        :param source_ports: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.42.0/docs/resources/network_manager_verifier_workspace_reachability_analysis_intent#source_ports NetworkManagerVerifierWorkspaceReachabilityAnalysisIntent#source_ports}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4ec5d9448776ab94815d310473160c84454182f9d24b770582ada6a09c2d3f1)
            check_type(argname="argument destination_ips", value=destination_ips, expected_type=type_hints["destination_ips"])
            check_type(argname="argument destination_ports", value=destination_ports, expected_type=type_hints["destination_ports"])
            check_type(argname="argument protocols", value=protocols, expected_type=type_hints["protocols"])
            check_type(argname="argument source_ips", value=source_ips, expected_type=type_hints["source_ips"])
            check_type(argname="argument source_ports", value=source_ports, expected_type=type_hints["source_ports"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination_ips": destination_ips,
            "destination_ports": destination_ports,
            "protocols": protocols,
            "source_ips": source_ips,
            "source_ports": source_ports,
        }

    @builtins.property
    def destination_ips(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.42.0/docs/resources/network_manager_verifier_workspace_reachability_analysis_intent#destination_ips NetworkManagerVerifierWorkspaceReachabilityAnalysisIntent#destination_ips}.'''
        result = self._values.get("destination_ips")
        assert result is not None, "Required property 'destination_ips' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def destination_ports(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.42.0/docs/resources/network_manager_verifier_workspace_reachability_analysis_intent#destination_ports NetworkManagerVerifierWorkspaceReachabilityAnalysisIntent#destination_ports}.'''
        result = self._values.get("destination_ports")
        assert result is not None, "Required property 'destination_ports' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def protocols(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.42.0/docs/resources/network_manager_verifier_workspace_reachability_analysis_intent#protocols NetworkManagerVerifierWorkspaceReachabilityAnalysisIntent#protocols}.'''
        result = self._values.get("protocols")
        assert result is not None, "Required property 'protocols' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def source_ips(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.42.0/docs/resources/network_manager_verifier_workspace_reachability_analysis_intent#source_ips NetworkManagerVerifierWorkspaceReachabilityAnalysisIntent#source_ips}.'''
        result = self._values.get("source_ips")
        assert result is not None, "Required property 'source_ips' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def source_ports(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.42.0/docs/resources/network_manager_verifier_workspace_reachability_analysis_intent#source_ports NetworkManagerVerifierWorkspaceReachabilityAnalysisIntent#source_ports}.'''
        result = self._values.get("source_ports")
        assert result is not None, "Required property 'source_ports' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkManagerVerifierWorkspaceReachabilityAnalysisIntentIpTraffic(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkManagerVerifierWorkspaceReachabilityAnalysisIntentIpTrafficOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.networkManagerVerifierWorkspaceReachabilityAnalysisIntent.NetworkManagerVerifierWorkspaceReachabilityAnalysisIntentIpTrafficOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3447b362b92db253aa97d72065cb703b4e9617f8f4c5dd2eab6483cf79d0b937)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="destinationIpsInput")
    def destination_ips_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "destinationIpsInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationPortsInput")
    def destination_ports_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "destinationPortsInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolsInput")
    def protocols_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "protocolsInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceIpsInput")
    def source_ips_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sourceIpsInput"))

    @builtins.property
    @jsii.member(jsii_name="sourcePortsInput")
    def source_ports_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sourcePortsInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationIps")
    def destination_ips(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "destinationIps"))

    @destination_ips.setter
    def destination_ips(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08f3c3b44997715bb43c941fc5961d0357dd8745de8200aedd72743adc36ca6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationIps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="destinationPorts")
    def destination_ports(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "destinationPorts"))

    @destination_ports.setter
    def destination_ports(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8f6e5214890a95a56f8aa1125bb3671b61bd381f602128b17a9cdc7bb9fc948)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationPorts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocols")
    def protocols(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "protocols"))

    @protocols.setter
    def protocols(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e7a53ad9d2691a627ac9e3d833ac3904ac273c18da4146c16e52bc9da21f205)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocols", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceIps")
    def source_ips(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sourceIps"))

    @source_ips.setter
    def source_ips(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7d54795c8faf24d32663f1bbc7bdca297f8990b926498e436d22df4d1d6edf7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceIps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourcePorts")
    def source_ports(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sourcePorts"))

    @source_ports.setter
    def source_ports(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5f2e9e7612be9ee73b15f8e6e47663c2c1ec1075526840de985830c78c28170)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourcePorts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkManagerVerifierWorkspaceReachabilityAnalysisIntentIpTraffic]:
        return typing.cast(typing.Optional[NetworkManagerVerifierWorkspaceReachabilityAnalysisIntentIpTraffic], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkManagerVerifierWorkspaceReachabilityAnalysisIntentIpTraffic],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e921093b6d1462d36b1733956f74cb1a0469e0f464da5892062377c5c0c04973)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.networkManagerVerifierWorkspaceReachabilityAnalysisIntent.NetworkManagerVerifierWorkspaceReachabilityAnalysisIntentTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "read": "read"},
)
class NetworkManagerVerifierWorkspaceReachabilityAnalysisIntentTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.42.0/docs/resources/network_manager_verifier_workspace_reachability_analysis_intent#create NetworkManagerVerifierWorkspaceReachabilityAnalysisIntent#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.42.0/docs/resources/network_manager_verifier_workspace_reachability_analysis_intent#delete NetworkManagerVerifierWorkspaceReachabilityAnalysisIntent#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.42.0/docs/resources/network_manager_verifier_workspace_reachability_analysis_intent#read NetworkManagerVerifierWorkspaceReachabilityAnalysisIntent#read}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76667a3d3cb93806fd19793a9ea7deb59fbc7896bdce9e72088986952a804239)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if read is not None:
            self._values["read"] = read

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.42.0/docs/resources/network_manager_verifier_workspace_reachability_analysis_intent#create NetworkManagerVerifierWorkspaceReachabilityAnalysisIntent#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.42.0/docs/resources/network_manager_verifier_workspace_reachability_analysis_intent#delete NetworkManagerVerifierWorkspaceReachabilityAnalysisIntent#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.42.0/docs/resources/network_manager_verifier_workspace_reachability_analysis_intent#read NetworkManagerVerifierWorkspaceReachabilityAnalysisIntent#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkManagerVerifierWorkspaceReachabilityAnalysisIntentTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkManagerVerifierWorkspaceReachabilityAnalysisIntentTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.networkManagerVerifierWorkspaceReachabilityAnalysisIntent.NetworkManagerVerifierWorkspaceReachabilityAnalysisIntentTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a7384f07726722fc59b84b87dde19d8945dce72b5b0cccd65c60ef1bf0e418c)
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
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e60c5713883203f8d1f895d2e5daf2fdc9b06472a88b5bff210426d32a0e7a58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__554e58e93215c60fe18e968f5173d462aaeeb4156d4c8143bcc49aa228b1455b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f2c66ede6cf20c26439df6df5bfedb6622df9437c9a9ef56aea6d4e205d3783)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkManagerVerifierWorkspaceReachabilityAnalysisIntentTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkManagerVerifierWorkspaceReachabilityAnalysisIntentTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkManagerVerifierWorkspaceReachabilityAnalysisIntentTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf3c9c926f0e04dd94e2253df865e54ce1076ebf69ccca5568016c30d6318304)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "NetworkManagerVerifierWorkspaceReachabilityAnalysisIntent",
    "NetworkManagerVerifierWorkspaceReachabilityAnalysisIntentConfig",
    "NetworkManagerVerifierWorkspaceReachabilityAnalysisIntentIpTraffic",
    "NetworkManagerVerifierWorkspaceReachabilityAnalysisIntentIpTrafficOutputReference",
    "NetworkManagerVerifierWorkspaceReachabilityAnalysisIntentTimeouts",
    "NetworkManagerVerifierWorkspaceReachabilityAnalysisIntentTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__67cea01c91b96e687666ab513281f4cf337cc897a7e25ddd19151e325fed8f39(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    destination_resource_id: builtins.str,
    ip_traffic: typing.Union[NetworkManagerVerifierWorkspaceReachabilityAnalysisIntentIpTraffic, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    source_resource_id: builtins.str,
    verifier_workspace_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[NetworkManagerVerifierWorkspaceReachabilityAnalysisIntentTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__f75f046dc83c54ac2c27c2086a4605397d0a83568ae352ab9e0819211dbb69fa(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3a5114ceb19fa91d154505c4eeccd120a6a283dcea42bed98af48b1cb524854(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c19aa4f0a0bd19f603219a9632d12bfec34a6f8ce825c001cd67e99d6bbd57d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f4fcffd447459fb94e14bad88b2df818bbf1fca2d84220c4db8d1e6022959a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afaf0ca5d5d6d26b44645a2b7552b8c4c0902d96e0994590c577bb231f8828de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56e5a7017ae3c2211d3e6cedebbf71da6cd51854152d3968043378e0a5a8f650(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa200bfb487c1a62c82971c909bf585646416dca1c1c92aa2be2b2a0d6394844(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29a8d10f50837b05b765fc58a12e4226586d39dd52b26e70acfefd7b72728193(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    destination_resource_id: builtins.str,
    ip_traffic: typing.Union[NetworkManagerVerifierWorkspaceReachabilityAnalysisIntentIpTraffic, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    source_resource_id: builtins.str,
    verifier_workspace_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[NetworkManagerVerifierWorkspaceReachabilityAnalysisIntentTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4ec5d9448776ab94815d310473160c84454182f9d24b770582ada6a09c2d3f1(
    *,
    destination_ips: typing.Sequence[builtins.str],
    destination_ports: typing.Sequence[builtins.str],
    protocols: typing.Sequence[builtins.str],
    source_ips: typing.Sequence[builtins.str],
    source_ports: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3447b362b92db253aa97d72065cb703b4e9617f8f4c5dd2eab6483cf79d0b937(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08f3c3b44997715bb43c941fc5961d0357dd8745de8200aedd72743adc36ca6a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8f6e5214890a95a56f8aa1125bb3671b61bd381f602128b17a9cdc7bb9fc948(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e7a53ad9d2691a627ac9e3d833ac3904ac273c18da4146c16e52bc9da21f205(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7d54795c8faf24d32663f1bbc7bdca297f8990b926498e436d22df4d1d6edf7(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5f2e9e7612be9ee73b15f8e6e47663c2c1ec1075526840de985830c78c28170(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e921093b6d1462d36b1733956f74cb1a0469e0f464da5892062377c5c0c04973(
    value: typing.Optional[NetworkManagerVerifierWorkspaceReachabilityAnalysisIntentIpTraffic],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76667a3d3cb93806fd19793a9ea7deb59fbc7896bdce9e72088986952a804239(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a7384f07726722fc59b84b87dde19d8945dce72b5b0cccd65c60ef1bf0e418c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e60c5713883203f8d1f895d2e5daf2fdc9b06472a88b5bff210426d32a0e7a58(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__554e58e93215c60fe18e968f5173d462aaeeb4156d4c8143bcc49aa228b1455b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f2c66ede6cf20c26439df6df5bfedb6622df9437c9a9ef56aea6d4e205d3783(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf3c9c926f0e04dd94e2253df865e54ce1076ebf69ccca5568016c30d6318304(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkManagerVerifierWorkspaceReachabilityAnalysisIntentTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
