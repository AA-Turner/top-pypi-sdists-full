r'''
# `google_compute_per_instance_config`

Refer to the Terraform Registry for docs: [`google_compute_per_instance_config`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config).
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


class ComputePerInstanceConfig(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computePerInstanceConfig.ComputePerInstanceConfig",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config google_compute_per_instance_config}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        instance_group_manager: builtins.str,
        name: builtins.str,
        id: typing.Optional[builtins.str] = None,
        minimal_action: typing.Optional[builtins.str] = None,
        most_disruptive_allowed_action: typing.Optional[builtins.str] = None,
        preserved_state: typing.Optional[typing.Union["ComputePerInstanceConfigPreservedState", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        remove_instance_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        remove_instance_state_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["ComputePerInstanceConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        zone: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config google_compute_per_instance_config} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param instance_group_manager: The instance group manager this instance config is part of. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#instance_group_manager ComputePerInstanceConfig#instance_group_manager}
        :param name: The name for this per-instance config and its corresponding instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#name ComputePerInstanceConfig#name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#id ComputePerInstanceConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param minimal_action: The minimal action to perform on the instance during an update. Default is 'NONE'. Possible values are: - REPLACE - RESTART - REFRESH - NONE Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#minimal_action ComputePerInstanceConfig#minimal_action}
        :param most_disruptive_allowed_action: The most disruptive action to perform on the instance during an update. Default is 'REPLACE'. Possible values are: - REPLACE - RESTART - REFRESH - NONE Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#most_disruptive_allowed_action ComputePerInstanceConfig#most_disruptive_allowed_action}
        :param preserved_state: preserved_state block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#preserved_state ComputePerInstanceConfig#preserved_state}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#project ComputePerInstanceConfig#project}.
        :param remove_instance_on_destroy: When true, deleting this config will immediately remove the underlying instance. When false, deleting this config will use the behavior as determined by remove_instance_on_destroy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#remove_instance_on_destroy ComputePerInstanceConfig#remove_instance_on_destroy}
        :param remove_instance_state_on_destroy: When true, deleting this config will immediately remove any specified state from the underlying instance. When false, deleting this config will *not* immediately remove any state from the underlying instance. State will be removed on the next instance recreation or update. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#remove_instance_state_on_destroy ComputePerInstanceConfig#remove_instance_state_on_destroy}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#timeouts ComputePerInstanceConfig#timeouts}
        :param zone: Zone where the containing instance group manager is located. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#zone ComputePerInstanceConfig#zone}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63da3adcec777321e69249f12627936c21f40c5feb9eca5a14dbd7c877474f15)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ComputePerInstanceConfigConfig(
            instance_group_manager=instance_group_manager,
            name=name,
            id=id,
            minimal_action=minimal_action,
            most_disruptive_allowed_action=most_disruptive_allowed_action,
            preserved_state=preserved_state,
            project=project,
            remove_instance_on_destroy=remove_instance_on_destroy,
            remove_instance_state_on_destroy=remove_instance_state_on_destroy,
            timeouts=timeouts,
            zone=zone,
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
        '''Generates CDKTF code for importing a ComputePerInstanceConfig resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ComputePerInstanceConfig to import.
        :param import_from_id: The id of the existing ComputePerInstanceConfig that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ComputePerInstanceConfig to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c81cb925bd9289a095fa4990811abae66ba4ef697cf673b6e20fa0f737577663)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putPreservedState")
    def put_preserved_state(
        self,
        *,
        disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputePerInstanceConfigPreservedStateDisk", typing.Dict[builtins.str, typing.Any]]]]] = None,
        external_ip: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputePerInstanceConfigPreservedStateExternalIp", typing.Dict[builtins.str, typing.Any]]]]] = None,
        internal_ip: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputePerInstanceConfigPreservedStateInternalIp", typing.Dict[builtins.str, typing.Any]]]]] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param disk: disk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#disk ComputePerInstanceConfig#disk}
        :param external_ip: external_ip block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#external_ip ComputePerInstanceConfig#external_ip}
        :param internal_ip: internal_ip block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#internal_ip ComputePerInstanceConfig#internal_ip}
        :param metadata: Preserved metadata defined for this instance. This is a list of key->value pairs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#metadata ComputePerInstanceConfig#metadata}
        '''
        value = ComputePerInstanceConfigPreservedState(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#create ComputePerInstanceConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#delete ComputePerInstanceConfig#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#update ComputePerInstanceConfig#update}.
        '''
        value = ComputePerInstanceConfigTimeouts(
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

    @jsii.member(jsii_name="resetRemoveInstanceOnDestroy")
    def reset_remove_instance_on_destroy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRemoveInstanceOnDestroy", []))

    @jsii.member(jsii_name="resetRemoveInstanceStateOnDestroy")
    def reset_remove_instance_state_on_destroy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRemoveInstanceStateOnDestroy", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetZone")
    def reset_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZone", []))

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
    ) -> "ComputePerInstanceConfigPreservedStateOutputReference":
        return typing.cast("ComputePerInstanceConfigPreservedStateOutputReference", jsii.get(self, "preservedState"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ComputePerInstanceConfigTimeoutsOutputReference":
        return typing.cast("ComputePerInstanceConfigTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceGroupManagerInput")
    def instance_group_manager_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceGroupManagerInput"))

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
    ) -> typing.Optional["ComputePerInstanceConfigPreservedState"]:
        return typing.cast(typing.Optional["ComputePerInstanceConfigPreservedState"], jsii.get(self, "preservedStateInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputePerInstanceConfigTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputePerInstanceConfigTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="zoneInput")
    def zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "zoneInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d970caac8d608b00572aabcb2c8f6d0f4427562bf8f4d0bd9aa4cefedfe7993)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceGroupManager")
    def instance_group_manager(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceGroupManager"))

    @instance_group_manager.setter
    def instance_group_manager(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc2de89792140e254e9689b09b86e26196a18aae45ae4ac7e8c356feb7090f5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceGroupManager", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minimalAction")
    def minimal_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minimalAction"))

    @minimal_action.setter
    def minimal_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab46cce1d0729c60b4031c59f63a8eabb2cbc0e4af23d726453cb89ebba09e9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minimalAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mostDisruptiveAllowedAction")
    def most_disruptive_allowed_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mostDisruptiveAllowedAction"))

    @most_disruptive_allowed_action.setter
    def most_disruptive_allowed_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4aa5f973786ed79c9d50d4be330da5bbc47bda3ec4261a011c45a87aa996edec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mostDisruptiveAllowedAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6e8c6edc6b8b626a448af4a3bdacaec1a441b6ee3d058824dd9b753889fdf5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e6d3f7a3f01ba4ab66640b46250e4e1e7a26a29127bc2f46786ff7f4ecb5e6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__ea6e3859cf6a41db8750af9551cf403e2ad16dcb98b918ae9feb612bb800ad14)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a479dd638bd01b29df091aa80a84e2c78d0712e014eb0388edab5c9527c1579)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "removeInstanceStateOnDestroy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zone")
    def zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zone"))

    @zone.setter
    def zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47c66bb6fb09c585d1e661ecc8f1d9f6caf2bda2d6155cb150214700974e42df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zone", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computePerInstanceConfig.ComputePerInstanceConfigConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "instance_group_manager": "instanceGroupManager",
        "name": "name",
        "id": "id",
        "minimal_action": "minimalAction",
        "most_disruptive_allowed_action": "mostDisruptiveAllowedAction",
        "preserved_state": "preservedState",
        "project": "project",
        "remove_instance_on_destroy": "removeInstanceOnDestroy",
        "remove_instance_state_on_destroy": "removeInstanceStateOnDestroy",
        "timeouts": "timeouts",
        "zone": "zone",
    },
)
class ComputePerInstanceConfigConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        instance_group_manager: builtins.str,
        name: builtins.str,
        id: typing.Optional[builtins.str] = None,
        minimal_action: typing.Optional[builtins.str] = None,
        most_disruptive_allowed_action: typing.Optional[builtins.str] = None,
        preserved_state: typing.Optional[typing.Union["ComputePerInstanceConfigPreservedState", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        remove_instance_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        remove_instance_state_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["ComputePerInstanceConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param instance_group_manager: The instance group manager this instance config is part of. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#instance_group_manager ComputePerInstanceConfig#instance_group_manager}
        :param name: The name for this per-instance config and its corresponding instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#name ComputePerInstanceConfig#name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#id ComputePerInstanceConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param minimal_action: The minimal action to perform on the instance during an update. Default is 'NONE'. Possible values are: - REPLACE - RESTART - REFRESH - NONE Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#minimal_action ComputePerInstanceConfig#minimal_action}
        :param most_disruptive_allowed_action: The most disruptive action to perform on the instance during an update. Default is 'REPLACE'. Possible values are: - REPLACE - RESTART - REFRESH - NONE Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#most_disruptive_allowed_action ComputePerInstanceConfig#most_disruptive_allowed_action}
        :param preserved_state: preserved_state block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#preserved_state ComputePerInstanceConfig#preserved_state}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#project ComputePerInstanceConfig#project}.
        :param remove_instance_on_destroy: When true, deleting this config will immediately remove the underlying instance. When false, deleting this config will use the behavior as determined by remove_instance_on_destroy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#remove_instance_on_destroy ComputePerInstanceConfig#remove_instance_on_destroy}
        :param remove_instance_state_on_destroy: When true, deleting this config will immediately remove any specified state from the underlying instance. When false, deleting this config will *not* immediately remove any state from the underlying instance. State will be removed on the next instance recreation or update. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#remove_instance_state_on_destroy ComputePerInstanceConfig#remove_instance_state_on_destroy}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#timeouts ComputePerInstanceConfig#timeouts}
        :param zone: Zone where the containing instance group manager is located. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#zone ComputePerInstanceConfig#zone}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(preserved_state, dict):
            preserved_state = ComputePerInstanceConfigPreservedState(**preserved_state)
        if isinstance(timeouts, dict):
            timeouts = ComputePerInstanceConfigTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa396248cd8614defd9eaf2fd1b77fec7ebd0e4b826df1b3c7194b53c2038614)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument instance_group_manager", value=instance_group_manager, expected_type=type_hints["instance_group_manager"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument minimal_action", value=minimal_action, expected_type=type_hints["minimal_action"])
            check_type(argname="argument most_disruptive_allowed_action", value=most_disruptive_allowed_action, expected_type=type_hints["most_disruptive_allowed_action"])
            check_type(argname="argument preserved_state", value=preserved_state, expected_type=type_hints["preserved_state"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument remove_instance_on_destroy", value=remove_instance_on_destroy, expected_type=type_hints["remove_instance_on_destroy"])
            check_type(argname="argument remove_instance_state_on_destroy", value=remove_instance_state_on_destroy, expected_type=type_hints["remove_instance_state_on_destroy"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument zone", value=zone, expected_type=type_hints["zone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_group_manager": instance_group_manager,
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
        if remove_instance_on_destroy is not None:
            self._values["remove_instance_on_destroy"] = remove_instance_on_destroy
        if remove_instance_state_on_destroy is not None:
            self._values["remove_instance_state_on_destroy"] = remove_instance_state_on_destroy
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if zone is not None:
            self._values["zone"] = zone

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
    def instance_group_manager(self) -> builtins.str:
        '''The instance group manager this instance config is part of.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#instance_group_manager ComputePerInstanceConfig#instance_group_manager}
        '''
        result = self._values.get("instance_group_manager")
        assert result is not None, "Required property 'instance_group_manager' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name for this per-instance config and its corresponding instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#name ComputePerInstanceConfig#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#id ComputePerInstanceConfig#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#minimal_action ComputePerInstanceConfig#minimal_action}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#most_disruptive_allowed_action ComputePerInstanceConfig#most_disruptive_allowed_action}
        '''
        result = self._values.get("most_disruptive_allowed_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preserved_state(
        self,
    ) -> typing.Optional["ComputePerInstanceConfigPreservedState"]:
        '''preserved_state block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#preserved_state ComputePerInstanceConfig#preserved_state}
        '''
        result = self._values.get("preserved_state")
        return typing.cast(typing.Optional["ComputePerInstanceConfigPreservedState"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#project ComputePerInstanceConfig#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remove_instance_on_destroy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When true, deleting this config will immediately remove the underlying instance.

        When false, deleting this config will use the behavior as determined by remove_instance_on_destroy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#remove_instance_on_destroy ComputePerInstanceConfig#remove_instance_on_destroy}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#remove_instance_state_on_destroy ComputePerInstanceConfig#remove_instance_state_on_destroy}
        '''
        result = self._values.get("remove_instance_state_on_destroy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ComputePerInstanceConfigTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#timeouts ComputePerInstanceConfig#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ComputePerInstanceConfigTimeouts"], result)

    @builtins.property
    def zone(self) -> typing.Optional[builtins.str]:
        '''Zone where the containing instance group manager is located.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#zone ComputePerInstanceConfig#zone}
        '''
        result = self._values.get("zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputePerInstanceConfigConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computePerInstanceConfig.ComputePerInstanceConfigPreservedState",
    jsii_struct_bases=[],
    name_mapping={
        "disk": "disk",
        "external_ip": "externalIp",
        "internal_ip": "internalIp",
        "metadata": "metadata",
    },
)
class ComputePerInstanceConfigPreservedState:
    def __init__(
        self,
        *,
        disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputePerInstanceConfigPreservedStateDisk", typing.Dict[builtins.str, typing.Any]]]]] = None,
        external_ip: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputePerInstanceConfigPreservedStateExternalIp", typing.Dict[builtins.str, typing.Any]]]]] = None,
        internal_ip: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputePerInstanceConfigPreservedStateInternalIp", typing.Dict[builtins.str, typing.Any]]]]] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param disk: disk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#disk ComputePerInstanceConfig#disk}
        :param external_ip: external_ip block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#external_ip ComputePerInstanceConfig#external_ip}
        :param internal_ip: internal_ip block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#internal_ip ComputePerInstanceConfig#internal_ip}
        :param metadata: Preserved metadata defined for this instance. This is a list of key->value pairs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#metadata ComputePerInstanceConfig#metadata}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7e801b0a5329fd5c42bc4d0b62acd7bddfba3e4f915365e2da2840fd7c7a782)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputePerInstanceConfigPreservedStateDisk"]]]:
        '''disk block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#disk ComputePerInstanceConfig#disk}
        '''
        result = self._values.get("disk")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputePerInstanceConfigPreservedStateDisk"]]], result)

    @builtins.property
    def external_ip(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputePerInstanceConfigPreservedStateExternalIp"]]]:
        '''external_ip block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#external_ip ComputePerInstanceConfig#external_ip}
        '''
        result = self._values.get("external_ip")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputePerInstanceConfigPreservedStateExternalIp"]]], result)

    @builtins.property
    def internal_ip(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputePerInstanceConfigPreservedStateInternalIp"]]]:
        '''internal_ip block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#internal_ip ComputePerInstanceConfig#internal_ip}
        '''
        result = self._values.get("internal_ip")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputePerInstanceConfigPreservedStateInternalIp"]]], result)

    @builtins.property
    def metadata(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Preserved metadata defined for this instance. This is a list of key->value pairs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#metadata ComputePerInstanceConfig#metadata}
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputePerInstanceConfigPreservedState(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computePerInstanceConfig.ComputePerInstanceConfigPreservedStateDisk",
    jsii_struct_bases=[],
    name_mapping={
        "device_name": "deviceName",
        "source": "source",
        "delete_rule": "deleteRule",
        "mode": "mode",
    },
)
class ComputePerInstanceConfigPreservedStateDisk:
    def __init__(
        self,
        *,
        device_name: builtins.str,
        source: builtins.str,
        delete_rule: typing.Optional[builtins.str] = None,
        mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param device_name: A unique device name that is reflected into the /dev/ tree of a Linux operating system running within the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#device_name ComputePerInstanceConfig#device_name}
        :param source: The URI of an existing persistent disk to attach under the specified device-name in the format 'projects/project-id/zones/zone/disks/disk-name'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#source ComputePerInstanceConfig#source}
        :param delete_rule: A value that prescribes what should happen to the stateful disk when the VM instance is deleted. The available options are 'NEVER' and 'ON_PERMANENT_INSTANCE_DELETION'. 'NEVER' - detach the disk when the VM is deleted, but do not delete the disk. 'ON_PERMANENT_INSTANCE_DELETION' will delete the stateful disk when the VM is permanently deleted from the instance group. Default value: "NEVER" Possible values: ["NEVER", "ON_PERMANENT_INSTANCE_DELETION"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#delete_rule ComputePerInstanceConfig#delete_rule}
        :param mode: The mode of the disk. Default value: "READ_WRITE" Possible values: ["READ_ONLY", "READ_WRITE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#mode ComputePerInstanceConfig#mode}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87e2daba97a4b5703095afd2e5d299ffb4c67118f546e25e785e8b967600c645)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#device_name ComputePerInstanceConfig#device_name}
        '''
        result = self._values.get("device_name")
        assert result is not None, "Required property 'device_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source(self) -> builtins.str:
        '''The URI of an existing persistent disk to attach under the specified device-name in the format 'projects/project-id/zones/zone/disks/disk-name'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#source ComputePerInstanceConfig#source}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#delete_rule ComputePerInstanceConfig#delete_rule}
        '''
        result = self._values.get("delete_rule")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''The mode of the disk. Default value: "READ_WRITE" Possible values: ["READ_ONLY", "READ_WRITE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#mode ComputePerInstanceConfig#mode}
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputePerInstanceConfigPreservedStateDisk(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputePerInstanceConfigPreservedStateDiskList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computePerInstanceConfig.ComputePerInstanceConfigPreservedStateDiskList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f79978129572585380adb0c324a4ce50f80cd9b6ae6fa935cf3065749dfb8801)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputePerInstanceConfigPreservedStateDiskOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3e6a81e3f766f657e65a0ffcf1c84ece48535a89205e4eaee1d0de406b01670)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputePerInstanceConfigPreservedStateDiskOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44df85600b87f38a161e662c842163eeeb3243475649b99e1ac44500fd6552ab)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb28acce13f2f407bc6178faeb807993dcabfa3b98173f2ece554e3bfb1b97f5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4d4037fc5401f01d2e0f5437314ec1e3fe19b53722ec483532ff0ff3e8d94155)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputePerInstanceConfigPreservedStateDisk]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputePerInstanceConfigPreservedStateDisk]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputePerInstanceConfigPreservedStateDisk]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__100b81f1fde0707efc36baa9d1dff9420d78196ce91d624490f318b10bb61ef2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputePerInstanceConfigPreservedStateDiskOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computePerInstanceConfig.ComputePerInstanceConfigPreservedStateDiskOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d7a6371969a7ce5612adf0c2a13e5ed83bf04fbdec03c6157d58a51d6f47b34)
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
            type_hints = typing.get_type_hints(_typecheckingstub__95c9e3272ae875df1464abb122a858a7d7b2b4e2bd26edd0015ec770ead4f267)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deleteRule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deviceName")
    def device_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deviceName"))

    @device_name.setter
    def device_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ad0bd839c888ed528b37ee3532c527c8f8f3f4b1a17a2cf4b09b3d045f9aad1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deviceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7cf4da5501324aae6a1436046241ceede6dfaa5fabe550d46e60deab8958032)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d105d13a9c874648ae0f19286013a4ce26c0bc659de8517566c90bee61bf5c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputePerInstanceConfigPreservedStateDisk]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputePerInstanceConfigPreservedStateDisk]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputePerInstanceConfigPreservedStateDisk]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93d0d822b5ecc70f03ff1ac1330c687535cf3c2096d41b3fbfc879ca8cbceed9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computePerInstanceConfig.ComputePerInstanceConfigPreservedStateExternalIp",
    jsii_struct_bases=[],
    name_mapping={
        "interface_name": "interfaceName",
        "auto_delete": "autoDelete",
        "ip_address": "ipAddress",
    },
)
class ComputePerInstanceConfigPreservedStateExternalIp:
    def __init__(
        self,
        *,
        interface_name: builtins.str,
        auto_delete: typing.Optional[builtins.str] = None,
        ip_address: typing.Optional[typing.Union["ComputePerInstanceConfigPreservedStateExternalIpIpAddress", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param interface_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#interface_name ComputePerInstanceConfig#interface_name}.
        :param auto_delete: These stateful IPs will never be released during autohealing, update or VM instance recreate operations. This flag is used to configure if the IP reservation should be deleted after it is no longer used by the group, e.g. when the given instance or the whole group is deleted. Default value: "NEVER" Possible values: ["NEVER", "ON_PERMANENT_INSTANCE_DELETION"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#auto_delete ComputePerInstanceConfig#auto_delete}
        :param ip_address: ip_address block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#ip_address ComputePerInstanceConfig#ip_address}
        '''
        if isinstance(ip_address, dict):
            ip_address = ComputePerInstanceConfigPreservedStateExternalIpIpAddress(**ip_address)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a92f74b721aa555d01bb960ee18e99c6bf19e8d8b07efc039e77404fc240d6e8)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#interface_name ComputePerInstanceConfig#interface_name}.'''
        result = self._values.get("interface_name")
        assert result is not None, "Required property 'interface_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auto_delete(self) -> typing.Optional[builtins.str]:
        '''These stateful IPs will never be released during autohealing, update or VM instance recreate operations.

        This flag is used to configure if the IP reservation should be deleted after it is no longer used by the group, e.g. when the given instance or the whole group is deleted. Default value: "NEVER" Possible values: ["NEVER", "ON_PERMANENT_INSTANCE_DELETION"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#auto_delete ComputePerInstanceConfig#auto_delete}
        '''
        result = self._values.get("auto_delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_address(
        self,
    ) -> typing.Optional["ComputePerInstanceConfigPreservedStateExternalIpIpAddress"]:
        '''ip_address block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#ip_address ComputePerInstanceConfig#ip_address}
        '''
        result = self._values.get("ip_address")
        return typing.cast(typing.Optional["ComputePerInstanceConfigPreservedStateExternalIpIpAddress"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputePerInstanceConfigPreservedStateExternalIp(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computePerInstanceConfig.ComputePerInstanceConfigPreservedStateExternalIpIpAddress",
    jsii_struct_bases=[],
    name_mapping={"address": "address"},
)
class ComputePerInstanceConfigPreservedStateExternalIpIpAddress:
    def __init__(self, *, address: typing.Optional[builtins.str] = None) -> None:
        '''
        :param address: The URL of the reservation for this IP address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#address ComputePerInstanceConfig#address}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af3761e875375739dfc6b3e1960700e5c613e01d51c7064e16365f6bd055e565)
            check_type(argname="argument address", value=address, expected_type=type_hints["address"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if address is not None:
            self._values["address"] = address

    @builtins.property
    def address(self) -> typing.Optional[builtins.str]:
        '''The URL of the reservation for this IP address.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#address ComputePerInstanceConfig#address}
        '''
        result = self._values.get("address")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputePerInstanceConfigPreservedStateExternalIpIpAddress(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputePerInstanceConfigPreservedStateExternalIpIpAddressOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computePerInstanceConfig.ComputePerInstanceConfigPreservedStateExternalIpIpAddressOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__512716d5fbc84ee0c8d0834354f7cfad8b93ced8e82812b5da1e3bb5d1226861)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f44077f4d4328ec66c90fdf256ab0579ae32ccdd13d468c84b4cb4757918b45d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputePerInstanceConfigPreservedStateExternalIpIpAddress]:
        return typing.cast(typing.Optional[ComputePerInstanceConfigPreservedStateExternalIpIpAddress], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputePerInstanceConfigPreservedStateExternalIpIpAddress],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93e0c27d43134ae3c1abf9c3759a273c8b009facb285ca9d512c78a7b343eb90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputePerInstanceConfigPreservedStateExternalIpList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computePerInstanceConfig.ComputePerInstanceConfigPreservedStateExternalIpList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b52bf370eb316530bc60732a332d4122aaf93d23a73eba6f4edb9fcb866a8a49)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputePerInstanceConfigPreservedStateExternalIpOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f545ed50213caf26d483450a7343669bbb055680e0746bf241de3843852edb4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputePerInstanceConfigPreservedStateExternalIpOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17c55efdedda391fdd13bc7a2daba9e39ebe7c105b1be7127aed9cc1de42e931)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d01ca65325875c5f5e542090f82900c13a37867466882d8e0af39d51f4c7acb9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6442dc9d68cfac57392a3e06babb7b18fd4dff3fd0d648f12885dde8b1bf3e0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputePerInstanceConfigPreservedStateExternalIp]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputePerInstanceConfigPreservedStateExternalIp]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputePerInstanceConfigPreservedStateExternalIp]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d517e260cc1d963de0310d9b4081f8bd6eae73a44fdba124ede35c4cfd6030a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputePerInstanceConfigPreservedStateExternalIpOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computePerInstanceConfig.ComputePerInstanceConfigPreservedStateExternalIpOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4781cd1ac7ee4308f864fd51de8035d1ea702096dd108eea128da7d11cf9abd0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putIpAddress")
    def put_ip_address(self, *, address: typing.Optional[builtins.str] = None) -> None:
        '''
        :param address: The URL of the reservation for this IP address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#address ComputePerInstanceConfig#address}
        '''
        value = ComputePerInstanceConfigPreservedStateExternalIpIpAddress(
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
    ) -> ComputePerInstanceConfigPreservedStateExternalIpIpAddressOutputReference:
        return typing.cast(ComputePerInstanceConfigPreservedStateExternalIpIpAddressOutputReference, jsii.get(self, "ipAddress"))

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
    ) -> typing.Optional[ComputePerInstanceConfigPreservedStateExternalIpIpAddress]:
        return typing.cast(typing.Optional[ComputePerInstanceConfigPreservedStateExternalIpIpAddress], jsii.get(self, "ipAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="autoDelete")
    def auto_delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "autoDelete"))

    @auto_delete.setter
    def auto_delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7230a7d9a1975a6fb5f10acbb4667af014133995b859fd012b8cff2d0a7ebc52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoDelete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="interfaceName")
    def interface_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "interfaceName"))

    @interface_name.setter
    def interface_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6010a2986e1433e78fecb02ee36995c502745496f44a9c2c376b7c193fdd1818)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interfaceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputePerInstanceConfigPreservedStateExternalIp]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputePerInstanceConfigPreservedStateExternalIp]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputePerInstanceConfigPreservedStateExternalIp]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__686b543c4d2cb4ca5daf82f3a512513de54e214c66612e2224bf88270d16af61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computePerInstanceConfig.ComputePerInstanceConfigPreservedStateInternalIp",
    jsii_struct_bases=[],
    name_mapping={
        "interface_name": "interfaceName",
        "auto_delete": "autoDelete",
        "ip_address": "ipAddress",
    },
)
class ComputePerInstanceConfigPreservedStateInternalIp:
    def __init__(
        self,
        *,
        interface_name: builtins.str,
        auto_delete: typing.Optional[builtins.str] = None,
        ip_address: typing.Optional[typing.Union["ComputePerInstanceConfigPreservedStateInternalIpIpAddress", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param interface_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#interface_name ComputePerInstanceConfig#interface_name}.
        :param auto_delete: These stateful IPs will never be released during autohealing, update or VM instance recreate operations. This flag is used to configure if the IP reservation should be deleted after it is no longer used by the group, e.g. when the given instance or the whole group is deleted. Default value: "NEVER" Possible values: ["NEVER", "ON_PERMANENT_INSTANCE_DELETION"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#auto_delete ComputePerInstanceConfig#auto_delete}
        :param ip_address: ip_address block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#ip_address ComputePerInstanceConfig#ip_address}
        '''
        if isinstance(ip_address, dict):
            ip_address = ComputePerInstanceConfigPreservedStateInternalIpIpAddress(**ip_address)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eea8f3f03bcbf951fd503a21b0610ba3e81aa4ade01040239d789d49f80f2fc9)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#interface_name ComputePerInstanceConfig#interface_name}.'''
        result = self._values.get("interface_name")
        assert result is not None, "Required property 'interface_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auto_delete(self) -> typing.Optional[builtins.str]:
        '''These stateful IPs will never be released during autohealing, update or VM instance recreate operations.

        This flag is used to configure if the IP reservation should be deleted after it is no longer used by the group, e.g. when the given instance or the whole group is deleted. Default value: "NEVER" Possible values: ["NEVER", "ON_PERMANENT_INSTANCE_DELETION"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#auto_delete ComputePerInstanceConfig#auto_delete}
        '''
        result = self._values.get("auto_delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_address(
        self,
    ) -> typing.Optional["ComputePerInstanceConfigPreservedStateInternalIpIpAddress"]:
        '''ip_address block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#ip_address ComputePerInstanceConfig#ip_address}
        '''
        result = self._values.get("ip_address")
        return typing.cast(typing.Optional["ComputePerInstanceConfigPreservedStateInternalIpIpAddress"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputePerInstanceConfigPreservedStateInternalIp(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computePerInstanceConfig.ComputePerInstanceConfigPreservedStateInternalIpIpAddress",
    jsii_struct_bases=[],
    name_mapping={"address": "address"},
)
class ComputePerInstanceConfigPreservedStateInternalIpIpAddress:
    def __init__(self, *, address: typing.Optional[builtins.str] = None) -> None:
        '''
        :param address: The URL of the reservation for this IP address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#address ComputePerInstanceConfig#address}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e0f9910c66a2e6be2ecf7bf14eb0a630eeb02e5c8962ad875b10fe01a9e4b7f)
            check_type(argname="argument address", value=address, expected_type=type_hints["address"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if address is not None:
            self._values["address"] = address

    @builtins.property
    def address(self) -> typing.Optional[builtins.str]:
        '''The URL of the reservation for this IP address.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#address ComputePerInstanceConfig#address}
        '''
        result = self._values.get("address")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputePerInstanceConfigPreservedStateInternalIpIpAddress(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputePerInstanceConfigPreservedStateInternalIpIpAddressOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computePerInstanceConfig.ComputePerInstanceConfigPreservedStateInternalIpIpAddressOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__675de3c8f56eca9281ce832cd9641408429a61bc9fac07fdbed59543f0ab9cdf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c45c20dc1527e3b854d17a9d5fe734303f03a5f1df33fe94fcd299aefdfb56fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputePerInstanceConfigPreservedStateInternalIpIpAddress]:
        return typing.cast(typing.Optional[ComputePerInstanceConfigPreservedStateInternalIpIpAddress], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputePerInstanceConfigPreservedStateInternalIpIpAddress],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c3c01d3535e38325ea9571be2a3ee62b1eddaf68c2910127c42ad4219a3f2c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputePerInstanceConfigPreservedStateInternalIpList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computePerInstanceConfig.ComputePerInstanceConfigPreservedStateInternalIpList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__587b3692f3355bdee6aea67b8623ad5b84f43c7a4967d6e0d734d9da17eb3639)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputePerInstanceConfigPreservedStateInternalIpOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21bff65d77ace74efda042d4db1bb9bc81fe6346137ef1ed9d8b9a09216c6986)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputePerInstanceConfigPreservedStateInternalIpOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__106f6dc54a861576f005c36b3b651e900e4de5a8737b45f19c727777ba9ec453)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd39b71347998cafa4214f1e211ad472e64a74102ef5a83de43c96fd9656fa52)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1dcfd030e060ddff260a1cccca1cf0419eaf50348cc3ebf680deb26304727005)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputePerInstanceConfigPreservedStateInternalIp]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputePerInstanceConfigPreservedStateInternalIp]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputePerInstanceConfigPreservedStateInternalIp]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c388d23d8caa799206428458172d9e9ea582f3fd0758cce05b3e57a122cc1929)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputePerInstanceConfigPreservedStateInternalIpOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computePerInstanceConfig.ComputePerInstanceConfigPreservedStateInternalIpOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__227a586f5267857c28edcc92d50951859db4d51e1bd27f69bab887d7a59c4bfe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putIpAddress")
    def put_ip_address(self, *, address: typing.Optional[builtins.str] = None) -> None:
        '''
        :param address: The URL of the reservation for this IP address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#address ComputePerInstanceConfig#address}
        '''
        value = ComputePerInstanceConfigPreservedStateInternalIpIpAddress(
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
    ) -> ComputePerInstanceConfigPreservedStateInternalIpIpAddressOutputReference:
        return typing.cast(ComputePerInstanceConfigPreservedStateInternalIpIpAddressOutputReference, jsii.get(self, "ipAddress"))

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
    ) -> typing.Optional[ComputePerInstanceConfigPreservedStateInternalIpIpAddress]:
        return typing.cast(typing.Optional[ComputePerInstanceConfigPreservedStateInternalIpIpAddress], jsii.get(self, "ipAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="autoDelete")
    def auto_delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "autoDelete"))

    @auto_delete.setter
    def auto_delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4dc69ad93a64aee7ed4c50ea991dc08b24488f274157532c85c75267e1a8ca0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoDelete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="interfaceName")
    def interface_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "interfaceName"))

    @interface_name.setter
    def interface_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1dc382604c6189edc9ed299cc19bf56ed211dad320d003ce8bc8160db77db68f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interfaceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputePerInstanceConfigPreservedStateInternalIp]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputePerInstanceConfigPreservedStateInternalIp]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputePerInstanceConfigPreservedStateInternalIp]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a8bd279da3d55cd15be49f9644e93c69cb85c57afdfd74c266a2a2648f007a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputePerInstanceConfigPreservedStateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computePerInstanceConfig.ComputePerInstanceConfigPreservedStateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a4bcef1333ed8011cec6ee8a514ae536318eca09c3b01d6889287a59d40f812)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDisk")
    def put_disk(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputePerInstanceConfigPreservedStateDisk, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b94e3a7d8487ae802dd7185247ab766a38898c2bf415ce4680ece0116d99f895)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDisk", [value]))

    @jsii.member(jsii_name="putExternalIp")
    def put_external_ip(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputePerInstanceConfigPreservedStateExternalIp, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfe38d17e7541a9c93753c2bcd0ddb1190a1f3902c99ed919b4ba4a2908cce02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putExternalIp", [value]))

    @jsii.member(jsii_name="putInternalIp")
    def put_internal_ip(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputePerInstanceConfigPreservedStateInternalIp, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__070ae3b088c9009233d6436ebe52af1dffa14f8aeeb2e19a197295d7a0b18335)
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
    def disk(self) -> ComputePerInstanceConfigPreservedStateDiskList:
        return typing.cast(ComputePerInstanceConfigPreservedStateDiskList, jsii.get(self, "disk"))

    @builtins.property
    @jsii.member(jsii_name="externalIp")
    def external_ip(self) -> ComputePerInstanceConfigPreservedStateExternalIpList:
        return typing.cast(ComputePerInstanceConfigPreservedStateExternalIpList, jsii.get(self, "externalIp"))

    @builtins.property
    @jsii.member(jsii_name="internalIp")
    def internal_ip(self) -> ComputePerInstanceConfigPreservedStateInternalIpList:
        return typing.cast(ComputePerInstanceConfigPreservedStateInternalIpList, jsii.get(self, "internalIp"))

    @builtins.property
    @jsii.member(jsii_name="diskInput")
    def disk_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputePerInstanceConfigPreservedStateDisk]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputePerInstanceConfigPreservedStateDisk]]], jsii.get(self, "diskInput"))

    @builtins.property
    @jsii.member(jsii_name="externalIpInput")
    def external_ip_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputePerInstanceConfigPreservedStateExternalIp]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputePerInstanceConfigPreservedStateExternalIp]]], jsii.get(self, "externalIpInput"))

    @builtins.property
    @jsii.member(jsii_name="internalIpInput")
    def internal_ip_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputePerInstanceConfigPreservedStateInternalIp]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputePerInstanceConfigPreservedStateInternalIp]]], jsii.get(self, "internalIpInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__0549d0fa2f03d899d422d038eeff9eb0c4adc9e7b8475640281442930aee55b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadata", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputePerInstanceConfigPreservedState]:
        return typing.cast(typing.Optional[ComputePerInstanceConfigPreservedState], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputePerInstanceConfigPreservedState],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f040389ee22a1b1b89a40b3c1e7d81dd4f92b45edc44f32c012e6529f6528e16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computePerInstanceConfig.ComputePerInstanceConfigTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ComputePerInstanceConfigTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#create ComputePerInstanceConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#delete ComputePerInstanceConfig#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#update ComputePerInstanceConfig#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3eea74df6c3f2af648e775b47b214b2358612fc0cf2efe2e02185269bf82045f)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#create ComputePerInstanceConfig#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#delete ComputePerInstanceConfig#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_per_instance_config#update ComputePerInstanceConfig#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputePerInstanceConfigTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputePerInstanceConfigTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computePerInstanceConfig.ComputePerInstanceConfigTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e4351e4af3f3045679d40893dfebbf1f4c57dcc34e7437c254f9fd70bfdbd062)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b85381fb3a944919518a68948e30433aeb419496e9f6adef4e56a3aba8b0074c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__685526ce4cb4578e3efdba4d23ff44ae6d0295a5a76c3bdb709c2946b6d84646)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6266a5518b5c3c384c206fc55432fd9f2c70515a990d0e1142959e68d43bc15a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputePerInstanceConfigTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputePerInstanceConfigTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputePerInstanceConfigTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e09f22ebb844e7275f641544def8415b77d016855345c98445829ce06e994e59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ComputePerInstanceConfig",
    "ComputePerInstanceConfigConfig",
    "ComputePerInstanceConfigPreservedState",
    "ComputePerInstanceConfigPreservedStateDisk",
    "ComputePerInstanceConfigPreservedStateDiskList",
    "ComputePerInstanceConfigPreservedStateDiskOutputReference",
    "ComputePerInstanceConfigPreservedStateExternalIp",
    "ComputePerInstanceConfigPreservedStateExternalIpIpAddress",
    "ComputePerInstanceConfigPreservedStateExternalIpIpAddressOutputReference",
    "ComputePerInstanceConfigPreservedStateExternalIpList",
    "ComputePerInstanceConfigPreservedStateExternalIpOutputReference",
    "ComputePerInstanceConfigPreservedStateInternalIp",
    "ComputePerInstanceConfigPreservedStateInternalIpIpAddress",
    "ComputePerInstanceConfigPreservedStateInternalIpIpAddressOutputReference",
    "ComputePerInstanceConfigPreservedStateInternalIpList",
    "ComputePerInstanceConfigPreservedStateInternalIpOutputReference",
    "ComputePerInstanceConfigPreservedStateOutputReference",
    "ComputePerInstanceConfigTimeouts",
    "ComputePerInstanceConfigTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__63da3adcec777321e69249f12627936c21f40c5feb9eca5a14dbd7c877474f15(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    instance_group_manager: builtins.str,
    name: builtins.str,
    id: typing.Optional[builtins.str] = None,
    minimal_action: typing.Optional[builtins.str] = None,
    most_disruptive_allowed_action: typing.Optional[builtins.str] = None,
    preserved_state: typing.Optional[typing.Union[ComputePerInstanceConfigPreservedState, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    remove_instance_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    remove_instance_state_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[ComputePerInstanceConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    zone: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__c81cb925bd9289a095fa4990811abae66ba4ef697cf673b6e20fa0f737577663(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d970caac8d608b00572aabcb2c8f6d0f4427562bf8f4d0bd9aa4cefedfe7993(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc2de89792140e254e9689b09b86e26196a18aae45ae4ac7e8c356feb7090f5a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab46cce1d0729c60b4031c59f63a8eabb2cbc0e4af23d726453cb89ebba09e9f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4aa5f973786ed79c9d50d4be330da5bbc47bda3ec4261a011c45a87aa996edec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6e8c6edc6b8b626a448af4a3bdacaec1a441b6ee3d058824dd9b753889fdf5b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e6d3f7a3f01ba4ab66640b46250e4e1e7a26a29127bc2f46786ff7f4ecb5e6b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea6e3859cf6a41db8750af9551cf403e2ad16dcb98b918ae9feb612bb800ad14(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a479dd638bd01b29df091aa80a84e2c78d0712e014eb0388edab5c9527c1579(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47c66bb6fb09c585d1e661ecc8f1d9f6caf2bda2d6155cb150214700974e42df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa396248cd8614defd9eaf2fd1b77fec7ebd0e4b826df1b3c7194b53c2038614(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    instance_group_manager: builtins.str,
    name: builtins.str,
    id: typing.Optional[builtins.str] = None,
    minimal_action: typing.Optional[builtins.str] = None,
    most_disruptive_allowed_action: typing.Optional[builtins.str] = None,
    preserved_state: typing.Optional[typing.Union[ComputePerInstanceConfigPreservedState, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    remove_instance_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    remove_instance_state_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[ComputePerInstanceConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7e801b0a5329fd5c42bc4d0b62acd7bddfba3e4f915365e2da2840fd7c7a782(
    *,
    disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputePerInstanceConfigPreservedStateDisk, typing.Dict[builtins.str, typing.Any]]]]] = None,
    external_ip: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputePerInstanceConfigPreservedStateExternalIp, typing.Dict[builtins.str, typing.Any]]]]] = None,
    internal_ip: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputePerInstanceConfigPreservedStateInternalIp, typing.Dict[builtins.str, typing.Any]]]]] = None,
    metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87e2daba97a4b5703095afd2e5d299ffb4c67118f546e25e785e8b967600c645(
    *,
    device_name: builtins.str,
    source: builtins.str,
    delete_rule: typing.Optional[builtins.str] = None,
    mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f79978129572585380adb0c324a4ce50f80cd9b6ae6fa935cf3065749dfb8801(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3e6a81e3f766f657e65a0ffcf1c84ece48535a89205e4eaee1d0de406b01670(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44df85600b87f38a161e662c842163eeeb3243475649b99e1ac44500fd6552ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb28acce13f2f407bc6178faeb807993dcabfa3b98173f2ece554e3bfb1b97f5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d4037fc5401f01d2e0f5437314ec1e3fe19b53722ec483532ff0ff3e8d94155(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__100b81f1fde0707efc36baa9d1dff9420d78196ce91d624490f318b10bb61ef2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputePerInstanceConfigPreservedStateDisk]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d7a6371969a7ce5612adf0c2a13e5ed83bf04fbdec03c6157d58a51d6f47b34(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95c9e3272ae875df1464abb122a858a7d7b2b4e2bd26edd0015ec770ead4f267(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ad0bd839c888ed528b37ee3532c527c8f8f3f4b1a17a2cf4b09b3d045f9aad1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7cf4da5501324aae6a1436046241ceede6dfaa5fabe550d46e60deab8958032(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d105d13a9c874648ae0f19286013a4ce26c0bc659de8517566c90bee61bf5c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93d0d822b5ecc70f03ff1ac1330c687535cf3c2096d41b3fbfc879ca8cbceed9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputePerInstanceConfigPreservedStateDisk]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a92f74b721aa555d01bb960ee18e99c6bf19e8d8b07efc039e77404fc240d6e8(
    *,
    interface_name: builtins.str,
    auto_delete: typing.Optional[builtins.str] = None,
    ip_address: typing.Optional[typing.Union[ComputePerInstanceConfigPreservedStateExternalIpIpAddress, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af3761e875375739dfc6b3e1960700e5c613e01d51c7064e16365f6bd055e565(
    *,
    address: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__512716d5fbc84ee0c8d0834354f7cfad8b93ced8e82812b5da1e3bb5d1226861(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f44077f4d4328ec66c90fdf256ab0579ae32ccdd13d468c84b4cb4757918b45d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93e0c27d43134ae3c1abf9c3759a273c8b009facb285ca9d512c78a7b343eb90(
    value: typing.Optional[ComputePerInstanceConfigPreservedStateExternalIpIpAddress],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b52bf370eb316530bc60732a332d4122aaf93d23a73eba6f4edb9fcb866a8a49(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f545ed50213caf26d483450a7343669bbb055680e0746bf241de3843852edb4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17c55efdedda391fdd13bc7a2daba9e39ebe7c105b1be7127aed9cc1de42e931(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d01ca65325875c5f5e542090f82900c13a37867466882d8e0af39d51f4c7acb9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6442dc9d68cfac57392a3e06babb7b18fd4dff3fd0d648f12885dde8b1bf3e0a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d517e260cc1d963de0310d9b4081f8bd6eae73a44fdba124ede35c4cfd6030a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputePerInstanceConfigPreservedStateExternalIp]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4781cd1ac7ee4308f864fd51de8035d1ea702096dd108eea128da7d11cf9abd0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7230a7d9a1975a6fb5f10acbb4667af014133995b859fd012b8cff2d0a7ebc52(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6010a2986e1433e78fecb02ee36995c502745496f44a9c2c376b7c193fdd1818(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__686b543c4d2cb4ca5daf82f3a512513de54e214c66612e2224bf88270d16af61(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputePerInstanceConfigPreservedStateExternalIp]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eea8f3f03bcbf951fd503a21b0610ba3e81aa4ade01040239d789d49f80f2fc9(
    *,
    interface_name: builtins.str,
    auto_delete: typing.Optional[builtins.str] = None,
    ip_address: typing.Optional[typing.Union[ComputePerInstanceConfigPreservedStateInternalIpIpAddress, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e0f9910c66a2e6be2ecf7bf14eb0a630eeb02e5c8962ad875b10fe01a9e4b7f(
    *,
    address: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__675de3c8f56eca9281ce832cd9641408429a61bc9fac07fdbed59543f0ab9cdf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c45c20dc1527e3b854d17a9d5fe734303f03a5f1df33fe94fcd299aefdfb56fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c3c01d3535e38325ea9571be2a3ee62b1eddaf68c2910127c42ad4219a3f2c2(
    value: typing.Optional[ComputePerInstanceConfigPreservedStateInternalIpIpAddress],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__587b3692f3355bdee6aea67b8623ad5b84f43c7a4967d6e0d734d9da17eb3639(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21bff65d77ace74efda042d4db1bb9bc81fe6346137ef1ed9d8b9a09216c6986(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__106f6dc54a861576f005c36b3b651e900e4de5a8737b45f19c727777ba9ec453(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd39b71347998cafa4214f1e211ad472e64a74102ef5a83de43c96fd9656fa52(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dcfd030e060ddff260a1cccca1cf0419eaf50348cc3ebf680deb26304727005(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c388d23d8caa799206428458172d9e9ea582f3fd0758cce05b3e57a122cc1929(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputePerInstanceConfigPreservedStateInternalIp]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__227a586f5267857c28edcc92d50951859db4d51e1bd27f69bab887d7a59c4bfe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dc69ad93a64aee7ed4c50ea991dc08b24488f274157532c85c75267e1a8ca0c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dc382604c6189edc9ed299cc19bf56ed211dad320d003ce8bc8160db77db68f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a8bd279da3d55cd15be49f9644e93c69cb85c57afdfd74c266a2a2648f007a3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputePerInstanceConfigPreservedStateInternalIp]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a4bcef1333ed8011cec6ee8a514ae536318eca09c3b01d6889287a59d40f812(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b94e3a7d8487ae802dd7185247ab766a38898c2bf415ce4680ece0116d99f895(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputePerInstanceConfigPreservedStateDisk, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfe38d17e7541a9c93753c2bcd0ddb1190a1f3902c99ed919b4ba4a2908cce02(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputePerInstanceConfigPreservedStateExternalIp, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__070ae3b088c9009233d6436ebe52af1dffa14f8aeeb2e19a197295d7a0b18335(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputePerInstanceConfigPreservedStateInternalIp, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0549d0fa2f03d899d422d038eeff9eb0c4adc9e7b8475640281442930aee55b1(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f040389ee22a1b1b89a40b3c1e7d81dd4f92b45edc44f32c012e6529f6528e16(
    value: typing.Optional[ComputePerInstanceConfigPreservedState],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3eea74df6c3f2af648e775b47b214b2358612fc0cf2efe2e02185269bf82045f(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4351e4af3f3045679d40893dfebbf1f4c57dcc34e7437c254f9fd70bfdbd062(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b85381fb3a944919518a68948e30433aeb419496e9f6adef4e56a3aba8b0074c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__685526ce4cb4578e3efdba4d23ff44ae6d0295a5a76c3bdb709c2946b6d84646(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6266a5518b5c3c384c206fc55432fd9f2c70515a990d0e1142959e68d43bc15a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e09f22ebb844e7275f641544def8415b77d016855345c98445829ce06e994e59(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputePerInstanceConfigTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
