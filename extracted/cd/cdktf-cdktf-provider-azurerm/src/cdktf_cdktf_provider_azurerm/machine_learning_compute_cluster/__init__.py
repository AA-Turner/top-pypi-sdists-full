r'''
# `azurerm_machine_learning_compute_cluster`

Refer to the Terraform Registry for docs: [`azurerm_machine_learning_compute_cluster`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster).
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


class MachineLearningComputeCluster(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.machineLearningComputeCluster.MachineLearningComputeCluster",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster azurerm_machine_learning_compute_cluster}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        machine_learning_workspace_id: builtins.str,
        name: builtins.str,
        scale_settings: typing.Union["MachineLearningComputeClusterScaleSettings", typing.Dict[builtins.str, typing.Any]],
        vm_priority: builtins.str,
        vm_size: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        identity: typing.Optional[typing.Union["MachineLearningComputeClusterIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        local_auth_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        node_public_ip_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ssh: typing.Optional[typing.Union["MachineLearningComputeClusterSsh", typing.Dict[builtins.str, typing.Any]]] = None,
        ssh_public_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        subnet_resource_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["MachineLearningComputeClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster azurerm_machine_learning_compute_cluster} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#location MachineLearningComputeCluster#location}.
        :param machine_learning_workspace_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#machine_learning_workspace_id MachineLearningComputeCluster#machine_learning_workspace_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#name MachineLearningComputeCluster#name}.
        :param scale_settings: scale_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#scale_settings MachineLearningComputeCluster#scale_settings}
        :param vm_priority: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#vm_priority MachineLearningComputeCluster#vm_priority}.
        :param vm_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#vm_size MachineLearningComputeCluster#vm_size}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#description MachineLearningComputeCluster#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#id MachineLearningComputeCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity: identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#identity MachineLearningComputeCluster#identity}
        :param local_auth_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#local_auth_enabled MachineLearningComputeCluster#local_auth_enabled}.
        :param node_public_ip_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#node_public_ip_enabled MachineLearningComputeCluster#node_public_ip_enabled}.
        :param ssh: ssh block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#ssh MachineLearningComputeCluster#ssh}
        :param ssh_public_access_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#ssh_public_access_enabled MachineLearningComputeCluster#ssh_public_access_enabled}.
        :param subnet_resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#subnet_resource_id MachineLearningComputeCluster#subnet_resource_id}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#tags MachineLearningComputeCluster#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#timeouts MachineLearningComputeCluster#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0c7bb38c8d5cca690107f0ed15225dc1c222a547b1487bf24e58ad0b23268d5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = MachineLearningComputeClusterConfig(
            location=location,
            machine_learning_workspace_id=machine_learning_workspace_id,
            name=name,
            scale_settings=scale_settings,
            vm_priority=vm_priority,
            vm_size=vm_size,
            description=description,
            id=id,
            identity=identity,
            local_auth_enabled=local_auth_enabled,
            node_public_ip_enabled=node_public_ip_enabled,
            ssh=ssh,
            ssh_public_access_enabled=ssh_public_access_enabled,
            subnet_resource_id=subnet_resource_id,
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
        '''Generates CDKTF code for importing a MachineLearningComputeCluster resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the MachineLearningComputeCluster to import.
        :param import_from_id: The id of the existing MachineLearningComputeCluster that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the MachineLearningComputeCluster to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69cf880a23b6e562c9916e6debef95da8be053acbde71df83edd6c9b7dee3009)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putIdentity")
    def put_identity(
        self,
        *,
        type: builtins.str,
        identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#type MachineLearningComputeCluster#type}.
        :param identity_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#identity_ids MachineLearningComputeCluster#identity_ids}.
        '''
        value = MachineLearningComputeClusterIdentity(
            type=type, identity_ids=identity_ids
        )

        return typing.cast(None, jsii.invoke(self, "putIdentity", [value]))

    @jsii.member(jsii_name="putScaleSettings")
    def put_scale_settings(
        self,
        *,
        max_node_count: jsii.Number,
        min_node_count: jsii.Number,
        scale_down_nodes_after_idle_duration: builtins.str,
    ) -> None:
        '''
        :param max_node_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#max_node_count MachineLearningComputeCluster#max_node_count}.
        :param min_node_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#min_node_count MachineLearningComputeCluster#min_node_count}.
        :param scale_down_nodes_after_idle_duration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#scale_down_nodes_after_idle_duration MachineLearningComputeCluster#scale_down_nodes_after_idle_duration}.
        '''
        value = MachineLearningComputeClusterScaleSettings(
            max_node_count=max_node_count,
            min_node_count=min_node_count,
            scale_down_nodes_after_idle_duration=scale_down_nodes_after_idle_duration,
        )

        return typing.cast(None, jsii.invoke(self, "putScaleSettings", [value]))

    @jsii.member(jsii_name="putSsh")
    def put_ssh(
        self,
        *,
        admin_username: builtins.str,
        admin_password: typing.Optional[builtins.str] = None,
        key_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param admin_username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#admin_username MachineLearningComputeCluster#admin_username}.
        :param admin_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#admin_password MachineLearningComputeCluster#admin_password}.
        :param key_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#key_value MachineLearningComputeCluster#key_value}.
        '''
        value = MachineLearningComputeClusterSsh(
            admin_username=admin_username,
            admin_password=admin_password,
            key_value=key_value,
        )

        return typing.cast(None, jsii.invoke(self, "putSsh", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#create MachineLearningComputeCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#delete MachineLearningComputeCluster#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#read MachineLearningComputeCluster#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#update MachineLearningComputeCluster#update}.
        '''
        value = MachineLearningComputeClusterTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIdentity")
    def reset_identity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentity", []))

    @jsii.member(jsii_name="resetLocalAuthEnabled")
    def reset_local_auth_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalAuthEnabled", []))

    @jsii.member(jsii_name="resetNodePublicIpEnabled")
    def reset_node_public_ip_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodePublicIpEnabled", []))

    @jsii.member(jsii_name="resetSsh")
    def reset_ssh(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSsh", []))

    @jsii.member(jsii_name="resetSshPublicAccessEnabled")
    def reset_ssh_public_access_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSshPublicAccessEnabled", []))

    @jsii.member(jsii_name="resetSubnetResourceId")
    def reset_subnet_resource_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnetResourceId", []))

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
    @jsii.member(jsii_name="identity")
    def identity(self) -> "MachineLearningComputeClusterIdentityOutputReference":
        return typing.cast("MachineLearningComputeClusterIdentityOutputReference", jsii.get(self, "identity"))

    @builtins.property
    @jsii.member(jsii_name="scaleSettings")
    def scale_settings(
        self,
    ) -> "MachineLearningComputeClusterScaleSettingsOutputReference":
        return typing.cast("MachineLearningComputeClusterScaleSettingsOutputReference", jsii.get(self, "scaleSettings"))

    @builtins.property
    @jsii.member(jsii_name="ssh")
    def ssh(self) -> "MachineLearningComputeClusterSshOutputReference":
        return typing.cast("MachineLearningComputeClusterSshOutputReference", jsii.get(self, "ssh"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "MachineLearningComputeClusterTimeoutsOutputReference":
        return typing.cast("MachineLearningComputeClusterTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="identityInput")
    def identity_input(
        self,
    ) -> typing.Optional["MachineLearningComputeClusterIdentity"]:
        return typing.cast(typing.Optional["MachineLearningComputeClusterIdentity"], jsii.get(self, "identityInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="localAuthEnabledInput")
    def local_auth_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "localAuthEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="machineLearningWorkspaceIdInput")
    def machine_learning_workspace_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "machineLearningWorkspaceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="nodePublicIpEnabledInput")
    def node_public_ip_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "nodePublicIpEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="scaleSettingsInput")
    def scale_settings_input(
        self,
    ) -> typing.Optional["MachineLearningComputeClusterScaleSettings"]:
        return typing.cast(typing.Optional["MachineLearningComputeClusterScaleSettings"], jsii.get(self, "scaleSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="sshInput")
    def ssh_input(self) -> typing.Optional["MachineLearningComputeClusterSsh"]:
        return typing.cast(typing.Optional["MachineLearningComputeClusterSsh"], jsii.get(self, "sshInput"))

    @builtins.property
    @jsii.member(jsii_name="sshPublicAccessEnabledInput")
    def ssh_public_access_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "sshPublicAccessEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetResourceIdInput")
    def subnet_resource_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetResourceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "MachineLearningComputeClusterTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "MachineLearningComputeClusterTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="vmPriorityInput")
    def vm_priority_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vmPriorityInput"))

    @builtins.property
    @jsii.member(jsii_name="vmSizeInput")
    def vm_size_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vmSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dc05c0055018b856d81ebfaacc05e8a8b827ac0e3fc4104921b4b9a6e502785)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1895d4ff01154004e10ee1b30f3182bcb53aac2ef5bf88865bcae917949e00dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localAuthEnabled")
    def local_auth_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "localAuthEnabled"))

    @local_auth_enabled.setter
    def local_auth_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc4aed4130b01dbd1f721b31d293b510ef68a6085cc42d6faa29d7af78aac21e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localAuthEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5d470f5ca7b328ba57c9915fe4edbddf02d394cecad6e75ac9352cc5939d741)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="machineLearningWorkspaceId")
    def machine_learning_workspace_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "machineLearningWorkspaceId"))

    @machine_learning_workspace_id.setter
    def machine_learning_workspace_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34ce70ceab6699d9dab0356dd330a46b57f21f049761a5759e2138d07ed5df65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "machineLearningWorkspaceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d51c267e3d9b9976e3895a28f1e89761883c57e1b82ccad232e3dcecac2cafb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodePublicIpEnabled")
    def node_public_ip_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "nodePublicIpEnabled"))

    @node_public_ip_enabled.setter
    def node_public_ip_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e6b7efca1a18d9b88ef93b64cc5680e461b920f15da43086d81947d08499db2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodePublicIpEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sshPublicAccessEnabled")
    def ssh_public_access_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "sshPublicAccessEnabled"))

    @ssh_public_access_enabled.setter
    def ssh_public_access_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79ea87d0e6e90f3761036488c8bcf0cd93f990cbbbe906c9b468e568d129989e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sshPublicAccessEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetResourceId")
    def subnet_resource_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetResourceId"))

    @subnet_resource_id.setter
    def subnet_resource_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc0f2e0a0ad18ea1a0b7968c4ca182c99009e084abae687a0a053fb840e57f3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetResourceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7273f459eb583d8b43a3dd142a61239100443079c427ac67ffd74eab88bae512)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vmPriority")
    def vm_priority(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vmPriority"))

    @vm_priority.setter
    def vm_priority(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__862dccdcd01e3786f9be4a7cb640e999a89bf76050bb3288e3540f27de065924)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vmPriority", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vmSize")
    def vm_size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vmSize"))

    @vm_size.setter
    def vm_size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da6edcff8cc4e2ea5dcfd04e6d1b6482d7c852f718fdbd1926d0c167b6fee84f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vmSize", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.machineLearningComputeCluster.MachineLearningComputeClusterConfig",
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
        "machine_learning_workspace_id": "machineLearningWorkspaceId",
        "name": "name",
        "scale_settings": "scaleSettings",
        "vm_priority": "vmPriority",
        "vm_size": "vmSize",
        "description": "description",
        "id": "id",
        "identity": "identity",
        "local_auth_enabled": "localAuthEnabled",
        "node_public_ip_enabled": "nodePublicIpEnabled",
        "ssh": "ssh",
        "ssh_public_access_enabled": "sshPublicAccessEnabled",
        "subnet_resource_id": "subnetResourceId",
        "tags": "tags",
        "timeouts": "timeouts",
    },
)
class MachineLearningComputeClusterConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        machine_learning_workspace_id: builtins.str,
        name: builtins.str,
        scale_settings: typing.Union["MachineLearningComputeClusterScaleSettings", typing.Dict[builtins.str, typing.Any]],
        vm_priority: builtins.str,
        vm_size: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        identity: typing.Optional[typing.Union["MachineLearningComputeClusterIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        local_auth_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        node_public_ip_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ssh: typing.Optional[typing.Union["MachineLearningComputeClusterSsh", typing.Dict[builtins.str, typing.Any]]] = None,
        ssh_public_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        subnet_resource_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["MachineLearningComputeClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#location MachineLearningComputeCluster#location}.
        :param machine_learning_workspace_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#machine_learning_workspace_id MachineLearningComputeCluster#machine_learning_workspace_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#name MachineLearningComputeCluster#name}.
        :param scale_settings: scale_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#scale_settings MachineLearningComputeCluster#scale_settings}
        :param vm_priority: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#vm_priority MachineLearningComputeCluster#vm_priority}.
        :param vm_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#vm_size MachineLearningComputeCluster#vm_size}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#description MachineLearningComputeCluster#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#id MachineLearningComputeCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity: identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#identity MachineLearningComputeCluster#identity}
        :param local_auth_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#local_auth_enabled MachineLearningComputeCluster#local_auth_enabled}.
        :param node_public_ip_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#node_public_ip_enabled MachineLearningComputeCluster#node_public_ip_enabled}.
        :param ssh: ssh block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#ssh MachineLearningComputeCluster#ssh}
        :param ssh_public_access_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#ssh_public_access_enabled MachineLearningComputeCluster#ssh_public_access_enabled}.
        :param subnet_resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#subnet_resource_id MachineLearningComputeCluster#subnet_resource_id}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#tags MachineLearningComputeCluster#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#timeouts MachineLearningComputeCluster#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(scale_settings, dict):
            scale_settings = MachineLearningComputeClusterScaleSettings(**scale_settings)
        if isinstance(identity, dict):
            identity = MachineLearningComputeClusterIdentity(**identity)
        if isinstance(ssh, dict):
            ssh = MachineLearningComputeClusterSsh(**ssh)
        if isinstance(timeouts, dict):
            timeouts = MachineLearningComputeClusterTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b78461cd4fa80479f5f5bbf2ecb0ef913e16b1338ad7ad6933727521dabb72f0)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument machine_learning_workspace_id", value=machine_learning_workspace_id, expected_type=type_hints["machine_learning_workspace_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument scale_settings", value=scale_settings, expected_type=type_hints["scale_settings"])
            check_type(argname="argument vm_priority", value=vm_priority, expected_type=type_hints["vm_priority"])
            check_type(argname="argument vm_size", value=vm_size, expected_type=type_hints["vm_size"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
            check_type(argname="argument local_auth_enabled", value=local_auth_enabled, expected_type=type_hints["local_auth_enabled"])
            check_type(argname="argument node_public_ip_enabled", value=node_public_ip_enabled, expected_type=type_hints["node_public_ip_enabled"])
            check_type(argname="argument ssh", value=ssh, expected_type=type_hints["ssh"])
            check_type(argname="argument ssh_public_access_enabled", value=ssh_public_access_enabled, expected_type=type_hints["ssh_public_access_enabled"])
            check_type(argname="argument subnet_resource_id", value=subnet_resource_id, expected_type=type_hints["subnet_resource_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
            "machine_learning_workspace_id": machine_learning_workspace_id,
            "name": name,
            "scale_settings": scale_settings,
            "vm_priority": vm_priority,
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
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if identity is not None:
            self._values["identity"] = identity
        if local_auth_enabled is not None:
            self._values["local_auth_enabled"] = local_auth_enabled
        if node_public_ip_enabled is not None:
            self._values["node_public_ip_enabled"] = node_public_ip_enabled
        if ssh is not None:
            self._values["ssh"] = ssh
        if ssh_public_access_enabled is not None:
            self._values["ssh_public_access_enabled"] = ssh_public_access_enabled
        if subnet_resource_id is not None:
            self._values["subnet_resource_id"] = subnet_resource_id
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
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#location MachineLearningComputeCluster#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def machine_learning_workspace_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#machine_learning_workspace_id MachineLearningComputeCluster#machine_learning_workspace_id}.'''
        result = self._values.get("machine_learning_workspace_id")
        assert result is not None, "Required property 'machine_learning_workspace_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#name MachineLearningComputeCluster#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def scale_settings(self) -> "MachineLearningComputeClusterScaleSettings":
        '''scale_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#scale_settings MachineLearningComputeCluster#scale_settings}
        '''
        result = self._values.get("scale_settings")
        assert result is not None, "Required property 'scale_settings' is missing"
        return typing.cast("MachineLearningComputeClusterScaleSettings", result)

    @builtins.property
    def vm_priority(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#vm_priority MachineLearningComputeCluster#vm_priority}.'''
        result = self._values.get("vm_priority")
        assert result is not None, "Required property 'vm_priority' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vm_size(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#vm_size MachineLearningComputeCluster#vm_size}.'''
        result = self._values.get("vm_size")
        assert result is not None, "Required property 'vm_size' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#description MachineLearningComputeCluster#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#id MachineLearningComputeCluster#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity(self) -> typing.Optional["MachineLearningComputeClusterIdentity"]:
        '''identity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#identity MachineLearningComputeCluster#identity}
        '''
        result = self._values.get("identity")
        return typing.cast(typing.Optional["MachineLearningComputeClusterIdentity"], result)

    @builtins.property
    def local_auth_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#local_auth_enabled MachineLearningComputeCluster#local_auth_enabled}.'''
        result = self._values.get("local_auth_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def node_public_ip_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#node_public_ip_enabled MachineLearningComputeCluster#node_public_ip_enabled}.'''
        result = self._values.get("node_public_ip_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ssh(self) -> typing.Optional["MachineLearningComputeClusterSsh"]:
        '''ssh block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#ssh MachineLearningComputeCluster#ssh}
        '''
        result = self._values.get("ssh")
        return typing.cast(typing.Optional["MachineLearningComputeClusterSsh"], result)

    @builtins.property
    def ssh_public_access_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#ssh_public_access_enabled MachineLearningComputeCluster#ssh_public_access_enabled}.'''
        result = self._values.get("ssh_public_access_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def subnet_resource_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#subnet_resource_id MachineLearningComputeCluster#subnet_resource_id}.'''
        result = self._values.get("subnet_resource_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#tags MachineLearningComputeCluster#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["MachineLearningComputeClusterTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#timeouts MachineLearningComputeCluster#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["MachineLearningComputeClusterTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MachineLearningComputeClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.machineLearningComputeCluster.MachineLearningComputeClusterIdentity",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "identity_ids": "identityIds"},
)
class MachineLearningComputeClusterIdentity:
    def __init__(
        self,
        *,
        type: builtins.str,
        identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#type MachineLearningComputeCluster#type}.
        :param identity_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#identity_ids MachineLearningComputeCluster#identity_ids}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b1faa5e89a47853f5bd265a1fa902ed42591d75d3ebb7d0cd30a07c9d1d82f2)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument identity_ids", value=identity_ids, expected_type=type_hints["identity_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if identity_ids is not None:
            self._values["identity_ids"] = identity_ids

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#type MachineLearningComputeCluster#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def identity_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#identity_ids MachineLearningComputeCluster#identity_ids}.'''
        result = self._values.get("identity_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MachineLearningComputeClusterIdentity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MachineLearningComputeClusterIdentityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.machineLearningComputeCluster.MachineLearningComputeClusterIdentityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c5b7ef5f05fdde80be1925cf4e2fcee498501dab68dee115d332cc217ea00b17)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIdentityIds")
    def reset_identity_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentityIds", []))

    @builtins.property
    @jsii.member(jsii_name="principalId")
    def principal_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "principalId"))

    @builtins.property
    @jsii.member(jsii_name="tenantId")
    def tenant_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tenantId"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__b67c45885f260b28175c26dce206bf3f73eb472fb4ec4fe45d8b57c9ee2b50b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15c22ec859bf70fd1e518f4b401e01172d16f64187d214df4afb1498c524390a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MachineLearningComputeClusterIdentity]:
        return typing.cast(typing.Optional[MachineLearningComputeClusterIdentity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MachineLearningComputeClusterIdentity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a19d9fc114802e7d257e10c2e6f04fb46be9154dd4d31ec2be8c0afb382f40f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.machineLearningComputeCluster.MachineLearningComputeClusterScaleSettings",
    jsii_struct_bases=[],
    name_mapping={
        "max_node_count": "maxNodeCount",
        "min_node_count": "minNodeCount",
        "scale_down_nodes_after_idle_duration": "scaleDownNodesAfterIdleDuration",
    },
)
class MachineLearningComputeClusterScaleSettings:
    def __init__(
        self,
        *,
        max_node_count: jsii.Number,
        min_node_count: jsii.Number,
        scale_down_nodes_after_idle_duration: builtins.str,
    ) -> None:
        '''
        :param max_node_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#max_node_count MachineLearningComputeCluster#max_node_count}.
        :param min_node_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#min_node_count MachineLearningComputeCluster#min_node_count}.
        :param scale_down_nodes_after_idle_duration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#scale_down_nodes_after_idle_duration MachineLearningComputeCluster#scale_down_nodes_after_idle_duration}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc4df50bee4d97b3684fafc19c16da900c7d755b6254baeaf9bc1ea1d99c0d48)
            check_type(argname="argument max_node_count", value=max_node_count, expected_type=type_hints["max_node_count"])
            check_type(argname="argument min_node_count", value=min_node_count, expected_type=type_hints["min_node_count"])
            check_type(argname="argument scale_down_nodes_after_idle_duration", value=scale_down_nodes_after_idle_duration, expected_type=type_hints["scale_down_nodes_after_idle_duration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "max_node_count": max_node_count,
            "min_node_count": min_node_count,
            "scale_down_nodes_after_idle_duration": scale_down_nodes_after_idle_duration,
        }

    @builtins.property
    def max_node_count(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#max_node_count MachineLearningComputeCluster#max_node_count}.'''
        result = self._values.get("max_node_count")
        assert result is not None, "Required property 'max_node_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def min_node_count(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#min_node_count MachineLearningComputeCluster#min_node_count}.'''
        result = self._values.get("min_node_count")
        assert result is not None, "Required property 'min_node_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def scale_down_nodes_after_idle_duration(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#scale_down_nodes_after_idle_duration MachineLearningComputeCluster#scale_down_nodes_after_idle_duration}.'''
        result = self._values.get("scale_down_nodes_after_idle_duration")
        assert result is not None, "Required property 'scale_down_nodes_after_idle_duration' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MachineLearningComputeClusterScaleSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MachineLearningComputeClusterScaleSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.machineLearningComputeCluster.MachineLearningComputeClusterScaleSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2f3c32f6b3333f0b2df7e6cbb17fc4cca2cb2fc4e6ef94b4e2a8edabfbd90df5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="maxNodeCountInput")
    def max_node_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxNodeCountInput"))

    @builtins.property
    @jsii.member(jsii_name="minNodeCountInput")
    def min_node_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minNodeCountInput"))

    @builtins.property
    @jsii.member(jsii_name="scaleDownNodesAfterIdleDurationInput")
    def scale_down_nodes_after_idle_duration_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scaleDownNodesAfterIdleDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="maxNodeCount")
    def max_node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxNodeCount"))

    @max_node_count.setter
    def max_node_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31387cad5f281a48e240b1450d9bf1e0c2ca4034bfd683bdf68f322994c0be97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxNodeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minNodeCount")
    def min_node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minNodeCount"))

    @min_node_count.setter
    def min_node_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__834f768715eaea291be0cb9b85585774efb075c0ee8126b63a281eb2d5012d94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minNodeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scaleDownNodesAfterIdleDuration")
    def scale_down_nodes_after_idle_duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scaleDownNodesAfterIdleDuration"))

    @scale_down_nodes_after_idle_duration.setter
    def scale_down_nodes_after_idle_duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67338b984c8165e74d6295cac571c92744128798fc299e7a8f266cfe82f73629)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scaleDownNodesAfterIdleDuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MachineLearningComputeClusterScaleSettings]:
        return typing.cast(typing.Optional[MachineLearningComputeClusterScaleSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MachineLearningComputeClusterScaleSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10ed54345b69c0a49f169465f43b459aa2363753d43f48554dc6c122bfed126b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.machineLearningComputeCluster.MachineLearningComputeClusterSsh",
    jsii_struct_bases=[],
    name_mapping={
        "admin_username": "adminUsername",
        "admin_password": "adminPassword",
        "key_value": "keyValue",
    },
)
class MachineLearningComputeClusterSsh:
    def __init__(
        self,
        *,
        admin_username: builtins.str,
        admin_password: typing.Optional[builtins.str] = None,
        key_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param admin_username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#admin_username MachineLearningComputeCluster#admin_username}.
        :param admin_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#admin_password MachineLearningComputeCluster#admin_password}.
        :param key_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#key_value MachineLearningComputeCluster#key_value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40f09a8f89ccd99398ba69bf5bde131ed845c58f60e5957d725fddf44139798d)
            check_type(argname="argument admin_username", value=admin_username, expected_type=type_hints["admin_username"])
            check_type(argname="argument admin_password", value=admin_password, expected_type=type_hints["admin_password"])
            check_type(argname="argument key_value", value=key_value, expected_type=type_hints["key_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "admin_username": admin_username,
        }
        if admin_password is not None:
            self._values["admin_password"] = admin_password
        if key_value is not None:
            self._values["key_value"] = key_value

    @builtins.property
    def admin_username(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#admin_username MachineLearningComputeCluster#admin_username}.'''
        result = self._values.get("admin_username")
        assert result is not None, "Required property 'admin_username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def admin_password(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#admin_password MachineLearningComputeCluster#admin_password}.'''
        result = self._values.get("admin_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#key_value MachineLearningComputeCluster#key_value}.'''
        result = self._values.get("key_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MachineLearningComputeClusterSsh(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MachineLearningComputeClusterSshOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.machineLearningComputeCluster.MachineLearningComputeClusterSshOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__552cce2b670021b546ee245807823215380d4d5369fb2809dbd23b51f60848f3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAdminPassword")
    def reset_admin_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdminPassword", []))

    @jsii.member(jsii_name="resetKeyValue")
    def reset_key_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyValue", []))

    @builtins.property
    @jsii.member(jsii_name="adminPasswordInput")
    def admin_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "adminPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="adminUsernameInput")
    def admin_username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "adminUsernameInput"))

    @builtins.property
    @jsii.member(jsii_name="keyValueInput")
    def key_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyValueInput"))

    @builtins.property
    @jsii.member(jsii_name="adminPassword")
    def admin_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "adminPassword"))

    @admin_password.setter
    def admin_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cf782cc332f8ae43e2122fa27baa4809d1c28b680c6e439f983d31d87c6e9d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adminPassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="adminUsername")
    def admin_username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "adminUsername"))

    @admin_username.setter
    def admin_username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21d4bff5d707e9d77f45671fdabbd8e0bd17eec2727cddfe1dd1d77ec75528a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adminUsername", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyValue")
    def key_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyValue"))

    @key_value.setter
    def key_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f170be3b8cf7ab41547737b719d32117d45f4ba00578fff68df4182826e9ba5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MachineLearningComputeClusterSsh]:
        return typing.cast(typing.Optional[MachineLearningComputeClusterSsh], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MachineLearningComputeClusterSsh],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d9eb22d0605561787dc0896b8884bd2ac2f99fe48265f94f3b15a548a27e75b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.machineLearningComputeCluster.MachineLearningComputeClusterTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class MachineLearningComputeClusterTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#create MachineLearningComputeCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#delete MachineLearningComputeCluster#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#read MachineLearningComputeCluster#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#update MachineLearningComputeCluster#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__047bb7b1d670003741345d2621a28bb3cc00a6d6cd54d89a74cd4c9985a35fe4)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#create MachineLearningComputeCluster#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#delete MachineLearningComputeCluster#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#read MachineLearningComputeCluster#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_compute_cluster#update MachineLearningComputeCluster#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MachineLearningComputeClusterTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MachineLearningComputeClusterTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.machineLearningComputeCluster.MachineLearningComputeClusterTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__694deef55bd1ab728066faf9b4b0d3f4e051ce019613b1ed00b4b60dffaa7442)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc7fa5b9aaf07c1716ee0ded4d5def50d3f0d7fd12b5d8163464ee1535d7191b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ab2eca252454952a52c292a5ec9a9a3d39d93a34fad9fd0febee11f452d2f83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__042348d0dfa019e505d00094b8df4ae82302fbce4fd9c1cae599e6248748c0dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6104e8fdb8b7d5a8fb23613d5bafc4a8265a71453e26dc035d9b6d34860b801e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MachineLearningComputeClusterTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MachineLearningComputeClusterTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MachineLearningComputeClusterTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dba23c8e515937a8eba257d428eddda39eb41ea80abe25425f803b435a72e18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "MachineLearningComputeCluster",
    "MachineLearningComputeClusterConfig",
    "MachineLearningComputeClusterIdentity",
    "MachineLearningComputeClusterIdentityOutputReference",
    "MachineLearningComputeClusterScaleSettings",
    "MachineLearningComputeClusterScaleSettingsOutputReference",
    "MachineLearningComputeClusterSsh",
    "MachineLearningComputeClusterSshOutputReference",
    "MachineLearningComputeClusterTimeouts",
    "MachineLearningComputeClusterTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__a0c7bb38c8d5cca690107f0ed15225dc1c222a547b1487bf24e58ad0b23268d5(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    machine_learning_workspace_id: builtins.str,
    name: builtins.str,
    scale_settings: typing.Union[MachineLearningComputeClusterScaleSettings, typing.Dict[builtins.str, typing.Any]],
    vm_priority: builtins.str,
    vm_size: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    identity: typing.Optional[typing.Union[MachineLearningComputeClusterIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    local_auth_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    node_public_ip_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ssh: typing.Optional[typing.Union[MachineLearningComputeClusterSsh, typing.Dict[builtins.str, typing.Any]]] = None,
    ssh_public_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    subnet_resource_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[MachineLearningComputeClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__69cf880a23b6e562c9916e6debef95da8be053acbde71df83edd6c9b7dee3009(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dc05c0055018b856d81ebfaacc05e8a8b827ac0e3fc4104921b4b9a6e502785(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1895d4ff01154004e10ee1b30f3182bcb53aac2ef5bf88865bcae917949e00dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc4aed4130b01dbd1f721b31d293b510ef68a6085cc42d6faa29d7af78aac21e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5d470f5ca7b328ba57c9915fe4edbddf02d394cecad6e75ac9352cc5939d741(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34ce70ceab6699d9dab0356dd330a46b57f21f049761a5759e2138d07ed5df65(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d51c267e3d9b9976e3895a28f1e89761883c57e1b82ccad232e3dcecac2cafb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e6b7efca1a18d9b88ef93b64cc5680e461b920f15da43086d81947d08499db2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79ea87d0e6e90f3761036488c8bcf0cd93f990cbbbe906c9b468e568d129989e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc0f2e0a0ad18ea1a0b7968c4ca182c99009e084abae687a0a053fb840e57f3f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7273f459eb583d8b43a3dd142a61239100443079c427ac67ffd74eab88bae512(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__862dccdcd01e3786f9be4a7cb640e999a89bf76050bb3288e3540f27de065924(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da6edcff8cc4e2ea5dcfd04e6d1b6482d7c852f718fdbd1926d0c167b6fee84f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b78461cd4fa80479f5f5bbf2ecb0ef913e16b1338ad7ad6933727521dabb72f0(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location: builtins.str,
    machine_learning_workspace_id: builtins.str,
    name: builtins.str,
    scale_settings: typing.Union[MachineLearningComputeClusterScaleSettings, typing.Dict[builtins.str, typing.Any]],
    vm_priority: builtins.str,
    vm_size: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    identity: typing.Optional[typing.Union[MachineLearningComputeClusterIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    local_auth_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    node_public_ip_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ssh: typing.Optional[typing.Union[MachineLearningComputeClusterSsh, typing.Dict[builtins.str, typing.Any]]] = None,
    ssh_public_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    subnet_resource_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[MachineLearningComputeClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b1faa5e89a47853f5bd265a1fa902ed42591d75d3ebb7d0cd30a07c9d1d82f2(
    *,
    type: builtins.str,
    identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5b7ef5f05fdde80be1925cf4e2fcee498501dab68dee115d332cc217ea00b17(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b67c45885f260b28175c26dce206bf3f73eb472fb4ec4fe45d8b57c9ee2b50b2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15c22ec859bf70fd1e518f4b401e01172d16f64187d214df4afb1498c524390a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a19d9fc114802e7d257e10c2e6f04fb46be9154dd4d31ec2be8c0afb382f40f4(
    value: typing.Optional[MachineLearningComputeClusterIdentity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc4df50bee4d97b3684fafc19c16da900c7d755b6254baeaf9bc1ea1d99c0d48(
    *,
    max_node_count: jsii.Number,
    min_node_count: jsii.Number,
    scale_down_nodes_after_idle_duration: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f3c32f6b3333f0b2df7e6cbb17fc4cca2cb2fc4e6ef94b4e2a8edabfbd90df5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31387cad5f281a48e240b1450d9bf1e0c2ca4034bfd683bdf68f322994c0be97(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__834f768715eaea291be0cb9b85585774efb075c0ee8126b63a281eb2d5012d94(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67338b984c8165e74d6295cac571c92744128798fc299e7a8f266cfe82f73629(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10ed54345b69c0a49f169465f43b459aa2363753d43f48554dc6c122bfed126b(
    value: typing.Optional[MachineLearningComputeClusterScaleSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40f09a8f89ccd99398ba69bf5bde131ed845c58f60e5957d725fddf44139798d(
    *,
    admin_username: builtins.str,
    admin_password: typing.Optional[builtins.str] = None,
    key_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__552cce2b670021b546ee245807823215380d4d5369fb2809dbd23b51f60848f3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cf782cc332f8ae43e2122fa27baa4809d1c28b680c6e439f983d31d87c6e9d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21d4bff5d707e9d77f45671fdabbd8e0bd17eec2727cddfe1dd1d77ec75528a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f170be3b8cf7ab41547737b719d32117d45f4ba00578fff68df4182826e9ba5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d9eb22d0605561787dc0896b8884bd2ac2f99fe48265f94f3b15a548a27e75b(
    value: typing.Optional[MachineLearningComputeClusterSsh],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__047bb7b1d670003741345d2621a28bb3cc00a6d6cd54d89a74cd4c9985a35fe4(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__694deef55bd1ab728066faf9b4b0d3f4e051ce019613b1ed00b4b60dffaa7442(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc7fa5b9aaf07c1716ee0ded4d5def50d3f0d7fd12b5d8163464ee1535d7191b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ab2eca252454952a52c292a5ec9a9a3d39d93a34fad9fd0febee11f452d2f83(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__042348d0dfa019e505d00094b8df4ae82302fbce4fd9c1cae599e6248748c0dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6104e8fdb8b7d5a8fb23613d5bafc4a8265a71453e26dc035d9b6d34860b801e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dba23c8e515937a8eba257d428eddda39eb41ea80abe25425f803b435a72e18(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MachineLearningComputeClusterTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
