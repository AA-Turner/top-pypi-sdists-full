r'''
# `google_container_azure_node_pool`

Refer to the Terraform Registry for docs: [`google_container_azure_node_pool`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool).
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


class ContainerAzureNodePool(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAzureNodePool.ContainerAzureNodePool",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool google_container_azure_node_pool}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        autoscaling: typing.Union["ContainerAzureNodePoolAutoscaling", typing.Dict[builtins.str, typing.Any]],
        cluster: builtins.str,
        config: typing.Union["ContainerAzureNodePoolConfigA", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        max_pods_constraint: typing.Union["ContainerAzureNodePoolMaxPodsConstraint", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        subnet_id: builtins.str,
        version: builtins.str,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        azure_availability_zone: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        management: typing.Optional[typing.Union["ContainerAzureNodePoolManagement", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ContainerAzureNodePoolTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool google_container_azure_node_pool} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param autoscaling: autoscaling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#autoscaling ContainerAzureNodePool#autoscaling}
        :param cluster: The azureCluster for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#cluster ContainerAzureNodePool#cluster}
        :param config: config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#config ContainerAzureNodePool#config}
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#location ContainerAzureNodePool#location}
        :param max_pods_constraint: max_pods_constraint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#max_pods_constraint ContainerAzureNodePool#max_pods_constraint}
        :param name: The name of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#name ContainerAzureNodePool#name}
        :param subnet_id: The ARM ID of the subnet where the node pool VMs run. Make sure it's a subnet under the virtual network in the cluster configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#subnet_id ContainerAzureNodePool#subnet_id}
        :param version: The Kubernetes version (e.g. ``1.19.10-gke.1000``) running on this node pool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#version ContainerAzureNodePool#version}
        :param annotations: Optional. Annotations on the node pool. This field has the same restrictions as Kubernetes annotations. The total size of all keys and values combined is limited to 256k. Keys can have 2 segments: prefix (optional) and name (required), separated by a slash (/). Prefix must be a DNS subdomain. Name must be 63 characters or less, begin and end with alphanumerics, with dashes (-), underscores (_), dots (.), and alphanumerics between. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field ``effective_annotations`` for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#annotations ContainerAzureNodePool#annotations}
        :param azure_availability_zone: Optional. The Azure availability zone of the nodes in this nodepool. When unspecified, it defaults to ``1``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#azure_availability_zone ContainerAzureNodePool#azure_availability_zone}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#id ContainerAzureNodePool#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param management: management block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#management ContainerAzureNodePool#management}
        :param project: The project for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#project ContainerAzureNodePool#project}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#timeouts ContainerAzureNodePool#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d4055f2e298ce2d0f1f221695aebdbcbff0bb1f68e3d2d3c579847162ad00d3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config_ = ContainerAzureNodePoolConfig(
            autoscaling=autoscaling,
            cluster=cluster,
            config=config,
            location=location,
            max_pods_constraint=max_pods_constraint,
            name=name,
            subnet_id=subnet_id,
            version=version,
            annotations=annotations,
            azure_availability_zone=azure_availability_zone,
            id=id,
            management=management,
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
        '''Generates CDKTF code for importing a ContainerAzureNodePool resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ContainerAzureNodePool to import.
        :param import_from_id: The id of the existing ContainerAzureNodePool that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ContainerAzureNodePool to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__407a00f41f50ed5506105df5e5975abb94b53da8dafd80ce6f67358a2f3382b0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAutoscaling")
    def put_autoscaling(
        self,
        *,
        max_node_count: jsii.Number,
        min_node_count: jsii.Number,
    ) -> None:
        '''
        :param max_node_count: Maximum number of nodes in the node pool. Must be >= min_node_count. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#max_node_count ContainerAzureNodePool#max_node_count}
        :param min_node_count: Minimum number of nodes in the node pool. Must be >= 1 and <= max_node_count. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#min_node_count ContainerAzureNodePool#min_node_count}
        '''
        value = ContainerAzureNodePoolAutoscaling(
            max_node_count=max_node_count, min_node_count=min_node_count
        )

        return typing.cast(None, jsii.invoke(self, "putAutoscaling", [value]))

    @jsii.member(jsii_name="putConfig")
    def put_config(
        self,
        *,
        ssh_config: typing.Union["ContainerAzureNodePoolConfigSshConfig", typing.Dict[builtins.str, typing.Any]],
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        proxy_config: typing.Optional[typing.Union["ContainerAzureNodePoolConfigProxyConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        root_volume: typing.Optional[typing.Union["ContainerAzureNodePoolConfigRootVolume", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        vm_size: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ssh_config: ssh_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#ssh_config ContainerAzureNodePool#ssh_config}
        :param labels: Optional. The initial labels assigned to nodes of this node pool. An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#labels ContainerAzureNodePool#labels}
        :param proxy_config: proxy_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#proxy_config ContainerAzureNodePool#proxy_config}
        :param root_volume: root_volume block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#root_volume ContainerAzureNodePool#root_volume}
        :param tags: Optional. A set of tags to apply to all underlying Azure resources for this node pool. This currently only includes Virtual Machine Scale Sets. Specify at most 50 pairs containing alphanumerics, spaces, and symbols (.+-=_:@/). Keys can be up to 127 Unicode characters. Values can be up to 255 Unicode characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#tags ContainerAzureNodePool#tags}
        :param vm_size: Optional. The Azure VM size name. Example: ``Standard_DS2_v2``. See (/anthos/clusters/docs/azure/reference/supported-vms) for options. When unspecified, it defaults to ``Standard_DS2_v2``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#vm_size ContainerAzureNodePool#vm_size}
        '''
        value = ContainerAzureNodePoolConfigA(
            ssh_config=ssh_config,
            labels=labels,
            proxy_config=proxy_config,
            root_volume=root_volume,
            tags=tags,
            vm_size=vm_size,
        )

        return typing.cast(None, jsii.invoke(self, "putConfig", [value]))

    @jsii.member(jsii_name="putManagement")
    def put_management(
        self,
        *,
        auto_repair: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param auto_repair: Optional. Whether or not the nodes will be automatically repaired. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#auto_repair ContainerAzureNodePool#auto_repair}
        '''
        value = ContainerAzureNodePoolManagement(auto_repair=auto_repair)

        return typing.cast(None, jsii.invoke(self, "putManagement", [value]))

    @jsii.member(jsii_name="putMaxPodsConstraint")
    def put_max_pods_constraint(self, *, max_pods_per_node: jsii.Number) -> None:
        '''
        :param max_pods_per_node: The maximum number of pods to schedule on a single node. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#max_pods_per_node ContainerAzureNodePool#max_pods_per_node}
        '''
        value = ContainerAzureNodePoolMaxPodsConstraint(
            max_pods_per_node=max_pods_per_node
        )

        return typing.cast(None, jsii.invoke(self, "putMaxPodsConstraint", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#create ContainerAzureNodePool#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#delete ContainerAzureNodePool#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#update ContainerAzureNodePool#update}.
        '''
        value = ContainerAzureNodePoolTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAnnotations")
    def reset_annotations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnnotations", []))

    @jsii.member(jsii_name="resetAzureAvailabilityZone")
    def reset_azure_availability_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAzureAvailabilityZone", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetManagement")
    def reset_management(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManagement", []))

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
    @jsii.member(jsii_name="autoscaling")
    def autoscaling(self) -> "ContainerAzureNodePoolAutoscalingOutputReference":
        return typing.cast("ContainerAzureNodePoolAutoscalingOutputReference", jsii.get(self, "autoscaling"))

    @builtins.property
    @jsii.member(jsii_name="config")
    def config(self) -> "ContainerAzureNodePoolConfigAOutputReference":
        return typing.cast("ContainerAzureNodePoolConfigAOutputReference", jsii.get(self, "config"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="effectiveAnnotations")
    def effective_annotations(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveAnnotations"))

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "etag"))

    @builtins.property
    @jsii.member(jsii_name="management")
    def management(self) -> "ContainerAzureNodePoolManagementOutputReference":
        return typing.cast("ContainerAzureNodePoolManagementOutputReference", jsii.get(self, "management"))

    @builtins.property
    @jsii.member(jsii_name="maxPodsConstraint")
    def max_pods_constraint(
        self,
    ) -> "ContainerAzureNodePoolMaxPodsConstraintOutputReference":
        return typing.cast("ContainerAzureNodePoolMaxPodsConstraintOutputReference", jsii.get(self, "maxPodsConstraint"))

    @builtins.property
    @jsii.member(jsii_name="reconciling")
    def reconciling(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "reconciling"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ContainerAzureNodePoolTimeoutsOutputReference":
        return typing.cast("ContainerAzureNodePoolTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    @jsii.member(jsii_name="autoscalingInput")
    def autoscaling_input(self) -> typing.Optional["ContainerAzureNodePoolAutoscaling"]:
        return typing.cast(typing.Optional["ContainerAzureNodePoolAutoscaling"], jsii.get(self, "autoscalingInput"))

    @builtins.property
    @jsii.member(jsii_name="azureAvailabilityZoneInput")
    def azure_availability_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "azureAvailabilityZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterInput")
    def cluster_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterInput"))

    @builtins.property
    @jsii.member(jsii_name="configInput")
    def config_input(self) -> typing.Optional["ContainerAzureNodePoolConfigA"]:
        return typing.cast(typing.Optional["ContainerAzureNodePoolConfigA"], jsii.get(self, "configInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="managementInput")
    def management_input(self) -> typing.Optional["ContainerAzureNodePoolManagement"]:
        return typing.cast(typing.Optional["ContainerAzureNodePoolManagement"], jsii.get(self, "managementInput"))

    @builtins.property
    @jsii.member(jsii_name="maxPodsConstraintInput")
    def max_pods_constraint_input(
        self,
    ) -> typing.Optional["ContainerAzureNodePoolMaxPodsConstraint"]:
        return typing.cast(typing.Optional["ContainerAzureNodePoolMaxPodsConstraint"], jsii.get(self, "maxPodsConstraintInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetIdInput")
    def subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ContainerAzureNodePoolTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ContainerAzureNodePoolTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="annotations")
    def annotations(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "annotations"))

    @annotations.setter
    def annotations(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bb306999e5a7d70aaa9d158593431cac3468c2cdc7c46a7e9befceae3c6be40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="azureAvailabilityZone")
    def azure_availability_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "azureAvailabilityZone"))

    @azure_availability_zone.setter
    def azure_availability_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1f1a96ee04b722e7c218335f52e2922da806721199dc3b52cb10416919b04fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "azureAvailabilityZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cluster"))

    @cluster.setter
    def cluster(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14f622c9cbf1241c9821bd908bbc78b24de8c3f02c3213f8ac260fc4caf7b487)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cluster", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97dff4656f23fc180dbde42b2921fd1c48984ca0a23fd811dc9a716667b461e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62499c142e149165eef90f190cce83777a15c473f38e360e61e3ea901626bb8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72d72b2f7e9d55693e05a5d14823bb472557d509ab331938ef7123f2aca06a0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7248ea40ee26aff4147d0fa5fa970470a029646fe9e5306655122e64bb2ffd22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74a5d8c7ced365272e5e1462c7766ba1da8c4841ce4b36c7af0dae314a3ba0e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1359d7d8b15b8ccc72aa074ac67438197449171f787340e2f086d93520aa4039)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAzureNodePool.ContainerAzureNodePoolAutoscaling",
    jsii_struct_bases=[],
    name_mapping={"max_node_count": "maxNodeCount", "min_node_count": "minNodeCount"},
)
class ContainerAzureNodePoolAutoscaling:
    def __init__(
        self,
        *,
        max_node_count: jsii.Number,
        min_node_count: jsii.Number,
    ) -> None:
        '''
        :param max_node_count: Maximum number of nodes in the node pool. Must be >= min_node_count. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#max_node_count ContainerAzureNodePool#max_node_count}
        :param min_node_count: Minimum number of nodes in the node pool. Must be >= 1 and <= max_node_count. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#min_node_count ContainerAzureNodePool#min_node_count}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7879b03a2f3c46f01e02a9cd2b722ac8c0cc75acf6906b17000e09388700d98d)
            check_type(argname="argument max_node_count", value=max_node_count, expected_type=type_hints["max_node_count"])
            check_type(argname="argument min_node_count", value=min_node_count, expected_type=type_hints["min_node_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "max_node_count": max_node_count,
            "min_node_count": min_node_count,
        }

    @builtins.property
    def max_node_count(self) -> jsii.Number:
        '''Maximum number of nodes in the node pool. Must be >= min_node_count.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#max_node_count ContainerAzureNodePool#max_node_count}
        '''
        result = self._values.get("max_node_count")
        assert result is not None, "Required property 'max_node_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def min_node_count(self) -> jsii.Number:
        '''Minimum number of nodes in the node pool. Must be >= 1 and <= max_node_count.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#min_node_count ContainerAzureNodePool#min_node_count}
        '''
        result = self._values.get("min_node_count")
        assert result is not None, "Required property 'min_node_count' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAzureNodePoolAutoscaling(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAzureNodePoolAutoscalingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAzureNodePool.ContainerAzureNodePoolAutoscalingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d089f004f3526db273162f4d9ea083ecbc569df39252b34329488a26d5fb8226)
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
    @jsii.member(jsii_name="maxNodeCount")
    def max_node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxNodeCount"))

    @max_node_count.setter
    def max_node_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a96726551fb1d02629296d15e824ec986e6853805635022328deddd0cedfbe69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxNodeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minNodeCount")
    def min_node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minNodeCount"))

    @min_node_count.setter
    def min_node_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2fa9086d31a931ca74954f799073d8ebb8ae0a6625837536423748f527ea392)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minNodeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ContainerAzureNodePoolAutoscaling]:
        return typing.cast(typing.Optional[ContainerAzureNodePoolAutoscaling], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerAzureNodePoolAutoscaling],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d4dd7e421fa84891d182ad2a387aa11c0cad3463a61b59234debe540742315e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAzureNodePool.ContainerAzureNodePoolConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "autoscaling": "autoscaling",
        "cluster": "cluster",
        "config": "config",
        "location": "location",
        "max_pods_constraint": "maxPodsConstraint",
        "name": "name",
        "subnet_id": "subnetId",
        "version": "version",
        "annotations": "annotations",
        "azure_availability_zone": "azureAvailabilityZone",
        "id": "id",
        "management": "management",
        "project": "project",
        "timeouts": "timeouts",
    },
)
class ContainerAzureNodePoolConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        autoscaling: typing.Union[ContainerAzureNodePoolAutoscaling, typing.Dict[builtins.str, typing.Any]],
        cluster: builtins.str,
        config: typing.Union["ContainerAzureNodePoolConfigA", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        max_pods_constraint: typing.Union["ContainerAzureNodePoolMaxPodsConstraint", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        subnet_id: builtins.str,
        version: builtins.str,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        azure_availability_zone: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        management: typing.Optional[typing.Union["ContainerAzureNodePoolManagement", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ContainerAzureNodePoolTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param autoscaling: autoscaling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#autoscaling ContainerAzureNodePool#autoscaling}
        :param cluster: The azureCluster for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#cluster ContainerAzureNodePool#cluster}
        :param config: config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#config ContainerAzureNodePool#config}
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#location ContainerAzureNodePool#location}
        :param max_pods_constraint: max_pods_constraint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#max_pods_constraint ContainerAzureNodePool#max_pods_constraint}
        :param name: The name of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#name ContainerAzureNodePool#name}
        :param subnet_id: The ARM ID of the subnet where the node pool VMs run. Make sure it's a subnet under the virtual network in the cluster configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#subnet_id ContainerAzureNodePool#subnet_id}
        :param version: The Kubernetes version (e.g. ``1.19.10-gke.1000``) running on this node pool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#version ContainerAzureNodePool#version}
        :param annotations: Optional. Annotations on the node pool. This field has the same restrictions as Kubernetes annotations. The total size of all keys and values combined is limited to 256k. Keys can have 2 segments: prefix (optional) and name (required), separated by a slash (/). Prefix must be a DNS subdomain. Name must be 63 characters or less, begin and end with alphanumerics, with dashes (-), underscores (_), dots (.), and alphanumerics between. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field ``effective_annotations`` for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#annotations ContainerAzureNodePool#annotations}
        :param azure_availability_zone: Optional. The Azure availability zone of the nodes in this nodepool. When unspecified, it defaults to ``1``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#azure_availability_zone ContainerAzureNodePool#azure_availability_zone}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#id ContainerAzureNodePool#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param management: management block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#management ContainerAzureNodePool#management}
        :param project: The project for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#project ContainerAzureNodePool#project}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#timeouts ContainerAzureNodePool#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(autoscaling, dict):
            autoscaling = ContainerAzureNodePoolAutoscaling(**autoscaling)
        if isinstance(config, dict):
            config = ContainerAzureNodePoolConfigA(**config)
        if isinstance(max_pods_constraint, dict):
            max_pods_constraint = ContainerAzureNodePoolMaxPodsConstraint(**max_pods_constraint)
        if isinstance(management, dict):
            management = ContainerAzureNodePoolManagement(**management)
        if isinstance(timeouts, dict):
            timeouts = ContainerAzureNodePoolTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9364503b2cd5beb72759adbe83e711515d7060f5470d5744988feb6669cce05)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument autoscaling", value=autoscaling, expected_type=type_hints["autoscaling"])
            check_type(argname="argument cluster", value=cluster, expected_type=type_hints["cluster"])
            check_type(argname="argument config", value=config, expected_type=type_hints["config"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument max_pods_constraint", value=max_pods_constraint, expected_type=type_hints["max_pods_constraint"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument annotations", value=annotations, expected_type=type_hints["annotations"])
            check_type(argname="argument azure_availability_zone", value=azure_availability_zone, expected_type=type_hints["azure_availability_zone"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument management", value=management, expected_type=type_hints["management"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "autoscaling": autoscaling,
            "cluster": cluster,
            "config": config,
            "location": location,
            "max_pods_constraint": max_pods_constraint,
            "name": name,
            "subnet_id": subnet_id,
            "version": version,
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
        if azure_availability_zone is not None:
            self._values["azure_availability_zone"] = azure_availability_zone
        if id is not None:
            self._values["id"] = id
        if management is not None:
            self._values["management"] = management
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
    def autoscaling(self) -> ContainerAzureNodePoolAutoscaling:
        '''autoscaling block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#autoscaling ContainerAzureNodePool#autoscaling}
        '''
        result = self._values.get("autoscaling")
        assert result is not None, "Required property 'autoscaling' is missing"
        return typing.cast(ContainerAzureNodePoolAutoscaling, result)

    @builtins.property
    def cluster(self) -> builtins.str:
        '''The azureCluster for the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#cluster ContainerAzureNodePool#cluster}
        '''
        result = self._values.get("cluster")
        assert result is not None, "Required property 'cluster' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def config(self) -> "ContainerAzureNodePoolConfigA":
        '''config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#config ContainerAzureNodePool#config}
        '''
        result = self._values.get("config")
        assert result is not None, "Required property 'config' is missing"
        return typing.cast("ContainerAzureNodePoolConfigA", result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location for the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#location ContainerAzureNodePool#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def max_pods_constraint(self) -> "ContainerAzureNodePoolMaxPodsConstraint":
        '''max_pods_constraint block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#max_pods_constraint ContainerAzureNodePool#max_pods_constraint}
        '''
        result = self._values.get("max_pods_constraint")
        assert result is not None, "Required property 'max_pods_constraint' is missing"
        return typing.cast("ContainerAzureNodePoolMaxPodsConstraint", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#name ContainerAzureNodePool#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subnet_id(self) -> builtins.str:
        '''The ARM ID of the subnet where the node pool VMs run.

        Make sure it's a subnet under the virtual network in the cluster configuration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#subnet_id ContainerAzureNodePool#subnet_id}
        '''
        result = self._values.get("subnet_id")
        assert result is not None, "Required property 'subnet_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version(self) -> builtins.str:
        '''The Kubernetes version (e.g. ``1.19.10-gke.1000``) running on this node pool.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#version ContainerAzureNodePool#version}
        '''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def annotations(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional.

        Annotations on the node pool. This field has the same restrictions as Kubernetes annotations. The total size of all keys and values combined is limited to 256k. Keys can have 2 segments: prefix (optional) and name (required), separated by a slash (/). Prefix must be a DNS subdomain. Name must be 63 characters or less, begin and end with alphanumerics, with dashes (-), underscores (_), dots (.), and alphanumerics between.

        **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration.
        Please refer to the field ``effective_annotations`` for all of the annotations present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#annotations ContainerAzureNodePool#annotations}
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def azure_availability_zone(self) -> typing.Optional[builtins.str]:
        '''Optional. The Azure availability zone of the nodes in this nodepool. When unspecified, it defaults to ``1``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#azure_availability_zone ContainerAzureNodePool#azure_availability_zone}
        '''
        result = self._values.get("azure_availability_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#id ContainerAzureNodePool#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def management(self) -> typing.Optional["ContainerAzureNodePoolManagement"]:
        '''management block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#management ContainerAzureNodePool#management}
        '''
        result = self._values.get("management")
        return typing.cast(typing.Optional["ContainerAzureNodePoolManagement"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''The project for the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#project ContainerAzureNodePool#project}
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ContainerAzureNodePoolTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#timeouts ContainerAzureNodePool#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ContainerAzureNodePoolTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAzureNodePoolConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAzureNodePool.ContainerAzureNodePoolConfigA",
    jsii_struct_bases=[],
    name_mapping={
        "ssh_config": "sshConfig",
        "labels": "labels",
        "proxy_config": "proxyConfig",
        "root_volume": "rootVolume",
        "tags": "tags",
        "vm_size": "vmSize",
    },
)
class ContainerAzureNodePoolConfigA:
    def __init__(
        self,
        *,
        ssh_config: typing.Union["ContainerAzureNodePoolConfigSshConfig", typing.Dict[builtins.str, typing.Any]],
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        proxy_config: typing.Optional[typing.Union["ContainerAzureNodePoolConfigProxyConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        root_volume: typing.Optional[typing.Union["ContainerAzureNodePoolConfigRootVolume", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        vm_size: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ssh_config: ssh_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#ssh_config ContainerAzureNodePool#ssh_config}
        :param labels: Optional. The initial labels assigned to nodes of this node pool. An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#labels ContainerAzureNodePool#labels}
        :param proxy_config: proxy_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#proxy_config ContainerAzureNodePool#proxy_config}
        :param root_volume: root_volume block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#root_volume ContainerAzureNodePool#root_volume}
        :param tags: Optional. A set of tags to apply to all underlying Azure resources for this node pool. This currently only includes Virtual Machine Scale Sets. Specify at most 50 pairs containing alphanumerics, spaces, and symbols (.+-=_:@/). Keys can be up to 127 Unicode characters. Values can be up to 255 Unicode characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#tags ContainerAzureNodePool#tags}
        :param vm_size: Optional. The Azure VM size name. Example: ``Standard_DS2_v2``. See (/anthos/clusters/docs/azure/reference/supported-vms) for options. When unspecified, it defaults to ``Standard_DS2_v2``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#vm_size ContainerAzureNodePool#vm_size}
        '''
        if isinstance(ssh_config, dict):
            ssh_config = ContainerAzureNodePoolConfigSshConfig(**ssh_config)
        if isinstance(proxy_config, dict):
            proxy_config = ContainerAzureNodePoolConfigProxyConfig(**proxy_config)
        if isinstance(root_volume, dict):
            root_volume = ContainerAzureNodePoolConfigRootVolume(**root_volume)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4c13a268ba1b2fda7919ee7fb079ebddb7f9215ce6759a3420ee22e6e4cc030)
            check_type(argname="argument ssh_config", value=ssh_config, expected_type=type_hints["ssh_config"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument proxy_config", value=proxy_config, expected_type=type_hints["proxy_config"])
            check_type(argname="argument root_volume", value=root_volume, expected_type=type_hints["root_volume"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument vm_size", value=vm_size, expected_type=type_hints["vm_size"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ssh_config": ssh_config,
        }
        if labels is not None:
            self._values["labels"] = labels
        if proxy_config is not None:
            self._values["proxy_config"] = proxy_config
        if root_volume is not None:
            self._values["root_volume"] = root_volume
        if tags is not None:
            self._values["tags"] = tags
        if vm_size is not None:
            self._values["vm_size"] = vm_size

    @builtins.property
    def ssh_config(self) -> "ContainerAzureNodePoolConfigSshConfig":
        '''ssh_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#ssh_config ContainerAzureNodePool#ssh_config}
        '''
        result = self._values.get("ssh_config")
        assert result is not None, "Required property 'ssh_config' is missing"
        return typing.cast("ContainerAzureNodePoolConfigSshConfig", result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional.

        The initial labels assigned to nodes of this node pool. An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#labels ContainerAzureNodePool#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def proxy_config(
        self,
    ) -> typing.Optional["ContainerAzureNodePoolConfigProxyConfig"]:
        '''proxy_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#proxy_config ContainerAzureNodePool#proxy_config}
        '''
        result = self._values.get("proxy_config")
        return typing.cast(typing.Optional["ContainerAzureNodePoolConfigProxyConfig"], result)

    @builtins.property
    def root_volume(self) -> typing.Optional["ContainerAzureNodePoolConfigRootVolume"]:
        '''root_volume block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#root_volume ContainerAzureNodePool#root_volume}
        '''
        result = self._values.get("root_volume")
        return typing.cast(typing.Optional["ContainerAzureNodePoolConfigRootVolume"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional.

        A set of tags to apply to all underlying Azure resources for this node pool. This currently only includes Virtual Machine Scale Sets. Specify at most 50 pairs containing alphanumerics, spaces, and symbols (.+-=_:@/). Keys can be up to 127 Unicode characters. Values can be up to 255 Unicode characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#tags ContainerAzureNodePool#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def vm_size(self) -> typing.Optional[builtins.str]:
        '''Optional. The Azure VM size name. Example: ``Standard_DS2_v2``. See (/anthos/clusters/docs/azure/reference/supported-vms) for options. When unspecified, it defaults to ``Standard_DS2_v2``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#vm_size ContainerAzureNodePool#vm_size}
        '''
        result = self._values.get("vm_size")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAzureNodePoolConfigA(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAzureNodePoolConfigAOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAzureNodePool.ContainerAzureNodePoolConfigAOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__067d5ea3d43274ee0ae12270e0e4c0fdca2220f2030b60a3983aee6800038823)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putProxyConfig")
    def put_proxy_config(
        self,
        *,
        resource_group_id: builtins.str,
        secret_id: builtins.str,
    ) -> None:
        '''
        :param resource_group_id: The ARM ID the of the resource group containing proxy keyvault. Resource group ids are formatted as ``/subscriptions/<subscription-id>/resourceGroups/<resource-group-name>``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#resource_group_id ContainerAzureNodePool#resource_group_id}
        :param secret_id: The URL the of the proxy setting secret with its version. Secret ids are formatted as ``https:<key-vault-name>.vault.azure.net/secrets/<secret-name>/<secret-version>``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#secret_id ContainerAzureNodePool#secret_id}
        '''
        value = ContainerAzureNodePoolConfigProxyConfig(
            resource_group_id=resource_group_id, secret_id=secret_id
        )

        return typing.cast(None, jsii.invoke(self, "putProxyConfig", [value]))

    @jsii.member(jsii_name="putRootVolume")
    def put_root_volume(self, *, size_gib: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param size_gib: Optional. The size of the disk, in GiBs. When unspecified, a default value is provided. See the specific reference in the parent resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#size_gib ContainerAzureNodePool#size_gib}
        '''
        value = ContainerAzureNodePoolConfigRootVolume(size_gib=size_gib)

        return typing.cast(None, jsii.invoke(self, "putRootVolume", [value]))

    @jsii.member(jsii_name="putSshConfig")
    def put_ssh_config(self, *, authorized_key: builtins.str) -> None:
        '''
        :param authorized_key: The SSH public key data for VMs managed by Anthos. This accepts the authorized_keys file format used in OpenSSH according to the sshd(8) manual page. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#authorized_key ContainerAzureNodePool#authorized_key}
        '''
        value = ContainerAzureNodePoolConfigSshConfig(authorized_key=authorized_key)

        return typing.cast(None, jsii.invoke(self, "putSshConfig", [value]))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetProxyConfig")
    def reset_proxy_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProxyConfig", []))

    @jsii.member(jsii_name="resetRootVolume")
    def reset_root_volume(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRootVolume", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetVmSize")
    def reset_vm_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVmSize", []))

    @builtins.property
    @jsii.member(jsii_name="proxyConfig")
    def proxy_config(self) -> "ContainerAzureNodePoolConfigProxyConfigOutputReference":
        return typing.cast("ContainerAzureNodePoolConfigProxyConfigOutputReference", jsii.get(self, "proxyConfig"))

    @builtins.property
    @jsii.member(jsii_name="rootVolume")
    def root_volume(self) -> "ContainerAzureNodePoolConfigRootVolumeOutputReference":
        return typing.cast("ContainerAzureNodePoolConfigRootVolumeOutputReference", jsii.get(self, "rootVolume"))

    @builtins.property
    @jsii.member(jsii_name="sshConfig")
    def ssh_config(self) -> "ContainerAzureNodePoolConfigSshConfigOutputReference":
        return typing.cast("ContainerAzureNodePoolConfigSshConfigOutputReference", jsii.get(self, "sshConfig"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="proxyConfigInput")
    def proxy_config_input(
        self,
    ) -> typing.Optional["ContainerAzureNodePoolConfigProxyConfig"]:
        return typing.cast(typing.Optional["ContainerAzureNodePoolConfigProxyConfig"], jsii.get(self, "proxyConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="rootVolumeInput")
    def root_volume_input(
        self,
    ) -> typing.Optional["ContainerAzureNodePoolConfigRootVolume"]:
        return typing.cast(typing.Optional["ContainerAzureNodePoolConfigRootVolume"], jsii.get(self, "rootVolumeInput"))

    @builtins.property
    @jsii.member(jsii_name="sshConfigInput")
    def ssh_config_input(
        self,
    ) -> typing.Optional["ContainerAzureNodePoolConfigSshConfig"]:
        return typing.cast(typing.Optional["ContainerAzureNodePoolConfigSshConfig"], jsii.get(self, "sshConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="vmSizeInput")
    def vm_size_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vmSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54605e476b214a0929b187a6468b93e85784fe82e5555ea7abe8956a5af2132f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c87d9ca2a20db1d0fa235856dd31090bcd914e5ee88f24b483f6195d14430865)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vmSize")
    def vm_size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vmSize"))

    @vm_size.setter
    def vm_size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3c3fd3ccde5966bad0cbd084c83d3baa31cf2203370101b90ea94c3c7a1c47b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vmSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ContainerAzureNodePoolConfigA]:
        return typing.cast(typing.Optional[ContainerAzureNodePoolConfigA], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerAzureNodePoolConfigA],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd86c03978a6d2b9b6593c507f84cced6850802d15a0d37bffec90bce9e5232b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAzureNodePool.ContainerAzureNodePoolConfigProxyConfig",
    jsii_struct_bases=[],
    name_mapping={"resource_group_id": "resourceGroupId", "secret_id": "secretId"},
)
class ContainerAzureNodePoolConfigProxyConfig:
    def __init__(
        self,
        *,
        resource_group_id: builtins.str,
        secret_id: builtins.str,
    ) -> None:
        '''
        :param resource_group_id: The ARM ID the of the resource group containing proxy keyvault. Resource group ids are formatted as ``/subscriptions/<subscription-id>/resourceGroups/<resource-group-name>``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#resource_group_id ContainerAzureNodePool#resource_group_id}
        :param secret_id: The URL the of the proxy setting secret with its version. Secret ids are formatted as ``https:<key-vault-name>.vault.azure.net/secrets/<secret-name>/<secret-version>``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#secret_id ContainerAzureNodePool#secret_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b6dfd8333b72ab1cedeb9495423951b66456b257e4a3c75f708ce0284405e42)
            check_type(argname="argument resource_group_id", value=resource_group_id, expected_type=type_hints["resource_group_id"])
            check_type(argname="argument secret_id", value=secret_id, expected_type=type_hints["secret_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "resource_group_id": resource_group_id,
            "secret_id": secret_id,
        }

    @builtins.property
    def resource_group_id(self) -> builtins.str:
        '''The ARM ID the of the resource group containing proxy keyvault. Resource group ids are formatted as ``/subscriptions/<subscription-id>/resourceGroups/<resource-group-name>``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#resource_group_id ContainerAzureNodePool#resource_group_id}
        '''
        result = self._values.get("resource_group_id")
        assert result is not None, "Required property 'resource_group_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secret_id(self) -> builtins.str:
        '''The URL the of the proxy setting secret with its version. Secret ids are formatted as ``https:<key-vault-name>.vault.azure.net/secrets/<secret-name>/<secret-version>``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#secret_id ContainerAzureNodePool#secret_id}
        '''
        result = self._values.get("secret_id")
        assert result is not None, "Required property 'secret_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAzureNodePoolConfigProxyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAzureNodePoolConfigProxyConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAzureNodePool.ContainerAzureNodePoolConfigProxyConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a3fe50eb9498a037d73fc0e0492d22bfcaa20154141211bf972e65758efddf2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="resourceGroupIdInput")
    def resource_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="secretIdInput")
    def secret_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretIdInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupId")
    def resource_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupId"))

    @resource_group_id.setter
    def resource_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e48fdfc0f97217ad4d84524f538d06ba0f9ea24e034ee73a01d3da7fff82da2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretId")
    def secret_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretId"))

    @secret_id.setter
    def secret_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1377216e821066a8d185a59fdcbecd0fa151f3a80ebe5619cbc6073e42cc5269)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ContainerAzureNodePoolConfigProxyConfig]:
        return typing.cast(typing.Optional[ContainerAzureNodePoolConfigProxyConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerAzureNodePoolConfigProxyConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5136c51cb15d3ffc822f6018b65ce986b4e9bdf4845b9a984037f4d2b333b46f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAzureNodePool.ContainerAzureNodePoolConfigRootVolume",
    jsii_struct_bases=[],
    name_mapping={"size_gib": "sizeGib"},
)
class ContainerAzureNodePoolConfigRootVolume:
    def __init__(self, *, size_gib: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param size_gib: Optional. The size of the disk, in GiBs. When unspecified, a default value is provided. See the specific reference in the parent resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#size_gib ContainerAzureNodePool#size_gib}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ead60016868f32e6b4fbf72a0d4696646a5664e6dcf46a79c9d01446d277015c)
            check_type(argname="argument size_gib", value=size_gib, expected_type=type_hints["size_gib"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if size_gib is not None:
            self._values["size_gib"] = size_gib

    @builtins.property
    def size_gib(self) -> typing.Optional[jsii.Number]:
        '''Optional.

        The size of the disk, in GiBs. When unspecified, a default value is provided. See the specific reference in the parent resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#size_gib ContainerAzureNodePool#size_gib}
        '''
        result = self._values.get("size_gib")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAzureNodePoolConfigRootVolume(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAzureNodePoolConfigRootVolumeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAzureNodePool.ContainerAzureNodePoolConfigRootVolumeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5be6fd34e5bf7d9d2bc0d5b4eacd7c0e86ea9568bb355cf7c9704c32c02e863f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetSizeGib")
    def reset_size_gib(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSizeGib", []))

    @builtins.property
    @jsii.member(jsii_name="sizeGibInput")
    def size_gib_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sizeGibInput"))

    @builtins.property
    @jsii.member(jsii_name="sizeGib")
    def size_gib(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sizeGib"))

    @size_gib.setter
    def size_gib(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c86813973abf504285f6ca341139afbfdb5a89b564d671fde04203741839304a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sizeGib", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ContainerAzureNodePoolConfigRootVolume]:
        return typing.cast(typing.Optional[ContainerAzureNodePoolConfigRootVolume], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerAzureNodePoolConfigRootVolume],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__930daf97a7062c0ab1c94588a2bb684a862f4aab1eec045dc692fcf3e621509c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAzureNodePool.ContainerAzureNodePoolConfigSshConfig",
    jsii_struct_bases=[],
    name_mapping={"authorized_key": "authorizedKey"},
)
class ContainerAzureNodePoolConfigSshConfig:
    def __init__(self, *, authorized_key: builtins.str) -> None:
        '''
        :param authorized_key: The SSH public key data for VMs managed by Anthos. This accepts the authorized_keys file format used in OpenSSH according to the sshd(8) manual page. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#authorized_key ContainerAzureNodePool#authorized_key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eab52340903888026c004283949ea0755bb4aa786bec8712e3bf794e6111e59b)
            check_type(argname="argument authorized_key", value=authorized_key, expected_type=type_hints["authorized_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "authorized_key": authorized_key,
        }

    @builtins.property
    def authorized_key(self) -> builtins.str:
        '''The SSH public key data for VMs managed by Anthos.

        This accepts the authorized_keys file format used in OpenSSH according to the sshd(8) manual page.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#authorized_key ContainerAzureNodePool#authorized_key}
        '''
        result = self._values.get("authorized_key")
        assert result is not None, "Required property 'authorized_key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAzureNodePoolConfigSshConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAzureNodePoolConfigSshConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAzureNodePool.ContainerAzureNodePoolConfigSshConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3db9094d8878e0bfd7a0dd19fc45a2fef058c5de7d879197c088470f2da70ac6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="authorizedKeyInput")
    def authorized_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authorizedKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="authorizedKey")
    def authorized_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authorizedKey"))

    @authorized_key.setter
    def authorized_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cafe75f2f60e2ac3e7b002c35a9cf4ddd204209f681e163e14ed8df8f11bd9e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authorizedKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ContainerAzureNodePoolConfigSshConfig]:
        return typing.cast(typing.Optional[ContainerAzureNodePoolConfigSshConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerAzureNodePoolConfigSshConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e7f9427313f020b7574a8855b17d38f0f5624f550d77ea7e85245e7a0f93c34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAzureNodePool.ContainerAzureNodePoolManagement",
    jsii_struct_bases=[],
    name_mapping={"auto_repair": "autoRepair"},
)
class ContainerAzureNodePoolManagement:
    def __init__(
        self,
        *,
        auto_repair: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param auto_repair: Optional. Whether or not the nodes will be automatically repaired. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#auto_repair ContainerAzureNodePool#auto_repair}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d14b07e6f43ed4270e55fa9da53ba02f2c184341408a94a2526f2c8265932947)
            check_type(argname="argument auto_repair", value=auto_repair, expected_type=type_hints["auto_repair"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auto_repair is not None:
            self._values["auto_repair"] = auto_repair

    @builtins.property
    def auto_repair(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional. Whether or not the nodes will be automatically repaired.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#auto_repair ContainerAzureNodePool#auto_repair}
        '''
        result = self._values.get("auto_repair")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAzureNodePoolManagement(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAzureNodePoolManagementOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAzureNodePool.ContainerAzureNodePoolManagementOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e0a39bc81b0b7fbbb0cb591753af44f271253ef462668599297ca3f6da767b7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAutoRepair")
    def reset_auto_repair(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoRepair", []))

    @builtins.property
    @jsii.member(jsii_name="autoRepairInput")
    def auto_repair_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "autoRepairInput"))

    @builtins.property
    @jsii.member(jsii_name="autoRepair")
    def auto_repair(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "autoRepair"))

    @auto_repair.setter
    def auto_repair(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37721e347828a5b2d7b9f58a804116069b71ec9bea181313cba4548e4bf154cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoRepair", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ContainerAzureNodePoolManagement]:
        return typing.cast(typing.Optional[ContainerAzureNodePoolManagement], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerAzureNodePoolManagement],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d69618bc468278ae560d5434aa150dc7dec0f864f7aaee774f5b5df929dc9a56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAzureNodePool.ContainerAzureNodePoolMaxPodsConstraint",
    jsii_struct_bases=[],
    name_mapping={"max_pods_per_node": "maxPodsPerNode"},
)
class ContainerAzureNodePoolMaxPodsConstraint:
    def __init__(self, *, max_pods_per_node: jsii.Number) -> None:
        '''
        :param max_pods_per_node: The maximum number of pods to schedule on a single node. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#max_pods_per_node ContainerAzureNodePool#max_pods_per_node}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59c160ae8c4845e504ec11f0fdbeacf01ea42bb0a097e4a1988826d93bf5e385)
            check_type(argname="argument max_pods_per_node", value=max_pods_per_node, expected_type=type_hints["max_pods_per_node"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "max_pods_per_node": max_pods_per_node,
        }

    @builtins.property
    def max_pods_per_node(self) -> jsii.Number:
        '''The maximum number of pods to schedule on a single node.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#max_pods_per_node ContainerAzureNodePool#max_pods_per_node}
        '''
        result = self._values.get("max_pods_per_node")
        assert result is not None, "Required property 'max_pods_per_node' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAzureNodePoolMaxPodsConstraint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAzureNodePoolMaxPodsConstraintOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAzureNodePool.ContainerAzureNodePoolMaxPodsConstraintOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__642f80e9c4971446bb3d9a3664d07aa7b35fea5af82721a49f5f12eb2a8d0844)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="maxPodsPerNodeInput")
    def max_pods_per_node_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxPodsPerNodeInput"))

    @builtins.property
    @jsii.member(jsii_name="maxPodsPerNode")
    def max_pods_per_node(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxPodsPerNode"))

    @max_pods_per_node.setter
    def max_pods_per_node(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bad1f7a4bcad8d866086c3035bd568f267d8ee0b6f3a5cc350cf39dd1d44b074)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxPodsPerNode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ContainerAzureNodePoolMaxPodsConstraint]:
        return typing.cast(typing.Optional[ContainerAzureNodePoolMaxPodsConstraint], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerAzureNodePoolMaxPodsConstraint],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2839dc3e776c0bf7a1459d75d7a8666353decbf27514934a946a9995d23ac808)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAzureNodePool.ContainerAzureNodePoolTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ContainerAzureNodePoolTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#create ContainerAzureNodePool#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#delete ContainerAzureNodePool#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#update ContainerAzureNodePool#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2fccc04a5efa699e7b515f11b10c360783680c81afa191d5d4d122a5195fbbc)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#create ContainerAzureNodePool#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#delete ContainerAzureNodePool#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_node_pool#update ContainerAzureNodePool#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAzureNodePoolTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAzureNodePoolTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAzureNodePool.ContainerAzureNodePoolTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c35347d5da17b06a745dabf16e8695b172cd329e12a4136fed31d5e15e9ba62b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b89ee4494f9322469c286184e925fbc035cb73c79ba02eb3bef66dbe2b4fd76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcd4a8bf68ced15f86af494e7e31850b64e69d212da52642ec410ec1d6981df7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a022bbadffb4823d9189264224dda276aa22fc396b532823d7bdbea1a6d88695)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAzureNodePoolTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAzureNodePoolTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAzureNodePoolTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8008a3c39c3d322e182794db73a127e1e404a51d0b7a29b8091dadffc26f6509)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ContainerAzureNodePool",
    "ContainerAzureNodePoolAutoscaling",
    "ContainerAzureNodePoolAutoscalingOutputReference",
    "ContainerAzureNodePoolConfig",
    "ContainerAzureNodePoolConfigA",
    "ContainerAzureNodePoolConfigAOutputReference",
    "ContainerAzureNodePoolConfigProxyConfig",
    "ContainerAzureNodePoolConfigProxyConfigOutputReference",
    "ContainerAzureNodePoolConfigRootVolume",
    "ContainerAzureNodePoolConfigRootVolumeOutputReference",
    "ContainerAzureNodePoolConfigSshConfig",
    "ContainerAzureNodePoolConfigSshConfigOutputReference",
    "ContainerAzureNodePoolManagement",
    "ContainerAzureNodePoolManagementOutputReference",
    "ContainerAzureNodePoolMaxPodsConstraint",
    "ContainerAzureNodePoolMaxPodsConstraintOutputReference",
    "ContainerAzureNodePoolTimeouts",
    "ContainerAzureNodePoolTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__7d4055f2e298ce2d0f1f221695aebdbcbff0bb1f68e3d2d3c579847162ad00d3(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    autoscaling: typing.Union[ContainerAzureNodePoolAutoscaling, typing.Dict[builtins.str, typing.Any]],
    cluster: builtins.str,
    config: typing.Union[ContainerAzureNodePoolConfigA, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    max_pods_constraint: typing.Union[ContainerAzureNodePoolMaxPodsConstraint, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    subnet_id: builtins.str,
    version: builtins.str,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    azure_availability_zone: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    management: typing.Optional[typing.Union[ContainerAzureNodePoolManagement, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ContainerAzureNodePoolTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__407a00f41f50ed5506105df5e5975abb94b53da8dafd80ce6f67358a2f3382b0(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bb306999e5a7d70aaa9d158593431cac3468c2cdc7c46a7e9befceae3c6be40(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1f1a96ee04b722e7c218335f52e2922da806721199dc3b52cb10416919b04fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14f622c9cbf1241c9821bd908bbc78b24de8c3f02c3213f8ac260fc4caf7b487(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97dff4656f23fc180dbde42b2921fd1c48984ca0a23fd811dc9a716667b461e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62499c142e149165eef90f190cce83777a15c473f38e360e61e3ea901626bb8e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72d72b2f7e9d55693e05a5d14823bb472557d509ab331938ef7123f2aca06a0e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7248ea40ee26aff4147d0fa5fa970470a029646fe9e5306655122e64bb2ffd22(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74a5d8c7ced365272e5e1462c7766ba1da8c4841ce4b36c7af0dae314a3ba0e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1359d7d8b15b8ccc72aa074ac67438197449171f787340e2f086d93520aa4039(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7879b03a2f3c46f01e02a9cd2b722ac8c0cc75acf6906b17000e09388700d98d(
    *,
    max_node_count: jsii.Number,
    min_node_count: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d089f004f3526db273162f4d9ea083ecbc569df39252b34329488a26d5fb8226(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a96726551fb1d02629296d15e824ec986e6853805635022328deddd0cedfbe69(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2fa9086d31a931ca74954f799073d8ebb8ae0a6625837536423748f527ea392(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d4dd7e421fa84891d182ad2a387aa11c0cad3463a61b59234debe540742315e(
    value: typing.Optional[ContainerAzureNodePoolAutoscaling],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9364503b2cd5beb72759adbe83e711515d7060f5470d5744988feb6669cce05(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    autoscaling: typing.Union[ContainerAzureNodePoolAutoscaling, typing.Dict[builtins.str, typing.Any]],
    cluster: builtins.str,
    config: typing.Union[ContainerAzureNodePoolConfigA, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    max_pods_constraint: typing.Union[ContainerAzureNodePoolMaxPodsConstraint, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    subnet_id: builtins.str,
    version: builtins.str,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    azure_availability_zone: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    management: typing.Optional[typing.Union[ContainerAzureNodePoolManagement, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ContainerAzureNodePoolTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4c13a268ba1b2fda7919ee7fb079ebddb7f9215ce6759a3420ee22e6e4cc030(
    *,
    ssh_config: typing.Union[ContainerAzureNodePoolConfigSshConfig, typing.Dict[builtins.str, typing.Any]],
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    proxy_config: typing.Optional[typing.Union[ContainerAzureNodePoolConfigProxyConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    root_volume: typing.Optional[typing.Union[ContainerAzureNodePoolConfigRootVolume, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    vm_size: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__067d5ea3d43274ee0ae12270e0e4c0fdca2220f2030b60a3983aee6800038823(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54605e476b214a0929b187a6468b93e85784fe82e5555ea7abe8956a5af2132f(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c87d9ca2a20db1d0fa235856dd31090bcd914e5ee88f24b483f6195d14430865(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3c3fd3ccde5966bad0cbd084c83d3baa31cf2203370101b90ea94c3c7a1c47b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd86c03978a6d2b9b6593c507f84cced6850802d15a0d37bffec90bce9e5232b(
    value: typing.Optional[ContainerAzureNodePoolConfigA],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b6dfd8333b72ab1cedeb9495423951b66456b257e4a3c75f708ce0284405e42(
    *,
    resource_group_id: builtins.str,
    secret_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a3fe50eb9498a037d73fc0e0492d22bfcaa20154141211bf972e65758efddf2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e48fdfc0f97217ad4d84524f538d06ba0f9ea24e034ee73a01d3da7fff82da2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1377216e821066a8d185a59fdcbecd0fa151f3a80ebe5619cbc6073e42cc5269(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5136c51cb15d3ffc822f6018b65ce986b4e9bdf4845b9a984037f4d2b333b46f(
    value: typing.Optional[ContainerAzureNodePoolConfigProxyConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ead60016868f32e6b4fbf72a0d4696646a5664e6dcf46a79c9d01446d277015c(
    *,
    size_gib: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5be6fd34e5bf7d9d2bc0d5b4eacd7c0e86ea9568bb355cf7c9704c32c02e863f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c86813973abf504285f6ca341139afbfdb5a89b564d671fde04203741839304a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__930daf97a7062c0ab1c94588a2bb684a862f4aab1eec045dc692fcf3e621509c(
    value: typing.Optional[ContainerAzureNodePoolConfigRootVolume],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eab52340903888026c004283949ea0755bb4aa786bec8712e3bf794e6111e59b(
    *,
    authorized_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3db9094d8878e0bfd7a0dd19fc45a2fef058c5de7d879197c088470f2da70ac6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cafe75f2f60e2ac3e7b002c35a9cf4ddd204209f681e163e14ed8df8f11bd9e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e7f9427313f020b7574a8855b17d38f0f5624f550d77ea7e85245e7a0f93c34(
    value: typing.Optional[ContainerAzureNodePoolConfigSshConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d14b07e6f43ed4270e55fa9da53ba02f2c184341408a94a2526f2c8265932947(
    *,
    auto_repair: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e0a39bc81b0b7fbbb0cb591753af44f271253ef462668599297ca3f6da767b7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37721e347828a5b2d7b9f58a804116069b71ec9bea181313cba4548e4bf154cd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d69618bc468278ae560d5434aa150dc7dec0f864f7aaee774f5b5df929dc9a56(
    value: typing.Optional[ContainerAzureNodePoolManagement],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59c160ae8c4845e504ec11f0fdbeacf01ea42bb0a097e4a1988826d93bf5e385(
    *,
    max_pods_per_node: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__642f80e9c4971446bb3d9a3664d07aa7b35fea5af82721a49f5f12eb2a8d0844(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bad1f7a4bcad8d866086c3035bd568f267d8ee0b6f3a5cc350cf39dd1d44b074(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2839dc3e776c0bf7a1459d75d7a8666353decbf27514934a946a9995d23ac808(
    value: typing.Optional[ContainerAzureNodePoolMaxPodsConstraint],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2fccc04a5efa699e7b515f11b10c360783680c81afa191d5d4d122a5195fbbc(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c35347d5da17b06a745dabf16e8695b172cd329e12a4136fed31d5e15e9ba62b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b89ee4494f9322469c286184e925fbc035cb73c79ba02eb3bef66dbe2b4fd76(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcd4a8bf68ced15f86af494e7e31850b64e69d212da52642ec410ec1d6981df7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a022bbadffb4823d9189264224dda276aa22fc396b532823d7bdbea1a6d88695(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8008a3c39c3d322e182794db73a127e1e404a51d0b7a29b8091dadffc26f6509(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAzureNodePoolTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
