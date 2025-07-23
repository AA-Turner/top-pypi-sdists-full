r'''
# `google_gkeonprem_vmware_node_pool`

Refer to the Terraform Registry for docs: [`google_gkeonprem_vmware_node_pool`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool).
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


class GkeonpremVmwareNodePool(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareNodePool.GkeonpremVmwareNodePool",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool google_gkeonprem_vmware_node_pool}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        config: typing.Union["GkeonpremVmwareNodePoolConfigA", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        name: builtins.str,
        vmware_cluster: builtins.str,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        node_pool_autoscaling: typing.Optional[typing.Union["GkeonpremVmwareNodePoolNodePoolAutoscaling", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GkeonpremVmwareNodePoolTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool google_gkeonprem_vmware_node_pool} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param config: config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#config GkeonpremVmwareNodePool#config}
        :param location: The location of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#location GkeonpremVmwareNodePool#location}
        :param name: The vmware node pool name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#name GkeonpremVmwareNodePool#name}
        :param vmware_cluster: The cluster this node pool belongs to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#vmware_cluster GkeonpremVmwareNodePool#vmware_cluster}
        :param annotations: Annotations on the node Pool. This field has the same restrictions as Kubernetes annotations. The total size of all keys and values combined is limited to 256k. Key can have 2 segments: prefix (optional) and name (required), separated by a slash (/). Prefix must be a DNS subdomain. Name must be 63 characters or less, begin and end with alphanumerics, with dashes (-), underscores (_), dots (.), and alphanumerics between. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#annotations GkeonpremVmwareNodePool#annotations}
        :param display_name: The display name for the node pool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#display_name GkeonpremVmwareNodePool#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#id GkeonpremVmwareNodePool#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param node_pool_autoscaling: node_pool_autoscaling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#node_pool_autoscaling GkeonpremVmwareNodePool#node_pool_autoscaling}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#project GkeonpremVmwareNodePool#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#timeouts GkeonpremVmwareNodePool#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a62e910fa7527da411324f8eab8af9ce7ccb1edbf095167ea892bf83675a15d6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config_ = GkeonpremVmwareNodePoolConfig(
            config=config,
            location=location,
            name=name,
            vmware_cluster=vmware_cluster,
            annotations=annotations,
            display_name=display_name,
            id=id,
            node_pool_autoscaling=node_pool_autoscaling,
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

        jsii.create(self.__class__, self, [scope, id_, config_])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a GkeonpremVmwareNodePool resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GkeonpremVmwareNodePool to import.
        :param import_from_id: The id of the existing GkeonpremVmwareNodePool that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GkeonpremVmwareNodePool to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b31dd49eb436b56364467dfd1d37afec494f3c68d646aabaf34b29b7b1958aa2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putConfig")
    def put_config(
        self,
        *,
        image_type: builtins.str,
        boot_disk_size_gb: typing.Optional[jsii.Number] = None,
        cpus: typing.Optional[jsii.Number] = None,
        enable_load_balancer: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        image: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        memory_mb: typing.Optional[jsii.Number] = None,
        replicas: typing.Optional[jsii.Number] = None,
        taints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeonpremVmwareNodePoolConfigTaints", typing.Dict[builtins.str, typing.Any]]]]] = None,
        vsphere_config: typing.Optional[typing.Union["GkeonpremVmwareNodePoolConfigVsphereConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param image_type: The OS image to be used for each node in a node pool. Currently 'cos', 'cos_cgv2', 'ubuntu', 'ubuntu_cgv2', 'ubuntu_containerd' and 'windows' are supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#image_type GkeonpremVmwareNodePool#image_type}
        :param boot_disk_size_gb: VMware disk size to be used during creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#boot_disk_size_gb GkeonpremVmwareNodePool#boot_disk_size_gb}
        :param cpus: The number of CPUs for each node in the node pool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#cpus GkeonpremVmwareNodePool#cpus}
        :param enable_load_balancer: Allow node pool traffic to be load balanced. Only works for clusters with MetalLB load balancers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#enable_load_balancer GkeonpremVmwareNodePool#enable_load_balancer}
        :param image: The OS image name in vCenter, only valid when using Windows. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#image GkeonpremVmwareNodePool#image}
        :param labels: The map of Kubernetes labels (key/value pairs) to be applied to each node. These will added in addition to any default label(s) that Kubernetes may apply to the node. In case of conflict in label keys, the applied set may differ depending on the Kubernetes version -- it's best to assume the behavior is undefined and conflicts should be avoided. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#labels GkeonpremVmwareNodePool#labels}
        :param memory_mb: The megabytes of memory for each node in the node pool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#memory_mb GkeonpremVmwareNodePool#memory_mb}
        :param replicas: The number of nodes in the node pool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#replicas GkeonpremVmwareNodePool#replicas}
        :param taints: taints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#taints GkeonpremVmwareNodePool#taints}
        :param vsphere_config: vsphere_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#vsphere_config GkeonpremVmwareNodePool#vsphere_config}
        '''
        value = GkeonpremVmwareNodePoolConfigA(
            image_type=image_type,
            boot_disk_size_gb=boot_disk_size_gb,
            cpus=cpus,
            enable_load_balancer=enable_load_balancer,
            image=image,
            labels=labels,
            memory_mb=memory_mb,
            replicas=replicas,
            taints=taints,
            vsphere_config=vsphere_config,
        )

        return typing.cast(None, jsii.invoke(self, "putConfig", [value]))

    @jsii.member(jsii_name="putNodePoolAutoscaling")
    def put_node_pool_autoscaling(
        self,
        *,
        max_replicas: jsii.Number,
        min_replicas: jsii.Number,
    ) -> None:
        '''
        :param max_replicas: Maximum number of replicas in the NodePool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#max_replicas GkeonpremVmwareNodePool#max_replicas}
        :param min_replicas: Minimum number of replicas in the NodePool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#min_replicas GkeonpremVmwareNodePool#min_replicas}
        '''
        value = GkeonpremVmwareNodePoolNodePoolAutoscaling(
            max_replicas=max_replicas, min_replicas=min_replicas
        )

        return typing.cast(None, jsii.invoke(self, "putNodePoolAutoscaling", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#create GkeonpremVmwareNodePool#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#delete GkeonpremVmwareNodePool#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#update GkeonpremVmwareNodePool#update}.
        '''
        value = GkeonpremVmwareNodePoolTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAnnotations")
    def reset_annotations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnnotations", []))

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetNodePoolAutoscaling")
    def reset_node_pool_autoscaling(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodePoolAutoscaling", []))

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
    @jsii.member(jsii_name="config")
    def config(self) -> "GkeonpremVmwareNodePoolConfigAOutputReference":
        return typing.cast("GkeonpremVmwareNodePoolConfigAOutputReference", jsii.get(self, "config"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="deleteTime")
    def delete_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deleteTime"))

    @builtins.property
    @jsii.member(jsii_name="effectiveAnnotations")
    def effective_annotations(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveAnnotations"))

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "etag"))

    @builtins.property
    @jsii.member(jsii_name="nodePoolAutoscaling")
    def node_pool_autoscaling(
        self,
    ) -> "GkeonpremVmwareNodePoolNodePoolAutoscalingOutputReference":
        return typing.cast("GkeonpremVmwareNodePoolNodePoolAutoscalingOutputReference", jsii.get(self, "nodePoolAutoscaling"))

    @builtins.property
    @jsii.member(jsii_name="onPremVersion")
    def on_prem_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "onPremVersion"))

    @builtins.property
    @jsii.member(jsii_name="reconciling")
    def reconciling(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "reconciling"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> "GkeonpremVmwareNodePoolStatusList":
        return typing.cast("GkeonpremVmwareNodePoolStatusList", jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GkeonpremVmwareNodePoolTimeoutsOutputReference":
        return typing.cast("GkeonpremVmwareNodePoolTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="uid")
    def uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uid"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="annotationsInput")
    def annotations_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "annotationsInput"))

    @builtins.property
    @jsii.member(jsii_name="configInput")
    def config_input(self) -> typing.Optional["GkeonpremVmwareNodePoolConfigA"]:
        return typing.cast(typing.Optional["GkeonpremVmwareNodePoolConfigA"], jsii.get(self, "configInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="nodePoolAutoscalingInput")
    def node_pool_autoscaling_input(
        self,
    ) -> typing.Optional["GkeonpremVmwareNodePoolNodePoolAutoscaling"]:
        return typing.cast(typing.Optional["GkeonpremVmwareNodePoolNodePoolAutoscaling"], jsii.get(self, "nodePoolAutoscalingInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GkeonpremVmwareNodePoolTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GkeonpremVmwareNodePoolTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="vmwareClusterInput")
    def vmware_cluster_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vmwareClusterInput"))

    @builtins.property
    @jsii.member(jsii_name="annotations")
    def annotations(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "annotations"))

    @annotations.setter
    def annotations(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be4dc77870b59b1671afa91887a239cfef7caecd196c3882e2155e9488e168f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1abf44b4d3f09c3dbb39e2dcf2b63aa400142c7ccba99095cf2ab74974c88994)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7a70ceafd5f08aae7444bbe311f988035cf47c8875563889ebd07923e87cae1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51563c744d94c840463ea50d5c9df2eb71a4d65b85a5f8453693c2b5a557c371)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__553a10c00132055b01a955df3f5ad3f167f8c0c8bdb3e600ed7b2952db8a3f89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8282f18c0dbe5c1c81dd7ed9d70a19566fb4cf1b0ceac0cb2a21ec75fa59e99d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vmwareCluster")
    def vmware_cluster(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vmwareCluster"))

    @vmware_cluster.setter
    def vmware_cluster(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__babd6b294c6caf4572f23e3499ef1c2a712b1ea147e564bf3d5febc1590b0d70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vmwareCluster", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareNodePool.GkeonpremVmwareNodePoolConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "config": "config",
        "location": "location",
        "name": "name",
        "vmware_cluster": "vmwareCluster",
        "annotations": "annotations",
        "display_name": "displayName",
        "id": "id",
        "node_pool_autoscaling": "nodePoolAutoscaling",
        "project": "project",
        "timeouts": "timeouts",
    },
)
class GkeonpremVmwareNodePoolConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        config: typing.Union["GkeonpremVmwareNodePoolConfigA", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        name: builtins.str,
        vmware_cluster: builtins.str,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        node_pool_autoscaling: typing.Optional[typing.Union["GkeonpremVmwareNodePoolNodePoolAutoscaling", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GkeonpremVmwareNodePoolTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param config: config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#config GkeonpremVmwareNodePool#config}
        :param location: The location of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#location GkeonpremVmwareNodePool#location}
        :param name: The vmware node pool name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#name GkeonpremVmwareNodePool#name}
        :param vmware_cluster: The cluster this node pool belongs to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#vmware_cluster GkeonpremVmwareNodePool#vmware_cluster}
        :param annotations: Annotations on the node Pool. This field has the same restrictions as Kubernetes annotations. The total size of all keys and values combined is limited to 256k. Key can have 2 segments: prefix (optional) and name (required), separated by a slash (/). Prefix must be a DNS subdomain. Name must be 63 characters or less, begin and end with alphanumerics, with dashes (-), underscores (_), dots (.), and alphanumerics between. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#annotations GkeonpremVmwareNodePool#annotations}
        :param display_name: The display name for the node pool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#display_name GkeonpremVmwareNodePool#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#id GkeonpremVmwareNodePool#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param node_pool_autoscaling: node_pool_autoscaling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#node_pool_autoscaling GkeonpremVmwareNodePool#node_pool_autoscaling}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#project GkeonpremVmwareNodePool#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#timeouts GkeonpremVmwareNodePool#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(config, dict):
            config = GkeonpremVmwareNodePoolConfigA(**config)
        if isinstance(node_pool_autoscaling, dict):
            node_pool_autoscaling = GkeonpremVmwareNodePoolNodePoolAutoscaling(**node_pool_autoscaling)
        if isinstance(timeouts, dict):
            timeouts = GkeonpremVmwareNodePoolTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52e1324f8be0dc2acc7e7e82a1e142a79e807bbbfb5d892bba036e462fe6ef6a)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument config", value=config, expected_type=type_hints["config"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument vmware_cluster", value=vmware_cluster, expected_type=type_hints["vmware_cluster"])
            check_type(argname="argument annotations", value=annotations, expected_type=type_hints["annotations"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument node_pool_autoscaling", value=node_pool_autoscaling, expected_type=type_hints["node_pool_autoscaling"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "config": config,
            "location": location,
            "name": name,
            "vmware_cluster": vmware_cluster,
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
        if annotations is not None:
            self._values["annotations"] = annotations
        if display_name is not None:
            self._values["display_name"] = display_name
        if id is not None:
            self._values["id"] = id
        if node_pool_autoscaling is not None:
            self._values["node_pool_autoscaling"] = node_pool_autoscaling
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
    def config(self) -> "GkeonpremVmwareNodePoolConfigA":
        '''config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#config GkeonpremVmwareNodePool#config}
        '''
        result = self._values.get("config")
        assert result is not None, "Required property 'config' is missing"
        return typing.cast("GkeonpremVmwareNodePoolConfigA", result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location of the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#location GkeonpremVmwareNodePool#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The vmware node pool name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#name GkeonpremVmwareNodePool#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vmware_cluster(self) -> builtins.str:
        '''The cluster this node pool belongs to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#vmware_cluster GkeonpremVmwareNodePool#vmware_cluster}
        '''
        result = self._values.get("vmware_cluster")
        assert result is not None, "Required property 'vmware_cluster' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def annotations(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Annotations on the node Pool.

        This field has the same restrictions as Kubernetes annotations.
        The total size of all keys and values combined is limited to 256k.
        Key can have 2 segments: prefix (optional) and name (required),
        separated by a slash (/).
        Prefix must be a DNS subdomain.
        Name must be 63 characters or less, begin and end with alphanumerics,
        with dashes (-), underscores (_), dots (.), and alphanumerics between.

        **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration.
        Please refer to the field 'effective_annotations' for all of the annotations present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#annotations GkeonpremVmwareNodePool#annotations}
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The display name for the node pool.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#display_name GkeonpremVmwareNodePool#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#id GkeonpremVmwareNodePool#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_pool_autoscaling(
        self,
    ) -> typing.Optional["GkeonpremVmwareNodePoolNodePoolAutoscaling"]:
        '''node_pool_autoscaling block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#node_pool_autoscaling GkeonpremVmwareNodePool#node_pool_autoscaling}
        '''
        result = self._values.get("node_pool_autoscaling")
        return typing.cast(typing.Optional["GkeonpremVmwareNodePoolNodePoolAutoscaling"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#project GkeonpremVmwareNodePool#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GkeonpremVmwareNodePoolTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#timeouts GkeonpremVmwareNodePool#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GkeonpremVmwareNodePoolTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareNodePoolConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareNodePool.GkeonpremVmwareNodePoolConfigA",
    jsii_struct_bases=[],
    name_mapping={
        "image_type": "imageType",
        "boot_disk_size_gb": "bootDiskSizeGb",
        "cpus": "cpus",
        "enable_load_balancer": "enableLoadBalancer",
        "image": "image",
        "labels": "labels",
        "memory_mb": "memoryMb",
        "replicas": "replicas",
        "taints": "taints",
        "vsphere_config": "vsphereConfig",
    },
)
class GkeonpremVmwareNodePoolConfigA:
    def __init__(
        self,
        *,
        image_type: builtins.str,
        boot_disk_size_gb: typing.Optional[jsii.Number] = None,
        cpus: typing.Optional[jsii.Number] = None,
        enable_load_balancer: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        image: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        memory_mb: typing.Optional[jsii.Number] = None,
        replicas: typing.Optional[jsii.Number] = None,
        taints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeonpremVmwareNodePoolConfigTaints", typing.Dict[builtins.str, typing.Any]]]]] = None,
        vsphere_config: typing.Optional[typing.Union["GkeonpremVmwareNodePoolConfigVsphereConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param image_type: The OS image to be used for each node in a node pool. Currently 'cos', 'cos_cgv2', 'ubuntu', 'ubuntu_cgv2', 'ubuntu_containerd' and 'windows' are supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#image_type GkeonpremVmwareNodePool#image_type}
        :param boot_disk_size_gb: VMware disk size to be used during creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#boot_disk_size_gb GkeonpremVmwareNodePool#boot_disk_size_gb}
        :param cpus: The number of CPUs for each node in the node pool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#cpus GkeonpremVmwareNodePool#cpus}
        :param enable_load_balancer: Allow node pool traffic to be load balanced. Only works for clusters with MetalLB load balancers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#enable_load_balancer GkeonpremVmwareNodePool#enable_load_balancer}
        :param image: The OS image name in vCenter, only valid when using Windows. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#image GkeonpremVmwareNodePool#image}
        :param labels: The map of Kubernetes labels (key/value pairs) to be applied to each node. These will added in addition to any default label(s) that Kubernetes may apply to the node. In case of conflict in label keys, the applied set may differ depending on the Kubernetes version -- it's best to assume the behavior is undefined and conflicts should be avoided. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#labels GkeonpremVmwareNodePool#labels}
        :param memory_mb: The megabytes of memory for each node in the node pool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#memory_mb GkeonpremVmwareNodePool#memory_mb}
        :param replicas: The number of nodes in the node pool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#replicas GkeonpremVmwareNodePool#replicas}
        :param taints: taints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#taints GkeonpremVmwareNodePool#taints}
        :param vsphere_config: vsphere_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#vsphere_config GkeonpremVmwareNodePool#vsphere_config}
        '''
        if isinstance(vsphere_config, dict):
            vsphere_config = GkeonpremVmwareNodePoolConfigVsphereConfig(**vsphere_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cb5c5560e77a0c8c4af5a68b494a5c76cf9b796cefd2320591b488bd993991b)
            check_type(argname="argument image_type", value=image_type, expected_type=type_hints["image_type"])
            check_type(argname="argument boot_disk_size_gb", value=boot_disk_size_gb, expected_type=type_hints["boot_disk_size_gb"])
            check_type(argname="argument cpus", value=cpus, expected_type=type_hints["cpus"])
            check_type(argname="argument enable_load_balancer", value=enable_load_balancer, expected_type=type_hints["enable_load_balancer"])
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument memory_mb", value=memory_mb, expected_type=type_hints["memory_mb"])
            check_type(argname="argument replicas", value=replicas, expected_type=type_hints["replicas"])
            check_type(argname="argument taints", value=taints, expected_type=type_hints["taints"])
            check_type(argname="argument vsphere_config", value=vsphere_config, expected_type=type_hints["vsphere_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "image_type": image_type,
        }
        if boot_disk_size_gb is not None:
            self._values["boot_disk_size_gb"] = boot_disk_size_gb
        if cpus is not None:
            self._values["cpus"] = cpus
        if enable_load_balancer is not None:
            self._values["enable_load_balancer"] = enable_load_balancer
        if image is not None:
            self._values["image"] = image
        if labels is not None:
            self._values["labels"] = labels
        if memory_mb is not None:
            self._values["memory_mb"] = memory_mb
        if replicas is not None:
            self._values["replicas"] = replicas
        if taints is not None:
            self._values["taints"] = taints
        if vsphere_config is not None:
            self._values["vsphere_config"] = vsphere_config

    @builtins.property
    def image_type(self) -> builtins.str:
        '''The OS image to be used for each node in a node pool.

        Currently 'cos', 'cos_cgv2', 'ubuntu', 'ubuntu_cgv2', 'ubuntu_containerd' and 'windows' are supported.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#image_type GkeonpremVmwareNodePool#image_type}
        '''
        result = self._values.get("image_type")
        assert result is not None, "Required property 'image_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def boot_disk_size_gb(self) -> typing.Optional[jsii.Number]:
        '''VMware disk size to be used during creation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#boot_disk_size_gb GkeonpremVmwareNodePool#boot_disk_size_gb}
        '''
        result = self._values.get("boot_disk_size_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def cpus(self) -> typing.Optional[jsii.Number]:
        '''The number of CPUs for each node in the node pool.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#cpus GkeonpremVmwareNodePool#cpus}
        '''
        result = self._values.get("cpus")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def enable_load_balancer(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Allow node pool traffic to be load balanced. Only works for clusters with MetalLB load balancers.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#enable_load_balancer GkeonpremVmwareNodePool#enable_load_balancer}
        '''
        result = self._values.get("enable_load_balancer")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def image(self) -> typing.Optional[builtins.str]:
        '''The OS image name in vCenter, only valid when using Windows.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#image GkeonpremVmwareNodePool#image}
        '''
        result = self._values.get("image")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The map of Kubernetes labels (key/value pairs) to be applied to each node.

        These will added in addition to any default label(s) that
        Kubernetes may apply to the node.
        In case of conflict in label keys, the applied set may differ depending on
        the Kubernetes version -- it's best to assume the behavior is undefined
        and conflicts should be avoided.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#labels GkeonpremVmwareNodePool#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def memory_mb(self) -> typing.Optional[jsii.Number]:
        '''The megabytes of memory for each node in the node pool.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#memory_mb GkeonpremVmwareNodePool#memory_mb}
        '''
        result = self._values.get("memory_mb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def replicas(self) -> typing.Optional[jsii.Number]:
        '''The number of nodes in the node pool.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#replicas GkeonpremVmwareNodePool#replicas}
        '''
        result = self._values.get("replicas")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def taints(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeonpremVmwareNodePoolConfigTaints"]]]:
        '''taints block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#taints GkeonpremVmwareNodePool#taints}
        '''
        result = self._values.get("taints")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeonpremVmwareNodePoolConfigTaints"]]], result)

    @builtins.property
    def vsphere_config(
        self,
    ) -> typing.Optional["GkeonpremVmwareNodePoolConfigVsphereConfig"]:
        '''vsphere_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#vsphere_config GkeonpremVmwareNodePool#vsphere_config}
        '''
        result = self._values.get("vsphere_config")
        return typing.cast(typing.Optional["GkeonpremVmwareNodePoolConfigVsphereConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareNodePoolConfigA(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremVmwareNodePoolConfigAOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareNodePool.GkeonpremVmwareNodePoolConfigAOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f6e8d03172e0e5c42e8bed0f4ae5a1782a74f24fdce1138ed76ad55bf6378513)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putTaints")
    def put_taints(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeonpremVmwareNodePoolConfigTaints", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc619b7372f1d86dec8acf215dc5bc0e6bc98a1012331b3b5cd8429851ec2949)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTaints", [value]))

    @jsii.member(jsii_name="putVsphereConfig")
    def put_vsphere_config(
        self,
        *,
        datastore: typing.Optional[builtins.str] = None,
        host_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeonpremVmwareNodePoolConfigVsphereConfigTags", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param datastore: The name of the vCenter datastore. Inherited from the user cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#datastore GkeonpremVmwareNodePool#datastore}
        :param host_groups: Vsphere host groups to apply to all VMs in the node pool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#host_groups GkeonpremVmwareNodePool#host_groups}
        :param tags: tags block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#tags GkeonpremVmwareNodePool#tags}
        '''
        value = GkeonpremVmwareNodePoolConfigVsphereConfig(
            datastore=datastore, host_groups=host_groups, tags=tags
        )

        return typing.cast(None, jsii.invoke(self, "putVsphereConfig", [value]))

    @jsii.member(jsii_name="resetBootDiskSizeGb")
    def reset_boot_disk_size_gb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBootDiskSizeGb", []))

    @jsii.member(jsii_name="resetCpus")
    def reset_cpus(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpus", []))

    @jsii.member(jsii_name="resetEnableLoadBalancer")
    def reset_enable_load_balancer(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableLoadBalancer", []))

    @jsii.member(jsii_name="resetImage")
    def reset_image(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImage", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetMemoryMb")
    def reset_memory_mb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemoryMb", []))

    @jsii.member(jsii_name="resetReplicas")
    def reset_replicas(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReplicas", []))

    @jsii.member(jsii_name="resetTaints")
    def reset_taints(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTaints", []))

    @jsii.member(jsii_name="resetVsphereConfig")
    def reset_vsphere_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVsphereConfig", []))

    @builtins.property
    @jsii.member(jsii_name="taints")
    def taints(self) -> "GkeonpremVmwareNodePoolConfigTaintsList":
        return typing.cast("GkeonpremVmwareNodePoolConfigTaintsList", jsii.get(self, "taints"))

    @builtins.property
    @jsii.member(jsii_name="vsphereConfig")
    def vsphere_config(
        self,
    ) -> "GkeonpremVmwareNodePoolConfigVsphereConfigOutputReference":
        return typing.cast("GkeonpremVmwareNodePoolConfigVsphereConfigOutputReference", jsii.get(self, "vsphereConfig"))

    @builtins.property
    @jsii.member(jsii_name="bootDiskSizeGbInput")
    def boot_disk_size_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "bootDiskSizeGbInput"))

    @builtins.property
    @jsii.member(jsii_name="cpusInput")
    def cpus_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "cpusInput"))

    @builtins.property
    @jsii.member(jsii_name="enableLoadBalancerInput")
    def enable_load_balancer_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableLoadBalancerInput"))

    @builtins.property
    @jsii.member(jsii_name="imageInput")
    def image_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageInput"))

    @builtins.property
    @jsii.member(jsii_name="imageTypeInput")
    def image_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="memoryMbInput")
    def memory_mb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "memoryMbInput"))

    @builtins.property
    @jsii.member(jsii_name="replicasInput")
    def replicas_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "replicasInput"))

    @builtins.property
    @jsii.member(jsii_name="taintsInput")
    def taints_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeonpremVmwareNodePoolConfigTaints"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeonpremVmwareNodePoolConfigTaints"]]], jsii.get(self, "taintsInput"))

    @builtins.property
    @jsii.member(jsii_name="vsphereConfigInput")
    def vsphere_config_input(
        self,
    ) -> typing.Optional["GkeonpremVmwareNodePoolConfigVsphereConfig"]:
        return typing.cast(typing.Optional["GkeonpremVmwareNodePoolConfigVsphereConfig"], jsii.get(self, "vsphereConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="bootDiskSizeGb")
    def boot_disk_size_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bootDiskSizeGb"))

    @boot_disk_size_gb.setter
    def boot_disk_size_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7de8b349500fa213ac7e06e7c8a47e24fcb64f50742ae2c31e84c51cca471e88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bootDiskSizeGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cpus")
    def cpus(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cpus"))

    @cpus.setter
    def cpus(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0998130adc9ab7a0340f8dac923a2b0ffe76d3cec65fe030ec8bf81c49f9dd4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableLoadBalancer")
    def enable_load_balancer(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableLoadBalancer"))

    @enable_load_balancer.setter
    def enable_load_balancer(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56e2a7439ff1d1fd8e631298b405936ecdad0a44b30926484a27d0067a4a8888)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableLoadBalancer", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "image"))

    @image.setter
    def image(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d00556bb03a3ef839eff88fffd7bdf49737c9b5d2378d5a3174bf4f5fb19b3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "image", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="imageType")
    def image_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageType"))

    @image_type.setter
    def image_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10995b207d6ae3f35a455b2639aae20c537d54da89face1b7244128fe5481290)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3132fb4071fdb109f90e9a19e3d502306e8b0b4da5593198b02053f1daea3fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memoryMb")
    def memory_mb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memoryMb"))

    @memory_mb.setter
    def memory_mb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__352ef4a4cdad71756c2900a3e93d83d3b7849dafe21925f7c9787c3b081dd061)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memoryMb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="replicas")
    def replicas(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "replicas"))

    @replicas.setter
    def replicas(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbe64adbc0888bee4bc961bdc5da03236235f177c4ea7b40302ed02a69ba4590)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replicas", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GkeonpremVmwareNodePoolConfigA]:
        return typing.cast(typing.Optional[GkeonpremVmwareNodePoolConfigA], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremVmwareNodePoolConfigA],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dad7d4485bf2014f730d409080690376c8c3d18e763aaf7affaaca9d99dd49e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareNodePool.GkeonpremVmwareNodePoolConfigTaints",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value", "effect": "effect"},
)
class GkeonpremVmwareNodePoolConfigTaints:
    def __init__(
        self,
        *,
        key: builtins.str,
        value: builtins.str,
        effect: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key: Key associated with the effect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#key GkeonpremVmwareNodePool#key}
        :param value: Value associated with the effect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#value GkeonpremVmwareNodePool#value}
        :param effect: Available taint effects. Possible values: ["EFFECT_UNSPECIFIED", "NO_SCHEDULE", "PREFER_NO_SCHEDULE", "NO_EXECUTE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#effect GkeonpremVmwareNodePool#effect}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b91faa930b4f771202bbbb9d85f52325f172a51b4c729e729c2cf4ea4f87ad98)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument effect", value=effect, expected_type=type_hints["effect"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "value": value,
        }
        if effect is not None:
            self._values["effect"] = effect

    @builtins.property
    def key(self) -> builtins.str:
        '''Key associated with the effect.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#key GkeonpremVmwareNodePool#key}
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Value associated with the effect.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#value GkeonpremVmwareNodePool#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def effect(self) -> typing.Optional[builtins.str]:
        '''Available taint effects. Possible values: ["EFFECT_UNSPECIFIED", "NO_SCHEDULE", "PREFER_NO_SCHEDULE", "NO_EXECUTE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#effect GkeonpremVmwareNodePool#effect}
        '''
        result = self._values.get("effect")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareNodePoolConfigTaints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremVmwareNodePoolConfigTaintsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareNodePool.GkeonpremVmwareNodePoolConfigTaintsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e1554d43debde666bafdeea6f40c51a5b3ed78babd71ba78fd44dd3cda8ee76)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeonpremVmwareNodePoolConfigTaintsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2ed8eae7a44962a638b2940bc1eb2f58d893771225e5891ba3f2248738b54cd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeonpremVmwareNodePoolConfigTaintsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5022d7b16977acfe97d424e47b43218c7c9434d7d14b60473788af089c14b31e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d17e74b9c0ff390e020f8f33d4ddadf96ff643f45d57f762dd1e39bae4ae29e8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__994d4ca2d172dd9a2dbac88d25b0c12c381c844016e6eb1eac36dc27e3da7367)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremVmwareNodePoolConfigTaints]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremVmwareNodePoolConfigTaints]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremVmwareNodePoolConfigTaints]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d4559443b5248322865461428eedc525dc6fef46662c34c1b55a4de3d709a3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremVmwareNodePoolConfigTaintsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareNodePool.GkeonpremVmwareNodePoolConfigTaintsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e634612dcf9c439322dd652a243d3a33eaa3f705fbe90575b6e23beef8f3dc6e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetEffect")
    def reset_effect(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEffect", []))

    @builtins.property
    @jsii.member(jsii_name="effectInput")
    def effect_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "effectInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="effect")
    def effect(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "effect"))

    @effect.setter
    def effect(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__174fcec20f74be1fc60c70586f2830d769c73039ad944184a12720b84cae4c37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "effect", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c65c4228aae10bbd00dac82c229abb8d59c667d56b3db3600929e8a0ee90c8b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d674f8808a82eead315ba51e1e59cfdcee68f208046b5c706c7aa4b96a4a8abe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremVmwareNodePoolConfigTaints]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremVmwareNodePoolConfigTaints]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremVmwareNodePoolConfigTaints]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6917d0c41132be81791cb60607038c76f1a05ce10c43eac43a9e4fc35723ac3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareNodePool.GkeonpremVmwareNodePoolConfigVsphereConfig",
    jsii_struct_bases=[],
    name_mapping={
        "datastore": "datastore",
        "host_groups": "hostGroups",
        "tags": "tags",
    },
)
class GkeonpremVmwareNodePoolConfigVsphereConfig:
    def __init__(
        self,
        *,
        datastore: typing.Optional[builtins.str] = None,
        host_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeonpremVmwareNodePoolConfigVsphereConfigTags", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param datastore: The name of the vCenter datastore. Inherited from the user cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#datastore GkeonpremVmwareNodePool#datastore}
        :param host_groups: Vsphere host groups to apply to all VMs in the node pool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#host_groups GkeonpremVmwareNodePool#host_groups}
        :param tags: tags block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#tags GkeonpremVmwareNodePool#tags}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c22224264be487d3024ba720b54164b4f20b208fb8a1a3d909e64cb3223aacfe)
            check_type(argname="argument datastore", value=datastore, expected_type=type_hints["datastore"])
            check_type(argname="argument host_groups", value=host_groups, expected_type=type_hints["host_groups"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if datastore is not None:
            self._values["datastore"] = datastore
        if host_groups is not None:
            self._values["host_groups"] = host_groups
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def datastore(self) -> typing.Optional[builtins.str]:
        '''The name of the vCenter datastore. Inherited from the user cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#datastore GkeonpremVmwareNodePool#datastore}
        '''
        result = self._values.get("datastore")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def host_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Vsphere host groups to apply to all VMs in the node pool.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#host_groups GkeonpremVmwareNodePool#host_groups}
        '''
        result = self._values.get("host_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeonpremVmwareNodePoolConfigVsphereConfigTags"]]]:
        '''tags block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#tags GkeonpremVmwareNodePool#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeonpremVmwareNodePoolConfigVsphereConfigTags"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareNodePoolConfigVsphereConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremVmwareNodePoolConfigVsphereConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareNodePool.GkeonpremVmwareNodePoolConfigVsphereConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__41f7b5927ef00d7180f77bf34419df06d68d06c5d99ce95ccc6fbdc766a4aa3b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putTags")
    def put_tags(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeonpremVmwareNodePoolConfigVsphereConfigTags", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e26c47a14b2f14436161a9cc913d3194368a62b72983112be8be25aac724fd90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTags", [value]))

    @jsii.member(jsii_name="resetDatastore")
    def reset_datastore(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatastore", []))

    @jsii.member(jsii_name="resetHostGroups")
    def reset_host_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostGroups", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> "GkeonpremVmwareNodePoolConfigVsphereConfigTagsList":
        return typing.cast("GkeonpremVmwareNodePoolConfigVsphereConfigTagsList", jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="datastoreInput")
    def datastore_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "datastoreInput"))

    @builtins.property
    @jsii.member(jsii_name="hostGroupsInput")
    def host_groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "hostGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeonpremVmwareNodePoolConfigVsphereConfigTags"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeonpremVmwareNodePoolConfigVsphereConfigTags"]]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="datastore")
    def datastore(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "datastore"))

    @datastore.setter
    def datastore(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d116997a494cd5a27b33b2d9dbe33c83180403c305006d933fb57066e7441035)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datastore", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostGroups")
    def host_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "hostGroups"))

    @host_groups.setter
    def host_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7357213bf1f57ac9073cb8356a2ca005fa2034c1b41a9506db1f17f5fa8f54f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremVmwareNodePoolConfigVsphereConfig]:
        return typing.cast(typing.Optional[GkeonpremVmwareNodePoolConfigVsphereConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremVmwareNodePoolConfigVsphereConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85293c7d0820c90a3b2f422f760e0a45d85846dde8437111361743178cd2d6ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareNodePool.GkeonpremVmwareNodePoolConfigVsphereConfigTags",
    jsii_struct_bases=[],
    name_mapping={"category": "category", "tag": "tag"},
)
class GkeonpremVmwareNodePoolConfigVsphereConfigTags:
    def __init__(
        self,
        *,
        category: typing.Optional[builtins.str] = None,
        tag: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param category: The Vsphere tag category. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#category GkeonpremVmwareNodePool#category}
        :param tag: The Vsphere tag name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#tag GkeonpremVmwareNodePool#tag}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88bcf5770fdd71f8d1106318be4eb0001a9aec5d6562dec1411fcb3aebbb53e8)
            check_type(argname="argument category", value=category, expected_type=type_hints["category"])
            check_type(argname="argument tag", value=tag, expected_type=type_hints["tag"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if category is not None:
            self._values["category"] = category
        if tag is not None:
            self._values["tag"] = tag

    @builtins.property
    def category(self) -> typing.Optional[builtins.str]:
        '''The Vsphere tag category.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#category GkeonpremVmwareNodePool#category}
        '''
        result = self._values.get("category")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag(self) -> typing.Optional[builtins.str]:
        '''The Vsphere tag name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#tag GkeonpremVmwareNodePool#tag}
        '''
        result = self._values.get("tag")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareNodePoolConfigVsphereConfigTags(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremVmwareNodePoolConfigVsphereConfigTagsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareNodePool.GkeonpremVmwareNodePoolConfigVsphereConfigTagsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb34075c6de6472617554ac4516435e48cf042e5f9f379e27460254ceeacc397)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeonpremVmwareNodePoolConfigVsphereConfigTagsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa19a8281f449149b81f8f28abafd438113bc2ce88b80b0873ad86180c8da6a1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeonpremVmwareNodePoolConfigVsphereConfigTagsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4ca6ba95930d1fd2c66fde1519d0dfd0c8fd34958d8724cac0543294d6d6cf5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fefd06ff93ee11fce63226869f961e02989b6063a971a6ff2f5ab004dbc89685)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d06926eab1a57ad02c99f828edf2dc72529db3d562cb8830c30e00628418d25f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremVmwareNodePoolConfigVsphereConfigTags]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremVmwareNodePoolConfigVsphereConfigTags]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremVmwareNodePoolConfigVsphereConfigTags]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbb4cd2edb806fcf79423eb5d5728010c879e8cf8c9cc502839458becdfab9e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremVmwareNodePoolConfigVsphereConfigTagsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareNodePool.GkeonpremVmwareNodePoolConfigVsphereConfigTagsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3d62e62c1af2e7df1c8b95038cbb0beb412e9bfe151ae9636288fcc78ac916f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetCategory")
    def reset_category(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCategory", []))

    @jsii.member(jsii_name="resetTag")
    def reset_tag(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTag", []))

    @builtins.property
    @jsii.member(jsii_name="categoryInput")
    def category_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "categoryInput"))

    @builtins.property
    @jsii.member(jsii_name="tagInput")
    def tag_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagInput"))

    @builtins.property
    @jsii.member(jsii_name="category")
    def category(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "category"))

    @category.setter
    def category(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8de3d5dccca719470631ee99a9f09033f0b46340ae4c613f07c8bdf9740f60c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "category", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tag")
    def tag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tag"))

    @tag.setter
    def tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c42b0eeac79d79ab9291c8221ad36929185c4b534edb487f04888d436691596f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tag", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremVmwareNodePoolConfigVsphereConfigTags]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremVmwareNodePoolConfigVsphereConfigTags]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremVmwareNodePoolConfigVsphereConfigTags]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67f3d4c8a3a5e4c0240ff9fe37c8f8fb61ed3910ce9f06389958092cccf24c5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareNodePool.GkeonpremVmwareNodePoolNodePoolAutoscaling",
    jsii_struct_bases=[],
    name_mapping={"max_replicas": "maxReplicas", "min_replicas": "minReplicas"},
)
class GkeonpremVmwareNodePoolNodePoolAutoscaling:
    def __init__(self, *, max_replicas: jsii.Number, min_replicas: jsii.Number) -> None:
        '''
        :param max_replicas: Maximum number of replicas in the NodePool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#max_replicas GkeonpremVmwareNodePool#max_replicas}
        :param min_replicas: Minimum number of replicas in the NodePool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#min_replicas GkeonpremVmwareNodePool#min_replicas}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__419e001c1ca4f112ef331f00e62b72f0426b9070c90f914e494699d526d3f874)
            check_type(argname="argument max_replicas", value=max_replicas, expected_type=type_hints["max_replicas"])
            check_type(argname="argument min_replicas", value=min_replicas, expected_type=type_hints["min_replicas"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "max_replicas": max_replicas,
            "min_replicas": min_replicas,
        }

    @builtins.property
    def max_replicas(self) -> jsii.Number:
        '''Maximum number of replicas in the NodePool.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#max_replicas GkeonpremVmwareNodePool#max_replicas}
        '''
        result = self._values.get("max_replicas")
        assert result is not None, "Required property 'max_replicas' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def min_replicas(self) -> jsii.Number:
        '''Minimum number of replicas in the NodePool.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#min_replicas GkeonpremVmwareNodePool#min_replicas}
        '''
        result = self._values.get("min_replicas")
        assert result is not None, "Required property 'min_replicas' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareNodePoolNodePoolAutoscaling(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremVmwareNodePoolNodePoolAutoscalingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareNodePool.GkeonpremVmwareNodePoolNodePoolAutoscalingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__33517f18fb4254940ca5bef13afc6944e0fd5f29709bfda1df457e3a472dc782)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="maxReplicasInput")
    def max_replicas_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxReplicasInput"))

    @builtins.property
    @jsii.member(jsii_name="minReplicasInput")
    def min_replicas_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minReplicasInput"))

    @builtins.property
    @jsii.member(jsii_name="maxReplicas")
    def max_replicas(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxReplicas"))

    @max_replicas.setter
    def max_replicas(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39e37cc49cef164e94bfb2285278d019eb92f05fd3e0c2ace04ed42f10e6bd49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxReplicas", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minReplicas")
    def min_replicas(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minReplicas"))

    @min_replicas.setter
    def min_replicas(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebe828226a2aedcca5da6bf448d6be8a61268039dfd2b5719088ed7250f6f0f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minReplicas", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremVmwareNodePoolNodePoolAutoscaling]:
        return typing.cast(typing.Optional[GkeonpremVmwareNodePoolNodePoolAutoscaling], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremVmwareNodePoolNodePoolAutoscaling],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b649e6197fdefb8c3baa848c674a7120cbd0cb7269d11ad16b563c86acb9f88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareNodePool.GkeonpremVmwareNodePoolStatus",
    jsii_struct_bases=[],
    name_mapping={},
)
class GkeonpremVmwareNodePoolStatus:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareNodePoolStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareNodePool.GkeonpremVmwareNodePoolStatusConditions",
    jsii_struct_bases=[],
    name_mapping={},
)
class GkeonpremVmwareNodePoolStatusConditions:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareNodePoolStatusConditions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremVmwareNodePoolStatusConditionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareNodePool.GkeonpremVmwareNodePoolStatusConditionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__207476f6bd1c6f36368a2121ec32676e17153d350cb0cc9903b0c6975dbb71bc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeonpremVmwareNodePoolStatusConditionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a89827448a7b8ea6fd1f1a35ab021291316075851c0e2226703abaf846460a3e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeonpremVmwareNodePoolStatusConditionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2349b024bc16e8539eba13b5b3a721b0a6ada3ba0e07f72a2c8b65ee96c53848)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb41eb4649b2588f68e3c3e30bb9d1965c1d6ea20f3e7406187fa99c2e6f87bc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e709a369240e988b74fe4c928ae01eeead181b8e41407e08dd5cebf37226128)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GkeonpremVmwareNodePoolStatusConditionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareNodePool.GkeonpremVmwareNodePoolStatusConditionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__32612ef29dcb39a45efac1754d17148a7e190a22fe3be264c4496a68eaaacf35)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="lastTransitionTime")
    def last_transition_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastTransitionTime"))

    @builtins.property
    @jsii.member(jsii_name="message")
    def message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "message"))

    @builtins.property
    @jsii.member(jsii_name="reason")
    def reason(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "reason"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremVmwareNodePoolStatusConditions]:
        return typing.cast(typing.Optional[GkeonpremVmwareNodePoolStatusConditions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremVmwareNodePoolStatusConditions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b43169916f812ce5bce617e027c91a2347657020f58733030e47717828f5bd08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremVmwareNodePoolStatusList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareNodePool.GkeonpremVmwareNodePoolStatusList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ba22a05f1e528ba085a0ca411988b0e21f3d61e1f92116766cce66f667fd549)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "GkeonpremVmwareNodePoolStatusOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6945992c25910cf3d0ff440c234f330c05da459c57775eab17974acae962fa30)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeonpremVmwareNodePoolStatusOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b42a171e546be4b3f796c32153228a09afe45e122d93b1870620fbdb91897084)
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
            type_hints = typing.get_type_hints(_typecheckingstub__12544a283ed4a8f2d53a6a2a5f6d5dd2145662468d8f1a2a3c52c9d00a0c8af6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__deb5ea078e99ef44153127c1123044894979499a2c63e16d8df80e3e4526d39d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GkeonpremVmwareNodePoolStatusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareNodePool.GkeonpremVmwareNodePoolStatusOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a92401aadeb2237a474a776b984f05abe51f11933e74e608742a62e6c2568563)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="conditions")
    def conditions(self) -> GkeonpremVmwareNodePoolStatusConditionsList:
        return typing.cast(GkeonpremVmwareNodePoolStatusConditionsList, jsii.get(self, "conditions"))

    @builtins.property
    @jsii.member(jsii_name="errorMessage")
    def error_message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "errorMessage"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GkeonpremVmwareNodePoolStatus]:
        return typing.cast(typing.Optional[GkeonpremVmwareNodePoolStatus], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremVmwareNodePoolStatus],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3494ba2b6ee0835b20c4dacc8ccec89ba24a24a8b7d891d5621b3dadb6a2619)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremVmwareNodePool.GkeonpremVmwareNodePoolTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GkeonpremVmwareNodePoolTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#create GkeonpremVmwareNodePool#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#delete GkeonpremVmwareNodePool#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#update GkeonpremVmwareNodePool#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9bd377a70518e72e44d5c737204537e676651a9c1cce350fc01ff1c25875c60)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#create GkeonpremVmwareNodePool#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#delete GkeonpremVmwareNodePool#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_vmware_node_pool#update GkeonpremVmwareNodePool#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremVmwareNodePoolTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremVmwareNodePoolTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremVmwareNodePool.GkeonpremVmwareNodePoolTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b6be19154a0b0011acbfb63d2be2f9b4db13b7c3fa8cf12199f72a514276a920)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef815c113595e67bf9503655c4eaccd954946ffcf89d2e8d66c4081f29e11ed7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd17a2acd8c7f06dfd6eee5ef02cbf04122e44b233fc962be36b02b9aa8414c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba83f51ad15701dc4c5085db930543f650ecd7f5e0723b0270bf70564104a5da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremVmwareNodePoolTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremVmwareNodePoolTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremVmwareNodePoolTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db7ae2a35abb56df94ca4641fbe76dcca3360688afd08458b83b3d5b8a93ba99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GkeonpremVmwareNodePool",
    "GkeonpremVmwareNodePoolConfig",
    "GkeonpremVmwareNodePoolConfigA",
    "GkeonpremVmwareNodePoolConfigAOutputReference",
    "GkeonpremVmwareNodePoolConfigTaints",
    "GkeonpremVmwareNodePoolConfigTaintsList",
    "GkeonpremVmwareNodePoolConfigTaintsOutputReference",
    "GkeonpremVmwareNodePoolConfigVsphereConfig",
    "GkeonpremVmwareNodePoolConfigVsphereConfigOutputReference",
    "GkeonpremVmwareNodePoolConfigVsphereConfigTags",
    "GkeonpremVmwareNodePoolConfigVsphereConfigTagsList",
    "GkeonpremVmwareNodePoolConfigVsphereConfigTagsOutputReference",
    "GkeonpremVmwareNodePoolNodePoolAutoscaling",
    "GkeonpremVmwareNodePoolNodePoolAutoscalingOutputReference",
    "GkeonpremVmwareNodePoolStatus",
    "GkeonpremVmwareNodePoolStatusConditions",
    "GkeonpremVmwareNodePoolStatusConditionsList",
    "GkeonpremVmwareNodePoolStatusConditionsOutputReference",
    "GkeonpremVmwareNodePoolStatusList",
    "GkeonpremVmwareNodePoolStatusOutputReference",
    "GkeonpremVmwareNodePoolTimeouts",
    "GkeonpremVmwareNodePoolTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__a62e910fa7527da411324f8eab8af9ce7ccb1edbf095167ea892bf83675a15d6(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    config: typing.Union[GkeonpremVmwareNodePoolConfigA, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    name: builtins.str,
    vmware_cluster: builtins.str,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    node_pool_autoscaling: typing.Optional[typing.Union[GkeonpremVmwareNodePoolNodePoolAutoscaling, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GkeonpremVmwareNodePoolTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__b31dd49eb436b56364467dfd1d37afec494f3c68d646aabaf34b29b7b1958aa2(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be4dc77870b59b1671afa91887a239cfef7caecd196c3882e2155e9488e168f8(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1abf44b4d3f09c3dbb39e2dcf2b63aa400142c7ccba99095cf2ab74974c88994(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7a70ceafd5f08aae7444bbe311f988035cf47c8875563889ebd07923e87cae1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51563c744d94c840463ea50d5c9df2eb71a4d65b85a5f8453693c2b5a557c371(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__553a10c00132055b01a955df3f5ad3f167f8c0c8bdb3e600ed7b2952db8a3f89(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8282f18c0dbe5c1c81dd7ed9d70a19566fb4cf1b0ceac0cb2a21ec75fa59e99d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__babd6b294c6caf4572f23e3499ef1c2a712b1ea147e564bf3d5febc1590b0d70(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52e1324f8be0dc2acc7e7e82a1e142a79e807bbbfb5d892bba036e462fe6ef6a(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    config: typing.Union[GkeonpremVmwareNodePoolConfigA, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    name: builtins.str,
    vmware_cluster: builtins.str,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    node_pool_autoscaling: typing.Optional[typing.Union[GkeonpremVmwareNodePoolNodePoolAutoscaling, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GkeonpremVmwareNodePoolTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cb5c5560e77a0c8c4af5a68b494a5c76cf9b796cefd2320591b488bd993991b(
    *,
    image_type: builtins.str,
    boot_disk_size_gb: typing.Optional[jsii.Number] = None,
    cpus: typing.Optional[jsii.Number] = None,
    enable_load_balancer: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    image: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    memory_mb: typing.Optional[jsii.Number] = None,
    replicas: typing.Optional[jsii.Number] = None,
    taints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremVmwareNodePoolConfigTaints, typing.Dict[builtins.str, typing.Any]]]]] = None,
    vsphere_config: typing.Optional[typing.Union[GkeonpremVmwareNodePoolConfigVsphereConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6e8d03172e0e5c42e8bed0f4ae5a1782a74f24fdce1138ed76ad55bf6378513(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc619b7372f1d86dec8acf215dc5bc0e6bc98a1012331b3b5cd8429851ec2949(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremVmwareNodePoolConfigTaints, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7de8b349500fa213ac7e06e7c8a47e24fcb64f50742ae2c31e84c51cca471e88(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0998130adc9ab7a0340f8dac923a2b0ffe76d3cec65fe030ec8bf81c49f9dd4b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56e2a7439ff1d1fd8e631298b405936ecdad0a44b30926484a27d0067a4a8888(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d00556bb03a3ef839eff88fffd7bdf49737c9b5d2378d5a3174bf4f5fb19b3f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10995b207d6ae3f35a455b2639aae20c537d54da89face1b7244128fe5481290(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3132fb4071fdb109f90e9a19e3d502306e8b0b4da5593198b02053f1daea3fb(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__352ef4a4cdad71756c2900a3e93d83d3b7849dafe21925f7c9787c3b081dd061(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbe64adbc0888bee4bc961bdc5da03236235f177c4ea7b40302ed02a69ba4590(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dad7d4485bf2014f730d409080690376c8c3d18e763aaf7affaaca9d99dd49e1(
    value: typing.Optional[GkeonpremVmwareNodePoolConfigA],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b91faa930b4f771202bbbb9d85f52325f172a51b4c729e729c2cf4ea4f87ad98(
    *,
    key: builtins.str,
    value: builtins.str,
    effect: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e1554d43debde666bafdeea6f40c51a5b3ed78babd71ba78fd44dd3cda8ee76(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2ed8eae7a44962a638b2940bc1eb2f58d893771225e5891ba3f2248738b54cd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5022d7b16977acfe97d424e47b43218c7c9434d7d14b60473788af089c14b31e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d17e74b9c0ff390e020f8f33d4ddadf96ff643f45d57f762dd1e39bae4ae29e8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__994d4ca2d172dd9a2dbac88d25b0c12c381c844016e6eb1eac36dc27e3da7367(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d4559443b5248322865461428eedc525dc6fef46662c34c1b55a4de3d709a3c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremVmwareNodePoolConfigTaints]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e634612dcf9c439322dd652a243d3a33eaa3f705fbe90575b6e23beef8f3dc6e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__174fcec20f74be1fc60c70586f2830d769c73039ad944184a12720b84cae4c37(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c65c4228aae10bbd00dac82c229abb8d59c667d56b3db3600929e8a0ee90c8b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d674f8808a82eead315ba51e1e59cfdcee68f208046b5c706c7aa4b96a4a8abe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6917d0c41132be81791cb60607038c76f1a05ce10c43eac43a9e4fc35723ac3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremVmwareNodePoolConfigTaints]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c22224264be487d3024ba720b54164b4f20b208fb8a1a3d909e64cb3223aacfe(
    *,
    datastore: typing.Optional[builtins.str] = None,
    host_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremVmwareNodePoolConfigVsphereConfigTags, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41f7b5927ef00d7180f77bf34419df06d68d06c5d99ce95ccc6fbdc766a4aa3b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e26c47a14b2f14436161a9cc913d3194368a62b72983112be8be25aac724fd90(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremVmwareNodePoolConfigVsphereConfigTags, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d116997a494cd5a27b33b2d9dbe33c83180403c305006d933fb57066e7441035(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7357213bf1f57ac9073cb8356a2ca005fa2034c1b41a9506db1f17f5fa8f54f7(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85293c7d0820c90a3b2f422f760e0a45d85846dde8437111361743178cd2d6ee(
    value: typing.Optional[GkeonpremVmwareNodePoolConfigVsphereConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88bcf5770fdd71f8d1106318be4eb0001a9aec5d6562dec1411fcb3aebbb53e8(
    *,
    category: typing.Optional[builtins.str] = None,
    tag: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb34075c6de6472617554ac4516435e48cf042e5f9f379e27460254ceeacc397(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa19a8281f449149b81f8f28abafd438113bc2ce88b80b0873ad86180c8da6a1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4ca6ba95930d1fd2c66fde1519d0dfd0c8fd34958d8724cac0543294d6d6cf5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fefd06ff93ee11fce63226869f961e02989b6063a971a6ff2f5ab004dbc89685(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d06926eab1a57ad02c99f828edf2dc72529db3d562cb8830c30e00628418d25f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbb4cd2edb806fcf79423eb5d5728010c879e8cf8c9cc502839458becdfab9e9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremVmwareNodePoolConfigVsphereConfigTags]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3d62e62c1af2e7df1c8b95038cbb0beb412e9bfe151ae9636288fcc78ac916f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8de3d5dccca719470631ee99a9f09033f0b46340ae4c613f07c8bdf9740f60c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c42b0eeac79d79ab9291c8221ad36929185c4b534edb487f04888d436691596f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67f3d4c8a3a5e4c0240ff9fe37c8f8fb61ed3910ce9f06389958092cccf24c5d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremVmwareNodePoolConfigVsphereConfigTags]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__419e001c1ca4f112ef331f00e62b72f0426b9070c90f914e494699d526d3f874(
    *,
    max_replicas: jsii.Number,
    min_replicas: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33517f18fb4254940ca5bef13afc6944e0fd5f29709bfda1df457e3a472dc782(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39e37cc49cef164e94bfb2285278d019eb92f05fd3e0c2ace04ed42f10e6bd49(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebe828226a2aedcca5da6bf448d6be8a61268039dfd2b5719088ed7250f6f0f7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b649e6197fdefb8c3baa848c674a7120cbd0cb7269d11ad16b563c86acb9f88(
    value: typing.Optional[GkeonpremVmwareNodePoolNodePoolAutoscaling],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__207476f6bd1c6f36368a2121ec32676e17153d350cb0cc9903b0c6975dbb71bc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a89827448a7b8ea6fd1f1a35ab021291316075851c0e2226703abaf846460a3e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2349b024bc16e8539eba13b5b3a721b0a6ada3ba0e07f72a2c8b65ee96c53848(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb41eb4649b2588f68e3c3e30bb9d1965c1d6ea20f3e7406187fa99c2e6f87bc(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e709a369240e988b74fe4c928ae01eeead181b8e41407e08dd5cebf37226128(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32612ef29dcb39a45efac1754d17148a7e190a22fe3be264c4496a68eaaacf35(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b43169916f812ce5bce617e027c91a2347657020f58733030e47717828f5bd08(
    value: typing.Optional[GkeonpremVmwareNodePoolStatusConditions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ba22a05f1e528ba085a0ca411988b0e21f3d61e1f92116766cce66f667fd549(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6945992c25910cf3d0ff440c234f330c05da459c57775eab17974acae962fa30(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b42a171e546be4b3f796c32153228a09afe45e122d93b1870620fbdb91897084(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12544a283ed4a8f2d53a6a2a5f6d5dd2145662468d8f1a2a3c52c9d00a0c8af6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__deb5ea078e99ef44153127c1123044894979499a2c63e16d8df80e3e4526d39d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a92401aadeb2237a474a776b984f05abe51f11933e74e608742a62e6c2568563(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3494ba2b6ee0835b20c4dacc8ccec89ba24a24a8b7d891d5621b3dadb6a2619(
    value: typing.Optional[GkeonpremVmwareNodePoolStatus],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9bd377a70518e72e44d5c737204537e676651a9c1cce350fc01ff1c25875c60(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6be19154a0b0011acbfb63d2be2f9b4db13b7c3fa8cf12199f72a514276a920(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef815c113595e67bf9503655c4eaccd954946ffcf89d2e8d66c4081f29e11ed7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd17a2acd8c7f06dfd6eee5ef02cbf04122e44b233fc962be36b02b9aa8414c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba83f51ad15701dc4c5085db930543f650ecd7f5e0723b0270bf70564104a5da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db7ae2a35abb56df94ca4641fbe76dcca3360688afd08458b83b3d5b8a93ba99(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremVmwareNodePoolTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
