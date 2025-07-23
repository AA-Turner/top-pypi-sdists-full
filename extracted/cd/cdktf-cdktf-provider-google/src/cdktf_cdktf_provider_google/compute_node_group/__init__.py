r'''
# `google_compute_node_group`

Refer to the Terraform Registry for docs: [`google_compute_node_group`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_group).
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


class ComputeNodeGroup(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeNodeGroup.ComputeNodeGroup",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_group google_compute_node_group}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        node_template: builtins.str,
        autoscaling_policy: typing.Optional[typing.Union["ComputeNodeGroupAutoscalingPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        initial_size: typing.Optional[jsii.Number] = None,
        maintenance_policy: typing.Optional[builtins.str] = None,
        maintenance_window: typing.Optional[typing.Union["ComputeNodeGroupMaintenanceWindow", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        share_settings: typing.Optional[typing.Union["ComputeNodeGroupShareSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["ComputeNodeGroupTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        zone: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_group google_compute_node_group} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Name of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_group#name ComputeNodeGroup#name}
        :param node_template: The URL of the node template to which this node group belongs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_group#node_template ComputeNodeGroup#node_template}
        :param autoscaling_policy: autoscaling_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_group#autoscaling_policy ComputeNodeGroup#autoscaling_policy}
        :param description: An optional textual description of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_group#description ComputeNodeGroup#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_group#id ComputeNodeGroup#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param initial_size: The initial number of nodes in the node group. One of 'initial_size' or 'autoscaling_policy' must be configured on resource creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_group#initial_size ComputeNodeGroup#initial_size}
        :param maintenance_policy: Specifies how to handle instances when a node in the group undergoes maintenance. Set to one of: DEFAULT, RESTART_IN_PLACE, or MIGRATE_WITHIN_NODE_GROUP. The default value is DEFAULT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_group#maintenance_policy ComputeNodeGroup#maintenance_policy}
        :param maintenance_window: maintenance_window block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_group#maintenance_window ComputeNodeGroup#maintenance_window}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_group#project ComputeNodeGroup#project}.
        :param share_settings: share_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_group#share_settings ComputeNodeGroup#share_settings}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_group#timeouts ComputeNodeGroup#timeouts}
        :param zone: Zone where this node group is located. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_group#zone ComputeNodeGroup#zone}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3841bc26729c3d700213d99d04ec47ae06e9d47e3113a644e1b02e2c193d4f3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ComputeNodeGroupConfig(
            name=name,
            node_template=node_template,
            autoscaling_policy=autoscaling_policy,
            description=description,
            id=id,
            initial_size=initial_size,
            maintenance_policy=maintenance_policy,
            maintenance_window=maintenance_window,
            project=project,
            share_settings=share_settings,
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
        '''Generates CDKTF code for importing a ComputeNodeGroup resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ComputeNodeGroup to import.
        :param import_from_id: The id of the existing ComputeNodeGroup that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_group#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ComputeNodeGroup to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15e48e12670072a5bb859509769b88f8a7e74b2f7f46df14cf1a0a5e2823bd19)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAutoscalingPolicy")
    def put_autoscaling_policy(
        self,
        *,
        max_nodes: typing.Optional[jsii.Number] = None,
        min_nodes: typing.Optional[jsii.Number] = None,
        mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param max_nodes: Maximum size of the node group. Set to a value less than or equal to 100 and greater than or equal to min-nodes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_group#max_nodes ComputeNodeGroup#max_nodes}
        :param min_nodes: Minimum size of the node group. Must be less than or equal to max-nodes. The default value is 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_group#min_nodes ComputeNodeGroup#min_nodes}
        :param mode: The autoscaling mode. Set to one of the following: - OFF: Disables the autoscaler. - ON: Enables scaling in and scaling out. - ONLY_SCALE_OUT: Enables only scaling out. You must use this mode if your node groups are configured to restart their hosted VMs on minimal servers. Possible values: ["OFF", "ON", "ONLY_SCALE_OUT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_group#mode ComputeNodeGroup#mode}
        '''
        value = ComputeNodeGroupAutoscalingPolicy(
            max_nodes=max_nodes, min_nodes=min_nodes, mode=mode
        )

        return typing.cast(None, jsii.invoke(self, "putAutoscalingPolicy", [value]))

    @jsii.member(jsii_name="putMaintenanceWindow")
    def put_maintenance_window(self, *, start_time: builtins.str) -> None:
        '''
        :param start_time: instances.start time of the window. This must be in UTC format that resolves to one of 00:00, 04:00, 08:00, 12:00, 16:00, or 20:00. For example, both 13:00-5 and 08:00 are valid. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_group#start_time ComputeNodeGroup#start_time}
        '''
        value = ComputeNodeGroupMaintenanceWindow(start_time=start_time)

        return typing.cast(None, jsii.invoke(self, "putMaintenanceWindow", [value]))

    @jsii.member(jsii_name="putShareSettings")
    def put_share_settings(
        self,
        *,
        share_type: builtins.str,
        project_map: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeNodeGroupShareSettingsProjectMap", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param share_type: Node group sharing type. Possible values: ["ORGANIZATION", "SPECIFIC_PROJECTS", "LOCAL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_group#share_type ComputeNodeGroup#share_type}
        :param project_map: project_map block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_group#project_map ComputeNodeGroup#project_map}
        '''
        value = ComputeNodeGroupShareSettings(
            share_type=share_type, project_map=project_map
        )

        return typing.cast(None, jsii.invoke(self, "putShareSettings", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_group#create ComputeNodeGroup#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_group#delete ComputeNodeGroup#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_group#update ComputeNodeGroup#update}.
        '''
        value = ComputeNodeGroupTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAutoscalingPolicy")
    def reset_autoscaling_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoscalingPolicy", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInitialSize")
    def reset_initial_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInitialSize", []))

    @jsii.member(jsii_name="resetMaintenancePolicy")
    def reset_maintenance_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaintenancePolicy", []))

    @jsii.member(jsii_name="resetMaintenanceWindow")
    def reset_maintenance_window(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaintenanceWindow", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetShareSettings")
    def reset_share_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetShareSettings", []))

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
    @jsii.member(jsii_name="autoscalingPolicy")
    def autoscaling_policy(self) -> "ComputeNodeGroupAutoscalingPolicyOutputReference":
        return typing.cast("ComputeNodeGroupAutoscalingPolicyOutputReference", jsii.get(self, "autoscalingPolicy"))

    @builtins.property
    @jsii.member(jsii_name="creationTimestamp")
    def creation_timestamp(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "creationTimestamp"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceWindow")
    def maintenance_window(self) -> "ComputeNodeGroupMaintenanceWindowOutputReference":
        return typing.cast("ComputeNodeGroupMaintenanceWindowOutputReference", jsii.get(self, "maintenanceWindow"))

    @builtins.property
    @jsii.member(jsii_name="selfLink")
    def self_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selfLink"))

    @builtins.property
    @jsii.member(jsii_name="shareSettings")
    def share_settings(self) -> "ComputeNodeGroupShareSettingsOutputReference":
        return typing.cast("ComputeNodeGroupShareSettingsOutputReference", jsii.get(self, "shareSettings"))

    @builtins.property
    @jsii.member(jsii_name="size")
    def size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "size"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ComputeNodeGroupTimeoutsOutputReference":
        return typing.cast("ComputeNodeGroupTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="autoscalingPolicyInput")
    def autoscaling_policy_input(
        self,
    ) -> typing.Optional["ComputeNodeGroupAutoscalingPolicy"]:
        return typing.cast(typing.Optional["ComputeNodeGroupAutoscalingPolicy"], jsii.get(self, "autoscalingPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="initialSizeInput")
    def initial_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "initialSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="maintenancePolicyInput")
    def maintenance_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maintenancePolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceWindowInput")
    def maintenance_window_input(
        self,
    ) -> typing.Optional["ComputeNodeGroupMaintenanceWindow"]:
        return typing.cast(typing.Optional["ComputeNodeGroupMaintenanceWindow"], jsii.get(self, "maintenanceWindowInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeTemplateInput")
    def node_template_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nodeTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="shareSettingsInput")
    def share_settings_input(self) -> typing.Optional["ComputeNodeGroupShareSettings"]:
        return typing.cast(typing.Optional["ComputeNodeGroupShareSettings"], jsii.get(self, "shareSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeNodeGroupTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeNodeGroupTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="zoneInput")
    def zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "zoneInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4e3fc068c0f6370e1f6cd841f01680a82559ce82678a9079e3200dc350e4064)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f27d302713195d2fe051f32173e56a179d1960e13cd1fdc2dccaa3df0bda7384)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="initialSize")
    def initial_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "initialSize"))

    @initial_size.setter
    def initial_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6baa6d5367f685f09ee63aec5505ec4d7862e75b151a6eea71bbccbeec83b08b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initialSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maintenancePolicy")
    def maintenance_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maintenancePolicy"))

    @maintenance_policy.setter
    def maintenance_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__934b6d9f5a3696cf9acbf136266248f42b2978094d6fcead1b4f5d8840d160f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maintenancePolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6dd59dad3fa3a29d5441a0fc0ade83b36d57e55fe05f91a7601b4bc4e765d990)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeTemplate")
    def node_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeTemplate"))

    @node_template.setter
    def node_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f8da1f8f2b13d74909d203c6b5125299db11a5c8c2d79dd0b2392fe1c14b233)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeTemplate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3422f36fb85edfb876d7ebcad1a11b3b36c33407d56bf0cf69147db8cbbe2312)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zone")
    def zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zone"))

    @zone.setter
    def zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe52f6c8652e6c9be6ea5a53c86cb38c1a335d58dfbec40b766e52496268f4b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zone", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeNodeGroup.ComputeNodeGroupAutoscalingPolicy",
    jsii_struct_bases=[],
    name_mapping={"max_nodes": "maxNodes", "min_nodes": "minNodes", "mode": "mode"},
)
class ComputeNodeGroupAutoscalingPolicy:
    def __init__(
        self,
        *,
        max_nodes: typing.Optional[jsii.Number] = None,
        min_nodes: typing.Optional[jsii.Number] = None,
        mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param max_nodes: Maximum size of the node group. Set to a value less than or equal to 100 and greater than or equal to min-nodes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_group#max_nodes ComputeNodeGroup#max_nodes}
        :param min_nodes: Minimum size of the node group. Must be less than or equal to max-nodes. The default value is 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_group#min_nodes ComputeNodeGroup#min_nodes}
        :param mode: The autoscaling mode. Set to one of the following: - OFF: Disables the autoscaler. - ON: Enables scaling in and scaling out. - ONLY_SCALE_OUT: Enables only scaling out. You must use this mode if your node groups are configured to restart their hosted VMs on minimal servers. Possible values: ["OFF", "ON", "ONLY_SCALE_OUT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_group#mode ComputeNodeGroup#mode}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9caaefa03175a20b73f0439620dce227c4bb8634ea25d58a8c888058a4bf0189)
            check_type(argname="argument max_nodes", value=max_nodes, expected_type=type_hints["max_nodes"])
            check_type(argname="argument min_nodes", value=min_nodes, expected_type=type_hints["min_nodes"])
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_nodes is not None:
            self._values["max_nodes"] = max_nodes
        if min_nodes is not None:
            self._values["min_nodes"] = min_nodes
        if mode is not None:
            self._values["mode"] = mode

    @builtins.property
    def max_nodes(self) -> typing.Optional[jsii.Number]:
        '''Maximum size of the node group.

        Set to a value less than or equal
        to 100 and greater than or equal to min-nodes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_group#max_nodes ComputeNodeGroup#max_nodes}
        '''
        result = self._values.get("max_nodes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_nodes(self) -> typing.Optional[jsii.Number]:
        '''Minimum size of the node group. Must be less than or equal to max-nodes. The default value is 0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_group#min_nodes ComputeNodeGroup#min_nodes}
        '''
        result = self._values.get("min_nodes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''The autoscaling mode.

        Set to one of the following:

        - OFF: Disables the autoscaler.
        - ON: Enables scaling in and scaling out.
        - ONLY_SCALE_OUT: Enables only scaling out.
          You must use this mode if your node groups are configured to
          restart their hosted VMs on minimal servers. Possible values: ["OFF", "ON", "ONLY_SCALE_OUT"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_group#mode ComputeNodeGroup#mode}
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeNodeGroupAutoscalingPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeNodeGroupAutoscalingPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeNodeGroup.ComputeNodeGroupAutoscalingPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__39d1644e539ee21ac567be25863734d4dc04874dc38659e997d332e3d105c79b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMaxNodes")
    def reset_max_nodes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxNodes", []))

    @jsii.member(jsii_name="resetMinNodes")
    def reset_min_nodes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinNodes", []))

    @jsii.member(jsii_name="resetMode")
    def reset_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMode", []))

    @builtins.property
    @jsii.member(jsii_name="maxNodesInput")
    def max_nodes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxNodesInput"))

    @builtins.property
    @jsii.member(jsii_name="minNodesInput")
    def min_nodes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minNodesInput"))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="maxNodes")
    def max_nodes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxNodes"))

    @max_nodes.setter
    def max_nodes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51e55d58bde0c13748c2603acd11e32e52df7ceb1c500a64a91a6433d0a3839e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxNodes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minNodes")
    def min_nodes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minNodes"))

    @min_nodes.setter
    def min_nodes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a0e9fd5ad2e8f83ebe2230578aea0746d57410375f31a922552308a1e34e270)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minNodes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75031449e639ce7af1a2d644c5b8aee81dba090a6c91e9f371548870ec441c1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeNodeGroupAutoscalingPolicy]:
        return typing.cast(typing.Optional[ComputeNodeGroupAutoscalingPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeNodeGroupAutoscalingPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de5a18329b26f8527345f3d95856b06b40f8c3b23967c62fbdd293a958ec89e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeNodeGroup.ComputeNodeGroupConfig",
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
        "node_template": "nodeTemplate",
        "autoscaling_policy": "autoscalingPolicy",
        "description": "description",
        "id": "id",
        "initial_size": "initialSize",
        "maintenance_policy": "maintenancePolicy",
        "maintenance_window": "maintenanceWindow",
        "project": "project",
        "share_settings": "shareSettings",
        "timeouts": "timeouts",
        "zone": "zone",
    },
)
class ComputeNodeGroupConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        node_template: builtins.str,
        autoscaling_policy: typing.Optional[typing.Union[ComputeNodeGroupAutoscalingPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        initial_size: typing.Optional[jsii.Number] = None,
        maintenance_policy: typing.Optional[builtins.str] = None,
        maintenance_window: typing.Optional[typing.Union["ComputeNodeGroupMaintenanceWindow", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        share_settings: typing.Optional[typing.Union["ComputeNodeGroupShareSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["ComputeNodeGroupTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
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
        :param name: Name of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_group#name ComputeNodeGroup#name}
        :param node_template: The URL of the node template to which this node group belongs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_group#node_template ComputeNodeGroup#node_template}
        :param autoscaling_policy: autoscaling_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_group#autoscaling_policy ComputeNodeGroup#autoscaling_policy}
        :param description: An optional textual description of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_group#description ComputeNodeGroup#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_group#id ComputeNodeGroup#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param initial_size: The initial number of nodes in the node group. One of 'initial_size' or 'autoscaling_policy' must be configured on resource creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_group#initial_size ComputeNodeGroup#initial_size}
        :param maintenance_policy: Specifies how to handle instances when a node in the group undergoes maintenance. Set to one of: DEFAULT, RESTART_IN_PLACE, or MIGRATE_WITHIN_NODE_GROUP. The default value is DEFAULT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_group#maintenance_policy ComputeNodeGroup#maintenance_policy}
        :param maintenance_window: maintenance_window block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_group#maintenance_window ComputeNodeGroup#maintenance_window}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_group#project ComputeNodeGroup#project}.
        :param share_settings: share_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_group#share_settings ComputeNodeGroup#share_settings}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_group#timeouts ComputeNodeGroup#timeouts}
        :param zone: Zone where this node group is located. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_group#zone ComputeNodeGroup#zone}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(autoscaling_policy, dict):
            autoscaling_policy = ComputeNodeGroupAutoscalingPolicy(**autoscaling_policy)
        if isinstance(maintenance_window, dict):
            maintenance_window = ComputeNodeGroupMaintenanceWindow(**maintenance_window)
        if isinstance(share_settings, dict):
            share_settings = ComputeNodeGroupShareSettings(**share_settings)
        if isinstance(timeouts, dict):
            timeouts = ComputeNodeGroupTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d81395937796b537b5699ae7dcb3363f7463907d4a2dc7684581ec31cfaa999)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument node_template", value=node_template, expected_type=type_hints["node_template"])
            check_type(argname="argument autoscaling_policy", value=autoscaling_policy, expected_type=type_hints["autoscaling_policy"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument initial_size", value=initial_size, expected_type=type_hints["initial_size"])
            check_type(argname="argument maintenance_policy", value=maintenance_policy, expected_type=type_hints["maintenance_policy"])
            check_type(argname="argument maintenance_window", value=maintenance_window, expected_type=type_hints["maintenance_window"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument share_settings", value=share_settings, expected_type=type_hints["share_settings"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument zone", value=zone, expected_type=type_hints["zone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "node_template": node_template,
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
        if autoscaling_policy is not None:
            self._values["autoscaling_policy"] = autoscaling_policy
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if initial_size is not None:
            self._values["initial_size"] = initial_size
        if maintenance_policy is not None:
            self._values["maintenance_policy"] = maintenance_policy
        if maintenance_window is not None:
            self._values["maintenance_window"] = maintenance_window
        if project is not None:
            self._values["project"] = project
        if share_settings is not None:
            self._values["share_settings"] = share_settings
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
    def name(self) -> builtins.str:
        '''Name of the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_group#name ComputeNodeGroup#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def node_template(self) -> builtins.str:
        '''The URL of the node template to which this node group belongs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_group#node_template ComputeNodeGroup#node_template}
        '''
        result = self._values.get("node_template")
        assert result is not None, "Required property 'node_template' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def autoscaling_policy(self) -> typing.Optional[ComputeNodeGroupAutoscalingPolicy]:
        '''autoscaling_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_group#autoscaling_policy ComputeNodeGroup#autoscaling_policy}
        '''
        result = self._values.get("autoscaling_policy")
        return typing.cast(typing.Optional[ComputeNodeGroupAutoscalingPolicy], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional textual description of the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_group#description ComputeNodeGroup#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_group#id ComputeNodeGroup#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def initial_size(self) -> typing.Optional[jsii.Number]:
        '''The initial number of nodes in the node group.

        One of 'initial_size' or 'autoscaling_policy' must be configured on resource creation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_group#initial_size ComputeNodeGroup#initial_size}
        '''
        result = self._values.get("initial_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def maintenance_policy(self) -> typing.Optional[builtins.str]:
        '''Specifies how to handle instances when a node in the group undergoes maintenance.

        Set to one of: DEFAULT, RESTART_IN_PLACE, or MIGRATE_WITHIN_NODE_GROUP. The default value is DEFAULT.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_group#maintenance_policy ComputeNodeGroup#maintenance_policy}
        '''
        result = self._values.get("maintenance_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maintenance_window(
        self,
    ) -> typing.Optional["ComputeNodeGroupMaintenanceWindow"]:
        '''maintenance_window block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_group#maintenance_window ComputeNodeGroup#maintenance_window}
        '''
        result = self._values.get("maintenance_window")
        return typing.cast(typing.Optional["ComputeNodeGroupMaintenanceWindow"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_group#project ComputeNodeGroup#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def share_settings(self) -> typing.Optional["ComputeNodeGroupShareSettings"]:
        '''share_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_group#share_settings ComputeNodeGroup#share_settings}
        '''
        result = self._values.get("share_settings")
        return typing.cast(typing.Optional["ComputeNodeGroupShareSettings"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ComputeNodeGroupTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_group#timeouts ComputeNodeGroup#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ComputeNodeGroupTimeouts"], result)

    @builtins.property
    def zone(self) -> typing.Optional[builtins.str]:
        '''Zone where this node group is located.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_group#zone ComputeNodeGroup#zone}
        '''
        result = self._values.get("zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeNodeGroupConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeNodeGroup.ComputeNodeGroupMaintenanceWindow",
    jsii_struct_bases=[],
    name_mapping={"start_time": "startTime"},
)
class ComputeNodeGroupMaintenanceWindow:
    def __init__(self, *, start_time: builtins.str) -> None:
        '''
        :param start_time: instances.start time of the window. This must be in UTC format that resolves to one of 00:00, 04:00, 08:00, 12:00, 16:00, or 20:00. For example, both 13:00-5 and 08:00 are valid. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_group#start_time ComputeNodeGroup#start_time}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eec3f6f98265e2abfa9d8afd34d49fbfdb389ca42cc77ec0db424f3e3e30560c)
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "start_time": start_time,
        }

    @builtins.property
    def start_time(self) -> builtins.str:
        '''instances.start time of the window. This must be in UTC format that resolves to one of 00:00, 04:00, 08:00, 12:00, 16:00, or 20:00. For example, both 13:00-5 and 08:00 are valid.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_group#start_time ComputeNodeGroup#start_time}
        '''
        result = self._values.get("start_time")
        assert result is not None, "Required property 'start_time' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeNodeGroupMaintenanceWindow(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeNodeGroupMaintenanceWindowOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeNodeGroup.ComputeNodeGroupMaintenanceWindowOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__029243ee7f80e2cc05bb132715c3098fcfe7f5097ffa25a990367adb0544ddff)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="startTimeInput")
    def start_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8acd49a61675449e9aafbc9d163efeccf93e164956680343d94f9b471a45f9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeNodeGroupMaintenanceWindow]:
        return typing.cast(typing.Optional[ComputeNodeGroupMaintenanceWindow], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeNodeGroupMaintenanceWindow],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a19687bf71b64081508ee4acdd2a2dc97a1b11b216883d73a2b97c20a677f4d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeNodeGroup.ComputeNodeGroupShareSettings",
    jsii_struct_bases=[],
    name_mapping={"share_type": "shareType", "project_map": "projectMap"},
)
class ComputeNodeGroupShareSettings:
    def __init__(
        self,
        *,
        share_type: builtins.str,
        project_map: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeNodeGroupShareSettingsProjectMap", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param share_type: Node group sharing type. Possible values: ["ORGANIZATION", "SPECIFIC_PROJECTS", "LOCAL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_group#share_type ComputeNodeGroup#share_type}
        :param project_map: project_map block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_group#project_map ComputeNodeGroup#project_map}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46cffd27bf45857d0fd173adabc90cd505910afd1ae138dabe9ae3eb61ec3b13)
            check_type(argname="argument share_type", value=share_type, expected_type=type_hints["share_type"])
            check_type(argname="argument project_map", value=project_map, expected_type=type_hints["project_map"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "share_type": share_type,
        }
        if project_map is not None:
            self._values["project_map"] = project_map

    @builtins.property
    def share_type(self) -> builtins.str:
        '''Node group sharing type. Possible values: ["ORGANIZATION", "SPECIFIC_PROJECTS", "LOCAL"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_group#share_type ComputeNodeGroup#share_type}
        '''
        result = self._values.get("share_type")
        assert result is not None, "Required property 'share_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_map(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeNodeGroupShareSettingsProjectMap"]]]:
        '''project_map block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_group#project_map ComputeNodeGroup#project_map}
        '''
        result = self._values.get("project_map")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeNodeGroupShareSettingsProjectMap"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeNodeGroupShareSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeNodeGroupShareSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeNodeGroup.ComputeNodeGroupShareSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__12dfdf2cae22537cd739c43d958dcd3ad6de90edf948d6a00b6c9952e6719815)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putProjectMap")
    def put_project_map(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeNodeGroupShareSettingsProjectMap", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12a89dd6446d0af76e1af418a4017904db7b18bcbd28c56c02debbc35ff1f0b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putProjectMap", [value]))

    @jsii.member(jsii_name="resetProjectMap")
    def reset_project_map(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProjectMap", []))

    @builtins.property
    @jsii.member(jsii_name="projectMap")
    def project_map(self) -> "ComputeNodeGroupShareSettingsProjectMapList":
        return typing.cast("ComputeNodeGroupShareSettingsProjectMapList", jsii.get(self, "projectMap"))

    @builtins.property
    @jsii.member(jsii_name="projectMapInput")
    def project_map_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeNodeGroupShareSettingsProjectMap"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeNodeGroupShareSettingsProjectMap"]]], jsii.get(self, "projectMapInput"))

    @builtins.property
    @jsii.member(jsii_name="shareTypeInput")
    def share_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "shareTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="shareType")
    def share_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "shareType"))

    @share_type.setter
    def share_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50a4cb07fae54ee701295411b1b62809887c6b2a6a3c4b1476d8f9e51a7c5601)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "shareType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeNodeGroupShareSettings]:
        return typing.cast(typing.Optional[ComputeNodeGroupShareSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeNodeGroupShareSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2010e9e0131cab93500ee08a2a9554c5ad6fd6bc9c2b760b07cb3edef685df7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeNodeGroup.ComputeNodeGroupShareSettingsProjectMap",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "project_id": "projectId"},
)
class ComputeNodeGroupShareSettingsProjectMap:
    def __init__(self, *, id: builtins.str, project_id: builtins.str) -> None:
        '''
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_group#id ComputeNodeGroup#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project_id: The project id/number should be the same as the key of this project config in the project map. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_group#project_id ComputeNodeGroup#project_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa105f3fae893e9560c64591fe087e5c24a15425f13e46da0951c979e37366a0)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
            "project_id": project_id,
        }

    @builtins.property
    def id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_group#id ComputeNodeGroup#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_id(self) -> builtins.str:
        '''The project id/number should be the same as the key of this project config in the project map.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_group#project_id ComputeNodeGroup#project_id}
        '''
        result = self._values.get("project_id")
        assert result is not None, "Required property 'project_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeNodeGroupShareSettingsProjectMap(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeNodeGroupShareSettingsProjectMapList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeNodeGroup.ComputeNodeGroupShareSettingsProjectMapList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f5f084178c5a9ebc048c7c387e04a17254900939a2c89b7f412d39b2bc6de26)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeNodeGroupShareSettingsProjectMapOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6cee4d0a78b1b5778bf49315c1da3677b090aebcba774631435b3b57aae0157)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeNodeGroupShareSettingsProjectMapOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__320cab66d03c7b996c542da65451f9180b8eff98d10dce5658a2087925bd9e24)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f7e4efe259b814ae1826a44ba2cf4ab288d61697d503be916ae165fc560ac8ca)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a945158b94e15e0cc64cf177c8cbe9ba1857c55d250a82b576228369ff5170e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeNodeGroupShareSettingsProjectMap]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeNodeGroupShareSettingsProjectMap]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeNodeGroupShareSettingsProjectMap]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77d54d12479baf25b7a1415ace264322800e438caadb3c89503f85193b794c86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeNodeGroupShareSettingsProjectMapOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeNodeGroup.ComputeNodeGroupShareSettingsProjectMapOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f36fe30444ce6e3607db97cc4075823e133ca17f92e3770c74f01a696ab5479a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fab2f440d80a534209840c3f5bd5b6c5af96fa3b568d6d542130eeef8353e4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf3fd3cccf7021c310fee287aaa335ee1d82406fe5ce1e58859a2e991573e73d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeNodeGroupShareSettingsProjectMap]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeNodeGroupShareSettingsProjectMap]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeNodeGroupShareSettingsProjectMap]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87fd356c5e17d2d386f5e196e366a061d7b38448e4d545f64d1e879b4c9a7376)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeNodeGroup.ComputeNodeGroupTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ComputeNodeGroupTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_group#create ComputeNodeGroup#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_group#delete ComputeNodeGroup#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_group#update ComputeNodeGroup#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1abe21e32df89cf947c56e3686a6d9fede9a4f1ce7fcb2749f7bbea63987e726)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_group#create ComputeNodeGroup#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_group#delete ComputeNodeGroup#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_group#update ComputeNodeGroup#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeNodeGroupTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeNodeGroupTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeNodeGroup.ComputeNodeGroupTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5930ab8751ab27572b5d88f2b9a3c7b0c71ef1b7856efb3464b26314ede3dd7e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__90a758ddc04e89d9bf0185dc7a3b87a3058440a1713234301e2b0deb1e06f9ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e005840e776b3f9ad07884c69b4445ed240b0af828a172435838163e6e3e39f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a9b908bd725cef5cf86ac9e35af772ee3913fc01f0aa91059329de166531db5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeNodeGroupTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeNodeGroupTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeNodeGroupTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06736d1b9f3e3c8d70a70faa732438f424f4a6028d144d55fc124aac2b29891b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ComputeNodeGroup",
    "ComputeNodeGroupAutoscalingPolicy",
    "ComputeNodeGroupAutoscalingPolicyOutputReference",
    "ComputeNodeGroupConfig",
    "ComputeNodeGroupMaintenanceWindow",
    "ComputeNodeGroupMaintenanceWindowOutputReference",
    "ComputeNodeGroupShareSettings",
    "ComputeNodeGroupShareSettingsOutputReference",
    "ComputeNodeGroupShareSettingsProjectMap",
    "ComputeNodeGroupShareSettingsProjectMapList",
    "ComputeNodeGroupShareSettingsProjectMapOutputReference",
    "ComputeNodeGroupTimeouts",
    "ComputeNodeGroupTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__b3841bc26729c3d700213d99d04ec47ae06e9d47e3113a644e1b02e2c193d4f3(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    node_template: builtins.str,
    autoscaling_policy: typing.Optional[typing.Union[ComputeNodeGroupAutoscalingPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    initial_size: typing.Optional[jsii.Number] = None,
    maintenance_policy: typing.Optional[builtins.str] = None,
    maintenance_window: typing.Optional[typing.Union[ComputeNodeGroupMaintenanceWindow, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    share_settings: typing.Optional[typing.Union[ComputeNodeGroupShareSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[ComputeNodeGroupTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__15e48e12670072a5bb859509769b88f8a7e74b2f7f46df14cf1a0a5e2823bd19(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4e3fc068c0f6370e1f6cd841f01680a82559ce82678a9079e3200dc350e4064(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f27d302713195d2fe051f32173e56a179d1960e13cd1fdc2dccaa3df0bda7384(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6baa6d5367f685f09ee63aec5505ec4d7862e75b151a6eea71bbccbeec83b08b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__934b6d9f5a3696cf9acbf136266248f42b2978094d6fcead1b4f5d8840d160f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dd59dad3fa3a29d5441a0fc0ade83b36d57e55fe05f91a7601b4bc4e765d990(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f8da1f8f2b13d74909d203c6b5125299db11a5c8c2d79dd0b2392fe1c14b233(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3422f36fb85edfb876d7ebcad1a11b3b36c33407d56bf0cf69147db8cbbe2312(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe52f6c8652e6c9be6ea5a53c86cb38c1a335d58dfbec40b766e52496268f4b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9caaefa03175a20b73f0439620dce227c4bb8634ea25d58a8c888058a4bf0189(
    *,
    max_nodes: typing.Optional[jsii.Number] = None,
    min_nodes: typing.Optional[jsii.Number] = None,
    mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39d1644e539ee21ac567be25863734d4dc04874dc38659e997d332e3d105c79b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51e55d58bde0c13748c2603acd11e32e52df7ceb1c500a64a91a6433d0a3839e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a0e9fd5ad2e8f83ebe2230578aea0746d57410375f31a922552308a1e34e270(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75031449e639ce7af1a2d644c5b8aee81dba090a6c91e9f371548870ec441c1e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de5a18329b26f8527345f3d95856b06b40f8c3b23967c62fbdd293a958ec89e7(
    value: typing.Optional[ComputeNodeGroupAutoscalingPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d81395937796b537b5699ae7dcb3363f7463907d4a2dc7684581ec31cfaa999(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    node_template: builtins.str,
    autoscaling_policy: typing.Optional[typing.Union[ComputeNodeGroupAutoscalingPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    initial_size: typing.Optional[jsii.Number] = None,
    maintenance_policy: typing.Optional[builtins.str] = None,
    maintenance_window: typing.Optional[typing.Union[ComputeNodeGroupMaintenanceWindow, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    share_settings: typing.Optional[typing.Union[ComputeNodeGroupShareSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[ComputeNodeGroupTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eec3f6f98265e2abfa9d8afd34d49fbfdb389ca42cc77ec0db424f3e3e30560c(
    *,
    start_time: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__029243ee7f80e2cc05bb132715c3098fcfe7f5097ffa25a990367adb0544ddff(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8acd49a61675449e9aafbc9d163efeccf93e164956680343d94f9b471a45f9a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a19687bf71b64081508ee4acdd2a2dc97a1b11b216883d73a2b97c20a677f4d8(
    value: typing.Optional[ComputeNodeGroupMaintenanceWindow],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46cffd27bf45857d0fd173adabc90cd505910afd1ae138dabe9ae3eb61ec3b13(
    *,
    share_type: builtins.str,
    project_map: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeNodeGroupShareSettingsProjectMap, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12dfdf2cae22537cd739c43d958dcd3ad6de90edf948d6a00b6c9952e6719815(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12a89dd6446d0af76e1af418a4017904db7b18bcbd28c56c02debbc35ff1f0b7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeNodeGroupShareSettingsProjectMap, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50a4cb07fae54ee701295411b1b62809887c6b2a6a3c4b1476d8f9e51a7c5601(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2010e9e0131cab93500ee08a2a9554c5ad6fd6bc9c2b760b07cb3edef685df7e(
    value: typing.Optional[ComputeNodeGroupShareSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa105f3fae893e9560c64591fe087e5c24a15425f13e46da0951c979e37366a0(
    *,
    id: builtins.str,
    project_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f5f084178c5a9ebc048c7c387e04a17254900939a2c89b7f412d39b2bc6de26(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6cee4d0a78b1b5778bf49315c1da3677b090aebcba774631435b3b57aae0157(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__320cab66d03c7b996c542da65451f9180b8eff98d10dce5658a2087925bd9e24(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7e4efe259b814ae1826a44ba2cf4ab288d61697d503be916ae165fc560ac8ca(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a945158b94e15e0cc64cf177c8cbe9ba1857c55d250a82b576228369ff5170e8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77d54d12479baf25b7a1415ace264322800e438caadb3c89503f85193b794c86(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeNodeGroupShareSettingsProjectMap]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f36fe30444ce6e3607db97cc4075823e133ca17f92e3770c74f01a696ab5479a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fab2f440d80a534209840c3f5bd5b6c5af96fa3b568d6d542130eeef8353e4d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf3fd3cccf7021c310fee287aaa335ee1d82406fe5ce1e58859a2e991573e73d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87fd356c5e17d2d386f5e196e366a061d7b38448e4d545f64d1e879b4c9a7376(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeNodeGroupShareSettingsProjectMap]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1abe21e32df89cf947c56e3686a6d9fede9a4f1ce7fcb2749f7bbea63987e726(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5930ab8751ab27572b5d88f2b9a3c7b0c71ef1b7856efb3464b26314ede3dd7e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90a758ddc04e89d9bf0185dc7a3b87a3058440a1713234301e2b0deb1e06f9ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e005840e776b3f9ad07884c69b4445ed240b0af828a172435838163e6e3e39f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a9b908bd725cef5cf86ac9e35af772ee3913fc01f0aa91059329de166531db5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06736d1b9f3e3c8d70a70faa732438f424f4a6028d144d55fc124aac2b29891b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeNodeGroupTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
