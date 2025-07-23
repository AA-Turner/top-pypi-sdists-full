r'''
# `google_container_aws_node_pool`

Refer to the Terraform Registry for docs: [`google_container_aws_node_pool`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool).
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


class ContainerAwsNodePool(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAwsNodePool.ContainerAwsNodePool",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool google_container_aws_node_pool}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        autoscaling: typing.Union["ContainerAwsNodePoolAutoscaling", typing.Dict[builtins.str, typing.Any]],
        cluster: builtins.str,
        config: typing.Union["ContainerAwsNodePoolConfigA", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        max_pods_constraint: typing.Union["ContainerAwsNodePoolMaxPodsConstraint", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        subnet_id: builtins.str,
        version: builtins.str,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        kubelet_config: typing.Optional[typing.Union["ContainerAwsNodePoolKubeletConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        management: typing.Optional[typing.Union["ContainerAwsNodePoolManagement", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ContainerAwsNodePoolTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        update_settings: typing.Optional[typing.Union["ContainerAwsNodePoolUpdateSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool google_container_aws_node_pool} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param autoscaling: autoscaling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#autoscaling ContainerAwsNodePool#autoscaling}
        :param cluster: The awsCluster for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#cluster ContainerAwsNodePool#cluster}
        :param config: config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#config ContainerAwsNodePool#config}
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#location ContainerAwsNodePool#location}
        :param max_pods_constraint: max_pods_constraint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#max_pods_constraint ContainerAwsNodePool#max_pods_constraint}
        :param name: The name of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#name ContainerAwsNodePool#name}
        :param subnet_id: The subnet where the node pool node run. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#subnet_id ContainerAwsNodePool#subnet_id}
        :param version: The Kubernetes version to run on this node pool (e.g. ``1.19.10-gke.1000``). You can list all supported versions on a given Google Cloud region by calling GetAwsServerConfig. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#version ContainerAwsNodePool#version}
        :param annotations: Optional. Annotations on the node pool. This field has the same restrictions as Kubernetes annotations. The total size of all keys and values combined is limited to 256k. Key can have 2 segments: prefix (optional) and name (required), separated by a slash (/). Prefix must be a DNS subdomain. Name must be 63 characters or less, begin and end with alphanumerics, with dashes (-), underscores (_), dots (.), and alphanumerics between. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field ``effective_annotations`` for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#annotations ContainerAwsNodePool#annotations}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#id ContainerAwsNodePool#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kubelet_config: kubelet_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#kubelet_config ContainerAwsNodePool#kubelet_config}
        :param management: management block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#management ContainerAwsNodePool#management}
        :param project: The project for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#project ContainerAwsNodePool#project}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#timeouts ContainerAwsNodePool#timeouts}
        :param update_settings: update_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#update_settings ContainerAwsNodePool#update_settings}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ad104cb8ba25f011d9c5a747e3062e01de95616d7b8d8333c2d536a182fbfa5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config_ = ContainerAwsNodePoolConfig(
            autoscaling=autoscaling,
            cluster=cluster,
            config=config,
            location=location,
            max_pods_constraint=max_pods_constraint,
            name=name,
            subnet_id=subnet_id,
            version=version,
            annotations=annotations,
            id=id,
            kubelet_config=kubelet_config,
            management=management,
            project=project,
            timeouts=timeouts,
            update_settings=update_settings,
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
        '''Generates CDKTF code for importing a ContainerAwsNodePool resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ContainerAwsNodePool to import.
        :param import_from_id: The id of the existing ContainerAwsNodePool that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ContainerAwsNodePool to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1d211073115aa34c305b0ffa505ffb0dc9e3aa0ed57e2f3094fe7635dd26ed0)
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
        :param max_node_count: Maximum number of nodes in the NodePool. Must be >= min_node_count. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#max_node_count ContainerAwsNodePool#max_node_count}
        :param min_node_count: Minimum number of nodes in the NodePool. Must be >= 1 and <= max_node_count. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#min_node_count ContainerAwsNodePool#min_node_count}
        '''
        value = ContainerAwsNodePoolAutoscaling(
            max_node_count=max_node_count, min_node_count=min_node_count
        )

        return typing.cast(None, jsii.invoke(self, "putAutoscaling", [value]))

    @jsii.member(jsii_name="putConfig")
    def put_config(
        self,
        *,
        config_encryption: typing.Union["ContainerAwsNodePoolConfigConfigEncryption", typing.Dict[builtins.str, typing.Any]],
        iam_instance_profile: builtins.str,
        autoscaling_metrics_collection: typing.Optional[typing.Union["ContainerAwsNodePoolConfigAutoscalingMetricsCollection", typing.Dict[builtins.str, typing.Any]]] = None,
        instance_type: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        proxy_config: typing.Optional[typing.Union["ContainerAwsNodePoolConfigProxyConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        root_volume: typing.Optional[typing.Union["ContainerAwsNodePoolConfigRootVolume", typing.Dict[builtins.str, typing.Any]]] = None,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        ssh_config: typing.Optional[typing.Union["ContainerAwsNodePoolConfigSshConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        taints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAwsNodePoolConfigTaints", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param config_encryption: config_encryption block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#config_encryption ContainerAwsNodePool#config_encryption}
        :param iam_instance_profile: The name of the AWS IAM role assigned to nodes in the pool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#iam_instance_profile ContainerAwsNodePool#iam_instance_profile}
        :param autoscaling_metrics_collection: autoscaling_metrics_collection block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#autoscaling_metrics_collection ContainerAwsNodePool#autoscaling_metrics_collection}
        :param instance_type: Optional. The AWS instance type. When unspecified, it defaults to ``m5.large``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#instance_type ContainerAwsNodePool#instance_type}
        :param labels: Optional. The initial labels assigned to nodes of this node pool. An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#labels ContainerAwsNodePool#labels}
        :param proxy_config: proxy_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#proxy_config ContainerAwsNodePool#proxy_config}
        :param root_volume: root_volume block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#root_volume ContainerAwsNodePool#root_volume}
        :param security_group_ids: Optional. The IDs of additional security groups to add to nodes in this pool. The manager will automatically create security groups with minimum rules needed for a functioning cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#security_group_ids ContainerAwsNodePool#security_group_ids}
        :param ssh_config: ssh_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#ssh_config ContainerAwsNodePool#ssh_config}
        :param tags: Optional. Key/value metadata to assign to each underlying AWS resource. Specify at most 50 pairs containing alphanumerics, spaces, and symbols (.+-=_:@/). Keys can be up to 127 Unicode characters. Values can be up to 255 Unicode characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#tags ContainerAwsNodePool#tags}
        :param taints: taints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#taints ContainerAwsNodePool#taints}
        '''
        value = ContainerAwsNodePoolConfigA(
            config_encryption=config_encryption,
            iam_instance_profile=iam_instance_profile,
            autoscaling_metrics_collection=autoscaling_metrics_collection,
            instance_type=instance_type,
            labels=labels,
            proxy_config=proxy_config,
            root_volume=root_volume,
            security_group_ids=security_group_ids,
            ssh_config=ssh_config,
            tags=tags,
            taints=taints,
        )

        return typing.cast(None, jsii.invoke(self, "putConfig", [value]))

    @jsii.member(jsii_name="putKubeletConfig")
    def put_kubelet_config(
        self,
        *,
        cpu_cfs_quota: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        cpu_cfs_quota_period: typing.Optional[builtins.str] = None,
        cpu_manager_policy: typing.Optional[builtins.str] = None,
        pod_pids_limit: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param cpu_cfs_quota: Whether or not to enable CPU CFS quota. Defaults to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#cpu_cfs_quota ContainerAwsNodePool#cpu_cfs_quota}
        :param cpu_cfs_quota_period: Optional. The CPU CFS quota period to use for the node. Defaults to "100ms". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#cpu_cfs_quota_period ContainerAwsNodePool#cpu_cfs_quota_period}
        :param cpu_manager_policy: The CpuManagerPolicy to use for the node. Defaults to "none". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#cpu_manager_policy ContainerAwsNodePool#cpu_manager_policy}
        :param pod_pids_limit: Optional. The maximum number of PIDs in each pod running on the node. The limit scales automatically based on underlying machine size if left unset. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#pod_pids_limit ContainerAwsNodePool#pod_pids_limit}
        '''
        value = ContainerAwsNodePoolKubeletConfig(
            cpu_cfs_quota=cpu_cfs_quota,
            cpu_cfs_quota_period=cpu_cfs_quota_period,
            cpu_manager_policy=cpu_manager_policy,
            pod_pids_limit=pod_pids_limit,
        )

        return typing.cast(None, jsii.invoke(self, "putKubeletConfig", [value]))

    @jsii.member(jsii_name="putManagement")
    def put_management(
        self,
        *,
        auto_repair: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param auto_repair: Optional. Whether or not the nodes will be automatically repaired. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#auto_repair ContainerAwsNodePool#auto_repair}
        '''
        value = ContainerAwsNodePoolManagement(auto_repair=auto_repair)

        return typing.cast(None, jsii.invoke(self, "putManagement", [value]))

    @jsii.member(jsii_name="putMaxPodsConstraint")
    def put_max_pods_constraint(self, *, max_pods_per_node: jsii.Number) -> None:
        '''
        :param max_pods_per_node: The maximum number of pods to schedule on a single node. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#max_pods_per_node ContainerAwsNodePool#max_pods_per_node}
        '''
        value = ContainerAwsNodePoolMaxPodsConstraint(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#create ContainerAwsNodePool#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#delete ContainerAwsNodePool#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#update ContainerAwsNodePool#update}.
        '''
        value = ContainerAwsNodePoolTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putUpdateSettings")
    def put_update_settings(
        self,
        *,
        surge_settings: typing.Optional[typing.Union["ContainerAwsNodePoolUpdateSettingsSurgeSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param surge_settings: surge_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#surge_settings ContainerAwsNodePool#surge_settings}
        '''
        value = ContainerAwsNodePoolUpdateSettings(surge_settings=surge_settings)

        return typing.cast(None, jsii.invoke(self, "putUpdateSettings", [value]))

    @jsii.member(jsii_name="resetAnnotations")
    def reset_annotations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnnotations", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetKubeletConfig")
    def reset_kubelet_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKubeletConfig", []))

    @jsii.member(jsii_name="resetManagement")
    def reset_management(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManagement", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetUpdateSettings")
    def reset_update_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdateSettings", []))

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
    def autoscaling(self) -> "ContainerAwsNodePoolAutoscalingOutputReference":
        return typing.cast("ContainerAwsNodePoolAutoscalingOutputReference", jsii.get(self, "autoscaling"))

    @builtins.property
    @jsii.member(jsii_name="config")
    def config(self) -> "ContainerAwsNodePoolConfigAOutputReference":
        return typing.cast("ContainerAwsNodePoolConfigAOutputReference", jsii.get(self, "config"))

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
    @jsii.member(jsii_name="kubeletConfig")
    def kubelet_config(self) -> "ContainerAwsNodePoolKubeletConfigOutputReference":
        return typing.cast("ContainerAwsNodePoolKubeletConfigOutputReference", jsii.get(self, "kubeletConfig"))

    @builtins.property
    @jsii.member(jsii_name="management")
    def management(self) -> "ContainerAwsNodePoolManagementOutputReference":
        return typing.cast("ContainerAwsNodePoolManagementOutputReference", jsii.get(self, "management"))

    @builtins.property
    @jsii.member(jsii_name="maxPodsConstraint")
    def max_pods_constraint(
        self,
    ) -> "ContainerAwsNodePoolMaxPodsConstraintOutputReference":
        return typing.cast("ContainerAwsNodePoolMaxPodsConstraintOutputReference", jsii.get(self, "maxPodsConstraint"))

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
    def timeouts(self) -> "ContainerAwsNodePoolTimeoutsOutputReference":
        return typing.cast("ContainerAwsNodePoolTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="uid")
    def uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uid"))

    @builtins.property
    @jsii.member(jsii_name="updateSettings")
    def update_settings(self) -> "ContainerAwsNodePoolUpdateSettingsOutputReference":
        return typing.cast("ContainerAwsNodePoolUpdateSettingsOutputReference", jsii.get(self, "updateSettings"))

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
    def autoscaling_input(self) -> typing.Optional["ContainerAwsNodePoolAutoscaling"]:
        return typing.cast(typing.Optional["ContainerAwsNodePoolAutoscaling"], jsii.get(self, "autoscalingInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterInput")
    def cluster_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterInput"))

    @builtins.property
    @jsii.member(jsii_name="configInput")
    def config_input(self) -> typing.Optional["ContainerAwsNodePoolConfigA"]:
        return typing.cast(typing.Optional["ContainerAwsNodePoolConfigA"], jsii.get(self, "configInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="kubeletConfigInput")
    def kubelet_config_input(
        self,
    ) -> typing.Optional["ContainerAwsNodePoolKubeletConfig"]:
        return typing.cast(typing.Optional["ContainerAwsNodePoolKubeletConfig"], jsii.get(self, "kubeletConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="managementInput")
    def management_input(self) -> typing.Optional["ContainerAwsNodePoolManagement"]:
        return typing.cast(typing.Optional["ContainerAwsNodePoolManagement"], jsii.get(self, "managementInput"))

    @builtins.property
    @jsii.member(jsii_name="maxPodsConstraintInput")
    def max_pods_constraint_input(
        self,
    ) -> typing.Optional["ContainerAwsNodePoolMaxPodsConstraint"]:
        return typing.cast(typing.Optional["ContainerAwsNodePoolMaxPodsConstraint"], jsii.get(self, "maxPodsConstraintInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ContainerAwsNodePoolTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ContainerAwsNodePoolTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="updateSettingsInput")
    def update_settings_input(
        self,
    ) -> typing.Optional["ContainerAwsNodePoolUpdateSettings"]:
        return typing.cast(typing.Optional["ContainerAwsNodePoolUpdateSettings"], jsii.get(self, "updateSettingsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__b82e7d7778ad3c68bcbb5f6fe3178faedfa39d1cfe953c9d2753eec13b3f6979)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cluster"))

    @cluster.setter
    def cluster(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dc7565ef085be22f63f6b915b96df2ac5b66659bed1fb47f48cb421377c0d86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cluster", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e19d676fe3de3da32c30150841547cb8e51f62f1546a91bb7afbc56908c2613)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb5233a6b16bcd5a94b2149eb69c485f143ef117cd4c4b9efd948d3633e47ad1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__763849d552b8a1e2a93cb19a037277bdf5a6152647633f66bd292b464229cf71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__387465ae57d441ae17ba01edc2d8fdb55b613964b97cc9d5d0c84ffc5870a292)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e30b5103ede4a39e1fe153416847acb7f758325c47fbc5ed3932237f41a6d2ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a52567506bfe976c6632df35807d3e9f5da4f8fa08043b1eaf6740c0cc31ee8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAwsNodePool.ContainerAwsNodePoolAutoscaling",
    jsii_struct_bases=[],
    name_mapping={"max_node_count": "maxNodeCount", "min_node_count": "minNodeCount"},
)
class ContainerAwsNodePoolAutoscaling:
    def __init__(
        self,
        *,
        max_node_count: jsii.Number,
        min_node_count: jsii.Number,
    ) -> None:
        '''
        :param max_node_count: Maximum number of nodes in the NodePool. Must be >= min_node_count. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#max_node_count ContainerAwsNodePool#max_node_count}
        :param min_node_count: Minimum number of nodes in the NodePool. Must be >= 1 and <= max_node_count. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#min_node_count ContainerAwsNodePool#min_node_count}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd64a433d527d89df9417424cb1a02825c465d00157837096d9706805e8a2c76)
            check_type(argname="argument max_node_count", value=max_node_count, expected_type=type_hints["max_node_count"])
            check_type(argname="argument min_node_count", value=min_node_count, expected_type=type_hints["min_node_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "max_node_count": max_node_count,
            "min_node_count": min_node_count,
        }

    @builtins.property
    def max_node_count(self) -> jsii.Number:
        '''Maximum number of nodes in the NodePool. Must be >= min_node_count.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#max_node_count ContainerAwsNodePool#max_node_count}
        '''
        result = self._values.get("max_node_count")
        assert result is not None, "Required property 'max_node_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def min_node_count(self) -> jsii.Number:
        '''Minimum number of nodes in the NodePool. Must be >= 1 and <= max_node_count.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#min_node_count ContainerAwsNodePool#min_node_count}
        '''
        result = self._values.get("min_node_count")
        assert result is not None, "Required property 'min_node_count' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAwsNodePoolAutoscaling(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAwsNodePoolAutoscalingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAwsNodePool.ContainerAwsNodePoolAutoscalingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__73e9459364640ef99580f75c9323c8459fff97206f8c21326ebe1017905c4802)
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
            type_hints = typing.get_type_hints(_typecheckingstub__090ea3ecbd6365c4a780e1b898942cc2bcd875eea3e52ef62d3a3543d475d23a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxNodeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minNodeCount")
    def min_node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minNodeCount"))

    @min_node_count.setter
    def min_node_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1af0b100f53875681d6a91bc56a078e937584f2055f55bb10702171e389feb33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minNodeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ContainerAwsNodePoolAutoscaling]:
        return typing.cast(typing.Optional[ContainerAwsNodePoolAutoscaling], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerAwsNodePoolAutoscaling],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2f853f7b49dbb0b15f5db63ce210f983f2a2f79c87029a7541c036e4f761a58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAwsNodePool.ContainerAwsNodePoolConfig",
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
        "id": "id",
        "kubelet_config": "kubeletConfig",
        "management": "management",
        "project": "project",
        "timeouts": "timeouts",
        "update_settings": "updateSettings",
    },
)
class ContainerAwsNodePoolConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        autoscaling: typing.Union[ContainerAwsNodePoolAutoscaling, typing.Dict[builtins.str, typing.Any]],
        cluster: builtins.str,
        config: typing.Union["ContainerAwsNodePoolConfigA", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        max_pods_constraint: typing.Union["ContainerAwsNodePoolMaxPodsConstraint", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        subnet_id: builtins.str,
        version: builtins.str,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        kubelet_config: typing.Optional[typing.Union["ContainerAwsNodePoolKubeletConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        management: typing.Optional[typing.Union["ContainerAwsNodePoolManagement", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ContainerAwsNodePoolTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        update_settings: typing.Optional[typing.Union["ContainerAwsNodePoolUpdateSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param autoscaling: autoscaling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#autoscaling ContainerAwsNodePool#autoscaling}
        :param cluster: The awsCluster for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#cluster ContainerAwsNodePool#cluster}
        :param config: config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#config ContainerAwsNodePool#config}
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#location ContainerAwsNodePool#location}
        :param max_pods_constraint: max_pods_constraint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#max_pods_constraint ContainerAwsNodePool#max_pods_constraint}
        :param name: The name of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#name ContainerAwsNodePool#name}
        :param subnet_id: The subnet where the node pool node run. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#subnet_id ContainerAwsNodePool#subnet_id}
        :param version: The Kubernetes version to run on this node pool (e.g. ``1.19.10-gke.1000``). You can list all supported versions on a given Google Cloud region by calling GetAwsServerConfig. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#version ContainerAwsNodePool#version}
        :param annotations: Optional. Annotations on the node pool. This field has the same restrictions as Kubernetes annotations. The total size of all keys and values combined is limited to 256k. Key can have 2 segments: prefix (optional) and name (required), separated by a slash (/). Prefix must be a DNS subdomain. Name must be 63 characters or less, begin and end with alphanumerics, with dashes (-), underscores (_), dots (.), and alphanumerics between. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field ``effective_annotations`` for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#annotations ContainerAwsNodePool#annotations}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#id ContainerAwsNodePool#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kubelet_config: kubelet_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#kubelet_config ContainerAwsNodePool#kubelet_config}
        :param management: management block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#management ContainerAwsNodePool#management}
        :param project: The project for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#project ContainerAwsNodePool#project}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#timeouts ContainerAwsNodePool#timeouts}
        :param update_settings: update_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#update_settings ContainerAwsNodePool#update_settings}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(autoscaling, dict):
            autoscaling = ContainerAwsNodePoolAutoscaling(**autoscaling)
        if isinstance(config, dict):
            config = ContainerAwsNodePoolConfigA(**config)
        if isinstance(max_pods_constraint, dict):
            max_pods_constraint = ContainerAwsNodePoolMaxPodsConstraint(**max_pods_constraint)
        if isinstance(kubelet_config, dict):
            kubelet_config = ContainerAwsNodePoolKubeletConfig(**kubelet_config)
        if isinstance(management, dict):
            management = ContainerAwsNodePoolManagement(**management)
        if isinstance(timeouts, dict):
            timeouts = ContainerAwsNodePoolTimeouts(**timeouts)
        if isinstance(update_settings, dict):
            update_settings = ContainerAwsNodePoolUpdateSettings(**update_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12b442ce3b8f6c99c96938646fa69f712da6eb1404ce878b0761ce06721b6938)
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
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument kubelet_config", value=kubelet_config, expected_type=type_hints["kubelet_config"])
            check_type(argname="argument management", value=management, expected_type=type_hints["management"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument update_settings", value=update_settings, expected_type=type_hints["update_settings"])
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
        if id is not None:
            self._values["id"] = id
        if kubelet_config is not None:
            self._values["kubelet_config"] = kubelet_config
        if management is not None:
            self._values["management"] = management
        if project is not None:
            self._values["project"] = project
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if update_settings is not None:
            self._values["update_settings"] = update_settings

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
    def autoscaling(self) -> ContainerAwsNodePoolAutoscaling:
        '''autoscaling block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#autoscaling ContainerAwsNodePool#autoscaling}
        '''
        result = self._values.get("autoscaling")
        assert result is not None, "Required property 'autoscaling' is missing"
        return typing.cast(ContainerAwsNodePoolAutoscaling, result)

    @builtins.property
    def cluster(self) -> builtins.str:
        '''The awsCluster for the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#cluster ContainerAwsNodePool#cluster}
        '''
        result = self._values.get("cluster")
        assert result is not None, "Required property 'cluster' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def config(self) -> "ContainerAwsNodePoolConfigA":
        '''config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#config ContainerAwsNodePool#config}
        '''
        result = self._values.get("config")
        assert result is not None, "Required property 'config' is missing"
        return typing.cast("ContainerAwsNodePoolConfigA", result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location for the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#location ContainerAwsNodePool#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def max_pods_constraint(self) -> "ContainerAwsNodePoolMaxPodsConstraint":
        '''max_pods_constraint block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#max_pods_constraint ContainerAwsNodePool#max_pods_constraint}
        '''
        result = self._values.get("max_pods_constraint")
        assert result is not None, "Required property 'max_pods_constraint' is missing"
        return typing.cast("ContainerAwsNodePoolMaxPodsConstraint", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#name ContainerAwsNodePool#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subnet_id(self) -> builtins.str:
        '''The subnet where the node pool node run.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#subnet_id ContainerAwsNodePool#subnet_id}
        '''
        result = self._values.get("subnet_id")
        assert result is not None, "Required property 'subnet_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version(self) -> builtins.str:
        '''The Kubernetes version to run on this node pool (e.g. ``1.19.10-gke.1000``). You can list all supported versions on a given Google Cloud region by calling GetAwsServerConfig.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#version ContainerAwsNodePool#version}
        '''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def annotations(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional.

        Annotations on the node pool. This field has the same restrictions as Kubernetes annotations. The total size of all keys and values combined is limited to 256k. Key can have 2 segments: prefix (optional) and name (required), separated by a slash (/). Prefix must be a DNS subdomain. Name must be 63 characters or less, begin and end with alphanumerics, with dashes (-), underscores (_), dots (.), and alphanumerics between.

        **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration.
        Please refer to the field ``effective_annotations`` for all of the annotations present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#annotations ContainerAwsNodePool#annotations}
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#id ContainerAwsNodePool#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kubelet_config(self) -> typing.Optional["ContainerAwsNodePoolKubeletConfig"]:
        '''kubelet_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#kubelet_config ContainerAwsNodePool#kubelet_config}
        '''
        result = self._values.get("kubelet_config")
        return typing.cast(typing.Optional["ContainerAwsNodePoolKubeletConfig"], result)

    @builtins.property
    def management(self) -> typing.Optional["ContainerAwsNodePoolManagement"]:
        '''management block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#management ContainerAwsNodePool#management}
        '''
        result = self._values.get("management")
        return typing.cast(typing.Optional["ContainerAwsNodePoolManagement"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''The project for the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#project ContainerAwsNodePool#project}
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ContainerAwsNodePoolTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#timeouts ContainerAwsNodePool#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ContainerAwsNodePoolTimeouts"], result)

    @builtins.property
    def update_settings(self) -> typing.Optional["ContainerAwsNodePoolUpdateSettings"]:
        '''update_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#update_settings ContainerAwsNodePool#update_settings}
        '''
        result = self._values.get("update_settings")
        return typing.cast(typing.Optional["ContainerAwsNodePoolUpdateSettings"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAwsNodePoolConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAwsNodePool.ContainerAwsNodePoolConfigA",
    jsii_struct_bases=[],
    name_mapping={
        "config_encryption": "configEncryption",
        "iam_instance_profile": "iamInstanceProfile",
        "autoscaling_metrics_collection": "autoscalingMetricsCollection",
        "instance_type": "instanceType",
        "labels": "labels",
        "proxy_config": "proxyConfig",
        "root_volume": "rootVolume",
        "security_group_ids": "securityGroupIds",
        "ssh_config": "sshConfig",
        "tags": "tags",
        "taints": "taints",
    },
)
class ContainerAwsNodePoolConfigA:
    def __init__(
        self,
        *,
        config_encryption: typing.Union["ContainerAwsNodePoolConfigConfigEncryption", typing.Dict[builtins.str, typing.Any]],
        iam_instance_profile: builtins.str,
        autoscaling_metrics_collection: typing.Optional[typing.Union["ContainerAwsNodePoolConfigAutoscalingMetricsCollection", typing.Dict[builtins.str, typing.Any]]] = None,
        instance_type: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        proxy_config: typing.Optional[typing.Union["ContainerAwsNodePoolConfigProxyConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        root_volume: typing.Optional[typing.Union["ContainerAwsNodePoolConfigRootVolume", typing.Dict[builtins.str, typing.Any]]] = None,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        ssh_config: typing.Optional[typing.Union["ContainerAwsNodePoolConfigSshConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        taints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAwsNodePoolConfigTaints", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param config_encryption: config_encryption block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#config_encryption ContainerAwsNodePool#config_encryption}
        :param iam_instance_profile: The name of the AWS IAM role assigned to nodes in the pool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#iam_instance_profile ContainerAwsNodePool#iam_instance_profile}
        :param autoscaling_metrics_collection: autoscaling_metrics_collection block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#autoscaling_metrics_collection ContainerAwsNodePool#autoscaling_metrics_collection}
        :param instance_type: Optional. The AWS instance type. When unspecified, it defaults to ``m5.large``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#instance_type ContainerAwsNodePool#instance_type}
        :param labels: Optional. The initial labels assigned to nodes of this node pool. An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#labels ContainerAwsNodePool#labels}
        :param proxy_config: proxy_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#proxy_config ContainerAwsNodePool#proxy_config}
        :param root_volume: root_volume block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#root_volume ContainerAwsNodePool#root_volume}
        :param security_group_ids: Optional. The IDs of additional security groups to add to nodes in this pool. The manager will automatically create security groups with minimum rules needed for a functioning cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#security_group_ids ContainerAwsNodePool#security_group_ids}
        :param ssh_config: ssh_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#ssh_config ContainerAwsNodePool#ssh_config}
        :param tags: Optional. Key/value metadata to assign to each underlying AWS resource. Specify at most 50 pairs containing alphanumerics, spaces, and symbols (.+-=_:@/). Keys can be up to 127 Unicode characters. Values can be up to 255 Unicode characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#tags ContainerAwsNodePool#tags}
        :param taints: taints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#taints ContainerAwsNodePool#taints}
        '''
        if isinstance(config_encryption, dict):
            config_encryption = ContainerAwsNodePoolConfigConfigEncryption(**config_encryption)
        if isinstance(autoscaling_metrics_collection, dict):
            autoscaling_metrics_collection = ContainerAwsNodePoolConfigAutoscalingMetricsCollection(**autoscaling_metrics_collection)
        if isinstance(proxy_config, dict):
            proxy_config = ContainerAwsNodePoolConfigProxyConfig(**proxy_config)
        if isinstance(root_volume, dict):
            root_volume = ContainerAwsNodePoolConfigRootVolume(**root_volume)
        if isinstance(ssh_config, dict):
            ssh_config = ContainerAwsNodePoolConfigSshConfig(**ssh_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79f3e405d986c2511257e72a2af0e3171bd60d67bf0c491cb789a74f4405be74)
            check_type(argname="argument config_encryption", value=config_encryption, expected_type=type_hints["config_encryption"])
            check_type(argname="argument iam_instance_profile", value=iam_instance_profile, expected_type=type_hints["iam_instance_profile"])
            check_type(argname="argument autoscaling_metrics_collection", value=autoscaling_metrics_collection, expected_type=type_hints["autoscaling_metrics_collection"])
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument proxy_config", value=proxy_config, expected_type=type_hints["proxy_config"])
            check_type(argname="argument root_volume", value=root_volume, expected_type=type_hints["root_volume"])
            check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
            check_type(argname="argument ssh_config", value=ssh_config, expected_type=type_hints["ssh_config"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument taints", value=taints, expected_type=type_hints["taints"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "config_encryption": config_encryption,
            "iam_instance_profile": iam_instance_profile,
        }
        if autoscaling_metrics_collection is not None:
            self._values["autoscaling_metrics_collection"] = autoscaling_metrics_collection
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if labels is not None:
            self._values["labels"] = labels
        if proxy_config is not None:
            self._values["proxy_config"] = proxy_config
        if root_volume is not None:
            self._values["root_volume"] = root_volume
        if security_group_ids is not None:
            self._values["security_group_ids"] = security_group_ids
        if ssh_config is not None:
            self._values["ssh_config"] = ssh_config
        if tags is not None:
            self._values["tags"] = tags
        if taints is not None:
            self._values["taints"] = taints

    @builtins.property
    def config_encryption(self) -> "ContainerAwsNodePoolConfigConfigEncryption":
        '''config_encryption block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#config_encryption ContainerAwsNodePool#config_encryption}
        '''
        result = self._values.get("config_encryption")
        assert result is not None, "Required property 'config_encryption' is missing"
        return typing.cast("ContainerAwsNodePoolConfigConfigEncryption", result)

    @builtins.property
    def iam_instance_profile(self) -> builtins.str:
        '''The name of the AWS IAM role assigned to nodes in the pool.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#iam_instance_profile ContainerAwsNodePool#iam_instance_profile}
        '''
        result = self._values.get("iam_instance_profile")
        assert result is not None, "Required property 'iam_instance_profile' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def autoscaling_metrics_collection(
        self,
    ) -> typing.Optional["ContainerAwsNodePoolConfigAutoscalingMetricsCollection"]:
        '''autoscaling_metrics_collection block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#autoscaling_metrics_collection ContainerAwsNodePool#autoscaling_metrics_collection}
        '''
        result = self._values.get("autoscaling_metrics_collection")
        return typing.cast(typing.Optional["ContainerAwsNodePoolConfigAutoscalingMetricsCollection"], result)

    @builtins.property
    def instance_type(self) -> typing.Optional[builtins.str]:
        '''Optional. The AWS instance type. When unspecified, it defaults to ``m5.large``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#instance_type ContainerAwsNodePool#instance_type}
        '''
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional.

        The initial labels assigned to nodes of this node pool. An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#labels ContainerAwsNodePool#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def proxy_config(self) -> typing.Optional["ContainerAwsNodePoolConfigProxyConfig"]:
        '''proxy_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#proxy_config ContainerAwsNodePool#proxy_config}
        '''
        result = self._values.get("proxy_config")
        return typing.cast(typing.Optional["ContainerAwsNodePoolConfigProxyConfig"], result)

    @builtins.property
    def root_volume(self) -> typing.Optional["ContainerAwsNodePoolConfigRootVolume"]:
        '''root_volume block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#root_volume ContainerAwsNodePool#root_volume}
        '''
        result = self._values.get("root_volume")
        return typing.cast(typing.Optional["ContainerAwsNodePoolConfigRootVolume"], result)

    @builtins.property
    def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional.

        The IDs of additional security groups to add to nodes in this pool. The manager will automatically create security groups with minimum rules needed for a functioning cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#security_group_ids ContainerAwsNodePool#security_group_ids}
        '''
        result = self._values.get("security_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ssh_config(self) -> typing.Optional["ContainerAwsNodePoolConfigSshConfig"]:
        '''ssh_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#ssh_config ContainerAwsNodePool#ssh_config}
        '''
        result = self._values.get("ssh_config")
        return typing.cast(typing.Optional["ContainerAwsNodePoolConfigSshConfig"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional.

        Key/value metadata to assign to each underlying AWS resource. Specify at most 50 pairs containing alphanumerics, spaces, and symbols (.+-=_:@/). Keys can be up to 127 Unicode characters. Values can be up to 255 Unicode characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#tags ContainerAwsNodePool#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def taints(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAwsNodePoolConfigTaints"]]]:
        '''taints block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#taints ContainerAwsNodePool#taints}
        '''
        result = self._values.get("taints")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAwsNodePoolConfigTaints"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAwsNodePoolConfigA(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAwsNodePoolConfigAOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAwsNodePool.ContainerAwsNodePoolConfigAOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9a08b76f6349bbdc9db142de3d01892c1aa2f4f235e302cf0ea858eedf02f5e8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAutoscalingMetricsCollection")
    def put_autoscaling_metrics_collection(
        self,
        *,
        granularity: builtins.str,
        metrics: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param granularity: The frequency at which EC2 Auto Scaling sends aggregated data to AWS CloudWatch. The only valid value is "1Minute". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#granularity ContainerAwsNodePool#granularity}
        :param metrics: The metrics to enable. For a list of valid metrics, see https://docs.aws.amazon.com/autoscaling/ec2/APIReference/API_EnableMetricsCollection.html. If you specify granularity and don't specify any metrics, all metrics are enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#metrics ContainerAwsNodePool#metrics}
        '''
        value = ContainerAwsNodePoolConfigAutoscalingMetricsCollection(
            granularity=granularity, metrics=metrics
        )

        return typing.cast(None, jsii.invoke(self, "putAutoscalingMetricsCollection", [value]))

    @jsii.member(jsii_name="putConfigEncryption")
    def put_config_encryption(self, *, kms_key_arn: builtins.str) -> None:
        '''
        :param kms_key_arn: The ARN of the AWS KMS key used to encrypt node pool configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#kms_key_arn ContainerAwsNodePool#kms_key_arn}
        '''
        value = ContainerAwsNodePoolConfigConfigEncryption(kms_key_arn=kms_key_arn)

        return typing.cast(None, jsii.invoke(self, "putConfigEncryption", [value]))

    @jsii.member(jsii_name="putProxyConfig")
    def put_proxy_config(
        self,
        *,
        secret_arn: builtins.str,
        secret_version: builtins.str,
    ) -> None:
        '''
        :param secret_arn: The ARN of the AWS Secret Manager secret that contains the HTTP(S) proxy configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#secret_arn ContainerAwsNodePool#secret_arn}
        :param secret_version: The version string of the AWS Secret Manager secret that contains the HTTP(S) proxy configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#secret_version ContainerAwsNodePool#secret_version}
        '''
        value = ContainerAwsNodePoolConfigProxyConfig(
            secret_arn=secret_arn, secret_version=secret_version
        )

        return typing.cast(None, jsii.invoke(self, "putProxyConfig", [value]))

    @jsii.member(jsii_name="putRootVolume")
    def put_root_volume(
        self,
        *,
        iops: typing.Optional[jsii.Number] = None,
        kms_key_arn: typing.Optional[builtins.str] = None,
        size_gib: typing.Optional[jsii.Number] = None,
        throughput: typing.Optional[jsii.Number] = None,
        volume_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param iops: Optional. The number of I/O operations per second (IOPS) to provision for GP3 volume. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#iops ContainerAwsNodePool#iops}
        :param kms_key_arn: Optional. The Amazon Resource Name (ARN) of the Customer Managed Key (CMK) used to encrypt AWS EBS volumes. If not specified, the default Amazon managed key associated to the AWS region where this cluster runs will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#kms_key_arn ContainerAwsNodePool#kms_key_arn}
        :param size_gib: Optional. The size of the volume, in GiBs. When unspecified, a default value is provided. See the specific reference in the parent resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#size_gib ContainerAwsNodePool#size_gib}
        :param throughput: Optional. The throughput to provision for the volume, in MiB/s. Only valid if the volume type is GP3. If volume type is gp3 and throughput is not specified, the throughput will defaults to 125. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#throughput ContainerAwsNodePool#throughput}
        :param volume_type: Optional. Type of the EBS volume. When unspecified, it defaults to GP2 volume. Possible values: VOLUME_TYPE_UNSPECIFIED, GP2, GP3. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#volume_type ContainerAwsNodePool#volume_type}
        '''
        value = ContainerAwsNodePoolConfigRootVolume(
            iops=iops,
            kms_key_arn=kms_key_arn,
            size_gib=size_gib,
            throughput=throughput,
            volume_type=volume_type,
        )

        return typing.cast(None, jsii.invoke(self, "putRootVolume", [value]))

    @jsii.member(jsii_name="putSshConfig")
    def put_ssh_config(self, *, ec2_key_pair: builtins.str) -> None:
        '''
        :param ec2_key_pair: The name of the EC2 key pair used to login into cluster machines. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#ec2_key_pair ContainerAwsNodePool#ec2_key_pair}
        '''
        value = ContainerAwsNodePoolConfigSshConfig(ec2_key_pair=ec2_key_pair)

        return typing.cast(None, jsii.invoke(self, "putSshConfig", [value]))

    @jsii.member(jsii_name="putTaints")
    def put_taints(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAwsNodePoolConfigTaints", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d55709bd351472853d7d3132a1c92e1172e3acba5108bd86113961779555038)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTaints", [value]))

    @jsii.member(jsii_name="resetAutoscalingMetricsCollection")
    def reset_autoscaling_metrics_collection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoscalingMetricsCollection", []))

    @jsii.member(jsii_name="resetInstanceType")
    def reset_instance_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceType", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetProxyConfig")
    def reset_proxy_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProxyConfig", []))

    @jsii.member(jsii_name="resetRootVolume")
    def reset_root_volume(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRootVolume", []))

    @jsii.member(jsii_name="resetSecurityGroupIds")
    def reset_security_group_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityGroupIds", []))

    @jsii.member(jsii_name="resetSshConfig")
    def reset_ssh_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSshConfig", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTaints")
    def reset_taints(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTaints", []))

    @builtins.property
    @jsii.member(jsii_name="autoscalingMetricsCollection")
    def autoscaling_metrics_collection(
        self,
    ) -> "ContainerAwsNodePoolConfigAutoscalingMetricsCollectionOutputReference":
        return typing.cast("ContainerAwsNodePoolConfigAutoscalingMetricsCollectionOutputReference", jsii.get(self, "autoscalingMetricsCollection"))

    @builtins.property
    @jsii.member(jsii_name="configEncryption")
    def config_encryption(
        self,
    ) -> "ContainerAwsNodePoolConfigConfigEncryptionOutputReference":
        return typing.cast("ContainerAwsNodePoolConfigConfigEncryptionOutputReference", jsii.get(self, "configEncryption"))

    @builtins.property
    @jsii.member(jsii_name="proxyConfig")
    def proxy_config(self) -> "ContainerAwsNodePoolConfigProxyConfigOutputReference":
        return typing.cast("ContainerAwsNodePoolConfigProxyConfigOutputReference", jsii.get(self, "proxyConfig"))

    @builtins.property
    @jsii.member(jsii_name="rootVolume")
    def root_volume(self) -> "ContainerAwsNodePoolConfigRootVolumeOutputReference":
        return typing.cast("ContainerAwsNodePoolConfigRootVolumeOutputReference", jsii.get(self, "rootVolume"))

    @builtins.property
    @jsii.member(jsii_name="sshConfig")
    def ssh_config(self) -> "ContainerAwsNodePoolConfigSshConfigOutputReference":
        return typing.cast("ContainerAwsNodePoolConfigSshConfigOutputReference", jsii.get(self, "sshConfig"))

    @builtins.property
    @jsii.member(jsii_name="taints")
    def taints(self) -> "ContainerAwsNodePoolConfigTaintsList":
        return typing.cast("ContainerAwsNodePoolConfigTaintsList", jsii.get(self, "taints"))

    @builtins.property
    @jsii.member(jsii_name="autoscalingMetricsCollectionInput")
    def autoscaling_metrics_collection_input(
        self,
    ) -> typing.Optional["ContainerAwsNodePoolConfigAutoscalingMetricsCollection"]:
        return typing.cast(typing.Optional["ContainerAwsNodePoolConfigAutoscalingMetricsCollection"], jsii.get(self, "autoscalingMetricsCollectionInput"))

    @builtins.property
    @jsii.member(jsii_name="configEncryptionInput")
    def config_encryption_input(
        self,
    ) -> typing.Optional["ContainerAwsNodePoolConfigConfigEncryption"]:
        return typing.cast(typing.Optional["ContainerAwsNodePoolConfigConfigEncryption"], jsii.get(self, "configEncryptionInput"))

    @builtins.property
    @jsii.member(jsii_name="iamInstanceProfileInput")
    def iam_instance_profile_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "iamInstanceProfileInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceTypeInput")
    def instance_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceTypeInput"))

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
    ) -> typing.Optional["ContainerAwsNodePoolConfigProxyConfig"]:
        return typing.cast(typing.Optional["ContainerAwsNodePoolConfigProxyConfig"], jsii.get(self, "proxyConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="rootVolumeInput")
    def root_volume_input(
        self,
    ) -> typing.Optional["ContainerAwsNodePoolConfigRootVolume"]:
        return typing.cast(typing.Optional["ContainerAwsNodePoolConfigRootVolume"], jsii.get(self, "rootVolumeInput"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupIdsInput")
    def security_group_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "securityGroupIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="sshConfigInput")
    def ssh_config_input(
        self,
    ) -> typing.Optional["ContainerAwsNodePoolConfigSshConfig"]:
        return typing.cast(typing.Optional["ContainerAwsNodePoolConfigSshConfig"], jsii.get(self, "sshConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="taintsInput")
    def taints_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAwsNodePoolConfigTaints"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAwsNodePoolConfigTaints"]]], jsii.get(self, "taintsInput"))

    @builtins.property
    @jsii.member(jsii_name="iamInstanceProfile")
    def iam_instance_profile(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "iamInstanceProfile"))

    @iam_instance_profile.setter
    def iam_instance_profile(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1991288d5c33d7347faaa0cb20afee4051c6f4dc541e03163555d0afaeef52c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "iamInstanceProfile", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceType")
    def instance_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceType"))

    @instance_type.setter
    def instance_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3ab6b46899f0c0b62b2717d8847e3d51471e7c07cf3217a44cbe8fdaadabf87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca6d38b40604fe88e56c340006f3c8545add9a4c4ee7184317b1cc78f20c3bc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityGroupIds")
    def security_group_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "securityGroupIds"))

    @security_group_ids.setter
    def security_group_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a9c669a5c925262c99aab9f17adc5689853f05a2404060b0275cbef0a71055f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroupIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61e4f802a4bdef352bc30714f0525a0a5ae01a7e5497ac8cea3053b2c19bbfba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ContainerAwsNodePoolConfigA]:
        return typing.cast(typing.Optional[ContainerAwsNodePoolConfigA], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerAwsNodePoolConfigA],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99f66c5ec88c382d19955dd978b19f2727ea6249c6ebee962aefbbc23a6ba1c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAwsNodePool.ContainerAwsNodePoolConfigAutoscalingMetricsCollection",
    jsii_struct_bases=[],
    name_mapping={"granularity": "granularity", "metrics": "metrics"},
)
class ContainerAwsNodePoolConfigAutoscalingMetricsCollection:
    def __init__(
        self,
        *,
        granularity: builtins.str,
        metrics: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param granularity: The frequency at which EC2 Auto Scaling sends aggregated data to AWS CloudWatch. The only valid value is "1Minute". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#granularity ContainerAwsNodePool#granularity}
        :param metrics: The metrics to enable. For a list of valid metrics, see https://docs.aws.amazon.com/autoscaling/ec2/APIReference/API_EnableMetricsCollection.html. If you specify granularity and don't specify any metrics, all metrics are enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#metrics ContainerAwsNodePool#metrics}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__deb1d7e895a22cd03558840c0e7f12fb1743b1ba71d569e73064a42f2c524fb4)
            check_type(argname="argument granularity", value=granularity, expected_type=type_hints["granularity"])
            check_type(argname="argument metrics", value=metrics, expected_type=type_hints["metrics"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "granularity": granularity,
        }
        if metrics is not None:
            self._values["metrics"] = metrics

    @builtins.property
    def granularity(self) -> builtins.str:
        '''The frequency at which EC2 Auto Scaling sends aggregated data to AWS CloudWatch. The only valid value is "1Minute".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#granularity ContainerAwsNodePool#granularity}
        '''
        result = self._values.get("granularity")
        assert result is not None, "Required property 'granularity' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def metrics(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The metrics to enable.

        For a list of valid metrics, see https://docs.aws.amazon.com/autoscaling/ec2/APIReference/API_EnableMetricsCollection.html. If you specify granularity and don't specify any metrics, all metrics are enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#metrics ContainerAwsNodePool#metrics}
        '''
        result = self._values.get("metrics")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAwsNodePoolConfigAutoscalingMetricsCollection(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAwsNodePoolConfigAutoscalingMetricsCollectionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAwsNodePool.ContainerAwsNodePoolConfigAutoscalingMetricsCollectionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0fbcf81f53b06429230e8b8f93327fa3638feb08fa144ce6b16e569cfacb9bcb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMetrics")
    def reset_metrics(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetrics", []))

    @builtins.property
    @jsii.member(jsii_name="granularityInput")
    def granularity_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "granularityInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsInput")
    def metrics_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "metricsInput"))

    @builtins.property
    @jsii.member(jsii_name="granularity")
    def granularity(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "granularity"))

    @granularity.setter
    def granularity(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__448e025fc50c0597f8f043c454c7d9f7483bc1295c1f8969c9199135af2a4b34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "granularity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metrics")
    def metrics(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "metrics"))

    @metrics.setter
    def metrics(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6af408e8652815d86757b4157803b550eae1f53fb7ebc9d4644fe86acb036784)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metrics", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ContainerAwsNodePoolConfigAutoscalingMetricsCollection]:
        return typing.cast(typing.Optional[ContainerAwsNodePoolConfigAutoscalingMetricsCollection], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerAwsNodePoolConfigAutoscalingMetricsCollection],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f04a6581725a8ec6232580249410cd04aaad53c7697831f54bfa235d6008d369)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAwsNodePool.ContainerAwsNodePoolConfigConfigEncryption",
    jsii_struct_bases=[],
    name_mapping={"kms_key_arn": "kmsKeyArn"},
)
class ContainerAwsNodePoolConfigConfigEncryption:
    def __init__(self, *, kms_key_arn: builtins.str) -> None:
        '''
        :param kms_key_arn: The ARN of the AWS KMS key used to encrypt node pool configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#kms_key_arn ContainerAwsNodePool#kms_key_arn}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c554313de55e128b926c59f160b77fc4f7a9b4428763a0df34093df18baa21a3)
            check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "kms_key_arn": kms_key_arn,
        }

    @builtins.property
    def kms_key_arn(self) -> builtins.str:
        '''The ARN of the AWS KMS key used to encrypt node pool configuration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#kms_key_arn ContainerAwsNodePool#kms_key_arn}
        '''
        result = self._values.get("kms_key_arn")
        assert result is not None, "Required property 'kms_key_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAwsNodePoolConfigConfigEncryption(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAwsNodePoolConfigConfigEncryptionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAwsNodePool.ContainerAwsNodePoolConfigConfigEncryptionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__781193cfaf5643ed444727f70f1645c1894b3027a1d25c5909522b69cc2e389f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="kmsKeyArnInput")
    def kms_key_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyArnInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyArn")
    def kms_key_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyArn"))

    @kms_key_arn.setter
    def kms_key_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__354f82e8d502084f1231b2c1fe855bf70ff415c67f35bcdae48736d6f95d81d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ContainerAwsNodePoolConfigConfigEncryption]:
        return typing.cast(typing.Optional[ContainerAwsNodePoolConfigConfigEncryption], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerAwsNodePoolConfigConfigEncryption],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83904fcf635de382cf76de8f07d2f963b6385e13edc1abd32827fbcf97f28b52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAwsNodePool.ContainerAwsNodePoolConfigProxyConfig",
    jsii_struct_bases=[],
    name_mapping={"secret_arn": "secretArn", "secret_version": "secretVersion"},
)
class ContainerAwsNodePoolConfigProxyConfig:
    def __init__(
        self,
        *,
        secret_arn: builtins.str,
        secret_version: builtins.str,
    ) -> None:
        '''
        :param secret_arn: The ARN of the AWS Secret Manager secret that contains the HTTP(S) proxy configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#secret_arn ContainerAwsNodePool#secret_arn}
        :param secret_version: The version string of the AWS Secret Manager secret that contains the HTTP(S) proxy configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#secret_version ContainerAwsNodePool#secret_version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0066d3ec0ce572ab0afe4cf849bf2db374ac872c56d7ef5bc2ed5e2b32b4fc6)
            check_type(argname="argument secret_arn", value=secret_arn, expected_type=type_hints["secret_arn"])
            check_type(argname="argument secret_version", value=secret_version, expected_type=type_hints["secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_arn": secret_arn,
            "secret_version": secret_version,
        }

    @builtins.property
    def secret_arn(self) -> builtins.str:
        '''The ARN of the AWS Secret Manager secret that contains the HTTP(S) proxy configuration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#secret_arn ContainerAwsNodePool#secret_arn}
        '''
        result = self._values.get("secret_arn")
        assert result is not None, "Required property 'secret_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secret_version(self) -> builtins.str:
        '''The version string of the AWS Secret Manager secret that contains the HTTP(S) proxy configuration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#secret_version ContainerAwsNodePool#secret_version}
        '''
        result = self._values.get("secret_version")
        assert result is not None, "Required property 'secret_version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAwsNodePoolConfigProxyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAwsNodePoolConfigProxyConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAwsNodePool.ContainerAwsNodePoolConfigProxyConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2f0d9faed265054fb89eab2f56c455b1a3b359d4aa8456da2807080547b7bf14)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="secretArnInput")
    def secret_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretArnInput"))

    @builtins.property
    @jsii.member(jsii_name="secretVersionInput")
    def secret_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="secretArn")
    def secret_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretArn"))

    @secret_arn.setter
    def secret_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba95f8e0c140159beb9eab0cbba882f5659b402383ad6978f54a9dedee7a6b93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretVersion")
    def secret_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretVersion"))

    @secret_version.setter
    def secret_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9e6fec33335eddcae03e3bec49aba4c8ea7bf2fede1c584b2365f306c02fcb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ContainerAwsNodePoolConfigProxyConfig]:
        return typing.cast(typing.Optional[ContainerAwsNodePoolConfigProxyConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerAwsNodePoolConfigProxyConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5f5c9dec546227f98e8030ebf08ff57d60af63b95522c83a9f511341b2f8e96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAwsNodePool.ContainerAwsNodePoolConfigRootVolume",
    jsii_struct_bases=[],
    name_mapping={
        "iops": "iops",
        "kms_key_arn": "kmsKeyArn",
        "size_gib": "sizeGib",
        "throughput": "throughput",
        "volume_type": "volumeType",
    },
)
class ContainerAwsNodePoolConfigRootVolume:
    def __init__(
        self,
        *,
        iops: typing.Optional[jsii.Number] = None,
        kms_key_arn: typing.Optional[builtins.str] = None,
        size_gib: typing.Optional[jsii.Number] = None,
        throughput: typing.Optional[jsii.Number] = None,
        volume_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param iops: Optional. The number of I/O operations per second (IOPS) to provision for GP3 volume. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#iops ContainerAwsNodePool#iops}
        :param kms_key_arn: Optional. The Amazon Resource Name (ARN) of the Customer Managed Key (CMK) used to encrypt AWS EBS volumes. If not specified, the default Amazon managed key associated to the AWS region where this cluster runs will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#kms_key_arn ContainerAwsNodePool#kms_key_arn}
        :param size_gib: Optional. The size of the volume, in GiBs. When unspecified, a default value is provided. See the specific reference in the parent resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#size_gib ContainerAwsNodePool#size_gib}
        :param throughput: Optional. The throughput to provision for the volume, in MiB/s. Only valid if the volume type is GP3. If volume type is gp3 and throughput is not specified, the throughput will defaults to 125. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#throughput ContainerAwsNodePool#throughput}
        :param volume_type: Optional. Type of the EBS volume. When unspecified, it defaults to GP2 volume. Possible values: VOLUME_TYPE_UNSPECIFIED, GP2, GP3. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#volume_type ContainerAwsNodePool#volume_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__334be749685ed3f67f961d8e566d16c65a93d333b69b9eceddb9a95a1ddd23a7)
            check_type(argname="argument iops", value=iops, expected_type=type_hints["iops"])
            check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
            check_type(argname="argument size_gib", value=size_gib, expected_type=type_hints["size_gib"])
            check_type(argname="argument throughput", value=throughput, expected_type=type_hints["throughput"])
            check_type(argname="argument volume_type", value=volume_type, expected_type=type_hints["volume_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if iops is not None:
            self._values["iops"] = iops
        if kms_key_arn is not None:
            self._values["kms_key_arn"] = kms_key_arn
        if size_gib is not None:
            self._values["size_gib"] = size_gib
        if throughput is not None:
            self._values["throughput"] = throughput
        if volume_type is not None:
            self._values["volume_type"] = volume_type

    @builtins.property
    def iops(self) -> typing.Optional[jsii.Number]:
        '''Optional. The number of I/O operations per second (IOPS) to provision for GP3 volume.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#iops ContainerAwsNodePool#iops}
        '''
        result = self._values.get("iops")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def kms_key_arn(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The Amazon Resource Name (ARN) of the Customer Managed Key (CMK) used to encrypt AWS EBS volumes. If not specified, the default Amazon managed key associated to the AWS region where this cluster runs will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#kms_key_arn ContainerAwsNodePool#kms_key_arn}
        '''
        result = self._values.get("kms_key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def size_gib(self) -> typing.Optional[jsii.Number]:
        '''Optional.

        The size of the volume, in GiBs. When unspecified, a default value is provided. See the specific reference in the parent resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#size_gib ContainerAwsNodePool#size_gib}
        '''
        result = self._values.get("size_gib")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def throughput(self) -> typing.Optional[jsii.Number]:
        '''Optional.

        The throughput to provision for the volume, in MiB/s. Only valid if the volume type is GP3. If volume type is gp3 and throughput is not specified, the throughput will defaults to 125.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#throughput ContainerAwsNodePool#throughput}
        '''
        result = self._values.get("throughput")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def volume_type(self) -> typing.Optional[builtins.str]:
        '''Optional. Type of the EBS volume. When unspecified, it defaults to GP2 volume. Possible values: VOLUME_TYPE_UNSPECIFIED, GP2, GP3.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#volume_type ContainerAwsNodePool#volume_type}
        '''
        result = self._values.get("volume_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAwsNodePoolConfigRootVolume(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAwsNodePoolConfigRootVolumeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAwsNodePool.ContainerAwsNodePoolConfigRootVolumeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7fcc67b4b303b328b7bef4214381d01eaf992f7ddbcd7ddc2665460e961480cc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIops")
    def reset_iops(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIops", []))

    @jsii.member(jsii_name="resetKmsKeyArn")
    def reset_kms_key_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyArn", []))

    @jsii.member(jsii_name="resetSizeGib")
    def reset_size_gib(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSizeGib", []))

    @jsii.member(jsii_name="resetThroughput")
    def reset_throughput(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThroughput", []))

    @jsii.member(jsii_name="resetVolumeType")
    def reset_volume_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVolumeType", []))

    @builtins.property
    @jsii.member(jsii_name="iopsInput")
    def iops_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "iopsInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyArnInput")
    def kms_key_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyArnInput"))

    @builtins.property
    @jsii.member(jsii_name="sizeGibInput")
    def size_gib_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sizeGibInput"))

    @builtins.property
    @jsii.member(jsii_name="throughputInput")
    def throughput_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "throughputInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeTypeInput")
    def volume_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "volumeTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="iops")
    def iops(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "iops"))

    @iops.setter
    def iops(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28394e5e6f5736e42bffec835c98430a71dd871f486d6950d51465c8bcac11a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "iops", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyArn")
    def kms_key_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyArn"))

    @kms_key_arn.setter
    def kms_key_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c576347caf8f79ca5988052768ceb8de7184f854c49e0b6fe67f65cc8e787c7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sizeGib")
    def size_gib(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sizeGib"))

    @size_gib.setter
    def size_gib(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04c64586c9f1af23a0a6b4100c033305f624beb18ba002616237fa4798e80b4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sizeGib", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="throughput")
    def throughput(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "throughput"))

    @throughput.setter
    def throughput(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__771a14c8995cabc15f1a0318e36bff6b353e223262ad2f650ae4a56f490f78f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "throughput", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="volumeType")
    def volume_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "volumeType"))

    @volume_type.setter
    def volume_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9a67bf4e1875be096a395f9df1930064469ea5bf2f8f34f6c27318dee44ac13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumeType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ContainerAwsNodePoolConfigRootVolume]:
        return typing.cast(typing.Optional[ContainerAwsNodePoolConfigRootVolume], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerAwsNodePoolConfigRootVolume],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8d52daab49f97548feef3de24d91b02021803652af55b75fb811d4b29d9a5e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAwsNodePool.ContainerAwsNodePoolConfigSshConfig",
    jsii_struct_bases=[],
    name_mapping={"ec2_key_pair": "ec2KeyPair"},
)
class ContainerAwsNodePoolConfigSshConfig:
    def __init__(self, *, ec2_key_pair: builtins.str) -> None:
        '''
        :param ec2_key_pair: The name of the EC2 key pair used to login into cluster machines. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#ec2_key_pair ContainerAwsNodePool#ec2_key_pair}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40e52343a801bf734b11f5192d5e6785a58e18350698bb7f247d61ed21e7c6eb)
            check_type(argname="argument ec2_key_pair", value=ec2_key_pair, expected_type=type_hints["ec2_key_pair"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ec2_key_pair": ec2_key_pair,
        }

    @builtins.property
    def ec2_key_pair(self) -> builtins.str:
        '''The name of the EC2 key pair used to login into cluster machines.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#ec2_key_pair ContainerAwsNodePool#ec2_key_pair}
        '''
        result = self._values.get("ec2_key_pair")
        assert result is not None, "Required property 'ec2_key_pair' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAwsNodePoolConfigSshConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAwsNodePoolConfigSshConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAwsNodePool.ContainerAwsNodePoolConfigSshConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c999c5401efaad70419c5e42c5a0ed867f39b9c89d7560395cc10f3d48f7216)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="ec2KeyPairInput")
    def ec2_key_pair_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ec2KeyPairInput"))

    @builtins.property
    @jsii.member(jsii_name="ec2KeyPair")
    def ec2_key_pair(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ec2KeyPair"))

    @ec2_key_pair.setter
    def ec2_key_pair(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e42a20b399c0be91460a400178e315cac0a9f6f817567b1fdf9447b003160d9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ec2KeyPair", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ContainerAwsNodePoolConfigSshConfig]:
        return typing.cast(typing.Optional[ContainerAwsNodePoolConfigSshConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerAwsNodePoolConfigSshConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1e4f53a13b8ab596c36928cb0fef196bbf1571fc91de138eb4de49f8864423a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAwsNodePool.ContainerAwsNodePoolConfigTaints",
    jsii_struct_bases=[],
    name_mapping={"effect": "effect", "key": "key", "value": "value"},
)
class ContainerAwsNodePoolConfigTaints:
    def __init__(
        self,
        *,
        effect: builtins.str,
        key: builtins.str,
        value: builtins.str,
    ) -> None:
        '''
        :param effect: The taint effect. Possible values: EFFECT_UNSPECIFIED, NO_SCHEDULE, PREFER_NO_SCHEDULE, NO_EXECUTE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#effect ContainerAwsNodePool#effect}
        :param key: Key for the taint. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#key ContainerAwsNodePool#key}
        :param value: Value for the taint. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#value ContainerAwsNodePool#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb06d30fdf866d69edbe6adef18ad261070f9850079463f929d3349bd4d5d1aa)
            check_type(argname="argument effect", value=effect, expected_type=type_hints["effect"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "effect": effect,
            "key": key,
            "value": value,
        }

    @builtins.property
    def effect(self) -> builtins.str:
        '''The taint effect. Possible values: EFFECT_UNSPECIFIED, NO_SCHEDULE, PREFER_NO_SCHEDULE, NO_EXECUTE.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#effect ContainerAwsNodePool#effect}
        '''
        result = self._values.get("effect")
        assert result is not None, "Required property 'effect' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def key(self) -> builtins.str:
        '''Key for the taint.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#key ContainerAwsNodePool#key}
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Value for the taint.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#value ContainerAwsNodePool#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAwsNodePoolConfigTaints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAwsNodePoolConfigTaintsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAwsNodePool.ContainerAwsNodePoolConfigTaintsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a27effe161c3280640f0db7ca5777fc84f5f448e80602a578b3d7f80fd6e2279)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ContainerAwsNodePoolConfigTaintsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__442715afe04ff3d24e4de10cba3d789a11245b054685711181f331618f1cdfc1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerAwsNodePoolConfigTaintsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cd588ccae49ac37843e5c04011101b16384b2d7f735e32a9647ecb525bd5a22)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca5757088c7ce4ad21fea18b2f02b934b9ebd5397c585eca5c518f4f71d5ff42)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e0d64a2236a3de8298f7c67e2ecf63c5b3eb884d11e857872db491c53cb3dee7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAwsNodePoolConfigTaints]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAwsNodePoolConfigTaints]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAwsNodePoolConfigTaints]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4d4c65f486eea79507789bebf7f4962dbcef5271cffc575d69bef913df49387)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAwsNodePoolConfigTaintsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAwsNodePool.ContainerAwsNodePoolConfigTaintsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a265acdd671124684979588f546bd593a0ced62ab85d502e10aacccd09fa302a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

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
            type_hints = typing.get_type_hints(_typecheckingstub__2efa028cc5143b2e91a6ae895184c64aaa66b0d9d54653a2d9fecff4e670e913)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "effect", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5529b4d8c436190b8fcb7e40f1420235207e835cde11b231804274d1e5ab4b89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2dae53b5bae16f90269f31f031e9f7382e32db68800540ad5bc7d6d5d7e06714)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAwsNodePoolConfigTaints]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAwsNodePoolConfigTaints]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAwsNodePoolConfigTaints]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7293b211621a38fb5b08d6dea908512005a2e3e30fa30bb04e429d42cc287421)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAwsNodePool.ContainerAwsNodePoolKubeletConfig",
    jsii_struct_bases=[],
    name_mapping={
        "cpu_cfs_quota": "cpuCfsQuota",
        "cpu_cfs_quota_period": "cpuCfsQuotaPeriod",
        "cpu_manager_policy": "cpuManagerPolicy",
        "pod_pids_limit": "podPidsLimit",
    },
)
class ContainerAwsNodePoolKubeletConfig:
    def __init__(
        self,
        *,
        cpu_cfs_quota: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        cpu_cfs_quota_period: typing.Optional[builtins.str] = None,
        cpu_manager_policy: typing.Optional[builtins.str] = None,
        pod_pids_limit: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param cpu_cfs_quota: Whether or not to enable CPU CFS quota. Defaults to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#cpu_cfs_quota ContainerAwsNodePool#cpu_cfs_quota}
        :param cpu_cfs_quota_period: Optional. The CPU CFS quota period to use for the node. Defaults to "100ms". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#cpu_cfs_quota_period ContainerAwsNodePool#cpu_cfs_quota_period}
        :param cpu_manager_policy: The CpuManagerPolicy to use for the node. Defaults to "none". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#cpu_manager_policy ContainerAwsNodePool#cpu_manager_policy}
        :param pod_pids_limit: Optional. The maximum number of PIDs in each pod running on the node. The limit scales automatically based on underlying machine size if left unset. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#pod_pids_limit ContainerAwsNodePool#pod_pids_limit}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f35bf4eeb5ee82688c0bf7f2170bdd4ab2b96b0b743e5598a513a5f41a52656)
            check_type(argname="argument cpu_cfs_quota", value=cpu_cfs_quota, expected_type=type_hints["cpu_cfs_quota"])
            check_type(argname="argument cpu_cfs_quota_period", value=cpu_cfs_quota_period, expected_type=type_hints["cpu_cfs_quota_period"])
            check_type(argname="argument cpu_manager_policy", value=cpu_manager_policy, expected_type=type_hints["cpu_manager_policy"])
            check_type(argname="argument pod_pids_limit", value=pod_pids_limit, expected_type=type_hints["pod_pids_limit"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cpu_cfs_quota is not None:
            self._values["cpu_cfs_quota"] = cpu_cfs_quota
        if cpu_cfs_quota_period is not None:
            self._values["cpu_cfs_quota_period"] = cpu_cfs_quota_period
        if cpu_manager_policy is not None:
            self._values["cpu_manager_policy"] = cpu_manager_policy
        if pod_pids_limit is not None:
            self._values["pod_pids_limit"] = pod_pids_limit

    @builtins.property
    def cpu_cfs_quota(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether or not to enable CPU CFS quota. Defaults to true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#cpu_cfs_quota ContainerAwsNodePool#cpu_cfs_quota}
        '''
        result = self._values.get("cpu_cfs_quota")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def cpu_cfs_quota_period(self) -> typing.Optional[builtins.str]:
        '''Optional. The CPU CFS quota period to use for the node. Defaults to "100ms".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#cpu_cfs_quota_period ContainerAwsNodePool#cpu_cfs_quota_period}
        '''
        result = self._values.get("cpu_cfs_quota_period")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cpu_manager_policy(self) -> typing.Optional[builtins.str]:
        '''The CpuManagerPolicy to use for the node. Defaults to "none".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#cpu_manager_policy ContainerAwsNodePool#cpu_manager_policy}
        '''
        result = self._values.get("cpu_manager_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pod_pids_limit(self) -> typing.Optional[jsii.Number]:
        '''Optional.

        The maximum number of PIDs in each pod running on the node. The limit scales automatically based on underlying machine size if left unset.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#pod_pids_limit ContainerAwsNodePool#pod_pids_limit}
        '''
        result = self._values.get("pod_pids_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAwsNodePoolKubeletConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAwsNodePoolKubeletConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAwsNodePool.ContainerAwsNodePoolKubeletConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b7ad81942418c80dd65aa5a39597af7acb7c24515c97ea95d841affa1a7abf4d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCpuCfsQuota")
    def reset_cpu_cfs_quota(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpuCfsQuota", []))

    @jsii.member(jsii_name="resetCpuCfsQuotaPeriod")
    def reset_cpu_cfs_quota_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpuCfsQuotaPeriod", []))

    @jsii.member(jsii_name="resetCpuManagerPolicy")
    def reset_cpu_manager_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpuManagerPolicy", []))

    @jsii.member(jsii_name="resetPodPidsLimit")
    def reset_pod_pids_limit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPodPidsLimit", []))

    @builtins.property
    @jsii.member(jsii_name="cpuCfsQuotaInput")
    def cpu_cfs_quota_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "cpuCfsQuotaInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuCfsQuotaPeriodInput")
    def cpu_cfs_quota_period_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cpuCfsQuotaPeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuManagerPolicyInput")
    def cpu_manager_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cpuManagerPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="podPidsLimitInput")
    def pod_pids_limit_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "podPidsLimitInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuCfsQuota")
    def cpu_cfs_quota(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "cpuCfsQuota"))

    @cpu_cfs_quota.setter
    def cpu_cfs_quota(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e4e0476cf692a10c7bd5788f86353e48191f5f0ee85cd728425e7a3f9981038)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuCfsQuota", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cpuCfsQuotaPeriod")
    def cpu_cfs_quota_period(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cpuCfsQuotaPeriod"))

    @cpu_cfs_quota_period.setter
    def cpu_cfs_quota_period(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2aec63e77377163de8e0af446a0d5d4cab87f5e6fb53652938c5c4255961c631)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuCfsQuotaPeriod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cpuManagerPolicy")
    def cpu_manager_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cpuManagerPolicy"))

    @cpu_manager_policy.setter
    def cpu_manager_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__525f571ecd9e79f1eeb321ea0add2d443a12c4f4ef79d7dbde9f3b61fc4b01a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuManagerPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="podPidsLimit")
    def pod_pids_limit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "podPidsLimit"))

    @pod_pids_limit.setter
    def pod_pids_limit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fea174dec0dc4c440762b5203b4d0015f3f20dad9441b229f75cce9fb0903516)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "podPidsLimit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ContainerAwsNodePoolKubeletConfig]:
        return typing.cast(typing.Optional[ContainerAwsNodePoolKubeletConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerAwsNodePoolKubeletConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2aae1d5eb2af73686b966935a8af79f8f1ecba0c632619eb6161f5e60b9a3f30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAwsNodePool.ContainerAwsNodePoolManagement",
    jsii_struct_bases=[],
    name_mapping={"auto_repair": "autoRepair"},
)
class ContainerAwsNodePoolManagement:
    def __init__(
        self,
        *,
        auto_repair: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param auto_repair: Optional. Whether or not the nodes will be automatically repaired. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#auto_repair ContainerAwsNodePool#auto_repair}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cad01253f11ea035595e73c4678cd759a57012b790cab724a4f27da04aaf629)
            check_type(argname="argument auto_repair", value=auto_repair, expected_type=type_hints["auto_repair"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auto_repair is not None:
            self._values["auto_repair"] = auto_repair

    @builtins.property
    def auto_repair(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional. Whether or not the nodes will be automatically repaired.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#auto_repair ContainerAwsNodePool#auto_repair}
        '''
        result = self._values.get("auto_repair")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAwsNodePoolManagement(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAwsNodePoolManagementOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAwsNodePool.ContainerAwsNodePoolManagementOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__62fdafb8d5fa278a6983b1c0fc2a8ac865bb0d1e24de2df19b992a1a76a9b65d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a8b6fc90ca0b5e8c39e836b3bf6856243564d3526c024310a50ba8f79424c45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoRepair", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ContainerAwsNodePoolManagement]:
        return typing.cast(typing.Optional[ContainerAwsNodePoolManagement], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerAwsNodePoolManagement],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02cc6d213315cecd4829794112a206f34fa83d4a6043bab8dc7076e5c657b30a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAwsNodePool.ContainerAwsNodePoolMaxPodsConstraint",
    jsii_struct_bases=[],
    name_mapping={"max_pods_per_node": "maxPodsPerNode"},
)
class ContainerAwsNodePoolMaxPodsConstraint:
    def __init__(self, *, max_pods_per_node: jsii.Number) -> None:
        '''
        :param max_pods_per_node: The maximum number of pods to schedule on a single node. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#max_pods_per_node ContainerAwsNodePool#max_pods_per_node}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08b69280c5452cbf128a2fdb997b0b33521e8992f0ce51a096870c8d97abdf37)
            check_type(argname="argument max_pods_per_node", value=max_pods_per_node, expected_type=type_hints["max_pods_per_node"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "max_pods_per_node": max_pods_per_node,
        }

    @builtins.property
    def max_pods_per_node(self) -> jsii.Number:
        '''The maximum number of pods to schedule on a single node.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#max_pods_per_node ContainerAwsNodePool#max_pods_per_node}
        '''
        result = self._values.get("max_pods_per_node")
        assert result is not None, "Required property 'max_pods_per_node' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAwsNodePoolMaxPodsConstraint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAwsNodePoolMaxPodsConstraintOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAwsNodePool.ContainerAwsNodePoolMaxPodsConstraintOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f176cf52faa43665bb9833836517122864819a64e784b565bd156ccb2902fee)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2b9c799f32b177069cf8a67b671b6301606fc60f1e739da9aaec974e6d3541e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxPodsPerNode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ContainerAwsNodePoolMaxPodsConstraint]:
        return typing.cast(typing.Optional[ContainerAwsNodePoolMaxPodsConstraint], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerAwsNodePoolMaxPodsConstraint],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c089e815abdf00ee29b6209bf785014763acc1f58d182a5636f21541302b3390)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAwsNodePool.ContainerAwsNodePoolTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ContainerAwsNodePoolTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#create ContainerAwsNodePool#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#delete ContainerAwsNodePool#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#update ContainerAwsNodePool#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d409cd4dcb787c5523a4ee4e33cd697f86577c624f67924310249fdd2366d0da)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#create ContainerAwsNodePool#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#delete ContainerAwsNodePool#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#update ContainerAwsNodePool#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAwsNodePoolTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAwsNodePoolTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAwsNodePool.ContainerAwsNodePoolTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c3620a7f4fdd0d2e4e5e9bd44058faa176c7a6e0d17990cbbdab5524e316b9f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__19aaef48b8255e8878f8476d29b2a719a4eb1fb31c4c7a99c3044f82d56b85b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d923ad6d711fd18092c9c0012fd7790ab37b88cf5e834205186cfc9a0e173f7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9bfbc834edd71b343894bca2242125d78c3907322abfaa11930eb5cd2ae4a42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAwsNodePoolTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAwsNodePoolTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAwsNodePoolTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37ea1ec61dd40c30ad7125049a11b755eb5e3ce7c6f39a56ba6482f52c08fbe3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAwsNodePool.ContainerAwsNodePoolUpdateSettings",
    jsii_struct_bases=[],
    name_mapping={"surge_settings": "surgeSettings"},
)
class ContainerAwsNodePoolUpdateSettings:
    def __init__(
        self,
        *,
        surge_settings: typing.Optional[typing.Union["ContainerAwsNodePoolUpdateSettingsSurgeSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param surge_settings: surge_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#surge_settings ContainerAwsNodePool#surge_settings}
        '''
        if isinstance(surge_settings, dict):
            surge_settings = ContainerAwsNodePoolUpdateSettingsSurgeSettings(**surge_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d86d75b65d3f7097ce493ee1d820410489aea30032b8ce645c46e4d312765294)
            check_type(argname="argument surge_settings", value=surge_settings, expected_type=type_hints["surge_settings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if surge_settings is not None:
            self._values["surge_settings"] = surge_settings

    @builtins.property
    def surge_settings(
        self,
    ) -> typing.Optional["ContainerAwsNodePoolUpdateSettingsSurgeSettings"]:
        '''surge_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#surge_settings ContainerAwsNodePool#surge_settings}
        '''
        result = self._values.get("surge_settings")
        return typing.cast(typing.Optional["ContainerAwsNodePoolUpdateSettingsSurgeSettings"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAwsNodePoolUpdateSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAwsNodePoolUpdateSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAwsNodePool.ContainerAwsNodePoolUpdateSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ba2b030e1095d9ec18371d7b7e484d2e7c013ada3fc1ff9e14c1a375aa58084)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSurgeSettings")
    def put_surge_settings(
        self,
        *,
        max_surge: typing.Optional[jsii.Number] = None,
        max_unavailable: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_surge: Optional. The maximum number of nodes that can be created beyond the current size of the node pool during the update process. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#max_surge ContainerAwsNodePool#max_surge}
        :param max_unavailable: Optional. The maximum number of nodes that can be simultaneously unavailable during the update process. A node is considered unavailable if its status is not Ready. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#max_unavailable ContainerAwsNodePool#max_unavailable}
        '''
        value = ContainerAwsNodePoolUpdateSettingsSurgeSettings(
            max_surge=max_surge, max_unavailable=max_unavailable
        )

        return typing.cast(None, jsii.invoke(self, "putSurgeSettings", [value]))

    @jsii.member(jsii_name="resetSurgeSettings")
    def reset_surge_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSurgeSettings", []))

    @builtins.property
    @jsii.member(jsii_name="surgeSettings")
    def surge_settings(
        self,
    ) -> "ContainerAwsNodePoolUpdateSettingsSurgeSettingsOutputReference":
        return typing.cast("ContainerAwsNodePoolUpdateSettingsSurgeSettingsOutputReference", jsii.get(self, "surgeSettings"))

    @builtins.property
    @jsii.member(jsii_name="surgeSettingsInput")
    def surge_settings_input(
        self,
    ) -> typing.Optional["ContainerAwsNodePoolUpdateSettingsSurgeSettings"]:
        return typing.cast(typing.Optional["ContainerAwsNodePoolUpdateSettingsSurgeSettings"], jsii.get(self, "surgeSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ContainerAwsNodePoolUpdateSettings]:
        return typing.cast(typing.Optional[ContainerAwsNodePoolUpdateSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerAwsNodePoolUpdateSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ad7dbe743b5777398ce7c27c276a5d63a61d5495ce3078d3ec8600bac5bb00c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAwsNodePool.ContainerAwsNodePoolUpdateSettingsSurgeSettings",
    jsii_struct_bases=[],
    name_mapping={"max_surge": "maxSurge", "max_unavailable": "maxUnavailable"},
)
class ContainerAwsNodePoolUpdateSettingsSurgeSettings:
    def __init__(
        self,
        *,
        max_surge: typing.Optional[jsii.Number] = None,
        max_unavailable: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_surge: Optional. The maximum number of nodes that can be created beyond the current size of the node pool during the update process. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#max_surge ContainerAwsNodePool#max_surge}
        :param max_unavailable: Optional. The maximum number of nodes that can be simultaneously unavailable during the update process. A node is considered unavailable if its status is not Ready. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#max_unavailable ContainerAwsNodePool#max_unavailable}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41703609ab0578e2de458a89e4a7e6834ded317c335d2c7e6398b4567cb1d4ae)
            check_type(argname="argument max_surge", value=max_surge, expected_type=type_hints["max_surge"])
            check_type(argname="argument max_unavailable", value=max_unavailable, expected_type=type_hints["max_unavailable"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_surge is not None:
            self._values["max_surge"] = max_surge
        if max_unavailable is not None:
            self._values["max_unavailable"] = max_unavailable

    @builtins.property
    def max_surge(self) -> typing.Optional[jsii.Number]:
        '''Optional.

        The maximum number of nodes that can be created beyond the current size of the node pool during the update process.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#max_surge ContainerAwsNodePool#max_surge}
        '''
        result = self._values.get("max_surge")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_unavailable(self) -> typing.Optional[jsii.Number]:
        '''Optional.

        The maximum number of nodes that can be simultaneously unavailable during the update process. A node is considered unavailable if its status is not Ready.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_node_pool#max_unavailable ContainerAwsNodePool#max_unavailable}
        '''
        result = self._values.get("max_unavailable")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAwsNodePoolUpdateSettingsSurgeSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAwsNodePoolUpdateSettingsSurgeSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAwsNodePool.ContainerAwsNodePoolUpdateSettingsSurgeSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__18125689e51741fdb2c433361295259b212102b458b18fdd250375a722072715)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMaxSurge")
    def reset_max_surge(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxSurge", []))

    @jsii.member(jsii_name="resetMaxUnavailable")
    def reset_max_unavailable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxUnavailable", []))

    @builtins.property
    @jsii.member(jsii_name="maxSurgeInput")
    def max_surge_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxSurgeInput"))

    @builtins.property
    @jsii.member(jsii_name="maxUnavailableInput")
    def max_unavailable_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxUnavailableInput"))

    @builtins.property
    @jsii.member(jsii_name="maxSurge")
    def max_surge(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxSurge"))

    @max_surge.setter
    def max_surge(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59fc3873e53f9fd9be1349ded263591cb3eae05d1daf92f4da02fe04f45facf1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxSurge", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxUnavailable")
    def max_unavailable(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxUnavailable"))

    @max_unavailable.setter
    def max_unavailable(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3743dc3459c5bdac1ccf017eb68ede31972f29ae0499c1329d415ed38549d92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxUnavailable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ContainerAwsNodePoolUpdateSettingsSurgeSettings]:
        return typing.cast(typing.Optional[ContainerAwsNodePoolUpdateSettingsSurgeSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerAwsNodePoolUpdateSettingsSurgeSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8baabb3cfb9f40f50ea106d93060ee7188610880fc65440654760df838b2352e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ContainerAwsNodePool",
    "ContainerAwsNodePoolAutoscaling",
    "ContainerAwsNodePoolAutoscalingOutputReference",
    "ContainerAwsNodePoolConfig",
    "ContainerAwsNodePoolConfigA",
    "ContainerAwsNodePoolConfigAOutputReference",
    "ContainerAwsNodePoolConfigAutoscalingMetricsCollection",
    "ContainerAwsNodePoolConfigAutoscalingMetricsCollectionOutputReference",
    "ContainerAwsNodePoolConfigConfigEncryption",
    "ContainerAwsNodePoolConfigConfigEncryptionOutputReference",
    "ContainerAwsNodePoolConfigProxyConfig",
    "ContainerAwsNodePoolConfigProxyConfigOutputReference",
    "ContainerAwsNodePoolConfigRootVolume",
    "ContainerAwsNodePoolConfigRootVolumeOutputReference",
    "ContainerAwsNodePoolConfigSshConfig",
    "ContainerAwsNodePoolConfigSshConfigOutputReference",
    "ContainerAwsNodePoolConfigTaints",
    "ContainerAwsNodePoolConfigTaintsList",
    "ContainerAwsNodePoolConfigTaintsOutputReference",
    "ContainerAwsNodePoolKubeletConfig",
    "ContainerAwsNodePoolKubeletConfigOutputReference",
    "ContainerAwsNodePoolManagement",
    "ContainerAwsNodePoolManagementOutputReference",
    "ContainerAwsNodePoolMaxPodsConstraint",
    "ContainerAwsNodePoolMaxPodsConstraintOutputReference",
    "ContainerAwsNodePoolTimeouts",
    "ContainerAwsNodePoolTimeoutsOutputReference",
    "ContainerAwsNodePoolUpdateSettings",
    "ContainerAwsNodePoolUpdateSettingsOutputReference",
    "ContainerAwsNodePoolUpdateSettingsSurgeSettings",
    "ContainerAwsNodePoolUpdateSettingsSurgeSettingsOutputReference",
]

publication.publish()

def _typecheckingstub__9ad104cb8ba25f011d9c5a747e3062e01de95616d7b8d8333c2d536a182fbfa5(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    autoscaling: typing.Union[ContainerAwsNodePoolAutoscaling, typing.Dict[builtins.str, typing.Any]],
    cluster: builtins.str,
    config: typing.Union[ContainerAwsNodePoolConfigA, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    max_pods_constraint: typing.Union[ContainerAwsNodePoolMaxPodsConstraint, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    subnet_id: builtins.str,
    version: builtins.str,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    kubelet_config: typing.Optional[typing.Union[ContainerAwsNodePoolKubeletConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    management: typing.Optional[typing.Union[ContainerAwsNodePoolManagement, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ContainerAwsNodePoolTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    update_settings: typing.Optional[typing.Union[ContainerAwsNodePoolUpdateSettings, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__d1d211073115aa34c305b0ffa505ffb0dc9e3aa0ed57e2f3094fe7635dd26ed0(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b82e7d7778ad3c68bcbb5f6fe3178faedfa39d1cfe953c9d2753eec13b3f6979(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dc7565ef085be22f63f6b915b96df2ac5b66659bed1fb47f48cb421377c0d86(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e19d676fe3de3da32c30150841547cb8e51f62f1546a91bb7afbc56908c2613(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb5233a6b16bcd5a94b2149eb69c485f143ef117cd4c4b9efd948d3633e47ad1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__763849d552b8a1e2a93cb19a037277bdf5a6152647633f66bd292b464229cf71(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__387465ae57d441ae17ba01edc2d8fdb55b613964b97cc9d5d0c84ffc5870a292(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e30b5103ede4a39e1fe153416847acb7f758325c47fbc5ed3932237f41a6d2ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a52567506bfe976c6632df35807d3e9f5da4f8fa08043b1eaf6740c0cc31ee8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd64a433d527d89df9417424cb1a02825c465d00157837096d9706805e8a2c76(
    *,
    max_node_count: jsii.Number,
    min_node_count: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73e9459364640ef99580f75c9323c8459fff97206f8c21326ebe1017905c4802(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__090ea3ecbd6365c4a780e1b898942cc2bcd875eea3e52ef62d3a3543d475d23a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1af0b100f53875681d6a91bc56a078e937584f2055f55bb10702171e389feb33(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2f853f7b49dbb0b15f5db63ce210f983f2a2f79c87029a7541c036e4f761a58(
    value: typing.Optional[ContainerAwsNodePoolAutoscaling],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12b442ce3b8f6c99c96938646fa69f712da6eb1404ce878b0761ce06721b6938(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    autoscaling: typing.Union[ContainerAwsNodePoolAutoscaling, typing.Dict[builtins.str, typing.Any]],
    cluster: builtins.str,
    config: typing.Union[ContainerAwsNodePoolConfigA, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    max_pods_constraint: typing.Union[ContainerAwsNodePoolMaxPodsConstraint, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    subnet_id: builtins.str,
    version: builtins.str,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    kubelet_config: typing.Optional[typing.Union[ContainerAwsNodePoolKubeletConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    management: typing.Optional[typing.Union[ContainerAwsNodePoolManagement, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ContainerAwsNodePoolTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    update_settings: typing.Optional[typing.Union[ContainerAwsNodePoolUpdateSettings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79f3e405d986c2511257e72a2af0e3171bd60d67bf0c491cb789a74f4405be74(
    *,
    config_encryption: typing.Union[ContainerAwsNodePoolConfigConfigEncryption, typing.Dict[builtins.str, typing.Any]],
    iam_instance_profile: builtins.str,
    autoscaling_metrics_collection: typing.Optional[typing.Union[ContainerAwsNodePoolConfigAutoscalingMetricsCollection, typing.Dict[builtins.str, typing.Any]]] = None,
    instance_type: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    proxy_config: typing.Optional[typing.Union[ContainerAwsNodePoolConfigProxyConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    root_volume: typing.Optional[typing.Union[ContainerAwsNodePoolConfigRootVolume, typing.Dict[builtins.str, typing.Any]]] = None,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ssh_config: typing.Optional[typing.Union[ContainerAwsNodePoolConfigSshConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    taints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAwsNodePoolConfigTaints, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a08b76f6349bbdc9db142de3d01892c1aa2f4f235e302cf0ea858eedf02f5e8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d55709bd351472853d7d3132a1c92e1172e3acba5108bd86113961779555038(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAwsNodePoolConfigTaints, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1991288d5c33d7347faaa0cb20afee4051c6f4dc541e03163555d0afaeef52c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3ab6b46899f0c0b62b2717d8847e3d51471e7c07cf3217a44cbe8fdaadabf87(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca6d38b40604fe88e56c340006f3c8545add9a4c4ee7184317b1cc78f20c3bc0(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a9c669a5c925262c99aab9f17adc5689853f05a2404060b0275cbef0a71055f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61e4f802a4bdef352bc30714f0525a0a5ae01a7e5497ac8cea3053b2c19bbfba(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99f66c5ec88c382d19955dd978b19f2727ea6249c6ebee962aefbbc23a6ba1c6(
    value: typing.Optional[ContainerAwsNodePoolConfigA],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__deb1d7e895a22cd03558840c0e7f12fb1743b1ba71d569e73064a42f2c524fb4(
    *,
    granularity: builtins.str,
    metrics: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fbcf81f53b06429230e8b8f93327fa3638feb08fa144ce6b16e569cfacb9bcb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__448e025fc50c0597f8f043c454c7d9f7483bc1295c1f8969c9199135af2a4b34(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6af408e8652815d86757b4157803b550eae1f53fb7ebc9d4644fe86acb036784(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f04a6581725a8ec6232580249410cd04aaad53c7697831f54bfa235d6008d369(
    value: typing.Optional[ContainerAwsNodePoolConfigAutoscalingMetricsCollection],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c554313de55e128b926c59f160b77fc4f7a9b4428763a0df34093df18baa21a3(
    *,
    kms_key_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__781193cfaf5643ed444727f70f1645c1894b3027a1d25c5909522b69cc2e389f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__354f82e8d502084f1231b2c1fe855bf70ff415c67f35bcdae48736d6f95d81d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83904fcf635de382cf76de8f07d2f963b6385e13edc1abd32827fbcf97f28b52(
    value: typing.Optional[ContainerAwsNodePoolConfigConfigEncryption],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0066d3ec0ce572ab0afe4cf849bf2db374ac872c56d7ef5bc2ed5e2b32b4fc6(
    *,
    secret_arn: builtins.str,
    secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f0d9faed265054fb89eab2f56c455b1a3b359d4aa8456da2807080547b7bf14(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba95f8e0c140159beb9eab0cbba882f5659b402383ad6978f54a9dedee7a6b93(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9e6fec33335eddcae03e3bec49aba4c8ea7bf2fede1c584b2365f306c02fcb4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5f5c9dec546227f98e8030ebf08ff57d60af63b95522c83a9f511341b2f8e96(
    value: typing.Optional[ContainerAwsNodePoolConfigProxyConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__334be749685ed3f67f961d8e566d16c65a93d333b69b9eceddb9a95a1ddd23a7(
    *,
    iops: typing.Optional[jsii.Number] = None,
    kms_key_arn: typing.Optional[builtins.str] = None,
    size_gib: typing.Optional[jsii.Number] = None,
    throughput: typing.Optional[jsii.Number] = None,
    volume_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fcc67b4b303b328b7bef4214381d01eaf992f7ddbcd7ddc2665460e961480cc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28394e5e6f5736e42bffec835c98430a71dd871f486d6950d51465c8bcac11a2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c576347caf8f79ca5988052768ceb8de7184f854c49e0b6fe67f65cc8e787c7c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04c64586c9f1af23a0a6b4100c033305f624beb18ba002616237fa4798e80b4e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__771a14c8995cabc15f1a0318e36bff6b353e223262ad2f650ae4a56f490f78f9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9a67bf4e1875be096a395f9df1930064469ea5bf2f8f34f6c27318dee44ac13(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8d52daab49f97548feef3de24d91b02021803652af55b75fb811d4b29d9a5e4(
    value: typing.Optional[ContainerAwsNodePoolConfigRootVolume],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40e52343a801bf734b11f5192d5e6785a58e18350698bb7f247d61ed21e7c6eb(
    *,
    ec2_key_pair: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c999c5401efaad70419c5e42c5a0ed867f39b9c89d7560395cc10f3d48f7216(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e42a20b399c0be91460a400178e315cac0a9f6f817567b1fdf9447b003160d9a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1e4f53a13b8ab596c36928cb0fef196bbf1571fc91de138eb4de49f8864423a(
    value: typing.Optional[ContainerAwsNodePoolConfigSshConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb06d30fdf866d69edbe6adef18ad261070f9850079463f929d3349bd4d5d1aa(
    *,
    effect: builtins.str,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a27effe161c3280640f0db7ca5777fc84f5f448e80602a578b3d7f80fd6e2279(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__442715afe04ff3d24e4de10cba3d789a11245b054685711181f331618f1cdfc1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cd588ccae49ac37843e5c04011101b16384b2d7f735e32a9647ecb525bd5a22(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca5757088c7ce4ad21fea18b2f02b934b9ebd5397c585eca5c518f4f71d5ff42(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0d64a2236a3de8298f7c67e2ecf63c5b3eb884d11e857872db491c53cb3dee7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4d4c65f486eea79507789bebf7f4962dbcef5271cffc575d69bef913df49387(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAwsNodePoolConfigTaints]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a265acdd671124684979588f546bd593a0ced62ab85d502e10aacccd09fa302a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2efa028cc5143b2e91a6ae895184c64aaa66b0d9d54653a2d9fecff4e670e913(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5529b4d8c436190b8fcb7e40f1420235207e835cde11b231804274d1e5ab4b89(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dae53b5bae16f90269f31f031e9f7382e32db68800540ad5bc7d6d5d7e06714(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7293b211621a38fb5b08d6dea908512005a2e3e30fa30bb04e429d42cc287421(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAwsNodePoolConfigTaints]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f35bf4eeb5ee82688c0bf7f2170bdd4ab2b96b0b743e5598a513a5f41a52656(
    *,
    cpu_cfs_quota: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    cpu_cfs_quota_period: typing.Optional[builtins.str] = None,
    cpu_manager_policy: typing.Optional[builtins.str] = None,
    pod_pids_limit: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7ad81942418c80dd65aa5a39597af7acb7c24515c97ea95d841affa1a7abf4d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e4e0476cf692a10c7bd5788f86353e48191f5f0ee85cd728425e7a3f9981038(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2aec63e77377163de8e0af446a0d5d4cab87f5e6fb53652938c5c4255961c631(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__525f571ecd9e79f1eeb321ea0add2d443a12c4f4ef79d7dbde9f3b61fc4b01a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fea174dec0dc4c440762b5203b4d0015f3f20dad9441b229f75cce9fb0903516(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2aae1d5eb2af73686b966935a8af79f8f1ecba0c632619eb6161f5e60b9a3f30(
    value: typing.Optional[ContainerAwsNodePoolKubeletConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cad01253f11ea035595e73c4678cd759a57012b790cab724a4f27da04aaf629(
    *,
    auto_repair: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62fdafb8d5fa278a6983b1c0fc2a8ac865bb0d1e24de2df19b992a1a76a9b65d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a8b6fc90ca0b5e8c39e836b3bf6856243564d3526c024310a50ba8f79424c45(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02cc6d213315cecd4829794112a206f34fa83d4a6043bab8dc7076e5c657b30a(
    value: typing.Optional[ContainerAwsNodePoolManagement],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08b69280c5452cbf128a2fdb997b0b33521e8992f0ce51a096870c8d97abdf37(
    *,
    max_pods_per_node: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f176cf52faa43665bb9833836517122864819a64e784b565bd156ccb2902fee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b9c799f32b177069cf8a67b671b6301606fc60f1e739da9aaec974e6d3541e5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c089e815abdf00ee29b6209bf785014763acc1f58d182a5636f21541302b3390(
    value: typing.Optional[ContainerAwsNodePoolMaxPodsConstraint],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d409cd4dcb787c5523a4ee4e33cd697f86577c624f67924310249fdd2366d0da(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c3620a7f4fdd0d2e4e5e9bd44058faa176c7a6e0d17990cbbdab5524e316b9f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19aaef48b8255e8878f8476d29b2a719a4eb1fb31c4c7a99c3044f82d56b85b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d923ad6d711fd18092c9c0012fd7790ab37b88cf5e834205186cfc9a0e173f7f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9bfbc834edd71b343894bca2242125d78c3907322abfaa11930eb5cd2ae4a42(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37ea1ec61dd40c30ad7125049a11b755eb5e3ce7c6f39a56ba6482f52c08fbe3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAwsNodePoolTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d86d75b65d3f7097ce493ee1d820410489aea30032b8ce645c46e4d312765294(
    *,
    surge_settings: typing.Optional[typing.Union[ContainerAwsNodePoolUpdateSettingsSurgeSettings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ba2b030e1095d9ec18371d7b7e484d2e7c013ada3fc1ff9e14c1a375aa58084(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ad7dbe743b5777398ce7c27c276a5d63a61d5495ce3078d3ec8600bac5bb00c(
    value: typing.Optional[ContainerAwsNodePoolUpdateSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41703609ab0578e2de458a89e4a7e6834ded317c335d2c7e6398b4567cb1d4ae(
    *,
    max_surge: typing.Optional[jsii.Number] = None,
    max_unavailable: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18125689e51741fdb2c433361295259b212102b458b18fdd250375a722072715(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59fc3873e53f9fd9be1349ded263591cb3eae05d1daf92f4da02fe04f45facf1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3743dc3459c5bdac1ccf017eb68ede31972f29ae0499c1329d415ed38549d92(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8baabb3cfb9f40f50ea106d93060ee7188610880fc65440654760df838b2352e(
    value: typing.Optional[ContainerAwsNodePoolUpdateSettingsSurgeSettings],
) -> None:
    """Type checking stubs"""
    pass
