r'''
# `google_compute_region_per_instance_config`

Refer to the Terraform Registry for docs: [`google_compute_region_per_instance_config`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config).
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


class ComputeRegionPerInstanceConfig(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionPerInstanceConfig.ComputeRegionPerInstanceConfig",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config google_compute_region_per_instance_config}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        region_instance_group_manager: builtins.str,
        id: typing.Optional[builtins.str] = None,
        minimal_action: typing.Optional[builtins.str] = None,
        most_disruptive_allowed_action: typing.Optional[builtins.str] = None,
        preserved_state: typing.Optional[typing.Union["ComputeRegionPerInstanceConfigPreservedState", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        remove_instance_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        remove_instance_state_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["ComputeRegionPerInstanceConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config google_compute_region_per_instance_config} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: The name for this per-instance config and its corresponding instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#name ComputeRegionPerInstanceConfig#name}
        :param region_instance_group_manager: The region instance group manager this instance config is part of. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#region_instance_group_manager ComputeRegionPerInstanceConfig#region_instance_group_manager}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#id ComputeRegionPerInstanceConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param minimal_action: The minimal action to perform on the instance during an update. Default is 'NONE'. Possible values are: - REPLACE - RESTART - REFRESH - NONE Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#minimal_action ComputeRegionPerInstanceConfig#minimal_action}
        :param most_disruptive_allowed_action: The most disruptive action to perform on the instance during an update. Default is 'REPLACE'. Possible values are: - REPLACE - RESTART - REFRESH - NONE Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#most_disruptive_allowed_action ComputeRegionPerInstanceConfig#most_disruptive_allowed_action}
        :param preserved_state: preserved_state block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#preserved_state ComputeRegionPerInstanceConfig#preserved_state}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#project ComputeRegionPerInstanceConfig#project}.
        :param region: Region where the containing instance group manager is located. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#region ComputeRegionPerInstanceConfig#region}
        :param remove_instance_on_destroy: When true, deleting this config will immediately remove the underlying instance. When false, deleting this config will use the behavior as determined by remove_instance_on_destroy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#remove_instance_on_destroy ComputeRegionPerInstanceConfig#remove_instance_on_destroy}
        :param remove_instance_state_on_destroy: When true, deleting this config will immediately remove any specified state from the underlying instance. When false, deleting this config will *not* immediately remove any state from the underlying instance. State will be removed on the next instance recreation or update. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#remove_instance_state_on_destroy ComputeRegionPerInstanceConfig#remove_instance_state_on_destroy}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#timeouts ComputeRegionPerInstanceConfig#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d3b4c07428889bc8bdc1f6d7e2a896449f9d80cc100b154cd57ab99f8546a67)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ComputeRegionPerInstanceConfigConfig(
            name=name,
            region_instance_group_manager=region_instance_group_manager,
            id=id,
            minimal_action=minimal_action,
            most_disruptive_allowed_action=most_disruptive_allowed_action,
            preserved_state=preserved_state,
            project=project,
            region=region,
            remove_instance_on_destroy=remove_instance_on_destroy,
            remove_instance_state_on_destroy=remove_instance_state_on_destroy,
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
        '''Generates CDKTF code for importing a ComputeRegionPerInstanceConfig resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ComputeRegionPerInstanceConfig to import.
        :param import_from_id: The id of the existing ComputeRegionPerInstanceConfig that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ComputeRegionPerInstanceConfig to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ab695e211ebf6f4fd605b5272ff852b4deb8ac528a9daa5d31a0805e6ad8d15)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putPreservedState")
    def put_preserved_state(
        self,
        *,
        disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionPerInstanceConfigPreservedStateDisk", typing.Dict[builtins.str, typing.Any]]]]] = None,
        external_ip: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionPerInstanceConfigPreservedStateExternalIp", typing.Dict[builtins.str, typing.Any]]]]] = None,
        internal_ip: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionPerInstanceConfigPreservedStateInternalIp", typing.Dict[builtins.str, typing.Any]]]]] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param disk: disk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#disk ComputeRegionPerInstanceConfig#disk}
        :param external_ip: external_ip block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#external_ip ComputeRegionPerInstanceConfig#external_ip}
        :param internal_ip: internal_ip block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#internal_ip ComputeRegionPerInstanceConfig#internal_ip}
        :param metadata: Preserved metadata defined for this instance. This is a list of key->value pairs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#metadata ComputeRegionPerInstanceConfig#metadata}
        '''
        value = ComputeRegionPerInstanceConfigPreservedState(
            disk=disk,
            external_ip=external_ip,
            internal_ip=internal_ip,
            metadata=metadata,
        )

        return typing.cast(None, jsii.invoke(self, "putPreservedState", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#create ComputeRegionPerInstanceConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#delete ComputeRegionPerInstanceConfig#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#update ComputeRegionPerInstanceConfig#update}.
        '''
        value = ComputeRegionPerInstanceConfigTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMinimalAction")
    def reset_minimal_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinimalAction", []))

    @jsii.member(jsii_name="resetMostDisruptiveAllowedAction")
    def reset_most_disruptive_allowed_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMostDisruptiveAllowedAction", []))

    @jsii.member(jsii_name="resetPreservedState")
    def reset_preserved_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreservedState", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetRemoveInstanceOnDestroy")
    def reset_remove_instance_on_destroy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRemoveInstanceOnDestroy", []))

    @jsii.member(jsii_name="resetRemoveInstanceStateOnDestroy")
    def reset_remove_instance_state_on_destroy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRemoveInstanceStateOnDestroy", []))

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
    @jsii.member(jsii_name="preservedState")
    def preserved_state(
        self,
    ) -> "ComputeRegionPerInstanceConfigPreservedStateOutputReference":
        return typing.cast("ComputeRegionPerInstanceConfigPreservedStateOutputReference", jsii.get(self, "preservedState"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ComputeRegionPerInstanceConfigTimeoutsOutputReference":
        return typing.cast("ComputeRegionPerInstanceConfigTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="minimalActionInput")
    def minimal_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minimalActionInput"))

    @builtins.property
    @jsii.member(jsii_name="mostDisruptiveAllowedActionInput")
    def most_disruptive_allowed_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mostDisruptiveAllowedActionInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="preservedStateInput")
    def preserved_state_input(
        self,
    ) -> typing.Optional["ComputeRegionPerInstanceConfigPreservedState"]:
        return typing.cast(typing.Optional["ComputeRegionPerInstanceConfigPreservedState"], jsii.get(self, "preservedStateInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInstanceGroupManagerInput")
    def region_instance_group_manager_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInstanceGroupManagerInput"))

    @builtins.property
    @jsii.member(jsii_name="removeInstanceOnDestroyInput")
    def remove_instance_on_destroy_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "removeInstanceOnDestroyInput"))

    @builtins.property
    @jsii.member(jsii_name="removeInstanceStateOnDestroyInput")
    def remove_instance_state_on_destroy_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "removeInstanceStateOnDestroyInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeRegionPerInstanceConfigTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeRegionPerInstanceConfigTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d08cf10da58fd57ee45c96187f5058b73d34b1895a5077e70345ba5402aeb6ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minimalAction")
    def minimal_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minimalAction"))

    @minimal_action.setter
    def minimal_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efb5b1a0acdb9d81e39748900f0ecd7305d712de7024fd4a3d3076dbfdc52231)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minimalAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mostDisruptiveAllowedAction")
    def most_disruptive_allowed_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mostDisruptiveAllowedAction"))

    @most_disruptive_allowed_action.setter
    def most_disruptive_allowed_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ed547a811601086f7bd8bb3e49e80e12df0977d23492347d3daba35f16f4c57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mostDisruptiveAllowedAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__316037137149f156a1017027a83aae75d90c9d1499999025a55b848d8613dc9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3aeac401bd2343fed7777645fa045f446249ce71a8648c7e7aae4914c5333b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7871ecee2b3d696057d8891209e45e79f640adeeb0e7b26e3fd7193ebdc920cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="regionInstanceGroupManager")
    def region_instance_group_manager(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "regionInstanceGroupManager"))

    @region_instance_group_manager.setter
    def region_instance_group_manager(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0af3dfbc2e843c5ea55fb0b5920b8a0b651bf4b933050cb1066a86cf1cef8c83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regionInstanceGroupManager", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="removeInstanceOnDestroy")
    def remove_instance_on_destroy(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "removeInstanceOnDestroy"))

    @remove_instance_on_destroy.setter
    def remove_instance_on_destroy(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d84930e55443aa748fe11e21d3cba1250bbe0a279415aca75f9aaa8c3433d61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "removeInstanceOnDestroy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="removeInstanceStateOnDestroy")
    def remove_instance_state_on_destroy(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "removeInstanceStateOnDestroy"))

    @remove_instance_state_on_destroy.setter
    def remove_instance_state_on_destroy(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de203a0bdfd48efd6332900a2db243919e50922bcf70a29085ee08553499f8af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "removeInstanceStateOnDestroy", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionPerInstanceConfig.ComputeRegionPerInstanceConfigConfig",
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
        "region_instance_group_manager": "regionInstanceGroupManager",
        "id": "id",
        "minimal_action": "minimalAction",
        "most_disruptive_allowed_action": "mostDisruptiveAllowedAction",
        "preserved_state": "preservedState",
        "project": "project",
        "region": "region",
        "remove_instance_on_destroy": "removeInstanceOnDestroy",
        "remove_instance_state_on_destroy": "removeInstanceStateOnDestroy",
        "timeouts": "timeouts",
    },
)
class ComputeRegionPerInstanceConfigConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        region_instance_group_manager: builtins.str,
        id: typing.Optional[builtins.str] = None,
        minimal_action: typing.Optional[builtins.str] = None,
        most_disruptive_allowed_action: typing.Optional[builtins.str] = None,
        preserved_state: typing.Optional[typing.Union["ComputeRegionPerInstanceConfigPreservedState", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        remove_instance_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        remove_instance_state_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["ComputeRegionPerInstanceConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: The name for this per-instance config and its corresponding instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#name ComputeRegionPerInstanceConfig#name}
        :param region_instance_group_manager: The region instance group manager this instance config is part of. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#region_instance_group_manager ComputeRegionPerInstanceConfig#region_instance_group_manager}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#id ComputeRegionPerInstanceConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param minimal_action: The minimal action to perform on the instance during an update. Default is 'NONE'. Possible values are: - REPLACE - RESTART - REFRESH - NONE Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#minimal_action ComputeRegionPerInstanceConfig#minimal_action}
        :param most_disruptive_allowed_action: The most disruptive action to perform on the instance during an update. Default is 'REPLACE'. Possible values are: - REPLACE - RESTART - REFRESH - NONE Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#most_disruptive_allowed_action ComputeRegionPerInstanceConfig#most_disruptive_allowed_action}
        :param preserved_state: preserved_state block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#preserved_state ComputeRegionPerInstanceConfig#preserved_state}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#project ComputeRegionPerInstanceConfig#project}.
        :param region: Region where the containing instance group manager is located. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#region ComputeRegionPerInstanceConfig#region}
        :param remove_instance_on_destroy: When true, deleting this config will immediately remove the underlying instance. When false, deleting this config will use the behavior as determined by remove_instance_on_destroy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#remove_instance_on_destroy ComputeRegionPerInstanceConfig#remove_instance_on_destroy}
        :param remove_instance_state_on_destroy: When true, deleting this config will immediately remove any specified state from the underlying instance. When false, deleting this config will *not* immediately remove any state from the underlying instance. State will be removed on the next instance recreation or update. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#remove_instance_state_on_destroy ComputeRegionPerInstanceConfig#remove_instance_state_on_destroy}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#timeouts ComputeRegionPerInstanceConfig#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(preserved_state, dict):
            preserved_state = ComputeRegionPerInstanceConfigPreservedState(**preserved_state)
        if isinstance(timeouts, dict):
            timeouts = ComputeRegionPerInstanceConfigTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b53754ff16f749d2f6de541ea9476c9ccfbcf2722d58ea149e0512ba6ad3719c)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument region_instance_group_manager", value=region_instance_group_manager, expected_type=type_hints["region_instance_group_manager"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument minimal_action", value=minimal_action, expected_type=type_hints["minimal_action"])
            check_type(argname="argument most_disruptive_allowed_action", value=most_disruptive_allowed_action, expected_type=type_hints["most_disruptive_allowed_action"])
            check_type(argname="argument preserved_state", value=preserved_state, expected_type=type_hints["preserved_state"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument remove_instance_on_destroy", value=remove_instance_on_destroy, expected_type=type_hints["remove_instance_on_destroy"])
            check_type(argname="argument remove_instance_state_on_destroy", value=remove_instance_state_on_destroy, expected_type=type_hints["remove_instance_state_on_destroy"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "region_instance_group_manager": region_instance_group_manager,
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
        if id is not None:
            self._values["id"] = id
        if minimal_action is not None:
            self._values["minimal_action"] = minimal_action
        if most_disruptive_allowed_action is not None:
            self._values["most_disruptive_allowed_action"] = most_disruptive_allowed_action
        if preserved_state is not None:
            self._values["preserved_state"] = preserved_state
        if project is not None:
            self._values["project"] = project
        if region is not None:
            self._values["region"] = region
        if remove_instance_on_destroy is not None:
            self._values["remove_instance_on_destroy"] = remove_instance_on_destroy
        if remove_instance_state_on_destroy is not None:
            self._values["remove_instance_state_on_destroy"] = remove_instance_state_on_destroy
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
        '''The name for this per-instance config and its corresponding instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#name ComputeRegionPerInstanceConfig#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def region_instance_group_manager(self) -> builtins.str:
        '''The region instance group manager this instance config is part of.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#region_instance_group_manager ComputeRegionPerInstanceConfig#region_instance_group_manager}
        '''
        result = self._values.get("region_instance_group_manager")
        assert result is not None, "Required property 'region_instance_group_manager' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#id ComputeRegionPerInstanceConfig#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def minimal_action(self) -> typing.Optional[builtins.str]:
        '''The minimal action to perform on the instance during an update.

        Default is 'NONE'. Possible values are:

        - REPLACE
        - RESTART
        - REFRESH
        - NONE

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#minimal_action ComputeRegionPerInstanceConfig#minimal_action}
        '''
        result = self._values.get("minimal_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def most_disruptive_allowed_action(self) -> typing.Optional[builtins.str]:
        '''The most disruptive action to perform on the instance during an update.

        Default is 'REPLACE'. Possible values are:

        - REPLACE
        - RESTART
        - REFRESH
        - NONE

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#most_disruptive_allowed_action ComputeRegionPerInstanceConfig#most_disruptive_allowed_action}
        '''
        result = self._values.get("most_disruptive_allowed_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preserved_state(
        self,
    ) -> typing.Optional["ComputeRegionPerInstanceConfigPreservedState"]:
        '''preserved_state block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#preserved_state ComputeRegionPerInstanceConfig#preserved_state}
        '''
        result = self._values.get("preserved_state")
        return typing.cast(typing.Optional["ComputeRegionPerInstanceConfigPreservedState"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#project ComputeRegionPerInstanceConfig#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where the containing instance group manager is located.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#region ComputeRegionPerInstanceConfig#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remove_instance_on_destroy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When true, deleting this config will immediately remove the underlying instance.

        When false, deleting this config will use the behavior as determined by remove_instance_on_destroy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#remove_instance_on_destroy ComputeRegionPerInstanceConfig#remove_instance_on_destroy}
        '''
        result = self._values.get("remove_instance_on_destroy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def remove_instance_state_on_destroy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When true, deleting this config will immediately remove any specified state from the underlying instance.

        When false, deleting this config will *not* immediately remove any state from the underlying instance.
        State will be removed on the next instance recreation or update.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#remove_instance_state_on_destroy ComputeRegionPerInstanceConfig#remove_instance_state_on_destroy}
        '''
        result = self._values.get("remove_instance_state_on_destroy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ComputeRegionPerInstanceConfigTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#timeouts ComputeRegionPerInstanceConfig#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ComputeRegionPerInstanceConfigTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionPerInstanceConfigConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionPerInstanceConfig.ComputeRegionPerInstanceConfigPreservedState",
    jsii_struct_bases=[],
    name_mapping={
        "disk": "disk",
        "external_ip": "externalIp",
        "internal_ip": "internalIp",
        "metadata": "metadata",
    },
)
class ComputeRegionPerInstanceConfigPreservedState:
    def __init__(
        self,
        *,
        disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionPerInstanceConfigPreservedStateDisk", typing.Dict[builtins.str, typing.Any]]]]] = None,
        external_ip: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionPerInstanceConfigPreservedStateExternalIp", typing.Dict[builtins.str, typing.Any]]]]] = None,
        internal_ip: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionPerInstanceConfigPreservedStateInternalIp", typing.Dict[builtins.str, typing.Any]]]]] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param disk: disk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#disk ComputeRegionPerInstanceConfig#disk}
        :param external_ip: external_ip block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#external_ip ComputeRegionPerInstanceConfig#external_ip}
        :param internal_ip: internal_ip block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#internal_ip ComputeRegionPerInstanceConfig#internal_ip}
        :param metadata: Preserved metadata defined for this instance. This is a list of key->value pairs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#metadata ComputeRegionPerInstanceConfig#metadata}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9bb7d8802853c6db61881d42f7db9768fe1b56c02ba10b6d558b956716cf1d6)
            check_type(argname="argument disk", value=disk, expected_type=type_hints["disk"])
            check_type(argname="argument external_ip", value=external_ip, expected_type=type_hints["external_ip"])
            check_type(argname="argument internal_ip", value=internal_ip, expected_type=type_hints["internal_ip"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if disk is not None:
            self._values["disk"] = disk
        if external_ip is not None:
            self._values["external_ip"] = external_ip
        if internal_ip is not None:
            self._values["internal_ip"] = internal_ip
        if metadata is not None:
            self._values["metadata"] = metadata

    @builtins.property
    def disk(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionPerInstanceConfigPreservedStateDisk"]]]:
        '''disk block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#disk ComputeRegionPerInstanceConfig#disk}
        '''
        result = self._values.get("disk")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionPerInstanceConfigPreservedStateDisk"]]], result)

    @builtins.property
    def external_ip(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionPerInstanceConfigPreservedStateExternalIp"]]]:
        '''external_ip block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#external_ip ComputeRegionPerInstanceConfig#external_ip}
        '''
        result = self._values.get("external_ip")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionPerInstanceConfigPreservedStateExternalIp"]]], result)

    @builtins.property
    def internal_ip(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionPerInstanceConfigPreservedStateInternalIp"]]]:
        '''internal_ip block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#internal_ip ComputeRegionPerInstanceConfig#internal_ip}
        '''
        result = self._values.get("internal_ip")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionPerInstanceConfigPreservedStateInternalIp"]]], result)

    @builtins.property
    def metadata(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Preserved metadata defined for this instance. This is a list of key->value pairs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#metadata ComputeRegionPerInstanceConfig#metadata}
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionPerInstanceConfigPreservedState(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionPerInstanceConfig.ComputeRegionPerInstanceConfigPreservedStateDisk",
    jsii_struct_bases=[],
    name_mapping={
        "device_name": "deviceName",
        "source": "source",
        "delete_rule": "deleteRule",
        "mode": "mode",
    },
)
class ComputeRegionPerInstanceConfigPreservedStateDisk:
    def __init__(
        self,
        *,
        device_name: builtins.str,
        source: builtins.str,
        delete_rule: typing.Optional[builtins.str] = None,
        mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param device_name: A unique device name that is reflected into the /dev/ tree of a Linux operating system running within the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#device_name ComputeRegionPerInstanceConfig#device_name}
        :param source: The URI of an existing persistent disk to attach under the specified device-name in the format 'projects/project-id/zones/zone/disks/disk-name'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#source ComputeRegionPerInstanceConfig#source}
        :param delete_rule: A value that prescribes what should happen to the stateful disk when the VM instance is deleted. The available options are 'NEVER' and 'ON_PERMANENT_INSTANCE_DELETION'. 'NEVER' - detach the disk when the VM is deleted, but do not delete the disk. 'ON_PERMANENT_INSTANCE_DELETION' will delete the stateful disk when the VM is permanently deleted from the instance group. Default value: "NEVER" Possible values: ["NEVER", "ON_PERMANENT_INSTANCE_DELETION"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#delete_rule ComputeRegionPerInstanceConfig#delete_rule}
        :param mode: The mode of the disk. Default value: "READ_WRITE" Possible values: ["READ_ONLY", "READ_WRITE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#mode ComputeRegionPerInstanceConfig#mode}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89ad95f010b05961a7a4ac5434319ea7626e4b00e8be99b762bf41695dea5fd9)
            check_type(argname="argument device_name", value=device_name, expected_type=type_hints["device_name"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument delete_rule", value=delete_rule, expected_type=type_hints["delete_rule"])
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "device_name": device_name,
            "source": source,
        }
        if delete_rule is not None:
            self._values["delete_rule"] = delete_rule
        if mode is not None:
            self._values["mode"] = mode

    @builtins.property
    def device_name(self) -> builtins.str:
        '''A unique device name that is reflected into the /dev/ tree of a Linux operating system running within the instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#device_name ComputeRegionPerInstanceConfig#device_name}
        '''
        result = self._values.get("device_name")
        assert result is not None, "Required property 'device_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source(self) -> builtins.str:
        '''The URI of an existing persistent disk to attach under the specified device-name in the format 'projects/project-id/zones/zone/disks/disk-name'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#source ComputeRegionPerInstanceConfig#source}
        '''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def delete_rule(self) -> typing.Optional[builtins.str]:
        '''A value that prescribes what should happen to the stateful disk when the VM instance is deleted.

        The available options are 'NEVER' and 'ON_PERMANENT_INSTANCE_DELETION'.
        'NEVER' - detach the disk when the VM is deleted, but do not delete the disk.
        'ON_PERMANENT_INSTANCE_DELETION' will delete the stateful disk when the VM is permanently
        deleted from the instance group. Default value: "NEVER" Possible values: ["NEVER", "ON_PERMANENT_INSTANCE_DELETION"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#delete_rule ComputeRegionPerInstanceConfig#delete_rule}
        '''
        result = self._values.get("delete_rule")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''The mode of the disk. Default value: "READ_WRITE" Possible values: ["READ_ONLY", "READ_WRITE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#mode ComputeRegionPerInstanceConfig#mode}
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionPerInstanceConfigPreservedStateDisk(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionPerInstanceConfigPreservedStateDiskList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionPerInstanceConfig.ComputeRegionPerInstanceConfigPreservedStateDiskList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__67130bdfe09826a986c27c9364bcca7d17823991e3c2ef60e6e44953cd4ff8fd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeRegionPerInstanceConfigPreservedStateDiskOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57fdb93cb9da5a4e0dd76d3251fe24b2ecf494552882751a324bb3129adb7918)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeRegionPerInstanceConfigPreservedStateDiskOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e97ef6b44bd74550678bf8d22740fe8bcca48ff69558a8551f230eea89bf4169)
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
            type_hints = typing.get_type_hints(_typecheckingstub__def7b4427ec6e1ae8d2cbe7639ca6956ba2671839810bd2c0b3cf6e8a4bfb470)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d7a37d440e74a78b0781b2ff7095bb3cd8aa0e129eac039265376a20a09b8776)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionPerInstanceConfigPreservedStateDisk]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionPerInstanceConfigPreservedStateDisk]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionPerInstanceConfigPreservedStateDisk]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a4cc0d6652da29d3e382769068f2b56634f409ed80417369f27c6c985ad4a91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRegionPerInstanceConfigPreservedStateDiskOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionPerInstanceConfig.ComputeRegionPerInstanceConfigPreservedStateDiskOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c94597de2c936f6d10de02269a6f04f4dc9a7698fb70fc19eff6b65eb968f19c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDeleteRule")
    def reset_delete_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeleteRule", []))

    @jsii.member(jsii_name="resetMode")
    def reset_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMode", []))

    @builtins.property
    @jsii.member(jsii_name="deleteRuleInput")
    def delete_rule_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="deviceNameInput")
    def device_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deviceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteRule")
    def delete_rule(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deleteRule"))

    @delete_rule.setter
    def delete_rule(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__febf33509f861a068d3219f56c9701aa6d869d413bed627e74e4c5a75895f772)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deleteRule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deviceName")
    def device_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deviceName"))

    @device_name.setter
    def device_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__916ee8557a44372fbcccf84a8b28ff31f80f813c9b903906c45d53b19a087d7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deviceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__642d0ca8effb9feb7bee78c484b4194577dd68be44cbc1900c044effba5a906f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6367248e161cb3684d3a48c243b75df8c79e5b03339957c04d8c5cd794355433)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionPerInstanceConfigPreservedStateDisk]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionPerInstanceConfigPreservedStateDisk]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionPerInstanceConfigPreservedStateDisk]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b4561caa7f99cf896d8fbab2529be04ae3b5584ad3af06bd4b5bb9e0235aa04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionPerInstanceConfig.ComputeRegionPerInstanceConfigPreservedStateExternalIp",
    jsii_struct_bases=[],
    name_mapping={
        "interface_name": "interfaceName",
        "auto_delete": "autoDelete",
        "ip_address": "ipAddress",
    },
)
class ComputeRegionPerInstanceConfigPreservedStateExternalIp:
    def __init__(
        self,
        *,
        interface_name: builtins.str,
        auto_delete: typing.Optional[builtins.str] = None,
        ip_address: typing.Optional[typing.Union["ComputeRegionPerInstanceConfigPreservedStateExternalIpIpAddress", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param interface_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#interface_name ComputeRegionPerInstanceConfig#interface_name}.
        :param auto_delete: These stateful IPs will never be released during autohealing, update or VM instance recreate operations. This flag is used to configure if the IP reservation should be deleted after it is no longer used by the group, e.g. when the given instance or the whole group is deleted. Default value: "NEVER" Possible values: ["NEVER", "ON_PERMANENT_INSTANCE_DELETION"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#auto_delete ComputeRegionPerInstanceConfig#auto_delete}
        :param ip_address: ip_address block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#ip_address ComputeRegionPerInstanceConfig#ip_address}
        '''
        if isinstance(ip_address, dict):
            ip_address = ComputeRegionPerInstanceConfigPreservedStateExternalIpIpAddress(**ip_address)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2704754efbd6726fc88db0a505a2ec49715d4972c5e163c1791e963bb1f5659a)
            check_type(argname="argument interface_name", value=interface_name, expected_type=type_hints["interface_name"])
            check_type(argname="argument auto_delete", value=auto_delete, expected_type=type_hints["auto_delete"])
            check_type(argname="argument ip_address", value=ip_address, expected_type=type_hints["ip_address"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "interface_name": interface_name,
        }
        if auto_delete is not None:
            self._values["auto_delete"] = auto_delete
        if ip_address is not None:
            self._values["ip_address"] = ip_address

    @builtins.property
    def interface_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#interface_name ComputeRegionPerInstanceConfig#interface_name}.'''
        result = self._values.get("interface_name")
        assert result is not None, "Required property 'interface_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auto_delete(self) -> typing.Optional[builtins.str]:
        '''These stateful IPs will never be released during autohealing, update or VM instance recreate operations.

        This flag is used to configure if the IP reservation should be deleted after it is no longer used by the group, e.g. when the given instance or the whole group is deleted. Default value: "NEVER" Possible values: ["NEVER", "ON_PERMANENT_INSTANCE_DELETION"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#auto_delete ComputeRegionPerInstanceConfig#auto_delete}
        '''
        result = self._values.get("auto_delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_address(
        self,
    ) -> typing.Optional["ComputeRegionPerInstanceConfigPreservedStateExternalIpIpAddress"]:
        '''ip_address block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#ip_address ComputeRegionPerInstanceConfig#ip_address}
        '''
        result = self._values.get("ip_address")
        return typing.cast(typing.Optional["ComputeRegionPerInstanceConfigPreservedStateExternalIpIpAddress"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionPerInstanceConfigPreservedStateExternalIp(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionPerInstanceConfig.ComputeRegionPerInstanceConfigPreservedStateExternalIpIpAddress",
    jsii_struct_bases=[],
    name_mapping={"address": "address"},
)
class ComputeRegionPerInstanceConfigPreservedStateExternalIpIpAddress:
    def __init__(self, *, address: typing.Optional[builtins.str] = None) -> None:
        '''
        :param address: The URL of the reservation for this IP address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#address ComputeRegionPerInstanceConfig#address}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb145ae8e4f37d10de0cfc078052fae10bf5909cc296ad9198b04f57730df2cb)
            check_type(argname="argument address", value=address, expected_type=type_hints["address"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if address is not None:
            self._values["address"] = address

    @builtins.property
    def address(self) -> typing.Optional[builtins.str]:
        '''The URL of the reservation for this IP address.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#address ComputeRegionPerInstanceConfig#address}
        '''
        result = self._values.get("address")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionPerInstanceConfigPreservedStateExternalIpIpAddress(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionPerInstanceConfigPreservedStateExternalIpIpAddressOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionPerInstanceConfig.ComputeRegionPerInstanceConfigPreservedStateExternalIpIpAddressOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a6461cc8a16a14ec905380eda16281ccada37b02b6d4dccf38def2096f1209c8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAddress")
    def reset_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddress", []))

    @builtins.property
    @jsii.member(jsii_name="addressInput")
    def address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "addressInput"))

    @builtins.property
    @jsii.member(jsii_name="address")
    def address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address"))

    @address.setter
    def address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52bd066cb821df59b09d4403fc752b38de6bd1b200888937e23e7bd4b3172da7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeRegionPerInstanceConfigPreservedStateExternalIpIpAddress]:
        return typing.cast(typing.Optional[ComputeRegionPerInstanceConfigPreservedStateExternalIpIpAddress], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionPerInstanceConfigPreservedStateExternalIpIpAddress],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b47ad898b4c84bff2bd373dd120644d9f801b44d8d66b319a61fe1c52a7dfd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRegionPerInstanceConfigPreservedStateExternalIpList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionPerInstanceConfig.ComputeRegionPerInstanceConfigPreservedStateExternalIpList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__59e6e47fe747a82d75bfa046514140a29330198a4f7872f70dd2844676f05588)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeRegionPerInstanceConfigPreservedStateExternalIpOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f05a4491b023a97e404bc205cc372009141a9f936f2228d7512c4d47083490b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeRegionPerInstanceConfigPreservedStateExternalIpOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__014585ba5373772362188ccbfe48d3ddc5866c8717995f053c92929af800462b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d1d8037e3dcc886b13067cecb1c3ad9887b26966b11bc598e1f48dc057ad23bf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ccca257b8df27e3b5cf974fce77610a6837d2ef6680577f53cf2f3af14a796bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionPerInstanceConfigPreservedStateExternalIp]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionPerInstanceConfigPreservedStateExternalIp]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionPerInstanceConfigPreservedStateExternalIp]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3b89377a102d888a8e0c82e812524e5784935f7047fa3dc8816e749e88f4d5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRegionPerInstanceConfigPreservedStateExternalIpOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionPerInstanceConfig.ComputeRegionPerInstanceConfigPreservedStateExternalIpOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b6024df91d671758d3923b7a5d42ccdd480f6dc8e3b65df5a9abc9dca37a43b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putIpAddress")
    def put_ip_address(self, *, address: typing.Optional[builtins.str] = None) -> None:
        '''
        :param address: The URL of the reservation for this IP address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#address ComputeRegionPerInstanceConfig#address}
        '''
        value = ComputeRegionPerInstanceConfigPreservedStateExternalIpIpAddress(
            address=address
        )

        return typing.cast(None, jsii.invoke(self, "putIpAddress", [value]))

    @jsii.member(jsii_name="resetAutoDelete")
    def reset_auto_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoDelete", []))

    @jsii.member(jsii_name="resetIpAddress")
    def reset_ip_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpAddress", []))

    @builtins.property
    @jsii.member(jsii_name="ipAddress")
    def ip_address(
        self,
    ) -> ComputeRegionPerInstanceConfigPreservedStateExternalIpIpAddressOutputReference:
        return typing.cast(ComputeRegionPerInstanceConfigPreservedStateExternalIpIpAddressOutputReference, jsii.get(self, "ipAddress"))

    @builtins.property
    @jsii.member(jsii_name="autoDeleteInput")
    def auto_delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "autoDeleteInput"))

    @builtins.property
    @jsii.member(jsii_name="interfaceNameInput")
    def interface_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "interfaceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="ipAddressInput")
    def ip_address_input(
        self,
    ) -> typing.Optional[ComputeRegionPerInstanceConfigPreservedStateExternalIpIpAddress]:
        return typing.cast(typing.Optional[ComputeRegionPerInstanceConfigPreservedStateExternalIpIpAddress], jsii.get(self, "ipAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="autoDelete")
    def auto_delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "autoDelete"))

    @auto_delete.setter
    def auto_delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aad4310f2e4717bf9a478d9e2febe0e0bb21f79f6b850029607c92fe4a8886cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoDelete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="interfaceName")
    def interface_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "interfaceName"))

    @interface_name.setter
    def interface_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f192f6e57704be73f31e031a51907f005cf3cd7b11b0678be665900989f5ec73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interfaceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionPerInstanceConfigPreservedStateExternalIp]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionPerInstanceConfigPreservedStateExternalIp]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionPerInstanceConfigPreservedStateExternalIp]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f3f7f55dbb4229ab303bb4116017462d300007a8ea5f1ee4e8be613de80712d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionPerInstanceConfig.ComputeRegionPerInstanceConfigPreservedStateInternalIp",
    jsii_struct_bases=[],
    name_mapping={
        "interface_name": "interfaceName",
        "auto_delete": "autoDelete",
        "ip_address": "ipAddress",
    },
)
class ComputeRegionPerInstanceConfigPreservedStateInternalIp:
    def __init__(
        self,
        *,
        interface_name: builtins.str,
        auto_delete: typing.Optional[builtins.str] = None,
        ip_address: typing.Optional[typing.Union["ComputeRegionPerInstanceConfigPreservedStateInternalIpIpAddress", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param interface_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#interface_name ComputeRegionPerInstanceConfig#interface_name}.
        :param auto_delete: These stateful IPs will never be released during autohealing, update or VM instance recreate operations. This flag is used to configure if the IP reservation should be deleted after it is no longer used by the group, e.g. when the given instance or the whole group is deleted. Default value: "NEVER" Possible values: ["NEVER", "ON_PERMANENT_INSTANCE_DELETION"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#auto_delete ComputeRegionPerInstanceConfig#auto_delete}
        :param ip_address: ip_address block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#ip_address ComputeRegionPerInstanceConfig#ip_address}
        '''
        if isinstance(ip_address, dict):
            ip_address = ComputeRegionPerInstanceConfigPreservedStateInternalIpIpAddress(**ip_address)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd16f2368e3b427066ecc2ccd0130c6bcf973d67d4c9dcc9f1cd5a9786d4114a)
            check_type(argname="argument interface_name", value=interface_name, expected_type=type_hints["interface_name"])
            check_type(argname="argument auto_delete", value=auto_delete, expected_type=type_hints["auto_delete"])
            check_type(argname="argument ip_address", value=ip_address, expected_type=type_hints["ip_address"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "interface_name": interface_name,
        }
        if auto_delete is not None:
            self._values["auto_delete"] = auto_delete
        if ip_address is not None:
            self._values["ip_address"] = ip_address

    @builtins.property
    def interface_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#interface_name ComputeRegionPerInstanceConfig#interface_name}.'''
        result = self._values.get("interface_name")
        assert result is not None, "Required property 'interface_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auto_delete(self) -> typing.Optional[builtins.str]:
        '''These stateful IPs will never be released during autohealing, update or VM instance recreate operations.

        This flag is used to configure if the IP reservation should be deleted after it is no longer used by the group, e.g. when the given instance or the whole group is deleted. Default value: "NEVER" Possible values: ["NEVER", "ON_PERMANENT_INSTANCE_DELETION"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#auto_delete ComputeRegionPerInstanceConfig#auto_delete}
        '''
        result = self._values.get("auto_delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_address(
        self,
    ) -> typing.Optional["ComputeRegionPerInstanceConfigPreservedStateInternalIpIpAddress"]:
        '''ip_address block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#ip_address ComputeRegionPerInstanceConfig#ip_address}
        '''
        result = self._values.get("ip_address")
        return typing.cast(typing.Optional["ComputeRegionPerInstanceConfigPreservedStateInternalIpIpAddress"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionPerInstanceConfigPreservedStateInternalIp(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionPerInstanceConfig.ComputeRegionPerInstanceConfigPreservedStateInternalIpIpAddress",
    jsii_struct_bases=[],
    name_mapping={"address": "address"},
)
class ComputeRegionPerInstanceConfigPreservedStateInternalIpIpAddress:
    def __init__(self, *, address: typing.Optional[builtins.str] = None) -> None:
        '''
        :param address: The URL of the reservation for this IP address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#address ComputeRegionPerInstanceConfig#address}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eba6c5e2780835d29b1ad97c7e6a39ce322b684ef3fcdd90fc9fb358e33bb85e)
            check_type(argname="argument address", value=address, expected_type=type_hints["address"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if address is not None:
            self._values["address"] = address

    @builtins.property
    def address(self) -> typing.Optional[builtins.str]:
        '''The URL of the reservation for this IP address.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#address ComputeRegionPerInstanceConfig#address}
        '''
        result = self._values.get("address")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionPerInstanceConfigPreservedStateInternalIpIpAddress(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionPerInstanceConfigPreservedStateInternalIpIpAddressOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionPerInstanceConfig.ComputeRegionPerInstanceConfigPreservedStateInternalIpIpAddressOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b79fd7b10a5f447f8150e95d38380d6977f55de3ab3a690f474cee1e43b2bac)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAddress")
    def reset_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddress", []))

    @builtins.property
    @jsii.member(jsii_name="addressInput")
    def address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "addressInput"))

    @builtins.property
    @jsii.member(jsii_name="address")
    def address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address"))

    @address.setter
    def address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4dfd7e9a9ceace042e7b9ed7f4266f5b22be78f6cdf26950f3f9a69ecaafa16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeRegionPerInstanceConfigPreservedStateInternalIpIpAddress]:
        return typing.cast(typing.Optional[ComputeRegionPerInstanceConfigPreservedStateInternalIpIpAddress], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionPerInstanceConfigPreservedStateInternalIpIpAddress],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3887c4e26234d0dedfdd0df4cd4aaa362dc18ae4d5213b79b6cff40cc8b8688)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRegionPerInstanceConfigPreservedStateInternalIpList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionPerInstanceConfig.ComputeRegionPerInstanceConfigPreservedStateInternalIpList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__75ecd56fbda5d4c771d766196b1711e52f32a0e2959198dc9e5a2874c30ddf6d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeRegionPerInstanceConfigPreservedStateInternalIpOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c942404586bd383b327c35d39d4265339c10b5e3ea65090294185790c2d7aba)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeRegionPerInstanceConfigPreservedStateInternalIpOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7219ef87c230288821740286c76e82386b254f2dc6e3c8edcb656174c847a954)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e3d6f4ca508161aef7864885fcc1300b7a8433773ea4b6b12d48ea49825e2cfe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1fc9cd514060ce660a28466ad32a12a493853606d18823382f1750bf99f2e72d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionPerInstanceConfigPreservedStateInternalIp]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionPerInstanceConfigPreservedStateInternalIp]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionPerInstanceConfigPreservedStateInternalIp]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b370673d6f2a90d7f459efe578e0e65969b7a1022a021ac10f31a9ebab66707)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRegionPerInstanceConfigPreservedStateInternalIpOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionPerInstanceConfig.ComputeRegionPerInstanceConfigPreservedStateInternalIpOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8441bde2d4fadf4fe9b3a9a782d7f4bd32a1da9225f8b42e3f7094a57eea08f8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putIpAddress")
    def put_ip_address(self, *, address: typing.Optional[builtins.str] = None) -> None:
        '''
        :param address: The URL of the reservation for this IP address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#address ComputeRegionPerInstanceConfig#address}
        '''
        value = ComputeRegionPerInstanceConfigPreservedStateInternalIpIpAddress(
            address=address
        )

        return typing.cast(None, jsii.invoke(self, "putIpAddress", [value]))

    @jsii.member(jsii_name="resetAutoDelete")
    def reset_auto_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoDelete", []))

    @jsii.member(jsii_name="resetIpAddress")
    def reset_ip_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpAddress", []))

    @builtins.property
    @jsii.member(jsii_name="ipAddress")
    def ip_address(
        self,
    ) -> ComputeRegionPerInstanceConfigPreservedStateInternalIpIpAddressOutputReference:
        return typing.cast(ComputeRegionPerInstanceConfigPreservedStateInternalIpIpAddressOutputReference, jsii.get(self, "ipAddress"))

    @builtins.property
    @jsii.member(jsii_name="autoDeleteInput")
    def auto_delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "autoDeleteInput"))

    @builtins.property
    @jsii.member(jsii_name="interfaceNameInput")
    def interface_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "interfaceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="ipAddressInput")
    def ip_address_input(
        self,
    ) -> typing.Optional[ComputeRegionPerInstanceConfigPreservedStateInternalIpIpAddress]:
        return typing.cast(typing.Optional[ComputeRegionPerInstanceConfigPreservedStateInternalIpIpAddress], jsii.get(self, "ipAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="autoDelete")
    def auto_delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "autoDelete"))

    @auto_delete.setter
    def auto_delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf53fa27ced52dd2f5bf7f1486c28967f59b40009b46c5eb79e9483705b267a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoDelete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="interfaceName")
    def interface_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "interfaceName"))

    @interface_name.setter
    def interface_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea8c1f4fe8f534ad3f92575329cf58a369e5e67edbfa593e195aace05c7bc88a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interfaceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionPerInstanceConfigPreservedStateInternalIp]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionPerInstanceConfigPreservedStateInternalIp]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionPerInstanceConfigPreservedStateInternalIp]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74e9420862a93f9a64f0e75e2654f7bb841dd7d7992256924c560fedeef0eac7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRegionPerInstanceConfigPreservedStateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionPerInstanceConfig.ComputeRegionPerInstanceConfigPreservedStateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f4bfdb9d761f510c9dc62185e9b0bdd0bb89f6a6abcfaadcceedf96f5ee5177e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDisk")
    def put_disk(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionPerInstanceConfigPreservedStateDisk, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddc840fc1d58916d21722a290cafa470777ea76b3d7674b8a995b2d3f70e226e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDisk", [value]))

    @jsii.member(jsii_name="putExternalIp")
    def put_external_ip(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionPerInstanceConfigPreservedStateExternalIp, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d289b16ad914bd0387331f47a4d8b3d6999298a610301de90fe15fa9839283a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putExternalIp", [value]))

    @jsii.member(jsii_name="putInternalIp")
    def put_internal_ip(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionPerInstanceConfigPreservedStateInternalIp, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93d069662a07b2e17fc51adf6e62fb0e20563a278b2ee48195f3be51a94e156e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInternalIp", [value]))

    @jsii.member(jsii_name="resetDisk")
    def reset_disk(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisk", []))

    @jsii.member(jsii_name="resetExternalIp")
    def reset_external_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalIp", []))

    @jsii.member(jsii_name="resetInternalIp")
    def reset_internal_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInternalIp", []))

    @jsii.member(jsii_name="resetMetadata")
    def reset_metadata(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetadata", []))

    @builtins.property
    @jsii.member(jsii_name="disk")
    def disk(self) -> ComputeRegionPerInstanceConfigPreservedStateDiskList:
        return typing.cast(ComputeRegionPerInstanceConfigPreservedStateDiskList, jsii.get(self, "disk"))

    @builtins.property
    @jsii.member(jsii_name="externalIp")
    def external_ip(self) -> ComputeRegionPerInstanceConfigPreservedStateExternalIpList:
        return typing.cast(ComputeRegionPerInstanceConfigPreservedStateExternalIpList, jsii.get(self, "externalIp"))

    @builtins.property
    @jsii.member(jsii_name="internalIp")
    def internal_ip(self) -> ComputeRegionPerInstanceConfigPreservedStateInternalIpList:
        return typing.cast(ComputeRegionPerInstanceConfigPreservedStateInternalIpList, jsii.get(self, "internalIp"))

    @builtins.property
    @jsii.member(jsii_name="diskInput")
    def disk_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionPerInstanceConfigPreservedStateDisk]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionPerInstanceConfigPreservedStateDisk]]], jsii.get(self, "diskInput"))

    @builtins.property
    @jsii.member(jsii_name="externalIpInput")
    def external_ip_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionPerInstanceConfigPreservedStateExternalIp]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionPerInstanceConfigPreservedStateExternalIp]]], jsii.get(self, "externalIpInput"))

    @builtins.property
    @jsii.member(jsii_name="internalIpInput")
    def internal_ip_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionPerInstanceConfigPreservedStateInternalIp]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionPerInstanceConfigPreservedStateInternalIp]]], jsii.get(self, "internalIpInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataInput")
    def metadata_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "metadataInput"))

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "metadata"))

    @metadata.setter
    def metadata(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4eeaa819a0f0ebe97236fe136ff5099756823e39632856a606eee8454c3366c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadata", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeRegionPerInstanceConfigPreservedState]:
        return typing.cast(typing.Optional[ComputeRegionPerInstanceConfigPreservedState], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionPerInstanceConfigPreservedState],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1de8fabc81cd776ea4b62373b6bb57df1afdc5d4bc3c21c004a5da36467ec67b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionPerInstanceConfig.ComputeRegionPerInstanceConfigTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ComputeRegionPerInstanceConfigTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#create ComputeRegionPerInstanceConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#delete ComputeRegionPerInstanceConfig#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#update ComputeRegionPerInstanceConfig#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d9b271f582cb8d88eefef254f79d10d0f640d0fc341658e619bab3fc772243a)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#create ComputeRegionPerInstanceConfig#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#delete ComputeRegionPerInstanceConfig#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_per_instance_config#update ComputeRegionPerInstanceConfig#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionPerInstanceConfigTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionPerInstanceConfigTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionPerInstanceConfig.ComputeRegionPerInstanceConfigTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d12dac853d1b12481326a9683c84ce28abe9db3fbf874d7ae590689ce14013c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b7b2fada7bb64f1a753db4abcf02175ea2026382afde6b06da04afcbffd48ecd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c7d79e264cd89005af6d1241c086792359647034186631569775a0988f23a1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa1cc960b7166cef3a8801a4866b92ce359450e42d99434a99f156a16c3d3cb2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionPerInstanceConfigTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionPerInstanceConfigTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionPerInstanceConfigTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5029b7bfcc76fe16d86990a4a4293064710b86a0e62b97777cececf03de9a7f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ComputeRegionPerInstanceConfig",
    "ComputeRegionPerInstanceConfigConfig",
    "ComputeRegionPerInstanceConfigPreservedState",
    "ComputeRegionPerInstanceConfigPreservedStateDisk",
    "ComputeRegionPerInstanceConfigPreservedStateDiskList",
    "ComputeRegionPerInstanceConfigPreservedStateDiskOutputReference",
    "ComputeRegionPerInstanceConfigPreservedStateExternalIp",
    "ComputeRegionPerInstanceConfigPreservedStateExternalIpIpAddress",
    "ComputeRegionPerInstanceConfigPreservedStateExternalIpIpAddressOutputReference",
    "ComputeRegionPerInstanceConfigPreservedStateExternalIpList",
    "ComputeRegionPerInstanceConfigPreservedStateExternalIpOutputReference",
    "ComputeRegionPerInstanceConfigPreservedStateInternalIp",
    "ComputeRegionPerInstanceConfigPreservedStateInternalIpIpAddress",
    "ComputeRegionPerInstanceConfigPreservedStateInternalIpIpAddressOutputReference",
    "ComputeRegionPerInstanceConfigPreservedStateInternalIpList",
    "ComputeRegionPerInstanceConfigPreservedStateInternalIpOutputReference",
    "ComputeRegionPerInstanceConfigPreservedStateOutputReference",
    "ComputeRegionPerInstanceConfigTimeouts",
    "ComputeRegionPerInstanceConfigTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__4d3b4c07428889bc8bdc1f6d7e2a896449f9d80cc100b154cd57ab99f8546a67(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    region_instance_group_manager: builtins.str,
    id: typing.Optional[builtins.str] = None,
    minimal_action: typing.Optional[builtins.str] = None,
    most_disruptive_allowed_action: typing.Optional[builtins.str] = None,
    preserved_state: typing.Optional[typing.Union[ComputeRegionPerInstanceConfigPreservedState, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    remove_instance_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    remove_instance_state_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[ComputeRegionPerInstanceConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__0ab695e211ebf6f4fd605b5272ff852b4deb8ac528a9daa5d31a0805e6ad8d15(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d08cf10da58fd57ee45c96187f5058b73d34b1895a5077e70345ba5402aeb6ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efb5b1a0acdb9d81e39748900f0ecd7305d712de7024fd4a3d3076dbfdc52231(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ed547a811601086f7bd8bb3e49e80e12df0977d23492347d3daba35f16f4c57(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__316037137149f156a1017027a83aae75d90c9d1499999025a55b848d8613dc9f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3aeac401bd2343fed7777645fa045f446249ce71a8648c7e7aae4914c5333b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7871ecee2b3d696057d8891209e45e79f640adeeb0e7b26e3fd7193ebdc920cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0af3dfbc2e843c5ea55fb0b5920b8a0b651bf4b933050cb1066a86cf1cef8c83(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d84930e55443aa748fe11e21d3cba1250bbe0a279415aca75f9aaa8c3433d61(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de203a0bdfd48efd6332900a2db243919e50922bcf70a29085ee08553499f8af(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b53754ff16f749d2f6de541ea9476c9ccfbcf2722d58ea149e0512ba6ad3719c(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    region_instance_group_manager: builtins.str,
    id: typing.Optional[builtins.str] = None,
    minimal_action: typing.Optional[builtins.str] = None,
    most_disruptive_allowed_action: typing.Optional[builtins.str] = None,
    preserved_state: typing.Optional[typing.Union[ComputeRegionPerInstanceConfigPreservedState, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    remove_instance_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    remove_instance_state_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[ComputeRegionPerInstanceConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9bb7d8802853c6db61881d42f7db9768fe1b56c02ba10b6d558b956716cf1d6(
    *,
    disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionPerInstanceConfigPreservedStateDisk, typing.Dict[builtins.str, typing.Any]]]]] = None,
    external_ip: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionPerInstanceConfigPreservedStateExternalIp, typing.Dict[builtins.str, typing.Any]]]]] = None,
    internal_ip: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionPerInstanceConfigPreservedStateInternalIp, typing.Dict[builtins.str, typing.Any]]]]] = None,
    metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89ad95f010b05961a7a4ac5434319ea7626e4b00e8be99b762bf41695dea5fd9(
    *,
    device_name: builtins.str,
    source: builtins.str,
    delete_rule: typing.Optional[builtins.str] = None,
    mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67130bdfe09826a986c27c9364bcca7d17823991e3c2ef60e6e44953cd4ff8fd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57fdb93cb9da5a4e0dd76d3251fe24b2ecf494552882751a324bb3129adb7918(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e97ef6b44bd74550678bf8d22740fe8bcca48ff69558a8551f230eea89bf4169(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__def7b4427ec6e1ae8d2cbe7639ca6956ba2671839810bd2c0b3cf6e8a4bfb470(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7a37d440e74a78b0781b2ff7095bb3cd8aa0e129eac039265376a20a09b8776(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a4cc0d6652da29d3e382769068f2b56634f409ed80417369f27c6c985ad4a91(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionPerInstanceConfigPreservedStateDisk]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c94597de2c936f6d10de02269a6f04f4dc9a7698fb70fc19eff6b65eb968f19c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__febf33509f861a068d3219f56c9701aa6d869d413bed627e74e4c5a75895f772(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__916ee8557a44372fbcccf84a8b28ff31f80f813c9b903906c45d53b19a087d7b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__642d0ca8effb9feb7bee78c484b4194577dd68be44cbc1900c044effba5a906f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6367248e161cb3684d3a48c243b75df8c79e5b03339957c04d8c5cd794355433(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b4561caa7f99cf896d8fbab2529be04ae3b5584ad3af06bd4b5bb9e0235aa04(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionPerInstanceConfigPreservedStateDisk]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2704754efbd6726fc88db0a505a2ec49715d4972c5e163c1791e963bb1f5659a(
    *,
    interface_name: builtins.str,
    auto_delete: typing.Optional[builtins.str] = None,
    ip_address: typing.Optional[typing.Union[ComputeRegionPerInstanceConfigPreservedStateExternalIpIpAddress, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb145ae8e4f37d10de0cfc078052fae10bf5909cc296ad9198b04f57730df2cb(
    *,
    address: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6461cc8a16a14ec905380eda16281ccada37b02b6d4dccf38def2096f1209c8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52bd066cb821df59b09d4403fc752b38de6bd1b200888937e23e7bd4b3172da7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b47ad898b4c84bff2bd373dd120644d9f801b44d8d66b319a61fe1c52a7dfd8(
    value: typing.Optional[ComputeRegionPerInstanceConfigPreservedStateExternalIpIpAddress],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59e6e47fe747a82d75bfa046514140a29330198a4f7872f70dd2844676f05588(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f05a4491b023a97e404bc205cc372009141a9f936f2228d7512c4d47083490b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__014585ba5373772362188ccbfe48d3ddc5866c8717995f053c92929af800462b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1d8037e3dcc886b13067cecb1c3ad9887b26966b11bc598e1f48dc057ad23bf(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccca257b8df27e3b5cf974fce77610a6837d2ef6680577f53cf2f3af14a796bb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3b89377a102d888a8e0c82e812524e5784935f7047fa3dc8816e749e88f4d5a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionPerInstanceConfigPreservedStateExternalIp]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b6024df91d671758d3923b7a5d42ccdd480f6dc8e3b65df5a9abc9dca37a43b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aad4310f2e4717bf9a478d9e2febe0e0bb21f79f6b850029607c92fe4a8886cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f192f6e57704be73f31e031a51907f005cf3cd7b11b0678be665900989f5ec73(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f3f7f55dbb4229ab303bb4116017462d300007a8ea5f1ee4e8be613de80712d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionPerInstanceConfigPreservedStateExternalIp]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd16f2368e3b427066ecc2ccd0130c6bcf973d67d4c9dcc9f1cd5a9786d4114a(
    *,
    interface_name: builtins.str,
    auto_delete: typing.Optional[builtins.str] = None,
    ip_address: typing.Optional[typing.Union[ComputeRegionPerInstanceConfigPreservedStateInternalIpIpAddress, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eba6c5e2780835d29b1ad97c7e6a39ce322b684ef3fcdd90fc9fb358e33bb85e(
    *,
    address: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b79fd7b10a5f447f8150e95d38380d6977f55de3ab3a690f474cee1e43b2bac(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4dfd7e9a9ceace042e7b9ed7f4266f5b22be78f6cdf26950f3f9a69ecaafa16(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3887c4e26234d0dedfdd0df4cd4aaa362dc18ae4d5213b79b6cff40cc8b8688(
    value: typing.Optional[ComputeRegionPerInstanceConfigPreservedStateInternalIpIpAddress],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75ecd56fbda5d4c771d766196b1711e52f32a0e2959198dc9e5a2874c30ddf6d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c942404586bd383b327c35d39d4265339c10b5e3ea65090294185790c2d7aba(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7219ef87c230288821740286c76e82386b254f2dc6e3c8edcb656174c847a954(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3d6f4ca508161aef7864885fcc1300b7a8433773ea4b6b12d48ea49825e2cfe(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fc9cd514060ce660a28466ad32a12a493853606d18823382f1750bf99f2e72d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b370673d6f2a90d7f459efe578e0e65969b7a1022a021ac10f31a9ebab66707(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionPerInstanceConfigPreservedStateInternalIp]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8441bde2d4fadf4fe9b3a9a782d7f4bd32a1da9225f8b42e3f7094a57eea08f8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf53fa27ced52dd2f5bf7f1486c28967f59b40009b46c5eb79e9483705b267a4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea8c1f4fe8f534ad3f92575329cf58a369e5e67edbfa593e195aace05c7bc88a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74e9420862a93f9a64f0e75e2654f7bb841dd7d7992256924c560fedeef0eac7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionPerInstanceConfigPreservedStateInternalIp]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4bfdb9d761f510c9dc62185e9b0bdd0bb89f6a6abcfaadcceedf96f5ee5177e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddc840fc1d58916d21722a290cafa470777ea76b3d7674b8a995b2d3f70e226e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionPerInstanceConfigPreservedStateDisk, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d289b16ad914bd0387331f47a4d8b3d6999298a610301de90fe15fa9839283a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionPerInstanceConfigPreservedStateExternalIp, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93d069662a07b2e17fc51adf6e62fb0e20563a278b2ee48195f3be51a94e156e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionPerInstanceConfigPreservedStateInternalIp, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4eeaa819a0f0ebe97236fe136ff5099756823e39632856a606eee8454c3366c5(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1de8fabc81cd776ea4b62373b6bb57df1afdc5d4bc3c21c004a5da36467ec67b(
    value: typing.Optional[ComputeRegionPerInstanceConfigPreservedState],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d9b271f582cb8d88eefef254f79d10d0f640d0fc341658e619bab3fc772243a(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d12dac853d1b12481326a9683c84ce28abe9db3fbf874d7ae590689ce14013c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7b2fada7bb64f1a753db4abcf02175ea2026382afde6b06da04afcbffd48ecd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c7d79e264cd89005af6d1241c086792359647034186631569775a0988f23a1d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa1cc960b7166cef3a8801a4866b92ce359450e42d99434a99f156a16c3d3cb2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5029b7bfcc76fe16d86990a4a4293064710b86a0e62b97777cececf03de9a7f7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionPerInstanceConfigTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
