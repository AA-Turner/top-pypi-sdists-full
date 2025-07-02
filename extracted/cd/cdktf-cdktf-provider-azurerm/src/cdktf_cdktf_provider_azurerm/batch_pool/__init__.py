r'''
# `azurerm_batch_pool`

Refer to the Terraform Registry for docs: [`azurerm_batch_pool`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool).
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


class BatchPool(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPool",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool azurerm_batch_pool}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        account_name: builtins.str,
        name: builtins.str,
        node_agent_sku_id: builtins.str,
        resource_group_name: builtins.str,
        storage_image_reference: typing.Union["BatchPoolStorageImageReference", typing.Dict[builtins.str, typing.Any]],
        vm_size: builtins.str,
        auto_scale: typing.Optional[typing.Union["BatchPoolAutoScale", typing.Dict[builtins.str, typing.Any]]] = None,
        certificate: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BatchPoolCertificate", typing.Dict[builtins.str, typing.Any]]]]] = None,
        container_configuration: typing.Optional[typing.Union["BatchPoolContainerConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        data_disks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BatchPoolDataDisks", typing.Dict[builtins.str, typing.Any]]]]] = None,
        disk_encryption: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BatchPoolDiskEncryption", typing.Dict[builtins.str, typing.Any]]]]] = None,
        display_name: typing.Optional[builtins.str] = None,
        extensions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BatchPoolExtensions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        fixed_scale: typing.Optional[typing.Union["BatchPoolFixedScale", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        identity: typing.Optional[typing.Union["BatchPoolIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        inter_node_communication: typing.Optional[builtins.str] = None,
        license_type: typing.Optional[builtins.str] = None,
        max_tasks_per_node: typing.Optional[jsii.Number] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        mount: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BatchPoolMount", typing.Dict[builtins.str, typing.Any]]]]] = None,
        network_configuration: typing.Optional[typing.Union["BatchPoolNetworkConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        node_placement: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BatchPoolNodePlacement", typing.Dict[builtins.str, typing.Any]]]]] = None,
        os_disk_placement: typing.Optional[builtins.str] = None,
        security_profile: typing.Optional[typing.Union["BatchPoolSecurityProfile", typing.Dict[builtins.str, typing.Any]]] = None,
        start_task: typing.Optional[typing.Union["BatchPoolStartTask", typing.Dict[builtins.str, typing.Any]]] = None,
        stop_pending_resize_operation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        target_node_communication_mode: typing.Optional[builtins.str] = None,
        task_scheduling_policy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BatchPoolTaskSchedulingPolicy", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["BatchPoolTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        user_accounts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BatchPoolUserAccounts", typing.Dict[builtins.str, typing.Any]]]]] = None,
        windows: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BatchPoolWindows", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool azurerm_batch_pool} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param account_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#account_name BatchPool#account_name}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#name BatchPool#name}.
        :param node_agent_sku_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#node_agent_sku_id BatchPool#node_agent_sku_id}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#resource_group_name BatchPool#resource_group_name}.
        :param storage_image_reference: storage_image_reference block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#storage_image_reference BatchPool#storage_image_reference}
        :param vm_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#vm_size BatchPool#vm_size}.
        :param auto_scale: auto_scale block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#auto_scale BatchPool#auto_scale}
        :param certificate: certificate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#certificate BatchPool#certificate}
        :param container_configuration: container_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#container_configuration BatchPool#container_configuration}
        :param data_disks: data_disks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#data_disks BatchPool#data_disks}
        :param disk_encryption: disk_encryption block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#disk_encryption BatchPool#disk_encryption}
        :param display_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#display_name BatchPool#display_name}.
        :param extensions: extensions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#extensions BatchPool#extensions}
        :param fixed_scale: fixed_scale block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#fixed_scale BatchPool#fixed_scale}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#id BatchPool#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity: identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#identity BatchPool#identity}
        :param inter_node_communication: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#inter_node_communication BatchPool#inter_node_communication}.
        :param license_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#license_type BatchPool#license_type}.
        :param max_tasks_per_node: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#max_tasks_per_node BatchPool#max_tasks_per_node}.
        :param metadata: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#metadata BatchPool#metadata}.
        :param mount: mount block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#mount BatchPool#mount}
        :param network_configuration: network_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#network_configuration BatchPool#network_configuration}
        :param node_placement: node_placement block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#node_placement BatchPool#node_placement}
        :param os_disk_placement: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#os_disk_placement BatchPool#os_disk_placement}.
        :param security_profile: security_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#security_profile BatchPool#security_profile}
        :param start_task: start_task block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#start_task BatchPool#start_task}
        :param stop_pending_resize_operation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#stop_pending_resize_operation BatchPool#stop_pending_resize_operation}.
        :param target_node_communication_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#target_node_communication_mode BatchPool#target_node_communication_mode}.
        :param task_scheduling_policy: task_scheduling_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#task_scheduling_policy BatchPool#task_scheduling_policy}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#timeouts BatchPool#timeouts}
        :param user_accounts: user_accounts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#user_accounts BatchPool#user_accounts}
        :param windows: windows block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#windows BatchPool#windows}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9927cfe471f7371287173b14c3427a8020a17b70d5d71930e162e35a3a4eeac2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = BatchPoolConfig(
            account_name=account_name,
            name=name,
            node_agent_sku_id=node_agent_sku_id,
            resource_group_name=resource_group_name,
            storage_image_reference=storage_image_reference,
            vm_size=vm_size,
            auto_scale=auto_scale,
            certificate=certificate,
            container_configuration=container_configuration,
            data_disks=data_disks,
            disk_encryption=disk_encryption,
            display_name=display_name,
            extensions=extensions,
            fixed_scale=fixed_scale,
            id=id,
            identity=identity,
            inter_node_communication=inter_node_communication,
            license_type=license_type,
            max_tasks_per_node=max_tasks_per_node,
            metadata=metadata,
            mount=mount,
            network_configuration=network_configuration,
            node_placement=node_placement,
            os_disk_placement=os_disk_placement,
            security_profile=security_profile,
            start_task=start_task,
            stop_pending_resize_operation=stop_pending_resize_operation,
            target_node_communication_mode=target_node_communication_mode,
            task_scheduling_policy=task_scheduling_policy,
            timeouts=timeouts,
            user_accounts=user_accounts,
            windows=windows,
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
        '''Generates CDKTF code for importing a BatchPool resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the BatchPool to import.
        :param import_from_id: The id of the existing BatchPool that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the BatchPool to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ceb722400d5153e0de9b1f027d5e667961eb620ad6d93e87346bdeffe7383203)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAutoScale")
    def put_auto_scale(
        self,
        *,
        formula: builtins.str,
        evaluation_interval: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param formula: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#formula BatchPool#formula}.
        :param evaluation_interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#evaluation_interval BatchPool#evaluation_interval}.
        '''
        value = BatchPoolAutoScale(
            formula=formula, evaluation_interval=evaluation_interval
        )

        return typing.cast(None, jsii.invoke(self, "putAutoScale", [value]))

    @jsii.member(jsii_name="putCertificate")
    def put_certificate(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BatchPoolCertificate", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07d370a736db7cb3c2bd2df984b861cffadcc8910ba867c2434e9c756e646d7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCertificate", [value]))

    @jsii.member(jsii_name="putContainerConfiguration")
    def put_container_configuration(
        self,
        *,
        container_image_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        container_registries: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BatchPoolContainerConfigurationContainerRegistries", typing.Dict[builtins.str, typing.Any]]]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param container_image_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#container_image_names BatchPool#container_image_names}.
        :param container_registries: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#container_registries BatchPool#container_registries}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#type BatchPool#type}.
        '''
        value = BatchPoolContainerConfiguration(
            container_image_names=container_image_names,
            container_registries=container_registries,
            type=type,
        )

        return typing.cast(None, jsii.invoke(self, "putContainerConfiguration", [value]))

    @jsii.member(jsii_name="putDataDisks")
    def put_data_disks(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BatchPoolDataDisks", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35257d15fed1c15a60db645c81026f4b8c27dfa7f143ee14aaca219e98e56f74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDataDisks", [value]))

    @jsii.member(jsii_name="putDiskEncryption")
    def put_disk_encryption(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BatchPoolDiskEncryption", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27c0c424f8504b933b82f1ccf646a562037fd5b0bf6264d115c53faa7597558f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDiskEncryption", [value]))

    @jsii.member(jsii_name="putExtensions")
    def put_extensions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BatchPoolExtensions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f31bf4dde13ab94425401b8db476711eec966f5d70870b75afd6a2294819dae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putExtensions", [value]))

    @jsii.member(jsii_name="putFixedScale")
    def put_fixed_scale(
        self,
        *,
        node_deallocation_method: typing.Optional[builtins.str] = None,
        resize_timeout: typing.Optional[builtins.str] = None,
        target_dedicated_nodes: typing.Optional[jsii.Number] = None,
        target_low_priority_nodes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param node_deallocation_method: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#node_deallocation_method BatchPool#node_deallocation_method}.
        :param resize_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#resize_timeout BatchPool#resize_timeout}.
        :param target_dedicated_nodes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#target_dedicated_nodes BatchPool#target_dedicated_nodes}.
        :param target_low_priority_nodes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#target_low_priority_nodes BatchPool#target_low_priority_nodes}.
        '''
        value = BatchPoolFixedScale(
            node_deallocation_method=node_deallocation_method,
            resize_timeout=resize_timeout,
            target_dedicated_nodes=target_dedicated_nodes,
            target_low_priority_nodes=target_low_priority_nodes,
        )

        return typing.cast(None, jsii.invoke(self, "putFixedScale", [value]))

    @jsii.member(jsii_name="putIdentity")
    def put_identity(
        self,
        *,
        identity_ids: typing.Sequence[builtins.str],
        type: builtins.str,
    ) -> None:
        '''
        :param identity_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#identity_ids BatchPool#identity_ids}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#type BatchPool#type}.
        '''
        value = BatchPoolIdentity(identity_ids=identity_ids, type=type)

        return typing.cast(None, jsii.invoke(self, "putIdentity", [value]))

    @jsii.member(jsii_name="putMount")
    def put_mount(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BatchPoolMount", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a23ec836dcc17734b65a525d817649ca7cc315fd6957af7461dc3c90bc1d42bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMount", [value]))

    @jsii.member(jsii_name="putNetworkConfiguration")
    def put_network_configuration(
        self,
        *,
        accelerated_networking_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        dynamic_vnet_assignment_scope: typing.Optional[builtins.str] = None,
        endpoint_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BatchPoolNetworkConfigurationEndpointConfiguration", typing.Dict[builtins.str, typing.Any]]]]] = None,
        public_address_provisioning_type: typing.Optional[builtins.str] = None,
        public_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnet_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param accelerated_networking_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#accelerated_networking_enabled BatchPool#accelerated_networking_enabled}.
        :param dynamic_vnet_assignment_scope: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#dynamic_vnet_assignment_scope BatchPool#dynamic_vnet_assignment_scope}.
        :param endpoint_configuration: endpoint_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#endpoint_configuration BatchPool#endpoint_configuration}
        :param public_address_provisioning_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#public_address_provisioning_type BatchPool#public_address_provisioning_type}.
        :param public_ips: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#public_ips BatchPool#public_ips}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#subnet_id BatchPool#subnet_id}.
        '''
        value = BatchPoolNetworkConfiguration(
            accelerated_networking_enabled=accelerated_networking_enabled,
            dynamic_vnet_assignment_scope=dynamic_vnet_assignment_scope,
            endpoint_configuration=endpoint_configuration,
            public_address_provisioning_type=public_address_provisioning_type,
            public_ips=public_ips,
            subnet_id=subnet_id,
        )

        return typing.cast(None, jsii.invoke(self, "putNetworkConfiguration", [value]))

    @jsii.member(jsii_name="putNodePlacement")
    def put_node_placement(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BatchPoolNodePlacement", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97a4b7225fd27e026980f86177b6ccb803f8033491ca08e9e6b818173b22f3f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNodePlacement", [value]))

    @jsii.member(jsii_name="putSecurityProfile")
    def put_security_profile(
        self,
        *,
        host_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        secure_boot_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        security_type: typing.Optional[builtins.str] = None,
        vtpm_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param host_encryption_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#host_encryption_enabled BatchPool#host_encryption_enabled}.
        :param secure_boot_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#secure_boot_enabled BatchPool#secure_boot_enabled}.
        :param security_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#security_type BatchPool#security_type}.
        :param vtpm_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#vtpm_enabled BatchPool#vtpm_enabled}.
        '''
        value = BatchPoolSecurityProfile(
            host_encryption_enabled=host_encryption_enabled,
            secure_boot_enabled=secure_boot_enabled,
            security_type=security_type,
            vtpm_enabled=vtpm_enabled,
        )

        return typing.cast(None, jsii.invoke(self, "putSecurityProfile", [value]))

    @jsii.member(jsii_name="putStartTask")
    def put_start_task(
        self,
        *,
        command_line: builtins.str,
        user_identity: typing.Union["BatchPoolStartTaskUserIdentity", typing.Dict[builtins.str, typing.Any]],
        common_environment_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        container: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BatchPoolStartTaskContainer", typing.Dict[builtins.str, typing.Any]]]]] = None,
        resource_file: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BatchPoolStartTaskResourceFile", typing.Dict[builtins.str, typing.Any]]]]] = None,
        task_retry_maximum: typing.Optional[jsii.Number] = None,
        wait_for_success: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param command_line: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#command_line BatchPool#command_line}.
        :param user_identity: user_identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#user_identity BatchPool#user_identity}
        :param common_environment_properties: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#common_environment_properties BatchPool#common_environment_properties}.
        :param container: container block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#container BatchPool#container}
        :param resource_file: resource_file block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#resource_file BatchPool#resource_file}
        :param task_retry_maximum: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#task_retry_maximum BatchPool#task_retry_maximum}.
        :param wait_for_success: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#wait_for_success BatchPool#wait_for_success}.
        '''
        value = BatchPoolStartTask(
            command_line=command_line,
            user_identity=user_identity,
            common_environment_properties=common_environment_properties,
            container=container,
            resource_file=resource_file,
            task_retry_maximum=task_retry_maximum,
            wait_for_success=wait_for_success,
        )

        return typing.cast(None, jsii.invoke(self, "putStartTask", [value]))

    @jsii.member(jsii_name="putStorageImageReference")
    def put_storage_image_reference(
        self,
        *,
        id: typing.Optional[builtins.str] = None,
        offer: typing.Optional[builtins.str] = None,
        publisher: typing.Optional[builtins.str] = None,
        sku: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#id BatchPool#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param offer: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#offer BatchPool#offer}.
        :param publisher: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#publisher BatchPool#publisher}.
        :param sku: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#sku BatchPool#sku}.
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#version BatchPool#version}.
        '''
        value = BatchPoolStorageImageReference(
            id=id, offer=offer, publisher=publisher, sku=sku, version=version
        )

        return typing.cast(None, jsii.invoke(self, "putStorageImageReference", [value]))

    @jsii.member(jsii_name="putTaskSchedulingPolicy")
    def put_task_scheduling_policy(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BatchPoolTaskSchedulingPolicy", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1045de5fbe3c07b0454e0b9ba24faf36085b0d172fff779fde68f75e75e0cbf6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTaskSchedulingPolicy", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#create BatchPool#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#delete BatchPool#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#read BatchPool#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#update BatchPool#update}.
        '''
        value = BatchPoolTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putUserAccounts")
    def put_user_accounts(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BatchPoolUserAccounts", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adce9721f01ea7caf079530820c53805e266c8e962bf6ae5d326667f64ef3b5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putUserAccounts", [value]))

    @jsii.member(jsii_name="putWindows")
    def put_windows(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BatchPoolWindows", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a949698364f033323419948f7662e9e1bfa2fd235797c2be394ebfc55bcb4d9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putWindows", [value]))

    @jsii.member(jsii_name="resetAutoScale")
    def reset_auto_scale(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoScale", []))

    @jsii.member(jsii_name="resetCertificate")
    def reset_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificate", []))

    @jsii.member(jsii_name="resetContainerConfiguration")
    def reset_container_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerConfiguration", []))

    @jsii.member(jsii_name="resetDataDisks")
    def reset_data_disks(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataDisks", []))

    @jsii.member(jsii_name="resetDiskEncryption")
    def reset_disk_encryption(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskEncryption", []))

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetExtensions")
    def reset_extensions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExtensions", []))

    @jsii.member(jsii_name="resetFixedScale")
    def reset_fixed_scale(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFixedScale", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIdentity")
    def reset_identity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentity", []))

    @jsii.member(jsii_name="resetInterNodeCommunication")
    def reset_inter_node_communication(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInterNodeCommunication", []))

    @jsii.member(jsii_name="resetLicenseType")
    def reset_license_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLicenseType", []))

    @jsii.member(jsii_name="resetMaxTasksPerNode")
    def reset_max_tasks_per_node(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxTasksPerNode", []))

    @jsii.member(jsii_name="resetMetadata")
    def reset_metadata(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetadata", []))

    @jsii.member(jsii_name="resetMount")
    def reset_mount(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMount", []))

    @jsii.member(jsii_name="resetNetworkConfiguration")
    def reset_network_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkConfiguration", []))

    @jsii.member(jsii_name="resetNodePlacement")
    def reset_node_placement(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodePlacement", []))

    @jsii.member(jsii_name="resetOsDiskPlacement")
    def reset_os_disk_placement(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOsDiskPlacement", []))

    @jsii.member(jsii_name="resetSecurityProfile")
    def reset_security_profile(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityProfile", []))

    @jsii.member(jsii_name="resetStartTask")
    def reset_start_task(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartTask", []))

    @jsii.member(jsii_name="resetStopPendingResizeOperation")
    def reset_stop_pending_resize_operation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStopPendingResizeOperation", []))

    @jsii.member(jsii_name="resetTargetNodeCommunicationMode")
    def reset_target_node_communication_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetNodeCommunicationMode", []))

    @jsii.member(jsii_name="resetTaskSchedulingPolicy")
    def reset_task_scheduling_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTaskSchedulingPolicy", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetUserAccounts")
    def reset_user_accounts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserAccounts", []))

    @jsii.member(jsii_name="resetWindows")
    def reset_windows(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWindows", []))

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
    @jsii.member(jsii_name="autoScale")
    def auto_scale(self) -> "BatchPoolAutoScaleOutputReference":
        return typing.cast("BatchPoolAutoScaleOutputReference", jsii.get(self, "autoScale"))

    @builtins.property
    @jsii.member(jsii_name="certificate")
    def certificate(self) -> "BatchPoolCertificateList":
        return typing.cast("BatchPoolCertificateList", jsii.get(self, "certificate"))

    @builtins.property
    @jsii.member(jsii_name="containerConfiguration")
    def container_configuration(
        self,
    ) -> "BatchPoolContainerConfigurationOutputReference":
        return typing.cast("BatchPoolContainerConfigurationOutputReference", jsii.get(self, "containerConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="dataDisks")
    def data_disks(self) -> "BatchPoolDataDisksList":
        return typing.cast("BatchPoolDataDisksList", jsii.get(self, "dataDisks"))

    @builtins.property
    @jsii.member(jsii_name="diskEncryption")
    def disk_encryption(self) -> "BatchPoolDiskEncryptionList":
        return typing.cast("BatchPoolDiskEncryptionList", jsii.get(self, "diskEncryption"))

    @builtins.property
    @jsii.member(jsii_name="extensions")
    def extensions(self) -> "BatchPoolExtensionsList":
        return typing.cast("BatchPoolExtensionsList", jsii.get(self, "extensions"))

    @builtins.property
    @jsii.member(jsii_name="fixedScale")
    def fixed_scale(self) -> "BatchPoolFixedScaleOutputReference":
        return typing.cast("BatchPoolFixedScaleOutputReference", jsii.get(self, "fixedScale"))

    @builtins.property
    @jsii.member(jsii_name="identity")
    def identity(self) -> "BatchPoolIdentityOutputReference":
        return typing.cast("BatchPoolIdentityOutputReference", jsii.get(self, "identity"))

    @builtins.property
    @jsii.member(jsii_name="mount")
    def mount(self) -> "BatchPoolMountList":
        return typing.cast("BatchPoolMountList", jsii.get(self, "mount"))

    @builtins.property
    @jsii.member(jsii_name="networkConfiguration")
    def network_configuration(self) -> "BatchPoolNetworkConfigurationOutputReference":
        return typing.cast("BatchPoolNetworkConfigurationOutputReference", jsii.get(self, "networkConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="nodePlacement")
    def node_placement(self) -> "BatchPoolNodePlacementList":
        return typing.cast("BatchPoolNodePlacementList", jsii.get(self, "nodePlacement"))

    @builtins.property
    @jsii.member(jsii_name="securityProfile")
    def security_profile(self) -> "BatchPoolSecurityProfileOutputReference":
        return typing.cast("BatchPoolSecurityProfileOutputReference", jsii.get(self, "securityProfile"))

    @builtins.property
    @jsii.member(jsii_name="startTask")
    def start_task(self) -> "BatchPoolStartTaskOutputReference":
        return typing.cast("BatchPoolStartTaskOutputReference", jsii.get(self, "startTask"))

    @builtins.property
    @jsii.member(jsii_name="storageImageReference")
    def storage_image_reference(
        self,
    ) -> "BatchPoolStorageImageReferenceOutputReference":
        return typing.cast("BatchPoolStorageImageReferenceOutputReference", jsii.get(self, "storageImageReference"))

    @builtins.property
    @jsii.member(jsii_name="taskSchedulingPolicy")
    def task_scheduling_policy(self) -> "BatchPoolTaskSchedulingPolicyList":
        return typing.cast("BatchPoolTaskSchedulingPolicyList", jsii.get(self, "taskSchedulingPolicy"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "BatchPoolTimeoutsOutputReference":
        return typing.cast("BatchPoolTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="userAccounts")
    def user_accounts(self) -> "BatchPoolUserAccountsList":
        return typing.cast("BatchPoolUserAccountsList", jsii.get(self, "userAccounts"))

    @builtins.property
    @jsii.member(jsii_name="windows")
    def windows(self) -> "BatchPoolWindowsList":
        return typing.cast("BatchPoolWindowsList", jsii.get(self, "windows"))

    @builtins.property
    @jsii.member(jsii_name="accountNameInput")
    def account_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountNameInput"))

    @builtins.property
    @jsii.member(jsii_name="autoScaleInput")
    def auto_scale_input(self) -> typing.Optional["BatchPoolAutoScale"]:
        return typing.cast(typing.Optional["BatchPoolAutoScale"], jsii.get(self, "autoScaleInput"))

    @builtins.property
    @jsii.member(jsii_name="certificateInput")
    def certificate_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BatchPoolCertificate"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BatchPoolCertificate"]]], jsii.get(self, "certificateInput"))

    @builtins.property
    @jsii.member(jsii_name="containerConfigurationInput")
    def container_configuration_input(
        self,
    ) -> typing.Optional["BatchPoolContainerConfiguration"]:
        return typing.cast(typing.Optional["BatchPoolContainerConfiguration"], jsii.get(self, "containerConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="dataDisksInput")
    def data_disks_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BatchPoolDataDisks"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BatchPoolDataDisks"]]], jsii.get(self, "dataDisksInput"))

    @builtins.property
    @jsii.member(jsii_name="diskEncryptionInput")
    def disk_encryption_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BatchPoolDiskEncryption"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BatchPoolDiskEncryption"]]], jsii.get(self, "diskEncryptionInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="extensionsInput")
    def extensions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BatchPoolExtensions"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BatchPoolExtensions"]]], jsii.get(self, "extensionsInput"))

    @builtins.property
    @jsii.member(jsii_name="fixedScaleInput")
    def fixed_scale_input(self) -> typing.Optional["BatchPoolFixedScale"]:
        return typing.cast(typing.Optional["BatchPoolFixedScale"], jsii.get(self, "fixedScaleInput"))

    @builtins.property
    @jsii.member(jsii_name="identityInput")
    def identity_input(self) -> typing.Optional["BatchPoolIdentity"]:
        return typing.cast(typing.Optional["BatchPoolIdentity"], jsii.get(self, "identityInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="interNodeCommunicationInput")
    def inter_node_communication_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "interNodeCommunicationInput"))

    @builtins.property
    @jsii.member(jsii_name="licenseTypeInput")
    def license_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "licenseTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="maxTasksPerNodeInput")
    def max_tasks_per_node_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxTasksPerNodeInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataInput")
    def metadata_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "metadataInput"))

    @builtins.property
    @jsii.member(jsii_name="mountInput")
    def mount_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BatchPoolMount"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BatchPoolMount"]]], jsii.get(self, "mountInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkConfigurationInput")
    def network_configuration_input(
        self,
    ) -> typing.Optional["BatchPoolNetworkConfiguration"]:
        return typing.cast(typing.Optional["BatchPoolNetworkConfiguration"], jsii.get(self, "networkConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeAgentSkuIdInput")
    def node_agent_sku_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nodeAgentSkuIdInput"))

    @builtins.property
    @jsii.member(jsii_name="nodePlacementInput")
    def node_placement_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BatchPoolNodePlacement"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BatchPoolNodePlacement"]]], jsii.get(self, "nodePlacementInput"))

    @builtins.property
    @jsii.member(jsii_name="osDiskPlacementInput")
    def os_disk_placement_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "osDiskPlacementInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="securityProfileInput")
    def security_profile_input(self) -> typing.Optional["BatchPoolSecurityProfile"]:
        return typing.cast(typing.Optional["BatchPoolSecurityProfile"], jsii.get(self, "securityProfileInput"))

    @builtins.property
    @jsii.member(jsii_name="startTaskInput")
    def start_task_input(self) -> typing.Optional["BatchPoolStartTask"]:
        return typing.cast(typing.Optional["BatchPoolStartTask"], jsii.get(self, "startTaskInput"))

    @builtins.property
    @jsii.member(jsii_name="stopPendingResizeOperationInput")
    def stop_pending_resize_operation_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "stopPendingResizeOperationInput"))

    @builtins.property
    @jsii.member(jsii_name="storageImageReferenceInput")
    def storage_image_reference_input(
        self,
    ) -> typing.Optional["BatchPoolStorageImageReference"]:
        return typing.cast(typing.Optional["BatchPoolStorageImageReference"], jsii.get(self, "storageImageReferenceInput"))

    @builtins.property
    @jsii.member(jsii_name="targetNodeCommunicationModeInput")
    def target_node_communication_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetNodeCommunicationModeInput"))

    @builtins.property
    @jsii.member(jsii_name="taskSchedulingPolicyInput")
    def task_scheduling_policy_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BatchPoolTaskSchedulingPolicy"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BatchPoolTaskSchedulingPolicy"]]], jsii.get(self, "taskSchedulingPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "BatchPoolTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "BatchPoolTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="userAccountsInput")
    def user_accounts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BatchPoolUserAccounts"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BatchPoolUserAccounts"]]], jsii.get(self, "userAccountsInput"))

    @builtins.property
    @jsii.member(jsii_name="vmSizeInput")
    def vm_size_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vmSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="windowsInput")
    def windows_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BatchPoolWindows"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BatchPoolWindows"]]], jsii.get(self, "windowsInput"))

    @builtins.property
    @jsii.member(jsii_name="accountName")
    def account_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountName"))

    @account_name.setter
    def account_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc5b51e173f2ebfb3068704bf2bcfc9b18ee913117c04330b9aa6de4ca0b80e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__221b15332d5e73630053eb10d53e00ac00553f4e5311861f5928071294d3b4b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2af8570637cba2c006ae37435935c593cc4ac36268c215ecc43262f35d8f7bec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="interNodeCommunication")
    def inter_node_communication(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "interNodeCommunication"))

    @inter_node_communication.setter
    def inter_node_communication(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bfa3b81639131d57750b85d52dd7594cb9b728f68bb8d9b00489d2b5666fc8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interNodeCommunication", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="licenseType")
    def license_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "licenseType"))

    @license_type.setter
    def license_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10125d092830cc51e63be2f688489852c049c71ce1c40e5e830493119278dc59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "licenseType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxTasksPerNode")
    def max_tasks_per_node(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxTasksPerNode"))

    @max_tasks_per_node.setter
    def max_tasks_per_node(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1db57ef2147d2cb5eaeeb0fbf4ef7d0b7b13f8b555cbd3a71f0ea4e9f54c6f40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxTasksPerNode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "metadata"))

    @metadata.setter
    def metadata(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9868424ab3a101126ea5f5815fd1a14cd16076fda9a5bbf8682caad04b1786d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadata", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__924768bc397860253da7a04bdebf669857de59b8e0d84cc1b83ee91b0089eba4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeAgentSkuId")
    def node_agent_sku_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeAgentSkuId"))

    @node_agent_sku_id.setter
    def node_agent_sku_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf0a3bc5f6ff8ab08cf01dce65bc1fcb8826a7275d51d37a73b5b9fb9422fb7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeAgentSkuId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="osDiskPlacement")
    def os_disk_placement(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "osDiskPlacement"))

    @os_disk_placement.setter
    def os_disk_placement(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d16ba2e2f3eafc8dc7f41705342f853b8ec4f35960bd1f44408ac7bbe839038a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "osDiskPlacement", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34b8ef9ebf4a75397424c610d0a81a61655c87962dd085c03f8e3e43a05297c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stopPendingResizeOperation")
    def stop_pending_resize_operation(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "stopPendingResizeOperation"))

    @stop_pending_resize_operation.setter
    def stop_pending_resize_operation(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc7af643b39cec19df23ff09892d4b3cbe2c4070c143e967facfde9743ba7cc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stopPendingResizeOperation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetNodeCommunicationMode")
    def target_node_communication_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetNodeCommunicationMode"))

    @target_node_communication_mode.setter
    def target_node_communication_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff326ee8545cf081bd5310ec39f6cc0de39f42ce591ecb2f8f55112309620cd7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetNodeCommunicationMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vmSize")
    def vm_size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vmSize"))

    @vm_size.setter
    def vm_size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a39a11702f8a0021705b2508f5bcabdf617f39d9180807cbbb5819b218e467ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vmSize", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolAutoScale",
    jsii_struct_bases=[],
    name_mapping={"formula": "formula", "evaluation_interval": "evaluationInterval"},
)
class BatchPoolAutoScale:
    def __init__(
        self,
        *,
        formula: builtins.str,
        evaluation_interval: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param formula: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#formula BatchPool#formula}.
        :param evaluation_interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#evaluation_interval BatchPool#evaluation_interval}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a88a77dba9609bf391147a8f7d36239744b34bcef8779f5eb80bb24e9646150a)
            check_type(argname="argument formula", value=formula, expected_type=type_hints["formula"])
            check_type(argname="argument evaluation_interval", value=evaluation_interval, expected_type=type_hints["evaluation_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "formula": formula,
        }
        if evaluation_interval is not None:
            self._values["evaluation_interval"] = evaluation_interval

    @builtins.property
    def formula(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#formula BatchPool#formula}.'''
        result = self._values.get("formula")
        assert result is not None, "Required property 'formula' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def evaluation_interval(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#evaluation_interval BatchPool#evaluation_interval}.'''
        result = self._values.get("evaluation_interval")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BatchPoolAutoScale(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BatchPoolAutoScaleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolAutoScaleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a75bf5b54a2f75bde0c327c561c375cb08ab350e16597b0b60c52520f9ded7c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEvaluationInterval")
    def reset_evaluation_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEvaluationInterval", []))

    @builtins.property
    @jsii.member(jsii_name="evaluationIntervalInput")
    def evaluation_interval_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "evaluationIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="formulaInput")
    def formula_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "formulaInput"))

    @builtins.property
    @jsii.member(jsii_name="evaluationInterval")
    def evaluation_interval(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "evaluationInterval"))

    @evaluation_interval.setter
    def evaluation_interval(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b1da7e5fb69f5b0d3a73a9b820014cad2af5a5c721627bac15938e55a99f0d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "evaluationInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="formula")
    def formula(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "formula"))

    @formula.setter
    def formula(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__737723f7650006e4ddbd74905ea4920296b7c52ba438928fe1c2ff32f14d17fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "formula", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BatchPoolAutoScale]:
        return typing.cast(typing.Optional[BatchPoolAutoScale], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[BatchPoolAutoScale]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3672b65d2e33f51455dd4b6b04137ed2e79468313b6d63d2e9b436f2b8279e75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolCertificate",
    jsii_struct_bases=[],
    name_mapping={
        "id": "id",
        "store_location": "storeLocation",
        "store_name": "storeName",
        "visibility": "visibility",
    },
)
class BatchPoolCertificate:
    def __init__(
        self,
        *,
        id: builtins.str,
        store_location: builtins.str,
        store_name: typing.Optional[builtins.str] = None,
        visibility: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#id BatchPool#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param store_location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#store_location BatchPool#store_location}.
        :param store_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#store_name BatchPool#store_name}.
        :param visibility: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#visibility BatchPool#visibility}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acce31f232bbe463e5730ff09b7fa9661c53f341c9dc58e4c2ed86c17de9c150)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument store_location", value=store_location, expected_type=type_hints["store_location"])
            check_type(argname="argument store_name", value=store_name, expected_type=type_hints["store_name"])
            check_type(argname="argument visibility", value=visibility, expected_type=type_hints["visibility"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
            "store_location": store_location,
        }
        if store_name is not None:
            self._values["store_name"] = store_name
        if visibility is not None:
            self._values["visibility"] = visibility

    @builtins.property
    def id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#id BatchPool#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def store_location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#store_location BatchPool#store_location}.'''
        result = self._values.get("store_location")
        assert result is not None, "Required property 'store_location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def store_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#store_name BatchPool#store_name}.'''
        result = self._values.get("store_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def visibility(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#visibility BatchPool#visibility}.'''
        result = self._values.get("visibility")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BatchPoolCertificate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BatchPoolCertificateList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolCertificateList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fa1551cfd5f7d08ea4a40a19a1801021453b7a5c0dede3b2337d4b7ca92fa7ac)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "BatchPoolCertificateOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cd774089f1f36a65f974575367ac37286456239dac0b30be8cb4bbe2b90ce8c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BatchPoolCertificateOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__422bffcb9c8a9f327ecc83e0b8f8f988e6bbeadf76f1896409053ce7c4bd8bf1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__91e7a6eb861b9cec8e530fccaabf312de8fb4c5dbb4ce08590c3dc0136573c18)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d34412073206174bf843a2e548e7946850c32449a805b59ee2ccc34597d86cf5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolCertificate]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolCertificate]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolCertificate]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d99091b0bf6daae35457e7d1669ccfd9576f2d5cee8972029b83038e65e60b3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BatchPoolCertificateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolCertificateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__796e152f5a6ed1d15dd95da8dbdd11c80d4b57e2937d1f6256881a6501e2eba6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetStoreName")
    def reset_store_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStoreName", []))

    @jsii.member(jsii_name="resetVisibility")
    def reset_visibility(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVisibility", []))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="storeLocationInput")
    def store_location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storeLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="storeNameInput")
    def store_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storeNameInput"))

    @builtins.property
    @jsii.member(jsii_name="visibilityInput")
    def visibility_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "visibilityInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49a8d9a5a066f103c5646ae73a72e9357e35aeece0277742e448d505895f074f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storeLocation")
    def store_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storeLocation"))

    @store_location.setter
    def store_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__174fa15082175525c08779199f3045e5c476b50417bfa3b8535f0f0654cafab5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storeLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storeName")
    def store_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storeName"))

    @store_name.setter
    def store_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09bdf9aabc67db626d34d514b9262015b6f1a3957b7ae75112cb05cf75a851b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storeName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="visibility")
    def visibility(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "visibility"))

    @visibility.setter
    def visibility(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d1a70945a2d4fc7aedd04d1e9af3dee01bb4c8e8508b43653a95cbcab481794)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "visibility", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolCertificate]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolCertificate]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolCertificate]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d985228b0ba3508b14ec3eedbd8ac8dbf3effef9816b23bdd1226828846b675)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "account_name": "accountName",
        "name": "name",
        "node_agent_sku_id": "nodeAgentSkuId",
        "resource_group_name": "resourceGroupName",
        "storage_image_reference": "storageImageReference",
        "vm_size": "vmSize",
        "auto_scale": "autoScale",
        "certificate": "certificate",
        "container_configuration": "containerConfiguration",
        "data_disks": "dataDisks",
        "disk_encryption": "diskEncryption",
        "display_name": "displayName",
        "extensions": "extensions",
        "fixed_scale": "fixedScale",
        "id": "id",
        "identity": "identity",
        "inter_node_communication": "interNodeCommunication",
        "license_type": "licenseType",
        "max_tasks_per_node": "maxTasksPerNode",
        "metadata": "metadata",
        "mount": "mount",
        "network_configuration": "networkConfiguration",
        "node_placement": "nodePlacement",
        "os_disk_placement": "osDiskPlacement",
        "security_profile": "securityProfile",
        "start_task": "startTask",
        "stop_pending_resize_operation": "stopPendingResizeOperation",
        "target_node_communication_mode": "targetNodeCommunicationMode",
        "task_scheduling_policy": "taskSchedulingPolicy",
        "timeouts": "timeouts",
        "user_accounts": "userAccounts",
        "windows": "windows",
    },
)
class BatchPoolConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        account_name: builtins.str,
        name: builtins.str,
        node_agent_sku_id: builtins.str,
        resource_group_name: builtins.str,
        storage_image_reference: typing.Union["BatchPoolStorageImageReference", typing.Dict[builtins.str, typing.Any]],
        vm_size: builtins.str,
        auto_scale: typing.Optional[typing.Union[BatchPoolAutoScale, typing.Dict[builtins.str, typing.Any]]] = None,
        certificate: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BatchPoolCertificate, typing.Dict[builtins.str, typing.Any]]]]] = None,
        container_configuration: typing.Optional[typing.Union["BatchPoolContainerConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        data_disks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BatchPoolDataDisks", typing.Dict[builtins.str, typing.Any]]]]] = None,
        disk_encryption: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BatchPoolDiskEncryption", typing.Dict[builtins.str, typing.Any]]]]] = None,
        display_name: typing.Optional[builtins.str] = None,
        extensions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BatchPoolExtensions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        fixed_scale: typing.Optional[typing.Union["BatchPoolFixedScale", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        identity: typing.Optional[typing.Union["BatchPoolIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        inter_node_communication: typing.Optional[builtins.str] = None,
        license_type: typing.Optional[builtins.str] = None,
        max_tasks_per_node: typing.Optional[jsii.Number] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        mount: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BatchPoolMount", typing.Dict[builtins.str, typing.Any]]]]] = None,
        network_configuration: typing.Optional[typing.Union["BatchPoolNetworkConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        node_placement: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BatchPoolNodePlacement", typing.Dict[builtins.str, typing.Any]]]]] = None,
        os_disk_placement: typing.Optional[builtins.str] = None,
        security_profile: typing.Optional[typing.Union["BatchPoolSecurityProfile", typing.Dict[builtins.str, typing.Any]]] = None,
        start_task: typing.Optional[typing.Union["BatchPoolStartTask", typing.Dict[builtins.str, typing.Any]]] = None,
        stop_pending_resize_operation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        target_node_communication_mode: typing.Optional[builtins.str] = None,
        task_scheduling_policy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BatchPoolTaskSchedulingPolicy", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["BatchPoolTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        user_accounts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BatchPoolUserAccounts", typing.Dict[builtins.str, typing.Any]]]]] = None,
        windows: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BatchPoolWindows", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param account_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#account_name BatchPool#account_name}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#name BatchPool#name}.
        :param node_agent_sku_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#node_agent_sku_id BatchPool#node_agent_sku_id}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#resource_group_name BatchPool#resource_group_name}.
        :param storage_image_reference: storage_image_reference block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#storage_image_reference BatchPool#storage_image_reference}
        :param vm_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#vm_size BatchPool#vm_size}.
        :param auto_scale: auto_scale block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#auto_scale BatchPool#auto_scale}
        :param certificate: certificate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#certificate BatchPool#certificate}
        :param container_configuration: container_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#container_configuration BatchPool#container_configuration}
        :param data_disks: data_disks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#data_disks BatchPool#data_disks}
        :param disk_encryption: disk_encryption block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#disk_encryption BatchPool#disk_encryption}
        :param display_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#display_name BatchPool#display_name}.
        :param extensions: extensions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#extensions BatchPool#extensions}
        :param fixed_scale: fixed_scale block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#fixed_scale BatchPool#fixed_scale}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#id BatchPool#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity: identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#identity BatchPool#identity}
        :param inter_node_communication: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#inter_node_communication BatchPool#inter_node_communication}.
        :param license_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#license_type BatchPool#license_type}.
        :param max_tasks_per_node: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#max_tasks_per_node BatchPool#max_tasks_per_node}.
        :param metadata: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#metadata BatchPool#metadata}.
        :param mount: mount block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#mount BatchPool#mount}
        :param network_configuration: network_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#network_configuration BatchPool#network_configuration}
        :param node_placement: node_placement block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#node_placement BatchPool#node_placement}
        :param os_disk_placement: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#os_disk_placement BatchPool#os_disk_placement}.
        :param security_profile: security_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#security_profile BatchPool#security_profile}
        :param start_task: start_task block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#start_task BatchPool#start_task}
        :param stop_pending_resize_operation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#stop_pending_resize_operation BatchPool#stop_pending_resize_operation}.
        :param target_node_communication_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#target_node_communication_mode BatchPool#target_node_communication_mode}.
        :param task_scheduling_policy: task_scheduling_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#task_scheduling_policy BatchPool#task_scheduling_policy}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#timeouts BatchPool#timeouts}
        :param user_accounts: user_accounts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#user_accounts BatchPool#user_accounts}
        :param windows: windows block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#windows BatchPool#windows}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(storage_image_reference, dict):
            storage_image_reference = BatchPoolStorageImageReference(**storage_image_reference)
        if isinstance(auto_scale, dict):
            auto_scale = BatchPoolAutoScale(**auto_scale)
        if isinstance(container_configuration, dict):
            container_configuration = BatchPoolContainerConfiguration(**container_configuration)
        if isinstance(fixed_scale, dict):
            fixed_scale = BatchPoolFixedScale(**fixed_scale)
        if isinstance(identity, dict):
            identity = BatchPoolIdentity(**identity)
        if isinstance(network_configuration, dict):
            network_configuration = BatchPoolNetworkConfiguration(**network_configuration)
        if isinstance(security_profile, dict):
            security_profile = BatchPoolSecurityProfile(**security_profile)
        if isinstance(start_task, dict):
            start_task = BatchPoolStartTask(**start_task)
        if isinstance(timeouts, dict):
            timeouts = BatchPoolTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f6eb9c097beed2d19e62c0ae46eba1beb78d7fe028abc742f58c606279012da)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument account_name", value=account_name, expected_type=type_hints["account_name"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument node_agent_sku_id", value=node_agent_sku_id, expected_type=type_hints["node_agent_sku_id"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument storage_image_reference", value=storage_image_reference, expected_type=type_hints["storage_image_reference"])
            check_type(argname="argument vm_size", value=vm_size, expected_type=type_hints["vm_size"])
            check_type(argname="argument auto_scale", value=auto_scale, expected_type=type_hints["auto_scale"])
            check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
            check_type(argname="argument container_configuration", value=container_configuration, expected_type=type_hints["container_configuration"])
            check_type(argname="argument data_disks", value=data_disks, expected_type=type_hints["data_disks"])
            check_type(argname="argument disk_encryption", value=disk_encryption, expected_type=type_hints["disk_encryption"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument extensions", value=extensions, expected_type=type_hints["extensions"])
            check_type(argname="argument fixed_scale", value=fixed_scale, expected_type=type_hints["fixed_scale"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
            check_type(argname="argument inter_node_communication", value=inter_node_communication, expected_type=type_hints["inter_node_communication"])
            check_type(argname="argument license_type", value=license_type, expected_type=type_hints["license_type"])
            check_type(argname="argument max_tasks_per_node", value=max_tasks_per_node, expected_type=type_hints["max_tasks_per_node"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument mount", value=mount, expected_type=type_hints["mount"])
            check_type(argname="argument network_configuration", value=network_configuration, expected_type=type_hints["network_configuration"])
            check_type(argname="argument node_placement", value=node_placement, expected_type=type_hints["node_placement"])
            check_type(argname="argument os_disk_placement", value=os_disk_placement, expected_type=type_hints["os_disk_placement"])
            check_type(argname="argument security_profile", value=security_profile, expected_type=type_hints["security_profile"])
            check_type(argname="argument start_task", value=start_task, expected_type=type_hints["start_task"])
            check_type(argname="argument stop_pending_resize_operation", value=stop_pending_resize_operation, expected_type=type_hints["stop_pending_resize_operation"])
            check_type(argname="argument target_node_communication_mode", value=target_node_communication_mode, expected_type=type_hints["target_node_communication_mode"])
            check_type(argname="argument task_scheduling_policy", value=task_scheduling_policy, expected_type=type_hints["task_scheduling_policy"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument user_accounts", value=user_accounts, expected_type=type_hints["user_accounts"])
            check_type(argname="argument windows", value=windows, expected_type=type_hints["windows"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account_name": account_name,
            "name": name,
            "node_agent_sku_id": node_agent_sku_id,
            "resource_group_name": resource_group_name,
            "storage_image_reference": storage_image_reference,
            "vm_size": vm_size,
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
        if auto_scale is not None:
            self._values["auto_scale"] = auto_scale
        if certificate is not None:
            self._values["certificate"] = certificate
        if container_configuration is not None:
            self._values["container_configuration"] = container_configuration
        if data_disks is not None:
            self._values["data_disks"] = data_disks
        if disk_encryption is not None:
            self._values["disk_encryption"] = disk_encryption
        if display_name is not None:
            self._values["display_name"] = display_name
        if extensions is not None:
            self._values["extensions"] = extensions
        if fixed_scale is not None:
            self._values["fixed_scale"] = fixed_scale
        if id is not None:
            self._values["id"] = id
        if identity is not None:
            self._values["identity"] = identity
        if inter_node_communication is not None:
            self._values["inter_node_communication"] = inter_node_communication
        if license_type is not None:
            self._values["license_type"] = license_type
        if max_tasks_per_node is not None:
            self._values["max_tasks_per_node"] = max_tasks_per_node
        if metadata is not None:
            self._values["metadata"] = metadata
        if mount is not None:
            self._values["mount"] = mount
        if network_configuration is not None:
            self._values["network_configuration"] = network_configuration
        if node_placement is not None:
            self._values["node_placement"] = node_placement
        if os_disk_placement is not None:
            self._values["os_disk_placement"] = os_disk_placement
        if security_profile is not None:
            self._values["security_profile"] = security_profile
        if start_task is not None:
            self._values["start_task"] = start_task
        if stop_pending_resize_operation is not None:
            self._values["stop_pending_resize_operation"] = stop_pending_resize_operation
        if target_node_communication_mode is not None:
            self._values["target_node_communication_mode"] = target_node_communication_mode
        if task_scheduling_policy is not None:
            self._values["task_scheduling_policy"] = task_scheduling_policy
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if user_accounts is not None:
            self._values["user_accounts"] = user_accounts
        if windows is not None:
            self._values["windows"] = windows

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
    def account_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#account_name BatchPool#account_name}.'''
        result = self._values.get("account_name")
        assert result is not None, "Required property 'account_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#name BatchPool#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def node_agent_sku_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#node_agent_sku_id BatchPool#node_agent_sku_id}.'''
        result = self._values.get("node_agent_sku_id")
        assert result is not None, "Required property 'node_agent_sku_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#resource_group_name BatchPool#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_image_reference(self) -> "BatchPoolStorageImageReference":
        '''storage_image_reference block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#storage_image_reference BatchPool#storage_image_reference}
        '''
        result = self._values.get("storage_image_reference")
        assert result is not None, "Required property 'storage_image_reference' is missing"
        return typing.cast("BatchPoolStorageImageReference", result)

    @builtins.property
    def vm_size(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#vm_size BatchPool#vm_size}.'''
        result = self._values.get("vm_size")
        assert result is not None, "Required property 'vm_size' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auto_scale(self) -> typing.Optional[BatchPoolAutoScale]:
        '''auto_scale block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#auto_scale BatchPool#auto_scale}
        '''
        result = self._values.get("auto_scale")
        return typing.cast(typing.Optional[BatchPoolAutoScale], result)

    @builtins.property
    def certificate(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolCertificate]]]:
        '''certificate block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#certificate BatchPool#certificate}
        '''
        result = self._values.get("certificate")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolCertificate]]], result)

    @builtins.property
    def container_configuration(
        self,
    ) -> typing.Optional["BatchPoolContainerConfiguration"]:
        '''container_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#container_configuration BatchPool#container_configuration}
        '''
        result = self._values.get("container_configuration")
        return typing.cast(typing.Optional["BatchPoolContainerConfiguration"], result)

    @builtins.property
    def data_disks(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BatchPoolDataDisks"]]]:
        '''data_disks block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#data_disks BatchPool#data_disks}
        '''
        result = self._values.get("data_disks")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BatchPoolDataDisks"]]], result)

    @builtins.property
    def disk_encryption(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BatchPoolDiskEncryption"]]]:
        '''disk_encryption block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#disk_encryption BatchPool#disk_encryption}
        '''
        result = self._values.get("disk_encryption")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BatchPoolDiskEncryption"]]], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#display_name BatchPool#display_name}.'''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def extensions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BatchPoolExtensions"]]]:
        '''extensions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#extensions BatchPool#extensions}
        '''
        result = self._values.get("extensions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BatchPoolExtensions"]]], result)

    @builtins.property
    def fixed_scale(self) -> typing.Optional["BatchPoolFixedScale"]:
        '''fixed_scale block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#fixed_scale BatchPool#fixed_scale}
        '''
        result = self._values.get("fixed_scale")
        return typing.cast(typing.Optional["BatchPoolFixedScale"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#id BatchPool#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity(self) -> typing.Optional["BatchPoolIdentity"]:
        '''identity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#identity BatchPool#identity}
        '''
        result = self._values.get("identity")
        return typing.cast(typing.Optional["BatchPoolIdentity"], result)

    @builtins.property
    def inter_node_communication(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#inter_node_communication BatchPool#inter_node_communication}.'''
        result = self._values.get("inter_node_communication")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def license_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#license_type BatchPool#license_type}.'''
        result = self._values.get("license_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_tasks_per_node(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#max_tasks_per_node BatchPool#max_tasks_per_node}.'''
        result = self._values.get("max_tasks_per_node")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def metadata(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#metadata BatchPool#metadata}.'''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def mount(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BatchPoolMount"]]]:
        '''mount block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#mount BatchPool#mount}
        '''
        result = self._values.get("mount")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BatchPoolMount"]]], result)

    @builtins.property
    def network_configuration(self) -> typing.Optional["BatchPoolNetworkConfiguration"]:
        '''network_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#network_configuration BatchPool#network_configuration}
        '''
        result = self._values.get("network_configuration")
        return typing.cast(typing.Optional["BatchPoolNetworkConfiguration"], result)

    @builtins.property
    def node_placement(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BatchPoolNodePlacement"]]]:
        '''node_placement block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#node_placement BatchPool#node_placement}
        '''
        result = self._values.get("node_placement")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BatchPoolNodePlacement"]]], result)

    @builtins.property
    def os_disk_placement(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#os_disk_placement BatchPool#os_disk_placement}.'''
        result = self._values.get("os_disk_placement")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_profile(self) -> typing.Optional["BatchPoolSecurityProfile"]:
        '''security_profile block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#security_profile BatchPool#security_profile}
        '''
        result = self._values.get("security_profile")
        return typing.cast(typing.Optional["BatchPoolSecurityProfile"], result)

    @builtins.property
    def start_task(self) -> typing.Optional["BatchPoolStartTask"]:
        '''start_task block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#start_task BatchPool#start_task}
        '''
        result = self._values.get("start_task")
        return typing.cast(typing.Optional["BatchPoolStartTask"], result)

    @builtins.property
    def stop_pending_resize_operation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#stop_pending_resize_operation BatchPool#stop_pending_resize_operation}.'''
        result = self._values.get("stop_pending_resize_operation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def target_node_communication_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#target_node_communication_mode BatchPool#target_node_communication_mode}.'''
        result = self._values.get("target_node_communication_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def task_scheduling_policy(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BatchPoolTaskSchedulingPolicy"]]]:
        '''task_scheduling_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#task_scheduling_policy BatchPool#task_scheduling_policy}
        '''
        result = self._values.get("task_scheduling_policy")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BatchPoolTaskSchedulingPolicy"]]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["BatchPoolTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#timeouts BatchPool#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["BatchPoolTimeouts"], result)

    @builtins.property
    def user_accounts(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BatchPoolUserAccounts"]]]:
        '''user_accounts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#user_accounts BatchPool#user_accounts}
        '''
        result = self._values.get("user_accounts")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BatchPoolUserAccounts"]]], result)

    @builtins.property
    def windows(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BatchPoolWindows"]]]:
        '''windows block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#windows BatchPool#windows}
        '''
        result = self._values.get("windows")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BatchPoolWindows"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BatchPoolConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolContainerConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "container_image_names": "containerImageNames",
        "container_registries": "containerRegistries",
        "type": "type",
    },
)
class BatchPoolContainerConfiguration:
    def __init__(
        self,
        *,
        container_image_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        container_registries: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BatchPoolContainerConfigurationContainerRegistries", typing.Dict[builtins.str, typing.Any]]]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param container_image_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#container_image_names BatchPool#container_image_names}.
        :param container_registries: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#container_registries BatchPool#container_registries}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#type BatchPool#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfada098c0f84c3f146a22230c13f394388c997516e4070450d808dddedc99f2)
            check_type(argname="argument container_image_names", value=container_image_names, expected_type=type_hints["container_image_names"])
            check_type(argname="argument container_registries", value=container_registries, expected_type=type_hints["container_registries"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if container_image_names is not None:
            self._values["container_image_names"] = container_image_names
        if container_registries is not None:
            self._values["container_registries"] = container_registries
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def container_image_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#container_image_names BatchPool#container_image_names}.'''
        result = self._values.get("container_image_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def container_registries(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BatchPoolContainerConfigurationContainerRegistries"]]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#container_registries BatchPool#container_registries}.'''
        result = self._values.get("container_registries")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BatchPoolContainerConfigurationContainerRegistries"]]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#type BatchPool#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BatchPoolContainerConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolContainerConfigurationContainerRegistries",
    jsii_struct_bases=[],
    name_mapping={
        "password": "password",
        "registry_server": "registryServer",
        "user_assigned_identity_id": "userAssignedIdentityId",
        "user_name": "userName",
    },
)
class BatchPoolContainerConfigurationContainerRegistries:
    def __init__(
        self,
        *,
        password: typing.Optional[builtins.str] = None,
        registry_server: typing.Optional[builtins.str] = None,
        user_assigned_identity_id: typing.Optional[builtins.str] = None,
        user_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#password BatchPool#password}.
        :param registry_server: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#registry_server BatchPool#registry_server}.
        :param user_assigned_identity_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#user_assigned_identity_id BatchPool#user_assigned_identity_id}.
        :param user_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#user_name BatchPool#user_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45a17df620eadcf077b70b088960155eb277265051c238d66c680886f69b557f)
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument registry_server", value=registry_server, expected_type=type_hints["registry_server"])
            check_type(argname="argument user_assigned_identity_id", value=user_assigned_identity_id, expected_type=type_hints["user_assigned_identity_id"])
            check_type(argname="argument user_name", value=user_name, expected_type=type_hints["user_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if password is not None:
            self._values["password"] = password
        if registry_server is not None:
            self._values["registry_server"] = registry_server
        if user_assigned_identity_id is not None:
            self._values["user_assigned_identity_id"] = user_assigned_identity_id
        if user_name is not None:
            self._values["user_name"] = user_name

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#password BatchPool#password}.'''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def registry_server(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#registry_server BatchPool#registry_server}.'''
        result = self._values.get("registry_server")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_assigned_identity_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#user_assigned_identity_id BatchPool#user_assigned_identity_id}.'''
        result = self._values.get("user_assigned_identity_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#user_name BatchPool#user_name}.'''
        result = self._values.get("user_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BatchPoolContainerConfigurationContainerRegistries(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BatchPoolContainerConfigurationContainerRegistriesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolContainerConfigurationContainerRegistriesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7056807b99fefd1c66d83f24c811bde7c3c0c745289b3bf98664b3af8640ae7c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BatchPoolContainerConfigurationContainerRegistriesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37404873f927c1e932ddee4426d83e57b74d1f6260597b59581215293cc5d0ad)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BatchPoolContainerConfigurationContainerRegistriesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__345815373dea00e2cf45d116c8df536b7405ea79b8c7bce8360d59ba14d291b0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__55179a0b174db52b8bf0ea4abb39b312e9982b90e24691d641cc8824ade23a37)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e35a65583ed202f06a9c4eb353e406924559bb90462ff503dce1f9d1d85ee2e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolContainerConfigurationContainerRegistries]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolContainerConfigurationContainerRegistries]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolContainerConfigurationContainerRegistries]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c3f98c0c751a450a01b0beeb12669ab567a572351334cbb71570853b3ecc9ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BatchPoolContainerConfigurationContainerRegistriesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolContainerConfigurationContainerRegistriesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__586f8288df8d36df2731c8d6f23c4820fe919eda6697b9a160b90f36349a9d6f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @jsii.member(jsii_name="resetRegistryServer")
    def reset_registry_server(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegistryServer", []))

    @jsii.member(jsii_name="resetUserAssignedIdentityId")
    def reset_user_assigned_identity_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserAssignedIdentityId", []))

    @jsii.member(jsii_name="resetUserName")
    def reset_user_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserName", []))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="registryServerInput")
    def registry_server_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "registryServerInput"))

    @builtins.property
    @jsii.member(jsii_name="userAssignedIdentityIdInput")
    def user_assigned_identity_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userAssignedIdentityIdInput"))

    @builtins.property
    @jsii.member(jsii_name="userNameInput")
    def user_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userNameInput"))

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25eb9f974350ff0ba1fae170da49d3ec85591778cca7900ce570bdaf915de27f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="registryServer")
    def registry_server(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "registryServer"))

    @registry_server.setter
    def registry_server(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f469e4ab0f783f71cef77c35814e0c8388042e0259f596588b1a140dbab5da9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "registryServer", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userAssignedIdentityId")
    def user_assigned_identity_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userAssignedIdentityId"))

    @user_assigned_identity_id.setter
    def user_assigned_identity_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9994e326908bf527065fac65a09d767f1bc96b7c748f97875307d5823535f9fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userAssignedIdentityId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userName")
    def user_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userName"))

    @user_name.setter
    def user_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcc41525a9a46077072c94114f3aafcf62a42a67d88b97880cb1bcf70fd9f065)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolContainerConfigurationContainerRegistries]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolContainerConfigurationContainerRegistries]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolContainerConfigurationContainerRegistries]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f862b7a1e3083468d99891bc83e4d06b1d38272c0ced347d844ce3065cb4960d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BatchPoolContainerConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolContainerConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__89c9f8233c46523369e9da7ecc546238fc1ab7f54bfa014bee2502388dc4fdda)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putContainerRegistries")
    def put_container_registries(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BatchPoolContainerConfigurationContainerRegistries, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a24759a85fe059eb1441a0c40bd502b7ddb3ecc14acb8a4ea7826ef853ca785)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putContainerRegistries", [value]))

    @jsii.member(jsii_name="resetContainerImageNames")
    def reset_container_image_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerImageNames", []))

    @jsii.member(jsii_name="resetContainerRegistries")
    def reset_container_registries(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerRegistries", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="containerRegistries")
    def container_registries(
        self,
    ) -> BatchPoolContainerConfigurationContainerRegistriesList:
        return typing.cast(BatchPoolContainerConfigurationContainerRegistriesList, jsii.get(self, "containerRegistries"))

    @builtins.property
    @jsii.member(jsii_name="containerImageNamesInput")
    def container_image_names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "containerImageNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="containerRegistriesInput")
    def container_registries_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolContainerConfigurationContainerRegistries]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolContainerConfigurationContainerRegistries]]], jsii.get(self, "containerRegistriesInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="containerImageNames")
    def container_image_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "containerImageNames"))

    @container_image_names.setter
    def container_image_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c613da81fae3db2118b6098529cec815f5cf630ac050e3f99663ed6b8b9a7adc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerImageNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5c33e09bb8120fedd5141fe00739abaa3e614d4cf8219b87c8ef0ef416f6594)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BatchPoolContainerConfiguration]:
        return typing.cast(typing.Optional[BatchPoolContainerConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BatchPoolContainerConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14db885f377d903c266d50d1ff8198805b1c8604febe716e3f656e540736fa61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolDataDisks",
    jsii_struct_bases=[],
    name_mapping={
        "disk_size_gb": "diskSizeGb",
        "lun": "lun",
        "caching": "caching",
        "storage_account_type": "storageAccountType",
    },
)
class BatchPoolDataDisks:
    def __init__(
        self,
        *,
        disk_size_gb: jsii.Number,
        lun: jsii.Number,
        caching: typing.Optional[builtins.str] = None,
        storage_account_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param disk_size_gb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#disk_size_gb BatchPool#disk_size_gb}.
        :param lun: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#lun BatchPool#lun}.
        :param caching: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#caching BatchPool#caching}.
        :param storage_account_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#storage_account_type BatchPool#storage_account_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35aca359df5cb87bfef12127a82cd948c2c6aa352102a9c98bc445bead07bf11)
            check_type(argname="argument disk_size_gb", value=disk_size_gb, expected_type=type_hints["disk_size_gb"])
            check_type(argname="argument lun", value=lun, expected_type=type_hints["lun"])
            check_type(argname="argument caching", value=caching, expected_type=type_hints["caching"])
            check_type(argname="argument storage_account_type", value=storage_account_type, expected_type=type_hints["storage_account_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "disk_size_gb": disk_size_gb,
            "lun": lun,
        }
        if caching is not None:
            self._values["caching"] = caching
        if storage_account_type is not None:
            self._values["storage_account_type"] = storage_account_type

    @builtins.property
    def disk_size_gb(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#disk_size_gb BatchPool#disk_size_gb}.'''
        result = self._values.get("disk_size_gb")
        assert result is not None, "Required property 'disk_size_gb' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def lun(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#lun BatchPool#lun}.'''
        result = self._values.get("lun")
        assert result is not None, "Required property 'lun' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def caching(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#caching BatchPool#caching}.'''
        result = self._values.get("caching")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_account_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#storage_account_type BatchPool#storage_account_type}.'''
        result = self._values.get("storage_account_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BatchPoolDataDisks(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BatchPoolDataDisksList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolDataDisksList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d477f5a0fed8996272406d4e7ba37d57572b6f160dcddb5b12bf38345f49011)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "BatchPoolDataDisksOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77bb319c3049dcb656a8aaf9886bce538877a68d12acecf086e76466ad134099)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BatchPoolDataDisksOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94f6c5951bac3265141ba6826f60100a486362d3fc2b07250424b24e6381fa1a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c2e2826cf5a9b348d0de5163eec6ccf01bfe8bf6da1f1f2aab328100ba547dd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e6386d3074c11659eef88e11cb8d8e92e6c4de9037ec11240d931d3b8526de2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolDataDisks]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolDataDisks]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolDataDisks]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dccd20a019851228c21d6809c551e5fe8e024e5f5092c227f107339a5c3d9a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BatchPoolDataDisksOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolDataDisksOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4433915d35a04f4f773e6309b6002bd7636176ff9bdce26c6a376bc60df59cc4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetCaching")
    def reset_caching(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCaching", []))

    @jsii.member(jsii_name="resetStorageAccountType")
    def reset_storage_account_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageAccountType", []))

    @builtins.property
    @jsii.member(jsii_name="cachingInput")
    def caching_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cachingInput"))

    @builtins.property
    @jsii.member(jsii_name="diskSizeGbInput")
    def disk_size_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "diskSizeGbInput"))

    @builtins.property
    @jsii.member(jsii_name="lunInput")
    def lun_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "lunInput"))

    @builtins.property
    @jsii.member(jsii_name="storageAccountTypeInput")
    def storage_account_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageAccountTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="caching")
    def caching(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "caching"))

    @caching.setter
    def caching(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04bf5efb79ce6c8f198082129939e9d7bc90882c12747593130a315928e70771)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "caching", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskSizeGb")
    def disk_size_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "diskSizeGb"))

    @disk_size_gb.setter
    def disk_size_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1d530976bc3813a3224706dabe884c7fc5f8a2b3f1e396a52ad4c7e47b98e09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskSizeGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lun")
    def lun(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "lun"))

    @lun.setter
    def lun(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f27c785bdb3c2c19f9129fe4e2551e59b5b8f030c853cfafef61be45a19cb877)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lun", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageAccountType")
    def storage_account_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageAccountType"))

    @storage_account_type.setter
    def storage_account_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc8fcc38d424fbfebc45310ac5f0cc47a655d69eff6f94b31ad45fa2f7d7d937)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageAccountType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolDataDisks]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolDataDisks]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolDataDisks]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef27b8686d23134c66b24f0e53ba87f1a8005ede087e285ef6c30541ea728941)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolDiskEncryption",
    jsii_struct_bases=[],
    name_mapping={"disk_encryption_target": "diskEncryptionTarget"},
)
class BatchPoolDiskEncryption:
    def __init__(self, *, disk_encryption_target: builtins.str) -> None:
        '''
        :param disk_encryption_target: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#disk_encryption_target BatchPool#disk_encryption_target}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__287173c4afaa43ef6d4f32e1a7f1fed8325099141c8b2df151cc7d07c86285f4)
            check_type(argname="argument disk_encryption_target", value=disk_encryption_target, expected_type=type_hints["disk_encryption_target"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "disk_encryption_target": disk_encryption_target,
        }

    @builtins.property
    def disk_encryption_target(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#disk_encryption_target BatchPool#disk_encryption_target}.'''
        result = self._values.get("disk_encryption_target")
        assert result is not None, "Required property 'disk_encryption_target' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BatchPoolDiskEncryption(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BatchPoolDiskEncryptionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolDiskEncryptionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f1d4c8da693cb8917fdb4dd659899885377925ec2d0d4f15d28453e36a66b23)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "BatchPoolDiskEncryptionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74637b1612e23460e2c90aef1837757c070940fe3400315d3f7a63a94bf6e37c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BatchPoolDiskEncryptionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a74d2c9510b9bb771c04c712e854aed49d5d8da8c6444fc3ff581698ef30c45)
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
            type_hints = typing.get_type_hints(_typecheckingstub__92e6b50ad65ac11685b1db0877fcbdb8cf1a1a51f631b33be92a84d55b463753)
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
            type_hints = typing.get_type_hints(_typecheckingstub__93ea1f98a2bfe5cfecd7e8573d9ea232cbfb352b110905cffa5e990a69a06ee2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolDiskEncryption]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolDiskEncryption]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolDiskEncryption]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d97e26a696eea2299a1e4cf10b25544f99def4e2c121b18fbf56f63793c4b9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BatchPoolDiskEncryptionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolDiskEncryptionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__96cc27ffa34e3e8c1b292b1a5f2b0d7a4ccf48846ad45c9fdb0fdc1a5ed86652)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="diskEncryptionTargetInput")
    def disk_encryption_target_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "diskEncryptionTargetInput"))

    @builtins.property
    @jsii.member(jsii_name="diskEncryptionTarget")
    def disk_encryption_target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskEncryptionTarget"))

    @disk_encryption_target.setter
    def disk_encryption_target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ca4c68f432cdac162675cb186a9fe555b9dc8e23a8bddf109ca90a642b92e7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskEncryptionTarget", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolDiskEncryption]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolDiskEncryption]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolDiskEncryption]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ac4701eddf1fca7504fb61621753fbfa98db7e92c3973716c737f30a816f6d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolExtensions",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "publisher": "publisher",
        "type": "type",
        "automatic_upgrade_enabled": "automaticUpgradeEnabled",
        "auto_upgrade_minor_version": "autoUpgradeMinorVersion",
        "protected_settings": "protectedSettings",
        "provision_after_extensions": "provisionAfterExtensions",
        "settings_json": "settingsJson",
        "type_handler_version": "typeHandlerVersion",
    },
)
class BatchPoolExtensions:
    def __init__(
        self,
        *,
        name: builtins.str,
        publisher: builtins.str,
        type: builtins.str,
        automatic_upgrade_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        auto_upgrade_minor_version: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        protected_settings: typing.Optional[builtins.str] = None,
        provision_after_extensions: typing.Optional[typing.Sequence[builtins.str]] = None,
        settings_json: typing.Optional[builtins.str] = None,
        type_handler_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#name BatchPool#name}.
        :param publisher: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#publisher BatchPool#publisher}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#type BatchPool#type}.
        :param automatic_upgrade_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#automatic_upgrade_enabled BatchPool#automatic_upgrade_enabled}.
        :param auto_upgrade_minor_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#auto_upgrade_minor_version BatchPool#auto_upgrade_minor_version}.
        :param protected_settings: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#protected_settings BatchPool#protected_settings}.
        :param provision_after_extensions: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#provision_after_extensions BatchPool#provision_after_extensions}.
        :param settings_json: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#settings_json BatchPool#settings_json}.
        :param type_handler_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#type_handler_version BatchPool#type_handler_version}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c418dbe46a4a9fdd67f33efc6fd4cb25b42aa13650298acdbe4e9772dbfe4015)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument publisher", value=publisher, expected_type=type_hints["publisher"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument automatic_upgrade_enabled", value=automatic_upgrade_enabled, expected_type=type_hints["automatic_upgrade_enabled"])
            check_type(argname="argument auto_upgrade_minor_version", value=auto_upgrade_minor_version, expected_type=type_hints["auto_upgrade_minor_version"])
            check_type(argname="argument protected_settings", value=protected_settings, expected_type=type_hints["protected_settings"])
            check_type(argname="argument provision_after_extensions", value=provision_after_extensions, expected_type=type_hints["provision_after_extensions"])
            check_type(argname="argument settings_json", value=settings_json, expected_type=type_hints["settings_json"])
            check_type(argname="argument type_handler_version", value=type_handler_version, expected_type=type_hints["type_handler_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "publisher": publisher,
            "type": type,
        }
        if automatic_upgrade_enabled is not None:
            self._values["automatic_upgrade_enabled"] = automatic_upgrade_enabled
        if auto_upgrade_minor_version is not None:
            self._values["auto_upgrade_minor_version"] = auto_upgrade_minor_version
        if protected_settings is not None:
            self._values["protected_settings"] = protected_settings
        if provision_after_extensions is not None:
            self._values["provision_after_extensions"] = provision_after_extensions
        if settings_json is not None:
            self._values["settings_json"] = settings_json
        if type_handler_version is not None:
            self._values["type_handler_version"] = type_handler_version

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#name BatchPool#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def publisher(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#publisher BatchPool#publisher}.'''
        result = self._values.get("publisher")
        assert result is not None, "Required property 'publisher' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#type BatchPool#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def automatic_upgrade_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#automatic_upgrade_enabled BatchPool#automatic_upgrade_enabled}.'''
        result = self._values.get("automatic_upgrade_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def auto_upgrade_minor_version(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#auto_upgrade_minor_version BatchPool#auto_upgrade_minor_version}.'''
        result = self._values.get("auto_upgrade_minor_version")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def protected_settings(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#protected_settings BatchPool#protected_settings}.'''
        result = self._values.get("protected_settings")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def provision_after_extensions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#provision_after_extensions BatchPool#provision_after_extensions}.'''
        result = self._values.get("provision_after_extensions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def settings_json(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#settings_json BatchPool#settings_json}.'''
        result = self._values.get("settings_json")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type_handler_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#type_handler_version BatchPool#type_handler_version}.'''
        result = self._values.get("type_handler_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BatchPoolExtensions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BatchPoolExtensionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolExtensionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__df3ae2bc448a540e888d670c20a8e223d1e5aef8ada6fd845db3a4115d07b827)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "BatchPoolExtensionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8d28c14a718f272f58c3edb5e8e76abd6320850894798b5c37a14b8b8e79c7f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BatchPoolExtensionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e859d2ebd92118ba47d2d88655c7e7ea32b8eeb1e14b7f9e760d5fdb51dbf78)
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
            type_hints = typing.get_type_hints(_typecheckingstub__db938ab15df83a5da06f70145ca1a812c5e3b5a802902327fb73ee05792a3c50)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cdac3372c73cb74e2dc31b830731fbec466ab09fcfb282d827ffbd74b2d77d6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolExtensions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolExtensions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolExtensions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0523fa0febbff3c1ab0c0594205739667dff8c10352153e6286aed25bf85e24b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BatchPoolExtensionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolExtensionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e130816bf36e099fee1e0a2555d022fe7adc7400d3d9befd30eae3d826c60bf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAutomaticUpgradeEnabled")
    def reset_automatic_upgrade_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutomaticUpgradeEnabled", []))

    @jsii.member(jsii_name="resetAutoUpgradeMinorVersion")
    def reset_auto_upgrade_minor_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoUpgradeMinorVersion", []))

    @jsii.member(jsii_name="resetProtectedSettings")
    def reset_protected_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProtectedSettings", []))

    @jsii.member(jsii_name="resetProvisionAfterExtensions")
    def reset_provision_after_extensions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProvisionAfterExtensions", []))

    @jsii.member(jsii_name="resetSettingsJson")
    def reset_settings_json(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSettingsJson", []))

    @jsii.member(jsii_name="resetTypeHandlerVersion")
    def reset_type_handler_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTypeHandlerVersion", []))

    @builtins.property
    @jsii.member(jsii_name="automaticUpgradeEnabledInput")
    def automatic_upgrade_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "automaticUpgradeEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="autoUpgradeMinorVersionInput")
    def auto_upgrade_minor_version_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "autoUpgradeMinorVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="protectedSettingsInput")
    def protected_settings_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protectedSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="provisionAfterExtensionsInput")
    def provision_after_extensions_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "provisionAfterExtensionsInput"))

    @builtins.property
    @jsii.member(jsii_name="publisherInput")
    def publisher_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "publisherInput"))

    @builtins.property
    @jsii.member(jsii_name="settingsJsonInput")
    def settings_json_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "settingsJsonInput"))

    @builtins.property
    @jsii.member(jsii_name="typeHandlerVersionInput")
    def type_handler_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeHandlerVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="automaticUpgradeEnabled")
    def automatic_upgrade_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "automaticUpgradeEnabled"))

    @automatic_upgrade_enabled.setter
    def automatic_upgrade_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb31fd58ea19fc171a413a00ce3e3083beb77ecebc3c2a8f705d4f69213c89ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "automaticUpgradeEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="autoUpgradeMinorVersion")
    def auto_upgrade_minor_version(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "autoUpgradeMinorVersion"))

    @auto_upgrade_minor_version.setter
    def auto_upgrade_minor_version(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__431f4c52df85a648997f116230e7c3aa0a5be53bca6673d6b0f61df25aaabe2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoUpgradeMinorVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1e2dce5f1cf5b7bf204be5b4de0766a40a4dedac349d389b634b7a99d8ce496)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protectedSettings")
    def protected_settings(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protectedSettings"))

    @protected_settings.setter
    def protected_settings(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d359fde8efb95262bc7469241e0e40f6057e5ab2ae9829ee3f97f906ae5871b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protectedSettings", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="provisionAfterExtensions")
    def provision_after_extensions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "provisionAfterExtensions"))

    @provision_after_extensions.setter
    def provision_after_extensions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b086271ff164287791b5873e2a698770035cffc55076c60fa15528a5d21de5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "provisionAfterExtensions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publisher")
    def publisher(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publisher"))

    @publisher.setter
    def publisher(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0e18fd3404bcf8bc483870d008eb47e9670566cc3193f4e646c80c7c84aab20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publisher", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="settingsJson")
    def settings_json(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "settingsJson"))

    @settings_json.setter
    def settings_json(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e2cee0fefb109207c5600e8c3be441d18af64e686038565c7c75d5cd4c599b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "settingsJson", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ddc4cedbfeafa5b962796f05cc4f428b1a14b6f84b8b0d314bd693ec03207f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="typeHandlerVersion")
    def type_handler_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "typeHandlerVersion"))

    @type_handler_version.setter
    def type_handler_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38fd4838082223a6b8e7948324b33b278e4639fca4b445450dc8232e81dc220f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "typeHandlerVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolExtensions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolExtensions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolExtensions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__066f3261a784317d743fab24784e1f1217f0703bad7ee3f4854689ef2071dd6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolFixedScale",
    jsii_struct_bases=[],
    name_mapping={
        "node_deallocation_method": "nodeDeallocationMethod",
        "resize_timeout": "resizeTimeout",
        "target_dedicated_nodes": "targetDedicatedNodes",
        "target_low_priority_nodes": "targetLowPriorityNodes",
    },
)
class BatchPoolFixedScale:
    def __init__(
        self,
        *,
        node_deallocation_method: typing.Optional[builtins.str] = None,
        resize_timeout: typing.Optional[builtins.str] = None,
        target_dedicated_nodes: typing.Optional[jsii.Number] = None,
        target_low_priority_nodes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param node_deallocation_method: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#node_deallocation_method BatchPool#node_deallocation_method}.
        :param resize_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#resize_timeout BatchPool#resize_timeout}.
        :param target_dedicated_nodes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#target_dedicated_nodes BatchPool#target_dedicated_nodes}.
        :param target_low_priority_nodes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#target_low_priority_nodes BatchPool#target_low_priority_nodes}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d9dd60afd90ab16965ec3002969a958196d8b83e355bbfdaa4fcc0f3c4cac57)
            check_type(argname="argument node_deallocation_method", value=node_deallocation_method, expected_type=type_hints["node_deallocation_method"])
            check_type(argname="argument resize_timeout", value=resize_timeout, expected_type=type_hints["resize_timeout"])
            check_type(argname="argument target_dedicated_nodes", value=target_dedicated_nodes, expected_type=type_hints["target_dedicated_nodes"])
            check_type(argname="argument target_low_priority_nodes", value=target_low_priority_nodes, expected_type=type_hints["target_low_priority_nodes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if node_deallocation_method is not None:
            self._values["node_deallocation_method"] = node_deallocation_method
        if resize_timeout is not None:
            self._values["resize_timeout"] = resize_timeout
        if target_dedicated_nodes is not None:
            self._values["target_dedicated_nodes"] = target_dedicated_nodes
        if target_low_priority_nodes is not None:
            self._values["target_low_priority_nodes"] = target_low_priority_nodes

    @builtins.property
    def node_deallocation_method(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#node_deallocation_method BatchPool#node_deallocation_method}.'''
        result = self._values.get("node_deallocation_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resize_timeout(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#resize_timeout BatchPool#resize_timeout}.'''
        result = self._values.get("resize_timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_dedicated_nodes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#target_dedicated_nodes BatchPool#target_dedicated_nodes}.'''
        result = self._values.get("target_dedicated_nodes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def target_low_priority_nodes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#target_low_priority_nodes BatchPool#target_low_priority_nodes}.'''
        result = self._values.get("target_low_priority_nodes")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BatchPoolFixedScale(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BatchPoolFixedScaleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolFixedScaleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a370d007823cc895849380309db255ccf49b35aaceb01b8c52c574db4468fa4e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetNodeDeallocationMethod")
    def reset_node_deallocation_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeDeallocationMethod", []))

    @jsii.member(jsii_name="resetResizeTimeout")
    def reset_resize_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResizeTimeout", []))

    @jsii.member(jsii_name="resetTargetDedicatedNodes")
    def reset_target_dedicated_nodes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetDedicatedNodes", []))

    @jsii.member(jsii_name="resetTargetLowPriorityNodes")
    def reset_target_low_priority_nodes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetLowPriorityNodes", []))

    @builtins.property
    @jsii.member(jsii_name="nodeDeallocationMethodInput")
    def node_deallocation_method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nodeDeallocationMethodInput"))

    @builtins.property
    @jsii.member(jsii_name="resizeTimeoutInput")
    def resize_timeout_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resizeTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="targetDedicatedNodesInput")
    def target_dedicated_nodes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "targetDedicatedNodesInput"))

    @builtins.property
    @jsii.member(jsii_name="targetLowPriorityNodesInput")
    def target_low_priority_nodes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "targetLowPriorityNodesInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeDeallocationMethod")
    def node_deallocation_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeDeallocationMethod"))

    @node_deallocation_method.setter
    def node_deallocation_method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a23b0104657e0a420dcf1f1736c49e0703a0a9db53f2d6520b8e92c7de5f28e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeDeallocationMethod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resizeTimeout")
    def resize_timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resizeTimeout"))

    @resize_timeout.setter
    def resize_timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9161840ab5598e5a95e5b482514abf2e6a6cbe03b320097ad00a7dd16c59f571)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resizeTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetDedicatedNodes")
    def target_dedicated_nodes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "targetDedicatedNodes"))

    @target_dedicated_nodes.setter
    def target_dedicated_nodes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51bd40320a74c9e991395bbc1b70a66e011ac7ee6e936e46e43d8e568793d16c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetDedicatedNodes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetLowPriorityNodes")
    def target_low_priority_nodes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "targetLowPriorityNodes"))

    @target_low_priority_nodes.setter
    def target_low_priority_nodes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f985ac344abe3aec2f9400ce47c9af01f50359597bba70d68ff9bca5ba2cfee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetLowPriorityNodes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BatchPoolFixedScale]:
        return typing.cast(typing.Optional[BatchPoolFixedScale], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[BatchPoolFixedScale]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e201f86b3e65801e0e71602c8dda2a8a36465c72c0f4b9d08ad6581a35b5e71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolIdentity",
    jsii_struct_bases=[],
    name_mapping={"identity_ids": "identityIds", "type": "type"},
)
class BatchPoolIdentity:
    def __init__(
        self,
        *,
        identity_ids: typing.Sequence[builtins.str],
        type: builtins.str,
    ) -> None:
        '''
        :param identity_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#identity_ids BatchPool#identity_ids}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#type BatchPool#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52492b24aec6855f9a7361602a0ce22220aab152985054f52e8a8ca1e3d8c157)
            check_type(argname="argument identity_ids", value=identity_ids, expected_type=type_hints["identity_ids"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "identity_ids": identity_ids,
            "type": type,
        }

    @builtins.property
    def identity_ids(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#identity_ids BatchPool#identity_ids}.'''
        result = self._values.get("identity_ids")
        assert result is not None, "Required property 'identity_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#type BatchPool#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BatchPoolIdentity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BatchPoolIdentityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolIdentityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__33c1a3afb52bcc0eb7d3e9dc26448ea5dc6c1215e1bf0eefb47192602bab498e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

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
            type_hints = typing.get_type_hints(_typecheckingstub__991f6742cb70f264e2251e88b181679e778cc2d8a6db9c0adb26ce44374b485b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2ec1fdea69b08dc0c52392a5b187c8685e6efac8fff4d78589d0a86b4e7390d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BatchPoolIdentity]:
        return typing.cast(typing.Optional[BatchPoolIdentity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[BatchPoolIdentity]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89fa856916b0e18fda0f2665cb22c497f45bb5e319b235bb95c7ef52de7e8976)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolMount",
    jsii_struct_bases=[],
    name_mapping={
        "azure_blob_file_system": "azureBlobFileSystem",
        "azure_file_share": "azureFileShare",
        "cifs_mount": "cifsMount",
        "nfs_mount": "nfsMount",
    },
)
class BatchPoolMount:
    def __init__(
        self,
        *,
        azure_blob_file_system: typing.Optional[typing.Union["BatchPoolMountAzureBlobFileSystem", typing.Dict[builtins.str, typing.Any]]] = None,
        azure_file_share: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BatchPoolMountAzureFileShare", typing.Dict[builtins.str, typing.Any]]]]] = None,
        cifs_mount: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BatchPoolMountCifsMount", typing.Dict[builtins.str, typing.Any]]]]] = None,
        nfs_mount: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BatchPoolMountNfsMount", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param azure_blob_file_system: azure_blob_file_system block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#azure_blob_file_system BatchPool#azure_blob_file_system}
        :param azure_file_share: azure_file_share block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#azure_file_share BatchPool#azure_file_share}
        :param cifs_mount: cifs_mount block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#cifs_mount BatchPool#cifs_mount}
        :param nfs_mount: nfs_mount block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#nfs_mount BatchPool#nfs_mount}
        '''
        if isinstance(azure_blob_file_system, dict):
            azure_blob_file_system = BatchPoolMountAzureBlobFileSystem(**azure_blob_file_system)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfc35f2df5b0c8f66bfd8110cc3c403b31c17ce00ecded4b56106f64e4cb1ca9)
            check_type(argname="argument azure_blob_file_system", value=azure_blob_file_system, expected_type=type_hints["azure_blob_file_system"])
            check_type(argname="argument azure_file_share", value=azure_file_share, expected_type=type_hints["azure_file_share"])
            check_type(argname="argument cifs_mount", value=cifs_mount, expected_type=type_hints["cifs_mount"])
            check_type(argname="argument nfs_mount", value=nfs_mount, expected_type=type_hints["nfs_mount"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if azure_blob_file_system is not None:
            self._values["azure_blob_file_system"] = azure_blob_file_system
        if azure_file_share is not None:
            self._values["azure_file_share"] = azure_file_share
        if cifs_mount is not None:
            self._values["cifs_mount"] = cifs_mount
        if nfs_mount is not None:
            self._values["nfs_mount"] = nfs_mount

    @builtins.property
    def azure_blob_file_system(
        self,
    ) -> typing.Optional["BatchPoolMountAzureBlobFileSystem"]:
        '''azure_blob_file_system block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#azure_blob_file_system BatchPool#azure_blob_file_system}
        '''
        result = self._values.get("azure_blob_file_system")
        return typing.cast(typing.Optional["BatchPoolMountAzureBlobFileSystem"], result)

    @builtins.property
    def azure_file_share(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BatchPoolMountAzureFileShare"]]]:
        '''azure_file_share block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#azure_file_share BatchPool#azure_file_share}
        '''
        result = self._values.get("azure_file_share")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BatchPoolMountAzureFileShare"]]], result)

    @builtins.property
    def cifs_mount(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BatchPoolMountCifsMount"]]]:
        '''cifs_mount block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#cifs_mount BatchPool#cifs_mount}
        '''
        result = self._values.get("cifs_mount")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BatchPoolMountCifsMount"]]], result)

    @builtins.property
    def nfs_mount(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BatchPoolMountNfsMount"]]]:
        '''nfs_mount block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#nfs_mount BatchPool#nfs_mount}
        '''
        result = self._values.get("nfs_mount")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BatchPoolMountNfsMount"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BatchPoolMount(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolMountAzureBlobFileSystem",
    jsii_struct_bases=[],
    name_mapping={
        "account_name": "accountName",
        "container_name": "containerName",
        "relative_mount_path": "relativeMountPath",
        "account_key": "accountKey",
        "blobfuse_options": "blobfuseOptions",
        "identity_id": "identityId",
        "sas_key": "sasKey",
    },
)
class BatchPoolMountAzureBlobFileSystem:
    def __init__(
        self,
        *,
        account_name: builtins.str,
        container_name: builtins.str,
        relative_mount_path: builtins.str,
        account_key: typing.Optional[builtins.str] = None,
        blobfuse_options: typing.Optional[builtins.str] = None,
        identity_id: typing.Optional[builtins.str] = None,
        sas_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param account_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#account_name BatchPool#account_name}.
        :param container_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#container_name BatchPool#container_name}.
        :param relative_mount_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#relative_mount_path BatchPool#relative_mount_path}.
        :param account_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#account_key BatchPool#account_key}.
        :param blobfuse_options: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#blobfuse_options BatchPool#blobfuse_options}.
        :param identity_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#identity_id BatchPool#identity_id}.
        :param sas_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#sas_key BatchPool#sas_key}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6defbd93299ac018afd24f97a882bfee9ac4622066462cd36eb65788d0026f2d)
            check_type(argname="argument account_name", value=account_name, expected_type=type_hints["account_name"])
            check_type(argname="argument container_name", value=container_name, expected_type=type_hints["container_name"])
            check_type(argname="argument relative_mount_path", value=relative_mount_path, expected_type=type_hints["relative_mount_path"])
            check_type(argname="argument account_key", value=account_key, expected_type=type_hints["account_key"])
            check_type(argname="argument blobfuse_options", value=blobfuse_options, expected_type=type_hints["blobfuse_options"])
            check_type(argname="argument identity_id", value=identity_id, expected_type=type_hints["identity_id"])
            check_type(argname="argument sas_key", value=sas_key, expected_type=type_hints["sas_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account_name": account_name,
            "container_name": container_name,
            "relative_mount_path": relative_mount_path,
        }
        if account_key is not None:
            self._values["account_key"] = account_key
        if blobfuse_options is not None:
            self._values["blobfuse_options"] = blobfuse_options
        if identity_id is not None:
            self._values["identity_id"] = identity_id
        if sas_key is not None:
            self._values["sas_key"] = sas_key

    @builtins.property
    def account_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#account_name BatchPool#account_name}.'''
        result = self._values.get("account_name")
        assert result is not None, "Required property 'account_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def container_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#container_name BatchPool#container_name}.'''
        result = self._values.get("container_name")
        assert result is not None, "Required property 'container_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def relative_mount_path(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#relative_mount_path BatchPool#relative_mount_path}.'''
        result = self._values.get("relative_mount_path")
        assert result is not None, "Required property 'relative_mount_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def account_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#account_key BatchPool#account_key}.'''
        result = self._values.get("account_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def blobfuse_options(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#blobfuse_options BatchPool#blobfuse_options}.'''
        result = self._values.get("blobfuse_options")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#identity_id BatchPool#identity_id}.'''
        result = self._values.get("identity_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sas_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#sas_key BatchPool#sas_key}.'''
        result = self._values.get("sas_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BatchPoolMountAzureBlobFileSystem(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BatchPoolMountAzureBlobFileSystemOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolMountAzureBlobFileSystemOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f51b125d927148c305a581f9a78e734d2140aba797e006d6f91ee62beb473c8e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAccountKey")
    def reset_account_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountKey", []))

    @jsii.member(jsii_name="resetBlobfuseOptions")
    def reset_blobfuse_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBlobfuseOptions", []))

    @jsii.member(jsii_name="resetIdentityId")
    def reset_identity_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentityId", []))

    @jsii.member(jsii_name="resetSasKey")
    def reset_sas_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSasKey", []))

    @builtins.property
    @jsii.member(jsii_name="accountKeyInput")
    def account_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="accountNameInput")
    def account_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountNameInput"))

    @builtins.property
    @jsii.member(jsii_name="blobfuseOptionsInput")
    def blobfuse_options_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "blobfuseOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="containerNameInput")
    def container_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "containerNameInput"))

    @builtins.property
    @jsii.member(jsii_name="identityIdInput")
    def identity_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "identityIdInput"))

    @builtins.property
    @jsii.member(jsii_name="relativeMountPathInput")
    def relative_mount_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "relativeMountPathInput"))

    @builtins.property
    @jsii.member(jsii_name="sasKeyInput")
    def sas_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sasKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="accountKey")
    def account_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountKey"))

    @account_key.setter
    def account_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c0dcbbbf3d79094f450609a3493804039233e7c98f8d23aa3738eddf299113e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="accountName")
    def account_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountName"))

    @account_name.setter
    def account_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bab89d2f72eacb24e4cfb1a0f10683957c63ca457274601cf0052c83c7f599d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="blobfuseOptions")
    def blobfuse_options(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "blobfuseOptions"))

    @blobfuse_options.setter
    def blobfuse_options(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__298173f68ccc1310f1a6a4fab0331e76f11723d8af4e74d88960e921c3a09968)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "blobfuseOptions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="containerName")
    def container_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "containerName"))

    @container_name.setter
    def container_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e63b45c1776736a84753d0c2be054702e6e3de251a2ea75643c504e21d84701f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="identityId")
    def identity_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identityId"))

    @identity_id.setter
    def identity_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e047619cb0d285c797cb6a92a83b8d45a3b1dfbcd6a942bad3865c756eabd6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="relativeMountPath")
    def relative_mount_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "relativeMountPath"))

    @relative_mount_path.setter
    def relative_mount_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f833bbbdc7a033edfcabf39927d2ee8e8492af053c813e084c31e239bab38d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "relativeMountPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sasKey")
    def sas_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sasKey"))

    @sas_key.setter
    def sas_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1e8f39d142fbd12cb5476ce7385cdbfef0f9aacd1731fa3fb226ef866e9dafd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sasKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BatchPoolMountAzureBlobFileSystem]:
        return typing.cast(typing.Optional[BatchPoolMountAzureBlobFileSystem], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BatchPoolMountAzureBlobFileSystem],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21a78a3c6ce1f4c3a4de3aa8d5fb271df4c31334b22433c43dce3cd45c6c2c7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolMountAzureFileShare",
    jsii_struct_bases=[],
    name_mapping={
        "account_key": "accountKey",
        "account_name": "accountName",
        "azure_file_url": "azureFileUrl",
        "relative_mount_path": "relativeMountPath",
        "mount_options": "mountOptions",
    },
)
class BatchPoolMountAzureFileShare:
    def __init__(
        self,
        *,
        account_key: builtins.str,
        account_name: builtins.str,
        azure_file_url: builtins.str,
        relative_mount_path: builtins.str,
        mount_options: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param account_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#account_key BatchPool#account_key}.
        :param account_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#account_name BatchPool#account_name}.
        :param azure_file_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#azure_file_url BatchPool#azure_file_url}.
        :param relative_mount_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#relative_mount_path BatchPool#relative_mount_path}.
        :param mount_options: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#mount_options BatchPool#mount_options}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34b8b4b25eb68021071bd9421f90215b9f716dbd2f16174d9501e8cea7ff506e)
            check_type(argname="argument account_key", value=account_key, expected_type=type_hints["account_key"])
            check_type(argname="argument account_name", value=account_name, expected_type=type_hints["account_name"])
            check_type(argname="argument azure_file_url", value=azure_file_url, expected_type=type_hints["azure_file_url"])
            check_type(argname="argument relative_mount_path", value=relative_mount_path, expected_type=type_hints["relative_mount_path"])
            check_type(argname="argument mount_options", value=mount_options, expected_type=type_hints["mount_options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account_key": account_key,
            "account_name": account_name,
            "azure_file_url": azure_file_url,
            "relative_mount_path": relative_mount_path,
        }
        if mount_options is not None:
            self._values["mount_options"] = mount_options

    @builtins.property
    def account_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#account_key BatchPool#account_key}.'''
        result = self._values.get("account_key")
        assert result is not None, "Required property 'account_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def account_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#account_name BatchPool#account_name}.'''
        result = self._values.get("account_name")
        assert result is not None, "Required property 'account_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def azure_file_url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#azure_file_url BatchPool#azure_file_url}.'''
        result = self._values.get("azure_file_url")
        assert result is not None, "Required property 'azure_file_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def relative_mount_path(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#relative_mount_path BatchPool#relative_mount_path}.'''
        result = self._values.get("relative_mount_path")
        assert result is not None, "Required property 'relative_mount_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def mount_options(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#mount_options BatchPool#mount_options}.'''
        result = self._values.get("mount_options")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BatchPoolMountAzureFileShare(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BatchPoolMountAzureFileShareList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolMountAzureFileShareList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__face89eaadb219af38ba71813b47c8b2f42befeea28633e511e8eaa6e54f15cb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "BatchPoolMountAzureFileShareOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__696213558190bd8cffb9956f7c9319f2349a24ff96134b787dbdd2f7253951bf)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BatchPoolMountAzureFileShareOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a80cf37645c71ee5cae45d6029332d6aab48a949e5313a84350faa1ed64f95ff)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d60ca19bf4bf5d19201e8ce9b2c1e4030af4de54e9fc55e50d026f8265bbcfed)
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
            type_hints = typing.get_type_hints(_typecheckingstub__55273d681036b9d170d4ed228e268eab0e040f52252b4f89ffca32239ab320ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolMountAzureFileShare]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolMountAzureFileShare]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolMountAzureFileShare]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3473c66625e6e921feb5e05f572eb56893b195a11f5b162b7e96e2c80f4bc6aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BatchPoolMountAzureFileShareOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolMountAzureFileShareOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d24d0efc7e77a7597e4457527db61a3b4d4fb3bfd796a2ceec3c8def703ec66)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetMountOptions")
    def reset_mount_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMountOptions", []))

    @builtins.property
    @jsii.member(jsii_name="accountKeyInput")
    def account_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="accountNameInput")
    def account_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountNameInput"))

    @builtins.property
    @jsii.member(jsii_name="azureFileUrlInput")
    def azure_file_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "azureFileUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="mountOptionsInput")
    def mount_options_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mountOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="relativeMountPathInput")
    def relative_mount_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "relativeMountPathInput"))

    @builtins.property
    @jsii.member(jsii_name="accountKey")
    def account_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountKey"))

    @account_key.setter
    def account_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__770cc9f569c278fb2cbef8e6b6e05a2e5663c14a4ff56e3c6a4896379c8f9dda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="accountName")
    def account_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountName"))

    @account_name.setter
    def account_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75d52b4d0820bbc88eb88fedf4f146d766a8770eaf4336c6f68992bef73d5824)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="azureFileUrl")
    def azure_file_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "azureFileUrl"))

    @azure_file_url.setter
    def azure_file_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49af354a2ee970b8cac814d7cac97341606b4eb247ca8a2f1a0fbd19efa66fc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "azureFileUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mountOptions")
    def mount_options(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mountOptions"))

    @mount_options.setter
    def mount_options(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e26baac0772b21a34b7b8092ebcb27c5830bcbcfe641f26b4a56a843a98379bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mountOptions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="relativeMountPath")
    def relative_mount_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "relativeMountPath"))

    @relative_mount_path.setter
    def relative_mount_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d9f7ee2ca6e3eb2c1f389131139e5ea8548813aca5ebc3b5740be2f06288023)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "relativeMountPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolMountAzureFileShare]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolMountAzureFileShare]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolMountAzureFileShare]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d736db030aba5cbeeb304d0ef6b31e3c1f88b6ae3f0b977d8ba5b39e7f10e2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolMountCifsMount",
    jsii_struct_bases=[],
    name_mapping={
        "password": "password",
        "relative_mount_path": "relativeMountPath",
        "source": "source",
        "user_name": "userName",
        "mount_options": "mountOptions",
    },
)
class BatchPoolMountCifsMount:
    def __init__(
        self,
        *,
        password: builtins.str,
        relative_mount_path: builtins.str,
        source: builtins.str,
        user_name: builtins.str,
        mount_options: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#password BatchPool#password}.
        :param relative_mount_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#relative_mount_path BatchPool#relative_mount_path}.
        :param source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#source BatchPool#source}.
        :param user_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#user_name BatchPool#user_name}.
        :param mount_options: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#mount_options BatchPool#mount_options}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bfc420329c793eaac34d21a4b43dabb0fa15a5d0c629be0d7b77c09aec49f70)
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument relative_mount_path", value=relative_mount_path, expected_type=type_hints["relative_mount_path"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument user_name", value=user_name, expected_type=type_hints["user_name"])
            check_type(argname="argument mount_options", value=mount_options, expected_type=type_hints["mount_options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "password": password,
            "relative_mount_path": relative_mount_path,
            "source": source,
            "user_name": user_name,
        }
        if mount_options is not None:
            self._values["mount_options"] = mount_options

    @builtins.property
    def password(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#password BatchPool#password}.'''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def relative_mount_path(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#relative_mount_path BatchPool#relative_mount_path}.'''
        result = self._values.get("relative_mount_path")
        assert result is not None, "Required property 'relative_mount_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#source BatchPool#source}.'''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def user_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#user_name BatchPool#user_name}.'''
        result = self._values.get("user_name")
        assert result is not None, "Required property 'user_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def mount_options(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#mount_options BatchPool#mount_options}.'''
        result = self._values.get("mount_options")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BatchPoolMountCifsMount(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BatchPoolMountCifsMountList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolMountCifsMountList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ffbe8d90917bb15aace439e21f2fa9255c73cc818d42e0b585659a3084cad9ed)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "BatchPoolMountCifsMountOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac00b1fd4d6022e66a02fbb7ab256fb6795985fbcd310e13c15210aef6196ad9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BatchPoolMountCifsMountOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84e44cceee9d71ee90bf168e8e69827bb5d6e00d14b1e8e96adf98d6937ddef4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c9da16ffc38a497eac85d3dc5a028a1397e1dad292964151a02577a153875dfa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c0bdbd6ea920be14bd646682fa05057409d403c077e45f5c243e891480c5be2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolMountCifsMount]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolMountCifsMount]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolMountCifsMount]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e0b06456f87328d8d61b5bb52e16819b81ae25788fbd16d9a521fd86947ea27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BatchPoolMountCifsMountOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolMountCifsMountOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__20eb0bf84d2f694d3bb71e5764016b58e14e298cc309571cff656fa70438035d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetMountOptions")
    def reset_mount_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMountOptions", []))

    @builtins.property
    @jsii.member(jsii_name="mountOptionsInput")
    def mount_options_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mountOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="relativeMountPathInput")
    def relative_mount_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "relativeMountPathInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="userNameInput")
    def user_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userNameInput"))

    @builtins.property
    @jsii.member(jsii_name="mountOptions")
    def mount_options(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mountOptions"))

    @mount_options.setter
    def mount_options(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aedc03eab0908066ddb1e90dbe295309734093c611c1acf932e16a5d7f38b119)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mountOptions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__846673ba4fe2d189489e4a7db3bd7f1fd13da1307ae184c4342d95493acc2abb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="relativeMountPath")
    def relative_mount_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "relativeMountPath"))

    @relative_mount_path.setter
    def relative_mount_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25d1d7a697b2cf22380110b2b48bcda732129553c3604248b84fc00aad2cc591)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "relativeMountPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__951eea3fb3e63a6dc52a4885a54f76cd2d235db6d6dfe1102f4d77a5f9255f9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userName")
    def user_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userName"))

    @user_name.setter
    def user_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5422baaacb5c94a63daf44ff40c24d7620c54344950e473d81b9ac75b8cec831)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolMountCifsMount]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolMountCifsMount]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolMountCifsMount]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc74faa003a7e3da6068aca0b2540782b4d4d43eb44665e4ae67d4005e1f0a2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BatchPoolMountList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolMountList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dcd2a92aa6a6ffbebc2b70ba5dd0579c0952b2eed6534b496535c717825144e8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "BatchPoolMountOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fb61a357f217140aa89c381b36ea8e2da2414c493ddcdbfa8c7a8dfd722bc72)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BatchPoolMountOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aaf86f739fd3691b6efa5b12223884bbabec4dfb8333957e9e423f0a7243548d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b8753c0131b67a8488d4b79dd9be5212a83b0d91cf40f3baab93ed00800045ac)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d88fda04eff58a8be84e1d3c56ec46944ac4cf9f62b63138e8f1d0eaebd12f4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolMount]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolMount]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolMount]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__583fb9071573e27e3ada827fca701866c1ccd59ccfaf5e8c7041b16d1339954f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolMountNfsMount",
    jsii_struct_bases=[],
    name_mapping={
        "relative_mount_path": "relativeMountPath",
        "source": "source",
        "mount_options": "mountOptions",
    },
)
class BatchPoolMountNfsMount:
    def __init__(
        self,
        *,
        relative_mount_path: builtins.str,
        source: builtins.str,
        mount_options: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param relative_mount_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#relative_mount_path BatchPool#relative_mount_path}.
        :param source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#source BatchPool#source}.
        :param mount_options: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#mount_options BatchPool#mount_options}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4c113fe3db939dbb452e49c99a36fc1cbb8e06f805a640a2f05ecc1c6797600)
            check_type(argname="argument relative_mount_path", value=relative_mount_path, expected_type=type_hints["relative_mount_path"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument mount_options", value=mount_options, expected_type=type_hints["mount_options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "relative_mount_path": relative_mount_path,
            "source": source,
        }
        if mount_options is not None:
            self._values["mount_options"] = mount_options

    @builtins.property
    def relative_mount_path(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#relative_mount_path BatchPool#relative_mount_path}.'''
        result = self._values.get("relative_mount_path")
        assert result is not None, "Required property 'relative_mount_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#source BatchPool#source}.'''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def mount_options(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#mount_options BatchPool#mount_options}.'''
        result = self._values.get("mount_options")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BatchPoolMountNfsMount(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BatchPoolMountNfsMountList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolMountNfsMountList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c98a525929281d1680a2178bc858991a5a667c432ca77a98cb36efc1209d13b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "BatchPoolMountNfsMountOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70e3d61b8352a2682310481c08d3dd9d52e9a248a55fc2a585419e90fd40b459)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BatchPoolMountNfsMountOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0c09311f4c73d3a0e6a74b7191b8ba26aa23420129b75b14256b998cc1a2301)
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
            type_hints = typing.get_type_hints(_typecheckingstub__48b94e0bf260dde37d3b6fea58889849e1a2804db4627aae8b8857ebc8c0c5ad)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a708651f4ac53e8703cd708b7df03b4d3e786f32e087f181b1cf79c61e595294)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolMountNfsMount]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolMountNfsMount]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolMountNfsMount]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c4975008f50c9f8faa521792da56b69c8d8ea21bd7ac481b2e0c20ceb8113b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BatchPoolMountNfsMountOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolMountNfsMountOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__25fbbb97f71441951aa4065cbea92240ba922bae32e9e611117ae0e9d66f98c9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetMountOptions")
    def reset_mount_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMountOptions", []))

    @builtins.property
    @jsii.member(jsii_name="mountOptionsInput")
    def mount_options_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mountOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="relativeMountPathInput")
    def relative_mount_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "relativeMountPathInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="mountOptions")
    def mount_options(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mountOptions"))

    @mount_options.setter
    def mount_options(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a446bf643467acc06ff22703cf079da6daf229ea5829223262332e33b89ab53c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mountOptions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="relativeMountPath")
    def relative_mount_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "relativeMountPath"))

    @relative_mount_path.setter
    def relative_mount_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a19b0b2002e0b9946ce7a5583bc2644f585efb1d42a527b3bba129c2baca4663)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "relativeMountPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__786cbb8526c54eddf88cbdc6ed2184816623174c29dcd02318dfa4699f06cd9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolMountNfsMount]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolMountNfsMount]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolMountNfsMount]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc4450cc9a21521833697bb227fb8413c69940841762d2948e78e781408fb4ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BatchPoolMountOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolMountOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8c91441bebed41841df65e63fbb0ba30f9a5fe05ff3ef4bd38d30eef8cc2b4e6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAzureBlobFileSystem")
    def put_azure_blob_file_system(
        self,
        *,
        account_name: builtins.str,
        container_name: builtins.str,
        relative_mount_path: builtins.str,
        account_key: typing.Optional[builtins.str] = None,
        blobfuse_options: typing.Optional[builtins.str] = None,
        identity_id: typing.Optional[builtins.str] = None,
        sas_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param account_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#account_name BatchPool#account_name}.
        :param container_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#container_name BatchPool#container_name}.
        :param relative_mount_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#relative_mount_path BatchPool#relative_mount_path}.
        :param account_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#account_key BatchPool#account_key}.
        :param blobfuse_options: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#blobfuse_options BatchPool#blobfuse_options}.
        :param identity_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#identity_id BatchPool#identity_id}.
        :param sas_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#sas_key BatchPool#sas_key}.
        '''
        value = BatchPoolMountAzureBlobFileSystem(
            account_name=account_name,
            container_name=container_name,
            relative_mount_path=relative_mount_path,
            account_key=account_key,
            blobfuse_options=blobfuse_options,
            identity_id=identity_id,
            sas_key=sas_key,
        )

        return typing.cast(None, jsii.invoke(self, "putAzureBlobFileSystem", [value]))

    @jsii.member(jsii_name="putAzureFileShare")
    def put_azure_file_share(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BatchPoolMountAzureFileShare, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aaf595d6284a4806e2ad05c07a69dd050aa5594ffa83aafa884aff4b6e1902d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAzureFileShare", [value]))

    @jsii.member(jsii_name="putCifsMount")
    def put_cifs_mount(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BatchPoolMountCifsMount, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11fecd0e11453120fab5ba783e51e1ebbc61a8d4b75e6ace47340caf52997dc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCifsMount", [value]))

    @jsii.member(jsii_name="putNfsMount")
    def put_nfs_mount(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BatchPoolMountNfsMount, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed73b1e0caa97d5662969ea5900b53d0b7108410f4600d9105e79b7b4ae26eab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNfsMount", [value]))

    @jsii.member(jsii_name="resetAzureBlobFileSystem")
    def reset_azure_blob_file_system(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAzureBlobFileSystem", []))

    @jsii.member(jsii_name="resetAzureFileShare")
    def reset_azure_file_share(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAzureFileShare", []))

    @jsii.member(jsii_name="resetCifsMount")
    def reset_cifs_mount(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCifsMount", []))

    @jsii.member(jsii_name="resetNfsMount")
    def reset_nfs_mount(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNfsMount", []))

    @builtins.property
    @jsii.member(jsii_name="azureBlobFileSystem")
    def azure_blob_file_system(
        self,
    ) -> BatchPoolMountAzureBlobFileSystemOutputReference:
        return typing.cast(BatchPoolMountAzureBlobFileSystemOutputReference, jsii.get(self, "azureBlobFileSystem"))

    @builtins.property
    @jsii.member(jsii_name="azureFileShare")
    def azure_file_share(self) -> BatchPoolMountAzureFileShareList:
        return typing.cast(BatchPoolMountAzureFileShareList, jsii.get(self, "azureFileShare"))

    @builtins.property
    @jsii.member(jsii_name="cifsMount")
    def cifs_mount(self) -> BatchPoolMountCifsMountList:
        return typing.cast(BatchPoolMountCifsMountList, jsii.get(self, "cifsMount"))

    @builtins.property
    @jsii.member(jsii_name="nfsMount")
    def nfs_mount(self) -> BatchPoolMountNfsMountList:
        return typing.cast(BatchPoolMountNfsMountList, jsii.get(self, "nfsMount"))

    @builtins.property
    @jsii.member(jsii_name="azureBlobFileSystemInput")
    def azure_blob_file_system_input(
        self,
    ) -> typing.Optional[BatchPoolMountAzureBlobFileSystem]:
        return typing.cast(typing.Optional[BatchPoolMountAzureBlobFileSystem], jsii.get(self, "azureBlobFileSystemInput"))

    @builtins.property
    @jsii.member(jsii_name="azureFileShareInput")
    def azure_file_share_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolMountAzureFileShare]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolMountAzureFileShare]]], jsii.get(self, "azureFileShareInput"))

    @builtins.property
    @jsii.member(jsii_name="cifsMountInput")
    def cifs_mount_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolMountCifsMount]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolMountCifsMount]]], jsii.get(self, "cifsMountInput"))

    @builtins.property
    @jsii.member(jsii_name="nfsMountInput")
    def nfs_mount_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolMountNfsMount]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolMountNfsMount]]], jsii.get(self, "nfsMountInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolMount]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolMount]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolMount]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba351f651a4d8863cf389fceb50e733a79197fa830bfcc1814b998b67ba70680)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolNetworkConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "accelerated_networking_enabled": "acceleratedNetworkingEnabled",
        "dynamic_vnet_assignment_scope": "dynamicVnetAssignmentScope",
        "endpoint_configuration": "endpointConfiguration",
        "public_address_provisioning_type": "publicAddressProvisioningType",
        "public_ips": "publicIps",
        "subnet_id": "subnetId",
    },
)
class BatchPoolNetworkConfiguration:
    def __init__(
        self,
        *,
        accelerated_networking_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        dynamic_vnet_assignment_scope: typing.Optional[builtins.str] = None,
        endpoint_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BatchPoolNetworkConfigurationEndpointConfiguration", typing.Dict[builtins.str, typing.Any]]]]] = None,
        public_address_provisioning_type: typing.Optional[builtins.str] = None,
        public_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnet_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param accelerated_networking_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#accelerated_networking_enabled BatchPool#accelerated_networking_enabled}.
        :param dynamic_vnet_assignment_scope: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#dynamic_vnet_assignment_scope BatchPool#dynamic_vnet_assignment_scope}.
        :param endpoint_configuration: endpoint_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#endpoint_configuration BatchPool#endpoint_configuration}
        :param public_address_provisioning_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#public_address_provisioning_type BatchPool#public_address_provisioning_type}.
        :param public_ips: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#public_ips BatchPool#public_ips}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#subnet_id BatchPool#subnet_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fba4c9d1f73ee9fd126825aa354f51dc979cb6ecad5bad2eb9c76b7bb95f215)
            check_type(argname="argument accelerated_networking_enabled", value=accelerated_networking_enabled, expected_type=type_hints["accelerated_networking_enabled"])
            check_type(argname="argument dynamic_vnet_assignment_scope", value=dynamic_vnet_assignment_scope, expected_type=type_hints["dynamic_vnet_assignment_scope"])
            check_type(argname="argument endpoint_configuration", value=endpoint_configuration, expected_type=type_hints["endpoint_configuration"])
            check_type(argname="argument public_address_provisioning_type", value=public_address_provisioning_type, expected_type=type_hints["public_address_provisioning_type"])
            check_type(argname="argument public_ips", value=public_ips, expected_type=type_hints["public_ips"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if accelerated_networking_enabled is not None:
            self._values["accelerated_networking_enabled"] = accelerated_networking_enabled
        if dynamic_vnet_assignment_scope is not None:
            self._values["dynamic_vnet_assignment_scope"] = dynamic_vnet_assignment_scope
        if endpoint_configuration is not None:
            self._values["endpoint_configuration"] = endpoint_configuration
        if public_address_provisioning_type is not None:
            self._values["public_address_provisioning_type"] = public_address_provisioning_type
        if public_ips is not None:
            self._values["public_ips"] = public_ips
        if subnet_id is not None:
            self._values["subnet_id"] = subnet_id

    @builtins.property
    def accelerated_networking_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#accelerated_networking_enabled BatchPool#accelerated_networking_enabled}.'''
        result = self._values.get("accelerated_networking_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def dynamic_vnet_assignment_scope(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#dynamic_vnet_assignment_scope BatchPool#dynamic_vnet_assignment_scope}.'''
        result = self._values.get("dynamic_vnet_assignment_scope")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def endpoint_configuration(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BatchPoolNetworkConfigurationEndpointConfiguration"]]]:
        '''endpoint_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#endpoint_configuration BatchPool#endpoint_configuration}
        '''
        result = self._values.get("endpoint_configuration")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BatchPoolNetworkConfigurationEndpointConfiguration"]]], result)

    @builtins.property
    def public_address_provisioning_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#public_address_provisioning_type BatchPool#public_address_provisioning_type}.'''
        result = self._values.get("public_address_provisioning_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def public_ips(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#public_ips BatchPool#public_ips}.'''
        result = self._values.get("public_ips")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def subnet_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#subnet_id BatchPool#subnet_id}.'''
        result = self._values.get("subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BatchPoolNetworkConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolNetworkConfigurationEndpointConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "backend_port": "backendPort",
        "frontend_port_range": "frontendPortRange",
        "name": "name",
        "protocol": "protocol",
        "network_security_group_rules": "networkSecurityGroupRules",
    },
)
class BatchPoolNetworkConfigurationEndpointConfiguration:
    def __init__(
        self,
        *,
        backend_port: jsii.Number,
        frontend_port_range: builtins.str,
        name: builtins.str,
        protocol: builtins.str,
        network_security_group_rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BatchPoolNetworkConfigurationEndpointConfigurationNetworkSecurityGroupRules", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param backend_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#backend_port BatchPool#backend_port}.
        :param frontend_port_range: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#frontend_port_range BatchPool#frontend_port_range}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#name BatchPool#name}.
        :param protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#protocol BatchPool#protocol}.
        :param network_security_group_rules: network_security_group_rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#network_security_group_rules BatchPool#network_security_group_rules}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cce14c684ec688cd0009a01d88340e2d26e95cba27cb5c1228d2f0695f840db2)
            check_type(argname="argument backend_port", value=backend_port, expected_type=type_hints["backend_port"])
            check_type(argname="argument frontend_port_range", value=frontend_port_range, expected_type=type_hints["frontend_port_range"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument network_security_group_rules", value=network_security_group_rules, expected_type=type_hints["network_security_group_rules"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "backend_port": backend_port,
            "frontend_port_range": frontend_port_range,
            "name": name,
            "protocol": protocol,
        }
        if network_security_group_rules is not None:
            self._values["network_security_group_rules"] = network_security_group_rules

    @builtins.property
    def backend_port(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#backend_port BatchPool#backend_port}.'''
        result = self._values.get("backend_port")
        assert result is not None, "Required property 'backend_port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def frontend_port_range(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#frontend_port_range BatchPool#frontend_port_range}.'''
        result = self._values.get("frontend_port_range")
        assert result is not None, "Required property 'frontend_port_range' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#name BatchPool#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def protocol(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#protocol BatchPool#protocol}.'''
        result = self._values.get("protocol")
        assert result is not None, "Required property 'protocol' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def network_security_group_rules(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BatchPoolNetworkConfigurationEndpointConfigurationNetworkSecurityGroupRules"]]]:
        '''network_security_group_rules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#network_security_group_rules BatchPool#network_security_group_rules}
        '''
        result = self._values.get("network_security_group_rules")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BatchPoolNetworkConfigurationEndpointConfigurationNetworkSecurityGroupRules"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BatchPoolNetworkConfigurationEndpointConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BatchPoolNetworkConfigurationEndpointConfigurationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolNetworkConfigurationEndpointConfigurationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__09d62094a096d0c49dca568752782504d3744fc6927e5c7ef1e97297c9c44c4f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BatchPoolNetworkConfigurationEndpointConfigurationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ede91b66cfb2dbbb3c7370fbfe4323fd069080a1aba2cca22d148b57d44c3779)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BatchPoolNetworkConfigurationEndpointConfigurationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d847cb2a7acb8d3247e8945d1cf59a31b271415bc4b34467cb1478da4e6f881)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e148e01eb097ffac89d51325a98f2ffbd3ed4f3f1c5265e1c1b563a1bb057912)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bce848aa29b6a52f8f6f75e609f304301e5130e102406f04710a2498a9d9a42c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolNetworkConfigurationEndpointConfiguration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolNetworkConfigurationEndpointConfiguration]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolNetworkConfigurationEndpointConfiguration]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cffa89b7625b14643d94eb96eafd9a66843f76a343af8539db5fb7cc45e27925)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolNetworkConfigurationEndpointConfigurationNetworkSecurityGroupRules",
    jsii_struct_bases=[],
    name_mapping={
        "access": "access",
        "priority": "priority",
        "source_address_prefix": "sourceAddressPrefix",
        "source_port_ranges": "sourcePortRanges",
    },
)
class BatchPoolNetworkConfigurationEndpointConfigurationNetworkSecurityGroupRules:
    def __init__(
        self,
        *,
        access: builtins.str,
        priority: jsii.Number,
        source_address_prefix: builtins.str,
        source_port_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param access: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#access BatchPool#access}.
        :param priority: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#priority BatchPool#priority}.
        :param source_address_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#source_address_prefix BatchPool#source_address_prefix}.
        :param source_port_ranges: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#source_port_ranges BatchPool#source_port_ranges}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bba713c87ffdc3fa6651d883c366ffa8e198170ccbd95268d1527f929d9f9064)
            check_type(argname="argument access", value=access, expected_type=type_hints["access"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument source_address_prefix", value=source_address_prefix, expected_type=type_hints["source_address_prefix"])
            check_type(argname="argument source_port_ranges", value=source_port_ranges, expected_type=type_hints["source_port_ranges"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "access": access,
            "priority": priority,
            "source_address_prefix": source_address_prefix,
        }
        if source_port_ranges is not None:
            self._values["source_port_ranges"] = source_port_ranges

    @builtins.property
    def access(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#access BatchPool#access}.'''
        result = self._values.get("access")
        assert result is not None, "Required property 'access' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def priority(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#priority BatchPool#priority}.'''
        result = self._values.get("priority")
        assert result is not None, "Required property 'priority' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def source_address_prefix(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#source_address_prefix BatchPool#source_address_prefix}.'''
        result = self._values.get("source_address_prefix")
        assert result is not None, "Required property 'source_address_prefix' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_port_ranges(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#source_port_ranges BatchPool#source_port_ranges}.'''
        result = self._values.get("source_port_ranges")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BatchPoolNetworkConfigurationEndpointConfigurationNetworkSecurityGroupRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BatchPoolNetworkConfigurationEndpointConfigurationNetworkSecurityGroupRulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolNetworkConfigurationEndpointConfigurationNetworkSecurityGroupRulesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__489fb3faf7b33671e5726d3574d7f1933a06cabf3614c0bc91c793769f7a45ac)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BatchPoolNetworkConfigurationEndpointConfigurationNetworkSecurityGroupRulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__675f1297dff23feea5bc9a3f7f83de75e8b5230168e779f0e37ed19ab5efceb8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BatchPoolNetworkConfigurationEndpointConfigurationNetworkSecurityGroupRulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b07b69b522ae1bcfccd704ca6f418dc82805a66e7eab2bd48e58efd21ca947ad)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc8e58320648418549b06c53477cec81600468b0343c99132b7e1073b7951ab2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__241eb0351d991f87d87ee211d4d951a3d4a45d523a3ce50477f88ee60f34aa7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolNetworkConfigurationEndpointConfigurationNetworkSecurityGroupRules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolNetworkConfigurationEndpointConfigurationNetworkSecurityGroupRules]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolNetworkConfigurationEndpointConfigurationNetworkSecurityGroupRules]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92c6523a9bf63f0855b3f3409f3a813499231f6d0cd69f0dc2d546e1bd7a1a31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BatchPoolNetworkConfigurationEndpointConfigurationNetworkSecurityGroupRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolNetworkConfigurationEndpointConfigurationNetworkSecurityGroupRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad9e640beaf3916dc9b7195bed260511d8e5afcd4eb5218a1ab2909080fbff3e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetSourcePortRanges")
    def reset_source_port_ranges(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourcePortRanges", []))

    @builtins.property
    @jsii.member(jsii_name="accessInput")
    def access_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessInput"))

    @builtins.property
    @jsii.member(jsii_name="priorityInput")
    def priority_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "priorityInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceAddressPrefixInput")
    def source_address_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceAddressPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="sourcePortRangesInput")
    def source_port_ranges_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sourcePortRangesInput"))

    @builtins.property
    @jsii.member(jsii_name="access")
    def access(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "access"))

    @access.setter
    def access(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bab27293c5127e026bf0ae7b0a2434aac79ab9c2656c36279b3b8790717a300)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "access", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01414ed157d36c554ef19c5d84ad1bdc0976d1363dbc37fd53f39e0d0535c509)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceAddressPrefix")
    def source_address_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceAddressPrefix"))

    @source_address_prefix.setter
    def source_address_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d67fdab7902e32893cd7b93e465bf3a321f0a3ca7358f678e8e62ab86bca8c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceAddressPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourcePortRanges")
    def source_port_ranges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sourcePortRanges"))

    @source_port_ranges.setter
    def source_port_ranges(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d663932364fe157f1c1fb1d5a678133c2ad7d665abdeb9a162cf514f6faa822a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourcePortRanges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolNetworkConfigurationEndpointConfigurationNetworkSecurityGroupRules]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolNetworkConfigurationEndpointConfigurationNetworkSecurityGroupRules]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolNetworkConfigurationEndpointConfigurationNetworkSecurityGroupRules]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a49c8bd5d4b3b79af9a142ae8480e35f5b26e9ceab1f509c19a5b0b156ea1ca3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BatchPoolNetworkConfigurationEndpointConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolNetworkConfigurationEndpointConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4893826a5e0c6266a59f62f9562e45a74d4bf409db1163b2c03551942de309d5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putNetworkSecurityGroupRules")
    def put_network_security_group_rules(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BatchPoolNetworkConfigurationEndpointConfigurationNetworkSecurityGroupRules, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69a2ce91da4d296582e852dc6f15befdf49332ab61e8cf711c01eb499f5b7a3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNetworkSecurityGroupRules", [value]))

    @jsii.member(jsii_name="resetNetworkSecurityGroupRules")
    def reset_network_security_group_rules(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkSecurityGroupRules", []))

    @builtins.property
    @jsii.member(jsii_name="networkSecurityGroupRules")
    def network_security_group_rules(
        self,
    ) -> BatchPoolNetworkConfigurationEndpointConfigurationNetworkSecurityGroupRulesList:
        return typing.cast(BatchPoolNetworkConfigurationEndpointConfigurationNetworkSecurityGroupRulesList, jsii.get(self, "networkSecurityGroupRules"))

    @builtins.property
    @jsii.member(jsii_name="backendPortInput")
    def backend_port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "backendPortInput"))

    @builtins.property
    @jsii.member(jsii_name="frontendPortRangeInput")
    def frontend_port_range_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "frontendPortRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkSecurityGroupRulesInput")
    def network_security_group_rules_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolNetworkConfigurationEndpointConfigurationNetworkSecurityGroupRules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolNetworkConfigurationEndpointConfigurationNetworkSecurityGroupRules]]], jsii.get(self, "networkSecurityGroupRulesInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolInput")
    def protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protocolInput"))

    @builtins.property
    @jsii.member(jsii_name="backendPort")
    def backend_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "backendPort"))

    @backend_port.setter
    def backend_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2de0e74051892d9d7ff25b0ac345fd112203e4b573726708fdd3fe854d3dbf84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backendPort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="frontendPortRange")
    def frontend_port_range(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "frontendPortRange"))

    @frontend_port_range.setter
    def frontend_port_range(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__203e1cc1627e9d65e8d682266066cf67f1ca10870da117dbfc0f98d2b379947b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "frontendPortRange", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95a1b3d8cadc9f8eb1970764f532d34995b00251a8c866b0d106267d2e2897af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d75e4668ccbf1410066c2c57f76faa99ce667bfc2c20f1ffe3ac958fb8977f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolNetworkConfigurationEndpointConfiguration]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolNetworkConfigurationEndpointConfiguration]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolNetworkConfigurationEndpointConfiguration]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26d2124e4ebdd90db69344e41d0c7d6c47c272fa9d64ea24240bc9b6740776d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BatchPoolNetworkConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolNetworkConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__68815728f08f37c5b02182bd1b9e6bae8650dcd05772a754ba51cbf4294c1242)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putEndpointConfiguration")
    def put_endpoint_configuration(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BatchPoolNetworkConfigurationEndpointConfiguration, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de07dbe5b2eff466170f14b0a8419ede1a5bb4a6fdae630364fb295e9373baa6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEndpointConfiguration", [value]))

    @jsii.member(jsii_name="resetAcceleratedNetworkingEnabled")
    def reset_accelerated_networking_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAcceleratedNetworkingEnabled", []))

    @jsii.member(jsii_name="resetDynamicVnetAssignmentScope")
    def reset_dynamic_vnet_assignment_scope(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDynamicVnetAssignmentScope", []))

    @jsii.member(jsii_name="resetEndpointConfiguration")
    def reset_endpoint_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndpointConfiguration", []))

    @jsii.member(jsii_name="resetPublicAddressProvisioningType")
    def reset_public_address_provisioning_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicAddressProvisioningType", []))

    @jsii.member(jsii_name="resetPublicIps")
    def reset_public_ips(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicIps", []))

    @jsii.member(jsii_name="resetSubnetId")
    def reset_subnet_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnetId", []))

    @builtins.property
    @jsii.member(jsii_name="endpointConfiguration")
    def endpoint_configuration(
        self,
    ) -> BatchPoolNetworkConfigurationEndpointConfigurationList:
        return typing.cast(BatchPoolNetworkConfigurationEndpointConfigurationList, jsii.get(self, "endpointConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="acceleratedNetworkingEnabledInput")
    def accelerated_networking_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "acceleratedNetworkingEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="dynamicVnetAssignmentScopeInput")
    def dynamic_vnet_assignment_scope_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dynamicVnetAssignmentScopeInput"))

    @builtins.property
    @jsii.member(jsii_name="endpointConfigurationInput")
    def endpoint_configuration_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolNetworkConfigurationEndpointConfiguration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolNetworkConfigurationEndpointConfiguration]]], jsii.get(self, "endpointConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="publicAddressProvisioningTypeInput")
    def public_address_provisioning_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "publicAddressProvisioningTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="publicIpsInput")
    def public_ips_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "publicIpsInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetIdInput")
    def subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="acceleratedNetworkingEnabled")
    def accelerated_networking_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "acceleratedNetworkingEnabled"))

    @accelerated_networking_enabled.setter
    def accelerated_networking_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dad4ce9369c594a972a1e2b6e98150a97578f41fe12aa2552caee3061e14c545)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceleratedNetworkingEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dynamicVnetAssignmentScope")
    def dynamic_vnet_assignment_scope(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dynamicVnetAssignmentScope"))

    @dynamic_vnet_assignment_scope.setter
    def dynamic_vnet_assignment_scope(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d7d2f924a1a2dc601a72722d4e4dce6b2ac4c26bc9fb8d6efbc26a895f7ab5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dynamicVnetAssignmentScope", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publicAddressProvisioningType")
    def public_address_provisioning_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicAddressProvisioningType"))

    @public_address_provisioning_type.setter
    def public_address_provisioning_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49758f71ec2e0216c3bcb0e27176df26d2fe653f7cd2cb247216724f867db76f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicAddressProvisioningType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publicIps")
    def public_ips(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "publicIps"))

    @public_ips.setter
    def public_ips(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73f359b290e7eba6567f70ef3e134ef43bb1b44d4b11816cf881de377bdeaee8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicIps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3eb06bff9fd78997e4744600222528755a705f5c7c5e5c1ec9932a6087148d0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BatchPoolNetworkConfiguration]:
        return typing.cast(typing.Optional[BatchPoolNetworkConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BatchPoolNetworkConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__515151df7f265c796e4e108d4593df87f5b665f979132f6608b6292b9fe7b33e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolNodePlacement",
    jsii_struct_bases=[],
    name_mapping={"policy": "policy"},
)
class BatchPoolNodePlacement:
    def __init__(self, *, policy: typing.Optional[builtins.str] = None) -> None:
        '''
        :param policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#policy BatchPool#policy}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06f081fa4b4c69915be5fe9a1e78f23e0b7a8999aac1f212a158ee2e32e7c36e)
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if policy is not None:
            self._values["policy"] = policy

    @builtins.property
    def policy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#policy BatchPool#policy}.'''
        result = self._values.get("policy")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BatchPoolNodePlacement(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BatchPoolNodePlacementList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolNodePlacementList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e788307fe9ecad0106ffb1b182c73b7483145f0712826fda10a5f2cc63a9193)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "BatchPoolNodePlacementOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d26feb2b7102e7c5f709fe5ba7a81d4c8a3e52fc5ce199f6b69ce12b95a74a40)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BatchPoolNodePlacementOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e2901102b2f2988913c8d51c210fca3f92fcfb4b01f83665f3809daca532e8a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d0980387d9a1a7834d783fdb5ec2d3a947ef2a652fe730a4927cd1d253ea2d41)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a1fc4d6ae9e65ee1be416d46555e61fda07275ca0ef68f44c63b5b9262110230)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolNodePlacement]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolNodePlacement]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolNodePlacement]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57540ce4bcc3a9515388fd742078bba7c036cdb87d4a05395d9d5c4233a7c612)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BatchPoolNodePlacementOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolNodePlacementOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a90277e23d1893f38b172b2071c4a425cbfae380a0c849347b76af2f7faa1fa3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetPolicy")
    def reset_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicy", []))

    @builtins.property
    @jsii.member(jsii_name="policyInput")
    def policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyInput"))

    @builtins.property
    @jsii.member(jsii_name="policy")
    def policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policy"))

    @policy.setter
    def policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f2cb428bb2932e564f07bd8e7263c4f64faf176e2c6221e34be749650840f60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolNodePlacement]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolNodePlacement]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolNodePlacement]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fddf2932ee765a489815b3c6a52800a7e1f582c9e2c6dbeef98141101543e93f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolSecurityProfile",
    jsii_struct_bases=[],
    name_mapping={
        "host_encryption_enabled": "hostEncryptionEnabled",
        "secure_boot_enabled": "secureBootEnabled",
        "security_type": "securityType",
        "vtpm_enabled": "vtpmEnabled",
    },
)
class BatchPoolSecurityProfile:
    def __init__(
        self,
        *,
        host_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        secure_boot_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        security_type: typing.Optional[builtins.str] = None,
        vtpm_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param host_encryption_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#host_encryption_enabled BatchPool#host_encryption_enabled}.
        :param secure_boot_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#secure_boot_enabled BatchPool#secure_boot_enabled}.
        :param security_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#security_type BatchPool#security_type}.
        :param vtpm_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#vtpm_enabled BatchPool#vtpm_enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b35e9d65bf04df18c26154dde97bf4c6613b73ba25288ea28fa684ca6cdd62a)
            check_type(argname="argument host_encryption_enabled", value=host_encryption_enabled, expected_type=type_hints["host_encryption_enabled"])
            check_type(argname="argument secure_boot_enabled", value=secure_boot_enabled, expected_type=type_hints["secure_boot_enabled"])
            check_type(argname="argument security_type", value=security_type, expected_type=type_hints["security_type"])
            check_type(argname="argument vtpm_enabled", value=vtpm_enabled, expected_type=type_hints["vtpm_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if host_encryption_enabled is not None:
            self._values["host_encryption_enabled"] = host_encryption_enabled
        if secure_boot_enabled is not None:
            self._values["secure_boot_enabled"] = secure_boot_enabled
        if security_type is not None:
            self._values["security_type"] = security_type
        if vtpm_enabled is not None:
            self._values["vtpm_enabled"] = vtpm_enabled

    @builtins.property
    def host_encryption_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#host_encryption_enabled BatchPool#host_encryption_enabled}.'''
        result = self._values.get("host_encryption_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def secure_boot_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#secure_boot_enabled BatchPool#secure_boot_enabled}.'''
        result = self._values.get("secure_boot_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def security_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#security_type BatchPool#security_type}.'''
        result = self._values.get("security_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vtpm_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#vtpm_enabled BatchPool#vtpm_enabled}.'''
        result = self._values.get("vtpm_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BatchPoolSecurityProfile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BatchPoolSecurityProfileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolSecurityProfileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__47ab1ac21fb50644a3ada765f4e3624183270b59f5625f7893d3355e45daeb5a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetHostEncryptionEnabled")
    def reset_host_encryption_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostEncryptionEnabled", []))

    @jsii.member(jsii_name="resetSecureBootEnabled")
    def reset_secure_boot_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecureBootEnabled", []))

    @jsii.member(jsii_name="resetSecurityType")
    def reset_security_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityType", []))

    @jsii.member(jsii_name="resetVtpmEnabled")
    def reset_vtpm_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVtpmEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="hostEncryptionEnabledInput")
    def host_encryption_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "hostEncryptionEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="secureBootEnabledInput")
    def secure_boot_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "secureBootEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="securityTypeInput")
    def security_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "securityTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="vtpmEnabledInput")
    def vtpm_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "vtpmEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="hostEncryptionEnabled")
    def host_encryption_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "hostEncryptionEnabled"))

    @host_encryption_enabled.setter
    def host_encryption_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9aa2340162a9ab76f4a4122776017a4b0249580223f577eaca9d868f4628ee33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostEncryptionEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secureBootEnabled")
    def secure_boot_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "secureBootEnabled"))

    @secure_boot_enabled.setter
    def secure_boot_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fa7f5616e0f9c0e7cd39d44c604cb36bbf1d63b7f389ef2029e58d8a6e668e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secureBootEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityType")
    def security_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityType"))

    @security_type.setter
    def security_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__229cd7c425f8c09e41758f7a593888e69ce62e4c388070947e54c0a9701b45b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vtpmEnabled")
    def vtpm_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "vtpmEnabled"))

    @vtpm_enabled.setter
    def vtpm_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac7a9540e9e9666bf918b1ddd0de2e7e58b3b1101a031945e8ba91fb6feba4a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vtpmEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BatchPoolSecurityProfile]:
        return typing.cast(typing.Optional[BatchPoolSecurityProfile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[BatchPoolSecurityProfile]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f2559b40d2b794935b5ec2f95a3bf00cd5d190e2ad3113df80156700f0f2e01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolStartTask",
    jsii_struct_bases=[],
    name_mapping={
        "command_line": "commandLine",
        "user_identity": "userIdentity",
        "common_environment_properties": "commonEnvironmentProperties",
        "container": "container",
        "resource_file": "resourceFile",
        "task_retry_maximum": "taskRetryMaximum",
        "wait_for_success": "waitForSuccess",
    },
)
class BatchPoolStartTask:
    def __init__(
        self,
        *,
        command_line: builtins.str,
        user_identity: typing.Union["BatchPoolStartTaskUserIdentity", typing.Dict[builtins.str, typing.Any]],
        common_environment_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        container: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BatchPoolStartTaskContainer", typing.Dict[builtins.str, typing.Any]]]]] = None,
        resource_file: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BatchPoolStartTaskResourceFile", typing.Dict[builtins.str, typing.Any]]]]] = None,
        task_retry_maximum: typing.Optional[jsii.Number] = None,
        wait_for_success: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param command_line: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#command_line BatchPool#command_line}.
        :param user_identity: user_identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#user_identity BatchPool#user_identity}
        :param common_environment_properties: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#common_environment_properties BatchPool#common_environment_properties}.
        :param container: container block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#container BatchPool#container}
        :param resource_file: resource_file block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#resource_file BatchPool#resource_file}
        :param task_retry_maximum: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#task_retry_maximum BatchPool#task_retry_maximum}.
        :param wait_for_success: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#wait_for_success BatchPool#wait_for_success}.
        '''
        if isinstance(user_identity, dict):
            user_identity = BatchPoolStartTaskUserIdentity(**user_identity)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b129410fb7c7457dea1af0197cf0fb7afa606adb52b25ed05c46d83c06c7ab0)
            check_type(argname="argument command_line", value=command_line, expected_type=type_hints["command_line"])
            check_type(argname="argument user_identity", value=user_identity, expected_type=type_hints["user_identity"])
            check_type(argname="argument common_environment_properties", value=common_environment_properties, expected_type=type_hints["common_environment_properties"])
            check_type(argname="argument container", value=container, expected_type=type_hints["container"])
            check_type(argname="argument resource_file", value=resource_file, expected_type=type_hints["resource_file"])
            check_type(argname="argument task_retry_maximum", value=task_retry_maximum, expected_type=type_hints["task_retry_maximum"])
            check_type(argname="argument wait_for_success", value=wait_for_success, expected_type=type_hints["wait_for_success"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "command_line": command_line,
            "user_identity": user_identity,
        }
        if common_environment_properties is not None:
            self._values["common_environment_properties"] = common_environment_properties
        if container is not None:
            self._values["container"] = container
        if resource_file is not None:
            self._values["resource_file"] = resource_file
        if task_retry_maximum is not None:
            self._values["task_retry_maximum"] = task_retry_maximum
        if wait_for_success is not None:
            self._values["wait_for_success"] = wait_for_success

    @builtins.property
    def command_line(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#command_line BatchPool#command_line}.'''
        result = self._values.get("command_line")
        assert result is not None, "Required property 'command_line' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def user_identity(self) -> "BatchPoolStartTaskUserIdentity":
        '''user_identity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#user_identity BatchPool#user_identity}
        '''
        result = self._values.get("user_identity")
        assert result is not None, "Required property 'user_identity' is missing"
        return typing.cast("BatchPoolStartTaskUserIdentity", result)

    @builtins.property
    def common_environment_properties(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#common_environment_properties BatchPool#common_environment_properties}.'''
        result = self._values.get("common_environment_properties")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def container(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BatchPoolStartTaskContainer"]]]:
        '''container block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#container BatchPool#container}
        '''
        result = self._values.get("container")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BatchPoolStartTaskContainer"]]], result)

    @builtins.property
    def resource_file(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BatchPoolStartTaskResourceFile"]]]:
        '''resource_file block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#resource_file BatchPool#resource_file}
        '''
        result = self._values.get("resource_file")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BatchPoolStartTaskResourceFile"]]], result)

    @builtins.property
    def task_retry_maximum(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#task_retry_maximum BatchPool#task_retry_maximum}.'''
        result = self._values.get("task_retry_maximum")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def wait_for_success(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#wait_for_success BatchPool#wait_for_success}.'''
        result = self._values.get("wait_for_success")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BatchPoolStartTask(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolStartTaskContainer",
    jsii_struct_bases=[],
    name_mapping={
        "image_name": "imageName",
        "registry": "registry",
        "run_options": "runOptions",
        "working_directory": "workingDirectory",
    },
)
class BatchPoolStartTaskContainer:
    def __init__(
        self,
        *,
        image_name: builtins.str,
        registry: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BatchPoolStartTaskContainerRegistry", typing.Dict[builtins.str, typing.Any]]]]] = None,
        run_options: typing.Optional[builtins.str] = None,
        working_directory: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param image_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#image_name BatchPool#image_name}.
        :param registry: registry block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#registry BatchPool#registry}
        :param run_options: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#run_options BatchPool#run_options}.
        :param working_directory: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#working_directory BatchPool#working_directory}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a36110245679d9ded5f4dcc61d437534a4626bb854e9714aff157db611fb8dd)
            check_type(argname="argument image_name", value=image_name, expected_type=type_hints["image_name"])
            check_type(argname="argument registry", value=registry, expected_type=type_hints["registry"])
            check_type(argname="argument run_options", value=run_options, expected_type=type_hints["run_options"])
            check_type(argname="argument working_directory", value=working_directory, expected_type=type_hints["working_directory"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "image_name": image_name,
        }
        if registry is not None:
            self._values["registry"] = registry
        if run_options is not None:
            self._values["run_options"] = run_options
        if working_directory is not None:
            self._values["working_directory"] = working_directory

    @builtins.property
    def image_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#image_name BatchPool#image_name}.'''
        result = self._values.get("image_name")
        assert result is not None, "Required property 'image_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def registry(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BatchPoolStartTaskContainerRegistry"]]]:
        '''registry block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#registry BatchPool#registry}
        '''
        result = self._values.get("registry")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BatchPoolStartTaskContainerRegistry"]]], result)

    @builtins.property
    def run_options(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#run_options BatchPool#run_options}.'''
        result = self._values.get("run_options")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def working_directory(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#working_directory BatchPool#working_directory}.'''
        result = self._values.get("working_directory")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BatchPoolStartTaskContainer(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BatchPoolStartTaskContainerList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolStartTaskContainerList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c743c3b102693d203eacb625000e0df00a5ee3e61682afe97e72c6eebec89ca7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "BatchPoolStartTaskContainerOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42a0954b1d728a180caa4ddfa2f1e48016cb0fdfadc02a549127c39bf0ef54ec)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BatchPoolStartTaskContainerOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fce61ae77d4588136042e63c08a84f1cc3ab45d69e1f6a6f9e2ff280e4ed6f5c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3fc71a8f5e2c51b6d1d514446471051cc194f706a1fa740b7fbb0c21d53ff736)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ee3603ea087f1184896538d782207cb4d80db1e8a5d938ac26ebb9cd545c2bae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolStartTaskContainer]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolStartTaskContainer]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolStartTaskContainer]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa16aa2dbd859a1af91778ed11cce182a251aee9654d623603803a6bb472c081)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BatchPoolStartTaskContainerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolStartTaskContainerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__edf307466a1386e5695f34cc59e1f9bf6cddccb246fb8ce49607872277b54a35)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putRegistry")
    def put_registry(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BatchPoolStartTaskContainerRegistry", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa1b4b6373482ae1efe0fffe5f659ccf8b08b5fe44ac45778de8a56e6d130e2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRegistry", [value]))

    @jsii.member(jsii_name="resetRegistry")
    def reset_registry(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegistry", []))

    @jsii.member(jsii_name="resetRunOptions")
    def reset_run_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRunOptions", []))

    @jsii.member(jsii_name="resetWorkingDirectory")
    def reset_working_directory(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkingDirectory", []))

    @builtins.property
    @jsii.member(jsii_name="registry")
    def registry(self) -> "BatchPoolStartTaskContainerRegistryList":
        return typing.cast("BatchPoolStartTaskContainerRegistryList", jsii.get(self, "registry"))

    @builtins.property
    @jsii.member(jsii_name="imageNameInput")
    def image_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageNameInput"))

    @builtins.property
    @jsii.member(jsii_name="registryInput")
    def registry_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BatchPoolStartTaskContainerRegistry"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BatchPoolStartTaskContainerRegistry"]]], jsii.get(self, "registryInput"))

    @builtins.property
    @jsii.member(jsii_name="runOptionsInput")
    def run_options_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "runOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="workingDirectoryInput")
    def working_directory_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workingDirectoryInput"))

    @builtins.property
    @jsii.member(jsii_name="imageName")
    def image_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageName"))

    @image_name.setter
    def image_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0511ed092cdf169918a0ec1940b90455f8bed3050dcdf4d1a9ec82df920c337)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runOptions")
    def run_options(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runOptions"))

    @run_options.setter
    def run_options(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd889da71ba18a4663bdce11a72fa6c9c2041ed305f4ec48fccdc44f21e36691)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runOptions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workingDirectory")
    def working_directory(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workingDirectory"))

    @working_directory.setter
    def working_directory(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__996fcefdaa6973faee3cbf833c5525a4e957427e4e5ca2568c505bf9607d5082)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workingDirectory", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolStartTaskContainer]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolStartTaskContainer]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolStartTaskContainer]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d5f7ae15045344fc613a1858452b3c8826b9c06fc8b84d1345825bd88a66a33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolStartTaskContainerRegistry",
    jsii_struct_bases=[],
    name_mapping={
        "registry_server": "registryServer",
        "password": "password",
        "user_assigned_identity_id": "userAssignedIdentityId",
        "user_name": "userName",
    },
)
class BatchPoolStartTaskContainerRegistry:
    def __init__(
        self,
        *,
        registry_server: builtins.str,
        password: typing.Optional[builtins.str] = None,
        user_assigned_identity_id: typing.Optional[builtins.str] = None,
        user_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param registry_server: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#registry_server BatchPool#registry_server}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#password BatchPool#password}.
        :param user_assigned_identity_id: The User Assigned Identity to use for Container Registry access. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#user_assigned_identity_id BatchPool#user_assigned_identity_id}
        :param user_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#user_name BatchPool#user_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8544707ba727677a0848727d979c591c9dbb431b773599955b26c91ae8269983)
            check_type(argname="argument registry_server", value=registry_server, expected_type=type_hints["registry_server"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument user_assigned_identity_id", value=user_assigned_identity_id, expected_type=type_hints["user_assigned_identity_id"])
            check_type(argname="argument user_name", value=user_name, expected_type=type_hints["user_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "registry_server": registry_server,
        }
        if password is not None:
            self._values["password"] = password
        if user_assigned_identity_id is not None:
            self._values["user_assigned_identity_id"] = user_assigned_identity_id
        if user_name is not None:
            self._values["user_name"] = user_name

    @builtins.property
    def registry_server(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#registry_server BatchPool#registry_server}.'''
        result = self._values.get("registry_server")
        assert result is not None, "Required property 'registry_server' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#password BatchPool#password}.'''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_assigned_identity_id(self) -> typing.Optional[builtins.str]:
        '''The User Assigned Identity to use for Container Registry access.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#user_assigned_identity_id BatchPool#user_assigned_identity_id}
        '''
        result = self._values.get("user_assigned_identity_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#user_name BatchPool#user_name}.'''
        result = self._values.get("user_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BatchPoolStartTaskContainerRegistry(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BatchPoolStartTaskContainerRegistryList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolStartTaskContainerRegistryList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__34c3ce504253a78b4004cf8b97b16d5dbff673ed08ffa06385c55587720dabbd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BatchPoolStartTaskContainerRegistryOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38f1de0259cb84cd737f939c5c862c3943de34e93eac985ccedc1e08558e8ad7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BatchPoolStartTaskContainerRegistryOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00794d05c1fcc1b9f0afeba08a0e7603c08c84a44a6b53a8a0d9ba65bc43b8af)
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
            type_hints = typing.get_type_hints(_typecheckingstub__422f1c8f74528f36896fc4a7e92a2077a626cf82a99af0ddd8b3fd85c23d8ac7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__81de57fc322ed44fd89a9d56d83ac57f4db8eb10982b842f68a19f9b0a942f86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolStartTaskContainerRegistry]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolStartTaskContainerRegistry]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolStartTaskContainerRegistry]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2326caee1ca8eede156eb491c00fa3dd1e51b90731bb124a2663fd147b6aff56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BatchPoolStartTaskContainerRegistryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolStartTaskContainerRegistryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2104a3de8a07e898ad80eb412140bc90411505751cf114741c5f5d5a1cf464f3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @jsii.member(jsii_name="resetUserAssignedIdentityId")
    def reset_user_assigned_identity_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserAssignedIdentityId", []))

    @jsii.member(jsii_name="resetUserName")
    def reset_user_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserName", []))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="registryServerInput")
    def registry_server_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "registryServerInput"))

    @builtins.property
    @jsii.member(jsii_name="userAssignedIdentityIdInput")
    def user_assigned_identity_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userAssignedIdentityIdInput"))

    @builtins.property
    @jsii.member(jsii_name="userNameInput")
    def user_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userNameInput"))

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__000b20f1b2f16024e570096806df4c4e0b8118a0e16e7c5ada363dcdaa8ac8c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="registryServer")
    def registry_server(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "registryServer"))

    @registry_server.setter
    def registry_server(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ec192032be37670a76cde9b6d9b330e6cc00d03325c4f0f99e63f9043b8b445)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "registryServer", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userAssignedIdentityId")
    def user_assigned_identity_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userAssignedIdentityId"))

    @user_assigned_identity_id.setter
    def user_assigned_identity_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e935134b75fe5f6776accb5542a8615574a2aa0e173ffd2575e90ab9024f7b5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userAssignedIdentityId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userName")
    def user_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userName"))

    @user_name.setter
    def user_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca2d22b15fe1692aa7c7107e36b342d64ee0f3bb1abe2ca7c22ab0edbd143cb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolStartTaskContainerRegistry]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolStartTaskContainerRegistry]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolStartTaskContainerRegistry]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eeae20723d01f6b496b5f3b5289d1f3816ce7bc6d0137a7d275b693c680c5b57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BatchPoolStartTaskOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolStartTaskOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__77e64a98e808f4b70b05e052de9e255808e09d44c50c0549f64c63512cc0eac0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putContainer")
    def put_container(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BatchPoolStartTaskContainer, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe84622db29542bfe280235aa00036180c4291ea2ae002b8566b52098709210a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putContainer", [value]))

    @jsii.member(jsii_name="putResourceFile")
    def put_resource_file(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BatchPoolStartTaskResourceFile", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b95a912a30741a98e6f031c47f6975d91165690f739ff6d0d6ee52d7118ab2ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putResourceFile", [value]))

    @jsii.member(jsii_name="putUserIdentity")
    def put_user_identity(
        self,
        *,
        auto_user: typing.Optional[typing.Union["BatchPoolStartTaskUserIdentityAutoUser", typing.Dict[builtins.str, typing.Any]]] = None,
        user_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param auto_user: auto_user block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#auto_user BatchPool#auto_user}
        :param user_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#user_name BatchPool#user_name}.
        '''
        value = BatchPoolStartTaskUserIdentity(
            auto_user=auto_user, user_name=user_name
        )

        return typing.cast(None, jsii.invoke(self, "putUserIdentity", [value]))

    @jsii.member(jsii_name="resetCommonEnvironmentProperties")
    def reset_common_environment_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommonEnvironmentProperties", []))

    @jsii.member(jsii_name="resetContainer")
    def reset_container(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainer", []))

    @jsii.member(jsii_name="resetResourceFile")
    def reset_resource_file(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceFile", []))

    @jsii.member(jsii_name="resetTaskRetryMaximum")
    def reset_task_retry_maximum(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTaskRetryMaximum", []))

    @jsii.member(jsii_name="resetWaitForSuccess")
    def reset_wait_for_success(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWaitForSuccess", []))

    @builtins.property
    @jsii.member(jsii_name="container")
    def container(self) -> BatchPoolStartTaskContainerList:
        return typing.cast(BatchPoolStartTaskContainerList, jsii.get(self, "container"))

    @builtins.property
    @jsii.member(jsii_name="resourceFile")
    def resource_file(self) -> "BatchPoolStartTaskResourceFileList":
        return typing.cast("BatchPoolStartTaskResourceFileList", jsii.get(self, "resourceFile"))

    @builtins.property
    @jsii.member(jsii_name="userIdentity")
    def user_identity(self) -> "BatchPoolStartTaskUserIdentityOutputReference":
        return typing.cast("BatchPoolStartTaskUserIdentityOutputReference", jsii.get(self, "userIdentity"))

    @builtins.property
    @jsii.member(jsii_name="commandLineInput")
    def command_line_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commandLineInput"))

    @builtins.property
    @jsii.member(jsii_name="commonEnvironmentPropertiesInput")
    def common_environment_properties_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "commonEnvironmentPropertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="containerInput")
    def container_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolStartTaskContainer]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolStartTaskContainer]]], jsii.get(self, "containerInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceFileInput")
    def resource_file_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BatchPoolStartTaskResourceFile"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BatchPoolStartTaskResourceFile"]]], jsii.get(self, "resourceFileInput"))

    @builtins.property
    @jsii.member(jsii_name="taskRetryMaximumInput")
    def task_retry_maximum_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "taskRetryMaximumInput"))

    @builtins.property
    @jsii.member(jsii_name="userIdentityInput")
    def user_identity_input(self) -> typing.Optional["BatchPoolStartTaskUserIdentity"]:
        return typing.cast(typing.Optional["BatchPoolStartTaskUserIdentity"], jsii.get(self, "userIdentityInput"))

    @builtins.property
    @jsii.member(jsii_name="waitForSuccessInput")
    def wait_for_success_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "waitForSuccessInput"))

    @builtins.property
    @jsii.member(jsii_name="commandLine")
    def command_line(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "commandLine"))

    @command_line.setter
    def command_line(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acfbb1cb7a44aaa13e5bebbaa084dc0af8d98ee4da3f320c4b3c5f61c74c131c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "commandLine", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="commonEnvironmentProperties")
    def common_environment_properties(
        self,
    ) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "commonEnvironmentProperties"))

    @common_environment_properties.setter
    def common_environment_properties(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f9100e0ec59a8cb28a939089edc65ab08c9d1337ab4da04579d847a2c0751ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "commonEnvironmentProperties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="taskRetryMaximum")
    def task_retry_maximum(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "taskRetryMaximum"))

    @task_retry_maximum.setter
    def task_retry_maximum(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64d499a447c49de0da1ea5f5977d81831b283ceb90cfed339a0b26bfb6bece9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "taskRetryMaximum", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="waitForSuccess")
    def wait_for_success(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "waitForSuccess"))

    @wait_for_success.setter
    def wait_for_success(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbe1958a67464281b085803005956abbaa466e9968fccf9fa5c0fd7f060a5967)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "waitForSuccess", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BatchPoolStartTask]:
        return typing.cast(typing.Optional[BatchPoolStartTask], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[BatchPoolStartTask]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aed837a001a1290e9012ca51b7b4f779ea5e9cd8a1f9f7f0b29c125d2dd0e08c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolStartTaskResourceFile",
    jsii_struct_bases=[],
    name_mapping={
        "auto_storage_container_name": "autoStorageContainerName",
        "blob_prefix": "blobPrefix",
        "file_mode": "fileMode",
        "file_path": "filePath",
        "http_url": "httpUrl",
        "storage_container_url": "storageContainerUrl",
        "user_assigned_identity_id": "userAssignedIdentityId",
    },
)
class BatchPoolStartTaskResourceFile:
    def __init__(
        self,
        *,
        auto_storage_container_name: typing.Optional[builtins.str] = None,
        blob_prefix: typing.Optional[builtins.str] = None,
        file_mode: typing.Optional[builtins.str] = None,
        file_path: typing.Optional[builtins.str] = None,
        http_url: typing.Optional[builtins.str] = None,
        storage_container_url: typing.Optional[builtins.str] = None,
        user_assigned_identity_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param auto_storage_container_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#auto_storage_container_name BatchPool#auto_storage_container_name}.
        :param blob_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#blob_prefix BatchPool#blob_prefix}.
        :param file_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#file_mode BatchPool#file_mode}.
        :param file_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#file_path BatchPool#file_path}.
        :param http_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#http_url BatchPool#http_url}.
        :param storage_container_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#storage_container_url BatchPool#storage_container_url}.
        :param user_assigned_identity_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#user_assigned_identity_id BatchPool#user_assigned_identity_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d9019af978675b13bbff60442f764a3411bba3aa9c453278cfbba2f871e6532)
            check_type(argname="argument auto_storage_container_name", value=auto_storage_container_name, expected_type=type_hints["auto_storage_container_name"])
            check_type(argname="argument blob_prefix", value=blob_prefix, expected_type=type_hints["blob_prefix"])
            check_type(argname="argument file_mode", value=file_mode, expected_type=type_hints["file_mode"])
            check_type(argname="argument file_path", value=file_path, expected_type=type_hints["file_path"])
            check_type(argname="argument http_url", value=http_url, expected_type=type_hints["http_url"])
            check_type(argname="argument storage_container_url", value=storage_container_url, expected_type=type_hints["storage_container_url"])
            check_type(argname="argument user_assigned_identity_id", value=user_assigned_identity_id, expected_type=type_hints["user_assigned_identity_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auto_storage_container_name is not None:
            self._values["auto_storage_container_name"] = auto_storage_container_name
        if blob_prefix is not None:
            self._values["blob_prefix"] = blob_prefix
        if file_mode is not None:
            self._values["file_mode"] = file_mode
        if file_path is not None:
            self._values["file_path"] = file_path
        if http_url is not None:
            self._values["http_url"] = http_url
        if storage_container_url is not None:
            self._values["storage_container_url"] = storage_container_url
        if user_assigned_identity_id is not None:
            self._values["user_assigned_identity_id"] = user_assigned_identity_id

    @builtins.property
    def auto_storage_container_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#auto_storage_container_name BatchPool#auto_storage_container_name}.'''
        result = self._values.get("auto_storage_container_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def blob_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#blob_prefix BatchPool#blob_prefix}.'''
        result = self._values.get("blob_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def file_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#file_mode BatchPool#file_mode}.'''
        result = self._values.get("file_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def file_path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#file_path BatchPool#file_path}.'''
        result = self._values.get("file_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http_url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#http_url BatchPool#http_url}.'''
        result = self._values.get("http_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_container_url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#storage_container_url BatchPool#storage_container_url}.'''
        result = self._values.get("storage_container_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_assigned_identity_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#user_assigned_identity_id BatchPool#user_assigned_identity_id}.'''
        result = self._values.get("user_assigned_identity_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BatchPoolStartTaskResourceFile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BatchPoolStartTaskResourceFileList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolStartTaskResourceFileList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__72cc9831fdb48b606cf605a1667daa96381ee430c7e5d9824afa640c2b4a0e15)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BatchPoolStartTaskResourceFileOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e56206ee18ee417ca51b303dda55355b0b8db7d0a6fde2c9fc9905b3578a202)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BatchPoolStartTaskResourceFileOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5670249586a037eb375147fa1d07483028d067bcadbf23bcfb80693d6cc09420)
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
            type_hints = typing.get_type_hints(_typecheckingstub__02ac937e62625c78cfcd87e0cb7be58da34bd4f99c1ce4a6ed324782ba784c03)
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
            type_hints = typing.get_type_hints(_typecheckingstub__35cfb786d7384152af37c6e826d83feffafba0c279317447047b4a209028f84d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolStartTaskResourceFile]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolStartTaskResourceFile]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolStartTaskResourceFile]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3467f00ee9b720ff54984ae9d61e83f3b4dd4804f6f712037b169c3a296896ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BatchPoolStartTaskResourceFileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolStartTaskResourceFileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3dabb265f57709dde0e44ee64489286bfee594886fde8f420668559c552d0e0d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAutoStorageContainerName")
    def reset_auto_storage_container_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoStorageContainerName", []))

    @jsii.member(jsii_name="resetBlobPrefix")
    def reset_blob_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBlobPrefix", []))

    @jsii.member(jsii_name="resetFileMode")
    def reset_file_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFileMode", []))

    @jsii.member(jsii_name="resetFilePath")
    def reset_file_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilePath", []))

    @jsii.member(jsii_name="resetHttpUrl")
    def reset_http_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpUrl", []))

    @jsii.member(jsii_name="resetStorageContainerUrl")
    def reset_storage_container_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageContainerUrl", []))

    @jsii.member(jsii_name="resetUserAssignedIdentityId")
    def reset_user_assigned_identity_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserAssignedIdentityId", []))

    @builtins.property
    @jsii.member(jsii_name="autoStorageContainerNameInput")
    def auto_storage_container_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "autoStorageContainerNameInput"))

    @builtins.property
    @jsii.member(jsii_name="blobPrefixInput")
    def blob_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "blobPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="fileModeInput")
    def file_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fileModeInput"))

    @builtins.property
    @jsii.member(jsii_name="filePathInput")
    def file_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filePathInput"))

    @builtins.property
    @jsii.member(jsii_name="httpUrlInput")
    def http_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="storageContainerUrlInput")
    def storage_container_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageContainerUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="userAssignedIdentityIdInput")
    def user_assigned_identity_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userAssignedIdentityIdInput"))

    @builtins.property
    @jsii.member(jsii_name="autoStorageContainerName")
    def auto_storage_container_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "autoStorageContainerName"))

    @auto_storage_container_name.setter
    def auto_storage_container_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43eb7c69a5f04b492fae1a77519da80162f85489531cb5749e6ecb5d0ad79e37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoStorageContainerName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="blobPrefix")
    def blob_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "blobPrefix"))

    @blob_prefix.setter
    def blob_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40806f800e16303c199c1db1c62b6505acd05edef2369aa31865755205a5b2ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "blobPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fileMode")
    def file_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fileMode"))

    @file_mode.setter
    def file_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10040c6afffd83980210dafaf1e4db9c2c44a53f7fab2496250520d4cdabe150)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="filePath")
    def file_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filePath"))

    @file_path.setter
    def file_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbdbc8f60e93d7f4b7cbd264e7ebe57f93b37bf13be07157b2e2790adfe2dd90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filePath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpUrl")
    def http_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpUrl"))

    @http_url.setter
    def http_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8afd906add560325e6bdded2bc6120d345a1f62a4cb136a99d4fb4bdaa801028)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageContainerUrl")
    def storage_container_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageContainerUrl"))

    @storage_container_url.setter
    def storage_container_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d790a0b944ef490f911de93fe2b001074f7631cffbe609d73a863a6bca01101)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageContainerUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userAssignedIdentityId")
    def user_assigned_identity_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userAssignedIdentityId"))

    @user_assigned_identity_id.setter
    def user_assigned_identity_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d085c271dfae1170866a95de5788c27ca5aaa50289ddc22192f95ad4ff2a72d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userAssignedIdentityId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolStartTaskResourceFile]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolStartTaskResourceFile]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolStartTaskResourceFile]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2575d089e18241f4e7475dcf1913e39dd8eefaaf19c35cd8b586bc782add2287)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolStartTaskUserIdentity",
    jsii_struct_bases=[],
    name_mapping={"auto_user": "autoUser", "user_name": "userName"},
)
class BatchPoolStartTaskUserIdentity:
    def __init__(
        self,
        *,
        auto_user: typing.Optional[typing.Union["BatchPoolStartTaskUserIdentityAutoUser", typing.Dict[builtins.str, typing.Any]]] = None,
        user_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param auto_user: auto_user block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#auto_user BatchPool#auto_user}
        :param user_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#user_name BatchPool#user_name}.
        '''
        if isinstance(auto_user, dict):
            auto_user = BatchPoolStartTaskUserIdentityAutoUser(**auto_user)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf4069ac861c4598020e75a7c3ee3385621f870fd970e2d931b6bbdafce069ed)
            check_type(argname="argument auto_user", value=auto_user, expected_type=type_hints["auto_user"])
            check_type(argname="argument user_name", value=user_name, expected_type=type_hints["user_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auto_user is not None:
            self._values["auto_user"] = auto_user
        if user_name is not None:
            self._values["user_name"] = user_name

    @builtins.property
    def auto_user(self) -> typing.Optional["BatchPoolStartTaskUserIdentityAutoUser"]:
        '''auto_user block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#auto_user BatchPool#auto_user}
        '''
        result = self._values.get("auto_user")
        return typing.cast(typing.Optional["BatchPoolStartTaskUserIdentityAutoUser"], result)

    @builtins.property
    def user_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#user_name BatchPool#user_name}.'''
        result = self._values.get("user_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BatchPoolStartTaskUserIdentity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolStartTaskUserIdentityAutoUser",
    jsii_struct_bases=[],
    name_mapping={"elevation_level": "elevationLevel", "scope": "scope"},
)
class BatchPoolStartTaskUserIdentityAutoUser:
    def __init__(
        self,
        *,
        elevation_level: typing.Optional[builtins.str] = None,
        scope: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param elevation_level: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#elevation_level BatchPool#elevation_level}.
        :param scope: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#scope BatchPool#scope}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec3aed7d18e610e6b4d8f2326355e7a315a318454b73abad04335a23c6e62ece)
            check_type(argname="argument elevation_level", value=elevation_level, expected_type=type_hints["elevation_level"])
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if elevation_level is not None:
            self._values["elevation_level"] = elevation_level
        if scope is not None:
            self._values["scope"] = scope

    @builtins.property
    def elevation_level(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#elevation_level BatchPool#elevation_level}.'''
        result = self._values.get("elevation_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scope(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#scope BatchPool#scope}.'''
        result = self._values.get("scope")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BatchPoolStartTaskUserIdentityAutoUser(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BatchPoolStartTaskUserIdentityAutoUserOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolStartTaskUserIdentityAutoUserOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d44c2d97bf05cbf5b12d58b9b4579766d3ceaee029ac6694352b0f7a46506107)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetElevationLevel")
    def reset_elevation_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetElevationLevel", []))

    @jsii.member(jsii_name="resetScope")
    def reset_scope(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScope", []))

    @builtins.property
    @jsii.member(jsii_name="elevationLevelInput")
    def elevation_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "elevationLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="scopeInput")
    def scope_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scopeInput"))

    @builtins.property
    @jsii.member(jsii_name="elevationLevel")
    def elevation_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "elevationLevel"))

    @elevation_level.setter
    def elevation_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e0db8a5627a47c43b9f34c1b57fa08a33f573dc43b47cb67df7d0a0c973995f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "elevationLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scope"))

    @scope.setter
    def scope(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a4072532adbe353bac7696b11ae22799f8f30681b5e1d8c55c81923d8a0f14a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scope", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BatchPoolStartTaskUserIdentityAutoUser]:
        return typing.cast(typing.Optional[BatchPoolStartTaskUserIdentityAutoUser], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BatchPoolStartTaskUserIdentityAutoUser],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c1e34d44b3ac0b73b8abaa73059c20c68109010090032edff917cb012cac566)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BatchPoolStartTaskUserIdentityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolStartTaskUserIdentityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2f8f3aacbdb8602eab17a27b85b1ab02934661c9486c48b08d540a69be33a326)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAutoUser")
    def put_auto_user(
        self,
        *,
        elevation_level: typing.Optional[builtins.str] = None,
        scope: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param elevation_level: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#elevation_level BatchPool#elevation_level}.
        :param scope: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#scope BatchPool#scope}.
        '''
        value = BatchPoolStartTaskUserIdentityAutoUser(
            elevation_level=elevation_level, scope=scope
        )

        return typing.cast(None, jsii.invoke(self, "putAutoUser", [value]))

    @jsii.member(jsii_name="resetAutoUser")
    def reset_auto_user(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoUser", []))

    @jsii.member(jsii_name="resetUserName")
    def reset_user_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserName", []))

    @builtins.property
    @jsii.member(jsii_name="autoUser")
    def auto_user(self) -> BatchPoolStartTaskUserIdentityAutoUserOutputReference:
        return typing.cast(BatchPoolStartTaskUserIdentityAutoUserOutputReference, jsii.get(self, "autoUser"))

    @builtins.property
    @jsii.member(jsii_name="autoUserInput")
    def auto_user_input(
        self,
    ) -> typing.Optional[BatchPoolStartTaskUserIdentityAutoUser]:
        return typing.cast(typing.Optional[BatchPoolStartTaskUserIdentityAutoUser], jsii.get(self, "autoUserInput"))

    @builtins.property
    @jsii.member(jsii_name="userNameInput")
    def user_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userNameInput"))

    @builtins.property
    @jsii.member(jsii_name="userName")
    def user_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userName"))

    @user_name.setter
    def user_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bce9880edbe48baf5e6a23f10f890f344071994cc3d768ee2d7591b79fcc73fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BatchPoolStartTaskUserIdentity]:
        return typing.cast(typing.Optional[BatchPoolStartTaskUserIdentity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BatchPoolStartTaskUserIdentity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51bd6b4632b17e91479366f2c9ac518163b2899191f39519935a5fb341783fa2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolStorageImageReference",
    jsii_struct_bases=[],
    name_mapping={
        "id": "id",
        "offer": "offer",
        "publisher": "publisher",
        "sku": "sku",
        "version": "version",
    },
)
class BatchPoolStorageImageReference:
    def __init__(
        self,
        *,
        id: typing.Optional[builtins.str] = None,
        offer: typing.Optional[builtins.str] = None,
        publisher: typing.Optional[builtins.str] = None,
        sku: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#id BatchPool#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param offer: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#offer BatchPool#offer}.
        :param publisher: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#publisher BatchPool#publisher}.
        :param sku: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#sku BatchPool#sku}.
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#version BatchPool#version}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60f2c35f6304e501c3a5241c1c0b08ffc5818faf02741d7dfd3102c430dcdefe)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument offer", value=offer, expected_type=type_hints["offer"])
            check_type(argname="argument publisher", value=publisher, expected_type=type_hints["publisher"])
            check_type(argname="argument sku", value=sku, expected_type=type_hints["sku"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if id is not None:
            self._values["id"] = id
        if offer is not None:
            self._values["offer"] = offer
        if publisher is not None:
            self._values["publisher"] = publisher
        if sku is not None:
            self._values["sku"] = sku
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#id BatchPool#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def offer(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#offer BatchPool#offer}.'''
        result = self._values.get("offer")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def publisher(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#publisher BatchPool#publisher}.'''
        result = self._values.get("publisher")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sku(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#sku BatchPool#sku}.'''
        result = self._values.get("sku")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#version BatchPool#version}.'''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BatchPoolStorageImageReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BatchPoolStorageImageReferenceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolStorageImageReferenceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3380b0cc976d85e34e8234b1f405393d40289062e4ea6ac7c14f14da747594a4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetOffer")
    def reset_offer(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOffer", []))

    @jsii.member(jsii_name="resetPublisher")
    def reset_publisher(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublisher", []))

    @jsii.member(jsii_name="resetSku")
    def reset_sku(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSku", []))

    @jsii.member(jsii_name="resetVersion")
    def reset_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersion", []))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="offerInput")
    def offer_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "offerInput"))

    @builtins.property
    @jsii.member(jsii_name="publisherInput")
    def publisher_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "publisherInput"))

    @builtins.property
    @jsii.member(jsii_name="skuInput")
    def sku_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "skuInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4073de4d2e90095b73b7ab6d0029556d6a745a0f190b700ea93bb769f206c6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="offer")
    def offer(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "offer"))

    @offer.setter
    def offer(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f6364a8a50cf51da162d4cda1de42ad47f9e0dc537a7405c3ac45e687c5f1d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "offer", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publisher")
    def publisher(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publisher"))

    @publisher.setter
    def publisher(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4dc17d9b0cbc7ff3d9b0e790e7792e8ee8d7bae6355b5a1856cdd6bdf0b47cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publisher", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sku")
    def sku(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sku"))

    @sku.setter
    def sku(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bf69c346e807f30b50ca9a1f9fdefa790fdacaf5ea76ced47121f47d541f867)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sku", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd118538bc8f859af39e3a48e3be69d609f5a634064e4919d21ecc050a99cffb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BatchPoolStorageImageReference]:
        return typing.cast(typing.Optional[BatchPoolStorageImageReference], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BatchPoolStorageImageReference],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__650088b5ff2a810a0be860efd9f91f36b39747321b85640a1949391482391626)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolTaskSchedulingPolicy",
    jsii_struct_bases=[],
    name_mapping={"node_fill_type": "nodeFillType"},
)
class BatchPoolTaskSchedulingPolicy:
    def __init__(self, *, node_fill_type: typing.Optional[builtins.str] = None) -> None:
        '''
        :param node_fill_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#node_fill_type BatchPool#node_fill_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__945763c0abd732e533a885948a7a36f875b2fbcac20c7e812dcc4a68401fde83)
            check_type(argname="argument node_fill_type", value=node_fill_type, expected_type=type_hints["node_fill_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if node_fill_type is not None:
            self._values["node_fill_type"] = node_fill_type

    @builtins.property
    def node_fill_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#node_fill_type BatchPool#node_fill_type}.'''
        result = self._values.get("node_fill_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BatchPoolTaskSchedulingPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BatchPoolTaskSchedulingPolicyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolTaskSchedulingPolicyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__76d8448e746fc6f5434af5bf3d2282cf6c2e7801b0547372c58c44047da67910)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "BatchPoolTaskSchedulingPolicyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba594b437e18e2edafb8b918de6a7f37f6a3797f9688f2dd73ddf36176ebb224)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BatchPoolTaskSchedulingPolicyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__340d603934ce8c0aa316bc6e9348c19972d8296d34ca29d6737f4583411148ad)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e6d205b26e903c1ee3a8aa67aceac99eefa2f6eee2c2455d8061b1947ae9a5c5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac2665ddd64f02122a578c43bd275708888f6ad42c513e13b5a13f1a273600aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolTaskSchedulingPolicy]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolTaskSchedulingPolicy]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolTaskSchedulingPolicy]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a5e54aaa212557d17558eb42f38c4491cded0692208aa08131ed99681f0f8ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BatchPoolTaskSchedulingPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolTaskSchedulingPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a0098463b1870df17473da7d12a0dfc0c5f7fc2f0985753e9497534f5be380d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetNodeFillType")
    def reset_node_fill_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeFillType", []))

    @builtins.property
    @jsii.member(jsii_name="nodeFillTypeInput")
    def node_fill_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nodeFillTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeFillType")
    def node_fill_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeFillType"))

    @node_fill_type.setter
    def node_fill_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6cc159a43d83dcd1b1ee86022867b09a06e336ff16d6321cafeae6ec07010cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeFillType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolTaskSchedulingPolicy]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolTaskSchedulingPolicy]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolTaskSchedulingPolicy]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__814c6b127752b286e253a6e8cfa3e26433251e41bde3040e57b5bd1503c7e5b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class BatchPoolTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#create BatchPool#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#delete BatchPool#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#read BatchPool#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#update BatchPool#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb151771b796f981020b716b74652c3254291af36aa451a866f841ab4427faf3)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#create BatchPool#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#delete BatchPool#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#read BatchPool#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#update BatchPool#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BatchPoolTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BatchPoolTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__268a7c374a8db56abbce08f53f105060051bd65bd6d8fd12dbecefba0fdeb3ad)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8133d93fad6326aee5aec3e8f6be47a5ec13e4197935965f3b3b07992e56c072)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef8ad46d06a38d4322e05684ce123a31283a5eee073f6fce7d6c9b1f90857aeb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7f99101da5c4047ed178cda3035ecd3d648c21681fc98513138bc85e098ce2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec5d654d2a6130e4a462368bc37a2503a0a2615e02d130d2a8f92a62d1a028d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e01c50556dca3461466f81fda4b569b6f946d3ab27e1867aeb0ffe81810ec28e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolUserAccounts",
    jsii_struct_bases=[],
    name_mapping={
        "elevation_level": "elevationLevel",
        "name": "name",
        "password": "password",
        "linux_user_configuration": "linuxUserConfiguration",
        "windows_user_configuration": "windowsUserConfiguration",
    },
)
class BatchPoolUserAccounts:
    def __init__(
        self,
        *,
        elevation_level: builtins.str,
        name: builtins.str,
        password: builtins.str,
        linux_user_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BatchPoolUserAccountsLinuxUserConfiguration", typing.Dict[builtins.str, typing.Any]]]]] = None,
        windows_user_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BatchPoolUserAccountsWindowsUserConfiguration", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param elevation_level: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#elevation_level BatchPool#elevation_level}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#name BatchPool#name}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#password BatchPool#password}.
        :param linux_user_configuration: linux_user_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#linux_user_configuration BatchPool#linux_user_configuration}
        :param windows_user_configuration: windows_user_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#windows_user_configuration BatchPool#windows_user_configuration}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16fbe5928d182db56ea3c2c5df121a519953cac9d2f702eec59b2282fcca1576)
            check_type(argname="argument elevation_level", value=elevation_level, expected_type=type_hints["elevation_level"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument linux_user_configuration", value=linux_user_configuration, expected_type=type_hints["linux_user_configuration"])
            check_type(argname="argument windows_user_configuration", value=windows_user_configuration, expected_type=type_hints["windows_user_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "elevation_level": elevation_level,
            "name": name,
            "password": password,
        }
        if linux_user_configuration is not None:
            self._values["linux_user_configuration"] = linux_user_configuration
        if windows_user_configuration is not None:
            self._values["windows_user_configuration"] = windows_user_configuration

    @builtins.property
    def elevation_level(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#elevation_level BatchPool#elevation_level}.'''
        result = self._values.get("elevation_level")
        assert result is not None, "Required property 'elevation_level' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#name BatchPool#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#password BatchPool#password}.'''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def linux_user_configuration(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BatchPoolUserAccountsLinuxUserConfiguration"]]]:
        '''linux_user_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#linux_user_configuration BatchPool#linux_user_configuration}
        '''
        result = self._values.get("linux_user_configuration")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BatchPoolUserAccountsLinuxUserConfiguration"]]], result)

    @builtins.property
    def windows_user_configuration(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BatchPoolUserAccountsWindowsUserConfiguration"]]]:
        '''windows_user_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#windows_user_configuration BatchPool#windows_user_configuration}
        '''
        result = self._values.get("windows_user_configuration")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BatchPoolUserAccountsWindowsUserConfiguration"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BatchPoolUserAccounts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolUserAccountsLinuxUserConfiguration",
    jsii_struct_bases=[],
    name_mapping={"gid": "gid", "ssh_private_key": "sshPrivateKey", "uid": "uid"},
)
class BatchPoolUserAccountsLinuxUserConfiguration:
    def __init__(
        self,
        *,
        gid: typing.Optional[jsii.Number] = None,
        ssh_private_key: typing.Optional[builtins.str] = None,
        uid: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param gid: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#gid BatchPool#gid}.
        :param ssh_private_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#ssh_private_key BatchPool#ssh_private_key}.
        :param uid: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#uid BatchPool#uid}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__860ff867c9bef3745df858028ed162906d9a2f7676cbb570adada9d1f2f01e3c)
            check_type(argname="argument gid", value=gid, expected_type=type_hints["gid"])
            check_type(argname="argument ssh_private_key", value=ssh_private_key, expected_type=type_hints["ssh_private_key"])
            check_type(argname="argument uid", value=uid, expected_type=type_hints["uid"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if gid is not None:
            self._values["gid"] = gid
        if ssh_private_key is not None:
            self._values["ssh_private_key"] = ssh_private_key
        if uid is not None:
            self._values["uid"] = uid

    @builtins.property
    def gid(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#gid BatchPool#gid}.'''
        result = self._values.get("gid")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ssh_private_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#ssh_private_key BatchPool#ssh_private_key}.'''
        result = self._values.get("ssh_private_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def uid(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#uid BatchPool#uid}.'''
        result = self._values.get("uid")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BatchPoolUserAccountsLinuxUserConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BatchPoolUserAccountsLinuxUserConfigurationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolUserAccountsLinuxUserConfigurationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__42a4562feee77c823d29f8890a0ebc43a120be4b64f6b5dcfc715580744c9009)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BatchPoolUserAccountsLinuxUserConfigurationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef72074a5e2cd0b4427764d3c994413f07c3d786cb254fc66f915ca2055c7c63)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BatchPoolUserAccountsLinuxUserConfigurationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af97320e5531f9c091637a72b4730ac2cccc6057239aa61ffa62c2edb7e80d22)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac3c005fa1bc644bc2b43fc314ab31af0ce35743b8daab0cefd150e2f8792524)
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
            type_hints = typing.get_type_hints(_typecheckingstub__47af667d16844e54da8823241e74db56bf64d4bcbfc14f7213c6d032ba669bbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolUserAccountsLinuxUserConfiguration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolUserAccountsLinuxUserConfiguration]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolUserAccountsLinuxUserConfiguration]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd395ce7d7899792b25d42d9ba43f53de1023f38b6ba112d06c6f62447d4ee41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BatchPoolUserAccountsLinuxUserConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolUserAccountsLinuxUserConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__13b21557f04feac4f3ebb2c7ed525a5160fffcc6af774f2c9aad88a0dc3bff4a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetGid")
    def reset_gid(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGid", []))

    @jsii.member(jsii_name="resetSshPrivateKey")
    def reset_ssh_private_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSshPrivateKey", []))

    @jsii.member(jsii_name="resetUid")
    def reset_uid(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUid", []))

    @builtins.property
    @jsii.member(jsii_name="gidInput")
    def gid_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "gidInput"))

    @builtins.property
    @jsii.member(jsii_name="sshPrivateKeyInput")
    def ssh_private_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sshPrivateKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="uidInput")
    def uid_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "uidInput"))

    @builtins.property
    @jsii.member(jsii_name="gid")
    def gid(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "gid"))

    @gid.setter
    def gid(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__937200869c92b5c701e03b93902549ecec7ab8c5f1da9d0af3fe4bf2961a09cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gid", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sshPrivateKey")
    def ssh_private_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sshPrivateKey"))

    @ssh_private_key.setter
    def ssh_private_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__159fdd4444501a338fb9adce27b450ddab1ddbafaec9b123fca57802d7c0dfc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sshPrivateKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uid")
    def uid(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "uid"))

    @uid.setter
    def uid(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1c65ec3637316be5b88afc0297b604b08578425bff586258cf30e3dda37493e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uid", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolUserAccountsLinuxUserConfiguration]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolUserAccountsLinuxUserConfiguration]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolUserAccountsLinuxUserConfiguration]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09cb04fa6c2725f77b6e1e2a49481c2ddb7d9bd4c5f277cab18c2d381d9cdc9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BatchPoolUserAccountsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolUserAccountsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb5a008cad9296bd09395ff8174766cf6ed29b1850574255dfa3c535f0041eb3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "BatchPoolUserAccountsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ecf1b0dbd9d4639c2f0f3ddfa122bef6c176fbb8bba5b7d40a8d5b47d09a18d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BatchPoolUserAccountsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3e04745bf630bacb07b3ef9fce41734e84e11f6a246c4ac08d3b3a6dc2ece39)
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
            type_hints = typing.get_type_hints(_typecheckingstub__acff7565cada32121fb5953a913f564b976a1821fedb531ab21be30b8510abcc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__465c0d6b73a2a4a4e48322032bac3ee0cb276ba73042634e3431874534f22a50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolUserAccounts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolUserAccounts]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolUserAccounts]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9f14dc7109eb02dc4f14a092248eff9c5e19d0f3e2420d8bc4d041e1607c6aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BatchPoolUserAccountsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolUserAccountsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__810003e32cebf4a1d8eff3382c7130ff386bd357313e96e55c4150fa36577f3b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putLinuxUserConfiguration")
    def put_linux_user_configuration(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BatchPoolUserAccountsLinuxUserConfiguration, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4758007952a2dc4298426013acc749a835d028e0bb47f72bfba2302039731716)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLinuxUserConfiguration", [value]))

    @jsii.member(jsii_name="putWindowsUserConfiguration")
    def put_windows_user_configuration(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BatchPoolUserAccountsWindowsUserConfiguration", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ff895fd26f38bcba0129bd46f62d3c88ee18fa89c5c263e7956c63795ac939e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putWindowsUserConfiguration", [value]))

    @jsii.member(jsii_name="resetLinuxUserConfiguration")
    def reset_linux_user_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLinuxUserConfiguration", []))

    @jsii.member(jsii_name="resetWindowsUserConfiguration")
    def reset_windows_user_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWindowsUserConfiguration", []))

    @builtins.property
    @jsii.member(jsii_name="linuxUserConfiguration")
    def linux_user_configuration(
        self,
    ) -> BatchPoolUserAccountsLinuxUserConfigurationList:
        return typing.cast(BatchPoolUserAccountsLinuxUserConfigurationList, jsii.get(self, "linuxUserConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="windowsUserConfiguration")
    def windows_user_configuration(
        self,
    ) -> "BatchPoolUserAccountsWindowsUserConfigurationList":
        return typing.cast("BatchPoolUserAccountsWindowsUserConfigurationList", jsii.get(self, "windowsUserConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="elevationLevelInput")
    def elevation_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "elevationLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="linuxUserConfigurationInput")
    def linux_user_configuration_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolUserAccountsLinuxUserConfiguration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolUserAccountsLinuxUserConfiguration]]], jsii.get(self, "linuxUserConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="windowsUserConfigurationInput")
    def windows_user_configuration_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BatchPoolUserAccountsWindowsUserConfiguration"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BatchPoolUserAccountsWindowsUserConfiguration"]]], jsii.get(self, "windowsUserConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="elevationLevel")
    def elevation_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "elevationLevel"))

    @elevation_level.setter
    def elevation_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4fb3e4ea2796ef57dfe0ce86e5f6607dec2fa376dc4bea0371fa40dfc8b123a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "elevationLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2354b2e32186f0c5186849a24d60542dfc93ae83a93f06f1cf162c16afb603dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59993ec021262db76f6401791752017161d91baa493da381f7e028e52d73d194)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolUserAccounts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolUserAccounts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolUserAccounts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__052c3ca46038d5a52b0ccd3824555814c5607ca65a6dedbab98b0b99b7652735)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolUserAccountsWindowsUserConfiguration",
    jsii_struct_bases=[],
    name_mapping={"login_mode": "loginMode"},
)
class BatchPoolUserAccountsWindowsUserConfiguration:
    def __init__(self, *, login_mode: builtins.str) -> None:
        '''
        :param login_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#login_mode BatchPool#login_mode}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae067d427001b50eac148deca0a356aff3a5dad4fb6164d49e0eb7da8bdd9e71)
            check_type(argname="argument login_mode", value=login_mode, expected_type=type_hints["login_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "login_mode": login_mode,
        }

    @builtins.property
    def login_mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#login_mode BatchPool#login_mode}.'''
        result = self._values.get("login_mode")
        assert result is not None, "Required property 'login_mode' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BatchPoolUserAccountsWindowsUserConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BatchPoolUserAccountsWindowsUserConfigurationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolUserAccountsWindowsUserConfigurationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__271edb5cb8d1e5f7f97e3b57ca1470afe4f9d3eff2ccfc01956512f3f05f1520)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BatchPoolUserAccountsWindowsUserConfigurationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1467c3c6a4d9081c7d8949c5d6e42a15394198d2145afe7a41ea33d82c312543)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BatchPoolUserAccountsWindowsUserConfigurationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4706f6591889ca58dcab395846e75f7d072b75b894a7f1303ae8942d133539f1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e2efcbbea55de77f05211550a79726c3598a7430ecdaa246d2a00cdbbaa3ce8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__72e413f032af4cd483b248f27823ed7ff5c9c0b55e67d0b122620af88f2b13df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolUserAccountsWindowsUserConfiguration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolUserAccountsWindowsUserConfiguration]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolUserAccountsWindowsUserConfiguration]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d01f3be38cfb021ae782b3ff847ea29d9db2e7b8dc41b465b7e89af310b0f6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BatchPoolUserAccountsWindowsUserConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolUserAccountsWindowsUserConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a0b10c843a2ac1e490c8bfbabaee4abd66227c1d1ac0d5b08fefc3999674124)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="loginModeInput")
    def login_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "loginModeInput"))

    @builtins.property
    @jsii.member(jsii_name="loginMode")
    def login_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loginMode"))

    @login_mode.setter
    def login_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3883cef82b12b7b5bb6c32b164be7d7314f7933090a32ad3f417506a3b4b385)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loginMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolUserAccountsWindowsUserConfiguration]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolUserAccountsWindowsUserConfiguration]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolUserAccountsWindowsUserConfiguration]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ab49e3c2bed1169409a4147b1f6d4fc60e6dcbeea8b9cffe7ef694b190ecb4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolWindows",
    jsii_struct_bases=[],
    name_mapping={"enable_automatic_updates": "enableAutomaticUpdates"},
)
class BatchPoolWindows:
    def __init__(
        self,
        *,
        enable_automatic_updates: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable_automatic_updates: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#enable_automatic_updates BatchPool#enable_automatic_updates}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b89b2c44e35b9298eb32de53e4171db49581b1d286039f5d1bbf8d06ca6873ca)
            check_type(argname="argument enable_automatic_updates", value=enable_automatic_updates, expected_type=type_hints["enable_automatic_updates"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enable_automatic_updates is not None:
            self._values["enable_automatic_updates"] = enable_automatic_updates

    @builtins.property
    def enable_automatic_updates(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/batch_pool#enable_automatic_updates BatchPool#enable_automatic_updates}.'''
        result = self._values.get("enable_automatic_updates")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BatchPoolWindows(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BatchPoolWindowsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolWindowsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__afb28756786136d0deaa2ab870b7b91393d9705649b825caf6ec05465fc01928)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "BatchPoolWindowsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b128cc3ef952c55a2bfe0b1617d9e967ac5c5478f22295fdbad995f50a9104e4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BatchPoolWindowsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b52db37dbabf9bfcab7c13585f8f1a92e3ee574a4a1b4a8979777ade50ca16e3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__98bcec575752d097e955665802498e55c3b9f8ab126b9640574c8c7ab02e28d4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c72af04b9269e8715f34822dfe8198e243d1a23b177a903e7a6e8768a43d674)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolWindows]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolWindows]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolWindows]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f81ce213b138e3657a430bc1a82b59b1c165aeaefd77f92ef5a840564800b32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BatchPoolWindowsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.batchPool.BatchPoolWindowsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4100ec27b5eecb21822b38c28a466b4b6d95e89d348d68d6bbedeb214a847cf0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetEnableAutomaticUpdates")
    def reset_enable_automatic_updates(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableAutomaticUpdates", []))

    @builtins.property
    @jsii.member(jsii_name="enableAutomaticUpdatesInput")
    def enable_automatic_updates_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableAutomaticUpdatesInput"))

    @builtins.property
    @jsii.member(jsii_name="enableAutomaticUpdates")
    def enable_automatic_updates(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableAutomaticUpdates"))

    @enable_automatic_updates.setter
    def enable_automatic_updates(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eeebf5a4e69eb06bcdd0ad6fc1fd87c177fad7d2b9d8e1aa9e26cf71a0684ca7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableAutomaticUpdates", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolWindows]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolWindows]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolWindows]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad612d3aba7733300e338a03fa4437e4425553a3339420296d12e39f6bd6b33c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "BatchPool",
    "BatchPoolAutoScale",
    "BatchPoolAutoScaleOutputReference",
    "BatchPoolCertificate",
    "BatchPoolCertificateList",
    "BatchPoolCertificateOutputReference",
    "BatchPoolConfig",
    "BatchPoolContainerConfiguration",
    "BatchPoolContainerConfigurationContainerRegistries",
    "BatchPoolContainerConfigurationContainerRegistriesList",
    "BatchPoolContainerConfigurationContainerRegistriesOutputReference",
    "BatchPoolContainerConfigurationOutputReference",
    "BatchPoolDataDisks",
    "BatchPoolDataDisksList",
    "BatchPoolDataDisksOutputReference",
    "BatchPoolDiskEncryption",
    "BatchPoolDiskEncryptionList",
    "BatchPoolDiskEncryptionOutputReference",
    "BatchPoolExtensions",
    "BatchPoolExtensionsList",
    "BatchPoolExtensionsOutputReference",
    "BatchPoolFixedScale",
    "BatchPoolFixedScaleOutputReference",
    "BatchPoolIdentity",
    "BatchPoolIdentityOutputReference",
    "BatchPoolMount",
    "BatchPoolMountAzureBlobFileSystem",
    "BatchPoolMountAzureBlobFileSystemOutputReference",
    "BatchPoolMountAzureFileShare",
    "BatchPoolMountAzureFileShareList",
    "BatchPoolMountAzureFileShareOutputReference",
    "BatchPoolMountCifsMount",
    "BatchPoolMountCifsMountList",
    "BatchPoolMountCifsMountOutputReference",
    "BatchPoolMountList",
    "BatchPoolMountNfsMount",
    "BatchPoolMountNfsMountList",
    "BatchPoolMountNfsMountOutputReference",
    "BatchPoolMountOutputReference",
    "BatchPoolNetworkConfiguration",
    "BatchPoolNetworkConfigurationEndpointConfiguration",
    "BatchPoolNetworkConfigurationEndpointConfigurationList",
    "BatchPoolNetworkConfigurationEndpointConfigurationNetworkSecurityGroupRules",
    "BatchPoolNetworkConfigurationEndpointConfigurationNetworkSecurityGroupRulesList",
    "BatchPoolNetworkConfigurationEndpointConfigurationNetworkSecurityGroupRulesOutputReference",
    "BatchPoolNetworkConfigurationEndpointConfigurationOutputReference",
    "BatchPoolNetworkConfigurationOutputReference",
    "BatchPoolNodePlacement",
    "BatchPoolNodePlacementList",
    "BatchPoolNodePlacementOutputReference",
    "BatchPoolSecurityProfile",
    "BatchPoolSecurityProfileOutputReference",
    "BatchPoolStartTask",
    "BatchPoolStartTaskContainer",
    "BatchPoolStartTaskContainerList",
    "BatchPoolStartTaskContainerOutputReference",
    "BatchPoolStartTaskContainerRegistry",
    "BatchPoolStartTaskContainerRegistryList",
    "BatchPoolStartTaskContainerRegistryOutputReference",
    "BatchPoolStartTaskOutputReference",
    "BatchPoolStartTaskResourceFile",
    "BatchPoolStartTaskResourceFileList",
    "BatchPoolStartTaskResourceFileOutputReference",
    "BatchPoolStartTaskUserIdentity",
    "BatchPoolStartTaskUserIdentityAutoUser",
    "BatchPoolStartTaskUserIdentityAutoUserOutputReference",
    "BatchPoolStartTaskUserIdentityOutputReference",
    "BatchPoolStorageImageReference",
    "BatchPoolStorageImageReferenceOutputReference",
    "BatchPoolTaskSchedulingPolicy",
    "BatchPoolTaskSchedulingPolicyList",
    "BatchPoolTaskSchedulingPolicyOutputReference",
    "BatchPoolTimeouts",
    "BatchPoolTimeoutsOutputReference",
    "BatchPoolUserAccounts",
    "BatchPoolUserAccountsLinuxUserConfiguration",
    "BatchPoolUserAccountsLinuxUserConfigurationList",
    "BatchPoolUserAccountsLinuxUserConfigurationOutputReference",
    "BatchPoolUserAccountsList",
    "BatchPoolUserAccountsOutputReference",
    "BatchPoolUserAccountsWindowsUserConfiguration",
    "BatchPoolUserAccountsWindowsUserConfigurationList",
    "BatchPoolUserAccountsWindowsUserConfigurationOutputReference",
    "BatchPoolWindows",
    "BatchPoolWindowsList",
    "BatchPoolWindowsOutputReference",
]

publication.publish()

def _typecheckingstub__9927cfe471f7371287173b14c3427a8020a17b70d5d71930e162e35a3a4eeac2(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    account_name: builtins.str,
    name: builtins.str,
    node_agent_sku_id: builtins.str,
    resource_group_name: builtins.str,
    storage_image_reference: typing.Union[BatchPoolStorageImageReference, typing.Dict[builtins.str, typing.Any]],
    vm_size: builtins.str,
    auto_scale: typing.Optional[typing.Union[BatchPoolAutoScale, typing.Dict[builtins.str, typing.Any]]] = None,
    certificate: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BatchPoolCertificate, typing.Dict[builtins.str, typing.Any]]]]] = None,
    container_configuration: typing.Optional[typing.Union[BatchPoolContainerConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    data_disks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BatchPoolDataDisks, typing.Dict[builtins.str, typing.Any]]]]] = None,
    disk_encryption: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BatchPoolDiskEncryption, typing.Dict[builtins.str, typing.Any]]]]] = None,
    display_name: typing.Optional[builtins.str] = None,
    extensions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BatchPoolExtensions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    fixed_scale: typing.Optional[typing.Union[BatchPoolFixedScale, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    identity: typing.Optional[typing.Union[BatchPoolIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    inter_node_communication: typing.Optional[builtins.str] = None,
    license_type: typing.Optional[builtins.str] = None,
    max_tasks_per_node: typing.Optional[jsii.Number] = None,
    metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    mount: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BatchPoolMount, typing.Dict[builtins.str, typing.Any]]]]] = None,
    network_configuration: typing.Optional[typing.Union[BatchPoolNetworkConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    node_placement: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BatchPoolNodePlacement, typing.Dict[builtins.str, typing.Any]]]]] = None,
    os_disk_placement: typing.Optional[builtins.str] = None,
    security_profile: typing.Optional[typing.Union[BatchPoolSecurityProfile, typing.Dict[builtins.str, typing.Any]]] = None,
    start_task: typing.Optional[typing.Union[BatchPoolStartTask, typing.Dict[builtins.str, typing.Any]]] = None,
    stop_pending_resize_operation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    target_node_communication_mode: typing.Optional[builtins.str] = None,
    task_scheduling_policy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BatchPoolTaskSchedulingPolicy, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[BatchPoolTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    user_accounts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BatchPoolUserAccounts, typing.Dict[builtins.str, typing.Any]]]]] = None,
    windows: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BatchPoolWindows, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__ceb722400d5153e0de9b1f027d5e667961eb620ad6d93e87346bdeffe7383203(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07d370a736db7cb3c2bd2df984b861cffadcc8910ba867c2434e9c756e646d7e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BatchPoolCertificate, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35257d15fed1c15a60db645c81026f4b8c27dfa7f143ee14aaca219e98e56f74(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BatchPoolDataDisks, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27c0c424f8504b933b82f1ccf646a562037fd5b0bf6264d115c53faa7597558f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BatchPoolDiskEncryption, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f31bf4dde13ab94425401b8db476711eec966f5d70870b75afd6a2294819dae(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BatchPoolExtensions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a23ec836dcc17734b65a525d817649ca7cc315fd6957af7461dc3c90bc1d42bc(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BatchPoolMount, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97a4b7225fd27e026980f86177b6ccb803f8033491ca08e9e6b818173b22f3f4(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BatchPoolNodePlacement, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1045de5fbe3c07b0454e0b9ba24faf36085b0d172fff779fde68f75e75e0cbf6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BatchPoolTaskSchedulingPolicy, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adce9721f01ea7caf079530820c53805e266c8e962bf6ae5d326667f64ef3b5c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BatchPoolUserAccounts, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a949698364f033323419948f7662e9e1bfa2fd235797c2be394ebfc55bcb4d9c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BatchPoolWindows, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc5b51e173f2ebfb3068704bf2bcfc9b18ee913117c04330b9aa6de4ca0b80e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__221b15332d5e73630053eb10d53e00ac00553f4e5311861f5928071294d3b4b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2af8570637cba2c006ae37435935c593cc4ac36268c215ecc43262f35d8f7bec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bfa3b81639131d57750b85d52dd7594cb9b728f68bb8d9b00489d2b5666fc8c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10125d092830cc51e63be2f688489852c049c71ce1c40e5e830493119278dc59(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1db57ef2147d2cb5eaeeb0fbf4ef7d0b7b13f8b555cbd3a71f0ea4e9f54c6f40(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9868424ab3a101126ea5f5815fd1a14cd16076fda9a5bbf8682caad04b1786d0(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__924768bc397860253da7a04bdebf669857de59b8e0d84cc1b83ee91b0089eba4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf0a3bc5f6ff8ab08cf01dce65bc1fcb8826a7275d51d37a73b5b9fb9422fb7a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d16ba2e2f3eafc8dc7f41705342f853b8ec4f35960bd1f44408ac7bbe839038a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34b8ef9ebf4a75397424c610d0a81a61655c87962dd085c03f8e3e43a05297c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc7af643b39cec19df23ff09892d4b3cbe2c4070c143e967facfde9743ba7cc6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff326ee8545cf081bd5310ec39f6cc0de39f42ce591ecb2f8f55112309620cd7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a39a11702f8a0021705b2508f5bcabdf617f39d9180807cbbb5819b218e467ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a88a77dba9609bf391147a8f7d36239744b34bcef8779f5eb80bb24e9646150a(
    *,
    formula: builtins.str,
    evaluation_interval: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a75bf5b54a2f75bde0c327c561c375cb08ab350e16597b0b60c52520f9ded7c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b1da7e5fb69f5b0d3a73a9b820014cad2af5a5c721627bac15938e55a99f0d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__737723f7650006e4ddbd74905ea4920296b7c52ba438928fe1c2ff32f14d17fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3672b65d2e33f51455dd4b6b04137ed2e79468313b6d63d2e9b436f2b8279e75(
    value: typing.Optional[BatchPoolAutoScale],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acce31f232bbe463e5730ff09b7fa9661c53f341c9dc58e4c2ed86c17de9c150(
    *,
    id: builtins.str,
    store_location: builtins.str,
    store_name: typing.Optional[builtins.str] = None,
    visibility: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa1551cfd5f7d08ea4a40a19a1801021453b7a5c0dede3b2337d4b7ca92fa7ac(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cd774089f1f36a65f974575367ac37286456239dac0b30be8cb4bbe2b90ce8c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__422bffcb9c8a9f327ecc83e0b8f8f988e6bbeadf76f1896409053ce7c4bd8bf1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91e7a6eb861b9cec8e530fccaabf312de8fb4c5dbb4ce08590c3dc0136573c18(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d34412073206174bf843a2e548e7946850c32449a805b59ee2ccc34597d86cf5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d99091b0bf6daae35457e7d1669ccfd9576f2d5cee8972029b83038e65e60b3c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolCertificate]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__796e152f5a6ed1d15dd95da8dbdd11c80d4b57e2937d1f6256881a6501e2eba6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49a8d9a5a066f103c5646ae73a72e9357e35aeece0277742e448d505895f074f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__174fa15082175525c08779199f3045e5c476b50417bfa3b8535f0f0654cafab5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09bdf9aabc67db626d34d514b9262015b6f1a3957b7ae75112cb05cf75a851b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d1a70945a2d4fc7aedd04d1e9af3dee01bb4c8e8508b43653a95cbcab481794(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d985228b0ba3508b14ec3eedbd8ac8dbf3effef9816b23bdd1226828846b675(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolCertificate]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f6eb9c097beed2d19e62c0ae46eba1beb78d7fe028abc742f58c606279012da(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    account_name: builtins.str,
    name: builtins.str,
    node_agent_sku_id: builtins.str,
    resource_group_name: builtins.str,
    storage_image_reference: typing.Union[BatchPoolStorageImageReference, typing.Dict[builtins.str, typing.Any]],
    vm_size: builtins.str,
    auto_scale: typing.Optional[typing.Union[BatchPoolAutoScale, typing.Dict[builtins.str, typing.Any]]] = None,
    certificate: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BatchPoolCertificate, typing.Dict[builtins.str, typing.Any]]]]] = None,
    container_configuration: typing.Optional[typing.Union[BatchPoolContainerConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    data_disks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BatchPoolDataDisks, typing.Dict[builtins.str, typing.Any]]]]] = None,
    disk_encryption: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BatchPoolDiskEncryption, typing.Dict[builtins.str, typing.Any]]]]] = None,
    display_name: typing.Optional[builtins.str] = None,
    extensions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BatchPoolExtensions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    fixed_scale: typing.Optional[typing.Union[BatchPoolFixedScale, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    identity: typing.Optional[typing.Union[BatchPoolIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    inter_node_communication: typing.Optional[builtins.str] = None,
    license_type: typing.Optional[builtins.str] = None,
    max_tasks_per_node: typing.Optional[jsii.Number] = None,
    metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    mount: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BatchPoolMount, typing.Dict[builtins.str, typing.Any]]]]] = None,
    network_configuration: typing.Optional[typing.Union[BatchPoolNetworkConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    node_placement: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BatchPoolNodePlacement, typing.Dict[builtins.str, typing.Any]]]]] = None,
    os_disk_placement: typing.Optional[builtins.str] = None,
    security_profile: typing.Optional[typing.Union[BatchPoolSecurityProfile, typing.Dict[builtins.str, typing.Any]]] = None,
    start_task: typing.Optional[typing.Union[BatchPoolStartTask, typing.Dict[builtins.str, typing.Any]]] = None,
    stop_pending_resize_operation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    target_node_communication_mode: typing.Optional[builtins.str] = None,
    task_scheduling_policy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BatchPoolTaskSchedulingPolicy, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[BatchPoolTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    user_accounts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BatchPoolUserAccounts, typing.Dict[builtins.str, typing.Any]]]]] = None,
    windows: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BatchPoolWindows, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfada098c0f84c3f146a22230c13f394388c997516e4070450d808dddedc99f2(
    *,
    container_image_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    container_registries: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BatchPoolContainerConfigurationContainerRegistries, typing.Dict[builtins.str, typing.Any]]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45a17df620eadcf077b70b088960155eb277265051c238d66c680886f69b557f(
    *,
    password: typing.Optional[builtins.str] = None,
    registry_server: typing.Optional[builtins.str] = None,
    user_assigned_identity_id: typing.Optional[builtins.str] = None,
    user_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7056807b99fefd1c66d83f24c811bde7c3c0c745289b3bf98664b3af8640ae7c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37404873f927c1e932ddee4426d83e57b74d1f6260597b59581215293cc5d0ad(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__345815373dea00e2cf45d116c8df536b7405ea79b8c7bce8360d59ba14d291b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55179a0b174db52b8bf0ea4abb39b312e9982b90e24691d641cc8824ade23a37(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e35a65583ed202f06a9c4eb353e406924559bb90462ff503dce1f9d1d85ee2e3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c3f98c0c751a450a01b0beeb12669ab567a572351334cbb71570853b3ecc9ad(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolContainerConfigurationContainerRegistries]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__586f8288df8d36df2731c8d6f23c4820fe919eda6697b9a160b90f36349a9d6f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25eb9f974350ff0ba1fae170da49d3ec85591778cca7900ce570bdaf915de27f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f469e4ab0f783f71cef77c35814e0c8388042e0259f596588b1a140dbab5da9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9994e326908bf527065fac65a09d767f1bc96b7c748f97875307d5823535f9fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcc41525a9a46077072c94114f3aafcf62a42a67d88b97880cb1bcf70fd9f065(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f862b7a1e3083468d99891bc83e4d06b1d38272c0ced347d844ce3065cb4960d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolContainerConfigurationContainerRegistries]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89c9f8233c46523369e9da7ecc546238fc1ab7f54bfa014bee2502388dc4fdda(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a24759a85fe059eb1441a0c40bd502b7ddb3ecc14acb8a4ea7826ef853ca785(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BatchPoolContainerConfigurationContainerRegistries, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c613da81fae3db2118b6098529cec815f5cf630ac050e3f99663ed6b8b9a7adc(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5c33e09bb8120fedd5141fe00739abaa3e614d4cf8219b87c8ef0ef416f6594(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14db885f377d903c266d50d1ff8198805b1c8604febe716e3f656e540736fa61(
    value: typing.Optional[BatchPoolContainerConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35aca359df5cb87bfef12127a82cd948c2c6aa352102a9c98bc445bead07bf11(
    *,
    disk_size_gb: jsii.Number,
    lun: jsii.Number,
    caching: typing.Optional[builtins.str] = None,
    storage_account_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d477f5a0fed8996272406d4e7ba37d57572b6f160dcddb5b12bf38345f49011(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77bb319c3049dcb656a8aaf9886bce538877a68d12acecf086e76466ad134099(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94f6c5951bac3265141ba6826f60100a486362d3fc2b07250424b24e6381fa1a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c2e2826cf5a9b348d0de5163eec6ccf01bfe8bf6da1f1f2aab328100ba547dd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6386d3074c11659eef88e11cb8d8e92e6c4de9037ec11240d931d3b8526de2f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dccd20a019851228c21d6809c551e5fe8e024e5f5092c227f107339a5c3d9a4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolDataDisks]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4433915d35a04f4f773e6309b6002bd7636176ff9bdce26c6a376bc60df59cc4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04bf5efb79ce6c8f198082129939e9d7bc90882c12747593130a315928e70771(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1d530976bc3813a3224706dabe884c7fc5f8a2b3f1e396a52ad4c7e47b98e09(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f27c785bdb3c2c19f9129fe4e2551e59b5b8f030c853cfafef61be45a19cb877(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc8fcc38d424fbfebc45310ac5f0cc47a655d69eff6f94b31ad45fa2f7d7d937(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef27b8686d23134c66b24f0e53ba87f1a8005ede087e285ef6c30541ea728941(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolDataDisks]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__287173c4afaa43ef6d4f32e1a7f1fed8325099141c8b2df151cc7d07c86285f4(
    *,
    disk_encryption_target: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f1d4c8da693cb8917fdb4dd659899885377925ec2d0d4f15d28453e36a66b23(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74637b1612e23460e2c90aef1837757c070940fe3400315d3f7a63a94bf6e37c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a74d2c9510b9bb771c04c712e854aed49d5d8da8c6444fc3ff581698ef30c45(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92e6b50ad65ac11685b1db0877fcbdb8cf1a1a51f631b33be92a84d55b463753(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93ea1f98a2bfe5cfecd7e8573d9ea232cbfb352b110905cffa5e990a69a06ee2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d97e26a696eea2299a1e4cf10b25544f99def4e2c121b18fbf56f63793c4b9b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolDiskEncryption]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96cc27ffa34e3e8c1b292b1a5f2b0d7a4ccf48846ad45c9fdb0fdc1a5ed86652(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ca4c68f432cdac162675cb186a9fe555b9dc8e23a8bddf109ca90a642b92e7c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ac4701eddf1fca7504fb61621753fbfa98db7e92c3973716c737f30a816f6d4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolDiskEncryption]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c418dbe46a4a9fdd67f33efc6fd4cb25b42aa13650298acdbe4e9772dbfe4015(
    *,
    name: builtins.str,
    publisher: builtins.str,
    type: builtins.str,
    automatic_upgrade_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    auto_upgrade_minor_version: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    protected_settings: typing.Optional[builtins.str] = None,
    provision_after_extensions: typing.Optional[typing.Sequence[builtins.str]] = None,
    settings_json: typing.Optional[builtins.str] = None,
    type_handler_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df3ae2bc448a540e888d670c20a8e223d1e5aef8ada6fd845db3a4115d07b827(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8d28c14a718f272f58c3edb5e8e76abd6320850894798b5c37a14b8b8e79c7f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e859d2ebd92118ba47d2d88655c7e7ea32b8eeb1e14b7f9e760d5fdb51dbf78(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db938ab15df83a5da06f70145ca1a812c5e3b5a802902327fb73ee05792a3c50(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdac3372c73cb74e2dc31b830731fbec466ab09fcfb282d827ffbd74b2d77d6b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0523fa0febbff3c1ab0c0594205739667dff8c10352153e6286aed25bf85e24b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolExtensions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e130816bf36e099fee1e0a2555d022fe7adc7400d3d9befd30eae3d826c60bf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb31fd58ea19fc171a413a00ce3e3083beb77ecebc3c2a8f705d4f69213c89ff(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__431f4c52df85a648997f116230e7c3aa0a5be53bca6673d6b0f61df25aaabe2e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1e2dce5f1cf5b7bf204be5b4de0766a40a4dedac349d389b634b7a99d8ce496(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d359fde8efb95262bc7469241e0e40f6057e5ab2ae9829ee3f97f906ae5871b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b086271ff164287791b5873e2a698770035cffc55076c60fa15528a5d21de5b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0e18fd3404bcf8bc483870d008eb47e9670566cc3193f4e646c80c7c84aab20(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e2cee0fefb109207c5600e8c3be441d18af64e686038565c7c75d5cd4c599b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ddc4cedbfeafa5b962796f05cc4f428b1a14b6f84b8b0d314bd693ec03207f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38fd4838082223a6b8e7948324b33b278e4639fca4b445450dc8232e81dc220f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__066f3261a784317d743fab24784e1f1217f0703bad7ee3f4854689ef2071dd6b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolExtensions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d9dd60afd90ab16965ec3002969a958196d8b83e355bbfdaa4fcc0f3c4cac57(
    *,
    node_deallocation_method: typing.Optional[builtins.str] = None,
    resize_timeout: typing.Optional[builtins.str] = None,
    target_dedicated_nodes: typing.Optional[jsii.Number] = None,
    target_low_priority_nodes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a370d007823cc895849380309db255ccf49b35aaceb01b8c52c574db4468fa4e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a23b0104657e0a420dcf1f1736c49e0703a0a9db53f2d6520b8e92c7de5f28e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9161840ab5598e5a95e5b482514abf2e6a6cbe03b320097ad00a7dd16c59f571(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51bd40320a74c9e991395bbc1b70a66e011ac7ee6e936e46e43d8e568793d16c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f985ac344abe3aec2f9400ce47c9af01f50359597bba70d68ff9bca5ba2cfee(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e201f86b3e65801e0e71602c8dda2a8a36465c72c0f4b9d08ad6581a35b5e71(
    value: typing.Optional[BatchPoolFixedScale],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52492b24aec6855f9a7361602a0ce22220aab152985054f52e8a8ca1e3d8c157(
    *,
    identity_ids: typing.Sequence[builtins.str],
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33c1a3afb52bcc0eb7d3e9dc26448ea5dc6c1215e1bf0eefb47192602bab498e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__991f6742cb70f264e2251e88b181679e778cc2d8a6db9c0adb26ce44374b485b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2ec1fdea69b08dc0c52392a5b187c8685e6efac8fff4d78589d0a86b4e7390d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89fa856916b0e18fda0f2665cb22c497f45bb5e319b235bb95c7ef52de7e8976(
    value: typing.Optional[BatchPoolIdentity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfc35f2df5b0c8f66bfd8110cc3c403b31c17ce00ecded4b56106f64e4cb1ca9(
    *,
    azure_blob_file_system: typing.Optional[typing.Union[BatchPoolMountAzureBlobFileSystem, typing.Dict[builtins.str, typing.Any]]] = None,
    azure_file_share: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BatchPoolMountAzureFileShare, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cifs_mount: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BatchPoolMountCifsMount, typing.Dict[builtins.str, typing.Any]]]]] = None,
    nfs_mount: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BatchPoolMountNfsMount, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6defbd93299ac018afd24f97a882bfee9ac4622066462cd36eb65788d0026f2d(
    *,
    account_name: builtins.str,
    container_name: builtins.str,
    relative_mount_path: builtins.str,
    account_key: typing.Optional[builtins.str] = None,
    blobfuse_options: typing.Optional[builtins.str] = None,
    identity_id: typing.Optional[builtins.str] = None,
    sas_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f51b125d927148c305a581f9a78e734d2140aba797e006d6f91ee62beb473c8e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c0dcbbbf3d79094f450609a3493804039233e7c98f8d23aa3738eddf299113e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bab89d2f72eacb24e4cfb1a0f10683957c63ca457274601cf0052c83c7f599d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__298173f68ccc1310f1a6a4fab0331e76f11723d8af4e74d88960e921c3a09968(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e63b45c1776736a84753d0c2be054702e6e3de251a2ea75643c504e21d84701f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e047619cb0d285c797cb6a92a83b8d45a3b1dfbcd6a942bad3865c756eabd6f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f833bbbdc7a033edfcabf39927d2ee8e8492af053c813e084c31e239bab38d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1e8f39d142fbd12cb5476ce7385cdbfef0f9aacd1731fa3fb226ef866e9dafd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21a78a3c6ce1f4c3a4de3aa8d5fb271df4c31334b22433c43dce3cd45c6c2c7e(
    value: typing.Optional[BatchPoolMountAzureBlobFileSystem],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34b8b4b25eb68021071bd9421f90215b9f716dbd2f16174d9501e8cea7ff506e(
    *,
    account_key: builtins.str,
    account_name: builtins.str,
    azure_file_url: builtins.str,
    relative_mount_path: builtins.str,
    mount_options: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__face89eaadb219af38ba71813b47c8b2f42befeea28633e511e8eaa6e54f15cb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__696213558190bd8cffb9956f7c9319f2349a24ff96134b787dbdd2f7253951bf(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a80cf37645c71ee5cae45d6029332d6aab48a949e5313a84350faa1ed64f95ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d60ca19bf4bf5d19201e8ce9b2c1e4030af4de54e9fc55e50d026f8265bbcfed(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55273d681036b9d170d4ed228e268eab0e040f52252b4f89ffca32239ab320ee(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3473c66625e6e921feb5e05f572eb56893b195a11f5b162b7e96e2c80f4bc6aa(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolMountAzureFileShare]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d24d0efc7e77a7597e4457527db61a3b4d4fb3bfd796a2ceec3c8def703ec66(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__770cc9f569c278fb2cbef8e6b6e05a2e5663c14a4ff56e3c6a4896379c8f9dda(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75d52b4d0820bbc88eb88fedf4f146d766a8770eaf4336c6f68992bef73d5824(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49af354a2ee970b8cac814d7cac97341606b4eb247ca8a2f1a0fbd19efa66fc1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e26baac0772b21a34b7b8092ebcb27c5830bcbcfe641f26b4a56a843a98379bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d9f7ee2ca6e3eb2c1f389131139e5ea8548813aca5ebc3b5740be2f06288023(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d736db030aba5cbeeb304d0ef6b31e3c1f88b6ae3f0b977d8ba5b39e7f10e2a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolMountAzureFileShare]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bfc420329c793eaac34d21a4b43dabb0fa15a5d0c629be0d7b77c09aec49f70(
    *,
    password: builtins.str,
    relative_mount_path: builtins.str,
    source: builtins.str,
    user_name: builtins.str,
    mount_options: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffbe8d90917bb15aace439e21f2fa9255c73cc818d42e0b585659a3084cad9ed(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac00b1fd4d6022e66a02fbb7ab256fb6795985fbcd310e13c15210aef6196ad9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84e44cceee9d71ee90bf168e8e69827bb5d6e00d14b1e8e96adf98d6937ddef4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9da16ffc38a497eac85d3dc5a028a1397e1dad292964151a02577a153875dfa(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0bdbd6ea920be14bd646682fa05057409d403c077e45f5c243e891480c5be2b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e0b06456f87328d8d61b5bb52e16819b81ae25788fbd16d9a521fd86947ea27(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolMountCifsMount]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20eb0bf84d2f694d3bb71e5764016b58e14e298cc309571cff656fa70438035d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aedc03eab0908066ddb1e90dbe295309734093c611c1acf932e16a5d7f38b119(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__846673ba4fe2d189489e4a7db3bd7f1fd13da1307ae184c4342d95493acc2abb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25d1d7a697b2cf22380110b2b48bcda732129553c3604248b84fc00aad2cc591(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__951eea3fb3e63a6dc52a4885a54f76cd2d235db6d6dfe1102f4d77a5f9255f9a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5422baaacb5c94a63daf44ff40c24d7620c54344950e473d81b9ac75b8cec831(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc74faa003a7e3da6068aca0b2540782b4d4d43eb44665e4ae67d4005e1f0a2b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolMountCifsMount]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcd2a92aa6a6ffbebc2b70ba5dd0579c0952b2eed6534b496535c717825144e8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fb61a357f217140aa89c381b36ea8e2da2414c493ddcdbfa8c7a8dfd722bc72(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaf86f739fd3691b6efa5b12223884bbabec4dfb8333957e9e423f0a7243548d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8753c0131b67a8488d4b79dd9be5212a83b0d91cf40f3baab93ed00800045ac(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d88fda04eff58a8be84e1d3c56ec46944ac4cf9f62b63138e8f1d0eaebd12f4c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__583fb9071573e27e3ada827fca701866c1ccd59ccfaf5e8c7041b16d1339954f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolMount]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4c113fe3db939dbb452e49c99a36fc1cbb8e06f805a640a2f05ecc1c6797600(
    *,
    relative_mount_path: builtins.str,
    source: builtins.str,
    mount_options: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c98a525929281d1680a2178bc858991a5a667c432ca77a98cb36efc1209d13b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70e3d61b8352a2682310481c08d3dd9d52e9a248a55fc2a585419e90fd40b459(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0c09311f4c73d3a0e6a74b7191b8ba26aa23420129b75b14256b998cc1a2301(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48b94e0bf260dde37d3b6fea58889849e1a2804db4627aae8b8857ebc8c0c5ad(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a708651f4ac53e8703cd708b7df03b4d3e786f32e087f181b1cf79c61e595294(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c4975008f50c9f8faa521792da56b69c8d8ea21bd7ac481b2e0c20ceb8113b8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolMountNfsMount]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25fbbb97f71441951aa4065cbea92240ba922bae32e9e611117ae0e9d66f98c9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a446bf643467acc06ff22703cf079da6daf229ea5829223262332e33b89ab53c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a19b0b2002e0b9946ce7a5583bc2644f585efb1d42a527b3bba129c2baca4663(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__786cbb8526c54eddf88cbdc6ed2184816623174c29dcd02318dfa4699f06cd9d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc4450cc9a21521833697bb227fb8413c69940841762d2948e78e781408fb4ce(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolMountNfsMount]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c91441bebed41841df65e63fbb0ba30f9a5fe05ff3ef4bd38d30eef8cc2b4e6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaf595d6284a4806e2ad05c07a69dd050aa5594ffa83aafa884aff4b6e1902d2(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BatchPoolMountAzureFileShare, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11fecd0e11453120fab5ba783e51e1ebbc61a8d4b75e6ace47340caf52997dc9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BatchPoolMountCifsMount, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed73b1e0caa97d5662969ea5900b53d0b7108410f4600d9105e79b7b4ae26eab(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BatchPoolMountNfsMount, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba351f651a4d8863cf389fceb50e733a79197fa830bfcc1814b998b67ba70680(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolMount]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fba4c9d1f73ee9fd126825aa354f51dc979cb6ecad5bad2eb9c76b7bb95f215(
    *,
    accelerated_networking_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    dynamic_vnet_assignment_scope: typing.Optional[builtins.str] = None,
    endpoint_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BatchPoolNetworkConfigurationEndpointConfiguration, typing.Dict[builtins.str, typing.Any]]]]] = None,
    public_address_provisioning_type: typing.Optional[builtins.str] = None,
    public_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cce14c684ec688cd0009a01d88340e2d26e95cba27cb5c1228d2f0695f840db2(
    *,
    backend_port: jsii.Number,
    frontend_port_range: builtins.str,
    name: builtins.str,
    protocol: builtins.str,
    network_security_group_rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BatchPoolNetworkConfigurationEndpointConfigurationNetworkSecurityGroupRules, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09d62094a096d0c49dca568752782504d3744fc6927e5c7ef1e97297c9c44c4f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ede91b66cfb2dbbb3c7370fbfe4323fd069080a1aba2cca22d148b57d44c3779(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d847cb2a7acb8d3247e8945d1cf59a31b271415bc4b34467cb1478da4e6f881(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e148e01eb097ffac89d51325a98f2ffbd3ed4f3f1c5265e1c1b563a1bb057912(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bce848aa29b6a52f8f6f75e609f304301e5130e102406f04710a2498a9d9a42c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cffa89b7625b14643d94eb96eafd9a66843f76a343af8539db5fb7cc45e27925(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolNetworkConfigurationEndpointConfiguration]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bba713c87ffdc3fa6651d883c366ffa8e198170ccbd95268d1527f929d9f9064(
    *,
    access: builtins.str,
    priority: jsii.Number,
    source_address_prefix: builtins.str,
    source_port_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__489fb3faf7b33671e5726d3574d7f1933a06cabf3614c0bc91c793769f7a45ac(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__675f1297dff23feea5bc9a3f7f83de75e8b5230168e779f0e37ed19ab5efceb8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b07b69b522ae1bcfccd704ca6f418dc82805a66e7eab2bd48e58efd21ca947ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc8e58320648418549b06c53477cec81600468b0343c99132b7e1073b7951ab2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__241eb0351d991f87d87ee211d4d951a3d4a45d523a3ce50477f88ee60f34aa7e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92c6523a9bf63f0855b3f3409f3a813499231f6d0cd69f0dc2d546e1bd7a1a31(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolNetworkConfigurationEndpointConfigurationNetworkSecurityGroupRules]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad9e640beaf3916dc9b7195bed260511d8e5afcd4eb5218a1ab2909080fbff3e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bab27293c5127e026bf0ae7b0a2434aac79ab9c2656c36279b3b8790717a300(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01414ed157d36c554ef19c5d84ad1bdc0976d1363dbc37fd53f39e0d0535c509(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d67fdab7902e32893cd7b93e465bf3a321f0a3ca7358f678e8e62ab86bca8c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d663932364fe157f1c1fb1d5a678133c2ad7d665abdeb9a162cf514f6faa822a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a49c8bd5d4b3b79af9a142ae8480e35f5b26e9ceab1f509c19a5b0b156ea1ca3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolNetworkConfigurationEndpointConfigurationNetworkSecurityGroupRules]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4893826a5e0c6266a59f62f9562e45a74d4bf409db1163b2c03551942de309d5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69a2ce91da4d296582e852dc6f15befdf49332ab61e8cf711c01eb499f5b7a3a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BatchPoolNetworkConfigurationEndpointConfigurationNetworkSecurityGroupRules, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2de0e74051892d9d7ff25b0ac345fd112203e4b573726708fdd3fe854d3dbf84(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__203e1cc1627e9d65e8d682266066cf67f1ca10870da117dbfc0f98d2b379947b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95a1b3d8cadc9f8eb1970764f532d34995b00251a8c866b0d106267d2e2897af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d75e4668ccbf1410066c2c57f76faa99ce667bfc2c20f1ffe3ac958fb8977f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26d2124e4ebdd90db69344e41d0c7d6c47c272fa9d64ea24240bc9b6740776d2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolNetworkConfigurationEndpointConfiguration]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68815728f08f37c5b02182bd1b9e6bae8650dcd05772a754ba51cbf4294c1242(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de07dbe5b2eff466170f14b0a8419ede1a5bb4a6fdae630364fb295e9373baa6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BatchPoolNetworkConfigurationEndpointConfiguration, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dad4ce9369c594a972a1e2b6e98150a97578f41fe12aa2552caee3061e14c545(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d7d2f924a1a2dc601a72722d4e4dce6b2ac4c26bc9fb8d6efbc26a895f7ab5c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49758f71ec2e0216c3bcb0e27176df26d2fe653f7cd2cb247216724f867db76f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73f359b290e7eba6567f70ef3e134ef43bb1b44d4b11816cf881de377bdeaee8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3eb06bff9fd78997e4744600222528755a705f5c7c5e5c1ec9932a6087148d0c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__515151df7f265c796e4e108d4593df87f5b665f979132f6608b6292b9fe7b33e(
    value: typing.Optional[BatchPoolNetworkConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06f081fa4b4c69915be5fe9a1e78f23e0b7a8999aac1f212a158ee2e32e7c36e(
    *,
    policy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e788307fe9ecad0106ffb1b182c73b7483145f0712826fda10a5f2cc63a9193(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d26feb2b7102e7c5f709fe5ba7a81d4c8a3e52fc5ce199f6b69ce12b95a74a40(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e2901102b2f2988913c8d51c210fca3f92fcfb4b01f83665f3809daca532e8a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0980387d9a1a7834d783fdb5ec2d3a947ef2a652fe730a4927cd1d253ea2d41(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1fc4d6ae9e65ee1be416d46555e61fda07275ca0ef68f44c63b5b9262110230(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57540ce4bcc3a9515388fd742078bba7c036cdb87d4a05395d9d5c4233a7c612(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolNodePlacement]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a90277e23d1893f38b172b2071c4a425cbfae380a0c849347b76af2f7faa1fa3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f2cb428bb2932e564f07bd8e7263c4f64faf176e2c6221e34be749650840f60(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fddf2932ee765a489815b3c6a52800a7e1f582c9e2c6dbeef98141101543e93f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolNodePlacement]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b35e9d65bf04df18c26154dde97bf4c6613b73ba25288ea28fa684ca6cdd62a(
    *,
    host_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    secure_boot_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    security_type: typing.Optional[builtins.str] = None,
    vtpm_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47ab1ac21fb50644a3ada765f4e3624183270b59f5625f7893d3355e45daeb5a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9aa2340162a9ab76f4a4122776017a4b0249580223f577eaca9d868f4628ee33(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fa7f5616e0f9c0e7cd39d44c604cb36bbf1d63b7f389ef2029e58d8a6e668e7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__229cd7c425f8c09e41758f7a593888e69ce62e4c388070947e54c0a9701b45b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac7a9540e9e9666bf918b1ddd0de2e7e58b3b1101a031945e8ba91fb6feba4a5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f2559b40d2b794935b5ec2f95a3bf00cd5d190e2ad3113df80156700f0f2e01(
    value: typing.Optional[BatchPoolSecurityProfile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b129410fb7c7457dea1af0197cf0fb7afa606adb52b25ed05c46d83c06c7ab0(
    *,
    command_line: builtins.str,
    user_identity: typing.Union[BatchPoolStartTaskUserIdentity, typing.Dict[builtins.str, typing.Any]],
    common_environment_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    container: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BatchPoolStartTaskContainer, typing.Dict[builtins.str, typing.Any]]]]] = None,
    resource_file: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BatchPoolStartTaskResourceFile, typing.Dict[builtins.str, typing.Any]]]]] = None,
    task_retry_maximum: typing.Optional[jsii.Number] = None,
    wait_for_success: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a36110245679d9ded5f4dcc61d437534a4626bb854e9714aff157db611fb8dd(
    *,
    image_name: builtins.str,
    registry: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BatchPoolStartTaskContainerRegistry, typing.Dict[builtins.str, typing.Any]]]]] = None,
    run_options: typing.Optional[builtins.str] = None,
    working_directory: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c743c3b102693d203eacb625000e0df00a5ee3e61682afe97e72c6eebec89ca7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42a0954b1d728a180caa4ddfa2f1e48016cb0fdfadc02a549127c39bf0ef54ec(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fce61ae77d4588136042e63c08a84f1cc3ab45d69e1f6a6f9e2ff280e4ed6f5c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fc71a8f5e2c51b6d1d514446471051cc194f706a1fa740b7fbb0c21d53ff736(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee3603ea087f1184896538d782207cb4d80db1e8a5d938ac26ebb9cd545c2bae(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa16aa2dbd859a1af91778ed11cce182a251aee9654d623603803a6bb472c081(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolStartTaskContainer]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edf307466a1386e5695f34cc59e1f9bf6cddccb246fb8ce49607872277b54a35(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa1b4b6373482ae1efe0fffe5f659ccf8b08b5fe44ac45778de8a56e6d130e2e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BatchPoolStartTaskContainerRegistry, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0511ed092cdf169918a0ec1940b90455f8bed3050dcdf4d1a9ec82df920c337(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd889da71ba18a4663bdce11a72fa6c9c2041ed305f4ec48fccdc44f21e36691(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__996fcefdaa6973faee3cbf833c5525a4e957427e4e5ca2568c505bf9607d5082(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d5f7ae15045344fc613a1858452b3c8826b9c06fc8b84d1345825bd88a66a33(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolStartTaskContainer]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8544707ba727677a0848727d979c591c9dbb431b773599955b26c91ae8269983(
    *,
    registry_server: builtins.str,
    password: typing.Optional[builtins.str] = None,
    user_assigned_identity_id: typing.Optional[builtins.str] = None,
    user_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34c3ce504253a78b4004cf8b97b16d5dbff673ed08ffa06385c55587720dabbd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38f1de0259cb84cd737f939c5c862c3943de34e93eac985ccedc1e08558e8ad7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00794d05c1fcc1b9f0afeba08a0e7603c08c84a44a6b53a8a0d9ba65bc43b8af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__422f1c8f74528f36896fc4a7e92a2077a626cf82a99af0ddd8b3fd85c23d8ac7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81de57fc322ed44fd89a9d56d83ac57f4db8eb10982b842f68a19f9b0a942f86(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2326caee1ca8eede156eb491c00fa3dd1e51b90731bb124a2663fd147b6aff56(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolStartTaskContainerRegistry]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2104a3de8a07e898ad80eb412140bc90411505751cf114741c5f5d5a1cf464f3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__000b20f1b2f16024e570096806df4c4e0b8118a0e16e7c5ada363dcdaa8ac8c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ec192032be37670a76cde9b6d9b330e6cc00d03325c4f0f99e63f9043b8b445(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e935134b75fe5f6776accb5542a8615574a2aa0e173ffd2575e90ab9024f7b5d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca2d22b15fe1692aa7c7107e36b342d64ee0f3bb1abe2ca7c22ab0edbd143cb4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eeae20723d01f6b496b5f3b5289d1f3816ce7bc6d0137a7d275b693c680c5b57(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolStartTaskContainerRegistry]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77e64a98e808f4b70b05e052de9e255808e09d44c50c0549f64c63512cc0eac0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe84622db29542bfe280235aa00036180c4291ea2ae002b8566b52098709210a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BatchPoolStartTaskContainer, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b95a912a30741a98e6f031c47f6975d91165690f739ff6d0d6ee52d7118ab2ca(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BatchPoolStartTaskResourceFile, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acfbb1cb7a44aaa13e5bebbaa084dc0af8d98ee4da3f320c4b3c5f61c74c131c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f9100e0ec59a8cb28a939089edc65ab08c9d1337ab4da04579d847a2c0751ad(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64d499a447c49de0da1ea5f5977d81831b283ceb90cfed339a0b26bfb6bece9a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbe1958a67464281b085803005956abbaa466e9968fccf9fa5c0fd7f060a5967(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aed837a001a1290e9012ca51b7b4f779ea5e9cd8a1f9f7f0b29c125d2dd0e08c(
    value: typing.Optional[BatchPoolStartTask],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d9019af978675b13bbff60442f764a3411bba3aa9c453278cfbba2f871e6532(
    *,
    auto_storage_container_name: typing.Optional[builtins.str] = None,
    blob_prefix: typing.Optional[builtins.str] = None,
    file_mode: typing.Optional[builtins.str] = None,
    file_path: typing.Optional[builtins.str] = None,
    http_url: typing.Optional[builtins.str] = None,
    storage_container_url: typing.Optional[builtins.str] = None,
    user_assigned_identity_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72cc9831fdb48b606cf605a1667daa96381ee430c7e5d9824afa640c2b4a0e15(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e56206ee18ee417ca51b303dda55355b0b8db7d0a6fde2c9fc9905b3578a202(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5670249586a037eb375147fa1d07483028d067bcadbf23bcfb80693d6cc09420(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02ac937e62625c78cfcd87e0cb7be58da34bd4f99c1ce4a6ed324782ba784c03(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35cfb786d7384152af37c6e826d83feffafba0c279317447047b4a209028f84d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3467f00ee9b720ff54984ae9d61e83f3b4dd4804f6f712037b169c3a296896ca(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolStartTaskResourceFile]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dabb265f57709dde0e44ee64489286bfee594886fde8f420668559c552d0e0d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43eb7c69a5f04b492fae1a77519da80162f85489531cb5749e6ecb5d0ad79e37(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40806f800e16303c199c1db1c62b6505acd05edef2369aa31865755205a5b2ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10040c6afffd83980210dafaf1e4db9c2c44a53f7fab2496250520d4cdabe150(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbdbc8f60e93d7f4b7cbd264e7ebe57f93b37bf13be07157b2e2790adfe2dd90(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8afd906add560325e6bdded2bc6120d345a1f62a4cb136a99d4fb4bdaa801028(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d790a0b944ef490f911de93fe2b001074f7631cffbe609d73a863a6bca01101(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d085c271dfae1170866a95de5788c27ca5aaa50289ddc22192f95ad4ff2a72d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2575d089e18241f4e7475dcf1913e39dd8eefaaf19c35cd8b586bc782add2287(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolStartTaskResourceFile]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf4069ac861c4598020e75a7c3ee3385621f870fd970e2d931b6bbdafce069ed(
    *,
    auto_user: typing.Optional[typing.Union[BatchPoolStartTaskUserIdentityAutoUser, typing.Dict[builtins.str, typing.Any]]] = None,
    user_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec3aed7d18e610e6b4d8f2326355e7a315a318454b73abad04335a23c6e62ece(
    *,
    elevation_level: typing.Optional[builtins.str] = None,
    scope: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d44c2d97bf05cbf5b12d58b9b4579766d3ceaee029ac6694352b0f7a46506107(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e0db8a5627a47c43b9f34c1b57fa08a33f573dc43b47cb67df7d0a0c973995f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a4072532adbe353bac7696b11ae22799f8f30681b5e1d8c55c81923d8a0f14a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c1e34d44b3ac0b73b8abaa73059c20c68109010090032edff917cb012cac566(
    value: typing.Optional[BatchPoolStartTaskUserIdentityAutoUser],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f8f3aacbdb8602eab17a27b85b1ab02934661c9486c48b08d540a69be33a326(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bce9880edbe48baf5e6a23f10f890f344071994cc3d768ee2d7591b79fcc73fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51bd6b4632b17e91479366f2c9ac518163b2899191f39519935a5fb341783fa2(
    value: typing.Optional[BatchPoolStartTaskUserIdentity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60f2c35f6304e501c3a5241c1c0b08ffc5818faf02741d7dfd3102c430dcdefe(
    *,
    id: typing.Optional[builtins.str] = None,
    offer: typing.Optional[builtins.str] = None,
    publisher: typing.Optional[builtins.str] = None,
    sku: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3380b0cc976d85e34e8234b1f405393d40289062e4ea6ac7c14f14da747594a4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4073de4d2e90095b73b7ab6d0029556d6a745a0f190b700ea93bb769f206c6f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f6364a8a50cf51da162d4cda1de42ad47f9e0dc537a7405c3ac45e687c5f1d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4dc17d9b0cbc7ff3d9b0e790e7792e8ee8d7bae6355b5a1856cdd6bdf0b47cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bf69c346e807f30b50ca9a1f9fdefa790fdacaf5ea76ced47121f47d541f867(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd118538bc8f859af39e3a48e3be69d609f5a634064e4919d21ecc050a99cffb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__650088b5ff2a810a0be860efd9f91f36b39747321b85640a1949391482391626(
    value: typing.Optional[BatchPoolStorageImageReference],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__945763c0abd732e533a885948a7a36f875b2fbcac20c7e812dcc4a68401fde83(
    *,
    node_fill_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76d8448e746fc6f5434af5bf3d2282cf6c2e7801b0547372c58c44047da67910(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba594b437e18e2edafb8b918de6a7f37f6a3797f9688f2dd73ddf36176ebb224(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__340d603934ce8c0aa316bc6e9348c19972d8296d34ca29d6737f4583411148ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6d205b26e903c1ee3a8aa67aceac99eefa2f6eee2c2455d8061b1947ae9a5c5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac2665ddd64f02122a578c43bd275708888f6ad42c513e13b5a13f1a273600aa(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a5e54aaa212557d17558eb42f38c4491cded0692208aa08131ed99681f0f8ea(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolTaskSchedulingPolicy]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a0098463b1870df17473da7d12a0dfc0c5f7fc2f0985753e9497534f5be380d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6cc159a43d83dcd1b1ee86022867b09a06e336ff16d6321cafeae6ec07010cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__814c6b127752b286e253a6e8cfa3e26433251e41bde3040e57b5bd1503c7e5b2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolTaskSchedulingPolicy]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb151771b796f981020b716b74652c3254291af36aa451a866f841ab4427faf3(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__268a7c374a8db56abbce08f53f105060051bd65bd6d8fd12dbecefba0fdeb3ad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8133d93fad6326aee5aec3e8f6be47a5ec13e4197935965f3b3b07992e56c072(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef8ad46d06a38d4322e05684ce123a31283a5eee073f6fce7d6c9b1f90857aeb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7f99101da5c4047ed178cda3035ecd3d648c21681fc98513138bc85e098ce2c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec5d654d2a6130e4a462368bc37a2503a0a2615e02d130d2a8f92a62d1a028d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e01c50556dca3461466f81fda4b569b6f946d3ab27e1867aeb0ffe81810ec28e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16fbe5928d182db56ea3c2c5df121a519953cac9d2f702eec59b2282fcca1576(
    *,
    elevation_level: builtins.str,
    name: builtins.str,
    password: builtins.str,
    linux_user_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BatchPoolUserAccountsLinuxUserConfiguration, typing.Dict[builtins.str, typing.Any]]]]] = None,
    windows_user_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BatchPoolUserAccountsWindowsUserConfiguration, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__860ff867c9bef3745df858028ed162906d9a2f7676cbb570adada9d1f2f01e3c(
    *,
    gid: typing.Optional[jsii.Number] = None,
    ssh_private_key: typing.Optional[builtins.str] = None,
    uid: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42a4562feee77c823d29f8890a0ebc43a120be4b64f6b5dcfc715580744c9009(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef72074a5e2cd0b4427764d3c994413f07c3d786cb254fc66f915ca2055c7c63(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af97320e5531f9c091637a72b4730ac2cccc6057239aa61ffa62c2edb7e80d22(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac3c005fa1bc644bc2b43fc314ab31af0ce35743b8daab0cefd150e2f8792524(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47af667d16844e54da8823241e74db56bf64d4bcbfc14f7213c6d032ba669bbe(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd395ce7d7899792b25d42d9ba43f53de1023f38b6ba112d06c6f62447d4ee41(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolUserAccountsLinuxUserConfiguration]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13b21557f04feac4f3ebb2c7ed525a5160fffcc6af774f2c9aad88a0dc3bff4a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__937200869c92b5c701e03b93902549ecec7ab8c5f1da9d0af3fe4bf2961a09cf(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__159fdd4444501a338fb9adce27b450ddab1ddbafaec9b123fca57802d7c0dfc2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1c65ec3637316be5b88afc0297b604b08578425bff586258cf30e3dda37493e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09cb04fa6c2725f77b6e1e2a49481c2ddb7d9bd4c5f277cab18c2d381d9cdc9e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolUserAccountsLinuxUserConfiguration]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb5a008cad9296bd09395ff8174766cf6ed29b1850574255dfa3c535f0041eb3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ecf1b0dbd9d4639c2f0f3ddfa122bef6c176fbb8bba5b7d40a8d5b47d09a18d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3e04745bf630bacb07b3ef9fce41734e84e11f6a246c4ac08d3b3a6dc2ece39(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acff7565cada32121fb5953a913f564b976a1821fedb531ab21be30b8510abcc(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__465c0d6b73a2a4a4e48322032bac3ee0cb276ba73042634e3431874534f22a50(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9f14dc7109eb02dc4f14a092248eff9c5e19d0f3e2420d8bc4d041e1607c6aa(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolUserAccounts]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__810003e32cebf4a1d8eff3382c7130ff386bd357313e96e55c4150fa36577f3b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4758007952a2dc4298426013acc749a835d028e0bb47f72bfba2302039731716(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BatchPoolUserAccountsLinuxUserConfiguration, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ff895fd26f38bcba0129bd46f62d3c88ee18fa89c5c263e7956c63795ac939e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BatchPoolUserAccountsWindowsUserConfiguration, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4fb3e4ea2796ef57dfe0ce86e5f6607dec2fa376dc4bea0371fa40dfc8b123a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2354b2e32186f0c5186849a24d60542dfc93ae83a93f06f1cf162c16afb603dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59993ec021262db76f6401791752017161d91baa493da381f7e028e52d73d194(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__052c3ca46038d5a52b0ccd3824555814c5607ca65a6dedbab98b0b99b7652735(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolUserAccounts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae067d427001b50eac148deca0a356aff3a5dad4fb6164d49e0eb7da8bdd9e71(
    *,
    login_mode: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__271edb5cb8d1e5f7f97e3b57ca1470afe4f9d3eff2ccfc01956512f3f05f1520(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1467c3c6a4d9081c7d8949c5d6e42a15394198d2145afe7a41ea33d82c312543(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4706f6591889ca58dcab395846e75f7d072b75b894a7f1303ae8942d133539f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e2efcbbea55de77f05211550a79726c3598a7430ecdaa246d2a00cdbbaa3ce8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72e413f032af4cd483b248f27823ed7ff5c9c0b55e67d0b122620af88f2b13df(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d01f3be38cfb021ae782b3ff847ea29d9db2e7b8dc41b465b7e89af310b0f6a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolUserAccountsWindowsUserConfiguration]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a0b10c843a2ac1e490c8bfbabaee4abd66227c1d1ac0d5b08fefc3999674124(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3883cef82b12b7b5bb6c32b164be7d7314f7933090a32ad3f417506a3b4b385(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ab49e3c2bed1169409a4147b1f6d4fc60e6dcbeea8b9cffe7ef694b190ecb4e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolUserAccountsWindowsUserConfiguration]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b89b2c44e35b9298eb32de53e4171db49581b1d286039f5d1bbf8d06ca6873ca(
    *,
    enable_automatic_updates: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afb28756786136d0deaa2ab870b7b91393d9705649b825caf6ec05465fc01928(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b128cc3ef952c55a2bfe0b1617d9e967ac5c5478f22295fdbad995f50a9104e4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b52db37dbabf9bfcab7c13585f8f1a92e3ee574a4a1b4a8979777ade50ca16e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98bcec575752d097e955665802498e55c3b9f8ab126b9640574c8c7ab02e28d4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c72af04b9269e8715f34822dfe8198e243d1a23b177a903e7a6e8768a43d674(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f81ce213b138e3657a430bc1a82b59b1c165aeaefd77f92ef5a840564800b32(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchPoolWindows]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4100ec27b5eecb21822b38c28a466b4b6d95e89d348d68d6bbedeb214a847cf0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eeebf5a4e69eb06bcdd0ad6fc1fd87c177fad7d2b9d8e1aa9e26cf71a0684ca7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad612d3aba7733300e338a03fa4437e4425553a3339420296d12e39f6bd6b33c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BatchPoolWindows]],
) -> None:
    """Type checking stubs"""
    pass
