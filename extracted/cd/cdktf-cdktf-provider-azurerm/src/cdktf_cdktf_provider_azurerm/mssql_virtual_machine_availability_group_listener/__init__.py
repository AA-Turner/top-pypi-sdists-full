r'''
# `azurerm_mssql_virtual_machine_availability_group_listener`

Refer to the Terraform Registry for docs: [`azurerm_mssql_virtual_machine_availability_group_listener`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_availability_group_listener).
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


class MssqlVirtualMachineAvailabilityGroupListener(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mssqlVirtualMachineAvailabilityGroupListener.MssqlVirtualMachineAvailabilityGroupListener",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_availability_group_listener azurerm_mssql_virtual_machine_availability_group_listener}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        replica: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MssqlVirtualMachineAvailabilityGroupListenerReplica", typing.Dict[builtins.str, typing.Any]]]],
        sql_virtual_machine_group_id: builtins.str,
        availability_group_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        load_balancer_configuration: typing.Optional[typing.Union["MssqlVirtualMachineAvailabilityGroupListenerLoadBalancerConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        multi_subnet_ip_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MssqlVirtualMachineAvailabilityGroupListenerMultiSubnetIpConfiguration", typing.Dict[builtins.str, typing.Any]]]]] = None,
        port: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["MssqlVirtualMachineAvailabilityGroupListenerTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_availability_group_listener azurerm_mssql_virtual_machine_availability_group_listener} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_availability_group_listener#name MssqlVirtualMachineAvailabilityGroupListener#name}.
        :param replica: replica block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_availability_group_listener#replica MssqlVirtualMachineAvailabilityGroupListener#replica}
        :param sql_virtual_machine_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_availability_group_listener#sql_virtual_machine_group_id MssqlVirtualMachineAvailabilityGroupListener#sql_virtual_machine_group_id}.
        :param availability_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_availability_group_listener#availability_group_name MssqlVirtualMachineAvailabilityGroupListener#availability_group_name}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_availability_group_listener#id MssqlVirtualMachineAvailabilityGroupListener#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param load_balancer_configuration: load_balancer_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_availability_group_listener#load_balancer_configuration MssqlVirtualMachineAvailabilityGroupListener#load_balancer_configuration}
        :param multi_subnet_ip_configuration: multi_subnet_ip_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_availability_group_listener#multi_subnet_ip_configuration MssqlVirtualMachineAvailabilityGroupListener#multi_subnet_ip_configuration}
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_availability_group_listener#port MssqlVirtualMachineAvailabilityGroupListener#port}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_availability_group_listener#timeouts MssqlVirtualMachineAvailabilityGroupListener#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97908daabeb7a950a73afcbeb72768c1b1397d183af007a4310c27c6dc8a5ba0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = MssqlVirtualMachineAvailabilityGroupListenerConfig(
            name=name,
            replica=replica,
            sql_virtual_machine_group_id=sql_virtual_machine_group_id,
            availability_group_name=availability_group_name,
            id=id,
            load_balancer_configuration=load_balancer_configuration,
            multi_subnet_ip_configuration=multi_subnet_ip_configuration,
            port=port,
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
        '''Generates CDKTF code for importing a MssqlVirtualMachineAvailabilityGroupListener resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the MssqlVirtualMachineAvailabilityGroupListener to import.
        :param import_from_id: The id of the existing MssqlVirtualMachineAvailabilityGroupListener that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_availability_group_listener#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the MssqlVirtualMachineAvailabilityGroupListener to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d806fdf4f3683a99a66b1569d7aed8af433d2f2d66a6a841edeb03dc213b29d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putLoadBalancerConfiguration")
    def put_load_balancer_configuration(
        self,
        *,
        load_balancer_id: builtins.str,
        private_ip_address: builtins.str,
        probe_port: jsii.Number,
        sql_virtual_machine_ids: typing.Sequence[builtins.str],
        subnet_id: builtins.str,
    ) -> None:
        '''
        :param load_balancer_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_availability_group_listener#load_balancer_id MssqlVirtualMachineAvailabilityGroupListener#load_balancer_id}.
        :param private_ip_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_availability_group_listener#private_ip_address MssqlVirtualMachineAvailabilityGroupListener#private_ip_address}.
        :param probe_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_availability_group_listener#probe_port MssqlVirtualMachineAvailabilityGroupListener#probe_port}.
        :param sql_virtual_machine_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_availability_group_listener#sql_virtual_machine_ids MssqlVirtualMachineAvailabilityGroupListener#sql_virtual_machine_ids}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_availability_group_listener#subnet_id MssqlVirtualMachineAvailabilityGroupListener#subnet_id}.
        '''
        value = MssqlVirtualMachineAvailabilityGroupListenerLoadBalancerConfiguration(
            load_balancer_id=load_balancer_id,
            private_ip_address=private_ip_address,
            probe_port=probe_port,
            sql_virtual_machine_ids=sql_virtual_machine_ids,
            subnet_id=subnet_id,
        )

        return typing.cast(None, jsii.invoke(self, "putLoadBalancerConfiguration", [value]))

    @jsii.member(jsii_name="putMultiSubnetIpConfiguration")
    def put_multi_subnet_ip_configuration(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MssqlVirtualMachineAvailabilityGroupListenerMultiSubnetIpConfiguration", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87b45c42447d3841cd1110700ab7401741d8bcbd718b55320f4cc74893eb6bd7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMultiSubnetIpConfiguration", [value]))

    @jsii.member(jsii_name="putReplica")
    def put_replica(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MssqlVirtualMachineAvailabilityGroupListenerReplica", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92ac9cbee8e56f0fd24c16aa45653c0f289b92737240ee668bb9104d09214ac7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putReplica", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_availability_group_listener#create MssqlVirtualMachineAvailabilityGroupListener#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_availability_group_listener#delete MssqlVirtualMachineAvailabilityGroupListener#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_availability_group_listener#read MssqlVirtualMachineAvailabilityGroupListener#read}.
        '''
        value = MssqlVirtualMachineAvailabilityGroupListenerTimeouts(
            create=create, delete=delete, read=read
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAvailabilityGroupName")
    def reset_availability_group_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvailabilityGroupName", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLoadBalancerConfiguration")
    def reset_load_balancer_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoadBalancerConfiguration", []))

    @jsii.member(jsii_name="resetMultiSubnetIpConfiguration")
    def reset_multi_subnet_ip_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMultiSubnetIpConfiguration", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

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
    @jsii.member(jsii_name="loadBalancerConfiguration")
    def load_balancer_configuration(
        self,
    ) -> "MssqlVirtualMachineAvailabilityGroupListenerLoadBalancerConfigurationOutputReference":
        return typing.cast("MssqlVirtualMachineAvailabilityGroupListenerLoadBalancerConfigurationOutputReference", jsii.get(self, "loadBalancerConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="multiSubnetIpConfiguration")
    def multi_subnet_ip_configuration(
        self,
    ) -> "MssqlVirtualMachineAvailabilityGroupListenerMultiSubnetIpConfigurationList":
        return typing.cast("MssqlVirtualMachineAvailabilityGroupListenerMultiSubnetIpConfigurationList", jsii.get(self, "multiSubnetIpConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="replica")
    def replica(self) -> "MssqlVirtualMachineAvailabilityGroupListenerReplicaList":
        return typing.cast("MssqlVirtualMachineAvailabilityGroupListenerReplicaList", jsii.get(self, "replica"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "MssqlVirtualMachineAvailabilityGroupListenerTimeoutsOutputReference":
        return typing.cast("MssqlVirtualMachineAvailabilityGroupListenerTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="availabilityGroupNameInput")
    def availability_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "availabilityGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancerConfigurationInput")
    def load_balancer_configuration_input(
        self,
    ) -> typing.Optional["MssqlVirtualMachineAvailabilityGroupListenerLoadBalancerConfiguration"]:
        return typing.cast(typing.Optional["MssqlVirtualMachineAvailabilityGroupListenerLoadBalancerConfiguration"], jsii.get(self, "loadBalancerConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="multiSubnetIpConfigurationInput")
    def multi_subnet_ip_configuration_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MssqlVirtualMachineAvailabilityGroupListenerMultiSubnetIpConfiguration"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MssqlVirtualMachineAvailabilityGroupListenerMultiSubnetIpConfiguration"]]], jsii.get(self, "multiSubnetIpConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="replicaInput")
    def replica_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MssqlVirtualMachineAvailabilityGroupListenerReplica"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MssqlVirtualMachineAvailabilityGroupListenerReplica"]]], jsii.get(self, "replicaInput"))

    @builtins.property
    @jsii.member(jsii_name="sqlVirtualMachineGroupIdInput")
    def sql_virtual_machine_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sqlVirtualMachineGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "MssqlVirtualMachineAvailabilityGroupListenerTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "MssqlVirtualMachineAvailabilityGroupListenerTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="availabilityGroupName")
    def availability_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availabilityGroupName"))

    @availability_group_name.setter
    def availability_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__833fa5bf2306b7ac27226c190025ae15679bc90fe0bb7f6afa9a8ad862393c7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f9b2b724df10e26138c72ce1a0593a58eb5f466d76c53bf13ba47435d74b927)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__098fe0e820ab45a9f211214c0c58f50fffc4e4a6f84c14047a09bb7d36fd3898)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d89bd2704cd1470881613372945dcba9ab20e9715bf5fdeed9563068d366fe49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sqlVirtualMachineGroupId")
    def sql_virtual_machine_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sqlVirtualMachineGroupId"))

    @sql_virtual_machine_group_id.setter
    def sql_virtual_machine_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84d670bb24c22a78d54c1d9c614878aee44c1437866af8c8e9f159b1e9584205)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sqlVirtualMachineGroupId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mssqlVirtualMachineAvailabilityGroupListener.MssqlVirtualMachineAvailabilityGroupListenerConfig",
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
        "replica": "replica",
        "sql_virtual_machine_group_id": "sqlVirtualMachineGroupId",
        "availability_group_name": "availabilityGroupName",
        "id": "id",
        "load_balancer_configuration": "loadBalancerConfiguration",
        "multi_subnet_ip_configuration": "multiSubnetIpConfiguration",
        "port": "port",
        "timeouts": "timeouts",
    },
)
class MssqlVirtualMachineAvailabilityGroupListenerConfig(
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
        name: builtins.str,
        replica: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MssqlVirtualMachineAvailabilityGroupListenerReplica", typing.Dict[builtins.str, typing.Any]]]],
        sql_virtual_machine_group_id: builtins.str,
        availability_group_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        load_balancer_configuration: typing.Optional[typing.Union["MssqlVirtualMachineAvailabilityGroupListenerLoadBalancerConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        multi_subnet_ip_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MssqlVirtualMachineAvailabilityGroupListenerMultiSubnetIpConfiguration", typing.Dict[builtins.str, typing.Any]]]]] = None,
        port: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["MssqlVirtualMachineAvailabilityGroupListenerTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_availability_group_listener#name MssqlVirtualMachineAvailabilityGroupListener#name}.
        :param replica: replica block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_availability_group_listener#replica MssqlVirtualMachineAvailabilityGroupListener#replica}
        :param sql_virtual_machine_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_availability_group_listener#sql_virtual_machine_group_id MssqlVirtualMachineAvailabilityGroupListener#sql_virtual_machine_group_id}.
        :param availability_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_availability_group_listener#availability_group_name MssqlVirtualMachineAvailabilityGroupListener#availability_group_name}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_availability_group_listener#id MssqlVirtualMachineAvailabilityGroupListener#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param load_balancer_configuration: load_balancer_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_availability_group_listener#load_balancer_configuration MssqlVirtualMachineAvailabilityGroupListener#load_balancer_configuration}
        :param multi_subnet_ip_configuration: multi_subnet_ip_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_availability_group_listener#multi_subnet_ip_configuration MssqlVirtualMachineAvailabilityGroupListener#multi_subnet_ip_configuration}
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_availability_group_listener#port MssqlVirtualMachineAvailabilityGroupListener#port}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_availability_group_listener#timeouts MssqlVirtualMachineAvailabilityGroupListener#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(load_balancer_configuration, dict):
            load_balancer_configuration = MssqlVirtualMachineAvailabilityGroupListenerLoadBalancerConfiguration(**load_balancer_configuration)
        if isinstance(timeouts, dict):
            timeouts = MssqlVirtualMachineAvailabilityGroupListenerTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46a5ac80780fbbb3ee49fabf85efceaca4a653a385bc40677b2b88817a958650)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument replica", value=replica, expected_type=type_hints["replica"])
            check_type(argname="argument sql_virtual_machine_group_id", value=sql_virtual_machine_group_id, expected_type=type_hints["sql_virtual_machine_group_id"])
            check_type(argname="argument availability_group_name", value=availability_group_name, expected_type=type_hints["availability_group_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument load_balancer_configuration", value=load_balancer_configuration, expected_type=type_hints["load_balancer_configuration"])
            check_type(argname="argument multi_subnet_ip_configuration", value=multi_subnet_ip_configuration, expected_type=type_hints["multi_subnet_ip_configuration"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "replica": replica,
            "sql_virtual_machine_group_id": sql_virtual_machine_group_id,
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
        if availability_group_name is not None:
            self._values["availability_group_name"] = availability_group_name
        if id is not None:
            self._values["id"] = id
        if load_balancer_configuration is not None:
            self._values["load_balancer_configuration"] = load_balancer_configuration
        if multi_subnet_ip_configuration is not None:
            self._values["multi_subnet_ip_configuration"] = multi_subnet_ip_configuration
        if port is not None:
            self._values["port"] = port
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_availability_group_listener#name MssqlVirtualMachineAvailabilityGroupListener#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def replica(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MssqlVirtualMachineAvailabilityGroupListenerReplica"]]:
        '''replica block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_availability_group_listener#replica MssqlVirtualMachineAvailabilityGroupListener#replica}
        '''
        result = self._values.get("replica")
        assert result is not None, "Required property 'replica' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MssqlVirtualMachineAvailabilityGroupListenerReplica"]], result)

    @builtins.property
    def sql_virtual_machine_group_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_availability_group_listener#sql_virtual_machine_group_id MssqlVirtualMachineAvailabilityGroupListener#sql_virtual_machine_group_id}.'''
        result = self._values.get("sql_virtual_machine_group_id")
        assert result is not None, "Required property 'sql_virtual_machine_group_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def availability_group_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_availability_group_listener#availability_group_name MssqlVirtualMachineAvailabilityGroupListener#availability_group_name}.'''
        result = self._values.get("availability_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_availability_group_listener#id MssqlVirtualMachineAvailabilityGroupListener#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def load_balancer_configuration(
        self,
    ) -> typing.Optional["MssqlVirtualMachineAvailabilityGroupListenerLoadBalancerConfiguration"]:
        '''load_balancer_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_availability_group_listener#load_balancer_configuration MssqlVirtualMachineAvailabilityGroupListener#load_balancer_configuration}
        '''
        result = self._values.get("load_balancer_configuration")
        return typing.cast(typing.Optional["MssqlVirtualMachineAvailabilityGroupListenerLoadBalancerConfiguration"], result)

    @builtins.property
    def multi_subnet_ip_configuration(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MssqlVirtualMachineAvailabilityGroupListenerMultiSubnetIpConfiguration"]]]:
        '''multi_subnet_ip_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_availability_group_listener#multi_subnet_ip_configuration MssqlVirtualMachineAvailabilityGroupListener#multi_subnet_ip_configuration}
        '''
        result = self._values.get("multi_subnet_ip_configuration")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MssqlVirtualMachineAvailabilityGroupListenerMultiSubnetIpConfiguration"]]], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_availability_group_listener#port MssqlVirtualMachineAvailabilityGroupListener#port}.'''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["MssqlVirtualMachineAvailabilityGroupListenerTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_availability_group_listener#timeouts MssqlVirtualMachineAvailabilityGroupListener#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["MssqlVirtualMachineAvailabilityGroupListenerTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MssqlVirtualMachineAvailabilityGroupListenerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mssqlVirtualMachineAvailabilityGroupListener.MssqlVirtualMachineAvailabilityGroupListenerLoadBalancerConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "load_balancer_id": "loadBalancerId",
        "private_ip_address": "privateIpAddress",
        "probe_port": "probePort",
        "sql_virtual_machine_ids": "sqlVirtualMachineIds",
        "subnet_id": "subnetId",
    },
)
class MssqlVirtualMachineAvailabilityGroupListenerLoadBalancerConfiguration:
    def __init__(
        self,
        *,
        load_balancer_id: builtins.str,
        private_ip_address: builtins.str,
        probe_port: jsii.Number,
        sql_virtual_machine_ids: typing.Sequence[builtins.str],
        subnet_id: builtins.str,
    ) -> None:
        '''
        :param load_balancer_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_availability_group_listener#load_balancer_id MssqlVirtualMachineAvailabilityGroupListener#load_balancer_id}.
        :param private_ip_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_availability_group_listener#private_ip_address MssqlVirtualMachineAvailabilityGroupListener#private_ip_address}.
        :param probe_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_availability_group_listener#probe_port MssqlVirtualMachineAvailabilityGroupListener#probe_port}.
        :param sql_virtual_machine_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_availability_group_listener#sql_virtual_machine_ids MssqlVirtualMachineAvailabilityGroupListener#sql_virtual_machine_ids}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_availability_group_listener#subnet_id MssqlVirtualMachineAvailabilityGroupListener#subnet_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32c314fa09a52e0f5525d2854170283470095fde25ac69e8bc620edb1c61eb17)
            check_type(argname="argument load_balancer_id", value=load_balancer_id, expected_type=type_hints["load_balancer_id"])
            check_type(argname="argument private_ip_address", value=private_ip_address, expected_type=type_hints["private_ip_address"])
            check_type(argname="argument probe_port", value=probe_port, expected_type=type_hints["probe_port"])
            check_type(argname="argument sql_virtual_machine_ids", value=sql_virtual_machine_ids, expected_type=type_hints["sql_virtual_machine_ids"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "load_balancer_id": load_balancer_id,
            "private_ip_address": private_ip_address,
            "probe_port": probe_port,
            "sql_virtual_machine_ids": sql_virtual_machine_ids,
            "subnet_id": subnet_id,
        }

    @builtins.property
    def load_balancer_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_availability_group_listener#load_balancer_id MssqlVirtualMachineAvailabilityGroupListener#load_balancer_id}.'''
        result = self._values.get("load_balancer_id")
        assert result is not None, "Required property 'load_balancer_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def private_ip_address(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_availability_group_listener#private_ip_address MssqlVirtualMachineAvailabilityGroupListener#private_ip_address}.'''
        result = self._values.get("private_ip_address")
        assert result is not None, "Required property 'private_ip_address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def probe_port(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_availability_group_listener#probe_port MssqlVirtualMachineAvailabilityGroupListener#probe_port}.'''
        result = self._values.get("probe_port")
        assert result is not None, "Required property 'probe_port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def sql_virtual_machine_ids(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_availability_group_listener#sql_virtual_machine_ids MssqlVirtualMachineAvailabilityGroupListener#sql_virtual_machine_ids}.'''
        result = self._values.get("sql_virtual_machine_ids")
        assert result is not None, "Required property 'sql_virtual_machine_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def subnet_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_availability_group_listener#subnet_id MssqlVirtualMachineAvailabilityGroupListener#subnet_id}.'''
        result = self._values.get("subnet_id")
        assert result is not None, "Required property 'subnet_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MssqlVirtualMachineAvailabilityGroupListenerLoadBalancerConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MssqlVirtualMachineAvailabilityGroupListenerLoadBalancerConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mssqlVirtualMachineAvailabilityGroupListener.MssqlVirtualMachineAvailabilityGroupListenerLoadBalancerConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__16c1aae7e0d69923895b47b72a13acbd5bf9b4fedd724897c9db5f31df5c3577)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="loadBalancerIdInput")
    def load_balancer_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "loadBalancerIdInput"))

    @builtins.property
    @jsii.member(jsii_name="privateIpAddressInput")
    def private_ip_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateIpAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="probePortInput")
    def probe_port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "probePortInput"))

    @builtins.property
    @jsii.member(jsii_name="sqlVirtualMachineIdsInput")
    def sql_virtual_machine_ids_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sqlVirtualMachineIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetIdInput")
    def subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancerId")
    def load_balancer_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loadBalancerId"))

    @load_balancer_id.setter
    def load_balancer_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__686456979c79658ad52a9aa7e863cc048d3fced3eabad70bd631362405cebbac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loadBalancerId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateIpAddress")
    def private_ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateIpAddress"))

    @private_ip_address.setter
    def private_ip_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8de94954660521c1eff29d7a71649da5e52ef174a618e9284ae209513ddaaa82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateIpAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="probePort")
    def probe_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "probePort"))

    @probe_port.setter
    def probe_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fddd1ad728f6537ef940987d6370d8aa2e4c561bf93e44c64de05fe2a39e4166)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "probePort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sqlVirtualMachineIds")
    def sql_virtual_machine_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sqlVirtualMachineIds"))

    @sql_virtual_machine_ids.setter
    def sql_virtual_machine_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f092df768bb999c6f25a12394e3d52c67cc627447f3eb03ea578ba5cfb20e070)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sqlVirtualMachineIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6aaee521e5877b18c1c16d7c4b9d501a62e9608b4ee15033e6f50f083ca83370)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MssqlVirtualMachineAvailabilityGroupListenerLoadBalancerConfiguration]:
        return typing.cast(typing.Optional[MssqlVirtualMachineAvailabilityGroupListenerLoadBalancerConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MssqlVirtualMachineAvailabilityGroupListenerLoadBalancerConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ef6b0dcc573e5d8fb545d8f273a4175ad6c4c28039f1461fa8829bc29390be3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mssqlVirtualMachineAvailabilityGroupListener.MssqlVirtualMachineAvailabilityGroupListenerMultiSubnetIpConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "private_ip_address": "privateIpAddress",
        "sql_virtual_machine_id": "sqlVirtualMachineId",
        "subnet_id": "subnetId",
    },
)
class MssqlVirtualMachineAvailabilityGroupListenerMultiSubnetIpConfiguration:
    def __init__(
        self,
        *,
        private_ip_address: builtins.str,
        sql_virtual_machine_id: builtins.str,
        subnet_id: builtins.str,
    ) -> None:
        '''
        :param private_ip_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_availability_group_listener#private_ip_address MssqlVirtualMachineAvailabilityGroupListener#private_ip_address}.
        :param sql_virtual_machine_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_availability_group_listener#sql_virtual_machine_id MssqlVirtualMachineAvailabilityGroupListener#sql_virtual_machine_id}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_availability_group_listener#subnet_id MssqlVirtualMachineAvailabilityGroupListener#subnet_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd419241ee51db414e3920d22c6853aec1c48d90f25403d96810bc1f01a3b3b0)
            check_type(argname="argument private_ip_address", value=private_ip_address, expected_type=type_hints["private_ip_address"])
            check_type(argname="argument sql_virtual_machine_id", value=sql_virtual_machine_id, expected_type=type_hints["sql_virtual_machine_id"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "private_ip_address": private_ip_address,
            "sql_virtual_machine_id": sql_virtual_machine_id,
            "subnet_id": subnet_id,
        }

    @builtins.property
    def private_ip_address(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_availability_group_listener#private_ip_address MssqlVirtualMachineAvailabilityGroupListener#private_ip_address}.'''
        result = self._values.get("private_ip_address")
        assert result is not None, "Required property 'private_ip_address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sql_virtual_machine_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_availability_group_listener#sql_virtual_machine_id MssqlVirtualMachineAvailabilityGroupListener#sql_virtual_machine_id}.'''
        result = self._values.get("sql_virtual_machine_id")
        assert result is not None, "Required property 'sql_virtual_machine_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subnet_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_availability_group_listener#subnet_id MssqlVirtualMachineAvailabilityGroupListener#subnet_id}.'''
        result = self._values.get("subnet_id")
        assert result is not None, "Required property 'subnet_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MssqlVirtualMachineAvailabilityGroupListenerMultiSubnetIpConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MssqlVirtualMachineAvailabilityGroupListenerMultiSubnetIpConfigurationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mssqlVirtualMachineAvailabilityGroupListener.MssqlVirtualMachineAvailabilityGroupListenerMultiSubnetIpConfigurationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4043a822317c101ff8727e05cd96e485f5f84afdf96e8d4d98f367ae4317f7c0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MssqlVirtualMachineAvailabilityGroupListenerMultiSubnetIpConfigurationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16e6542ecfe8ba15c1c6e2748d1551ccc048810a74b76424d1623150aae79f31)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MssqlVirtualMachineAvailabilityGroupListenerMultiSubnetIpConfigurationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__010959af5f009a62db74d920da1d7503c5509a5b7e32c96ade1565a60c391f2a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__66c008efff2253428a3961882b365730a3015516018d4663e6713daa7bda007b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f59ab415684cde0060352efe917341fdf08825c8ae18a82c757fb69e14e51efa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MssqlVirtualMachineAvailabilityGroupListenerMultiSubnetIpConfiguration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MssqlVirtualMachineAvailabilityGroupListenerMultiSubnetIpConfiguration]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MssqlVirtualMachineAvailabilityGroupListenerMultiSubnetIpConfiguration]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1df0a9e40d3e8649d094ef1b25d6a8d150d2320a80d22ce76024e4251fa7655e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MssqlVirtualMachineAvailabilityGroupListenerMultiSubnetIpConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mssqlVirtualMachineAvailabilityGroupListener.MssqlVirtualMachineAvailabilityGroupListenerMultiSubnetIpConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c0dc5aab36e1a1d6ae334f8f514fbdfecb8b14724f72ba62f4e91731af7be026)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="privateIpAddressInput")
    def private_ip_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateIpAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="sqlVirtualMachineIdInput")
    def sql_virtual_machine_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sqlVirtualMachineIdInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetIdInput")
    def subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="privateIpAddress")
    def private_ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateIpAddress"))

    @private_ip_address.setter
    def private_ip_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7d6daba7657dfbacdfd58d4b61bf19117b4c01f1eff16a781f7390f2aa5ff06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateIpAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sqlVirtualMachineId")
    def sql_virtual_machine_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sqlVirtualMachineId"))

    @sql_virtual_machine_id.setter
    def sql_virtual_machine_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46310a65b6cc6146d825723c64a2208d45619d0147d91cedc7044a17c7b6d644)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sqlVirtualMachineId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f06b79dff0d7fe848d0008941ccf846d8ec4a630699edd318e0c2d6f018a147d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MssqlVirtualMachineAvailabilityGroupListenerMultiSubnetIpConfiguration]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MssqlVirtualMachineAvailabilityGroupListenerMultiSubnetIpConfiguration]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MssqlVirtualMachineAvailabilityGroupListenerMultiSubnetIpConfiguration]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c614e863121160b82ac90311b328f6e32db85b974e0cb3277b3faae3537b2675)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mssqlVirtualMachineAvailabilityGroupListener.MssqlVirtualMachineAvailabilityGroupListenerReplica",
    jsii_struct_bases=[],
    name_mapping={
        "commit": "commit",
        "failover_mode": "failoverMode",
        "readable_secondary": "readableSecondary",
        "role": "role",
        "sql_virtual_machine_id": "sqlVirtualMachineId",
    },
)
class MssqlVirtualMachineAvailabilityGroupListenerReplica:
    def __init__(
        self,
        *,
        commit: builtins.str,
        failover_mode: builtins.str,
        readable_secondary: builtins.str,
        role: builtins.str,
        sql_virtual_machine_id: builtins.str,
    ) -> None:
        '''
        :param commit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_availability_group_listener#commit MssqlVirtualMachineAvailabilityGroupListener#commit}.
        :param failover_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_availability_group_listener#failover_mode MssqlVirtualMachineAvailabilityGroupListener#failover_mode}.
        :param readable_secondary: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_availability_group_listener#readable_secondary MssqlVirtualMachineAvailabilityGroupListener#readable_secondary}.
        :param role: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_availability_group_listener#role MssqlVirtualMachineAvailabilityGroupListener#role}.
        :param sql_virtual_machine_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_availability_group_listener#sql_virtual_machine_id MssqlVirtualMachineAvailabilityGroupListener#sql_virtual_machine_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f79546e8bf9575acef6ccbfecde035b574ea55ad27168541e165e72d9c06bc17)
            check_type(argname="argument commit", value=commit, expected_type=type_hints["commit"])
            check_type(argname="argument failover_mode", value=failover_mode, expected_type=type_hints["failover_mode"])
            check_type(argname="argument readable_secondary", value=readable_secondary, expected_type=type_hints["readable_secondary"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument sql_virtual_machine_id", value=sql_virtual_machine_id, expected_type=type_hints["sql_virtual_machine_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "commit": commit,
            "failover_mode": failover_mode,
            "readable_secondary": readable_secondary,
            "role": role,
            "sql_virtual_machine_id": sql_virtual_machine_id,
        }

    @builtins.property
    def commit(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_availability_group_listener#commit MssqlVirtualMachineAvailabilityGroupListener#commit}.'''
        result = self._values.get("commit")
        assert result is not None, "Required property 'commit' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def failover_mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_availability_group_listener#failover_mode MssqlVirtualMachineAvailabilityGroupListener#failover_mode}.'''
        result = self._values.get("failover_mode")
        assert result is not None, "Required property 'failover_mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def readable_secondary(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_availability_group_listener#readable_secondary MssqlVirtualMachineAvailabilityGroupListener#readable_secondary}.'''
        result = self._values.get("readable_secondary")
        assert result is not None, "Required property 'readable_secondary' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_availability_group_listener#role MssqlVirtualMachineAvailabilityGroupListener#role}.'''
        result = self._values.get("role")
        assert result is not None, "Required property 'role' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sql_virtual_machine_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_availability_group_listener#sql_virtual_machine_id MssqlVirtualMachineAvailabilityGroupListener#sql_virtual_machine_id}.'''
        result = self._values.get("sql_virtual_machine_id")
        assert result is not None, "Required property 'sql_virtual_machine_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MssqlVirtualMachineAvailabilityGroupListenerReplica(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MssqlVirtualMachineAvailabilityGroupListenerReplicaList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mssqlVirtualMachineAvailabilityGroupListener.MssqlVirtualMachineAvailabilityGroupListenerReplicaList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b85edcd0426036ff49f456d3cfe7c4425a0560d2246f9e9dec5c19a958a1a3aa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MssqlVirtualMachineAvailabilityGroupListenerReplicaOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f23f95730158dd5766dc97e2970f9feccfbd77a63e72d3e185a01e7d4c316d38)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MssqlVirtualMachineAvailabilityGroupListenerReplicaOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f57b33ac8549ef68bb00e9c490b0f94b1e86d8e2d29e035692957b617a45471)
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
            type_hints = typing.get_type_hints(_typecheckingstub__76df63066a05edb03c2bd716207880bd39e22f8a54ad3f84c8ebaf2a420527e0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__290c3a95934b048d9b7004114fe42794e830434ef37552dd5c2643acbd648ab5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MssqlVirtualMachineAvailabilityGroupListenerReplica]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MssqlVirtualMachineAvailabilityGroupListenerReplica]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MssqlVirtualMachineAvailabilityGroupListenerReplica]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1a1620096c48b4e93c680214abb251bbd71c34867c130408a67598631a42314)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MssqlVirtualMachineAvailabilityGroupListenerReplicaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mssqlVirtualMachineAvailabilityGroupListener.MssqlVirtualMachineAvailabilityGroupListenerReplicaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a10632b220ca76dc43b24b9087c1454f1071f0a18eea42892c3d6d162ae975e2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="commitInput")
    def commit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commitInput"))

    @builtins.property
    @jsii.member(jsii_name="failoverModeInput")
    def failover_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "failoverModeInput"))

    @builtins.property
    @jsii.member(jsii_name="readableSecondaryInput")
    def readable_secondary_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "readableSecondaryInput"))

    @builtins.property
    @jsii.member(jsii_name="roleInput")
    def role_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleInput"))

    @builtins.property
    @jsii.member(jsii_name="sqlVirtualMachineIdInput")
    def sql_virtual_machine_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sqlVirtualMachineIdInput"))

    @builtins.property
    @jsii.member(jsii_name="commit")
    def commit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "commit"))

    @commit.setter
    def commit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa56c14c896a4f75fa74cabd30bedb8a78565468695fcd7b9829b0eb930405d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "commit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="failoverMode")
    def failover_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "failoverMode"))

    @failover_mode.setter
    def failover_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__816aa9d3f7708b01eb36bb4ba6445dd3d04fbed8f85512e0b6d8ab4c7ceeea7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failoverMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="readableSecondary")
    def readable_secondary(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "readableSecondary"))

    @readable_secondary.setter
    def readable_secondary(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb59c8a2063cbb9b33b43bf5ae27eb9804380307df80dade0cca33cd53b2ee41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "readableSecondary", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "role"))

    @role.setter
    def role(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38f77723be16fa73c39af5eb101dcbcd7ae6ca32f4ee2402ddeb7676602ac620)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "role", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sqlVirtualMachineId")
    def sql_virtual_machine_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sqlVirtualMachineId"))

    @sql_virtual_machine_id.setter
    def sql_virtual_machine_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a990579d2a2285d3ef95e259e033cb1c9579cf127818f50d041f6e48b9e2ec9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sqlVirtualMachineId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MssqlVirtualMachineAvailabilityGroupListenerReplica]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MssqlVirtualMachineAvailabilityGroupListenerReplica]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MssqlVirtualMachineAvailabilityGroupListenerReplica]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8293d2e93461d1dba54201dbe7014c9ea099d181c06867179e49a96d8b2aea5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mssqlVirtualMachineAvailabilityGroupListener.MssqlVirtualMachineAvailabilityGroupListenerTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "read": "read"},
)
class MssqlVirtualMachineAvailabilityGroupListenerTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_availability_group_listener#create MssqlVirtualMachineAvailabilityGroupListener#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_availability_group_listener#delete MssqlVirtualMachineAvailabilityGroupListener#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_availability_group_listener#read MssqlVirtualMachineAvailabilityGroupListener#read}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d55010d59d32b84e8192c43e96ddeb25d53e1a7f4391a1be518e961afff4c769)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_availability_group_listener#create MssqlVirtualMachineAvailabilityGroupListener#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_availability_group_listener#delete MssqlVirtualMachineAvailabilityGroupListener#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine_availability_group_listener#read MssqlVirtualMachineAvailabilityGroupListener#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MssqlVirtualMachineAvailabilityGroupListenerTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MssqlVirtualMachineAvailabilityGroupListenerTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mssqlVirtualMachineAvailabilityGroupListener.MssqlVirtualMachineAvailabilityGroupListenerTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a9d92ec013d5eb34d953b79faa46d9975cfe3d495c48de99429d355a5add6a08)
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
            type_hints = typing.get_type_hints(_typecheckingstub__554eaa494f32f84399a2604ca473a3b6d91dbb2f0ad60f998cf56a55ff02253c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acb8d9a8e254d51f2fb8479f5c83aaaf384a62c0e0a7b4dc921e2bb15cd4e110)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__891097fa3fff0df8329f0df486bb160356fc8653af6c5a729c87533e019d82b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MssqlVirtualMachineAvailabilityGroupListenerTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MssqlVirtualMachineAvailabilityGroupListenerTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MssqlVirtualMachineAvailabilityGroupListenerTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b99a68bdbd015fba01157d156854e6a623d88cbf58f66426bf33ab34324d03a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "MssqlVirtualMachineAvailabilityGroupListener",
    "MssqlVirtualMachineAvailabilityGroupListenerConfig",
    "MssqlVirtualMachineAvailabilityGroupListenerLoadBalancerConfiguration",
    "MssqlVirtualMachineAvailabilityGroupListenerLoadBalancerConfigurationOutputReference",
    "MssqlVirtualMachineAvailabilityGroupListenerMultiSubnetIpConfiguration",
    "MssqlVirtualMachineAvailabilityGroupListenerMultiSubnetIpConfigurationList",
    "MssqlVirtualMachineAvailabilityGroupListenerMultiSubnetIpConfigurationOutputReference",
    "MssqlVirtualMachineAvailabilityGroupListenerReplica",
    "MssqlVirtualMachineAvailabilityGroupListenerReplicaList",
    "MssqlVirtualMachineAvailabilityGroupListenerReplicaOutputReference",
    "MssqlVirtualMachineAvailabilityGroupListenerTimeouts",
    "MssqlVirtualMachineAvailabilityGroupListenerTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__97908daabeb7a950a73afcbeb72768c1b1397d183af007a4310c27c6dc8a5ba0(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    replica: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MssqlVirtualMachineAvailabilityGroupListenerReplica, typing.Dict[builtins.str, typing.Any]]]],
    sql_virtual_machine_group_id: builtins.str,
    availability_group_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    load_balancer_configuration: typing.Optional[typing.Union[MssqlVirtualMachineAvailabilityGroupListenerLoadBalancerConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    multi_subnet_ip_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MssqlVirtualMachineAvailabilityGroupListenerMultiSubnetIpConfiguration, typing.Dict[builtins.str, typing.Any]]]]] = None,
    port: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[MssqlVirtualMachineAvailabilityGroupListenerTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__7d806fdf4f3683a99a66b1569d7aed8af433d2f2d66a6a841edeb03dc213b29d(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87b45c42447d3841cd1110700ab7401741d8bcbd718b55320f4cc74893eb6bd7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MssqlVirtualMachineAvailabilityGroupListenerMultiSubnetIpConfiguration, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92ac9cbee8e56f0fd24c16aa45653c0f289b92737240ee668bb9104d09214ac7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MssqlVirtualMachineAvailabilityGroupListenerReplica, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__833fa5bf2306b7ac27226c190025ae15679bc90fe0bb7f6afa9a8ad862393c7e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f9b2b724df10e26138c72ce1a0593a58eb5f466d76c53bf13ba47435d74b927(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__098fe0e820ab45a9f211214c0c58f50fffc4e4a6f84c14047a09bb7d36fd3898(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d89bd2704cd1470881613372945dcba9ab20e9715bf5fdeed9563068d366fe49(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84d670bb24c22a78d54c1d9c614878aee44c1437866af8c8e9f159b1e9584205(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46a5ac80780fbbb3ee49fabf85efceaca4a653a385bc40677b2b88817a958650(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    replica: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MssqlVirtualMachineAvailabilityGroupListenerReplica, typing.Dict[builtins.str, typing.Any]]]],
    sql_virtual_machine_group_id: builtins.str,
    availability_group_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    load_balancer_configuration: typing.Optional[typing.Union[MssqlVirtualMachineAvailabilityGroupListenerLoadBalancerConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    multi_subnet_ip_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MssqlVirtualMachineAvailabilityGroupListenerMultiSubnetIpConfiguration, typing.Dict[builtins.str, typing.Any]]]]] = None,
    port: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[MssqlVirtualMachineAvailabilityGroupListenerTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32c314fa09a52e0f5525d2854170283470095fde25ac69e8bc620edb1c61eb17(
    *,
    load_balancer_id: builtins.str,
    private_ip_address: builtins.str,
    probe_port: jsii.Number,
    sql_virtual_machine_ids: typing.Sequence[builtins.str],
    subnet_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16c1aae7e0d69923895b47b72a13acbd5bf9b4fedd724897c9db5f31df5c3577(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__686456979c79658ad52a9aa7e863cc048d3fced3eabad70bd631362405cebbac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8de94954660521c1eff29d7a71649da5e52ef174a618e9284ae209513ddaaa82(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fddd1ad728f6537ef940987d6370d8aa2e4c561bf93e44c64de05fe2a39e4166(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f092df768bb999c6f25a12394e3d52c67cc627447f3eb03ea578ba5cfb20e070(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6aaee521e5877b18c1c16d7c4b9d501a62e9608b4ee15033e6f50f083ca83370(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ef6b0dcc573e5d8fb545d8f273a4175ad6c4c28039f1461fa8829bc29390be3(
    value: typing.Optional[MssqlVirtualMachineAvailabilityGroupListenerLoadBalancerConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd419241ee51db414e3920d22c6853aec1c48d90f25403d96810bc1f01a3b3b0(
    *,
    private_ip_address: builtins.str,
    sql_virtual_machine_id: builtins.str,
    subnet_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4043a822317c101ff8727e05cd96e485f5f84afdf96e8d4d98f367ae4317f7c0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16e6542ecfe8ba15c1c6e2748d1551ccc048810a74b76424d1623150aae79f31(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__010959af5f009a62db74d920da1d7503c5509a5b7e32c96ade1565a60c391f2a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66c008efff2253428a3961882b365730a3015516018d4663e6713daa7bda007b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f59ab415684cde0060352efe917341fdf08825c8ae18a82c757fb69e14e51efa(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1df0a9e40d3e8649d094ef1b25d6a8d150d2320a80d22ce76024e4251fa7655e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MssqlVirtualMachineAvailabilityGroupListenerMultiSubnetIpConfiguration]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0dc5aab36e1a1d6ae334f8f514fbdfecb8b14724f72ba62f4e91731af7be026(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7d6daba7657dfbacdfd58d4b61bf19117b4c01f1eff16a781f7390f2aa5ff06(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46310a65b6cc6146d825723c64a2208d45619d0147d91cedc7044a17c7b6d644(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f06b79dff0d7fe848d0008941ccf846d8ec4a630699edd318e0c2d6f018a147d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c614e863121160b82ac90311b328f6e32db85b974e0cb3277b3faae3537b2675(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MssqlVirtualMachineAvailabilityGroupListenerMultiSubnetIpConfiguration]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f79546e8bf9575acef6ccbfecde035b574ea55ad27168541e165e72d9c06bc17(
    *,
    commit: builtins.str,
    failover_mode: builtins.str,
    readable_secondary: builtins.str,
    role: builtins.str,
    sql_virtual_machine_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b85edcd0426036ff49f456d3cfe7c4425a0560d2246f9e9dec5c19a958a1a3aa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f23f95730158dd5766dc97e2970f9feccfbd77a63e72d3e185a01e7d4c316d38(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f57b33ac8549ef68bb00e9c490b0f94b1e86d8e2d29e035692957b617a45471(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76df63066a05edb03c2bd716207880bd39e22f8a54ad3f84c8ebaf2a420527e0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__290c3a95934b048d9b7004114fe42794e830434ef37552dd5c2643acbd648ab5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1a1620096c48b4e93c680214abb251bbd71c34867c130408a67598631a42314(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MssqlVirtualMachineAvailabilityGroupListenerReplica]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a10632b220ca76dc43b24b9087c1454f1071f0a18eea42892c3d6d162ae975e2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa56c14c896a4f75fa74cabd30bedb8a78565468695fcd7b9829b0eb930405d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__816aa9d3f7708b01eb36bb4ba6445dd3d04fbed8f85512e0b6d8ab4c7ceeea7c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb59c8a2063cbb9b33b43bf5ae27eb9804380307df80dade0cca33cd53b2ee41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38f77723be16fa73c39af5eb101dcbcd7ae6ca32f4ee2402ddeb7676602ac620(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a990579d2a2285d3ef95e259e033cb1c9579cf127818f50d041f6e48b9e2ec9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8293d2e93461d1dba54201dbe7014c9ea099d181c06867179e49a96d8b2aea5d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MssqlVirtualMachineAvailabilityGroupListenerReplica]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d55010d59d32b84e8192c43e96ddeb25d53e1a7f4391a1be518e961afff4c769(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9d92ec013d5eb34d953b79faa46d9975cfe3d495c48de99429d355a5add6a08(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__554eaa494f32f84399a2604ca473a3b6d91dbb2f0ad60f998cf56a55ff02253c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acb8d9a8e254d51f2fb8479f5c83aaaf384a62c0e0a7b4dc921e2bb15cd4e110(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__891097fa3fff0df8329f0df486bb160356fc8653af6c5a729c87533e019d82b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b99a68bdbd015fba01157d156854e6a623d88cbf58f66426bf33ab34324d03a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MssqlVirtualMachineAvailabilityGroupListenerTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
