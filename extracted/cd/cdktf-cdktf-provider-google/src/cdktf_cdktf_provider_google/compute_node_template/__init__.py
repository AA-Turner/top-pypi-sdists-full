r'''
# `google_compute_node_template`

Refer to the Terraform Registry for docs: [`google_compute_node_template`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_template).
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


class ComputeNodeTemplate(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeNodeTemplate.ComputeNodeTemplate",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_template google_compute_node_template}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        accelerators: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeNodeTemplateAccelerators", typing.Dict[builtins.str, typing.Any]]]]] = None,
        cpu_overcommit_type: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        disks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeNodeTemplateDisks", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        node_affinity_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        node_type: typing.Optional[builtins.str] = None,
        node_type_flexibility: typing.Optional[typing.Union["ComputeNodeTemplateNodeTypeFlexibility", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        server_binding: typing.Optional[typing.Union["ComputeNodeTemplateServerBinding", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["ComputeNodeTemplateTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_template google_compute_node_template} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Name of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_template#name ComputeNodeTemplate#name}
        :param accelerators: accelerators block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_template#accelerators ComputeNodeTemplate#accelerators}
        :param cpu_overcommit_type: CPU overcommit. Default value: "NONE" Possible values: ["ENABLED", "NONE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_template#cpu_overcommit_type ComputeNodeTemplate#cpu_overcommit_type}
        :param description: An optional textual description of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_template#description ComputeNodeTemplate#description}
        :param disks: disks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_template#disks ComputeNodeTemplate#disks}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_template#id ComputeNodeTemplate#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param node_affinity_labels: Labels to use for node affinity, which will be used in instance scheduling. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_template#node_affinity_labels ComputeNodeTemplate#node_affinity_labels}
        :param node_type: Node type to use for nodes group that are created from this template. Only one of nodeTypeFlexibility and nodeType can be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_template#node_type ComputeNodeTemplate#node_type}
        :param node_type_flexibility: node_type_flexibility block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_template#node_type_flexibility ComputeNodeTemplate#node_type_flexibility}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_template#project ComputeNodeTemplate#project}.
        :param region: Region where nodes using the node template will be created. If it is not provided, the provider region is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_template#region ComputeNodeTemplate#region}
        :param server_binding: server_binding block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_template#server_binding ComputeNodeTemplate#server_binding}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_template#timeouts ComputeNodeTemplate#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5a7fd3496aa64577524335df376838dc98d6ec71472a09fc5b8f9afe09fa14d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ComputeNodeTemplateConfig(
            name=name,
            accelerators=accelerators,
            cpu_overcommit_type=cpu_overcommit_type,
            description=description,
            disks=disks,
            id=id,
            node_affinity_labels=node_affinity_labels,
            node_type=node_type,
            node_type_flexibility=node_type_flexibility,
            project=project,
            region=region,
            server_binding=server_binding,
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
        '''Generates CDKTF code for importing a ComputeNodeTemplate resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ComputeNodeTemplate to import.
        :param import_from_id: The id of the existing ComputeNodeTemplate that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_template#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ComputeNodeTemplate to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9af846e6a9a50608e7ef3f89c02826edf61e860afb3d4bd586bcd3a4425b008d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAccelerators")
    def put_accelerators(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeNodeTemplateAccelerators", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4df88687b58ecb36d37492a9c791cd54ea86a1ff6458d6af64f2b435ddb43912)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAccelerators", [value]))

    @jsii.member(jsii_name="putDisks")
    def put_disks(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeNodeTemplateDisks", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8afb67bb2633f6d8ba387dc8ea9b9af489280e17725fa9057abf19a9898bb496)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDisks", [value]))

    @jsii.member(jsii_name="putNodeTypeFlexibility")
    def put_node_type_flexibility(
        self,
        *,
        cpus: typing.Optional[builtins.str] = None,
        memory: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cpus: Number of virtual CPUs to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_template#cpus ComputeNodeTemplate#cpus}
        :param memory: Physical memory available to the node, defined in MB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_template#memory ComputeNodeTemplate#memory}
        '''
        value = ComputeNodeTemplateNodeTypeFlexibility(cpus=cpus, memory=memory)

        return typing.cast(None, jsii.invoke(self, "putNodeTypeFlexibility", [value]))

    @jsii.member(jsii_name="putServerBinding")
    def put_server_binding(self, *, type: builtins.str) -> None:
        '''
        :param type: Type of server binding policy. If 'RESTART_NODE_ON_ANY_SERVER', nodes using this template will restart on any physical server following a maintenance event. If 'RESTART_NODE_ON_MINIMAL_SERVER', nodes using this template will restart on the same physical server following a maintenance event, instead of being live migrated to or restarted on a new physical server. This option may be useful if you are using software licenses tied to the underlying server characteristics such as physical sockets or cores, to avoid the need for additional licenses when maintenance occurs. However, VMs on such nodes will experience outages while maintenance is applied. Possible values: ["RESTART_NODE_ON_ANY_SERVER", "RESTART_NODE_ON_MINIMAL_SERVERS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_template#type ComputeNodeTemplate#type}
        '''
        value = ComputeNodeTemplateServerBinding(type=type)

        return typing.cast(None, jsii.invoke(self, "putServerBinding", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_template#create ComputeNodeTemplate#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_template#delete ComputeNodeTemplate#delete}.
        '''
        value = ComputeNodeTemplateTimeouts(create=create, delete=delete)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAccelerators")
    def reset_accelerators(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccelerators", []))

    @jsii.member(jsii_name="resetCpuOvercommitType")
    def reset_cpu_overcommit_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpuOvercommitType", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDisks")
    def reset_disks(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisks", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetNodeAffinityLabels")
    def reset_node_affinity_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeAffinityLabels", []))

    @jsii.member(jsii_name="resetNodeType")
    def reset_node_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeType", []))

    @jsii.member(jsii_name="resetNodeTypeFlexibility")
    def reset_node_type_flexibility(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeTypeFlexibility", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetServerBinding")
    def reset_server_binding(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServerBinding", []))

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
    @jsii.member(jsii_name="accelerators")
    def accelerators(self) -> "ComputeNodeTemplateAcceleratorsList":
        return typing.cast("ComputeNodeTemplateAcceleratorsList", jsii.get(self, "accelerators"))

    @builtins.property
    @jsii.member(jsii_name="creationTimestamp")
    def creation_timestamp(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "creationTimestamp"))

    @builtins.property
    @jsii.member(jsii_name="disks")
    def disks(self) -> "ComputeNodeTemplateDisksList":
        return typing.cast("ComputeNodeTemplateDisksList", jsii.get(self, "disks"))

    @builtins.property
    @jsii.member(jsii_name="nodeTypeFlexibility")
    def node_type_flexibility(
        self,
    ) -> "ComputeNodeTemplateNodeTypeFlexibilityOutputReference":
        return typing.cast("ComputeNodeTemplateNodeTypeFlexibilityOutputReference", jsii.get(self, "nodeTypeFlexibility"))

    @builtins.property
    @jsii.member(jsii_name="selfLink")
    def self_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selfLink"))

    @builtins.property
    @jsii.member(jsii_name="serverBinding")
    def server_binding(self) -> "ComputeNodeTemplateServerBindingOutputReference":
        return typing.cast("ComputeNodeTemplateServerBindingOutputReference", jsii.get(self, "serverBinding"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ComputeNodeTemplateTimeoutsOutputReference":
        return typing.cast("ComputeNodeTemplateTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="acceleratorsInput")
    def accelerators_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeNodeTemplateAccelerators"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeNodeTemplateAccelerators"]]], jsii.get(self, "acceleratorsInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuOvercommitTypeInput")
    def cpu_overcommit_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cpuOvercommitTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="disksInput")
    def disks_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeNodeTemplateDisks"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeNodeTemplateDisks"]]], jsii.get(self, "disksInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeAffinityLabelsInput")
    def node_affinity_labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "nodeAffinityLabelsInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeTypeFlexibilityInput")
    def node_type_flexibility_input(
        self,
    ) -> typing.Optional["ComputeNodeTemplateNodeTypeFlexibility"]:
        return typing.cast(typing.Optional["ComputeNodeTemplateNodeTypeFlexibility"], jsii.get(self, "nodeTypeFlexibilityInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeTypeInput")
    def node_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nodeTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="serverBindingInput")
    def server_binding_input(
        self,
    ) -> typing.Optional["ComputeNodeTemplateServerBinding"]:
        return typing.cast(typing.Optional["ComputeNodeTemplateServerBinding"], jsii.get(self, "serverBindingInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeNodeTemplateTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeNodeTemplateTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuOvercommitType")
    def cpu_overcommit_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cpuOvercommitType"))

    @cpu_overcommit_type.setter
    def cpu_overcommit_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5d712415022023d522e69564f9019cdf851b9002c33313e386bfc723e0f02e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuOvercommitType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28ac3c3079370c43fdbf841b600c0bfe3e2c9d870462424e8654ce67a2645b41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84a0f5120ed469cdbebfc8950b0579d11e194d769bed485d6c1a56c13ac9e842)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6201fd4ba29837e86bf3e0ed9588c0a3fbc74732c167f9d99296aa13041a9780)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeAffinityLabels")
    def node_affinity_labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "nodeAffinityLabels"))

    @node_affinity_labels.setter
    def node_affinity_labels(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1409542951ff74adc9a708ac250baf154c0386d25582cd8ca0ce30279ffb77a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeAffinityLabels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeType")
    def node_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeType"))

    @node_type.setter
    def node_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__539dd9ec3771332e287766c1f462eb6b4f65516b8cdfeaef7a9e4f100504b2f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc4db10982f760bc8958bea98db2287b4ed0df0f8dea4191cf78cab9cc4e410f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2516b6a95f51cce0c6dc0a3f1ad71e6f3fa7d440abb1a64938207cb760c0e412)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeNodeTemplate.ComputeNodeTemplateAccelerators",
    jsii_struct_bases=[],
    name_mapping={
        "accelerator_count": "acceleratorCount",
        "accelerator_type": "acceleratorType",
    },
)
class ComputeNodeTemplateAccelerators:
    def __init__(
        self,
        *,
        accelerator_count: typing.Optional[jsii.Number] = None,
        accelerator_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param accelerator_count: The number of the guest accelerator cards exposed to this node template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_template#accelerator_count ComputeNodeTemplate#accelerator_count}
        :param accelerator_type: Full or partial URL of the accelerator type resource to expose to this node template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_template#accelerator_type ComputeNodeTemplate#accelerator_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e728be4f4b61b3e78b56d58458749dfd6e7938241358734dcc7ac2693c81974)
            check_type(argname="argument accelerator_count", value=accelerator_count, expected_type=type_hints["accelerator_count"])
            check_type(argname="argument accelerator_type", value=accelerator_type, expected_type=type_hints["accelerator_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if accelerator_count is not None:
            self._values["accelerator_count"] = accelerator_count
        if accelerator_type is not None:
            self._values["accelerator_type"] = accelerator_type

    @builtins.property
    def accelerator_count(self) -> typing.Optional[jsii.Number]:
        '''The number of the guest accelerator cards exposed to this node template.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_template#accelerator_count ComputeNodeTemplate#accelerator_count}
        '''
        result = self._values.get("accelerator_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def accelerator_type(self) -> typing.Optional[builtins.str]:
        '''Full or partial URL of the accelerator type resource to expose to this node template.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_template#accelerator_type ComputeNodeTemplate#accelerator_type}
        '''
        result = self._values.get("accelerator_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeNodeTemplateAccelerators(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeNodeTemplateAcceleratorsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeNodeTemplate.ComputeNodeTemplateAcceleratorsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e899786a40f0b54075ecf29bc28129bd096040641365234a1d3b24fa2d271bdc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeNodeTemplateAcceleratorsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b87f2276bfeb40dfbc6fdb8955d5a0d7f029ad2dd7cb428997d7d2d68f6bf64)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeNodeTemplateAcceleratorsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65d46a725d9aa37bd4afbbce24a6b86cceff1e8a21f90244c697c6efa6d26f28)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b200ee199d5953e65c4927a7579b9bd4e3268e9eadc6b634523e72099b313577)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b955a94ff9df6e4ddbafb80074968c05af597d72e7b0fba38360c73f86210f60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeNodeTemplateAccelerators]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeNodeTemplateAccelerators]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeNodeTemplateAccelerators]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__274d3e96e0146cbe9cc4a099258e29b775cdd934fd0095bb101fef5043bef9bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeNodeTemplateAcceleratorsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeNodeTemplate.ComputeNodeTemplateAcceleratorsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e24ba7c0af7b2de91fc6d40b43e44ae061b12930cbd34c7480c6f61701a9a952)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAcceleratorCount")
    def reset_accelerator_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAcceleratorCount", []))

    @jsii.member(jsii_name="resetAcceleratorType")
    def reset_accelerator_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAcceleratorType", []))

    @builtins.property
    @jsii.member(jsii_name="acceleratorCountInput")
    def accelerator_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "acceleratorCountInput"))

    @builtins.property
    @jsii.member(jsii_name="acceleratorTypeInput")
    def accelerator_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "acceleratorTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="acceleratorCount")
    def accelerator_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "acceleratorCount"))

    @accelerator_count.setter
    def accelerator_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb155b3149395d759b6f0c2fe7084817c8659af85c71e92ed87ad5c0bbc6ce6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceleratorCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="acceleratorType")
    def accelerator_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "acceleratorType"))

    @accelerator_type.setter
    def accelerator_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b646e54cf0dc98f549cbfc161f77286d7e025a84bcfd54078d4cbb48f708620)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceleratorType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeNodeTemplateAccelerators]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeNodeTemplateAccelerators]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeNodeTemplateAccelerators]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7108b47c7e6aa8a7389e7dbbf7ec53a0b8bd4e3b55f55874e4b834f7387f87fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeNodeTemplate.ComputeNodeTemplateConfig",
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
        "accelerators": "accelerators",
        "cpu_overcommit_type": "cpuOvercommitType",
        "description": "description",
        "disks": "disks",
        "id": "id",
        "node_affinity_labels": "nodeAffinityLabels",
        "node_type": "nodeType",
        "node_type_flexibility": "nodeTypeFlexibility",
        "project": "project",
        "region": "region",
        "server_binding": "serverBinding",
        "timeouts": "timeouts",
    },
)
class ComputeNodeTemplateConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        accelerators: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeNodeTemplateAccelerators, typing.Dict[builtins.str, typing.Any]]]]] = None,
        cpu_overcommit_type: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        disks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeNodeTemplateDisks", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        node_affinity_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        node_type: typing.Optional[builtins.str] = None,
        node_type_flexibility: typing.Optional[typing.Union["ComputeNodeTemplateNodeTypeFlexibility", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        server_binding: typing.Optional[typing.Union["ComputeNodeTemplateServerBinding", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["ComputeNodeTemplateTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Name of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_template#name ComputeNodeTemplate#name}
        :param accelerators: accelerators block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_template#accelerators ComputeNodeTemplate#accelerators}
        :param cpu_overcommit_type: CPU overcommit. Default value: "NONE" Possible values: ["ENABLED", "NONE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_template#cpu_overcommit_type ComputeNodeTemplate#cpu_overcommit_type}
        :param description: An optional textual description of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_template#description ComputeNodeTemplate#description}
        :param disks: disks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_template#disks ComputeNodeTemplate#disks}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_template#id ComputeNodeTemplate#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param node_affinity_labels: Labels to use for node affinity, which will be used in instance scheduling. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_template#node_affinity_labels ComputeNodeTemplate#node_affinity_labels}
        :param node_type: Node type to use for nodes group that are created from this template. Only one of nodeTypeFlexibility and nodeType can be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_template#node_type ComputeNodeTemplate#node_type}
        :param node_type_flexibility: node_type_flexibility block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_template#node_type_flexibility ComputeNodeTemplate#node_type_flexibility}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_template#project ComputeNodeTemplate#project}.
        :param region: Region where nodes using the node template will be created. If it is not provided, the provider region is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_template#region ComputeNodeTemplate#region}
        :param server_binding: server_binding block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_template#server_binding ComputeNodeTemplate#server_binding}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_template#timeouts ComputeNodeTemplate#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(node_type_flexibility, dict):
            node_type_flexibility = ComputeNodeTemplateNodeTypeFlexibility(**node_type_flexibility)
        if isinstance(server_binding, dict):
            server_binding = ComputeNodeTemplateServerBinding(**server_binding)
        if isinstance(timeouts, dict):
            timeouts = ComputeNodeTemplateTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f37221f6afb49466914e56fec11d93e17202b06e7750389bfbba0452250477ac)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument accelerators", value=accelerators, expected_type=type_hints["accelerators"])
            check_type(argname="argument cpu_overcommit_type", value=cpu_overcommit_type, expected_type=type_hints["cpu_overcommit_type"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument disks", value=disks, expected_type=type_hints["disks"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument node_affinity_labels", value=node_affinity_labels, expected_type=type_hints["node_affinity_labels"])
            check_type(argname="argument node_type", value=node_type, expected_type=type_hints["node_type"])
            check_type(argname="argument node_type_flexibility", value=node_type_flexibility, expected_type=type_hints["node_type_flexibility"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument server_binding", value=server_binding, expected_type=type_hints["server_binding"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
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
        if accelerators is not None:
            self._values["accelerators"] = accelerators
        if cpu_overcommit_type is not None:
            self._values["cpu_overcommit_type"] = cpu_overcommit_type
        if description is not None:
            self._values["description"] = description
        if disks is not None:
            self._values["disks"] = disks
        if id is not None:
            self._values["id"] = id
        if node_affinity_labels is not None:
            self._values["node_affinity_labels"] = node_affinity_labels
        if node_type is not None:
            self._values["node_type"] = node_type
        if node_type_flexibility is not None:
            self._values["node_type_flexibility"] = node_type_flexibility
        if project is not None:
            self._values["project"] = project
        if region is not None:
            self._values["region"] = region
        if server_binding is not None:
            self._values["server_binding"] = server_binding
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
        '''Name of the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_template#name ComputeNodeTemplate#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def accelerators(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeNodeTemplateAccelerators]]]:
        '''accelerators block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_template#accelerators ComputeNodeTemplate#accelerators}
        '''
        result = self._values.get("accelerators")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeNodeTemplateAccelerators]]], result)

    @builtins.property
    def cpu_overcommit_type(self) -> typing.Optional[builtins.str]:
        '''CPU overcommit. Default value: "NONE" Possible values: ["ENABLED", "NONE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_template#cpu_overcommit_type ComputeNodeTemplate#cpu_overcommit_type}
        '''
        result = self._values.get("cpu_overcommit_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional textual description of the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_template#description ComputeNodeTemplate#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disks(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeNodeTemplateDisks"]]]:
        '''disks block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_template#disks ComputeNodeTemplate#disks}
        '''
        result = self._values.get("disks")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeNodeTemplateDisks"]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_template#id ComputeNodeTemplate#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_affinity_labels(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Labels to use for node affinity, which will be used in instance scheduling.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_template#node_affinity_labels ComputeNodeTemplate#node_affinity_labels}
        '''
        result = self._values.get("node_affinity_labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def node_type(self) -> typing.Optional[builtins.str]:
        '''Node type to use for nodes group that are created from this template.

        Only one of nodeTypeFlexibility and nodeType can be specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_template#node_type ComputeNodeTemplate#node_type}
        '''
        result = self._values.get("node_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_type_flexibility(
        self,
    ) -> typing.Optional["ComputeNodeTemplateNodeTypeFlexibility"]:
        '''node_type_flexibility block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_template#node_type_flexibility ComputeNodeTemplate#node_type_flexibility}
        '''
        result = self._values.get("node_type_flexibility")
        return typing.cast(typing.Optional["ComputeNodeTemplateNodeTypeFlexibility"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_template#project ComputeNodeTemplate#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where nodes using the node template will be created. If it is not provided, the provider region is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_template#region ComputeNodeTemplate#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def server_binding(self) -> typing.Optional["ComputeNodeTemplateServerBinding"]:
        '''server_binding block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_template#server_binding ComputeNodeTemplate#server_binding}
        '''
        result = self._values.get("server_binding")
        return typing.cast(typing.Optional["ComputeNodeTemplateServerBinding"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ComputeNodeTemplateTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_template#timeouts ComputeNodeTemplate#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ComputeNodeTemplateTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeNodeTemplateConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeNodeTemplate.ComputeNodeTemplateDisks",
    jsii_struct_bases=[],
    name_mapping={
        "disk_count": "diskCount",
        "disk_size_gb": "diskSizeGb",
        "disk_type": "diskType",
    },
)
class ComputeNodeTemplateDisks:
    def __init__(
        self,
        *,
        disk_count: typing.Optional[jsii.Number] = None,
        disk_size_gb: typing.Optional[jsii.Number] = None,
        disk_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param disk_count: Specifies the number of such disks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_template#disk_count ComputeNodeTemplate#disk_count}
        :param disk_size_gb: Specifies the size of the disk in base-2 GB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_template#disk_size_gb ComputeNodeTemplate#disk_size_gb}
        :param disk_type: Specifies the desired disk type on the node. This disk type must be a local storage type (e.g.: local-ssd). Note that for nodeTemplates, this should be the name of the disk type and not its URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_template#disk_type ComputeNodeTemplate#disk_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ed5807a8547f291e833107c2b2848bc60c39c8aa2132cd165567b192bb74100)
            check_type(argname="argument disk_count", value=disk_count, expected_type=type_hints["disk_count"])
            check_type(argname="argument disk_size_gb", value=disk_size_gb, expected_type=type_hints["disk_size_gb"])
            check_type(argname="argument disk_type", value=disk_type, expected_type=type_hints["disk_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if disk_count is not None:
            self._values["disk_count"] = disk_count
        if disk_size_gb is not None:
            self._values["disk_size_gb"] = disk_size_gb
        if disk_type is not None:
            self._values["disk_type"] = disk_type

    @builtins.property
    def disk_count(self) -> typing.Optional[jsii.Number]:
        '''Specifies the number of such disks.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_template#disk_count ComputeNodeTemplate#disk_count}
        '''
        result = self._values.get("disk_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def disk_size_gb(self) -> typing.Optional[jsii.Number]:
        '''Specifies the size of the disk in base-2 GB.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_template#disk_size_gb ComputeNodeTemplate#disk_size_gb}
        '''
        result = self._values.get("disk_size_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def disk_type(self) -> typing.Optional[builtins.str]:
        '''Specifies the desired disk type on the node.

        This disk type must be a local storage type (e.g.: local-ssd). Note that for nodeTemplates, this should be the name of the disk type and not its URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_template#disk_type ComputeNodeTemplate#disk_type}
        '''
        result = self._values.get("disk_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeNodeTemplateDisks(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeNodeTemplateDisksList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeNodeTemplate.ComputeNodeTemplateDisksList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9bc3d8ef71d546d2b2e1cc2942b0db3079f68bcf864d36e0a586a0a5fde225c1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ComputeNodeTemplateDisksOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__797b20adec67d5899c3c05b65dc973df791b4794ef004e02ddfaddb697a61817)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeNodeTemplateDisksOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34eb32b54b8f5451db5dc9045f6b4cd161eaf4cbdfb5c64c3590f671eb4596c1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__59490f23b737595096c61ce32d7eee38092a7bfcfe1cfcbb88e0136cf5cb4498)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9d8028d8a84720ec1a7f15bff04f55c04e32c11ad4d7b89a03763bf5316ab8d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeNodeTemplateDisks]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeNodeTemplateDisks]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeNodeTemplateDisks]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9985cf3047c3ef8220929e0eef58ab52feef62214282f5bc50f7095a81ab0455)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeNodeTemplateDisksOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeNodeTemplate.ComputeNodeTemplateDisksOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c27010758d889597ab9f87ad1b062462efe7fbbe2482d2384412713f0c47f9a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDiskCount")
    def reset_disk_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskCount", []))

    @jsii.member(jsii_name="resetDiskSizeGb")
    def reset_disk_size_gb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskSizeGb", []))

    @jsii.member(jsii_name="resetDiskType")
    def reset_disk_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskType", []))

    @builtins.property
    @jsii.member(jsii_name="diskCountInput")
    def disk_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "diskCountInput"))

    @builtins.property
    @jsii.member(jsii_name="diskSizeGbInput")
    def disk_size_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "diskSizeGbInput"))

    @builtins.property
    @jsii.member(jsii_name="diskTypeInput")
    def disk_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "diskTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="diskCount")
    def disk_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "diskCount"))

    @disk_count.setter
    def disk_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__921145908a163c3383a28a55c6c08f45629f72d7b510d01d2e88eff3cf398a77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskSizeGb")
    def disk_size_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "diskSizeGb"))

    @disk_size_gb.setter
    def disk_size_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__806e1966eb2f7890d058f1d01b8271367f13fc8d917c94499a5a1a37af3bd3d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskSizeGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskType")
    def disk_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskType"))

    @disk_type.setter
    def disk_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63aa1c79f92414af5600f6353fa83bd956c6ababbecb5c3922eea3f33997d4c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeNodeTemplateDisks]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeNodeTemplateDisks]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeNodeTemplateDisks]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ead639bd5eb9940f64ea261b4320a8defa4d51aa2f67d6097deb44276665899f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeNodeTemplate.ComputeNodeTemplateNodeTypeFlexibility",
    jsii_struct_bases=[],
    name_mapping={"cpus": "cpus", "memory": "memory"},
)
class ComputeNodeTemplateNodeTypeFlexibility:
    def __init__(
        self,
        *,
        cpus: typing.Optional[builtins.str] = None,
        memory: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cpus: Number of virtual CPUs to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_template#cpus ComputeNodeTemplate#cpus}
        :param memory: Physical memory available to the node, defined in MB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_template#memory ComputeNodeTemplate#memory}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__faba0bc9816df5e52650b1154dbfd16276733b397b0828ad5c46465d1de25158)
            check_type(argname="argument cpus", value=cpus, expected_type=type_hints["cpus"])
            check_type(argname="argument memory", value=memory, expected_type=type_hints["memory"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cpus is not None:
            self._values["cpus"] = cpus
        if memory is not None:
            self._values["memory"] = memory

    @builtins.property
    def cpus(self) -> typing.Optional[builtins.str]:
        '''Number of virtual CPUs to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_template#cpus ComputeNodeTemplate#cpus}
        '''
        result = self._values.get("cpus")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def memory(self) -> typing.Optional[builtins.str]:
        '''Physical memory available to the node, defined in MB.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_template#memory ComputeNodeTemplate#memory}
        '''
        result = self._values.get("memory")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeNodeTemplateNodeTypeFlexibility(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeNodeTemplateNodeTypeFlexibilityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeNodeTemplate.ComputeNodeTemplateNodeTypeFlexibilityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__42b95c78f767b8e39cf540eb679b39aa2380e6a429f202e6d33fb354e41da32c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCpus")
    def reset_cpus(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpus", []))

    @jsii.member(jsii_name="resetMemory")
    def reset_memory(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemory", []))

    @builtins.property
    @jsii.member(jsii_name="localSsd")
    def local_ssd(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localSsd"))

    @builtins.property
    @jsii.member(jsii_name="cpusInput")
    def cpus_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cpusInput"))

    @builtins.property
    @jsii.member(jsii_name="memoryInput")
    def memory_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "memoryInput"))

    @builtins.property
    @jsii.member(jsii_name="cpus")
    def cpus(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cpus"))

    @cpus.setter
    def cpus(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75a9ef706830a01f82adf530c43ff886c38667c8da412b1eba759d35a7c072ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memory")
    def memory(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "memory"))

    @memory.setter
    def memory(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b715353d07087de787c127c078f5fb49582635107278fdfa832ae81db01c72f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memory", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeNodeTemplateNodeTypeFlexibility]:
        return typing.cast(typing.Optional[ComputeNodeTemplateNodeTypeFlexibility], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeNodeTemplateNodeTypeFlexibility],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__936e7b3ac930806529a157b4509c666e015ba25566abb85ec3483838fa3e7198)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeNodeTemplate.ComputeNodeTemplateServerBinding",
    jsii_struct_bases=[],
    name_mapping={"type": "type"},
)
class ComputeNodeTemplateServerBinding:
    def __init__(self, *, type: builtins.str) -> None:
        '''
        :param type: Type of server binding policy. If 'RESTART_NODE_ON_ANY_SERVER', nodes using this template will restart on any physical server following a maintenance event. If 'RESTART_NODE_ON_MINIMAL_SERVER', nodes using this template will restart on the same physical server following a maintenance event, instead of being live migrated to or restarted on a new physical server. This option may be useful if you are using software licenses tied to the underlying server characteristics such as physical sockets or cores, to avoid the need for additional licenses when maintenance occurs. However, VMs on such nodes will experience outages while maintenance is applied. Possible values: ["RESTART_NODE_ON_ANY_SERVER", "RESTART_NODE_ON_MINIMAL_SERVERS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_template#type ComputeNodeTemplate#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edf6d368448bd004749888bf72fe5e2b4b0020499f9718365312a56cd641ea0a)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }

    @builtins.property
    def type(self) -> builtins.str:
        '''Type of server binding policy. If 'RESTART_NODE_ON_ANY_SERVER', nodes using this template will restart on any physical server following a maintenance event.

        If 'RESTART_NODE_ON_MINIMAL_SERVER', nodes using this template
        will restart on the same physical server following a maintenance
        event, instead of being live migrated to or restarted on a new
        physical server. This option may be useful if you are using
        software licenses tied to the underlying server characteristics
        such as physical sockets or cores, to avoid the need for
        additional licenses when maintenance occurs. However, VMs on such
        nodes will experience outages while maintenance is applied. Possible values: ["RESTART_NODE_ON_ANY_SERVER", "RESTART_NODE_ON_MINIMAL_SERVERS"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_template#type ComputeNodeTemplate#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeNodeTemplateServerBinding(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeNodeTemplateServerBindingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeNodeTemplate.ComputeNodeTemplateServerBindingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca9eb1e90d9f8f70caaad2e6f959aa22e7c03c902d38f025b11e66cb0aae1611)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8c8cb26733673e8cf69c7e02d18b8700551dd65caf68925d531efce4bd19db3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeNodeTemplateServerBinding]:
        return typing.cast(typing.Optional[ComputeNodeTemplateServerBinding], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeNodeTemplateServerBinding],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0aac106b0f9990fa231d75b6cd4a81728b26afc4572bb158212031789689bda5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeNodeTemplate.ComputeNodeTemplateTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class ComputeNodeTemplateTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_template#create ComputeNodeTemplate#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_template#delete ComputeNodeTemplate#delete}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77f18e1d98be0a5526aff9af50a949e77e691f212c6ddb61348817a89d538c3c)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_template#create ComputeNodeTemplate#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_node_template#delete ComputeNodeTemplate#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeNodeTemplateTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeNodeTemplateTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeNodeTemplate.ComputeNodeTemplateTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4e49fb7f82707f3d436f2680c60d1e4e059fde83258dbb996493170ce62dd053)
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
            type_hints = typing.get_type_hints(_typecheckingstub__95dc06b6a4ef25dd00985adc0e669a4c2a12a1f47e827eb585f675146a2c5764)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96a77fad9a003a81abe7cefbfd567f45c88ada0a42fb0662e825d87d4205b99d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeNodeTemplateTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeNodeTemplateTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeNodeTemplateTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16a83ffb28093d770220f699ef8d62549dc8887a44335ffb30737a86b50a0f1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ComputeNodeTemplate",
    "ComputeNodeTemplateAccelerators",
    "ComputeNodeTemplateAcceleratorsList",
    "ComputeNodeTemplateAcceleratorsOutputReference",
    "ComputeNodeTemplateConfig",
    "ComputeNodeTemplateDisks",
    "ComputeNodeTemplateDisksList",
    "ComputeNodeTemplateDisksOutputReference",
    "ComputeNodeTemplateNodeTypeFlexibility",
    "ComputeNodeTemplateNodeTypeFlexibilityOutputReference",
    "ComputeNodeTemplateServerBinding",
    "ComputeNodeTemplateServerBindingOutputReference",
    "ComputeNodeTemplateTimeouts",
    "ComputeNodeTemplateTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__d5a7fd3496aa64577524335df376838dc98d6ec71472a09fc5b8f9afe09fa14d(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    accelerators: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeNodeTemplateAccelerators, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cpu_overcommit_type: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    disks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeNodeTemplateDisks, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    node_affinity_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    node_type: typing.Optional[builtins.str] = None,
    node_type_flexibility: typing.Optional[typing.Union[ComputeNodeTemplateNodeTypeFlexibility, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    server_binding: typing.Optional[typing.Union[ComputeNodeTemplateServerBinding, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[ComputeNodeTemplateTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__9af846e6a9a50608e7ef3f89c02826edf61e860afb3d4bd586bcd3a4425b008d(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4df88687b58ecb36d37492a9c791cd54ea86a1ff6458d6af64f2b435ddb43912(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeNodeTemplateAccelerators, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8afb67bb2633f6d8ba387dc8ea9b9af489280e17725fa9057abf19a9898bb496(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeNodeTemplateDisks, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5d712415022023d522e69564f9019cdf851b9002c33313e386bfc723e0f02e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28ac3c3079370c43fdbf841b600c0bfe3e2c9d870462424e8654ce67a2645b41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84a0f5120ed469cdbebfc8950b0579d11e194d769bed485d6c1a56c13ac9e842(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6201fd4ba29837e86bf3e0ed9588c0a3fbc74732c167f9d99296aa13041a9780(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1409542951ff74adc9a708ac250baf154c0386d25582cd8ca0ce30279ffb77a4(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__539dd9ec3771332e287766c1f462eb6b4f65516b8cdfeaef7a9e4f100504b2f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc4db10982f760bc8958bea98db2287b4ed0df0f8dea4191cf78cab9cc4e410f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2516b6a95f51cce0c6dc0a3f1ad71e6f3fa7d440abb1a64938207cb760c0e412(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e728be4f4b61b3e78b56d58458749dfd6e7938241358734dcc7ac2693c81974(
    *,
    accelerator_count: typing.Optional[jsii.Number] = None,
    accelerator_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e899786a40f0b54075ecf29bc28129bd096040641365234a1d3b24fa2d271bdc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b87f2276bfeb40dfbc6fdb8955d5a0d7f029ad2dd7cb428997d7d2d68f6bf64(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65d46a725d9aa37bd4afbbce24a6b86cceff1e8a21f90244c697c6efa6d26f28(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b200ee199d5953e65c4927a7579b9bd4e3268e9eadc6b634523e72099b313577(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b955a94ff9df6e4ddbafb80074968c05af597d72e7b0fba38360c73f86210f60(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__274d3e96e0146cbe9cc4a099258e29b775cdd934fd0095bb101fef5043bef9bd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeNodeTemplateAccelerators]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e24ba7c0af7b2de91fc6d40b43e44ae061b12930cbd34c7480c6f61701a9a952(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb155b3149395d759b6f0c2fe7084817c8659af85c71e92ed87ad5c0bbc6ce6b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b646e54cf0dc98f549cbfc161f77286d7e025a84bcfd54078d4cbb48f708620(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7108b47c7e6aa8a7389e7dbbf7ec53a0b8bd4e3b55f55874e4b834f7387f87fe(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeNodeTemplateAccelerators]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f37221f6afb49466914e56fec11d93e17202b06e7750389bfbba0452250477ac(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    accelerators: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeNodeTemplateAccelerators, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cpu_overcommit_type: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    disks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeNodeTemplateDisks, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    node_affinity_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    node_type: typing.Optional[builtins.str] = None,
    node_type_flexibility: typing.Optional[typing.Union[ComputeNodeTemplateNodeTypeFlexibility, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    server_binding: typing.Optional[typing.Union[ComputeNodeTemplateServerBinding, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[ComputeNodeTemplateTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ed5807a8547f291e833107c2b2848bc60c39c8aa2132cd165567b192bb74100(
    *,
    disk_count: typing.Optional[jsii.Number] = None,
    disk_size_gb: typing.Optional[jsii.Number] = None,
    disk_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bc3d8ef71d546d2b2e1cc2942b0db3079f68bcf864d36e0a586a0a5fde225c1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__797b20adec67d5899c3c05b65dc973df791b4794ef004e02ddfaddb697a61817(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34eb32b54b8f5451db5dc9045f6b4cd161eaf4cbdfb5c64c3590f671eb4596c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59490f23b737595096c61ce32d7eee38092a7bfcfe1cfcbb88e0136cf5cb4498(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d8028d8a84720ec1a7f15bff04f55c04e32c11ad4d7b89a03763bf5316ab8d4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9985cf3047c3ef8220929e0eef58ab52feef62214282f5bc50f7095a81ab0455(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeNodeTemplateDisks]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c27010758d889597ab9f87ad1b062462efe7fbbe2482d2384412713f0c47f9a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__921145908a163c3383a28a55c6c08f45629f72d7b510d01d2e88eff3cf398a77(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__806e1966eb2f7890d058f1d01b8271367f13fc8d917c94499a5a1a37af3bd3d6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63aa1c79f92414af5600f6353fa83bd956c6ababbecb5c3922eea3f33997d4c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ead639bd5eb9940f64ea261b4320a8defa4d51aa2f67d6097deb44276665899f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeNodeTemplateDisks]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__faba0bc9816df5e52650b1154dbfd16276733b397b0828ad5c46465d1de25158(
    *,
    cpus: typing.Optional[builtins.str] = None,
    memory: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42b95c78f767b8e39cf540eb679b39aa2380e6a429f202e6d33fb354e41da32c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75a9ef706830a01f82adf530c43ff886c38667c8da412b1eba759d35a7c072ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b715353d07087de787c127c078f5fb49582635107278fdfa832ae81db01c72f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__936e7b3ac930806529a157b4509c666e015ba25566abb85ec3483838fa3e7198(
    value: typing.Optional[ComputeNodeTemplateNodeTypeFlexibility],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edf6d368448bd004749888bf72fe5e2b4b0020499f9718365312a56cd641ea0a(
    *,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca9eb1e90d9f8f70caaad2e6f959aa22e7c03c902d38f025b11e66cb0aae1611(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8c8cb26733673e8cf69c7e02d18b8700551dd65caf68925d531efce4bd19db3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0aac106b0f9990fa231d75b6cd4a81728b26afc4572bb158212031789689bda5(
    value: typing.Optional[ComputeNodeTemplateServerBinding],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77f18e1d98be0a5526aff9af50a949e77e691f212c6ddb61348817a89d538c3c(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e49fb7f82707f3d436f2680c60d1e4e059fde83258dbb996493170ce62dd053(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95dc06b6a4ef25dd00985adc0e669a4c2a12a1f47e827eb585f675146a2c5764(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96a77fad9a003a81abe7cefbfd567f45c88ada0a42fb0662e825d87d4205b99d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16a83ffb28093d770220f699ef8d62549dc8887a44335ffb30737a86b50a0f1a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeNodeTemplateTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
